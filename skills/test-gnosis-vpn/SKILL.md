---
name: test-gnosis-vpn
description: Install, fund and test the latest Gnosis VPN client on a remote Linux server over SSH without locking yourself out. Use when asked to deploy, upgrade, fund (faucet codes), or exercise Gnosis VPN on a server, or when a tool that drives gnosis_vpn-ctl needs re-validating against a new client version.
---

# Testing Gnosis VPN on a remote server

The server address comes from the user each time. Never write it into files, commits or memory.

## 0. Golden rule: connecting the VPN kills your SSH session

When a tunnel comes up, the client:
- adds `0.0.0.0/1` + `128.0.0.0/1` via the TUN, so everything except HOPR peer IPs and RFC1918 goes into the tunnel, and
- installs a **killswitch**: nftables table `inet gnosis_vpn_ks` with default-drop `input`/`output`/`forward` chains. It allows only loopback, DHCP/NDP, the tunnel interface, HOPR peers and (unless `lan_lockdown`) private ranges.

So SSH from a public IP dies, and a route pin alone is NOT enough. The client re-applies the table atomically (add/del/add) whenever peers change, so a one-shot `nft insert` gets wiped. `GNOSISVPN_FORCE_STATIC_ROUTING` in old env files does nothing any more.

**Before the first `connect`, always install both guards** (scripts next to this file):

1. `scripts/ssh-keeper.sh MYIP WAN_GW WAN_DEV`: every second, it pins `MYIP/32` via the WAN gateway and re-inserts `ip saddr/daddr MYIP accept` into the killswitch chains when missing.
2. `scripts/deadman.sh`: watches `/run/gvpn-deadman.alive`. If stale for more than 6 min, it disconnects, stops the worker and deletes the killswitch table. If stale for more than 12 min, it reboots once. `/run` is cleared on boot, so it can't loop.

```bash
MYIP=$(curl -s -4 https://ifconfig.me)                  # locally
ssh root@HOST 'ip route show default'                    # -> WAN_GW, WAN_DEV
scp scripts/*.sh root@HOST:/root/gvpn-guard/            # or: tar c | ssh tar x (rsync may be missing)
ssh root@HOST 'chmod +x /root/gvpn-guard/*.sh;
  systemd-run --unit=gvpn-ssh-keeper /root/gvpn-guard/ssh-keeper.sh MYIP WAN_GW WAN_DEV;
  systemd-run --unit=gvpn-deadman   /root/gvpn-guard/deadman.sh'
```
Use transient `systemd-run` units, so a reboot leaves nothing behind. Then keep a **local heartbeat** running in the background for the whole session:
```bash
while true; do timeout 20 ssh -o ConnectTimeout=10 root@HOST 'touch /run/gvpn-deadman.alive' && echo "$(date +%T) ok" || echo "$(date +%T) FAIL"; sleep 60; done
```
Test the guards with one manual connect, polling SSH every ~10 s. `journalctl -u gvpn-ssh-keeper` should show "inserted killswitch allow".

Run anything long under `tmux new -d -s NAME "cmd > log 2>&1"` on the server, then poll the log file.

**Teardown order matters:** first disconnect, then `systemctl stop gvpn-deadman gvpn-ssh-keeper`, and only then stop the local heartbeat. Otherwise the deadman reboots the box. When killing the heartbeat with `pkill -f`, use a pattern that does not match your own shell command, or you kill yourself (exit 144).

If you are locked out anyway, the user must reboot the droplet or run `gnosis_vpn-ctl disconnect` from the provider console. After a reboot the worker comes up idle, so SSH works again.

## 1. Survey the server first

```bash
systemctl list-units --type=service --state=running; docker ps -a; ss -tlnp
dpkg -l gnosisvpn; gnosis_vpn-ctl --version; ls /etc/gnosisvpn; systemctl is-enabled gnosisvpn
```
HOPR relays usually run as `hoprd` docker containers. Stop only what the user said to stop. Note the existing config: `/etc/gnosisvpn/config.toml` and `gnosisvpn-dynamic.env`, where `GNOSISVPN_HOPR_BLOKLI_URL` shows the network, e.g. `blokli-jura.prod.hoprnet.link` means jura-prod.

## 2. Find and install the latest version

The download page `https://download.vpn.gnosis.eth.limo/` is a JS SPA, so the links live in `assets/index-*.js`:
```bash
curl -sL https://download.vpn.gnosis.eth.limo/ | grep -o 'assets/index-[^"]*\.js'
curl -sL https://download.vpn.gnosis.eth.limo/assets/<that>.js | grep -oE 'https?://[^"`]+' | sort -u
```
The authoritative source is the APT index:
```bash
curl -fsSL https://download.vpn.gnosis.eth.limo/linux/apt/dists/stable/main/binary-amd64/Packages | grep -E '^(Version|Filename)'
```
Install or upgrade with the official script. It sets up the keyring and apt source and handles channel downgrades:
```bash
curl -fsSL https://download.vpn.gnosis.eth.limo/linux/install.sh | bash
# options: --channel=stable|snapshot|experimental  --network=<name>  --reset-identity
```
- The **package** version (e.g. 0.95.2) differs from the **client** version that `gnosis_vpn-ctl --version` and `info` report (e.g. 0.96.3). Report both.
- Config is kept (dpkg confold) and backed up as `config.toml.backup.<ts>`. Node identity is kept unless `--reset-identity`, so an old node may already be funded.
- The service is enabled and running after install, but the **worker is idle** ("Worker offline").

## 3. Drive the client (gnosis_vpn-ctl)

Always check `gnosis_vpn-ctl --help` first. The CLI changes between versions. As of 0.96:
```bash
gnosis_vpn-ctl start-client 30m      # required; keep-alive resets on each command (not info/ping/stop-client)
gnosis_vpn-ctl -o json status        # global -o plain|json|yaml  (old --json flag is gone)
gnosis_vpn-ctl -o json balance       # node/safe balances, info.node_address, funding_status
gnosis_vpn-ctl connect <DestinationId>   # e.g. Austria, returns before the tunnel is up
gnosis_vpn-ctl disconnect
gnosis_vpn-ctl info | nerd-stats | telemetry | check-update | stop-client
```
Use a short keep-alive such as `30m`, never days. If you lose access, the worker then stops by itself and takes the tunnel down.

Detecting an idle worker: `-o json status` still exits **0** and returns destinations, with `run_mode: "NotRunning"`. Don't rely on exit codes for this. After `start-client`, poll until `run_mode` is `Running`; it goes NotRunning → Warmup → Running in about 5 s. Exit code `69` (EX_UNAVAILABLE) shows up for worker-only commands while offline, and `76` means disconnect while not connected (harmless).

Any tool that connects on a remote host must tear the tunnel down on every exit path: try/finally, plus a SIGTERM/SIGHUP handler that raises SystemExit. It should then verify `connected/connecting/reconnecting/disconnecting` are all empty, and fall back to `stop-client` if not. A disconnect also removes the killswitch table.

JSON status (`.Status`): `run_mode` (`Running`/`Warmup`/`PreparingSafe`/`NotRunning` …), `destinations[].destination.{id,address(hex string),meta.{location,flag}}` plus `route_health`, and `connecting` / `reconnecting` / `connected` / `disconnecting[]`, each carrying `destination_id`. Poll until `connected.destination_id` matches; this takes about 7-10 s when healthy. Verify the tunnel with `curl -s https://ifconfig.me`, which should no longer show the server IP.

When behaviour is unclear, read the source instead of guessing (`git clone --depth 50 https://github.com/gnosis/gnosis_vpn-client`):
- `gnosis_vpn-lib/src/command/mod.rs`: status and response types
- `gnosis_vpn-ctl/src/cli.rs`: CLI
- `gnosis_vpn-lib/src/killswitch/`: firewall
- `gnosis_vpn-root/src/routing/linux.rs`: routes

## 4. Fund via faucet codes

The faucet `https://faucet.vpn.gnosis.eth.limo/` is also an SPA. The API is a single POST, found in its `assets/index-*.js` (re-grep for `fetch(` if it has moved):
```bash
curl -sS -X POST https://cfp-funding-api-656686060169.europe-west1.run.app/api/cfp-funding-tool/airdrop \
  -H 'Content-Type: application/json' \
  -d '{"address":"<NODE_ADDRESS>","code":"<SECRET CODE>"}'
```
- The address is the **node address**, i.e. "Gnosis VPN Address" in the UI, from `balance` → `info.node_address`. It is not the safe address.
- Success looks like `{"success":true,"message":"Successfully sent 0.005 xDAI and 241.01 wxHOPR ..."}`. Errors come back in `.error`.
- Codes are single-use. Never write codes into files or memory.
- `gnosis_vpn-ctl funding-tool <SECRET>` is the in-client alternative during onboarding.

Afterwards, check `balance`: `funding_status.traffic/gas` should be `Good` and the deficits `null`.

## 5. Test plan

1. Status is `Ready (Node is running)`, and the destinations list is populated with route health `ReadyToConnect`.
2. Connect to one exit (with guards on), wait for `connected`, check the exit IP, and run a small download (`https://speed.cloudflare.com/__down?bytes=10485760`) and a ping.
3. Disconnect and confirm `connected: null` and that the killswitch table is gone (`nft list tables`).
4. For tools driving the client: run each of their commands once, briefly. Use a scratch copy with shortened gaps and exit counts instead of full multi-hour runs. Treat a stalled transfer that hits its timeout as a VPN observation, not a tool bug.
5. Clean up in the teardown order from section 0, and report package and client versions, funding result, and per-command pass/fail.
