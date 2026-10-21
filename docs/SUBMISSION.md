# Submit a short, evidence-based report

Your teacher assigns the phase numbers before work begins. Follow [EXERCISES.md](EXERCISES.md), copy [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md) to `report.md`, and read [the worked Phase 1 example](REPORT-EXAMPLE.md). Answer four questions for each assigned phase: prediction, decision, evidence and interpretation. Keep answers concise; clear reasoning matters more than length.

## Files to submit

Submit one ZIP named `student-ID-linux-security.zip` with `report.md`, `manifest.json` and the evidence files required for your assigned phases. Each phase's exercise page lists the exact required filenames. Replace a filename only when necessary and update the report link. Do not submit executables or full container exports.

Start `manifest.json` from [manifest.example.json](manifest.example.json). Enter your ID, assignment reference, assigned phases and the evidence paths you included. The manifest records the assignment; it does not change its scope.

## Evidence to include

For each test, record the machine, execution user, command, expected result, observed result and exit status when meaningful. Link the relevant attachment and identify the useful lines. Record exit status immediately after the tested command. Do not confuse UID 0 with exit status 0.

Phase 0 is an ungraded setup check. Phase 1 records two interpreted inventory observations; it does not require a configuration change or refused operation. Later tests depend on the control: Phase 6 compares file creation modes, Phase 14 detects an expected integrity difference, and Phase 15 corroborates an inventory finding. Preserve unexpected results and explain them. Never invent output.

Exclude passwords, private SSH keys, tokens, unrelated personal data and full environment dumps. Redact sensitive values while preserving the context needed to interpret the test. Public fingerprints are sufficient for key-verification evidence.

## Marking criteria

Each assigned phase is worth 10 points:

| Question | Points | What the teacher looks for |
|---|---:|---|
| Prediction | 1 | A specific initial expectation, distinct from later corrections. |
| Decision | 2 | A suitable recommendation/control and a reasoned explanation of its scope or tradeoff. |
| Evidence | 4 | Required files and relevant results, with traceable command and machine/user context. |
| Interpretation | 3 | The mechanism behind the result and a meaningful limitation or mismatch. |

A wrong initial prediction can earn credit when honestly analysed. A failed experiment can show useful reasoning and diagnosis. Alternative justified solutions are welcome.

The suggested conversion is `20 × points earned / (10 × number of assigned phases)`. Phase 0 is ungraded. Phase 11A and 11B form one phase. The teacher specifies the scope before work starts. Finish with a risk-delta note of at most 200 words linking initial observations to tested changes and remaining limits; it has no separate points.

## Using AI

AI may help explain a concept, suggest a test or debug an error. Verify suggestions against your actual lab. Briefly identify one suggestion you accepted, corrected or rejected, with a link to the observation that informed your decision. State if you did not use AI. Full chat transcripts are unnecessary.

Try [the tutor prompt](AI-TUTOR.md) when you get stuck. It may ask for your prediction, attempt and observed output before giving another hint. Your own observations and explanations remain the basis of the report.
