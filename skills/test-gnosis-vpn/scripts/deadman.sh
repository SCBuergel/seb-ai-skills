#!/bin/bash
# Operator heartbeat watchdog for remote Gnosis VPN tests.
# Stale > SOFT: tear the VPN down. Stale > HARD: reboot once (/run is cleared on boot).
HB=/run/gvpn-deadman.alive; SOFT=${SOFT:-360}; HARD=${HARD:-720}; fired=0
touch $HB
while true; do
  age=$(( $(date +%s) - $(stat -c %Y $HB 2>/dev/null || date +%s) ))
  if [ $age -gt $HARD ]; then
    echo "$(date -Is) heartbeat ${age}s stale, rebooting"; sync; systemctl reboot; sleep 600
  elif [ $age -gt $SOFT ] && [ $fired -eq 0 ]; then
    echo "$(date -Is) heartbeat ${age}s stale, tearing VPN down"
    timeout 30 gnosis_vpn-ctl disconnect; timeout 30 gnosis_vpn-ctl stop-client
    sleep 5; for fam in inet ip ip6; do nft delete table $fam gnosis_vpn_ks 2>/dev/null; done
    fired=1
  elif [ $age -le $SOFT ]; then fired=0
  fi
  sleep 10
done
