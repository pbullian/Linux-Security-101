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

## Validation in the restored original order

A fresh run on 15 October 2026 passed **71/71 executable blocks**, including 13 expected nonzero outcomes, on Linux x86_64 with osquery 5.23.1. It followed original phase order, with rate/concurrency after Phase 10 and before Fail2ban. Host-key uniqueness, loopback binding, log permissions, binary ownership and preservation of the firewall after invalid input also passed. The disposable project was removed. [Current run](VALIDATION-2026-10-15.json) records exact guide hashes and results; [the prior run](VALIDATION-2026.json) is retained as history.

Build the images, then run `python3 tests/validate_guide.py --extensions`. Docker Desktop, ARM runtime behaviour and VM boot/scheduler behaviour need separate classroom preflight.

## Restored teaching sequence

The original Phase 0–15 sequence is restored. Phase 0 explains mission, setup and deliverables; Phase 1 defines the threat surface and the purpose of the baseline audit. Every phase places its practical after the corresponding concepts. Section checkpoints identify where to pause inside the command reference. The historical EXTENSIONS-2026.md filename now contains TP 11A, part of the original rate/concurrency topic.

Students use the same phase numbers in the questions and Markdown report. The new worked Phase 1 example shows observations, evidence, decisions and limitations using clearly labelled fictional snippets. Phase 1 does not require a configuration change. Later phases use tests appropriate to their control. The final risk-delta note returns to the starting inventory.

All 63 core and 8 rate/concurrency Bash blocks remain byte-for-byte identical to the corrected edition. [The comparison](DOCUMENTATION-VALIDATION-2026.json) records this; the fresh run additionally validates their restored execution order. Private teacher answers are maintained in the separate private course repository.
