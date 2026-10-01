# Practice adapting the ideas with open notes and code

Complete all six parts before attempting [the practice assessment](https://github.com/kaw393939/is218-statistics-practice). Your completed prerequisite, course notes, and prior code are useful resources. The aim is to apply a known design to changed requirements, not reconstruct every file from memory.

The practice and [real exam](https://github.com/kaw393939/is218-statistics-exam) each allow 90 minutes. Follow each repository's published contracts and resource rules: work individually, use permitted notes/prior code, and do not use AI assistance or communicate with others during the attempt. Environment instructions and supplied parsing keep the focus on adaptation.

## Use the same ideas for different tasks

| Concept | Teaching preparation | Practice application | Exam application |
| --- | --- | --- | --- |
| Static math and callable composition | Binary/unary math, power, sum | Calibration adjustment and collection span | Distance and bounded clipping |
| Factory creation | Names, counts, and named settings | Register the practice operations and settings | Register different operations/settings |
| Application command | Calculate, history, clear, help | Inspect the last successful entry | Execute a batch and report a summary |
| Successful-only state | Compute before recording | Repair recording that happens before success | Preserve successes and separately report failures |
| Input and math separation | CSV observations feed shared math | Apply the practice collection operation to CSV | Prepare calculations from supplied CSV request rows |
| Recovery | Invalid terminal request followed by valid request; prepared sequence continues | Trace recovery and unchanged state | Continue after an expected row failure |

Read the exact formulas, row format, return contracts, and failure policy in the assessment itself. The distinction is behavioral adaptation, not a changed class name, dataset, or deviation default. You may reuse useful infrastructure, but unchanged teaching code cannot supply all required behavior.

The teaching sequence exercise prepares the execute-and-continue idea. Exam parsing infrastructure is supplied so new row syntax is not a memory test of pandas details. Separate row preparation from execution: a returned calculation is not yet a successful result.

## Rehearse decisions before the timer

Without looking at a solution, identify where each of these changes belongs: a unary formula, a named setting, a collection minimum rule, a new history-reading action, another input source, and continued processing after failure. Draw a successful request and an exception path. Check whether your explanation names values, return types, and skipped state changes.

Practice using your notes as an index. Locate a callable-reference example, argument unpacking, narrow exception handling, a history read, a CSV fixture, and a recovery test. Finding relevant evidence is more useful than copying complete files and hoping the contracts match.

| Time | Suggested allocation |
| --- | --- |
| 0–10 minutes | Read the changed contracts; confirm environment and supplied infrastructure |
| 10–30 | Implement operations and creation adaptations |
| 30–50 | Implement the new action and state behavior |
| 50–65 | Complete input/integration behavior and expected-error recovery |
| 65–80 | Write discriminating tests and short traces/design explanation |
| 80–90 | Run checks, commit, push, and submit the required revision identity |

This allocation is a planning aid. Use the assessment's own deadline, submission instructions, and setup policy.

## Interpret the score correctly

The rubric is 60 points for automated behavior, 20 for meaningful student-written tests, and 20 for request traces/design explanation. Passing every automated check establishes the behavior portion, not an automatic 100/100. Fork feedback is provisional; official grading targets the submitted commit with instructor-owned checks and review.

A strong student test detects a plausible adaptation bug—for example, ignored nondefault settings or later work skipped after a failure. Explain its claim. A strong trace identifies preparation, execution, state change, and recovery rather than listing method names alone.

After the practice attempt, compare your design and tests with the released practice reference. Repeat a bounded variation from a clean starter. Do not use a public real-exam solution as preparation; the instructor maintains the exam reference separately.
