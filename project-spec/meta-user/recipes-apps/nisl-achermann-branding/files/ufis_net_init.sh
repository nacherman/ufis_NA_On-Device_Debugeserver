#!/bin/sh

NET_IF="${UFIS_NET_IF:-}"
FALLBACK_IP="${UFIS_STATIC_IP:-192.168.2.50/24}"

if [ -z "$NET_IF" ]; then
    NET_IF=$(ip -o link show | awk -F': ' '{print $2}' | cut -d@ -f1 | grep -Ev '^(lo|sit0)$' | head -n 1)
fi

if [ -z "$NET_IF" ] || ! ip link show "$NET_IF" >/dev/null 2>&1; then
    exit 0
fi

ip link set "$NET_IF" up >/dev/null 2>&1 || true

if ip -4 -o addr show dev "$NET_IF" | grep -q 'inet '; then
    exit 0
fi

if command -v udhcpc >/dev/null 2>&1; then
    udhcpc -i "$NET_IF" -n -q >/dev/null 2>&1 || true
fi

if ip -4 -o addr show dev "$NET_IF" | grep -q 'inet '; then
    exit 0
fi

ip addr flush dev "$NET_IF" >/dev/null 2>&1 || true
ip addr add "$FALLBACK_IP" dev "$NET_IF" >/dev/null 2>&1 || true
