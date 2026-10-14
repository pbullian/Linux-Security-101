# Linux security practical report

- Student ID: <your ID>
- Assignment: <teacher's assignment reference>
- Assigned exercises: <teacher's list>
- Scenario variants: <teacher's E1=A, E2=B, ...>
- Lab platform and versions: <OS/architecture, Docker, relevant tool versions>
- Collaborators, if permitted: <names or none>

Keep only the assigned exercise sections. Answer under each stable question ID. Aim for about 150–250 words per exercise, excluding tables and raw output; concise complete answers are welcome. Replace placeholders and use relative evidence links. A result that differs from your prediction is useful when explained honestly.


## E1: Accounts and delegated administration

Assigned scenario: <A or B>

### E1.1 Prediction

Before testing, predict the effective UID of the administrative command for Alice and the result of Bob running the same command. State which role difference matters.

<Your answer>

### E1.2 Decision

Explain the role/group and sudo policy you used. Why is it useful for this lab, and why might it be too broad for a real log reader?

<Your answer>

### E1.3 Evidence

Provide a baseline listener observation, both account identities, the relevant sudoers fragment, its syntax-check result, and Alice's successful and Bob's refused tests. Record execution context and exit status.

<Your answer>

| Test | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| Normal / baseline | <context> | <command> | <prediction> | <actual result> | [output](evidence/E1/identities-and-baseline.txt) |
| Counter-test / difference / corroboration | <context> | <command> | <prediction> | <actual result> | <relative link> |

### E1.4 Interpretation

Explain why Bob can know the correct password and still fail. Does locking root's password remove Alice's delegated administration? Discuss one mismatch or limitation in your results.

<Your answer>

### E1.5 Changed-condition scenario

<Identify the assigned variant and changed assumption. Justify an adaptation and a test that could disprove your explanation. Consult EXERCISES.md for the exact prompt.>


## E2: Permissions and a deliberate SUID path

Assigned scenario: <A or B>

### E2.1 Prediction

Predict the effective UID when student runs the lab's shroot command before and after your proposed fix. Why would a root-run test fail to demonstrate this difference?

<Your answer>

### E2.2 Decision

Justify the files and directory permissions you change. Explain why you do not remove SUID indiscriminately from every system tool.

<Your answer>

### E2.3 Evidence

Attach the relevant inventory and ownership/modes, plus the exact same ordinary-user test before and after the change. Identify the tested process's effective UID.

<Your answer>

| Test | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| Normal / baseline | <context> | <command> | <prediction> | <actual result> | [output](evidence/E2/suid-inventory.txt) |
| Counter-test / difference / corroboration | <context> | <command> | <prediction> | <actual result> | <relative link> |

### E2.4 Interpretation

What precisely did the fix prevent? The student account still has sudo for setup: how does that limit your conclusion?

<Your answer>

### E2.5 Changed-condition scenario

<Identify the assigned variant and changed assumption. Justify an adaptation and a test that could disprove your explanation. Consult EXERCISES.md for the exact prompt.>


## E3: Creation defaults and inherited ACLs

Assigned scenario: <A or B>

### E3.1 Prediction

Predict a regular file and directory created with requested modes 0666 and 0777 under umask 027, before a default ACL is introduced. Explain the operation in words.

<Your answer>

### E3.2 Decision

Explain the project group, SGID directory bit, auditor ACL, default ACL and mask. Which mechanism applies to existing objects and which affects future creation?

<Your answer>

### E3.3 Evidence

Attach creation modes and getfacl output for the directory and a new report. Show Alice creating content, Bob reading it, and Bob's refused modification in their own contexts.

<Your answer>

| Test | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| Normal / baseline | <context> | <command> | <prediction> | <actual result> | [output](evidence/E3/creation-modes.txt) |
| Counter-test / difference / corroboration | <context> | <command> | <prediction> | <actual result> | <relative link> |

### E3.4 Interpretation

Explain why Bob's read and write attempts differ and why the new regular file is not executable. Identify one way an existing object could differ from a newly created one.

<Your answer>

### E3.5 Changed-condition scenario

<Identify the assigned variant and changed assumption. Justify an adaptation and a test that could disprove your explanation. Consult EXERCISES.md for the exact prompt.>


## E4: Password failures and SSH key access

Assigned scenario: <A or B>

### E4.1 Prediction

Predict the result of a correct password after five failed attempts, and then the outcomes of Alice's key, a password attempt and student's valid key after the SSH policy change.

<Your answer>

### E4.2 Decision

Explain the order of your changes and recovery route. Distinguish known_hosts, authorized_keys, SSH key verification and PAM account checks.

<Your answer>

### E4.3 Evidence

Provide lock-counter/recovery evidence, matching public fingerprints, relevant effective sshd settings, and all three final login outcomes. Never attach the private key or passwords.

<Your answer>

| Test | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| Normal / baseline | <context> | <command> | <prediction> | <actual result> | [output](evidence/E4/lockout-and-recovery.txt) |
| Counter-test / difference / corroboration | <context> | <command> | <prediction> | <actual result> | <relative link> |

### E4.4 Interpretation

Explain the reason for each refusal and how logs support it. Why can a valid key still fail? Why is copying the client-container key path into a laptop command insufficient?

<Your answer>

### E4.5 Changed-condition scenario

<Identify the assigned variant and changed assumption. Justify an adaptation and a test that could disprove your explanation. Consult EXERCISES.md for the exact prompt.>


## E5: Source policy and stateful filtering

Assigned scenario: <A or B>

### E5.1 Prediction

Predict what a second client with the same valid lab key can do before and after the source allowlist. Then predict HTTP access from the approved and new client after the firewall is applied.

<Your answer>

### E5.2 Decision

Explain the distinction between sshd authorization and packet filtering, rule order, and why you use nft-lab rather than flushing the whole ruleset.

<Your answer>

### E5.3 Evidence

Provide the same-key/different-source SSH test, the two-client HTTP tests, relevant rules/counters, and post-restart policy, SSH and DNS checks. Identify any manually started service that stopped.

<Your answer>

| Test | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| Normal / baseline | <context> | <command> | <prediction> | <actual result> | [output](evidence/E5/source-and-client-tests.txt) |
| Counter-test / difference / corroboration | <context> | <command> | <prediction> | <actual result> | <relative link> |

### E5.4 Interpretation

Explain which layer caused each refusal. Why might an existing connection behave differently from a fresh one? What does the restart test prove and not prove?

<Your answer>

### E5.5 Changed-condition scenario

<Identify the assigned variant and changed assumption. Justify an adaptation and a test that could disprove your explanation. Consult EXERCISES.md for the exact prompt.>


## E6: Log events and temporary bans

Assigned scenario: <A or B>

### E6.1 Prediction

Predict normal access after five distinct 404 requests and after the sixth within the configured window. Why might counting both Python log lines produce an earlier ban?

<Your answer>

### E6.2 Decision

Explain which line your filter counts, why the backend fits the environment, and the purpose of each threshold/window value.

<Your answer>

### E6.3 Evidence

Attach filter-count evidence, the not-banned and banned states, a blocked request and the successful request after unban. Link each result to the same source address.

<Your answer>

| Test | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| Normal / baseline | <context> | <command> | <prediction> | <actual result> | [output](evidence/E6/filter-and-event-counts.txt) |
| Counter-test / difference / corroboration | <context> | <command> | <prediction> | <actual result> | <relative link> |

### E6.4 Interpretation

Does a ban prove that the client was malicious? Explain a plausible false positive and how you would observe it before changing the detector.

<Your answer>

### E6.5 Changed-condition scenario

<Identify the assigned variant and changed assumption. Justify an adaptation and a test that could disprove your explanation. Consult EXERCISES.md for the exact prompt.>


## E7: Mount restrictions and a limited service identity

Assigned scenario: <A or B>

### E7.1 Prediction

Predict direct execution of the binary/script on noexec /tmp and explicit interpreter execution. Predict the path visible inside chroot for a file stored under /srv/jail/www outside.

<Your answer>

### E7.2 Decision

Explain why you combine mount policy, a changed filesystem root, a separate service UID and root-owned static content. What does each contribute?

<Your answer>

### E7.3 Evidence

Provide effective mount options, direct/interpreter outcomes, restored noexec refusal, the HTTP response, actual service PID/UID and inside/outside path checks.

<Your answer>

| Test | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| Normal / baseline | <context> | <command> | <prediction> | <actual result> | [output](evidence/E7/mount-tests.txt) |
| Counter-test / difference / corroboration | <context> | <command> | <prediction> | <actual result> | <relative link> |

### E7.4 Interpretation

Why is a missing /etc inside this small jail expected? Does successful HTTP mean the service is safely isolated? State two boundaries this experiment does not provide.

<Your answer>

### E7.5 Changed-condition scenario

<Identify the assigned variant and changed assumption. Justify an adaptation and a test that could disprove your explanation. Consult EXERCISES.md for the exact prompt.>


## E8: Updates and reviewed integrity changes

Assigned scenario: <A or B>

### E8.1 Prediction

Predict the AIDE result before and after the controlled /etc/hosts change. What can a dry run establish about update policy, and what can it not establish about automatic scheduling?

<Your answer>

### E8.2 Decision

Explain the security origin policy, monitored scope, exact exclusions and reason for reviewing a difference before accepting a new baseline.

<Your answer>

### E8.3 Evidence

Attach effective update policy/dry-run evidence and the clean, changed and reviewed-clean AIDE outcomes. Include the relevant diff and decision; do not invent installed updates if none were available.

<Your answer>

| Test | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| Normal / baseline | <context> | <command> | <prediction> | <actual result> | [output](evidence/E8/update-policy-and-actions.txt) |
| Counter-test / difference / corroboration | <context> | <command> | <prediction> | <actual result> | <relative link> |

### E8.4 Interpretation

Explain why a clean integrity report does not prove absence of compromise. How do the baseline's trust and monitored scope limit the conclusion?

<Your answer>

### E8.5 Changed-condition scenario

<Identify the assigned variant and changed assumption. Justify an adaptation and a test that could disprove your explanation. Consult EXERCISES.md for the exact prompt.>


## E9: Inventory and an evidence-based investigation

Assigned scenario: <A or B>

### E9.1 Prediction

Before querying, name one listener/process relationship you expect to find and one reason a session or inventory table might be empty without proving absence of activity.

<Your answer>

### E9.2 Decision

Explain your join/filter and file constraints. Why do you inspect the installed schema and avoid ordinary numeric bit operations on the file table's octal mode text?

<Your answer>

### E9.3 Evidence

Attach the exact queries, JSON output, installed version/schema evidence and a comparison with ss/ps or find. For one finding, record a counter-check that could change your initial interpretation.

<Your answer>

| Test | Machine / user | Command | Expected | Observed / exit status | Evidence |
|---|---|---|---|---|---|
| Normal / baseline | <context> | <command> | <prediction> | <actual result> | [output](evidence/E9/queries-and-version.txt) |
| Counter-test / difference / corroboration | <context> | <command> | <prediction> | <actual result> | <relative link> |

### E9.4 Interpretation

Select one actual finding. Explain what you can conclude, one alternative explanation, a justified next action and a limitation of the container observation.

<Your answer>

### E9.5 Changed-condition scenario

<Identify the assigned variant and changed assumption. Justify an adaptation and a test that could disprove your explanation. Consult EXERCISES.md for the exact prompt.>


## AI use and verification

<If used, name the tool and one useful suggestion that you accepted, corrected or rejected. Explain how you verified it and link the relevant observation. If no AI was used, state that. Do not attach entire chat histories.>
