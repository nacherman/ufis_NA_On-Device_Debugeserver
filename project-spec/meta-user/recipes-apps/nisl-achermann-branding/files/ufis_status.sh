#!/bin/sh
NET_IF="${UFIS_NET_IF:-}"

if [ -z "$NET_IF" ]; then
    NET_IF=$(ip -o link show | awk -F': ' '{print $2}' | cut -d@ -f1 | grep -Ev '^(lo|sit0)$' | head -n 1)
fi

echo "--- UFIS-NA System Status ---"
echo "Hostname: $(hostname)"
echo "Uptime:   $(uptime -p)"
echo "Date:     $(date)"
echo ""
echo "--- FPGA Status ---"
if [ -d /sys/class/fpga_manager/fpga0 ]; then
    STATE=$(cat /sys/class/fpga_manager/fpga0/state)
    echo "FPGA Manager State: $STATE"
else
    echo "FPGA Manager not found in /sys/class/fpga_manager/fpga0"
fi
echo ""
echo "--- Network Status ---"
if [ -n "$NET_IF" ] && ip link show "$NET_IF" >/dev/null 2>&1; then
    echo "Interface: $NET_IF"
    IP4_ADDR=$(ip -4 -o addr show dev "$NET_IF" | awk '{print $4}' | cut -d/ -f1 | head -n 1)
    if [ -n "$IP4_ADDR" ]; then
        echo "IP Address: $IP4_ADDR"
    else
        echo "IP Address: (none)"
    fi
    if [ -f /usr/sbin/ethtool ]; then
        ethtool "$NET_IF" | grep "Link detected"
    fi
else
    echo "No active non-loopback interface found."
fi
echo ""
echo "--- Memory Usage ---"
free -h
echo "-----------------------------"
