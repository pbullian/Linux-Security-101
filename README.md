# Linux Security 101

Disposable Ubuntu 24.04 target and Debian 12 client for the CPE Linux security course.

- [Student exercises in original Phases 0–15](docs/EXERCISES.md)
- [Markdown report template](docs/REPORT-TEMPLATE.md) and [submission instructions](docs/SUBMISSION.md)
- [Phase 11 rate and concurrency practical](docs/EXTENSIONS-2026.md)

The original course order is preserved: **Phase 0 setup and deliverables; Phase 1 threat surface; then Phases 2–15 in order**. The slides explain each concept before the matching exercise. Use the same phase numbers in your notes and report. Phase 11 has two practice cycles.

Start by showing [the worked Phase 1 report](docs/REPORT-EXAMPLE.md). It explains what students should look for and how to connect an observation to a justified decision. The audit records the starting state; it does not require arbitrary changes. The complete sequence needs roughly 13–14 hours plus breaks at the suggested pace; assign the phases that fit your available teaching time.

## Get started

Install Git and Docker Engine with the Compose plugin, or Docker Desktop configured for Linux containers. Start Docker, then run these commands in a laptop terminal:

```sh
git clone https://github.com/pbullian/Linux-Security-101.git
cd Linux-Security-101
docker compose up -d --build
docker compose ps
```

The first build downloads the container images and may take a few minutes. Open two more terminals in the repository and start the target and client consoles:

```sh
docker compose exec target bash
```

```sh
docker compose exec client bash
```

Open the last two commands in separate terminals. Their prompts show `root@target` and `root@client`. Both consoles start as root inside their container. The guide marks checks that must run as an ordinary user.

The target is reachable as `target:22` from the client. Its SSH port is published only at `127.0.0.1:2222`. Set `LAB_SSH_PORT` before starting if that port is occupied. Client tools are already installed. The client and target have separate filesystems: a key generated in the client does not exist on your laptop.

This lab deliberately includes the password `student:student`, two SUID binaries and a world-writable directory. Run it only as a disposable teaching lab. Mount only the artifacts directory. The mount exercise needs `SYS_ADMIN`; firewall exercises need `NET_ADMIN`. These privileges apply to the target container, so do not use this configuration as a production server template.

## Preflight

```sh
docker compose exec target bash -c 'sshd -t; nft --version; findmnt -T /tmp -no OPTIONS; ls -l /var/log/auth.log'
docker compose exec client bash -c 'ip -4 addr show eth0; command -v ssh curl nc nmap; getent hosts target'
```

Builds use each machine's native architecture. Run the preflight checks below before beginning the exercises.

## Evidence and restart

`./artifacts` on the laptop is mounted at `/artifacts` on the target. Save evidence from the root target console. From an ordinary user's session use `sudo tee /artifacts/name.txt`; `sudo command > /artifacts/name.txt` does not elevate the shell's redirection.

Use `nft-lab reset` to replace only the lab's `inet filter` table. Never use `nft flush ruleset` here: it also deletes Docker's DNS NAT rules. Use `nft-lab save` to persist the lab table across `docker compose restart target`. Fail2ban manages its own table and recreates its bans separately.

```sh
# Restart preserves container accounts/configuration and saved firewall policy.
docker compose restart target
# Destroy and recreate containers to return to the initial exercise state.
docker compose down
docker compose up -d
```

The bind-mounted `artifacts` directory survives both commands, including `down -v`. Archive or clear it deliberately on the laptop when needed. Resetting recreates SSH host keys; verify the new fingerprint before replacing a stale known-host entry.

The root Dockerfile/start.sh are authoritative. Copies under `target/` remain for the legacy build command `docker build -f target/Dockerfile .` with the repository root as its build context.

The update exercise changes packages inside the disposable target. It needs repository access; the osquery installation also needs GitHub release access.
