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

## Final Docker verification of all phases

On 15 October 2026, both images were rebuilt without cache. The final Linux x86_64 run passed **72/72 executable blocks**, including 13 expected nonzero results. [Final results](VALIDATION-2026-10-15-FINAL.json) match the published guide hash and record image IDs, package versions and osquery 5.23.1.

A separate [full run with reused student consoles](VALIDATION-2026-10-15-CONSOLES.json) passed 72/72 and verified the terminal context through the sequence. This caught Bob's stale group membership in an earlier attempt. The final strict run also includes the last Phase 3 map clarification and stricter inner chroot assertions.

The guide now restores the umask and working directory, requires a fresh Bob console after group changes, waits for readiness after target restart, and uses an AIDE subshell that keeps the recovery console open. It explicitly checks password recovery, authorized-source SSH and chroot code/content write restrictions. Setup/lifecycle checks verify artifact persistence, stop/start, recreation and new host keys. All twelve osquery JSON evidence files parse successfully.

Build the images, then run `python3 tests/validate_guide.py --extensions`. Repeat with `--persistent-shells` to model reused student consoles. Both modes clean up their disposable projects. Docker Desktop, ARM runtime behavior and VM boot/scheduler behavior need separate preflight. [Earlier restored-order results](VALIDATION-2026-10-15.json) remain historical.

## Restored teaching sequence

The original Phase 0–15 sequence is restored. Phase 0 explains mission, setup and deliverables; Phase 1 defines the threat surface and the purpose of the baseline audit. Every phase places its practical after the corresponding concepts. Section checkpoints identify where to pause inside the command reference. The historical EXTENSIONS-2026.md filename now contains TP 11A, part of the original rate/concurrency topic.

Students use the same phase numbers in the questions and Markdown report. The new worked Phase 1 example shows observations, evidence, decisions and limitations using clearly labelled fictional snippets. Phase 1 does not require a configuration change. Later phases use tests appropriate to their control. The final risk-delta note returns to the starting inventory.

The guide now contains 64 core blocks and 8 rate/concurrency blocks. [The source comparison](DOCUMENTATION-VALIDATION-2026.json) records added/changed blocks and links the final validation. Private teacher answers remain in the separate private course repository.
