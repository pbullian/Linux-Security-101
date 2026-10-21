# Worked report example: Phase 1

This is a **fictional teaching example** showing the expected reasoning and evidence structure. The short outputs in `examples/phase-01/` are deliberately labelled illustrative. Use your own observations and values in your report.

## Phase 1: Understanding the threat surface

### 1.1 Prediction

I expect SSH because this server must support remote administration. Before changing settings, I want to identify its listening address and process, then determine which access-policy questions need further testing.

### 1.2 Decision

| Observation | Purpose | Decision and reason |
|---|---|---|
| sshd listens on TCP 22 | Remote administration | Keep it, then restrict authentication and authorized users/sources in later phases. Removing it now would break the stated requirement. |
| rsyslogd is running without a TCP listener in this snapshot | Local event collection | Keep it for authentication and troubleshooting evidence. Its presence alone does not prove that every relevant event is logged. |

### 1.3 Evidence

| Context | Command | Relevant result | Evidence |
|---|---|---|---|
| Target, root console | `ss -tulpn`, `ps aux`, inventory review | TCP 22 listener, sshd and rsyslogd process entries, with two findings and recommendations | [illustrative listener output](examples/phase-01/listeners.txt) |

The root console provides process-owner visibility. This illustrative snippet is not proof that a student ran the lab. The actual submission uses the single combined transcript `evidence/phase-01/phase-01-evidence.txt`.

### 1.4 Interpretation

The SSH listener creates a remote authentication surface. The inventory does not establish weak authentication, a vulnerable version or Internet reachability. `0.0.0.0` describes the container's interfaces; the lab's laptop publication is restricted to loopback.

My next tests will check that Alice can connect using the approved key and that an unauthorized account or source is refused. No hardening has occurred in Phase 1, so I do not claim a reduction in risk yet.

## What makes this entry useful

It separates observed facts, the server's purpose, the decision, the next test and the remaining uncertainty. It does not equate a root-owned listener with a vulnerability. The first audit establishes a baseline; later phases must include their required evidence and verification.
