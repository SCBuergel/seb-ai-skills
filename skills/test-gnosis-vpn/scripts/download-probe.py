#!/usr/bin/env python3
"""One download through the Gnosis VPN tunnel, sampled once per second, written as CSV.

Row per second: wall time, elapsed, bytes received by the HTTP reader that second and in total,
download rate (app level and tunnel-interface rx), ping RTT to PING_TARGET for the echo sent in that
second (empty + ping_lost=1 when no reply), and the client connection state (polled every 15 s,
which also resets the worker keep-alive, so a transfer longer than the keep-alive is not cut).

Usage (on the server, as root, guards on, under tmux): download-probe.py OUT.csv DESTINATION [URL]
Connects to DESTINATION, waits for connected, runs the transfer, always disconnects.
Env: PING_TARGET (1.1.1.1), MAX_S (5400, hard cap on the transfer)."""
import csv, json, os, re, signal, subprocess, sys, threading, time, urllib.request

OUT, DEST = sys.argv[1], sys.argv[2]
URL = sys.argv[3] if len(sys.argv) > 3 else "https://fsn1-speed.hetzner.com/1GB.bin"
PING_TARGET = os.environ.get("PING_TARGET", "1.1.1.1")
MAX_S = int(os.environ.get("MAX_S", "5400"))
IFACE = "wg0_gnosisvpn"


def ctl(*a, timeout=30):
    return subprocess.run(["gnosis_vpn-ctl", *a], capture_output=True, text=True, timeout=timeout).stdout


def status():
    try:
        return json.loads(ctl("-o", "json", "status"))["Status"]
    except Exception:
        return {}


def conn_state(s):
    for k in ("connected", "connecting", "reconnecting", "disconnecting"):
        v = s.get(k)
        if v:
            return k
    return "none"


def teardown():
    ctl("disconnect")
    for _ in range(20):
        s = status()
        if conn_state(s) == "none":
            return
        time.sleep(1)
    ctl("stop-client")


def on_sig(*_):
    raise SystemExit(1)


signal.signal(signal.SIGTERM, on_sig)
signal.signal(signal.SIGHUP, on_sig)

total = 0
done = threading.Event()
err = []


def reader():
    global total
    try:
        with urllib.request.urlopen(URL, timeout=60) as r:
            while True:
                b = r.read(65536)
                if not b:
                    break
                total += len(b)
    except Exception as e:
        err.append(repr(e))
    done.set()


def rx():
    try:
        return int(open(f"/sys/class/net/{IFACE}/statistics/rx_bytes").read())
    except Exception:
        return None


try:
    ctl("start-client", "3h")
    ctl("connect", DEST)
    t0 = time.time()
    while conn_state(status()) != "connected":
        if time.time() - t0 > 180:
            raise SystemExit("connect timeout")
        time.sleep(1)
    print(f"connected after {time.time()-t0:.1f}s", flush=True)
    print("exit ip:", subprocess.run(["curl", "-s", "--max-time", "15", "https://ifconfig.me"],
                                     capture_output=True, text=True).stdout, flush=True)

    rtt = {}  # icmp_seq -> rtt ms
    ping = subprocess.Popen(["ping", "-n", "-i", "1", "-W", "3", PING_TARGET], stdout=subprocess.PIPE, text=True)

    def ping_reader():
        for line in ping.stdout:
            m = re.search(r"icmp_seq=(\d+).*time=([\d.]+)", line)
            if m:
                rtt[int(m.group(1))] = float(m.group(2))

    threading.Thread(target=ping_reader, daemon=True).start()
    start = time.time()
    threading.Thread(target=reader, daemon=True).start()

    rows, last_total, last_rx, state, k = [], 0, rx(), "connected", 0
    while True:
        k += 1
        time.sleep(max(0, start + k - time.time()))
        cur, cur_rx = total, rx()
        if k % 15 == 0:
            state = conn_state(status())
        rows.append([time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), k, cur - last_total, cur,
                     round((cur - last_total) * 8 / 1e6, 3),
                     round((cur_rx - last_rx) * 8 / 1e6, 3) if cur_rx is not None and last_rx is not None else "",
                     state])
        last_total, last_rx = cur, cur_rx
        if k % 30 == 0:
            print(f"{k}s {cur/2**20:.0f} MiB state={state}", flush=True)
        if done.is_set() or k >= MAX_S:
            break
    time.sleep(4)  # let the last pings come back
    ping.terminate()
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["utc_time", "elapsed_s", "bytes_this_second", "bytes_total", "download_mbit_s",
                    "tunnel_rx_mbit_s", "ping_ms", "ping_lost", "connection_state"])
        for r in rows:
            p = rtt.get(r[1])  # echo seq N is sent ~N-1 s after start, i.e. during second N
            w.writerow(r[:6] + ["" if p is None else p, 0 if p is not None else 1, r[6]])
    el = rows[-1][1] if rows else 0
    print(f"done={done.is_set()} bytes={total} seconds={el} avg_mbit={total*8/1e6/max(el,1):.2f} err={err}", flush=True)
finally:
    teardown()
    print("disconnected; final state:", conn_state(status()), flush=True)
