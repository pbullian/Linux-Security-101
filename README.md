# Linux Security 101

Disposable Ubuntu 24.04 target and Debian 12 client for the CPE Linux security course.

- [Corrected practical guide](docs/TP-2026.md)
- [Optional rate and concurrency practical](docs/EXTENSIONS-2026.md)
- [Changes and validation](docs/CHANGES-2026.md)

The course uses short theory pairs followed by practice and a debrief. Session 1 follows guide sections **1, 2, 4, 5**; session 2 follows **3, 7, 8**; the subsequent session follows **6, 10, 9, 11, 12**. Keep the same containers between sessions. The guide is a complete command reference, not a single-afternoon exercise.

## Start

Use Docker Engine with Compose on Linux, or Docker Desktop with Linux containers.
Run these commands in this repository, on your laptop:

```sh
mkdir -p artifacts
docker compose up -d --build
docker compose ps
docker compose exec host bash
docker compose exec attacker bash
```

Open the last two commands in separate terminals. Both consoles start as root **inside their container**. The guide explicitly marks checks that must run as an ordinary user. Use `docker compose exec` rather than assuming fixed container names.

The target is reachable as `host:22` from the client. Its SSH port is published only at `127.0.0.1:2222`. Set `LAB_SSH_PORT` before starting if that port is occupied. Client tools are already installed. The client and target have separate filesystems: a key generated in the client does not exist on your laptop.

This lab deliberately includes the password `student:student`, two SUID binaries and a world-writable directory. Run it only as a disposable teaching lab. Mount only the artifacts directory. The mount exercise needs `SYS_ADMIN`; firewall exercises need `NET_ADMIN`. These privileges apply to the target container, so do not use this configuration as a production server template.

## Preflight

```sh
docker compose exec host bash -c 'sshd -t; nft --version; findmnt -T /tmp -no OPTIONS; ls -l /var/log/auth.log'
docker compose exec attacker bash -c 'ip -4 addr show eth0; command -v ssh curl nc nmap; getent hosts host'
```

Builds use each machine's native architecture. The October 2026 audit was run on Linux x86_64; macOS, Windows and ARM still need a classroom preflight. The old `pbullian/sec_host_win` image was amd64 only. This Compose file builds the corrected source instead.

## Evidence and restart

`./artifacts` on the laptop is mounted at `/artifacts` on the target. Save evidence from the root target console. From an ordinary user's session use `sudo tee /artifacts/name.txt`; `sudo command > /artifacts/name.txt` does not elevate the shell's redirection.

Use `nft-lab reset` to replace only the lab's `inet filter` table. Never use `nft flush ruleset` here: it also deletes Docker's DNS NAT rules. Use `nft-lab save` to persist the lab table across `docker compose restart host`. Fail2ban manages its own table and recreates its bans separately.

```sh
# Restart preserves container accounts/configuration and saved firewall policy.
docker compose restart host
# Destroy and recreate containers to return to the initial exercise state.
docker compose down
docker compose up -d
```

The bind-mounted `artifacts` directory survives both commands, including `down -v`. Archive or clear it deliberately on the laptop when needed. Resetting recreates SSH host keys; verify the new fingerprint before replacing a stale known-host entry.

The root Dockerfile/start.sh are authoritative. Copies under `host/` remain for the legacy build command `docker build -f host/Dockerfile .` with the repository root as its build context.

## Validate the practical

After building the images, run `python3 tests/validate_guide.py --extensions`. The validator creates its own disposable Compose project, executes the guide's exact marked commands in teaching order, checks expected refusals, and removes only that project. It refuses to reuse an existing project. Use `--order reference` to follow document order instead. Results, command output and a guide hash are saved under the ignored `artifacts/validation/` directory. Use `--keep` only to inspect a failed disposable run. Docker Engine, Compose and Python 3 are required.

The update exercise changes packages inside the disposable target. It needs repository access; the osquery installation also needs GitHub release access. Set `--port` if the default validation port 22223 is occupied.
