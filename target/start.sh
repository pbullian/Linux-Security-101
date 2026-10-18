#!/bin/sh
set -eu
mkdir -p /run/sshd /run/fail2ban /var/spool/rsyslog /artifacts
ssh-keygen -A
# The previous rsyslog process ended with the container; its pidfile can remain.
touch /var/log/auth.log /var/log/syslog /var/log/http-access.log
chown root:adm /var/log/auth.log /var/log/syslog /var/log/http-access.log
chmod 0640 /var/log/auth.log /var/log/syslog /var/log/http-access.log
rm -f /run/rsyslogd.pid
rm -f /run/fail2ban/fail2ban.sock /run/fail2ban/fail2ban.pid
rsyslogd
if [ -s /etc/nftables-lab.conf ]; then
    nft-lab load /etc/nftables-lab.conf
else
    nft-lab reset
fi
service fail2ban start
# Log authentication to rsyslog. PID 1 is the listener, so reload with HUP 1.
exec /usr/sbin/sshd -D
