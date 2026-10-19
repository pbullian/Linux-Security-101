# Student exercises in the original phase order

## The mission and why we start with an audit

You administer a small Linux server that must remain usable for approved work. First understand its threat surface: what an attacker can touch or interact with. Inventory what is running, why it is needed, who can reach it and which identity runs it. Then restrict unnecessary access, maintain software and detect changes through the later phases.

Phase 1 establishes the before-state. You are not asked to invent vulnerabilities or stop every service. Record observations, justified recommendations and questions needing another test. Later phases must show the effect and limits of the control you changed.

## What you do and submit

After a short explanation, complete the matching TP before moving to the next phase. Use the original phase numbers throughout your report. TP reference section numbers are locations for command blocks; the map below tells you which blocks to use. Phase 11 has two practical blocks, 11A and 11B, within the same phase.

Submit one ZIP with report.md, manifest.json and linked evidence files. For each assigned phase, answer five short questions: prediction, decision, evidence, interpretation and the teacher's scenario variant. Keep actual command/context/output, explain why the result matters, and state a limitation. Finish with a risk-delta note of at most 200 words.

Read [REPORT-EXAMPLE.md](REPORT-EXAMPLE.md) before starting. It shows a complete Phase 1 entry with explicitly fictional evidence. Use [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md) for your own results and [SUBMISSION.md](SUBMISSION.md) for the structure and rubric. The executable commands are in [TP-2026.md](TP-2026.md), with [EXTENSIONS-2026.md](EXTENSIONS-2026.md) for TP 11A.

## Phase 0: setup checklist

- [ ] Both containers run and I can identify the target/client/laptop contexts.
- [ ] I know when to use root and when a test must run as Alice, Bob or student.
- [ ] I checked the tools, target name resolution and relevant port mapping.
- [ ] I saved a small file under /artifacts and found it on the laptop.
- [ ] I know the recovery console and the difference between restart and recreation.
- [ ] I read the worked report example and know the assigned phases/scenarios.

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

**Commands:** TP reference 1. **Practice:** about 20 minutes.

### 1.1 Prediction

Before running commands, name one required service you expect and one threat-surface question you want to investigate.

### 1.2 Decision

Choose two meaningful observations. For each, state its purpose and a keep, restrict or investigate recommendation with a reason. Do not change configuration in this phase.

### 1.3 Evidence

Attach listener and process output. In a small findings table, identify the address/port or process, execution context, evidence path and question raised.

### 1.4 Interpretation

Explain one plausible risk, the assumption behind it and one next test. What does this inventory fail to establish?

### 1.5 Changed-condition scenario

Answer your teacher's assigned variant.

**Variant A:** You find an unfamiliar root-owned listener. Would you stop it immediately? What would you check first?

**Variant B:** A service listens on 0.0.0.0 inside a container whose published port is bound to laptop loopback. Is it necessarily reachable from the Internet? Explain the missing checks.

**Suggested evidence:**

- `evidence/phase-01/listeners.txt`
- `evidence/phase-01/processes.txt`
- `evidence/phase-01/findings.md`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 2: Accounts and sudo

**Why:** Limit the authority available after one account is compromised.

**Goal:** Give Alice an administrative role and prove Bob does not have it.

**Commands:** TP reference 2. **Practice:** about 25 minutes.

### 2.1 Prediction

Before testing, predict the effective UID of the administrative command for Alice and the result of Bob running the same command. State which role difference matters.

### 2.2 Decision

Explain the role/group and sudo policy you used. Why is it useful for this lab, and why might it be too broad for a real log reader?

### 2.3 Evidence

Provide both account identities, the sudoers fragment and syntax-check result, plus Alice's successful and Bob's refused tests. Record context and exit status.

### 2.4 Interpretation

Explain why Bob can know the correct password and still fail. Does locking root's password remove Alice's delegated administration? Discuss one mismatch or limitation in your results.

### 2.5 Changed-condition scenario

Answer your teacher's assigned variant.

**Variant A:** An auditor only needs to read selected application logs. Would you add them to admin? Propose a smaller change, an allowed test and a refused test.

**Variant B:** You remove Alice from the admin group, but an existing session still has old group credentials. Explain how you would verify revocation and deal with already-running access.

**Suggested evidence:**

- `evidence/phase-02/identities-and-baseline.txt`
- `evidence/phase-02/sudoers.txt`
- `evidence/phase-02/sudo-tests.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 3: PAM: Pluggable Authentication Modules

**Why:** Services need a consistent way to combine credential, account and session policy.

**Goal:** Observe password success, repeated failures, lockout and recovery.

**Commands:** TP reference 3: server-fingerprint through password-recovered. **Practice:** about 25 minutes.

### 3.1 Prediction

Predict a correct password before failures and after five failed attempts. What state changed?

### 3.2 Decision

Explain the PAM stack and the deny/unlock_time policy. What do preauth, authfail and the account call do in this lab?

### 3.3 Evidence

Save the relevant PAM files and threshold configuration, initial successful login, failure counter, refused correct-password attempt and reset and successful recovery evidence.

### 3.4 Interpretation

Why does a valid password not guarantee access? Explain one benefit and one risk of account lockout.

### 3.5 Changed-condition scenario

Answer your teacher's assigned variant.

**Variant A:** An attacker deliberately locks a legitimate administrator out. What would you investigate or change without simply removing all controls?

**Variant B:** A rule with sufficient is placed before the lockout check. Why must you inspect the whole stack?

**Suggested evidence:**

- `evidence/phase-03/pam-policy.txt`
- `evidence/phase-03/lockout-tests.txt`
- `evidence/phase-03/counter-and-recovery.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 4: SSH: keys over passwords

**Why:** Remove password guessing as an SSH login path and verify the remote server.

**Goal:** Verify key-only access for the authorized account.

**Commands:** TP reference 3: install-keys through unauthorized-group-refused. **Practice:** about 30 minutes.

### 4.1 Prediction

After the policy change, predict Alice's key, a password attempt and student's enrolled key.

### 4.2 Decision

Explain key installation, host verification and safe change order. Distinguish known_hosts from authorized_keys.

### 4.3 Evidence

Provide public fingerprints, relevant effective sshd settings, and all three final login results. Exclude private keys and passwords.

### 4.4 Interpretation

Explain each refusal. Why can a valid key fail, and why does changing a password not revoke a stolen SSH key?

### 4.5 Changed-condition scenario

Answer your teacher's assigned variant.

**Variant A:** Alice's enrolled private key is stolen. Would changing her password solve the problem? Propose credential revocation, evidence to inspect and one verification test.

**Variant B:** The key works for an admin account but not for another account with the same public key installed. Which authorization conditions and filesystem details would you verify before weakening SSH policy?

**Suggested evidence:**

- `evidence/phase-04/public-fingerprints-and-settings.txt`
- `evidence/phase-04/ssh-policy.txt`
- `evidence/phase-04/ssh-outcomes-redacted.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 5: SUID and SGID

**Why:** Privileged executables can turn a local flaw into wider authority.

**Goal:** Inventory privileged files and close the deliberate SUID path.

**Commands:** TP reference 4. **Practice:** about 30 minutes.

### 5.1 Prediction

Predict the effective UID when student runs the lab's shroot command before and after your proposed fix. Why would a root-run test fail to demonstrate this difference?

### 5.2 Decision

Justify the files and directory permissions you change. Explain why you do not remove SUID indiscriminately from every system tool.

### 5.3 Evidence

Attach the relevant inventory and ownership/modes, plus the exact same ordinary-user test before and after the change. Identify the tested process's effective UID.

### 5.4 Interpretation

What precisely did the fix prevent? The student account still has sudo for setup: how does that limit your conclusion?

### 5.5 Changed-condition scenario

Answer your teacher's assigned variant.

**Variant A:** Your scan also finds the legitimate sudo binary with SUID. Should you remove that bit too? State the information and tests needed before deciding.

**Variant B:** The SUID bits are removed, but the tools directory remains writable by everyone. What risk remains, and under what additional condition could it become privilege escalation?

**Suggested evidence:**

- `evidence/phase-05/suid-inventory.txt`
- `evidence/phase-05/modes-before-after.txt`
- `evidence/phase-05/same-user-tests.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 6: umask: default permissions

**Why:** New files should not expose more access than their purpose requires.

**Goal:** Predict and verify creation modes before introducing default ACLs.

**Practice:** about 15 minutes. Follow the practical steps below; they name the machine, user context and evidence to record.

### Practical steps

Run this in the **target container**, not on your laptop. From the cloned `Linux-Security-101` directory, start a target shell with `docker compose exec target bash`.

1. Record the current mask with `umask`. Predict the file and directory modes before changing it.
2. Paste this block into that same target shell. It uses a fresh temporary directory so a previous run cannot make an old file look like a new result.

```bash
lab_previous_umask=$(umask)
lab_previous_dir=$PWD
lab_test_dir=$(mktemp -d /tmp/umask.XXXXXX)
cd "$lab_test_dir"
umask 027
touch report.txt
mkdir project-dir
stat -c '%a %n' report.txt project-dir
umask 077
touch private.txt
stat -c '%a %n' private.txt
umask "$lab_previous_umask"
cd "$lab_previous_dir"
unset lab_previous_umask lab_previous_dir lab_test_dir
```

3. Save the commands and actual `stat` output as `evidence/phase-06/creation-modes.txt`. Explain the file and directory results using the requested modes, and state why an existing file would not change.
4. Confirm `umask` has returned to its original value before continuing to Phase 7. The test directory remains under `/tmp`; it is disposable lab data.

The demonstration assumes no default ACL on the new `/tmp` directory. A directory default ACL can add another creation rule.

### 6.1 Prediction

Predict new regular-file and directory modes under umask 027, with requested modes 0666 and 0777 and no default ACL.

### 6.2 Decision

Explain why you set the mask in the tested shell, and what a login-default change would affect.

### 6.3 Evidence

Attach the current mask, creation commands and modes of the fresh file and directory, with context.

### 6.4 Interpretation

Explain the observed permissions and a collaboration case where 027 is unsuitable.

### 6.5 Changed-condition scenario

Answer your teacher's assigned variant.

**Variant A:** A file already exists with mode 0666 when you run umask 027. What do you expect and how would you correct it?

**Variant B:** A long-running service still creates broadly accessible files after a login-default edit. What would you inspect?

**Suggested evidence:**

- `evidence/phase-06/creation-modes.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 7: ACL: Access Control Lists

**Why:** Represent a read-only auditor alongside a writing project role.

**Goal:** Make Alice's new report readable but not writable by Bob.

**Practice:** about 25 minutes. Follow the practical steps below; they name the machine, user context and evidence to record.

### Practical steps

Complete Phase 2 first so the target has Alice, Bob and the `admin` group. The base image creates only the `student` account. Then use the disposable **target container** and open a root setup shell from the cloned `Linux-Security-101` directory with `docker compose exec target bash`.

1. Run `id alice`, `id bob` and `getent group admin`; confirm all checks succeed. Predict the intended directory, report and Bob permissions before configuring them.
2. In the root target shell, prepare the project and auditor role:

```bash
getent group auditors >/dev/null || groupadd auditors
usermod -aG auditors bob
mkdir -p /srv/project
chgrp admin /srv/project
chmod 2770 /srv/project
setfacl -b -k /srv/project
```

3. Add an access ACL and a default ACL to `/srv/project` with `setfacl`. The requirement is: Alice can create and update reports; Bob, as an auditor, can read new reports but cannot change them. Use these command forms, then inspect the effective result:

```bash
setfacl -m g:admin:rwx,g:auditors:rx,m:rwx /srv/project
setfacl -d -m g:admin:rwx,g:auditors:rx,m:rwx /srv/project
getfacl -e /srv/project
```

The access ACL governs this directory now; the default ACL supplies entries to children created later. Capture `getfacl -e /srv/project` in `evidence/phase-07/project-acls.txt`.
4. From your laptop, open a new Alice console with `docker compose exec --user alice target bash`. At the new target prompt, create a fresh report and subdirectory, then inspect them:

```bash
printf 'reviewable report\n' > /srv/project/report
mkdir /srv/project/subdir
stat -c '%a %G %n' /srv/project/report /srv/project/subdir
getfacl -e /srv/project/report /srv/project/subdir
```

Copy the commands and output into your evidence file. If repeating the test, choose fresh names or remove only your named test objects first.
5. Exit Alice’s console. From your laptop, open a **fresh Bob target shell** with `docker compose exec --user bob target bash` so it receives the updated supplementary group. At the Bob prompt, run:

```bash
id
cat /srv/project/report
printf 'unapproved change\n' >> /srv/project/report
```

Record the actual read result and the write result, including the latter's exit status. The intended test is a successful read and refused write. Do not run the Bob checks as root. Save these results in `evidence/phase-07/alice-bob-access.txt`.
6. Explain the output: the directory's SGID bit affects group ownership; the default ACL affects new children; the ACL mask limits effective group-class access. A new regular file requested without execute bits does not become executable merely because the default ACL mentions execute.

After changing Bob's group membership, close any old Bob console and use the fresh one above. Existing processes keep their previous supplementary groups.

### 7.1 Prediction

Before testing, predict Alice's creation of a report, Bob's read and Bob's modification. What should be inherited?

### 7.2 Decision

Explain the project group, SGID directory bit, auditor ACL, default ACL and mask. Which mechanism applies to existing objects and which affects future creation?

### 7.3 Evidence

Attach creation modes and getfacl output for the directory and a new report. Show Alice creating content, Bob reading it, and Bob's refused modification in their own contexts.

### 7.4 Interpretation

Explain why Bob's read and write attempts differ and why the new regular file is not executable. Identify one way an existing object could differ from a newly created one.

### 7.5 Changed-condition scenario

Answer your teacher's assigned variant.

**Variant A:** An administrator runs chmod g-r on a file with an extended ACL. Bob's named/group entry still appears to include read permission, yet reading fails. What would you inspect and why?

**Variant B:** A new reviewer should read future reports but never modify them. How would you test both the role assignment and inheritance, including an already-existing report?

**Suggested evidence:**

- `evidence/phase-07/project-acls.txt`
- `evidence/phase-07/alice-bob-access.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 8: fstab and mount options

**Why:** Restrict particular execution and device/privilege behavior on writable filesystems.

**Goal:** Demonstrate noexec, its interpreter limitation and policy restoration.

**Practice:** about 25 minutes. Follow the practical steps below; they name the machine, user context and evidence to record.

### Practical steps

Run these checks in the **target container**, not on the laptop. From the cloned `Linux-Security-101` directory, open `docker compose exec target bash`.

1. Check which mount actually contains each temporary path:

```bash
for p in /tmp /var/tmp /dev/shm /home /var /var/log; do
  printf '%s: ' "$p"
  findmnt -T "$p" -no TARGET,OPTIONS
done
```

2. Predict what will happen, then create a harmless test binary and script in `/tmp`:

```bash
cp /bin/true /tmp/t
printf '#!/bin/sh\necho interpreted-script\n' > /tmp/s.sh
chmod +x /tmp/s.sh
set +e
/tmp/t; printf 'binary direct status=%s\n' "$?"
/tmp/s.sh; printf 'script direct status=%s\n' "$?"
bash /tmp/s.sh; printf 'bash interpreter status=%s\n' "$?"
```

With the lab's `noexec` mount, direct execution should be refused (usually status 126), while the explicit `bash` interpreter can read the script. Capture the printed status after each test.
3. Temporarily remount only the disposable container's `/tmp` with `exec`, prove `/tmp/t` now runs, then restore `noexec` and prove it is refused again:

```bash
mount -o remount,exec /tmp
/tmp/t; printf 'exec mount status=%s\n' "$?"
mount -o remount,noexec /tmp
/tmp/t; printf 'restored noexec status=%s\n' "$?"
```

4. Save `findmnt` output and all test results as `evidence/phase-08/`. Explain what `noexec` reduces and why it is not a script sandbox. Do not edit host `/etc/fstab` or apply the slide's example to your laptop. `docker-compose.yml` creates this lab's `/tmp` with `noexec,nosuid,nodev`; the exercise verifies that active mount, not boot-time persistence.

### 8.1 Prediction

Predict direct execution of the binary/script on noexec /tmp and explicit interpreter execution.

### 8.2 Decision

Explain the chosen mount flags, temporary exception and restoration. Why does this lab not verify fstab boot policy?

### 8.3 Evidence

Provide effective mount options, direct/interpreter outcomes, the temporary exec result and restored noexec refusal.

### 8.4 Interpretation

What risk did noexec reduce, and what remains possible? Why not bind /var/tmp to volatile /tmp blindly?

### 8.5 Changed-condition scenario

Answer your teacher's assigned variant.

**Variant A:** An installer requires executable temporary files. Propose a bounded exception and a verification step.

**Variant B:** A script runs through bash despite noexec. Is that alone a bypass of a promise made by the flag?

**Suggested evidence:**

- `evidence/phase-08/mount-options.txt`
- `evidence/phase-08/mount-tests.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 9: Remote access restrictions

**Why:** A valid credential should only work within the intended source/account policy.

**Goal:** Isolate source authorization before adding packet filtering.

**Practice:** about 20 minutes. Follow the practical steps below; they name the machine, user context and evidence to record.

### Practical steps

Use the target and client containers. Keep the target root console open as a recovery path.

1. From the target console, determine the approved client address and write an explicit SSH account/source allowlist. Validate before reload:

```bash
lab_client_ip=$(getent ahostsv4 client | awk 'NR==1{print $1}')
test -n "$lab_client_ip"
printf 'AllowUsers alice@%s\n' "$lab_client_ip" > /etc/ssh/sshd_config.d/01-allowlist.conf
sshd -t
kill -HUP 1
```

2. From the client container, test the approved account and credential. Preserve the command result and source address:

```bash
ssh -i /root/.ssh/labkey -o BatchMode=yes -o ConnectTimeout=3 alice@target true
```

3. Test the **same lab key** from a second client source using the laptop command below. It must be a different disposable container, not a copied key on your laptop:

```bash
docker compose exec -T client tar -C /root/.ssh -cf - labkey known_hosts | \
  docker compose run --rm -T --no-deps client bash -ec '
    mkdir -p /root/.ssh
    tar -xf - -C /root/.ssh
    chmod 600 /root/.ssh/labkey
    ssh -i /root/.ssh/labkey -o BatchMode=yes -o ConnectTimeout=3 alice@target true
  '
```

4. Save the allowlist, both source addresses and SSH outcomes in `evidence/phase-09/`. Explain how the unchanged key and changed source isolate account/source authorization. Do this phase before the firewall phase.

### 9.1 Prediction

Predict the new-source test using the same valid lab key after the account/source allowlist.

### 9.2 Decision

Explain the explicit allowlist and why a Match Address block alone does not deny all other sources.

### 9.3 Evidence

Attach the allowlist, both source identities and the same-key/different-source SSH result before the firewall is applied.

### 9.4 Interpretation

Which layer refused the attempt? What can change when the approved container is recreated?

### 9.5 Changed-condition scenario

Answer your teacher's assigned variant.

**Variant A:** The approved client is recreated and receives a different IP. Access stops. How do you diagnose and repair the smallest relevant policy while retaining the deny-by-default intent?

**Variant B:** The correct key is installed for two accounts, but only one is allowed by group policy. Would you remove AllowGroups to make both work? Explain your diagnosis and decision.

**Suggested evidence:**

- `evidence/phase-09/ssh-source-policy.txt`
- `evidence/phase-09/source-tests.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 10: Host firewall with nftables

**Why:** Keep network exposure aligned with the services and clients the host needs.

**Goal:** Prove source-specific filtering, persistence and required DNS behavior.

**Practice:** about 35 minutes. Follow the practical steps below; they name the machine, user context and evidence to record.

### Practical steps

Use the target root console and the named client containers. Keep the root console open while applying the policy.

1. Determine the approved client's IPv4 address and build a dedicated `inet filter` input table. Allow established replies, loopback, SSH and the lab web service from that source; drop other input. Load only the lab table with `nft-lab`, which preserves Docker-managed DNS rules:

```bash
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
nft list table inet filter
getent hosts archive.ubuntu.com
```

2. From a **client** console, test the approved flows:

```bash
ssh -i /root/.ssh/labkey -o BatchMode=yes -o ConnectTimeout=3 alice@target true
curl --fail --max-time 3 http://target:8080/report
```

3. From your laptop, test HTTP from a new client address and inspect target counters:

```bash
docker compose run --rm --no-deps client curl --fail --max-time 2 http://target:8080/report
```

This request should be refused. Run `nft list table inet filter` in the target console to see rule counters.
4. In the target console, save the lab policy with `nft-lab save`. Then, from the laptop, restart the target and wait for readiness:

```bash
docker compose restart target
docker compose up -d --wait --no-build
docker compose exec target bash
```

The restart closes the old target console. In the new target console, verify persistence and DNS with `nft list table inet filter`, `grep 'policy drop' /etc/nftables-lab.conf` and `getent hosts archive.ubuntu.com`. From the client console, repeat the SSH test. The manually started HTTP server stops on restart; check `ss -ltnp | grep ':8080'` before diagnosing a timeout.
5. Save rules, counters, client results and restart/DNS checks in `evidence/phase-10/`. Explain rule order, new versus established traffic, the IPv4-only `ip saddr` condition, and what the restart did and did not persist. Do not flush the full ruleset.

### 10.1 Prediction

Predict SSH/HTTP from the approved client and HTTP from a new source after filtering.

### 10.2 Decision

Explain rule order, connection state, source scope and why the lab replaces only its own table.

### 10.3 Evidence

Attach rules/counters, both client HTTP results, and post-restart policy, SSH and DNS checks.

### 10.4 Interpretation

What does the restart test prove, and how would you distinguish a missing listener from packet filtering?

### 10.5 Changed-condition scenario

Answer your teacher's assigned variant.

**Variant A:** The approved client is recreated and receives a different IP. Access stops. How do you diagnose and repair the smallest relevant policy while retaining the deny-by-default intent?

**Variant B:** The service must support approved IPv6 clients. Does the existing ip saddr rule permit them? Explain what policy and tests would be needed, including necessary IPv6 control traffic.

**Suggested evidence:**

- `evidence/phase-10/firewall-and-counters.txt`
- `evidence/phase-10/client-tests.txt`
- `evidence/phase-10/restart-and-dns.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 11: Rate limits, connection caps and Fail2ban

**Why:** Constrain excessive activity without confusing an event threshold with malicious intent.

**Goal:** Compare rate and concurrency, then prove a log-driven ban and recovery.

**Practice:** about 60 minutes. Follow the practical steps below; they name the machine, user context and evidence to record.

### Practical steps

This phase has two separate cycles. Complete **11A** in [`EXTENSIONS-2026.md`](EXTENSIONS-2026.md) first. It tests a per-source request-rate meter and a concurrent SSH connection cap. Record the first two allowed connections, the third refused connection and the meter's other-source control. Clean up 11A before continuing.

For **11B**, use the target and client containers:

1. On the target root console, prepare the HTTP log, server, filter and jail:

```bash
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
2. From the **client** console, generate five distinct events and check the valid page:

```bash
for i in 1 2 3 4 5; do curl -sS -o /dev/null -w '%{http_code}\n' http://target:8090/nope$i; done
curl --fail --max-time 2 http://target:8090/report
```

On the target, run `fail2ban-regex /var/log/http-access.log /etc/fail2ban/filter.d/pyhttp-404.conf` and `fail2ban-client status pyhttp-404`; confirm the source is not yet banned.
3. Generate one more 404 from the same client, wait three seconds, and test the report again:

```bash
curl -sS -o /dev/null -w '%{http_code}\n' http://target:8090/nope6
sleep 3
curl --fail --max-time 2 http://target:8090/report
```

The request should now be blocked. On the target inspect `fail2ban-client status pyhttp-404` and `nft list ruleset`.
4. On the target, unban the client address and prove the report works again. Then stop the test jail/server, reset and save only the teaching table, and confirm DNS still resolves. Use `fail2ban-client set pyhttp-404 unbanip CLIENT_IP`, `fail2ban-client stop pyhttp-404`, `kill "$(cat /run/http8090.pid)"`, `nft-lab reset`, `nft-lab save` and `getent hosts archive.ubuntu.com`. Replace `CLIENT_IP` with the observed client address.
5. Save matching/non-matching log evidence, fifth/sixth-event status, blocked request and recovery in `evidence/phase-11/`. Explain that one 404 request creates multiple log lines but the filter should count only the access line. A ban shows the configured signal/action, not intent.

### 11.1 Prediction

Predict a third simultaneous SSH connection under the cap, a third quick HTTP request under the meter, and access after five/six counted 404 events.

### 11.2 Decision

Explain what each control counts, rule order, the matched log line and the jail thresholds.

### 11.3 Evidence

Attach 11A allowed/refused tests and counters; then 11B filter counts, fifth/sixth-event states, a blocked request and successful recovery.

### 11.4 Interpretation

Explain one false-positive risk and one limit of your measurement. Does a ban establish intent?

### 11.5 Changed-condition scenario

Answer your teacher's assigned variant.

**Variant A:** Forty legitimate users share one public NAT address. Propose a safer detection/enforcement experiment and identify a metric for collateral damage.

**Variant B:** The log format changes after an application upgrade and the filter matches no events. Does the empty ban list prove attacks stopped? Propose a test that would expose the problem.

**Suggested evidence:**

- `evidence/phase-11/cap-and-meter-tests.txt`
- `evidence/phase-11/filter-and-event-counts.txt`
- `evidence/phase-11/ban-and-recovery.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 12: Updates and baseline hygiene

**Why:** Reduce exposure to known flaws while verifying operational continuity.

**Goal:** Inspect actual update policy/actions and preserve maintenance evidence.

**Practice:** about 25 minutes. Follow the practical steps below; they name the machine, user context and evidence to record.

### Practical steps

Run these tasks in the **target container**. The helper tools are installed in the lab image.

1. Save package state before and after a strict metadata refresh and upgrade:

```bash
dpkg-query -W > /artifacts/packages-before.txt
apt-get -o APT::Update::Error-Mode=any update
DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::=--force-confold -y upgrade
dpkg-query -W > /artifacts/packages-after.txt
```

2. Configure the security-only origin and periodic policy, inspect the effective settings, run a dry run and test a temporary package hold:

```bash
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

The dry run checks candidates and policy; it is not the scheduler.
3. Compare package versions and history; check relevant service state. State whether packages changed or no updates were available.
4. Save evidence under `evidence/phase-12/`. This container does not run systemd timers, so these checks do not prove automatic scheduling. Do not describe a dry run as a completed automatic update or a package hold as rollback.

### 12.1 Prediction

What do you expect a strict metadata refresh and a dry run to establish? Could no available updates be a valid outcome?

### 12.2 Decision

Explain trusted origins, the selected update policy and your restart/recovery considerations.

### 12.3 Evidence

Attach effective policy, dry-run/actual output, relevant package history and reboot/restart observations.

### 12.4 Interpretation

What can the container prove about package maintenance, and what needs a VM/host check?

### 12.5 Changed-condition scenario

Answer your teacher's assigned variant.

**Variant A:** A package update succeeds but the service still runs old code. What would you verify next?

**Variant B:** A fragile application has a package on hold. What should a documented exception contain?

**Suggested evidence:**

- `evidence/phase-12/update-policy.txt`
- `evidence/phase-12/update-actions-and-history.txt`
- `evidence/phase-12/packages-before.txt`
- `evidence/phase-12/packages-after.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 13: Chroot

**Why:** Narrow a service's filesystem view and run it with limited ordinary authority.

**Goal:** Observe the same service from inside and outside its jail.

**Practice:** about 35 minutes. Follow the practical steps below; they name the machine, user context and evidence to record.

### Practical steps

Use the **target root console** to prepare and start the service. Do not enable `noexec` on the filesystem that contains the BusyBox binary.

1. In the target root console, create the jail and static page, then start the HTTP process as its dedicated account:

```bash
install -d -m 0755 /srv/jail /srv/jail/bin /srv/jail/www
install -d -m 1777 /srv/jail/tmp
install -m 0755 "$(command -v busybox)" /srv/jail/bin/busybox
id www-chroot >/dev/null 2>&1 || useradd -r -s /usr/sbin/nologin www-chroot
lab_uid=$(id -u www-chroot)
lab_gid=$(id -g www-chroot)
echo 'OK: chrooted web' > /srv/jail/www/index.html
chmod 0644 /srv/jail/www/index.html
chroot --userspec="$lab_uid:$lab_gid" /srv/jail /bin/busybox httpd -f -v -p 0.0.0.0:8091 -h /www > /tmp/jail-http.log 2>&1 &
echo $! > /run/jail-http.pid
sleep 1
lab_pid=$(cat /run/jail-http.pid)
ps -o pid,user,args -p "$lab_pid"
awk '/Uid|Gid/' "/proc/$lab_pid/status"
ss -ltnp | grep 8091
runuser -u www-chroot -- readlink "/proc/$lab_pid/root"
```

The `/proc` checks should identify the service UID and `/srv/jail` root.
2. From the client console, run `curl -fsS --max-time 2 http://target:8091` and save the response.
3. Run and record these checks from the target console:

```bash
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
4. Stop the recorded test server PID and remove its PID file.
5. Save HTTP, `/proc`, root-path, read/write and cleanup evidence in `evidence/phase-13/`. Explain that a different filesystem root and UID limit different things; the kernel and network remain shared.

### 13.1 Prediction

Predict the inside path for /srv/jail/www and whether the prepared jail contains the target's /etc.

### 13.2 Decision

Explain the minimal static binary, dedicated UID and root-owned executable/static content.

### 13.3 Evidence

Provide the HTTP result, actual service PID/UID/root path, inside/outside observations and read-only code/content tests.

### 13.4 Interpretation

State a benefit and two boundaries chroot does not provide.

### 13.5 Changed-condition scenario

Answer your teacher's assigned variant.

**Variant A:** The jailed service now accepts uploads. Would you make its executable and whole web tree writable by the service account? Propose a smaller writable area and tests.

**Variant B:** A teammate says chroot prevents the service from reaching an external address. Explain why that conclusion does not follow and which separate control you would investigate.

**Suggested evidence:**

- `evidence/phase-13/service-response-and-identity.txt`
- `evidence/phase-13/jail-paths.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 14: AIDE: file integrity monitoring

**Why:** Detect meaningful file changes and investigate them before accepting a new state.

**Goal:** Compare a protected baseline, controlled change and reviewed new baseline.

**Practice:** about 30 minutes. Follow the practical steps below; they name the machine, user context and evidence to record.

### Practical steps

Run the integrity checks in the **target container**. Keep the baseline database protected and do not update it automatically after a difference.

1. On the target, create the baseline and selected `/etc` scope:

```bash
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

The `p/i/n/u/g/s/m/c/sha256` attributes are explained in Phase 14 slides; exclusions create blind spots.
2. Add the harmless classroom change and run the comparison in a subshell. Record the status immediately after the subshell:

```bash
echo '# authorized classroom test' >> /etc/hosts
(
  set +e
  aide --config /etc/aide/aide.conf --check | tee /artifacts/aide-changed.txt
  exit "${PIPESTATUS[0]}"
)
echo "AIDE status: $?"
```

The expected status for detected differences is 4. The subshell keeps the recovery console open.
3. Record the immediate exit status and save both clean and changed reports in `evidence/phase-14/`. Explain which attributes changed and why status 4 means differences were detected, not that AIDE failed or compromise was proven.
4. After reviewing the report, update and check the baseline:

```bash
aide --config /etc/aide/aide.conf --init
install -m 0600 /var/lib/aide/aide.db.new /var/lib/aide/aide.db
aide --config /etc/aide/aide.conf --check
```

State why this change is authorized before accepting it.

### 14.1 Prediction

Predict the initial comparison and the result after the controlled /etc/hosts change.

### 14.2 Decision

Explain monitored properties, scope, exclusions and why review precedes accepting a baseline.

### 14.3 Evidence

Attach clean, changed and reviewed-clean outputs plus the actual diff and acceptance decision.

### 14.4 Interpretation

Why does a clean result not prove absence of compromise?

### 14.5 Changed-condition scenario

Answer your teacher's assigned variant.

**Variant A:** A package update and an unexplained configuration edit occurred close together. AIDE reports a difference. What evidence would justify accepting it, and what would make you delay re-baselining?

**Variant B:** The account you are investigating can also modify the AIDE database. How should that affect your confidence in a clean result and your next comparison?

**Suggested evidence:**

- `evidence/phase-14/aide-comparisons.txt`
- `evidence/phase-14/reviewed-diff.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# Phase 15: osquery

**Why:** Make the initial audit repeatable and connect separate observations through structured queries.

**Goal:** Investigate listeners, privileged files and process state after the earlier controls.

**Practice:** about 35 minutes. Follow the practical steps below; they name the machine, user context and evidence to record.

### Practical steps

Run osquery in the **target container** and save JSON directly under `/artifacts`.

1. Install the pinned lab version with `install-osquery-lab`; inspect the `kernel_info` and `file` schemas before writing queries.
2. Export listener/process, user/session, system and interface observations as JSON:

```bash
osqueryi --json 'SELECT lp.address,lp.port,lp.protocol,p.pid,p.name,p.cmdline FROM listening_ports lp LEFT JOIN processes p ON lp.pid=p.pid ORDER BY lp.port;' > /artifacts/listeners.json
osqueryi --json 'SELECT username,uid,gid,directory,shell FROM users ORDER BY uid;' > /artifacts/users.json
osqueryi --json 'SELECT user,tty,host,time FROM logged_in_users;' > /artifacts/sessions.json
osqueryi --json 'SELECT name,version,platform,platform_like FROM os_version;' > /artifacts/os.json
osqueryi --json 'SELECT version,arguments,path,device FROM kernel_info;' > /artifacts/kernel.json
osqueryi --json 'SELECT hardware_model,cpu_brand,physical_memory FROM system_info;' > /artifacts/hardware.json
osqueryi --json 'SELECT total_seconds,days,hours FROM uptime;' > /artifacts/uptime.json
osqueryi --json "SELECT interface,address,mask,broadcast FROM interface_addresses WHERE address NOT LIKE '127.%' AND address != '::1';" > /artifacts/interfaces.json
```

3. Also investigate privileged files, selected paths, root listeners and largest processes:

```bash
osqueryi --json 'SELECT path,username,groupname,permissions FROM suid_bin;' > /artifacts/suid.json
osqueryi --json "SELECT path,mode FROM file WHERE path IN ('/usr/bin/sudo','/opt/labtools/shroot');" > /artifacts/selected-files.json
osqueryi --json 'SELECT lp.address,lp.port,p.pid,p.name,p.euid FROM listening_ports lp JOIN processes p ON lp.pid=p.pid WHERE p.euid=0 ORDER BY lp.port;' > /artifacts/root-listeners.json
osqueryi --json 'SELECT pid,name,resident_size FROM processes ORDER BY resident_size DESC LIMIT 10;' > /artifacts/top-memory.json
```
4. Compare one finding with `ss`, `ps` or the earlier `find` inventory.
5. Copy only relevant JSON and comparison output to `evidence/phase-15/`. Explain what the container can and cannot observe: kernel and hardware may describe the Docker host/VM; empty sessions can be normal; `file` needs a path constraint; `mode` is octal text.
6. End with a bounded risk-delta note. A query result is an observation; corroborate it and state its scope.

### 15.1 Prediction

Before querying, name one listener/process relationship you expect to find and one reason a session or inventory table might be empty without proving absence of activity.

### 15.2 Decision

Explain your join/filter and file constraints. Why do you inspect the installed schema and avoid ordinary numeric bit operations on the file table's octal mode text?

### 15.3 Evidence

Attach exact queries, JSON output and version/schema evidence for the inventory, SUID/SGID, root-owned listeners and top ten resident-memory processes. Corroborate one finding with ss/ps or find.

### 15.4 Interpretation

Select one actual finding and compare it with the earlier baseline. Explain an alternative interpretation, a justified next action and a scope/timing limitation.

### 15.5 Changed-condition scenario

Answer your teacher's assigned variant.

**Variant A:** Your query finds the SSH listener owned by root. Is that enough to recommend shutting it down? Explain the missing context and a safer decision process.

**Variant B:** An unexpected root-owned Python HTTP listener appears. Propose the first evidence to collect, one legitimate explanation and a change you would test if the service only needs to serve static files.

**Suggested evidence:**

- `evidence/phase-15/queries-and-version.txt`
- `evidence/phase-15/inventory.json`
- `evidence/phase-15/corroboration.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->
