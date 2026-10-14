# Practical revision, October 2026

The revision keeps the original Linux-security topics and makes the practical reproducible from this repository. It is a disposable teaching environment, not a production hardening template.

## Runtime

- Compose now builds the corrected source. The Debian client includes the required network tools.
- SSH is published on laptop loopback only. Each fresh target generates its own host keys.
- The target has the packages, mount options and capabilities needed by the exercises.
- File logging works without systemd/journald; authentication logs are root/adm-readable rather than world-readable.
- Restart removes stale rsyslog/Fail2ban runtime files and reloads the saved teaching firewall.
- `nft-lab` validates and replaces only the lab's `inet filter` table, preserving Docker's DNS NAT tables.
- osquery is pinned to **5.23.1**, checked against the [official release](https://github.com/osquery/osquery/releases/tag/5.23.1) on 14 October 2026. Its x86_64 and ARM archive digests are fixed in the installer; extraction does not restore the archive's UID 1000 ownership.

## Practical corrections

- Explicit target/client/laptop and root/ordinary-user execution contexts; correct artifact redirection and reset semantics.
- PAM stack and SSH key handling separated; fingerprint comparison, lockout recovery and effective-policy checks.
- Explicit account/source allowlist, including a valid-key test from a new source before packet filtering.
- Parenthesized SUID/SGID search, before/after ordinary-user tests, selective fixes and a clear statement that the setup account still has sudo.
- Correct umask bit semantics and tested inherited ACL access.
- Mount tests distinguish direct execution from explicit interpreter use; real fstab and reboot work are VM-only.
- Stateful firewall preserves DNS and survives target restart. Rate/concurrency controls precede acceptance and use per-source state where intended.
- Fail2ban counts one HTTP request once; five/six-event thresholds, actual blocking and recovery are tested.
- Strict package refresh, inspected security origins and a dry run; no claim that timers run in this container.
- Chroot uses a non-conflicting variable name, the actual service PID and a separate UID with root-owned content.
- AIDE creates needed directories, uses `database_in`, anchors exact file exclusions and requires review before a new baseline.
- osquery queries use actual schema columns, constrain the `file` table and avoid treating octal mode text as decimal numbers.

## Reproduce validation

The final fresh run on 14 October 2026 passed **71/71 executable blocks** in teaching order: 63 core blocks and 8 extension blocks, including 13 expected nonzero outcomes. It used osquery 5.23.1. Host-key uniqueness, loopback binding, log permissions, binary ownership and preservation of an existing firewall after invalid input also passed. The disposable project was removed. [Machine-readable results](VALIDATION-2026.json) record the source hashes and individual results.

Build the images, then run `python3 tests/validate_guide.py --extensions`. The validator checks the guide's exact executable blocks, expected nonzero outcomes, independent host keys, loopback exposure, log readability and binary ownership. It records the guide hash and removes its own disposable project. See the README for teaching order, output paths and dependencies.

Linux x86_64 is the exercised platform. ARM execution, macOS/Windows Docker Desktop and VM boot/scheduler behaviour still need separate classroom preflight. Checksums for an architecture are not proof of runtime testing on that architecture.

## Teaching and report revision

The generic E1–E9 sequence now alternates about 20 minutes of explanation with practice and a short review. Student questions, a Markdown report template, an evidence manifest and submission guidance use the same IDs. Questions require predictions, actual output, an explanation of limits and an assigned changed-condition scenario. Optional tutoring hints do not provide copy protection.

This revision changes prose and student documents only. All 63 core and 8 extension Bash blocks remain byte-for-byte identical to the previously validated revision. The historical runtime result retains its original whole-document hashes; [the documentation comparison](DOCUMENTATION-VALIDATION-2026.json) records the new prose hash and unchanged command blocks. No new runtime pass is claimed for this documentation-only change.
