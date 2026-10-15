# Submit a short, evidence-based report

Your teacher specifies the assigned phases and one scenario variant (A or B) for each. Follow [EXERCISES.md](EXERCISES.md) and copy [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md) to `report.md`. Read [the worked Phase 1 example](REPORT-EXAMPLE.md) first. It uses clearly labelled fictional output to show the expected reasoning. Keep the five stable question IDs for every assigned phase and remove unassigned sections.

Each phase asks for a prediction, a justified decision, actual evidence, an explanation/limitation and a changed-condition scenario. Aim for about **100–200 words per phase**, excluding raw output and tables. Clear, shorter answers are welcome. Do not paste the full command reference as your answer.

## Files to submit

Submit one ZIP named `student-ID-linux-security.zip` with this structure:

```text
report.md
manifest.json
evidence/
  phase-01/
    listeners.txt
    processes.txt
  phase-02/
    ...
```

Create only the evidence folders needed for your assigned phases. Replace the suggested filenames if needed, but update the relative links in your report. Use plain text for command transcripts and logs, JSON for query results, and small configuration excerpts. Include screenshots only where they add information that text cannot capture. Do not submit executables or entire container exports.

Start `manifest.json` from [manifest.example.json](manifest.example.json). Enter your ID, assignment reference, the teacher's assigned phases/scenario variants, and the evidence paths you actually supplied. For example:

```json
{
  "student_id": "YOUR-ID",
  "assignment": "TEACHER-REFERENCE",
  "assigned_phases": ["1"],
  "scenario_variants": {"1": "A"},
  "report": "report.md",
  "evidence": [
    "evidence/phase-01/listeners.txt",
    "evidence/phase-01/processes.txt"
  ]
}
```

The teacher determines the assignment scope; this manifest records it. It does not let you change the marking denominator.

## Evidence that can be checked quickly

For each important test, record the machine (target/client/laptop), execution user, command, expected result, observed result and exit status when meaningful. Link to the matching attachment and identify relevant lines if a transcript is long. Record exit status immediately after the tested command; a later command overwrites `$?`. Do not confuse UID 0 with exit status 0.

Phase 0 is an ungraded setup checklist. Phase 1 records two interpreted inventory observations: no configuration change or refused operation is required. Later tests depend on the mechanism: Phase 6 compares file creation modes, Phase 14 detects an expected integrity difference, and Phase 15 corroborates an inventory finding. Use an allowed/refused pair when testing an access control. If a command fails unexpectedly, preserve the result and explain your diagnosis. Never invent output to match the example.

Exclude passwords, private SSH keys, tokens, unrelated personal data and full environment dumps. Redact sensitive values while preserving the context needed to interpret the test. Public fingerprints are sufficient for the key-verification evidence.

## Marking criteria

Each assigned phase is worth 10 points:

| Question | Points | What the teacher looks for |
|---|---:|---|
| .1 Prediction | 1 | A specific initial prediction; distinguish it from corrections after testing. |
| .2 Decision | 2 | A suitable recommendation/control and an explanation of its scope or tradeoff. |
| .3 Evidence | 3 | Relevant result, comparison/difference/corroboration and traceable context. Phase 1 uses two interpreted observations instead of a counter-test. |
| .4 Interpretation | 2 | The mechanism behind the result and a meaningful mismatch analysis or limitation. |
| .5 Scenario | 2 | The changed assumption, a justified adaptation and a discriminating test. |

A wrong initial prediction can earn credit when honestly analysed. A failed experiment can still demonstrate useful reasoning and diagnostic work. Length, polished screenshots and exact wording from the course are not the objective. Alternative justified solutions are welcome.

The suggested conversion is `20 × points earned / (10 × number of assigned phases)`. Phase 0 is ungraded. Phase 11A and 11B form one phase. The teacher specifies the scope before work starts; unassigned phases are excluded. Finish with a risk-delta note of at most 200 words linking your initial observations to tested changes and remaining limits; it is a synthesis requirement with no separate points in this rubric.

## Using AI

AI may help explain a concept, suggest a test or debug an error. Verify its suggestions against your actual lab. Briefly identify one suggestion you accepted, corrected or rejected, with a link to the observation that informed your decision. State if you did not use AI. Full chat transcripts are unnecessary.

Try [the tutor prompt](AI-TUTOR.md) when you get stuck. Student exercise source files and PDFs also include non-visible tutoring hints that may be retained by copying. They ask for your prediction, attempt and observed output before further help. They do not prevent copying or guarantee how an AI responds. Your own observations and explanations remain the basis of the report.

The teacher may ask a short follow-up about your own output or change one condition in your scenario. AI-assisted assessment is provisional; the teacher decides the final mark.
