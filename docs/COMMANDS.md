# Command-by-command practical guide

Use this alongside [the TP](EXERCISES.md). Each step names where to run it: **LAPTOP** means a terminal in the cloned repository; **TARGET** and **CLIENT** mean the corresponding container console. Start at [Phase 0 setup](../README.md#get-started). Keep the target root console open for recovery. Run each block in order and save the evidence it creates under `/artifacts` when indicated.

Commands below are for the disposable course lab only. Never reuse the lab passwords or apply these configuration changes to a personal or production machine. For Phase 11, complete 11A before 11B.


## Phase 1: Threat-surface audit


### 1. Audit target services and processes.

```bash
# TARGET [baseline]
whoami
ss -tulpn | tee /artifacts/listeners-before.txt
ps aux | tee /artifacts/processes-before.txt
nft --version
sshd -t
findmnt -T /tmp -no TARGET,OPTIONS
test -f /var/log/auth.log
```


### 2. Check client network tools and target name resolution.

```bash
# CLIENT [client-tools]
ip -4 addr show eth0
command -v ssh curl nc nmap
getent hosts target
```


## Phase 2: Accounts and sudo


### 1. Create the lab roles and validate sudo policy.

```bash
# TARGET [accounts]
groupadd admin
useradd -m -s /bin/bash -G admin alice
echo 'alice:LabAlice2026' | chpasswd
useradd -m -s /bin/bash bob
echo 'bob:LabBob2026' | chpasswd
passwd -l root
printf '%s\n' '%admin ALL=(ALL:ALL) ALL' > /etc/sudoers.d/90-admin
chmod 0440 /etc/sudoers.d/90-admin
visudo -c
id alice
id bob
cp /etc/sudoers.d/90-admin /artifacts/90-admin
```


### 2. Verify Alice can use delegated administration.

```bash
# TARGET [alice-sudo] user=alice
printf '%s\n' LabAlice2026 | sudo -S -k id -u
```


### 3. Verify Bob is refused.

```bash
# TARGET [bob-sudo-denied] user=bob expect=1
printf '%s\n' LabBob2026 | sudo -S -k id -u
```


## Phase 3: PAM lockout


### 1. Record the target SSH host fingerprint.

```bash
# TARGET [server-fingerprint]
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```


### 2. Verify the fingerprint from the client.

```bash
# CLIENT [client-fingerprint]
mkdir -p /root/.ssh
ssh-keyscan -t ed25519 target 2>/dev/null > /root/.ssh/known_hosts
ssh-keygen -lf /root/.ssh/known_hosts
```


### 3. Apply the lab PAM lockout policy.

```bash
# TARGET [pam-config]
cp /etc/pam.d/common-auth /root/common-auth.before
cp /etc/pam.d/common-account /root/common-account.before
cat > /etc/security/faillock.conf <<'CONF'
deny = 5
unlock_time = 900
CONF
cat > /etc/pam.d/common-auth <<'CONF'
auth required pam_faillock.so preauth silent
auth [success=1 default=bad] pam_unix.so try_first_pass
auth [default=die] pam_faillock.so authfail
auth required pam_permit.so
CONF
cat > /etc/pam.d/common-account <<'CONF'
account required pam_unix.so
account required pam_faillock.so
CONF
faillock --user alice --reset
```


### 4. Confirm password login before failures.

```bash
# CLIENT [password-works]
sshpass -p LabAlice2026 ssh -o NumberOfPasswordPrompts=1 -o PreferredAuthentications=password -o PubkeyAuthentication=no alice@target 'echo PASSWORD_OK'
```


### 5. Generate five failed logins.

```bash
# CLIENT [five-failures]
for i in 1 2 3 4 5; do
  if sshpass -p WrongPassword ssh -o NumberOfPasswordPrompts=1 -o PreferredAuthentications=password -o PubkeyAuthentication=no alice@target true; then
    echo 'Unexpected authentication success'; exit 1
  fi
done
```


### 6. Inspect the failure counter.

```bash
# TARGET [lock-counter]
faillock --user alice | tee /artifacts/faillock.txt
```


### 7. Confirm the valid password is temporarily refused.

```bash
# CLIENT [correct-password-locked] expect=255
sshpass -p LabAlice2026 ssh -o NumberOfPasswordPrompts=1 -o PreferredAuthentications=password -o PubkeyAuthentication=no alice@target true
```


### 8. Reset the lab account lock.

```bash
# TARGET [reset-lock]
faillock --user alice --reset
faillock --user alice
```


### 9. Confirm recovery.

```bash
# CLIENT [password-recovered]
sshpass -p LabAlice2026 ssh -o NumberOfPasswordPrompts=1 -o PreferredAuthentications=password -o PubkeyAuthentication=no alice@target 'echo RECOVERED_PASSWORD_OK'
```


## Phase 4: SSH keys


### 1. Create and install the lab SSH key.

```bash
# CLIENT [install-keys]
ssh-keygen -q -t ed25519 -f /root/.ssh/labkey -N ''
ssh-keygen -lf /root/.ssh/labkey.pub
sshpass -p LabAlice2026 ssh-copy-id -i /root/.ssh/labkey.pub alice@target
sshpass -p student ssh-copy-id -i /root/.ssh/labkey.pub student@target
ssh -i /root/.ssh/labkey -o BatchMode=yes alice@target 'id; echo KEY_OK'
```


### 2. Apply and validate SSH policy.

```bash
# TARGET [ssh-harden]
cat > /etc/ssh/sshd_config.d/00-lab.conf <<'CONF'
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitEmptyPasswords no
PubkeyAuthentication yes
AllowGroups admin
MaxAuthTries 2
LoginGraceTime 30
CONF
sshd -t
kill -HUP 1
sshd -T | grep -E 'permitrootlogin|passwordauthentication|kbdinteractive|allowgroups'
cp /etc/ssh/sshd_config.d/00-lab.conf /artifacts/sshd-lab.conf
```


### 3. Test key access.

```bash
# CLIENT [key-allowed]
ssh -i /root/.ssh/labkey -o BatchMode=yes alice@target 'echo KEY_OK'
```


### 4. Test that password login is refused.

```bash
# CLIENT [password-refused] expect=255
sshpass -p LabAlice2026 ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no alice@target true
```


### 5. Test that an unapproved account is refused.

```bash
# CLIENT [unauthorized-group-refused] expect=255
ssh -i /root/.ssh/labkey -o BatchMode=yes student@target true
```


## Phase 5: SUID and SGID


### 1. Inventory SUID/SGID files.

```bash
# TARGET [suid-inventory]
find / -xdev -type f \( -perm -4000 -o -perm -2000 \) -print 2>/dev/null | sort | tee /artifacts/suid_sgid.txt
stat -c '%a %U %n' /usr/local/bin/vimroot /opt/labtools/shroot /opt/labtools
```


### 2. Test the lab binary as student.

```bash
# TARGET [suid-before] user=student
/opt/labtools/shroot -p -c 'id; test "$(id -u)" = 0'
```


### 3. Remove the deliberate elevation.

```bash
# TARGET [suid-fix]
chmod u-s /usr/local/bin/vimroot /opt/labtools/shroot
chmod 0755 /opt/labtools
setcap cap_net_raw+ep /usr/bin/ping
getcap /usr/bin/ping
```


### 4. Repeat the test.

```bash
# TARGET [suid-after] user=student
/opt/labtools/shroot -p -c 'id; test "$(id -u)" != 0'
```


## Phase 6: umask


### 1. Compare created file and directory permissions.

```bash
# TARGET [umask]
lab_previous_umask=$(umask)
lab_previous_dir=$PWD
mkdir -p /tmp/umask-demo
cd /tmp/umask-demo
umask 027
touch f
mkdir d
stat -c '%a %n' f d
test "$(stat -c %a f)" = 640
test "$(stat -c %a d)" = 750
umask 077
touch private
test "$(stat -c %a private)" = 600
# Restore this terminal before continuing to ACLs and service setup.
umask "$lab_previous_umask"
cd "$lab_previous_dir"
unset lab_previous_umask lab_previous_dir
```


## Phase 7: ACLs


### 1. Create the project group and default ACL.

```bash
# TARGET [acl-setup]
groupadd auditors
usermod -aG auditors bob
mkdir -p /srv/project
chgrp admin /srv/project
chmod 2770 /srv/project
setfacl -m g:admin:rwx,g:auditors:rx,m:rwx /srv/project
setfacl -d -m g:admin:rwx,g:auditors:rx,m:rwx /srv/project
getfacl /srv/project | tee /artifacts/project-acl.txt
```


### 2. Create a file as Alice and inspect inherited permissions.

```bash
# TARGET [acl-alice-write] user=alice
echo 'reviewable report' > /srv/project/report
mkdir /srv/project/subdir
stat -c '%a %G %n' /srv/project/report /srv/project/subdir
getfacl /srv/project/report /srv/project/subdir
```


### 3. Open a fresh Bob session and test read access.

```bash
# TARGET [acl-bob-read] user=bob fresh-session
id
cat /srv/project/report
```


### 4. Test that Bob cannot write.

```bash
# TARGET [acl-bob-write-refused] user=bob expect=1
echo 'unapproved change' >> /srv/project/report
```


## Phase 8: Mount flags


### 1. Inspect mount options and prepare test files.

```bash
# TARGET [mount-observation]
for p in /tmp /var/tmp /dev/shm /home /var /var/log; do
  printf '%s: ' "$p"
  findmnt -T "$p" -no TARGET,OPTIONS
done
cp /bin/true /tmp/t
printf '#!/bin/sh\necho interpreted-script\n' > /tmp/s.sh
chmod +x /tmp/s.sh
```


### 2. Test direct binary execution.

```bash
# TARGET [noexec-binary-refused] expect=126
/tmp/t
```


### 3. Test direct script execution.

```bash
# TARGET [noexec-script-refused] expect=126
/tmp/s.sh
```


### 4. Show the interpreter limitation, then restore noexec.

```bash
# TARGET [noexec-interpreter-limit]
bash /tmp/s.sh
mount -o remount,exec /tmp
/tmp/t
mount -o remount,noexec /tmp
```


### 5. Confirm direct execution is blocked again.

```bash
# TARGET [noexec-restored] expect=126
/tmp/t
```


## Phase 9: SSH source policy


### 1. Restrict SSH to the approved client address.

```bash
# TARGET [source-policy]
lab_client_ip=$(getent ahostsv4 client | awk 'NR==1{print $1}')
test -n "$lab_client_ip"
printf 'AllowUsers alice@%s\n' "$lab_client_ip" > /etc/ssh/sshd_config.d/01-allowlist.conf
sshd -t
kill -HUP 1
python3 -m http.server 8080 --directory /srv/project > /tmp/http8080.log 2>&1 &
echo $! > /run/http8080.pid
sleep 1
```


### 2. Confirm SSH and HTTP from the approved client.

```bash
# CLIENT [web-before-filter]
ssh -i /root/.ssh/labkey -o BatchMode=yes -o ConnectTimeout=3 alice@target true
curl --fail --max-time 3 http://target:8080/report
```


### 3. Test the same key from a new client address.

```bash
# LAPTOP [ssh-other-source-refused] expect=255
docker compose exec -T client tar -C /root/.ssh -cf - labkey known_hosts |
  docker compose run --rm -T --no-deps client bash -ec '
    mkdir -p /root/.ssh
    tar -xf - -C /root/.ssh
    chmod 600 /root/.ssh/labkey
    ssh -i /root/.ssh/labkey -o BatchMode=yes -o ConnectTimeout=3 alice@target true
  '
```


## Phase 10: nftables firewall


### 1. Apply a stateful firewall allowing approved client traffic.

```bash
# TARGET [firewall]
lab_client_ip=$(getent ahostsv4 client | awk 'NR==1{print $1}')
cat > /root/lab-firewall.nft <<RULES
table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;
    ct state established,related accept
    iif lo accept
    ip saddr $lab_client_ip tcp dport 22 counter accept
    ip saddr $lab_client_ip tcp dport 8080 counter accept
    counter drop
  }
}
RULES
nft-lab load /root/lab-firewall.nft
nft list table inet filter | tee /artifacts/nft.ruleset.txt
getent hosts archive.ubuntu.com
```


### 2. Verify the allowed SSH and HTTP flows.

```bash
# CLIENT [allowed-after-filter]
ssh -i /root/.ssh/labkey -o BatchMode=yes -o ConnectTimeout=3 alice@target true
curl --fail --max-time 3 http://target:8080/report
```


### 3. Verify a new client is blocked.

```bash
# LAPTOP [other-client-refused] expect=28
docker compose run --rm --no-deps client curl --fail --max-time 2 http://target:8080/report
```


### 4. Save the lab firewall policy.

```bash
# TARGET [save-firewall]
nft-lab save
```


### 5. Restart target and wait for readiness.

```bash
# LAPTOP [restart-target]
docker compose restart target
docker compose up -d --wait --no-build
```


### 6. Verify firewall and DNS after restart.

```bash
# TARGET [check-persistence]
nft list table inet filter
grep 'policy drop' /etc/nftables-lab.conf
nft list table inet filter | grep 'policy drop'
getent hosts archive.ubuntu.com
```


### 7. Verify SSH after restart.

```bash
# CLIENT [ssh-after-restart]
ssh -i /root/.ssh/labkey -o BatchMode=yes -o ConnectTimeout=3 alice@target true
```


## Phase 11A: Rate and connection limits


### 1. Add a per-source concurrent SSH connection cap.

```bash
# TARGET [extension-cap-policy]
nft-lab reset
nft add set inet filter ssh_conn '{ type ipv4_addr; flags dynamic; }'
nft add rule inet filter input ct state established,related accept
nft add rule inet filter input iif lo accept
nft add rule inet filter input tcp dport 22 ct state new add @ssh_conn '{ ip saddr ct count over 2 }' counter reject
nft add rule inet filter input tcp dport 22 counter accept
```


### 2. Keep two SSH sessions open and test a third.

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


### 3. Save the rule evidence and reset the lab table.

```bash
# TARGET [extension-cap-evidence]
nft list table inet filter | tee /artifacts/connection-cap.txt
nft-lab reset
```


### 4. Start the HTTP service and add a per-source rate meter.

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


### 5. Send two permitted requests.

```bash
# CLIENT [extension-meter-two-allowed]
curl --fail --max-time 2 http://target:8092/report
curl --fail --max-time 2 http://target:8092/report
```


### 6. Test the rate limit.

```bash
# CLIENT [extension-meter-third-refused] expect=7
curl --fail --max-time 2 http://target:8092/report
```


### 7. Verify a second source has its own rate bucket.

```bash
# LAPTOP [extension-meter-other-source-allowed]
docker compose run --rm -T --no-deps client curl --fail --max-time 2 http://target:8092/report
```


### 8. Save evidence, stop the service and reset policy.

```bash
# TARGET [extension-cleanup]
nft list table inet filter | tee /artifacts/per-source-meter.txt
kill "$(cat /run/meter-http.pid)"
rm /run/meter-http.pid
nft-lab reset
nft-lab save
getent hosts archive.ubuntu.com
```


## Phase 11B: Fail2ban


### 1. Configure Fail2ban for HTTP 404 events.

```bash
# TARGET [fail2ban-setup]
nft-lab reset
nft-lab save
: > /var/log/http-access.log
python3 -u -m http.server 8090 --bind 0.0.0.0 --directory /srv/project >> /var/log/http-access.log 2>&1 &
echo $! > /run/http8090.pid
cat > /etc/fail2ban/filter.d/pyhttp-404.conf <<'CONF'
[Definition]
failregex = ^<HOST>\s.*"[^"]*"\s+404(?:\s|$)
ignoreregex =
CONF
cat > /etc/fail2ban/jail.d/pyhttp-404.local <<'CONF'
[pyhttp-404]
enabled = true
port = 8090
filter = pyhttp-404
logpath = /var/log/http-access.log
backend = polling
maxretry = 6
findtime = 60
bantime = 600
action = nftables[name=pyhttp-404, chain=input, protocol=tcp, port=8090]
CONF
service fail2ban restart
sleep 2
fail2ban-client ping
fail2ban-client status pyhttp-404
```


### 2. Send five events and verify access remains.

```bash
# CLIENT [five-http-events]
for i in 1 2 3 4 5; do
  test "$(curl -sS -o /dev/null -w '%{http_code}' --max-time 2 http://target:8090/nope$i)" = 404
done
sleep 3
curl --fail --max-time 2 http://target:8090/report
```


### 3. Inspect matches and confirm no ban yet.

```bash
# TARGET [five-events-not-banned]
fail2ban-regex /var/log/http-access.log /etc/fail2ban/filter.d/pyhttp-404.conf
fail2ban-client status pyhttp-404
lab_client_ip=$(getent ahostsv4 client | awk 'NR==1{print $1}')
test "$(fail2ban-client get pyhttp-404 banned "$lab_client_ip")" = 0
```


### 4. Send the sixth event.

```bash
# CLIENT [sixth-http-event]
test "$(curl -sS -o /dev/null -w '%{http_code}' --max-time 2 http://target:8090/nope6)" = 404
sleep 3
```


### 5. Verify the ban and save evidence.

```bash
# TARGET [six-events-banned]
lab_client_ip=$(getent ahostsv4 client | awk 'NR==1{print $1}')
test "$(fail2ban-client get pyhttp-404 banned "$lab_client_ip")" = 1
fail2ban-client status pyhttp-404 | tee /artifacts/fail2ban-status.txt
fail2ban-regex /var/log/http-access.log /etc/fail2ban/filter.d/pyhttp-404.conf | tee /artifacts/fail2ban-regex.txt
nft list ruleset
```


### 6. Confirm the banned client is blocked.

```bash
# CLIENT [banned-http-refused] expect=7
curl --fail --max-time 2 http://target:8090/report
```


### 7. Remove the temporary ban.

```bash
# TARGET [unban]
lab_client_ip=$(getent ahostsv4 client | awk 'NR==1{print $1}')
fail2ban-client set pyhttp-404 unbanip "$lab_client_ip"
```


### 8. Confirm access after unban.

```bash
# CLIENT [http-after-unban]
curl --fail --max-time 2 http://target:8090/report
```


### 9. Disable the jail and clean up.

```bash
# TARGET [ban-cleanup]
fail2ban-client stop pyhttp-404
sed -i 's/enabled = true/enabled = false/' /etc/fail2ban/jail.d/pyhttp-404.local
kill "$(cat /run/http8090.pid)"
rm /run/http8090.pid
nft-lab reset
nft-lab save
getent hosts archive.ubuntu.com
```


## Phase 12: Updates


### 1. Refresh package indexes, upgrade and record package state.

```bash
# TARGET [update-refresh]
dpkg-query -W > /artifacts/packages-before.txt
apt-get -o APT::Update::Error-Mode=any update
DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::=--force-confold -y upgrade
dpkg-query -W > /artifacts/packages-after.txt
```


### 2. Configure and inspect the unattended security update policy.

```bash
# TARGET [security-update-policy]
cat > /etc/apt/apt.conf.d/20auto-upgrades <<'CONF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::Unattended-Upgrade "1";
APT::Periodic::AutocleanInterval "7";
CONF
cat > /etc/apt/apt.conf.d/52lab-security-only <<'CONF'
#clear Unattended-Upgrade::Allowed-Origins;
Unattended-Upgrade::Allowed-Origins {
 "${distro_id}:${distro_codename}-security";
};
CONF
apt-config dump | grep -E 'Allowed-Origins|APT::Periodic'
unattended-upgrade --dry-run --debug > /artifacts/updates.log 2>&1
tail -n 15 /artifacts/updates.log
apt-mark hold vim
apt-mark showhold
apt-mark unhold vim
cp /var/log/apt/history.log /artifacts/apt-history.log
```


## Phase 13: chroot


### 1. Build the chroot and start its web service as a reduced UID.

```bash
# TARGET [chroot-start]
install -d -m 0755 /srv/jail /srv/jail/bin /srv/jail/www
install -d -m 1777 /srv/jail/tmp
install -m 0755 "$(command -v busybox)" /srv/jail/bin/busybox
useradd -r -s /usr/sbin/nologin www-chroot
lab_uid=$(id -u www-chroot)
lab_gid=$(id -g www-chroot)
echo 'OK: chrooted web' > /srv/jail/www/index.html
chmod 0644 /srv/jail/www/index.html
# Keep static served files root-owned: the service only needs to read them.
chroot --userspec="$lab_uid:$lab_gid" /srv/jail /bin/busybox httpd -f -v -p 0.0.0.0:8091 -h /www > /tmp/jail-http.log 2>&1 &
echo $! > /run/jail-http.pid
sleep 1
lab_pid=$(cat /run/jail-http.pid)
ps -o pid,user,args -p "$lab_pid"
awk '/Uid|Gid/' "/proc/$lab_pid/status"
test "$(awk '/^Uid:/{print $2}' "/proc/$lab_pid/status")" = "$lab_uid"
ss -ltnp | grep 8091
# Inspect as the service UID: the container root lacks CAP_SYS_PTRACE.
runuser -u www-chroot -- readlink "/proc/$lab_pid/root"
test "$(runuser -u www-chroot -- readlink "/proc/$lab_pid/root")" = /srv/jail
```


### 2. Test the service from the client.

```bash
# CLIENT [chroot-http]
test "$(curl -fsS --max-time 2 http://target:8091)" = 'OK: chrooted web'
```


### 3. Inspect filesystem and write boundaries inside the chroot.

```bash
# TARGET [chroot-inside]
lab_uid=$(id -u www-chroot)
lab_gid=$(id -g www-chroot)
chroot --userspec="$lab_uid:$lab_gid" /srv/jail /bin/busybox sh -ec '
  /bin/busybox pwd
  /bin/busybox ls -l /
  /bin/busybox id
  /bin/busybox cat /www/index.html
  test ! -w /bin/busybox
  test ! -w /www/index.html
  test ! -e /etc
  echo jail-marker > /tmp/jail-only
'
test -f /srv/jail/tmp/jail-only
test ! -f /tmp/jail-only
```


### 4. Stop the service.

```bash
# TARGET [chroot-cleanup]
kill "$(cat /run/jail-http.pid)"
rm /run/jail-http.pid
```


## Phase 14: AIDE integrity monitoring


### 1. Create and verify an initial AIDE baseline.

```bash
# TARGET [aide-baseline]
mkdir -p /etc/aide /var/lib/aide
cat > /etc/aide/aide.conf <<'CONF'
@@define DBDIR /var/lib/aide
database_in=file:@@{DBDIR}/aide.db
database_out=file:@@{DBDIR}/aide.db.new
gzip_dbout=yes
LAB = p+i+n+u+g+s+m+c+sha256
/etc LAB
!/etc/mtab$
!/etc/ld\.so\.cache$
!/etc/resolv\.conf$
CONF
aide --config /etc/aide/aide.conf --init
install -D -m 0600 /var/lib/aide/aide.db.new /var/lib/aide/aide.db
aide --config /etc/aide/aide.conf --check | tee /artifacts/aide-clean.txt
```


### 2. Make a lab change and record detected differences.

```bash
# TARGET [aide-change] expect=4
echo '# authorized classroom test' >> /etc/hosts
(
  # Exit only this subshell, preserving the recovery console.
  set +e
  aide --config /etc/aide/aide.conf --check | tee /artifacts/aide-changed.txt
  exit "${PIPESTATUS[0]}"
)
```


### 3. Review the change and update the baseline.

```bash
# TARGET [aide-reviewed-baseline]
aide --config /etc/aide/aide.conf --init
install -m 0600 /var/lib/aide/aide.db.new /var/lib/aide/aide.db
aide --config /etc/aide/aide.conf --check
```


## Phase 15: osquery inventory


### 1. Install the pinned osquery build and inspect schemas.

```bash
# TARGET [osquery-install]
install-osquery-lab
osqueryi '.schema kernel_info'
osqueryi '.schema file'
```


### 2. Query host, user, session and network inventory.

```bash
# TARGET [osquery-inventory]
osqueryi --json 'SELECT lp.address,lp.port,lp.protocol,p.pid,p.name,p.cmdline FROM listening_ports lp LEFT JOIN processes p ON lp.pid=p.pid ORDER BY lp.port;' > /artifacts/listeners.json
osqueryi --json 'SELECT username,uid,gid,directory,shell FROM users ORDER BY uid;' > /artifacts/users.json
osqueryi --json 'SELECT user,tty,host,time FROM logged_in_users;' > /artifacts/sessions.json
osqueryi --json 'SELECT name,version,platform,platform_like FROM os_version;' > /artifacts/os.json
osqueryi --json 'SELECT version,arguments,path,device FROM kernel_info;' > /artifacts/kernel.json
osqueryi --json 'SELECT hardware_model,cpu_brand,physical_memory FROM system_info;' > /artifacts/hardware.json
osqueryi --json 'SELECT total_seconds,days,hours FROM uptime;' > /artifacts/uptime.json
osqueryi --json "SELECT interface,address,mask,broadcast FROM interface_addresses WHERE address NOT LIKE '127.%' AND address != '::1';" > /artifacts/interfaces.json
```


### 3. Query privileged files and process details.

```bash
# TARGET [osquery-investigation]
osqueryi --json 'SELECT path,username,groupname,permissions FROM suid_bin;' > /artifacts/suid.json
osqueryi --json "SELECT path,mode FROM file WHERE path IN ('/usr/bin/sudo','/opt/labtools/shroot');" > /artifacts/selected-files.json
osqueryi --json 'SELECT lp.address,lp.port,p.pid,p.name,p.euid FROM listening_ports lp JOIN processes p ON lp.pid=p.pid WHERE p.euid=0 ORDER BY lp.port;' > /artifacts/root-listeners.json
osqueryi --json 'SELECT pid,name,resident_size FROM processes ORDER BY resident_size DESC LIMIT 10;' > /artifacts/top-memory.json
```


## Finish and submit

Collect the files created under `/artifacts` into the matching `evidence/phase-XX/` folders on the laptop. Complete the five short TP questions for each assigned phase, then follow [SUBMISSION.md](SUBMISSION.md). Do not submit private keys or real credentials.
