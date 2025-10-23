# Linux Security Lab (Block 1)

Two containers:
- `sec_host` (Ubuntu 24.04): sshd, sudo, nftables, rsyslog, PAM tools, Fail2ban, ACL utils.
- `sec_attacker` (Debian 12): used to test SSH + firewall from same Docker network.
- Shared volume: `./artifacts`

## Run
```bash
docker compose up -d --build
docker exec -it sec_host bash
docker exec -it sec_attacker bash
```

## Prepare attacker with tools
```bash
# inside sec_attacker
apt update && apt install -y openssh-client iputils-ping nmap
ssh-keygen -t ed25519 -f ~/.ssh/labkey -N ''
```

## Install the key on the host (student user)
```bash
# show public key in attacker
cat ~/.ssh/labkey.pub

# paste into sec_host (as root or student with sudo)
install -d -m 700 ~student/.ssh
echo "<paste the public key here>" >> ~student/.ssh/authorized_keys
chown -R student:student ~student/.ssh
chmod 600 ~student/.ssh/authorized_keys
```

## Switch host to key-only SSH
```bash
# on sec_host
sed -i 's/^PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
kill -HUP $(pidof sshd)
```

## Verify
```bash
# from sec_attacker (container network)
ssh -i ~/.ssh/labkey student@host 'echo OK'

# from your laptop (host -> container)
ssh -p 2222 -i ~/.ssh/labkey student@localhost 'echo OK'
```

## Save artifacts
```bash
# on sec_host
nft list ruleset > /artifacts/nft.ruleset.txt
find / -xdev -type f -perm -4000 -o -perm -2000 2>/dev/null | sort > /artifacts/suid_sgid.txt
tail -n 100 /var/log/auth.log > /artifacts/auth_tail.txt
```

## Reset
```bash
docker compose down -v
```
