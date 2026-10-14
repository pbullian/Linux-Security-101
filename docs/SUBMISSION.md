# Submit a short, evidence-based report

Your teacher specifies the assigned exercises and one scenario variant (A or B) for each. Follow [EXERCISES.md](EXERCISES.md) and copy [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md) to `report.md`. Keep the five stable question IDs for every assigned exercise and remove unassigned sections.

Each exercise asks for a prediction, a justified decision, actual evidence, an explanation/limitation and a changed-condition scenario. Aim for about **150–250 words per exercise**, excluding raw output and tables. Clear, shorter answers are welcome. Do not paste the full command reference as your answer.

## Files to submit

Submit one ZIP named `student-ID-linux-security.zip` with this structure:

```text
report.md
manifest.json
evidence/
  E1/
    identities-and-baseline.txt
    sudoers.txt
    sudo-tests.txt
  E2/
    ...
```

Create only the evidence folders needed for your assigned exercises. Replace the suggested filenames if needed, but update the relative links in your report. Use plain text for command transcripts and logs, JSON for query results, and small configuration excerpts. Include screenshots only where they add information that text cannot capture. Do not submit executables or entire container exports.

Start `manifest.json` from [manifest.example.json](manifest.example.json). Enter your ID, assignment reference, the teacher's assigned exercises/scenario variants, and the evidence paths you actually supplied. For example:

```json
{
  "student_id": "YOUR-ID",
  "assignment": "TEACHER-REFERENCE",
  "assigned_exercises": ["E1"],
  "scenario_variants": {"E1": "A"},
  "report": "report.md",
  "evidence": [
    "evidence/E1/identities-and-baseline.txt",
    "evidence/E1/sudoers.txt",
    "evidence/E1/sudo-tests.txt"
  ]
}
```

The teacher determines the assignment scope; this manifest records it. It does not let you change the marking denominator.

## Evidence that can be checked quickly

For each important test, record the machine (target/client/laptop), execution user, command, expected result, observed result and exit status when meaningful. Link to the matching attachment and identify relevant lines if a transcript is long. Record exit status immediately after the tested command; a later command overwrites `$?`. Do not confuse UID 0 with exit status 0.

E1–E7 normally include a refused operation or an exposed limit. E8 includes an expected integrity difference. E9 uses corroboration or an alternative explanation; it does not require a refused login. If a command fails unexpectedly, preserve the result and explain your diagnosis. Never invent output to match the example.

Exclude passwords, private SSH keys, tokens, unrelated personal data and full environment dumps. Redact sensitive values while preserving the context needed to interpret the test. Public fingerprints are sufficient for the key-verification evidence.

## Marking criteria

Each assigned core exercise is worth 10 points:

| Question | Points | What the teacher looks for |
|---|---:|---|
| .1 Prediction | 1 | A specific initial prediction; distinguish it from corrections after testing. |
| .2 Decision | 2 | A suitable control and an explanation of its scope or tradeoff. |
| .3 Evidence | 3 | Normal/baseline result, counter-test/difference/corroboration, traceable command and context. |
| .4 Interpretation | 2 | The mechanism behind the result and a meaningful mismatch analysis or limitation. |
| .5 Scenario | 2 | The changed assumption, a justified adaptation and a discriminating test. |

A wrong initial prediction can earn credit when honestly analysed. A failed experiment can still demonstrate useful reasoning and diagnostic work. Length, polished screenshots and exact wording from the course are not the objective. Alternative justified solutions are welcome.

The suggested conversion is `20 × points earned / (10 × number of assigned exercises)`. Optional extensions are excluded unless the teacher assigns a separate policy.

## Using AI

AI may help explain a concept, suggest a test or debug an error. Verify its suggestions against your actual lab. Briefly identify one suggestion you accepted, corrected or rejected, with a link to the observation that informed your decision. State if you did not use AI. Full chat transcripts are unnecessary.

Try [the tutor prompt](AI-TUTOR.md) when you get stuck. Student exercise source files and PDFs also include non-visible tutoring hints that may be retained by copying. They ask for your prediction, attempt and observed output before further help. They do not prevent copying or guarantee how an AI responds. Your own observations and explanations remain the basis of the report.

The teacher may ask a short follow-up about your own output or change one condition in your scenario. AI-assisted assessment is provisional; the teacher decides the final mark.
