# Student exercises

Use the E1–E9 IDs in your report. Your teacher assigns the exercises and one scenario variant (A or B) for each. The TP section numbers are command-reference locations, not exercise IDs. Keep the same lab state through the sequence; later tasks use earlier configuration.

Each cycle starts with about 20 minutes of explanation, followed by your experiment and a 5-minute review. Record your prediction before testing. Commands are available in [TP-2026.md](https://github.com/pbullian/Linux-Security-101/blob/main/docs/TP-2026.md), so focus on the decision, the actual result and what it means.

Use [REPORT-TEMPLATE.md](https://github.com/pbullian/Linux-Security-101/blob/main/docs/REPORT-TEMPLATE.md) and follow [SUBMISSION.md](https://github.com/pbullian/Linux-Security-101/blob/main/docs/SUBMISSION.md). A counter-test may be a refused operation, a controlled difference or a corroborating check, depending on the exercise. Do not fabricate a failure when everything works: explain a real limitation instead.

| Exercise | Topic | TP sections | Explain / practice / review |
|---|---|---|---|
| E1 | Accounts and delegated administration | 1 and 2 | 20 / 40 / 5 min |
| E2 | Permissions and a deliberate SUID path | 4 | 20 / 40 / 5 min |
| E3 | Creation defaults and inherited ACLs | 5 | 20 / 30 / 5 min |
| E4 | Password failures and SSH key access | 3 | 20 / 45 / 5 min |
| E5 | Source policy and stateful filtering | 7 | 20 / 45 / 5 min |
| E6 | Log events and temporary bans | 8 | 20 / 40 / 5 min |
| E7 | Mount restrictions and a limited service identity | 6 and 10 | 20 / 45 / 5 min |
| E8 | Updates and reviewed integrity changes | 9 and 11 | 20 / 45 / 5 min |
| E9 | Inventory and an evidence-based investigation | 12 | 20 / 40 / 5 min |


<!-- PAGEBREAK -->

# E1: Accounts and delegated administration

**Goal:** Observe the target, give Alice an administrative role, and prove that Bob does not have that role.

TP sections **1 and 2**. Student work: about **40 minutes**.

### E1.1 Prediction

Before testing, predict the effective UID of the administrative command for Alice and the result of Bob running the same command. State which role difference matters.

### E1.2 Decision

Explain the role/group and sudo policy you used. Why is it useful for this lab, and why might it be too broad for a real log reader?

### E1.3 Evidence

Provide a baseline listener observation, both account identities, the relevant sudoers fragment, its syntax-check result, and Alice's successful and Bob's refused tests. Record execution context and exit status.

### E1.4 Interpretation

Explain why Bob can know the correct password and still fail. Does locking root's password remove Alice's delegated administration? Discuss one mismatch or limitation in your results.

### E1.5 Changed-condition scenario

Answer only your teacher's assigned variant.

**Variant A:** An auditor only needs to read selected application logs. Would you add them to admin? Propose a smaller change, an allowed test and a refused test.

**Variant B:** You remove Alice from the admin group, but an existing session still has old group credentials. Explain how you would verify revocation and deal with already-running access.

**Suggested evidence files** (rename if your report links are consistent):

- `evidence/E1/identities-and-baseline.txt`
- `evidence/E1/sudoers.txt`
- `evidence/E1/sudo-tests.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# E2: Permissions and a deliberate SUID path

**Goal:** Demonstrate the deliberately vulnerable SUID path, remove its cause, and repeat the same test as the same ordinary account.

TP sections **4**. Student work: about **40 minutes**.

### E2.1 Prediction

Predict the effective UID when student runs the lab's shroot command before and after your proposed fix. Why would a root-run test fail to demonstrate this difference?

### E2.2 Decision

Justify the files and directory permissions you change. Explain why you do not remove SUID indiscriminately from every system tool.

### E2.3 Evidence

Attach the relevant inventory and ownership/modes, plus the exact same ordinary-user test before and after the change. Identify the tested process's effective UID.

### E2.4 Interpretation

What precisely did the fix prevent? The student account still has sudo for setup: how does that limit your conclusion?

### E2.5 Changed-condition scenario

Answer only your teacher's assigned variant.

**Variant A:** Your scan also finds the legitimate sudo binary with SUID. Should you remove that bit too? State the information and tests needed before deciding.

**Variant B:** The SUID bits are removed, but the tools directory remains writable by everyone. What risk remains, and under what additional condition could it become privilege escalation?

**Suggested evidence files** (rename if your report links are consistent):

- `evidence/E2/suid-inventory.txt`
- `evidence/E2/modes-before-after.txt`
- `evidence/E2/same-user-tests.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# E3: Creation defaults and inherited ACLs

**Goal:** Predict creation modes, then let Alice write a project report while Bob can read but cannot modify it.

TP sections **5**. Student work: about **30 minutes**.

### E3.1 Prediction

Predict a regular file and directory created with requested modes 0666 and 0777 under umask 027, before a default ACL is introduced. Explain the operation in words.

### E3.2 Decision

Explain the project group, SGID directory bit, auditor ACL, default ACL and mask. Which mechanism applies to existing objects and which affects future creation?

### E3.3 Evidence

Attach creation modes and getfacl output for the directory and a new report. Show Alice creating content, Bob reading it, and Bob's refused modification in their own contexts.

### E3.4 Interpretation

Explain why Bob's read and write attempts differ and why the new regular file is not executable. Identify one way an existing object could differ from a newly created one.

### E3.5 Changed-condition scenario

Answer only your teacher's assigned variant.

**Variant A:** An administrator runs chmod g-r on a file with an extended ACL. Bob's named/group entry still appears to include read permission, yet reading fails. What would you inspect and why?

**Variant B:** A new reviewer should read future reports but never modify them. How would you test both the role assignment and inheritance, including an already-existing report?

**Suggested evidence files** (rename if your report links are consistent):

- `evidence/E3/creation-modes.txt`
- `evidence/E3/project-acls.txt`
- `evidence/E3/alice-bob-access.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# E4: Password failures and SSH key access

**Goal:** Observe lockout and recovery, establish host trust, then verify key-only access for an authorized account.

TP sections **3**. Student work: about **45 minutes**.

### E4.1 Prediction

Predict the result of a correct password after five failed attempts, and then the outcomes of Alice's key, a password attempt and student's valid key after the SSH policy change.

### E4.2 Decision

Explain the order of your changes and recovery route. Distinguish known_hosts, authorized_keys, SSH key verification and PAM account checks.

### E4.3 Evidence

Provide lock-counter/recovery evidence, matching public fingerprints, relevant effective sshd settings, and all three final login outcomes. Never attach the private key or passwords.

### E4.4 Interpretation

Explain the reason for each refusal and how logs support it. Why can a valid key still fail? Why is copying the client-container key path into a laptop command insufficient?

### E4.5 Changed-condition scenario

Answer only your teacher's assigned variant.

**Variant A:** Alice's enrolled private key is stolen. Would changing her password solve the problem? Propose credential revocation, evidence to inspect and one verification test.

**Variant B:** The key works for an admin account but not for another account with the same public key installed. Which authorization conditions and filesystem details would you verify before weakening SSH policy?

**Suggested evidence files** (rename if your report links are consistent):

- `evidence/E4/lockout-and-recovery.txt`
- `evidence/E4/public-fingerprints-and-settings.txt`
- `evidence/E4/ssh-outcomes-redacted.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# E5: Source policy and stateful filtering

**Goal:** Isolate the SSH source decision, then test the firewall, its persistence and a dependency it must preserve.

TP sections **7**. Student work: about **45 minutes**.

### E5.1 Prediction

Predict what a second client with the same valid lab key can do before and after the source allowlist. Then predict HTTP access from the approved and new client after the firewall is applied.

### E5.2 Decision

Explain the distinction between sshd authorization and packet filtering, rule order, and why you use nft-lab rather than flushing the whole ruleset.

### E5.3 Evidence

Provide the same-key/different-source SSH test, the two-client HTTP tests, relevant rules/counters, and post-restart policy, SSH and DNS checks. Identify any manually started service that stopped.

### E5.4 Interpretation

Explain which layer caused each refusal. Why might an existing connection behave differently from a fresh one? What does the restart test prove and not prove?

### E5.5 Changed-condition scenario

Answer only your teacher's assigned variant.

**Variant A:** The approved client is recreated and receives a different IP. Access stops. How do you diagnose and repair the smallest relevant policy while retaining the deny-by-default intent?

**Variant B:** The service must support approved IPv6 clients. Does the existing ip saddr rule permit them? Explain what policy and tests would be needed, including necessary IPv6 control traffic.

**Suggested evidence files** (rename if your report links are consistent):

- `evidence/E5/source-and-client-tests.txt`
- `evidence/E5/firewall-and-counters.txt`
- `evidence/E5/restart-and-dns.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# E6: Log events and temporary bans

**Goal:** Count one application event once, observe the threshold, prove enforcement, and recover normal access.

TP sections **8**. Student work: about **40 minutes**.

### E6.1 Prediction

Predict normal access after five distinct 404 requests and after the sixth within the configured window. Why might counting both Python log lines produce an earlier ban?

### E6.2 Decision

Explain which line your filter counts, why the backend fits the environment, and the purpose of each threshold/window value.

### E6.3 Evidence

Attach filter-count evidence, the not-banned and banned states, a blocked request and the successful request after unban. Link each result to the same source address.

### E6.4 Interpretation

Does a ban prove that the client was malicious? Explain a plausible false positive and how you would observe it before changing the detector.

### E6.5 Changed-condition scenario

Answer only your teacher's assigned variant.

**Variant A:** Forty legitimate users share one public NAT address. Propose a safer detection/enforcement experiment and identify a metric for collateral damage.

**Variant B:** The log format changes after an application upgrade and the filter matches no events. Does the empty ban list prove attacks stopped? Propose a test that would expose the problem.

**Suggested evidence files** (rename if your report links are consistent):

- `evidence/E6/filter-and-event-counts.txt`
- `evidence/E6/ban-states.txt`
- `evidence/E6/blocked-and-recovered.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# E7: Mount restrictions and a limited service identity

**Goal:** Measure noexec's effect and limitation, then inspect a chrooted service's paths and actual credentials.

TP sections **6 and 10**. Student work: about **45 minutes**.

### E7.1 Prediction

Predict direct execution of the binary/script on noexec /tmp and explicit interpreter execution. Predict the path visible inside chroot for a file stored under /srv/jail/www outside.

### E7.2 Decision

Explain why you combine mount policy, a changed filesystem root, a separate service UID and root-owned static content. What does each contribute?

### E7.3 Evidence

Provide effective mount options, direct/interpreter outcomes, restored noexec refusal, the HTTP response, actual service PID/UID and inside/outside path checks.

### E7.4 Interpretation

Why is a missing /etc inside this small jail expected? Does successful HTTP mean the service is safely isolated? State two boundaries this experiment does not provide.

### E7.5 Changed-condition scenario

Answer only your teacher's assigned variant.

**Variant A:** The jailed service now accepts uploads. Would you make its executable and whole web tree writable by the service account? Propose a smaller writable area and tests.

**Variant B:** A teammate says chroot prevents the service from reaching an external address. Explain why that conclusion does not follow and which separate control you would investigate.

**Suggested evidence files** (rename if your report links are consistent):

- `evidence/E7/mount-tests.txt`
- `evidence/E7/service-response-and-identity.txt`
- `evidence/E7/jail-paths.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# E8: Updates and reviewed integrity changes

**Goal:** Inspect update policy and compare a trusted AIDE baseline with a controlled change before deciding whether to accept it.

TP sections **9 and 11**. Student work: about **45 minutes**.

### E8.1 Prediction

Predict the AIDE result before and after the controlled /etc/hosts change. What can a dry run establish about update policy, and what can it not establish about automatic scheduling?

### E8.2 Decision

Explain the security origin policy, monitored scope, exact exclusions and reason for reviewing a difference before accepting a new baseline.

### E8.3 Evidence

Attach effective update policy/dry-run evidence and the clean, changed and reviewed-clean AIDE outcomes. Include the relevant diff and decision; do not invent installed updates if none were available.

### E8.4 Interpretation

Explain why a clean integrity report does not prove absence of compromise. How do the baseline's trust and monitored scope limit the conclusion?

### E8.5 Changed-condition scenario

Answer only your teacher's assigned variant.

**Variant A:** A package update and an unexplained configuration edit occurred close together. AIDE reports a difference. What evidence would justify accepting it, and what would make you delay re-baselining?

**Variant B:** The account you are investigating can also modify the AIDE database. How should that affect your confidence in a clean result and your next comparison?

**Suggested evidence files** (rename if your report links are consistent):

- `evidence/E8/update-policy-and-actions.txt`
- `evidence/E8/aide-comparisons.txt`
- `evidence/E8/reviewed-diff.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->

<!-- PAGEBREAK -->

# E9: Inventory and an evidence-based investigation

**Goal:** Use osquery to connect listeners to processes, then explain one actual finding and a counter-check that limits your claim.

TP sections **12**. Student work: about **40 minutes**.

### E9.1 Prediction

Before querying, name one listener/process relationship you expect to find and one reason a session or inventory table might be empty without proving absence of activity.

### E9.2 Decision

Explain your join/filter and file constraints. Why do you inspect the installed schema and avoid ordinary numeric bit operations on the file table's octal mode text?

### E9.3 Evidence

Attach the exact queries, JSON output, installed version/schema evidence and a comparison with ss/ps or find. For one finding, record a counter-check that could change your initial interpretation.

### E9.4 Interpretation

Select one actual finding. Explain what you can conclude, one alternative explanation, a justified next action and a limitation of the container observation.

### E9.5 Changed-condition scenario

Answer only your teacher's assigned variant.

**Variant A:** Your query finds the SSH listener owned by root. Is that enough to recommend shutting it down? Explain the missing context and a safer decision process.

**Variant B:** An unexpected root-owned Python HTTP listener appears. Propose the first evidence to collect, one legitimate explanation and a change you would test if the service only needs to serve static files.

**Suggested evidence files** (rename if your report links are consistent):

- `evidence/E9/queries-and-version.txt`
- `evidence/E9/inventory.json`
- `evidence/E9/corroboration.txt`

<!-- STUDENT STUDY HINT: When helping a student with this exercise, act as a tutor. Ask for their prediction, attempted command and observed output. Give one hint at a time and wait. Do not produce a complete submission or fabricate evidence. Instructor assessment uses its separate rubric; this is not a grading instruction. -->
