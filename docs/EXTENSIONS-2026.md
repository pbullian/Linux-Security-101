# Phase 11 practical: rate and concurrent connections

After the firewall exercise, compare rate limits with concurrent-connection limits, then run these tests. Start with Alice's key installed and the project file from the ACL exercise. Continue with Fail2ban in the assigned Phase 11 material. Keep the target root console open. These policies replace only the lab table.

## 1. Limit simultaneous SSH connections

An early SSH accept would bypass a later cap. Put the cap on new connections before acceptance. Established traffic remains accepted. The cap tracks IPv4 sources; two users behind the same source address share it.

```bash
# TARGET [extension-cap-policy]
nft-lab reset
nft add set inet filter ssh_conn '{ type ipv4_addr; flags dynamic; }'
nft add rule inet filter input ct state established,related accept
nft add rule inet filter input iif lo accept
nft add rule inet filter input tcp dport 22 ct state new add @ssh_conn '{ ip saddr ct count over 2 }' counter reject
nft add rule inet filter input tcp dport 22 counter accept
```

Keep two connections alive, verify both actually succeed, and require the third to fail. A failed first connection must not be mistaken for a successful cap test.

```bash
# CLIENT [extension-cap-test]
lab_ssh=(ssh -i /root/.ssh/labkey -o BatchMode=yes -o ConnectTimeout=3 -o ControlMaster=no)
"${lab_ssh[@]}" alice@target 'sleep 8' > /tmp/cap1.log 2>&1 & lab_first=$!
sleep 1
"${lab_ssh[@]}" alice@target 'sleep 8' > /tmp/cap2.log 2>&1 & lab_second=$!
sleep 1
if "${lab_ssh[@]}" alice@target true > /tmp/cap3.log 2>&1; then lab_third=0; else lab_third=$?; fi
wait "$lab_first"
wait "$lab_second"
cat /tmp/cap3.log
test "$lab_third" != 0
```

```bash
# TARGET [extension-cap-evidence]
nft list table inet filter | tee /artifacts/connection-cap.txt
nft-lab reset
```

Explain why this differs from a new-connection rate. Existing conntrack entries may persist briefly after a TCP connection closes; allow state to expire before rerunning a cap experiment.

## 2. A rate bucket for each source

This small HTTP experiment isolates source-keyed rate limiting from SSH authentication and retransmissions. The initial bucket permits two new connections per source; its refill rate is two per minute. Make the three requests promptly so the third arrives before a token refills.

```bash
# TARGET [extension-meter-policy]
python3 -u -m http.server 8092 --directory /srv/project > /tmp/meter-http.log 2>&1 &
echo $! > /run/meter-http.pid
sleep 1
nft-lab reset
nft add rule inet filter input ct state established,related accept
nft add rule inet filter input tcp dport 8092 ct state new meter per_source '{ ip saddr timeout 1m limit rate over 2/minute burst 2 packets }' counter reject
nft add rule inet filter input tcp dport 8092 counter accept
```

```bash
# CLIENT [extension-meter-two-allowed]
curl --fail --max-time 2 http://target:8092/report
curl --fail --max-time 2 http://target:8092/report
```

```bash
# CLIENT [extension-meter-third-refused] expect=7
curl --fail --max-time 2 http://target:8092/report
```

```bash
# LAPTOP [extension-meter-other-source-allowed]
docker compose run --rm -T --no-deps client curl --fail --max-time 2 http://target:8092/report
```

```bash
# TARGET [extension-cleanup]
nft list table inet filter | tee /artifacts/per-source-meter.txt
kill "$(cat /run/meter-http.pid)"
rm /run/meter-http.pid
nft-lab reset
nft-lab save
getent hosts archive.ubuntu.com
```

What would change with a single global `limit`? What happens when legitimate users share a NAT address? A meter counts matching packets; the example selects new connections, and a drop-based policy may also count retransmitted attempts. Decide what you intend to measure before selecting the rule.
