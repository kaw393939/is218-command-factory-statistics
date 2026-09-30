# Prepare for a timed attempt

The tutorial teaches incrementally with worked references. The [practice test](https://github.com/kaw393939/is218-statistics-practice) supplies a fresh skeleton and a 100-point feedback workflow. You should be able to implement the relationships without copying whole files blindly.

**The real test will not be exactly the same.** Expect a bounded change in the calculation or requirements. Read its README carefully; familiar interfaces do not guarantee identical expectations.

## Readiness check

Without looking at the solution, can you:

- Explain Command and Simple Factory using actual responsibilities?
- Store input during construction and execute later?
- Read the fixed value column with pandas?
- Apply one validation/calculation policy to both sources?
- Recover from invalid requests in a terminal loop?
- Install dependencies, run tests, push a commit, and find an Actions score?

## Rehearse the entire workflow

Fork the practice starter, clone your fork, follow its environment instructions, and start a 90-minute attempt. Use its published resource policy. The incomplete starter scores 5/100 for the supplied abstract interface and is expected to fail. Run pytest and grading/grade.py as you build.

Commit and push your final work; record the commit SHA. Actions produces a score summary and downloadable feedback. A failed workflow can still have a valid partial-score artifact. Review the public solution branch after the attempt, identify gaps in your learning log, and repeat from a fresh starter if useful.

## Suggested time allocation

| Time | Work |
| --- | --- |
| 0–10 minutes | Read requirements, verify setup and skeleton |
| 10–35 | Shared calculation and manual request |
| 35–55 | CSV request and factory |
| 55–75 | CLI, errors, and focused tests |
| 75–90 | Full checks, explanation, commit, push, submission |

These are planning estimates, not required timestamps. Keep the final submission step inside the time limit.

## Feedback is evidence, not the whole assessment

Twenty acceptance checks award five points each. Public fork tests can be changed, so the instructor uses their unchanged tests against the submitted commit for official grading. The short design explanation helps confirm that classes have meaningful responsibilities. No tutorial or exam requirement asks you to implement every pattern in the overview.
