# Linux security practical report

- Student ID: <your ID>
- Assignment: <teacher's reference>
- Assigned phases: <teacher's list>
- Platform and versions: <OS, architecture, Docker and relevant tools>
- Collaborators, if permitted: <names or none>

Read REPORT-EXAMPLE.md first. Keep only assigned phases. Use your own observations and relative evidence links. A concise paragraph or two plus the evidence table is enough for most phases, approximately 100–200 words excluding raw output. Keep the initial prediction separate from later corrections.

## Phase 0: setup checklist

- [ ] Both containers run and I can identify the target/client/laptop contexts.
- [ ] I know when to use root and when a test must run as Alice, Bob or student.
- [ ] I checked the tools, target name resolution and relevant port mapping.
- [ ] I saved a small file under /artifacts and found it on the laptop.
- [ ] I know the recovery console and the difference between restart and recreation.
- [ ] I read the worked report example and know the phases assigned to me.

Record platform details and any setup problem. Phase 0 is a readiness check, not a scored hardening result.

## Phase 1: Understanding the threat surface

### Required evidence — attach every item

- `evidence/phase-01/phase-01-evidence.txt` — listeners, processes and two documented findings; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 1.1 Prediction

Before the inventory, name one service you expect and one detail you will check.

<Your answer>

### 1.2 Decision

Choose two observed services or processes. State their purpose if known and whether you recommend keeping, restricting or investigating each. Do not change the configuration.

<Your answer>

### 1.3 Evidence

Attach every file in the Required evidence list. For each observation, identify the command, target/user context and relevant output.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-01/phase-01-evidence.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-01/phase-01-evidence.txt) |

### 1.4 Interpretation

What did the inventory establish? Give one justified next action and one thing the inventory cannot prove.

<Your answer>


## Phase 2: Accounts and sudo

### Required evidence — attach every item

- `evidence/phase-02/phase-02-evidence.txt` — account identities, validated sudo rule, Alice and Bob test results; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 2.1 Prediction

Before testing, predict whether Alice’s administrative command will succeed and whether Bob’s will succeed.

<Your answer>

### 2.2 Decision

Describe the lab’s admin group and sudo rule. State which account should be able to administer the target.

<Your answer>

### 2.3 Evidence

Attach every file in the Required evidence list. Include both account identities, the sudo rule and the results of the same command as Alice and Bob.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-02/phase-02-evidence.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-02/phase-02-evidence.txt) |

### 2.4 Interpretation

Explain how the account roles produced the observed results. State one limit of this lab’s broad admin role.

<Your answer>


## Phase 3: PAM: Pluggable Authentication Modules

### Required evidence — attach every item

- `evidence/phase-03/phase-03-evidence.txt` — PAM settings, initial login, lockout attempt, counter and recovery result; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 3.1 Prediction

Before the failed-login test, predict the result for a correct password before and after the configured failure threshold.

<Your answer>

### 3.2 Decision

Describe the PAM rule that counts failures and the configured lockout and recovery settings.

<Your answer>

### 3.3 Evidence

Attach every file in the Required evidence list. Include the initial successful login, failed attempts, correct-password attempt while locked, counter/reset and successful recovery.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-03/phase-03-evidence.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-03/phase-03-evidence.txt) |

### 3.4 Interpretation

Explain why the correct password was refused while the account was locked. State one benefit and one risk of lockout.

<Your answer>


## Phase 4: SSH: keys over passwords

### Required evidence — attach every item

- `evidence/phase-04/phase-04-evidence.txt` — public fingerprints, active SSH settings, validation and redacted login results; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 4.1 Prediction

After the SSH policy change, predict the result for Alice’s key, a password attempt and the student key.

<Your answer>

### 4.2 Decision

Describe how you installed the key, verified the target fingerprint and applied the SSH policy.

<Your answer>

### 4.3 Evidence

Attach every file in the Required evidence list. Include public fingerprints, effective SSH settings and all three login results. Do not submit private keys or passwords.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-04/phase-04-evidence.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-04/phase-04-evidence.txt) |

### 4.4 Interpretation

Explain each observed result. Identify which policy or identity explains each refusal.

<Your answer>


## Phase 5: SUID and SGID

### Required evidence — attach every item

- `evidence/phase-05/phase-05-evidence.txt` — SUID/capability inventory, permissions before and after, same-user test results; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 5.1 Prediction

Predict the effective UID when student runs the lab’s shroot command before and after the fix.

<Your answer>

### 5.2 Decision

Identify the lab-created file or directory you changed and explain why that change is limited to the unnecessary privilege.

<Your answer>

### 5.3 Evidence

Attach every file in the Required evidence list. Include the privileged-file inventory, ownership/modes and the same before/after test run as the ordinary student user.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-05/phase-05-evidence.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-05/phase-05-evidence.txt) |

### 5.4 Interpretation

State what the test proves and what it does not prove about the account’s other administrative access.

<Your answer>


## Phase 6: umask: default permissions

### Required evidence — attach every item

- `evidence/phase-06/phase-06-evidence.txt` — original and test umask values, fresh file/directory modes, restored value; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 6.1 Prediction

Predict the modes of a new file and directory when the shell uses umask 027.

<Your answer>

### 6.2 Decision

Explain where you set the umask for this test and why the test must use newly created files.

<Your answer>

### 6.3 Evidence

Attach every file in the Required evidence list. Include the original/restored mask, creation commands and actual modes for a fresh file and directory.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-06/phase-06-evidence.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-06/phase-06-evidence.txt) |

### 6.4 Interpretation

Explain which permission bits the mask removed. State why changing umask does not change an existing file.

<Your answer>


## Phase 7: ACL: Access Control Lists

### Required evidence — attach every item

- `evidence/phase-07/phase-07-evidence.txt` — project and file ACLs, Alice creation, Bob read/write test results; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 7.1 Prediction

Before testing, predict whether Bob can read and modify a report created by Alice in the project directory.

<Your answer>

### 7.2 Decision

Describe the project group, SGID bit and ACL entries you configured.

<Your answer>

### 7.3 Evidence

Attach every file in the Required evidence list. Include directory/new-file ACLs, Alice’s creation, and Bob’s read and refused-write results from a fresh Bob session.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-07/phase-07-evidence.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-07/phase-07-evidence.txt) |

### 7.4 Interpretation

Explain how SGID, the default ACL and ACL mask produced the observed access.

<Your answer>


## Phase 8: fstab and mount options

### Required evidence — attach every item

- `evidence/phase-08/phase-08-evidence.txt` — mount options, direct/interpreter test results, restored noexec result; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 8.1 Prediction

Predict the result of directly running a file from /tmp and running the same file through an interpreter.

<Your answer>

### 8.2 Decision

State which mount option you tested and how you restored the original lab setting.

<Your answer>

### 8.3 Evidence

Attach every file in the Required evidence list. Include effective mount options, direct and interpreter results, temporary exec result and restored noexec result.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-08/phase-08-evidence.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-08/phase-08-evidence.txt) |

### 8.4 Interpretation

Explain what noexec blocks and why an interpreter can still read a script.

<Your answer>


## Phase 9: Remote access restrictions

### Required evidence — attach every item

- `evidence/phase-09/phase-09-evidence.txt` — validated SSH source policy and same-key results from both clients; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 9.1 Prediction

Predict whether Alice’s same valid key will work from the approved and the other client after the source allowlist.

<Your answer>

### 9.2 Decision

Describe the account/source rule and why the root recovery console stayed open.

<Your answer>

### 9.3 Evidence

Attach every file in the Required evidence list. Include effective SSH policy, both source addresses and same-key results before the firewall phase.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-09/phase-09-evidence.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-09/phase-09-evidence.txt) |

### 9.4 Interpretation

Identify the layer that refused the other-source connection. State one reason the approved client address may change.

<Your answer>


## Phase 10: Host firewall with nftables

### Required evidence — attach every item

- `evidence/phase-10/phase-10-evidence.txt` — firewall rules/counters, client tests, restart, DNS and saved-policy checks; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 10.1 Prediction

Predict the SSH and HTTP results from the approved client and the HTTP result from the other client after filtering.

<Your answer>

### 10.2 Decision

Describe the allowed flows, denied flow, rule order and how you preserved Docker’s networking rules.

<Your answer>

### 10.3 Evidence

Attach every file in the Required evidence list. Include rules/counters, client tests, saved policy, post-restart SSH and DNS checks.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-10/phase-10-evidence.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-10/phase-10-evidence.txt) |

### 10.4 Interpretation

Explain what persisted after restart and how the evidence distinguishes filtering from a stopped service.

<Your answer>


## Phase 11: Rate limits, connection caps and Fail2ban

### Required evidence — attach every item

- `evidence/phase-11/phase-11-evidence.txt` — rate/cap tests, Fail2ban match and threshold checks, ban and recovery tests; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 11.1 Prediction

Predict the third simultaneous SSH connection, the rate-limited HTTP request, and the result after the sixth matching 404.

<Your answer>

### 11.2 Decision

Describe what the rate meter, connection cap and Fail2ban jail count in this lab.

<Your answer>

### 11.3 Evidence

Attach every file in the Required evidence list. Include 11A allowed/refused tests and counters; for 11B include matched events, fifth/sixth-event state, blocked request and successful recovery.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-11/phase-11-evidence.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-11/phase-11-evidence.txt) |

### 11.4 Interpretation

Explain what the ban proves and one reason a legitimate client could be affected.

<Your answer>


## Phase 12: Updates and baseline hygiene

### Required evidence — attach every item

- `evidence/phase-12/phase-12-evidence.txt` — update policy, package state before/after, actions, dry run and history; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 12.1 Prediction

State what a package-list refresh, upgrade and unattended-upgrade dry run will show.

<Your answer>

### 12.2 Decision

Describe the allowed update origin and the maintenance policy you configured.

<Your answer>

### 12.3 Evidence

Attach every file in the Required evidence list. Include package lists before/after, effective policy, dry-run output and package history.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-12/phase-12-evidence.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-12/phase-12-evidence.txt) |

### 12.4 Interpretation

State what the container run proves and what it cannot prove about automatic scheduling or a real host reboot.

<Your answer>


## Phase 13: Chroot

### Required evidence — attach every item

- `evidence/phase-13/phase-13-evidence.txt` — HTTP response, service identity and inside/outside jail path checks; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 13.1 Prediction

Predict what path the service sees as / and whether /etc is available inside the prepared jail.

<Your answer>

### 13.2 Decision

Describe the service account, jail root and read-only files used for the test.

<Your answer>

### 13.3 Evidence

Attach every file in the Required evidence list. Include HTTP response, process PID/UID/root path and inside/outside read/write tests.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-13/phase-13-evidence.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-13/phase-13-evidence.txt) |

### 13.4 Interpretation

State what the jail restricts and two protections it does not provide.

<Your answer>


## Phase 14: AIDE: file integrity monitoring

### Required evidence — attach every item

- `evidence/phase-14/phase-14-evidence.txt` — clean and changed AIDE checks, reviewed difference and final baseline check; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 14.1 Prediction

Predict the initial AIDE check and the check after the documented /etc/hosts change.

<Your answer>

### 14.2 Decision

Describe the paths/properties monitored and how you decide whether a difference is expected before updating the baseline.

<Your answer>

### 14.3 Evidence

Attach every file in the Required evidence list. Include the clean, changed and reviewed checks, status and relevant diff.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-14/phase-14-evidence.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-14/phase-14-evidence.txt) |

### 14.4 Interpretation

Explain why AIDE reports a difference and why a clean result does not prove the whole host is unchanged.

<Your answer>


## Phase 15: osquery

### Required evidence — attach every item

- `evidence/phase-15/phase-15-evidence.txt` — osquery version/schema, JSON query results and comparison with system tools; include commands, target/user context, expected and actual results, and exit status where relevant.

For every test, record the command, target and user context, expected result, actual output, and exit status when meaningful. Redact credentials.

### 15.1 Prediction

Before running osquery, name one listener/process relation you expect to find.

<Your answer>

### 15.2 Decision

State which query you used to inspect that finding and which native command you used to corroborate it.

<Your answer>

### 15.3 Evidence

Attach every file in the Required evidence list. Include osquery version/schema, JSON results and one corroborating command/output.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-15/phase-15-evidence.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-15/phase-15-evidence.txt) |

### 15.4 Interpretation

Compare one actual finding with an earlier phase. State one scope or timing limit of the result.

<Your answer>


## Final risk-delta note (maximum 200 words)

<Return to your initial inventory: what changed, what became harder for an attacker, which legitimate actions still work, and what remains outside the lab's protection? Cite your evidence. Do not claim changes you have not tested.>

## AI use and verification

<If used, name the tool and one suggestion accepted, corrected or rejected, with the observation you used to verify it. State if no AI was used. Full chat histories are unnecessary.>
