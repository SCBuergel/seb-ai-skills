#!/usr/bin/env python3
"""Connect to every destination in turn: exit IP, a short download, 10 pings, disconnect.

Usage (on the server, as root, guards on, under tmux): exit-sweep.py > exits.log
Prints one JSON line per exit, then "final state: none" once the tunnel is down.
Env: SIZE_MIB (25), URL (a file of at least SIZE_MIB; fetched with a byte range)."""
import json, os, re, signal, subprocess, time

URL = os.environ.get("URL", "https://fsn1-speed.hetzner.com/100MB.bin")
SIZE = int(os.environ.get("SIZE_MIB", "25")) * 2**20


def sh(argv, timeout):
    try:
        return subprocess.run(argv, capture_output=True, text=True, timeout=timeout).stdout
    except subprocess.TimeoutExpired:
        return ""


def status():
    try:
        return json.loads(sh(["gnosis_vpn-ctl", "-o", "json", "status"], 30))["Status"]
    except Exception:
        return {}


def state(s):
    for k in ("connected", "connecting", "reconnecting", "disconnecting"):
        if s.get(k):
            return k, s[k]
    return "none", None


def disconnect():
    sh(["gnosis_vpn-ctl", "disconnect"], 30)
    for _ in range(30):
        if state(status())[0] == "none":
            return True
        time.sleep(1)
    return False


def on_sig(*_):
    raise SystemExit(1)


signal.signal(signal.SIGTERM, on_sig)
signal.signal(signal.SIGHUP, on_sig)
try:
    sh(["gnosis_vpn-ctl", "start-client", "60m"], 30)
    dests = [d["destination"] for d in status().get("destinations", [])]
    for d in dests:
        r = {"exit": d["id"], "location": d.get("meta", {}).get("location")}
        sh(["gnosis_vpn-ctl", "connect", d["id"]], 30)
        t0 = time.time()
        while True:
            st, v = state(status())
            if st == "connected":  # the previous exit was disconnected first, so this is d
                r["connect_s"] = round(time.time() - t0, 1)
                break
            if time.time() - t0 > 180:
                r["error"] = "connect timeout (state %s)" % st
                break
            time.sleep(1)
        if "connect_s" in r:
            r["exit_ip"] = sh(["curl", "-s", "--max-time", "20", "https://ifconfig.me"], 25).strip()
            out = sh(["curl", "-s", "-o", "/dev/null", "--max-time", "120", "-r", "0-%d" % (SIZE - 1),
                      "-w", "%{http_code} %{size_download} %{time_total}", URL], 130).split()
            if len(out) == 3 and int(out[1]) > 0:
                r["dl_bytes"], r["dl_s"] = int(out[1]), float(out[2])
                r["dl_mbit_s"] = round(int(out[1]) * 8 / 1e6 / float(out[2]), 2)
                r["dl_complete"] = int(out[1]) == SIZE
            else:
                r["dl_error"] = " ".join(out) or "curl timeout"
            p = sh(["ping", "-c", "10", "-i", "1", "-W", "3", "1.1.1.1"], 45)
            m = re.search(r"(\d+)% packet loss", p)
            r["ping_loss_pct"] = int(m.group(1)) if m else None
            m = re.search(r"= ([\d.]+)/([\d.]+)/([\d.]+)", p)
            if m:
                r["ping_min_ms"], r["ping_avg_ms"], r["ping_max_ms"] = (float(x) for x in m.groups())
        r["disconnected"] = disconnect()
        print(json.dumps(r), flush=True)
finally:
    disconnect()
    print("final state:", state(status())[0], flush=True)
