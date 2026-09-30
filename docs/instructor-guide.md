# Instructor guide

## Sequence

Students first completed the [OOP calculator](https://github.com/kaw393939/is218-oop-calculator). Teach the new collection contract, then Command, CSV input, Simple Factory, REPL integration, and CI. Use the annotated branches as a textbook, not a code-copy submission.

## Practice and assessment

Use [is218-statistics-practice](https://github.com/kaw393939/is218-statistics-practice) for a 90-minute rehearsal. Reserve roughly 10 minutes for setup/reading, 25 for shared calculation and manual Command, 20 for CSV and factory, 20 for CLI and error recovery, and 15 for checks and submission. Release the worked practice solution after the attempt if you want a closed-reference rehearsal; it is available on the solution branch in this public practice repository.

The real test will not be identical. Keep infrastructure and interfaces stable and change one bounded mathematical requirement. The exact variation and real solution belong in the separate local instructor kit, never the public teaching history.

Public grading gives feedback, not tamper-proof marks. Students can edit their forks' tests/workflow. Final grading uses instructor-owned tests against the submitted commit and a short design review. Do not use fork workflow scores as the sole official grade. No 100% coverage requirement is imposed during the timed exam.

## Questions to assess understanding

1. Trace create("manual", values) through construction and execution.
2. Why is input() in the CLI rather than a Command?
3. Where is the one mathematical policy, and why share it?
4. Why is this Simple Factory rather than Factory Method?
5. How would you adapt to a changed statistic?

Set reference-material/AI policy and a deadline in the exam README before release. The default policy permits course notes and one's own practice code but requires individual work and prohibits AI assistance or communication during the timed attempt. Adjust to your course rules.
