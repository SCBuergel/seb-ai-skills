---
name: test-gnosis-vpn
description: Install, fund and test the latest Gnosis VPN client on a remote Linux server over SSH without locking yourself out. Use when asked to deploy, upgrade, fund (faucet codes or a direct wxHOPR transfer), measure (download speed and ping per second, or a quick check of every exit), or exercise Gnosis VPN on a server, including a throwaway cloud VM that is created for the test and destroyed afterwards with its funds returned, or when a tool that drives gnosis_vpn-ctl needs re-validating against a new client version.
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
ssh root@HOST 'chmod +x /root/gvpn-guard/*.sh; touch /run/gvpn-deadman.alive;
  systemctl reset-failed gvpn-ssh-keeper gvpn-deadman 2>/dev/null;
  systemd-run --unit=gvpn-ssh-keeper /root/gvpn-guard/ssh-keeper.sh MYIP WAN_GW WAN_DEV;
  systemd-run --unit=gvpn-deadman   /root/gvpn-guard/deadman.sh'
```
Use transient `systemd-run` units, so a reboot leaves nothing behind. The `reset-failed` lets you start the guards again on a host where they ran before. Then keep a **local heartbeat** running in the background for the whole session:
```bash
while true; do timeout 20 ssh -o ConnectTimeout=10 root@HOST 'touch /run/gvpn-deadman.alive' && echo "$(date +%T) ok" || echo "$(date +%T) FAIL"; sleep 60; done
```
Test the guards with one manual connect, polling SSH every ~10 s. `journalctl -u gvpn-ssh-keeper` should show "inserted killswitch allow".

Run anything long under `tmux new -d -s NAME "cmd > log 2>&1"` on the server, then poll the log file.

**Teardown order matters:** first disconnect, then `systemctl stop gvpn-deadman gvpn-ssh-keeper`, and only then stop the local heartbeat. Otherwise the deadman reboots the box. When killing the heartbeat with `pkill -f`, use a pattern that does not match your own shell command, or you kill yourself (exit 144).

If you are locked out anyway, the user must reboot the droplet or run `gnosis_vpn-ctl disconnect` from the provider console. After a reboot the worker comes up idle, so SSH works again.

## 1. Get a server

If the user names a server, survey it first:
```bash
systemctl list-units --type=service --state=running; docker ps -a; ss -tlnp
dpkg -l gnosisvpn; gnosis_vpn-ctl --version; ls /etc/gnosisvpn; systemctl is-enabled gnosisvpn
```
HOPR relays usually run as `hoprd` docker containers. Stop only what the user said to stop. Note the existing config: `/etc/gnosisvpn/config.toml` and `gnosisvpn-dynamic.env`, where `GNOSISVPN_HOPR_BLOKLI_URL` shows the network, e.g. `blokli-jura.prod.hoprnet.link` means jura-prod.

If the user asks for a new VM, create a throwaway one and destroy it at the end (section 6). On DigitalOcean, use the API directly; a one-off test needs no fleet tooling:
- Read the API token from a file the user points to and send it only to `api.digitalocean.com`. Never print it.
- List the sizes that fit before choosing: `GET /v2/sizes?per_page=200`, filtered on `vcpus`, `available` and the wanted region in `regions`. Regions differ a lot: on 2026-10-05, fra1 offered only shared-CPU `s-8vcpu-*` at 8 vCPUs, while lon1 also had dedicated `c-8`/`g-8vcpu-32gb`. Pick the region closest to the exit under test, and say so if you deviate from what the user asked for.
- Use image `ubuntu-24-04-x64`; the client needs a recent glibc.
- An account SSH key may be missing, or the token may lack the scope to read keys. Pass the public key in `user_data` instead. Without an account key, DigitalOcean expires root's password, and sshd then refuses even key logins until the password is changed, so unexpire it first:
  ```bash
  #!/bin/bash
  chage -d "$(date +%F)" -M 99999 root
  install -d -m 700 /root/.ssh; echo 'PUBKEY' >> /root/.ssh/authorized_keys; chmod 600 /root/.ssh/authorized_keys
  export DEBIAN_FRONTEND=noninteractive
  for i in $(seq 1 60); do apt-get update -qq && break; sleep 5; done
  apt-get install -y -qq jq curl tmux iputils-ping nftables; touch /var/lib/gvpn-ready
  ```
- `POST /v2/droplets` with `name`, `region`, `size`, `image`, `user_data`. Poll `GET /v2/droplets/ID` until `status` is `active`, take the public v4 address, then poll SSH until `/var/lib/gvpn-ready` exists. This takes about 1-2 min. If the user keeps their test machines in a DO project, assign the droplet there: `POST /v2/projects/PID/resources` with `{"resources":["do:droplet:ID"]}`.
- Use `-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null` for a throwaway host, so a recycled IP does not trip known_hosts.

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
Use a short keep-alive such as `30m`, never days. If you lose access, the worker then stops by itself and takes the tunnel down. Only commands reset the keep-alive; tunnel traffic does not. So a transfer that runs longer than the keep-alive is cut when the worker stops. For a long measurement, start the worker with a keep-alive longer than the test, and send `status` periodically while it runs (`scripts/download-probe.py` does both).

Detecting an idle worker: `-o json status` still exits **0** and returns destinations, with `run_mode: "NotRunning"`. Don't rely on exit codes for this. After `start-client`, poll until `run_mode` is `Running`. On a funded node it goes NotRunning → Warmup → Running in about 5 s. On a fresh identity it goes through `PreparingSafe` (waiting for funds, section 4) and `DeployingSafe` first. Exit code `69` (EX_UNAVAILABLE) shows up for worker-only commands while offline, and `76` means disconnect while not connected (harmless).

Any tool that connects on a remote host must tear the tunnel down on every exit path: try/finally, plus a SIGTERM/SIGHUP handler that raises SystemExit. It should then verify `connected/connecting/reconnecting/disconnecting` are all empty, and fall back to `stop-client` if not. A disconnect also removes the killswitch table.

JSON status (`.Status`): `run_mode` (`Running`/`Warmup`/`PreparingSafe`/`DeployingSafe`/`NotRunning` …), `destinations[].destination.{id,address(hex string),meta.{location,flag}}` plus `route_health`, and `connecting` / `reconnecting` / `connected` / `disconnecting[]`, each carrying `destination_id`. Poll until `connected.destination_id` matches. Verify the tunnel with `curl -s https://ifconfig.me`, which should no longer show the server IP.

How long a connect takes depends on the node's channels:
- A node with its channels open connects in about 7-10 s when healthy.
- A fresh node has no channels. Its destinations show route health `NeedsPeering`, then `NeedsChannel`, and stay there until you connect, so do not wait for `ReadyToConnect` before the first connect. That connect opens the channels on-chain and took 30-75 s on 0.96.3. Allow at least 180 s before calling it a timeout.

When behaviour is unclear, read the source instead of guessing (`git clone --depth 50 https://github.com/gnosis/gnosis_vpn-client`):
- `gnosis_vpn-lib/src/command/mod.rs`: status and response types
- `gnosis_vpn-ctl/src/cli.rs`: CLI
- `gnosis_vpn-lib/src/killswitch/`: firewall
- `gnosis_vpn-root/src/routing/linux.rs`: routes

## 4. Fund the node

The address to fund is the **node address**, i.e. "Gnosis VPN Address" in the UI. It is not the safe address. While the worker is in `PreparingSafe`, read it from `status` → `PreparingSafe.node_address`, together with `balance_recommendation` (how much wxHOPR to send). `balance` returns "balance data not yet available" at this stage. Once the node is running, it is in `balance` → `info.node_address`.

There are two ways to fund. Ask the user which one, unless they or your memory already name a source.

**Faucet code.** The faucet `https://faucet.vpn.gnosis.eth.limo/` is also an SPA. The API is a single POST, found in its `assets/index-*.js` (re-grep for `fetch(` if it has moved):
```bash
curl -sS -X POST https://cfp-funding-api-656686060169.europe-west1.run.app/api/cfp-funding-tool/airdrop \
  -H 'Content-Type: application/json' \
  -d '{"address":"<NODE_ADDRESS>","code":"<SECRET CODE>"}'
```
- Success looks like `{"success":true,"message":"Successfully sent 0.005 xDAI and 241.01 wxHOPR ..."}`. Errors come back in `.error`.
- Codes are single-use. Never write codes into files or memory. A user may keep a code file plus a ledger of used codes. Mark a code as used only when the faucet actually judged it (success, or "The code has no uses left"), never on `Rate limit exceeded`.
- Codes in a stockpile go stale: "The code has no uses left" is common, and every code in a 15-code file came back that way. After about 10 claims in quick succession the faucet answers `Rate limit exceeded` for about a minute. If several codes in a row are spent, stop and ask the user for fresh codes or a direct transfer, rather than burning through the file.
- `gnosis_vpn-ctl funding-tool <SECRET>` is the in-client alternative during onboarding.

**Direct transfer.** No faucet is needed. Send at least `balance_recommendation.wxhopr` (241 wxHOPR on 0.96.3) and 0.005 xDai to the node address on Gnosis Chain. Any account the user controls can be the source. Simulate first and send only what the user agreed to. The client sees the funds, deploys its own Safe and moves the wxHOPR into it. It reached `Running` about 2 min after the transfer. wxHOPR is `0xD4fdec44DB9D44B8f2b6d529620f9C0C7066A2c1`; the public RPC `https://rpc.gnosischain.com` works.

Afterwards, check `balance`: `funding_status.traffic/gas` should be `Good` and the deficits `null`. `capacity_allocations.safe.byte_capacity` shows roughly how much traffic the stake covers (about 8.5 GB for 249 wxHOPR).

## 5. Test plan

1. Status is `Ready (Node is running)`, and the destinations list is populated. On a node that has connected before, route health is `ReadyToConnect`; on a fresh one it is `NeedsChannel` (section 3).
2. Connect to one exit (with guards on), wait for `connected`, check the exit IP, and run a small download and a ping.
3. Disconnect and confirm `connected: null` and that the killswitch table is gone (`nft list tables`).
4. For tools driving the client: run each of their commands once, briefly. Use a scratch copy with shortened gaps and exit counts instead of full multi-hour runs. Treat a stalled transfer that hits its timeout as a VPN observation, not a tool bug.
5. Clean up in the teardown order from section 0, and report package and client versions, funding result, and per-command pass/fail.

**Download sources.** `speed.cloudflare.com/__down` answered 403 from a DigitalOcean droplet, even for 100 MB. Hetzner's `https://fsn1-speed.hetzner.com/{100MB,1GB,10GB}.bin` works (also `nbg1-`, `hel1-`, `ash-`, `hil-`), and `curl -r 0-N` cuts any size. Check the source without the VPN first: from a DO droplet in fra1 it delivered about 1.9 Gbit/s, so the server is never the bottleneck.

**Measurement scripts** (copy them to the server next to the guards; run them as root under tmux, with the guards and heartbeat on; both always disconnect on exit):
- `scripts/download-probe.py OUT.csv DESTINATION [URL]`: one download (default 1 GiB from Hetzner), and a CSV row per second with download Mbit/s (app level and tunnel interface), ping RTT and loss to `PING_TARGET`, and connection state. It prints progress every 30 s and a summary at the end. Use this when the user wants speed and ping over time.
- `scripts/exit-sweep.py > exits.log`: for every destination, it connects, reads the exit IP, downloads `SIZE_MIB` (25), sends 10 pings and disconnects. It prints one JSON line per exit. Use this for "check every exit".

What to expect, as of 0.96.3 on jura-prod from fra1:
- The first ~30 s of a session run at about 2 Mbit/s while it ramps up. Short downloads therefore read lower than long ones: Austria gave 6.8 Mbit/s for 25 MiB against 8.2 Mbit/s for 1 GiB.
- A 1 GiB transfer took 17 min.
- Ping through the tunnel has a median in the hundreds of ms, even for a nearby exit, with rare multi-second outliers.

## 6. Return funds and destroy a throwaway VM

When the user asks to send the funds back or to delete the machine, do it in this order:

1. **Disconnect, then stop and mask the service:** `gnosis_vpn-ctl stop-client; systemctl stop gnosisvpn; systemctl mask gnosisvpn`. A running node can re-fund its channels from the Safe while you drain it. Then stop the guards, and only then the heartbeat (section 0).
2. **Back up the identity locally**, before anything is deleted: `/var/lib/gnosisvpn/.config/gnosisvpn-hopr.{id,pass,safe}`, into a mode-700 directory. The Safe is controlled only by this key; lose the key and you lose the funds.
3. **Drain the Safe.** After use, part of the wxHOPR sits in outgoing payment channels (8 channels with 110 wxHOPR after one exit sweep), not in the Safe. The identity's `chain_key` is the sole owner (threshold 1) of the Safe. Each step is a Safe `execTransaction` sent from the node address, with the pre-validated signature `r = owner, s = 0, v = 1`, and the node's xDai pays the gas:
   - `HoprChannels.initiateOutgoingChannelClosureSafe(node, dest)` for every OPEN channel. HoprChannels is `0x860f50B24Ba6A862736c5045747323e03aa52Aa4`; list the channels via blokli or the contract.
   - Wait out the notice period (300 s on jura; read it from the contract). Then call `finalizeOutgoingChannelClosureSafe(node, dest)`, leaving a couple of blocks of margin after `closureTime`.
   - Call `wxHOPR.transfer(dest, safeBalance)`, and send the node's leftover xDai minus about 0.002 for gas.
   - The keystore is scrypt + aes-128-ctr around JSON with `chain_key`; the password is in `.pass`. Sign with `cast mktx` and never echo the key. If the user has a sweep tool for this, prefer it, and point it at the local identity copy instead of SSH.
   - Expect a little less back than was sent; the traffic is paid for. 11 of 250 wxHOPR went on 1 GiB plus an 8-exit sweep.
4. **Verify on-chain** that the node's Safe holds 0 wxHOPR and the destination received the funds.
5. **Destroy the VM:** `DELETE /v2/droplets/ID` (204). Then list the droplets to confirm it is gone and that nothing else was touched.
