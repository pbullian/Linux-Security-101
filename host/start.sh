#!/bin/sh
set -e
rsyslogd
# initialize a permissive nftables base so container is reachable
if ! nft list tables | grep -q '^table inet filter'; then
  nft add table inet filter
  nft add chain inet filter input '{ type filter hook input priority 0; policy accept; }'
fi
service fail2ban start || true
exec /usr/sbin/sshd -D -e
