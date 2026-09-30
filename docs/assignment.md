# Assignment and completion criteria

## Purpose

Build a small statistics application while learning to assign responsibilities, recognize Command and Simple Factory, and explain the design using a vocabulary that transfers to other programs and languages. The calculator is the worked setting, not the limit of the concepts.

Follow the six lessons in your own cumulative solution. Keep a learning log and retain earlier tests. The tutorial is not a 90-minute assignment; it prepares you for the separate practice assessment.

## Required behavior

| Request | Acceptance example |
| --- | --- |
| manual | Enter 10 20 30 40 50; display Standard deviation: 15.8114 |
| csv | Read values.csv's fixed value column and display the same answer for the same observations |
| exit | End with Goodbye! |

Calculate sample standard deviation explicitly using ddof=1. Both sources share standard_deviation(values). Require at least two finite numeric values. Reject failed numeric conversion, missing cells, NaN, infinity, and nonfinite results. Completely blank CSV lines follow pandas' default skip behavior; a quoted empty cell is a missing observation and must be rejected.

Unknown commands, invalid manual input, missing files, missing columns, and expected CSV parsing failures show an Error: message and allow another request. EOF and Ctrl+C terminate cleanly. The CLI formats four decimal places; the shared function returns a float rather than preformatted text.

No column/filename selection, history/removal, GUI, extra arithmetic, undo, or Facade is required.

## Required design

| Component | Contract |
| --- | --- |
| standard_deviation(values) | Shared validation and mathematical policy |
| Command | Abstract execute() -> float contract |
| ManualStdDevCommand(values) | Store a snapshot and delegate during execution |
| CsvStdDevCommand(path="values.csv") | Store a path, read with pandas during execution, select value column, delegate |
| CommandFactory.create(name, values=None) | Normalize name; construct a request without executing; reject unknown names/absent manual values |
| CLI run() | Collect input, use factory, invoke execute(), display results, handle expected failures |

The assignment uses Simple Factory, not formal Factory Method. Refer to the matching Refactoring.Guru comparison when explaining that choice.

## Completion evidence

1. Your repository contains the app, supplied data, requirements, pytest settings, meaningful tests, and the CI workflow.
2. Your README lets someone install and run it from a fresh clone.
3. Tests and the four CI matrix jobs pass on your latest commit.
4. Your history records incremental checkpoints and your learning log records predictions and corrections.
5. Your reflection answers the final lesson's design and language-transfer questions.

The reference ends with twenty-two test cases. You may have more from independent exercises. No exact test count or 100% coverage gate is required. Explain the claims in your assertions; a green check alone does not establish understanding.

## How understanding is assessed

| Area | Evidence |
| --- | --- |
| Behavior | Demonstrate both sources and recovery after invalid input |
| Design | Trace request construction and execution; identify the shared policy |
| Vocabulary | Explain pattern categories and distinguish Simple Factory from Factory Method |
| Testing | Explain a fixture, assertion, and missing-path test |
| Workflow | Reproduce setup and investigate a CI failure |
| Transfer | Plan a new input source or recognize a suitable pattern in another scenario |

## Practice assessment

The forkable practice exam is 90 minutes, uses supplied skeletons, and produces a 100-point automated feedback score. The real test will not be exactly the same; expect a bounded change to the calculation or requirements. The instructor uses unchanged tests and design review for official grading. See [practice preparation](practice-preparation.md).
