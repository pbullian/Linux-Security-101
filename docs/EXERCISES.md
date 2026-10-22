# Student exercises in the original phase order

## The mission and why we start with an audit

You administer a small Linux server that must remain usable for approved work. First understand its threat surface: what an attacker can touch or interact with. Inventory what is running, why it is needed, who can reach it and which identity runs it. Then restrict unnecessary access, maintain software and detect changes through the later phases.

Phase 1 establishes the before-state. You are not asked to invent vulnerabilities or stop every service. Record observations, justified recommendations and questions needing another test. Later phases must show the effect and limits of the control you changed.

## What you do and submit

After a short explanation, complete the matching TP before moving to the next phase. Use the original phase numbers throughout your report. Follow the numbered steps in this document and use the lecture examples to choose your own commands. Phase 11 has two practical blocks, 11A and 11B, within the same phase.

Submit one ZIP with report.md, manifest.json and linked evidence files. For each assigned phase, answer four short questions: prediction, decision, evidence and interpretation. Attach every item in that phase’s Required evidence list. Record the command, target and user, expected and actual results, and exit status when relevant. Finish with a risk-delta note of at most 200 words.

Read [REPORT-EXAMPLE.md](REPORT-EXAMPLE.md) before starting. It shows a complete Phase 1 entry with explicitly fictional evidence. Use [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md) for your own results and [SUBMISSION.md](SUBMISSION.md) for the structure and rubric. Each phase below specifies where to work, what to change, what to test and what evidence to keep. Command blocks are provided for Docker operations and test setup, such as starting a temporary server; the security configuration and investigation are your work. Save the relevant output together in the single evidence file listed for each phase.

## Phase 0: setup checklist

1. Follow the [README setup](../README.md#get-started) to build and start the target and client. Record your platform and Docker version.
2. Open separate target and client consoles from laptop terminals in the repository directory:
   ```bash
   docker compose exec target bash
   ```
   ```bash
   docker compose exec client bash
   ```
3. Identify the laptop, target and client terminals. Confirm that the container consoles run as root. Keep the target root console open as your recovery path.
4. From the client, check its IPv4 address and confirm that the name `target` resolves. On the target, check that SSH is listening and its configuration is valid.
5. Create a small evidence file in the target's `/artifacts` directory and confirm that it appears in the laptop's `artifacts` directory.
6. Read [REPORT-EXAMPLE.md](REPORT-EXAMPLE.md), identify the assigned phases and prepare your report. Keep one evidence text file per phase; include relevant output rather than screenshots of every action.
7. Distinguish a container restart, which preserves configuration, from deleting and recreating containers, which resets your work. Keep the same containers through the phases.

Alice and Bob are created in Phase 2. After that, use these Docker commands from the laptop when a step requires a fresh ordinary-user session. Keep each session in a separate terminal and check its identity before testing:

```bash
docker compose exec --user alice target bash
```
```bash
docker compose exec --user bob target bash
```
```bash
docker compose exec --user student target bash
```

Record platform details and any setup problem. Phase 0 is a readiness check, not a scored hardening result.

# Phase map

| Phase | Concept | Explain / practice / review |
|---|---|---|
| 0 | Mission, setup and deliverables | 15 / 15–20 / 5 min |
| 1 | Understanding the threat surface | 20 / 20 / 5 min |
| 2 | Accounts and sudo | 20 / 25 / 5 min |
| 3 | PAM: Pluggable Authentication Modules | 20 / 25 / 5 min |
| 4 | SSH: keys over passwords | 20 / 30 / 5 min |
| 5 | SUID and SGID | 20 / 30 / 5 min |
| 6 | umask: default permissions | 10 / 15 / 5 min |
| 7 | ACL: Access Control Lists | 15 / 25 / 5 min |
| 8 | fstab and mount options | 20 / 25 / 5 min |
| 9 | Remote access restrictions | 15 / 20 / 5 min |
| 10 | Host firewall with nftables | 20 / 35 / 5 min |
| 11 | Rate limits, connection caps and Fail2ban | 30 / 60 / 5 min |
| 12 | Updates and baseline hygiene | 20 / 25 / 5 min |
| 13 | Chroot | 20 / 35 / 5 min |
| 14 | AIDE: file integrity monitoring | 20 / 30 / 5 min |
| 15 | osquery | 20 / 35 / 5 min |

<!-- PAGEBREAK -->

# Phase 1: Understanding the threat surface

**Why:** We cannot choose sensible hardening controls without knowing what is present and needed.

**Goal:** Build an initial inventory and justify what to keep, restrict or investigate.

**Practice:** about 20 minutes. Follow the numbered steps below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Work in the target root console. This phase records the starting state; do not change services or permissions.

1. List the listening network services. Record their addresses, ports and associated processes.
2. List the running processes and the users that own them. Identify which process is PID 1 in this container.
3. Choose two observations from your lists. For each, identify the service or process, its likely purpose and the identity under which it runs.
4. For a network listener, explain which interface it uses and which clients might reach it. Distinguish listening inside the container from publishing a port on the laptop.
5. Recommend keeping, restricting or investigating each selected entry. Support each recommendation with an observation and one question you would need to check next.
6. Save the relevant listener/process output and your two findings in the Phase 1 evidence file. Keep this baseline for the final comparison.

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

**Practice:** about 25 minutes. Follow the numbered steps below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Work in the target root console for setup, then use separate ordinary-user consoles for the tests. This is where you create the accounts used in later phases.

1. Check whether `alice`, `bob` and the `admin` group already exist. On a fresh lab, create the group and both accounts with home directories and Bash shells. Add Alice to `admin`; keep Bob outside administrative groups.
2. Set disposable lab passwords for Alice and Bob so that you can test sudo and SSH. Keep them available for Phase 3, but do not include them in the report.
3. Lock password login for root. Keep the Docker root console open for recovery; locking the password does not close this console.
4. Create a sudoers drop-in for the `admin` group, using the lecture's administrative-role policy. Make it root-owned and readable only as appropriate for sudoers files. Validate the complete sudoers configuration and correct any errors before testing.
5. Open fresh Alice and Bob sessions using the Docker commands in Phase 0. Check each account's identity and group membership.
6. As Alice, use sudo for a harmless administrative check that reports the effective identity. Repeat exactly that check as Bob. Record both outcomes and the rule that explains them.
7. Save the identities, group memberships, validated sudo rule and test results. Keep both accounts for the following phases.

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

**Practice:** about 25 minutes. Follow the numbered steps below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Use the accounts from Phase 2. Keep the target root console open and perform SSH login attempts from the client.

1. On the target, read the existing ED25519 SSH host-key fingerprint. From the client, obtain the advertised host key and compare its fingerprint with the target's value. Only trust the client record after they match.
2. On the target, back up the PAM authentication and account files you will change. Apply the lab stack explained in the lecture: check the failure state before password authentication, count failed passwords, and enforce the account lock during account checks.
3. Configure a lock after five failures with a 900-second unlock time. Inspect the PAM module order and clear any previous failure state for Alice before starting the test.
4. From the client, make one successful password login as Alice. Force password authentication so an existing SSH key cannot bypass this test. End that session.
5. Make five separate attempts using an incorrect password. Use one password prompt per connection so each attempt is easy to count. Record the refusals.
6. On the target, inspect Alice's failure counter and the authentication log. From the client, try the correct password while the account is locked and record the outcome.
7. From the target root console, reset Alice's failure state. Confirm that the counter is cleared, then retry the correct password from the client.
8. Save the PAM settings, initial success, lockout evidence and recovered login. Leave Alice unlocked for Phase 4.

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

**Practice:** about 30 minutes. Follow the numbered steps below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Continue with the target and client from Phase 3. Keep the target root console open while changing SSH access.

1. Confirm that the client's trusted target host key matches the fingerprint checked in Phase 3.
2. In the client container, create an ED25519 lab key pair at `/root/.ssh/labkey` if it does not already exist. Keep the private key there. Record only its public fingerprint.
3. Install that public key for Alice and for the existing `student` account on the target. Check ownership and permissions of their SSH directories and authorized-key files.
4. From the client, verify key authentication for both accounts before applying the account restriction. Disable password fallback for these tests so success proves the key works.
5. On the target, apply the lecture's SSH policy: allow public keys, disable password and keyboard-interactive authentication, refuse root login and restrict access to the `admin` group. Keep the lecture's limits of two authentication attempts and a 30-second login grace period.
6. Validate the SSH configuration before reloading it. Inspect the effective settings to confirm that another configuration file has not overridden your policy. In this container, sshd is PID 1; use its reload mechanism from the lecture, not a systemd service command.
7. From the client, test Alice's key again. Then test a password-only login as Alice and a key login as `student`. Record all three results and inspect the target authentication log to explain each refusal.
8. Keep Alice's working key and the client's trusted host record for the later network phases. Save public fingerprints, effective settings, validation and login results; never include the private key.

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

**Practice:** about 30 minutes. Follow the numbered steps below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Inspect and change permissions from the target root console, but run the privilege tests as the ordinary `student` user.

1. Inventory SUID and SGID files on the target filesystem, then inventory file capabilities. Record ownership and modes for the lab-created files you identify.
2. Inspect `/opt/labtools/shroot` and its parent directory. Explain who can execute the file and who can change files in the directory.
3. In a fresh `student` session, run the lab shell with the privilege-preservation option explained in class. Use it for a harmless check of the process's effective identity. Record the result without invoking sudo.
4. From the target root console, remove the unnecessary SUID permission from the deliberate lab copies you found and restrict writes to their directory. Do not remove SUID indiscriminately from legitimate system tools.
5. Return to the same ordinary-user context and repeat the exact test from step 3. Record the new effective identity and the file/directory permissions after the fix.
6. Compare before and after. Explain what this proves about the tested SUID path and why it does not remove the `student` account's separate sudo rights.

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

**Practice:** about 15 minutes. Follow the numbered steps below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Work in one target console and keep using that same shell throughout the experiment.

1. Record your user, current directory and current umask so you can restore the original shell settings.
2. Create a fresh test directory under `/tmp` with no default ACL, and work inside it. Use new names for every file and directory in this exercise.
3. Set the current shell's umask to `027`. Predict the permissions for a newly created ordinary file and directory, then create both and inspect their actual modes.
4. Change the shell's umask to `077` and create another ordinary file. Inspect its mode and compare it with the first file.
5. Inspect the first file again. Explain whether changing the umask affected that existing file.
6. Restore your original umask and working directory. Verify the restored value and save the masks and observed modes in one evidence file.

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

**Practice:** about 25 minutes. Follow the numbered steps below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Use the Alice and Bob accounts from Phase 2. Configure permissions in the target root console; test access as the named ordinary user.

1. Create the `auditors` group if necessary and add Bob to it. Confirm that Alice belongs to `admin` and Bob does not. Reopen Bob's session after changing his groups.
2. Create `/srv/project` with group `admin`. Give the owner and project group full directory access, exclude other users, and set SGID so new entries inherit the project group.
3. Apply an access ACL giving `admin` full directory access and `auditors` read/traverse access without write access. Check that the ACL mask permits the intended group permissions.
4. Add a default ACL to the directory with the same project and auditor roles, so new entries inherit the intended access. Inspect both the access and default ACLs.
5. As Alice, create a text file named `/srv/project/report` and a subdirectory. Inspect their group ownership, modes and inherited ACLs.
6. In a fresh Bob session, verify that `auditors` appears in his groups. Try reading the report and then appending text to it. Record both results without using sudo.
7. Explain how the directory SGID bit, inherited ACL and effective mask account for the results. Keep the report in place: later HTTP exercises serve this file.

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

**Practice:** about 25 minutes. Follow the numbered steps below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

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

**Practice:** about 20 minutes. Follow the numbered steps below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

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

**Practice:** about 35 minutes. Follow the numbered steps below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Use the Phase 9 target and approved client. Keep the target root console open for recovery. Alice's key and SSH source rule must already work; `/srv/project/report` comes from Phase 7.

1. Record the approved client's current IPv4 address. Confirm that Alice can still connect from that client using the lab key.
2. Start a temporary HTTP server on the target to serve the project directory on port `8080`. Run this setup command in the **target root console**, after checking that the port is free:
   ```bash
   python3 -u -m http.server 8080 --bind 0.0.0.0 --directory /srv/project > /tmp/http8080.log 2>&1 &
   echo $! > /run/http8080.pid
   ```
   Confirm that the process is running and listening. From the approved client, request `http://target:8080/report` and record the response before filtering.
3. Open another **laptop terminal in the repository directory** and start a temporary second client:
   ```bash
   docker compose run --rm --no-deps client bash
   ```
   Keep this terminal open for the before/after comparison. Record its IPv4 address, verify it differs from the approved client's address, and request the same HTTP page. Both clients should reach HTTP before the new firewall is applied.
4. In the target root console, prepare a policy for the lab's `inet filter` table. Set the input chain's default policy to drop. Allow established/related traffic and loopback, then allow new TCP connections to SSH port `22` and HTTP port `8080` only from the approved IPv4 address. Add counters to the tested accept rules and final drop rule.
5. Validate and load your policy using the course's `nft-lab` helper. Use its load operation with your rule file; it replaces only the lab table. Do not flush the whole ruleset or replace Docker's DNS tables. Inspect the active rules and their order.
6. From the approved client, make fresh SSH and HTTP connections. From the second client, repeat the HTTP request with a short timeout. Record all results, then inspect the target's counters. Confirm that the server is still listening so a failed request cannot simply be explained by a stopped service.
7. From the target, verify that `archive.ubuntu.com` still resolves. Save only the lab policy using the helper's save operation and inspect `/etc/nftables-lab.conf`.
8. Restart the target from a **laptop terminal**, then wait for it to become ready:
   ```bash
   docker compose restart target
   docker compose up -d --wait --no-build
   docker compose exec target bash
   ```
   The last command reopens the root console closed by the restart. Inspect the active and saved firewall policy, test DNS again, and retry Alice's SSH login from the approved client.
9. Check whether the temporary HTTP server survived the restart. Start it again with the setup command in step 2, then repeat the two clients' HTTP tests. Record the difference between restoring a firewall policy and restarting an application.
10. Save the rules/counters, both source addresses, before/after tests and restart checks in one evidence file. Stop the temporary HTTP server using its recorded PID, then close the second-client shell; Docker removes that temporary client. Keep the saved firewall policy for the next phase.

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

**Practice:** about 60 minutes. Follow the numbered steps below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Complete both parts using the accounts, keys and report file from the earlier phases. Keep the target root console open. Use only the lab's `inet filter` table for your own rules; Fail2ban manages its own table separately.

### 11A. Compare simultaneous connections and connection rate

1. Record the current lab firewall policy, then use the lab helper's reset operation to prepare the isolated test. Keep the SSH account/source restriction from Phase 9. Confirm that Alice's key still works from the approved client.
2. Configure a per-source cap of two tracked SSH connections. Preserve established/related and loopback traffic. Place the excess-connection rejection before the rule that accepts new SSH traffic; include counters.
3. From the approved client, open two independent SSH connections as Alice and keep both active. Use separate client terminals if useful; open each from the laptop with:
   ```bash
   docker compose exec client bash
   ```
   Verify that both connections succeeded. Disable SSH connection sharing for this test. While both remain open, attempt a third connection from that same client address and record the result and target counters.
4. Close the first two sessions, allow their connection-tracking state to expire, and test again. Explain the difference between simultaneous connections and connections made over time.
5. Reset the lab table for the rate experiment. On the **target**, start the temporary HTTP service on port `8092`:
   ```bash
   python3 -u -m http.server 8092 --bind 0.0.0.0 --directory /srv/project > /tmp/meter-http.log 2>&1 &
   echo $! > /run/meter-http.pid
   ```
   Check that the approved client can request `http://target:8092/report` before adding the rate rule.
6. Configure a separate rate bucket for each IPv4 source: a burst of two new HTTP connections and a refill rate of two per minute. Reject excess new connections before accepting HTTP; keep established traffic working. Add counters.
7. From the approved client, make three separate HTTP connections promptly, before a token refills. Record each outcome and inspect the target counters. Avoid reusing one persistent HTTP connection.
8. From another laptop terminal, start a second client:
   ```bash
   docker compose run --rm --no-deps client bash
   ```
   Record its different address and request the same page once. Compare this result with the approved client's third request. Close the temporary client when finished.
9. Stop the port `8092` server using its recorded PID. Reset and save the lab table using the helper, then verify DNS still works. Keep the cap and rate evidence together for Phase 11.

### 11B. Count HTTP events, trigger a ban and recover

1. On the target, check that the earlier rate and cap rules are cleared. Start with an empty `/var/log/http-access.log` for this isolated test, and start the HTTP server on port `8090`:
   ```bash
   python3 -u -m http.server 8090 --bind 0.0.0.0 --directory /srv/project >> /var/log/http-access.log 2>&1 &
   echo $! > /run/http8090.pid
   ```
   Confirm that the approved client can request `http://target:8090/report` successfully.
2. Create a Fail2ban filter called `pyhttp-404`. It must extract the source address and match an HTTP access record with status `404`, once per request. A successful request and the separate error-description line must not match. Validate your filter against sample records before enabling the jail; keep sample events out of the live test log.
3. Configure the `pyhttp-404` jail for `/var/log/http-access.log`, file polling and TCP port `8090`. Use six matching events within 60 seconds, a 600-second ban and an nftables action. Reload or restart Fail2ban and confirm that the jail is active with no initial ban.
4. From the approved client, request five different nonexistent paths on port `8090`. Confirm five HTTP 404 responses. Inspect the filter match count and jail state on the target; check that the source is not yet banned and that the existing report page still works.
5. Within the same 60-second window, request a sixth nonexistent path. Allow the polling backend to process the log, then inspect the match count, jail ban list and firewall action. If the window expired while inspecting, reset the test state and repeat; do not treat expired events as a failed detector.
6. From the same client, request the known existing report page again. Record whether the connection is blocked, alongside the jail state. Distinguish an HTTP 404 response from a network refusal.
7. From the target root console, unban the test client's address. Retry the existing page and record recovery.
8. Stop and disable the test jail, stop the temporary HTTP server using its recorded PID, and reset/save the lab firewall table. Verify DNS and normal client connectivity before Phase 12. Save the matched-event counts, fifth/sixth-event states, blocked test and recovered response in the Phase 11 evidence file.

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

**Practice:** about 25 minutes. Follow the numbered steps below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Work in the target root console after Phase 11 cleanup. The container needs DNS and access to Ubuntu package repositories.

1. Record the installed package versions before maintenance. Check DNS and repository connectivity if the package refresh fails.
2. Refresh package metadata and check that every required repository refresh succeeded. Inspect which upgrades are available before applying them.
3. Apply the available upgrades inside the disposable target. Preserve your intentional lab configuration when prompted, and record any reported problem. Record the resulting package versions; if no updates were available, state that explicitly.
4. Configure the unattended-upgrade policy to allow Ubuntu security updates. Set daily package-list refresh, download and unattended-upgrade intervals, with weekly cache cleanup.
5. Inspect the effective APT settings, including the allowed origins, rather than relying only on the file you edited. Run an unattended-upgrade dry run and save the relevant output.
6. Put the installed `vim` package on hold, verify the hold, then release it and verify that it is gone. Explain what a hold postpones.
7. Compare the before/after package state with APT history. Check that SSH still works and save the policy, actual maintenance results, dry run and hold/release evidence.
8. State what you demonstrated manually. This container does not run systemd timers, so it does not demonstrate automatic scheduling or reboot handling.

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

**Practice:** about 35 minutes. Follow the numbered steps below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Work in the target root console for setup and use the approved client for the HTTP test. Phase 11 cleanup should have removed the earlier restrictive test rules.

1. Create `/srv/jail` with `bin`, `www` and `tmp` subdirectories. Copy the installed static BusyBox binary into its `bin` directory. Give the temporary directory shared temporary-file permissions with the sticky bit.
2. Create a dedicated system account named `www-chroot` with no login shell, if it does not already exist. Record its UID and GID.
3. Create `/srv/jail/www/index.html` containing a short identifiable message. Keep the executable and static content owned by root and readable/executable as needed, with no write permission for the service account. Check the parent directories' permissions too.
4. Start the test server in the jail under the dedicated account. This is the **target-side server launch command**, after you have prepared the account and files:
   ```bash
   chroot --userspec="$(id -u www-chroot):$(id -g www-chroot)" /srv/jail /bin/busybox httpd -f -v -p 0.0.0.0:8091 -h /www > /tmp/jail-http.log 2>&1 &
   echo $! > /run/jail-http.pid
   ```
5. From the client, request `http://target:8091/` and verify your page is returned. On the target, inspect the live server PID, effective UID/GID and listener.
6. Inspect the process's filesystem root through `/proc`. Perform the root-path inspection as `www-chroot` if container root lacks the capability needed to read it. Record the outside path that corresponds to the service's root.
7. Open a test shell inside the jail using the same UID/GID and the static BusyBox shell. List its root, read the page, and test whether that identity can write to the executable or static page. Check whether `/etc` is present inside this minimal jail.
8. From that jailed shell, create a marker file in its `/tmp`. From the outside target console, locate the same file under `/srv/jail/tmp` and compare it with the target's own `/tmp`.
9. Stop the HTTP server using its recorded PID and confirm the listener is gone. Save the HTTP response, live identity/root path and file-access tests. Explain two resources or privileges that chroot alone does not isolate.

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

**Practice:** about 30 minutes. Follow the numbered steps below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Work in the target root console after the earlier configuration changes are complete.

1. Configure AIDE to monitor `/etc` using the lecture's rule for permissions, inode/link information, owner/group, size, timestamps and SHA-256. Explicitly exclude `/etc/mtab`, `/etc/ld.so.cache` and `/etc/resolv.conf` for this lab, and note that excluded paths are not checked.
2. Configure separate current and newly generated database files under `/var/lib/aide`. Initialize the baseline from the reviewed current state and install it as the active database with root-only access.
3. Run a comparison immediately, without changing monitored files. Record the clean result and AIDE's own exit status.
4. Append one harmless comment to `/etc/hosts`, leaving all existing mappings intact. Record the exact change and why you made it.
5. Compare again. Save the changed-file report and AIDE's exit status, taking care to record AIDE's status rather than an output-copying tool's status.
6. Review the reported path and changed attributes against your deliberate edit. Explain the difference before accepting it; investigate any additional unexpected changes.
7. Once the classroom change is accounted for, create and install a new baseline with the same protected permissions. Run another comparison and record the result.
8. Save the initial clean check, deliberate edit, detected difference and final check together. Explain one limit of the monitored scope and why an unexplained difference must not be silently accepted.

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

**Practice:** about 35 minutes. Follow the numbered steps below. Use the commands and concepts explained in class; choose your own safe way to complete the checks.

Work in the target root console. Keep Phase 1's inventory and Phase 5's permission evidence available for comparison.

1. Install the course-pinned osquery release using the supplied installer helper described in the lecture. Record the actual installed version and confirm installation succeeded before querying.
2. Inspect the schemas for the tables you will use, including `kernel_info`, `file`, `listening_ports` and `processes`. Use column names from the installed version.
3. Write queries returning listeners and their owning processes: include listening address/port, PID, process name and command line. Add a query that selects listeners owned by processes with effective UID zero.
4. Query the local users, recorded login sessions, OS/kernel information, uptime and non-loopback interface addresses. Explain empty session results or observations that refer to the shared Docker host/VM.
5. Query the SUID inventory. Then use a path-constrained file query to inspect the modes of `/usr/bin/sudo` and `/opt/labtools/shroot`. Compare the latter with your Phase 5 evidence.
6. Query the ten processes with the largest resident memory usage, including PID, name and resident size. Choose one finding from this phase to investigate further.
7. Check that finding with an independent native tool introduced in class. Record both observations and explain any difference in scope or timing.
8. Save the relevant schemas, queries and JSON results together in the Phase 15 evidence text file; separate JSON attachments are not required. Finish your report with at most 200 words on what changed since Phase 1, which legitimate actions still work and what remains outside the lab's protection.

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
