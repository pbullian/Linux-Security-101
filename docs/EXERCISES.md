# Student exercises in the original phase order

## The mission and why we start with an audit

You administer a small Linux server that must remain usable for approved work. First understand its threat surface: what an attacker can touch or interact with. Inventory what is running, why it is needed, who can reach it and which identity runs it. Then restrict unnecessary access, maintain software and detect changes through the later phases.

Phase 1 establishes the before-state. You are not asked to invent vulnerabilities or stop every service. Record observations, justified recommendations and questions needing another test. Later phases must show the effect and limits of the control you changed.

## What you do and submit

After a short explanation, complete the matching TP before moving to the next phase. Use the original phase numbers throughout your report. TP reference section numbers are locations for command blocks; the map below tells you which blocks to use. Phase 11 has two practical blocks, 11A and 11B, within the same phase.

Submit one ZIP with report.md, manifest.json and linked evidence files. For each assigned phase, answer four short questions: prediction, decision, evidence and interpretation. Attach every item in that phase’s Required evidence list. Record the command, target and user, expected and actual results, and exit status when relevant. Finish with a risk-delta note of at most 200 words.

Read [REPORT-EXAMPLE.md](REPORT-EXAMPLE.md) before starting. It shows a complete Phase 1 entry with explicitly fictional evidence. Use [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md) for your own results and [SUBMISSION.md](SUBMISSION.md) for the structure and rubric. The executable commands are in [TP-2026.md](TP-2026.md), with [EXTENSIONS-2026.md](EXTENSIONS-2026.md) for TP 11A.

## Phase 0: setup checklist

- [ ] Both containers run and I can identify the target/client/laptop contexts.
- [ ] I know when to use root and when a test must run as Alice, Bob or student.
- [ ] I checked the tools, target name resolution and relevant port mapping.
- [ ] I saved a small file under /artifacts and found it on the laptop.
- [ ] I know the recovery console and the difference between restart and recreation.
- [ ] I read the worked report example and know the phases assigned to me.

Record platform details and any setup problem. Phase 0 is a readiness check, not a scored hardening result.

# Phase map

| Phase | Original concept | TP reference | Explain / practice / review |
|---|---|---|---|
| 0 | Mission, setup and deliverables | README / setup checklist | 15 / 15–20 / 5 min |
| 1 | Understanding the threat surface | 1 | 20 / 20 / 5 min |
| 2 | Accounts and sudo | 2 | 20 / 25 / 5 min |
| 3 | PAM: Pluggable Authentication Modules | 3: server-fingerprint through password-recovered | 20 / 25 / 5 min |
| 4 | SSH: keys over passwords | 3: install-keys through unauthorized-group-refused | 20 / 30 / 5 min |
| 5 | SUID and SGID | 4 | 20 / 30 / 5 min |
| 6 | umask: default permissions | 6: practical steps in EXERCISES.md | 10 / 15 / 5 min |
| 7 | ACL: Access Control Lists | 7: practical steps in EXERCISES.md | 15 / 25 / 5 min |
| 8 | fstab and mount options | 8: practical steps in EXERCISES.md | 20 / 25 / 5 min |
| 9 | Remote access restrictions | 9: practical steps in EXERCISES.md | 15 / 20 / 5 min |
| 10 | Host firewall with nftables | 10: practical steps in EXERCISES.md | 20 / 35 / 5 min |
| 11 | Rate limits, connection caps and Fail2ban | 11: practical steps in EXERCISES.md | 30 / 60 / 5 min |
| 12 | Updates and baseline hygiene | 12: practical steps in EXERCISES.md | 20 / 25 / 5 min |
| 13 | Chroot | 13: practical steps in EXERCISES.md | 20 / 35 / 5 min |
| 14 | AIDE: file integrity monitoring | 14: practical steps in EXERCISES.md | 20 / 30 / 5 min |
| 15 | osquery | 15: practical steps in EXERCISES.md | 20 / 35 / 5 min |

<!-- PAGEBREAK -->

# Phase 1: Understanding the threat surface

**Why:** We cannot choose sensible hardening controls without knowing what is present and needed.

**Goal:** Build an initial inventory and justify what to keep, restrict or investigate.

**Practice:** about 20 minutes. Follow the short task instructions below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Use the target container. Record the listening services and running processes with the tools introduced in the slides. Choose two entries, identify their purpose if possible and decide whether to keep, restrict or investigate them. Do not change configuration in this phase.

### Required evidence — attach every item

- `evidence/phase-01/phase-01-evidence.txt` — listeners, processes and two documented findings; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 1.1 Prediction

Before the inventory, name one service you expect and one detail you will check.

### 1.2 Decision

Choose two observed services or processes. State their purpose if known and whether you recommend keeping, restricting or investigating each. Do not change the configuration.

### 1.3 Evidence

Attach every file in the Required evidence list. For each observation, identify the command, target/user context and relevant output.

### 1.4 Interpretation

What did the inventory establish? Give one justified next action and one thing the inventory cannot prove.

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 2: Accounts and sudo

**Why:** Limit the authority available after one account is compromised.

**Goal:** Give Alice an administrative role and prove Bob does not have it.

**Practice:** about 25 minutes. Follow the short task instructions below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Use the supplied Alice and Bob accounts on the target. Check their identities and group membership, inspect and validate the lab sudo rule, then run the same administrative check as each account. Record which action succeeds and which is refused.

### Required evidence — attach every item

- `evidence/phase-02/phase-02-evidence.txt` — account identities, validated sudo rule, Alice and Bob test results; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 2.1 Prediction

Before testing, predict whether Alice’s administrative command will succeed and whether Bob’s will succeed.

### 2.2 Decision

Describe the lab’s admin group and sudo rule. State which account should be able to administer the target.

### 2.3 Evidence

Attach every file in the Required evidence list. Include both account identities, the sudo rule and the results of the same command as Alice and Bob.

### 2.4 Interpretation

Explain how the account roles produced the observed results. State one limit of this lab’s broad admin role.

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 3: PAM: Pluggable Authentication Modules

**Why:** Services need a consistent way to combine credential, account and session policy.

**Goal:** Observe password success, repeated failures, lockout and recovery.

**Practice:** about 25 minutes. Follow the short task instructions below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Use the target account and SSH client from the TP. Confirm the server fingerprint first. Test a successful login, make the configured number of failed attempts, retry the correct password while locked, inspect the counter/log, reset the test lock and confirm login works again.

### Required evidence — attach every item

- `evidence/phase-03/phase-03-evidence.txt` — PAM settings, initial login, lockout attempt, counter and recovery result; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 3.1 Prediction

Before the failed-login test, predict the result for a correct password before and after the configured failure threshold.

### 3.2 Decision

Describe the PAM rule that counts failures and the configured lockout and recovery settings.

### 3.3 Evidence

Attach every file in the Required evidence list. Include the initial successful login, failed attempts, correct-password attempt while locked, counter/reset and successful recovery.

### 3.4 Interpretation

Explain why the correct password was refused while the account was locked. State one benefit and one risk of lockout.

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 4: SSH: keys over passwords

**Why:** Remove password guessing as an SSH login path and verify the remote server.

**Goal:** Verify key-only access for the authorized account.

**Practice:** about 30 minutes. Follow the short task instructions below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Use the target and client consoles. Verify the target fingerprint, install and test Alice’s SSH key, then apply the key-only and account policy from the lecture. Test Alice’s key, a password login and the student key. Keep the root recovery console open and never include private keys or passwords in your report.

### Required evidence — attach every item

- `evidence/phase-04/phase-04-evidence.txt` — public fingerprints, active SSH settings, validation and redacted login results; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 4.1 Prediction

After the SSH policy change, predict the result for Alice’s key, a password attempt and the student key.

### 4.2 Decision

Describe how you installed the key, verified the target fingerprint and applied the SSH policy.

### 4.3 Evidence

Attach every file in the Required evidence list. Include public fingerprints, effective SSH settings and all three login results. Do not submit private keys or passwords.

### 4.4 Interpretation

Explain each observed result. Identify which policy or identity explains each refusal.

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 5: SUID and SGID

**Why:** Privileged executables can turn a local flaw into wider authority.

**Goal:** Inventory privileged files and close the deliberate SUID path.

**Practice:** about 30 minutes. Follow the short task instructions below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

On the target, inventory SUID/SGID files and file capabilities. Inspect the lab-created shroot file and its parent directory. As the ordinary student user, run the same shroot check before and after correcting only the unnecessary lab permissions. Do not remove SUID from system tools such as sudo or passwd.

### Required evidence — attach every item

- `evidence/phase-05/phase-05-evidence.txt` — SUID/capability inventory, permissions before and after, same-user test results; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 5.1 Prediction

Predict the effective UID when student runs the lab’s shroot command before and after the fix.

### 5.2 Decision

Identify the lab-created file or directory you changed and explain why that change is limited to the unnecessary privilege.

### 5.3 Evidence

Attach every file in the Required evidence list. Include the privileged-file inventory, ownership/modes and the same before/after test run as the ordinary student user.

### 5.4 Interpretation

State what the test proves and what it does not prove about the account’s other administrative access.

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 6: umask: default permissions

**Why:** New files should not expose more access than their purpose requires.

**Goal:** Predict and verify creation modes before introducing default ACLs.

**Practice:** about 15 minutes. Follow the short task instructions below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

On the target, note the current umask. In a fresh temporary directory, set umask 027, create a new file and directory, and record their modes. Try umask 077 and record one new file. Restore the original umask and directory before continuing.

### Required evidence — attach every item

- `evidence/phase-06/phase-06-evidence.txt` — original and test umask values, fresh file/directory modes, restored value; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 6.1 Prediction

Predict the modes of a new file and directory when the shell uses umask 027.

### 6.2 Decision

Explain where you set the umask for this test and why the test must use newly created files.

### 6.3 Evidence

Attach every file in the Required evidence list. Include the original/restored mask, creation commands and actual modes for a fresh file and directory.

### 6.4 Interpretation

Explain which permission bits the mask removed. State why changing umask does not change an existing file.

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 7: ACL: Access Control Lists

**Why:** Represent a read-only auditor alongside a writing project role.

**Goal:** Make Alice's new report readable but not writable by Bob.

**Practice:** about 25 minutes. Follow the short task instructions below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Use the target’s Alice and Bob accounts. Configure the project group and the access/default ACLs shown in the lecture. Have Alice create a report. In a fresh Bob session, test reading and modifying it, then inspect the directory and report ACLs.

### Required evidence — attach every item

- `evidence/phase-07/phase-07-evidence.txt` — project and file ACLs, Alice creation, Bob read/write test results; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 7.1 Prediction

Before testing, predict whether Bob can read and modify a report created by Alice in the project directory.

### 7.2 Decision

Describe the project group, SGID bit and ACL entries you configured.

### 7.3 Evidence

Attach every file in the Required evidence list. Include directory/new-file ACLs, Alice’s creation, and Bob’s read and refused-write results from a fresh Bob session.

### 7.4 Interpretation

Explain how SGID, the default ACL and ACL mask produced the observed access.

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 8: fstab and mount options

**Why:** Restrict particular execution and device/privilege behavior on writable filesystems.

**Goal:** Demonstrate noexec, its interpreter limitation and policy restoration.

**Practice:** about 25 minutes. Follow the short task instructions below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Complete these steps in the target container's root console. Mount changes apply only to the disposable container. Do not edit the host fstab.

1. Inspect `/tmp`'s active mount options and record them.
2. Make sure `noexec` is absent. If it is present, remount `/tmp` with execution enabled, then verify the option is gone.
3. Create a small shell script in `/tmp` that prints a message. Make it executable, run it directly by its path, and record the result.
4. Remount `/tmp` with `noexec`, verify the option is present, and try the same direct execution again. Record the result.
5. Without moving or changing the script, run it through a shell interpreter. Record the result and explain why this still works.
6. Leave `noexec` enabled, verify it is restored, and remove the test script.

### Required evidence — attach every item

- `evidence/phase-08/phase-08-evidence.txt` — mount options, both direct-execution results, interpreter result, and final `noexec` check; include target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 8.1 Prediction

Predict what will happen when you run the script directly before and after enabling `noexec`. Then explain how the interpreter ran it while `noexec` remained enabled.

### 8.2 Decision

State whether `noexec` was initially present, what remounts you performed, and how you verified the final lab setting.

### 8.3 Evidence

Attach every file in the Required evidence list. Include mount options and results from both direct-execution attempts, the interpreter run, and the final restoration check.

### 8.4 Interpretation

Explain what `noexec` blocks and why the script can still be run through an interpreter.

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 9: Remote access restrictions

**Why:** A valid credential should only work within the intended source/account policy.

**Goal:** Isolate source authorization before adding packet filtering.

**Practice:** about 20 minutes. Follow the short task instructions below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Complete these steps before Phase 10. Use the target root console for configuration and keep it open for recovery.

1. In the target's root console, identify the approved client's IPv4 address and record it. Keep this console open throughout the test.
2. Configure sshd to allow Alice to connect only from that approved address. Validate the configuration before reloading sshd. If validation reports an error, correct the configuration before continuing.
3. From the approved client, connect as Alice using the existing lab key. Record the result; the connection should succeed. Do not change the account or key between tests.
4. From the laptop terminal, at the root of the student repository, run the following command to start a temporary second client. It transfers the same lab key and known-host record directly between containers, prints the second client's address, and attempts the same SSH connection:
   ```bash
   docker compose exec -T client tar -C /root/.ssh -cf - labkey known_hosts |
     docker compose run --rm -T --no-deps client bash -ec '
       mkdir -p /root/.ssh
       tar -xf - -C /root/.ssh
       chmod 600 /root/.ssh/labkey
       ip -4 -o addr show eth0
       ssh -i /root/.ssh/labkey -o BatchMode=yes -o ConnectTimeout=3 alice@target true
     '
   ```
   The second connection should be refused by sshd and return exit status `255`. Record the second client's address and result. Because the approved connection succeeded with the same key, this comparison tests the source rule. The key stays inside the disposable containers; do not copy it to the laptop or attach it to your report.
5. Compare the two client addresses and connection results. Explain why changing the source address changes the outcome while the account and key remain the same.
6. Leave the allowlist in place for the next phase and confirm the approved client can still connect.

### Required evidence — attach every item

- `evidence/phase-09/phase-09-evidence.txt` — approved client IP, validated SSH source policy, both client addresses, and same-key results from both clients; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 9.1 Prediction

Predict whether Alice’s same valid key will work from the approved and the other client after the source allowlist.

### 9.2 Decision

Describe the account/source rule and why the root recovery console stayed open.

### 9.3 Evidence

Attach every file in the Required evidence list. Include effective SSH policy, both source addresses, and same-key results before the firewall phase. Do not attach the private key.

### 9.4 Interpretation

Identify the layer that refused the other-source connection. State one reason the approved client address may change.

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 10: Host firewall with nftables

**Why:** Keep network exposure aligned with the services and clients the host needs.

**Goal:** Prove source-specific filtering, persistence and required DNS behavior.

**Practice:** about 35 minutes. Follow the short task instructions below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Use the target and two clients. Apply an nftables policy that allows the lab SSH and HTTP traffic from the approved client and refuses HTTP from the other client. Check the rules and counters, save the lab policy, restart the target, then recheck SSH, DNS and the saved policy. Do not flush the full ruleset.

### Required evidence — attach every item

- `evidence/phase-10/phase-10-evidence.txt` — firewall rules/counters, client tests, restart, DNS and saved-policy checks; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 10.1 Prediction

Predict the SSH and HTTP results from the approved client and the HTTP result from the other client after filtering.

### 10.2 Decision

Describe the allowed flows, denied flow, rule order and how you preserved Docker’s networking rules.

### 10.3 Evidence

Attach every file in the Required evidence list. Include rules/counters, client tests, saved policy, post-restart SSH and DNS checks.

### 10.4 Interpretation

Explain what persisted after restart and how the evidence distinguishes filtering from a stopped service.

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 11: Rate limits, connection caps and Fail2ban

**Why:** Constrain excessive activity without confusing an event threshold with malicious intent.

**Goal:** Compare rate and concurrency, then prove a log-driven ban and recovery.

**Practice:** about 60 minutes. Follow the short task instructions below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Complete both parts of this phase. In 11A, test the per-source HTTP rate limit and SSH connection cap from the client containers. In 11B, generate the configured number of 404 requests, check the ban state, verify a blocked request, then unban and confirm recovery. Stop the temporary service and restore the lab firewall table.

### Required evidence — attach every item

- `evidence/phase-11/phase-11-evidence.txt` — rate/cap tests, Fail2ban match and threshold checks, ban and recovery tests; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 11.1 Prediction

Predict the third simultaneous SSH connection, the rate-limited HTTP request, and the result after the sixth matching 404.

### 11.2 Decision

Describe what the rate meter, connection cap and Fail2ban jail count in this lab.

### 11.3 Evidence

Attach every file in the Required evidence list. Include 11A allowed/refused tests and counters; for 11B include matched events, fifth/sixth-event state, blocked request and successful recovery.

### 11.4 Interpretation

Explain what the ban proves and one reason a legitimate client could be affected.

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 12: Updates and baseline hygiene

**Why:** Reduce exposure to known flaws while verifying operational continuity.

**Goal:** Inspect actual update policy/actions and preserve maintenance evidence.

**Practice:** about 25 minutes. Follow the short task instructions below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

On the target, record package state, refresh package metadata and apply available updates. Configure the security update origin and periodic policy, inspect the effective settings, run the dry run and test then release a package hold. Compare package state and history. This container does not prove that systemd timers or host reboot behavior work.

### Required evidence — attach every item

- `evidence/phase-12/phase-12-evidence.txt` — update policy, package state before/after, actions, dry run and history; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 12.1 Prediction

State what a package-list refresh, upgrade and unattended-upgrade dry run will show.

### 12.2 Decision

Describe the allowed update origin and the maintenance policy you configured.

### 12.3 Evidence

Attach every file in the Required evidence list. Include package lists before/after, effective policy, dry-run output and package history.

### 12.4 Interpretation

State what the container run proves and what it cannot prove about automatic scheduling or a real host reboot.

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 13: Chroot

**Why:** Narrow a service's filesystem view and run it with limited ordinary authority.

**Goal:** Observe the same service from inside and outside its jail.

**Practice:** about 35 minutes. Follow the short task instructions below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

On the target, create the prepared jail and run the static web service under its dedicated account. From the client, request the page. Inspect the running process UID and root path, then test which files are visible and writable inside and outside the jail. Stop the test service when finished.

### Required evidence — attach every item

- `evidence/phase-13/phase-13-evidence.txt` — HTTP response, service identity and inside/outside jail path checks; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 13.1 Prediction

Predict what path the service sees as / and whether /etc is available inside the prepared jail.

### 13.2 Decision

Describe the service account, jail root and read-only files used for the test.

### 13.3 Evidence

Attach every file in the Required evidence list. Include HTTP response, process PID/UID/root path and inside/outside read/write tests.

### 13.4 Interpretation

State what the jail restricts and two protections it does not provide.

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 14: AIDE: file integrity monitoring

**Why:** Detect meaningful file changes and investigate them before accepting a new state.

**Goal:** Compare a protected baseline, controlled change and reviewed new baseline.

**Practice:** about 30 minutes. Follow the short task instructions below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

On the target, initialize an AIDE baseline for the configured /etc scope and confirm a clean check. Make the documented harmless change, run the check again and inspect the reported difference and exit status. Review the change before accepting it; then update and verify the baseline.

### Required evidence — attach every item

- `evidence/phase-14/phase-14-evidence.txt` — clean and changed AIDE checks, reviewed difference and final baseline check; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 14.1 Prediction

Predict the initial AIDE check and the check after the documented /etc/hosts change.

### 14.2 Decision

Describe the paths/properties monitored and how you decide whether a difference is expected before updating the baseline.

### 14.3 Evidence

Attach every file in the Required evidence list. Include the clean, changed and reviewed checks, status and relevant diff.

### 14.4 Interpretation

Explain why AIDE reports a difference and why a clean result does not prove the whole host is unchanged.

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 15: osquery

**Why:** Make the initial audit repeatable and connect separate observations through structured queries.

**Goal:** Investigate listeners, privileged files and process state after the earlier controls.

**Practice:** about 35 minutes. Follow the short task instructions below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Run the pinned osquery version on the target. Inspect the schema, collect the requested listener, user, system, privileged-file and process results as JSON, then compare one result with ss, ps or find. Finish with a short risk-delta note tied to evidence from earlier phases.

### Required evidence — attach every item

- `evidence/phase-15/phase-15-evidence.txt` — osquery version/schema, JSON query results and comparison with system tools; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 15.1 Prediction

Before running osquery, name one listener/process relation you expect to find.

### 15.2 Decision

State which query you used to inspect that finding and which native command you used to corroborate it.

### 15.3 Evidence

Attach every file in the Required evidence list. Include osquery version/schema, JSON results and one corroborating command/output.

### 15.4 Interpretation

Compare one actual finding with an earlier phase. State one scope or timing limit of the result.

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->
