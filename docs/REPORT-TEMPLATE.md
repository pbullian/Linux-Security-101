# Linux security practical report

- Student ID: <your ID>
- Assignment: <teacher's reference>
- Assigned phases: <teacher's list>
- Scenario variants: <teacher's phase-to-A/B assignments>
- Platform and versions: <OS, architecture, Docker and relevant tools>
- Collaborators, if permitted: <names or none>

Read REPORT-EXAMPLE.md first. Keep only assigned phases. Use your own observations and relative evidence links. A concise paragraph or two plus the evidence table is enough for most phases, approximately 100–200 words excluding raw output. Keep the initial prediction separate from later corrections.

## Phase 0: setup checklist

- [ ] Both containers run and I can identify the target/client/laptop contexts.
- [ ] I know when to use root and when a test must run as Alice, Bob or student.
- [ ] I checked the tools, target name resolution and relevant port mapping.
- [ ] I saved a small file under /artifacts and found it on the laptop.
- [ ] I know the recovery console and the difference between restart and recreation.
- [ ] I read the worked report example and know the assigned phases/scenarios.

Record platform details and any setup problem. Phase 0 is a readiness check, not a scored hardening result.

## Phase 1: Understanding the threat surface

Assigned scenario: <A or B>

### 1.1 Prediction

Before running commands, name one required service you expect and one threat-surface question you want to investigate.

<Your answer>

### 1.2 Decision

Choose two meaningful observations. For each, state its purpose and a keep, restrict or investigate recommendation with a reason. Do not change configuration in this phase.

<Your answer>

### 1.3 Evidence

Attach listener and process output. In a small findings table, identify the address/port or process, execution context, evidence path and question raised.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-01/listeners.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | <relative link> |

### 1.4 Interpretation

Explain one plausible risk, the assumption behind it and one next test. What does this inventory fail to establish?

<Your answer>

### 1.5 Changed-condition scenario

<Identify variant A or B from EXERCISES.md. Explain the changed assumption, your justified response and a test or additional observation.>


## Phase 2: Accounts and sudo

Assigned scenario: <A or B>

### 2.1 Prediction

Before testing, predict the effective UID of the administrative command for Alice and the result of Bob running the same command. State which role difference matters.

<Your answer>

### 2.2 Decision

Explain the role/group and sudo policy you used. Why is it useful for this lab, and why might it be too broad for a real log reader?

<Your answer>

### 2.3 Evidence

Provide both account identities, the sudoers fragment and syntax-check result, plus Alice's successful and Bob's refused tests. Record context and exit status.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-02/identities-and-baseline.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | <relative link> |

### 2.4 Interpretation

Explain why Bob can know the correct password and still fail. Does locking root's password remove Alice's delegated administration? Discuss one mismatch or limitation in your results.

<Your answer>

### 2.5 Changed-condition scenario

<Identify variant A or B from EXERCISES.md. Explain the changed assumption, your justified response and a test or additional observation.>


## Phase 3: PAM: Pluggable Authentication Modules

Assigned scenario: <A or B>

### 3.1 Prediction

Predict a correct password before failures and after five failed attempts. What state changed?

<Your answer>

### 3.2 Decision

Explain the PAM stack and the deny/unlock_time policy. What do preauth, authfail and the account call do in this lab?

<Your answer>

### 3.3 Evidence

Save the relevant PAM files and threshold configuration, initial successful login, failure counter, refused correct-password attempt and reset and successful recovery evidence.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-03/pam-policy.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | <relative link> |

### 3.4 Interpretation

Why does a valid password not guarantee access? Explain one benefit and one risk of account lockout.

<Your answer>

### 3.5 Changed-condition scenario

<Identify variant A or B from EXERCISES.md. Explain the changed assumption, your justified response and a test or additional observation.>


## Phase 4: SSH: keys over passwords

Assigned scenario: <A or B>

### 4.1 Prediction

After the policy change, predict Alice's key, a password attempt and student's enrolled key.

<Your answer>

### 4.2 Decision

Explain key installation, host verification and safe change order. Distinguish known_hosts from authorized_keys.

<Your answer>

### 4.3 Evidence

Provide public fingerprints, relevant effective sshd settings, and all three final login results. Exclude private keys and passwords.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-04/public-fingerprints-and-settings.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | <relative link> |

### 4.4 Interpretation

Explain each refusal. Why can a valid key fail, and why does changing a password not revoke a stolen SSH key?

<Your answer>

### 4.5 Changed-condition scenario

<Identify variant A or B from EXERCISES.md. Explain the changed assumption, your justified response and a test or additional observation.>


## Phase 5: SUID and SGID

Assigned scenario: <A or B>

### 5.1 Prediction

Predict the effective UID when student runs the lab's shroot command before and after your proposed fix. Why would a root-run test fail to demonstrate this difference?

<Your answer>

### 5.2 Decision

Justify the files and directory permissions you change. Explain why you do not remove SUID indiscriminately from every system tool.

<Your answer>

### 5.3 Evidence

Attach the relevant inventory and ownership/modes, plus the exact same ordinary-user test before and after the change. Identify the tested process's effective UID.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-05/suid-inventory.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | <relative link> |

### 5.4 Interpretation

What precisely did the fix prevent? The student account still has sudo for setup: how does that limit your conclusion?

<Your answer>

### 5.5 Changed-condition scenario

<Identify variant A or B from EXERCISES.md. Explain the changed assumption, your justified response and a test or additional observation.>


## Phase 6: umask: default permissions

Assigned scenario: <A or B>

### 6.1 Prediction

Predict new regular-file and directory modes under umask 027, with requested modes 0666 and 0777 and no default ACL.

<Your answer>

### 6.2 Decision

Explain why you set the mask in the tested shell, and what a login-default change would affect.

<Your answer>

### 6.3 Evidence

Attach the current mask, creation commands and modes of the fresh file and directory, with context.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-06/creation-modes.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | <relative link> |

### 6.4 Interpretation

Explain the observed permissions and a collaboration case where 027 is unsuitable.

<Your answer>

### 6.5 Changed-condition scenario

<Identify variant A or B from EXERCISES.md. Explain the changed assumption, your justified response and a test or additional observation.>


## Phase 7: ACL: Access Control Lists

Assigned scenario: <A or B>

### 7.1 Prediction

Before testing, predict Alice's creation of a report, Bob's read and Bob's modification. What should be inherited?

<Your answer>

### 7.2 Decision

Explain the project group, SGID directory bit, auditor ACL, default ACL and mask. Which mechanism applies to existing objects and which affects future creation?

<Your answer>

### 7.3 Evidence

Attach creation modes and getfacl output for the directory and a new report. Show Alice creating content, Bob reading it, and Bob's refused modification in their own contexts.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-07/project-acls.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | <relative link> |

### 7.4 Interpretation

Explain why Bob's read and write attempts differ and why the new regular file is not executable. Identify one way an existing object could differ from a newly created one.

<Your answer>

### 7.5 Changed-condition scenario

<Identify variant A or B from EXERCISES.md. Explain the changed assumption, your justified response and a test or additional observation.>


## Phase 8: fstab and mount options

Assigned scenario: <A or B>

### 8.1 Prediction

Predict direct execution of the binary/script on noexec /tmp and explicit interpreter execution.

<Your answer>

### 8.2 Decision

Explain the chosen mount flags, temporary exception and restoration. Why does this lab not verify fstab boot policy?

<Your answer>

### 8.3 Evidence

Provide effective mount options, direct/interpreter outcomes, the temporary exec result and restored noexec refusal.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-08/mount-options.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | <relative link> |

### 8.4 Interpretation

What risk did noexec reduce, and what remains possible? Why not bind /var/tmp to volatile /tmp blindly?

<Your answer>

### 8.5 Changed-condition scenario

<Identify variant A or B from EXERCISES.md. Explain the changed assumption, your justified response and a test or additional observation.>


## Phase 9: Remote access restrictions

Assigned scenario: <A or B>

### 9.1 Prediction

Predict the new-source test using the same valid lab key after the account/source allowlist.

<Your answer>

### 9.2 Decision

Explain the explicit allowlist and why a Match Address block alone does not deny all other sources.

<Your answer>

### 9.3 Evidence

Attach the allowlist, both source identities and the same-key/different-source SSH result before the firewall is applied.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-09/ssh-source-policy.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | <relative link> |

### 9.4 Interpretation

Which layer refused the attempt? What can change when the approved container is recreated?

<Your answer>

### 9.5 Changed-condition scenario

<Identify variant A or B from EXERCISES.md. Explain the changed assumption, your justified response and a test or additional observation.>


## Phase 10: Host firewall with nftables

Assigned scenario: <A or B>

### 10.1 Prediction

Predict SSH/HTTP from the approved client and HTTP from a new source after filtering.

<Your answer>

### 10.2 Decision

Explain rule order, connection state, source scope and why the lab replaces only its own table.

<Your answer>

### 10.3 Evidence

Attach rules/counters, both client HTTP results, and post-restart policy, SSH and DNS checks.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-10/firewall-and-counters.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | <relative link> |

### 10.4 Interpretation

What does the restart test prove, and how would you distinguish a missing listener from packet filtering?

<Your answer>

### 10.5 Changed-condition scenario

<Identify variant A or B from EXERCISES.md. Explain the changed assumption, your justified response and a test or additional observation.>


## Phase 11: Rate limits, connection caps and Fail2ban

Assigned scenario: <A or B>

### 11.1 Prediction

Predict a third simultaneous SSH connection under the cap, a third quick HTTP request under the meter, and access after five/six counted 404 events.

<Your answer>

### 11.2 Decision

Explain what each control counts, rule order, the matched log line and the jail thresholds.

<Your answer>

### 11.3 Evidence

Attach 11A allowed/refused tests and counters; then 11B filter counts, fifth/sixth-event states, a blocked request and successful recovery.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-11/cap-and-meter-tests.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | <relative link> |

### 11.4 Interpretation

Explain one false-positive risk and one limit of your measurement. Does a ban establish intent?

<Your answer>

### 11.5 Changed-condition scenario

<Identify variant A or B from EXERCISES.md. Explain the changed assumption, your justified response and a test or additional observation.>


## Phase 12: Updates and baseline hygiene

Assigned scenario: <A or B>

### 12.1 Prediction

What do you expect a strict metadata refresh and a dry run to establish? Could no available updates be a valid outcome?

<Your answer>

### 12.2 Decision

Explain trusted origins, the selected update policy and your restart/recovery considerations.

<Your answer>

### 12.3 Evidence

Attach effective policy, dry-run/actual output, relevant package history and reboot/restart observations.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-12/update-policy.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | <relative link> |

### 12.4 Interpretation

What can the container prove about package maintenance, and what needs a VM/host check?

<Your answer>

### 12.5 Changed-condition scenario

<Identify variant A or B from EXERCISES.md. Explain the changed assumption, your justified response and a test or additional observation.>


## Phase 13: Chroot

Assigned scenario: <A or B>

### 13.1 Prediction

Predict the inside path for /srv/jail/www and whether the prepared jail contains the target's /etc.

<Your answer>

### 13.2 Decision

Explain the minimal static binary, dedicated UID and root-owned executable/static content.

<Your answer>

### 13.3 Evidence

Provide the HTTP result, actual service PID/UID/root path, inside/outside observations and read-only code/content tests.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-13/service-response-and-identity.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | <relative link> |

### 13.4 Interpretation

State a benefit and two boundaries chroot does not provide.

<Your answer>

### 13.5 Changed-condition scenario

<Identify variant A or B from EXERCISES.md. Explain the changed assumption, your justified response and a test or additional observation.>


## Phase 14: AIDE: file integrity monitoring

Assigned scenario: <A or B>

### 14.1 Prediction

Predict the initial comparison and the result after the controlled /etc/hosts change.

<Your answer>

### 14.2 Decision

Explain monitored properties, scope, exclusions and why review precedes accepting a baseline.

<Your answer>

### 14.3 Evidence

Attach clean, changed and reviewed-clean outputs plus the actual diff and acceptance decision.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-14/aide-comparisons.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | <relative link> |

### 14.4 Interpretation

Why does a clean result not prove absence of compromise?

<Your answer>

### 14.5 Changed-condition scenario

<Identify variant A or B from EXERCISES.md. Explain the changed assumption, your justified response and a test or additional observation.>


## Phase 15: osquery

Assigned scenario: <A or B>

### 15.1 Prediction

Before querying, name one listener/process relationship you expect to find and one reason a session or inventory table might be empty without proving absence of activity.

<Your answer>

### 15.2 Decision

Explain your join/filter and file constraints. Why do you inspect the installed schema and avoid ordinary numeric bit operations on the file table's octal mode text?

<Your answer>

### 15.3 Evidence

Attach exact queries, JSON output and version/schema evidence for the inventory, SUID/SGID, root-owned listeners and top ten resident-memory processes. Corroborate one finding with ss/ps or find.

<Your answer>

| Test / observation | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| <baseline / wanted operation> | <context> | <command> | <prediction> | <actual> | [output](evidence/phase-15/queries-and-version.txt) |
| <comparison / refusal / corroboration if relevant> | <context> | <command> | <prediction> | <actual> | <relative link> |

### 15.4 Interpretation

Select one actual finding and compare it with the earlier baseline. Explain an alternative interpretation, a justified next action and a scope/timing limitation.

<Your answer>

### 15.5 Changed-condition scenario

<Identify variant A or B from EXERCISES.md. Explain the changed assumption, your justified response and a test or additional observation.>


## Final risk-delta note (maximum 200 words)

<Return to your initial inventory: what changed, what became harder for an attacker, which legitimate actions still work, and what remains outside the lab's protection? Cite your evidence. Do not claim changes you have not tested.>

## AI use and verification

<If used, name the tool and one suggestion accepted, corrected or rejected, with the observation you used to verify it. State if no AI was used. Full chat histories are unnecessary.>
