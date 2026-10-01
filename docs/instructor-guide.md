# Teach the extension from a known working program

Students have completed [the OOP calculator](https://github.com/kaw393939/is218-oop-calculator). That course already covers objects, abstract `Calculation`, `Add`/`Subtract`, polymorphism, encapsulated `History`, REPL, finite-number validation, recovery, pytest, coverage, and CI. Begin by retrieving that knowledge, then introduce the changed requirement. The textbook takes several sessions; it is not the 90-minute assessment.

## Diagnose the starting knowledge

Ask students to trace `Add(2, 3).get_result()`, explain a shallow history-list copy, and identify why a rejected calculation is not recorded. Ask which checks ran for their submitted commit. These are prerequisite diagnostics, not new graded content. Give a specific prerequisite reading when one explanation is missing.

Do not restart with a blank project or teach each existing mechanism as unfamiliar. State which behavior survives the refactoring and which API changes deliberately. Preserve their regression assertions while updating tests that depend on an intentionally changed interface.

## Keep six main parts and smaller checkpoints

| Part | New conceptual focus | Prediction pause | Evidence of understanding |
| --- | --- | --- | --- |
| 1: Refactoring | Static operations and a composed two-operand calculation | Is the stored operation a function or an answer? | Contrast callable/call and construction/execution |
| 2: Factory | Centralized selection and construction, still fixed arity | What does `create()` return? | Factory spy test and name-to-object trace |
| 3: Flexible inputs | Unary/collection arity, then positional/named forwarding | What exactly reaches the operation? | Expand `*values`/`**options` and test a nondefault setting |
| 4: Commands | Distinct application actions using familiar abstraction | Which state changes after a failed calculation? | Concrete actions first; private history access; skipped-add trace |
| 5: Statistics and CSV | Shared observation policy across input sources | Where could missing data be lost? | Table/column/value trace and source-equivalence tests |
| 6: Transfer | Prepared sequences and independent adaptation; CI review | Does later work run after one item fails? | Valid/invalid/valid sequence and successful-only history |

The final application has many collaborating elements. Do not present the entire file map before students understand one request. Begin with fixed two-operand interfaces, introduce a factory, then generalize when unary/collection/settings requirements make it necessary. Use explicit option-validation loops before compact set operations or dictionary transformations.

Write concrete commands before adding `Command(ABC)`. Students recognize ABC from the prerequisite; retrieval should explain the new contract rather than repeat an entire introduction. Compare static math, instance result retrieval, and abstract action requirements. A missing-method failure establishes Python's enforcement, not semantic correctness or return-type checking.

Keep encapsulation intact. `History` owns `_entries`; `CalculatorSession` owns a `History` and computes before adding. Commands use `get_history()`/`clear()`. Saved results avoid re-execution, while shallow reads still share contained calculation objects. Explain both benefits and limits.

## Give each checkpoint a learning rhythm

Start with a concrete requirement and a prediction. Explain a small worked change beside the relevant lines. Trace values/types, control flow, and state. Offer a completion task with one missing decision, then an independent variation. Finish with a retrieval question about an earlier part.

The complete file comes after those steps. Telling students to type one method at a time while showing only a finished implementation supplies little conceptual scaffolding. Gradually reduce help rather than abruptly moving from copying to a whole application.

The [IES practice guide](https://ies.ed.gov/ncee/wwc/PracticeGuide/1) supports alternating worked examples and problem solving and integrating concrete and abstract representations. These general recommendations inform the structure; they do not prove this precise programming sequence is effective. Pilot tasks with representative students and revise based on observed difficulty and time.

Teach one test before parametrization and a named fake-input function before a lambda. Revisit an earlier concept in a changed setting: construction timing through a spy, encapsulation through a returned-copy mutation, recovery through two consecutive requests. Distinguish syntactic familiarity from explaining responsibility.

## Keep error handling connected to correctness

Use failure frequency as the EAFP/LBYL heuristic, not CPU-versus-memory categories or unpredictable input order. Conversion can attempt `float()`; count rules can check explicitly; file reads can fail after existence checks. Trace the origin, propagation, handler, and skipped state change.

Registries reduce repeated selection logic. They do not establish faster hardware execution. Branch prediction and benchmark interpretation remain optional enrichment in [error handling](error-handling.md), not required performance claims.

## Align open-code assessments with the practiced thinking

The practice and exam reuse the same design ideas but require different behavior. Useful prior code is allowed; unchanged copying must be insufficient. Avoid superficial distinctions such as renamed classes, changed example data, or one default constant.

| Objective | Practice evidence | Exam evidence |
| --- | --- | --- |
| Configure static behavior | Adjustment and span with published contracts | Distance and clipping with different published contracts |
| Construct without executing | Factory adaptations | Factory adaptations inside prepared batch requests |
| Execute application actions | Last successful entry | Batch execution and success/failure summary |
| Control owned state | Repair record-before-success defect | Retain successful entries while tracking/reporting expected failures |
| Separate input from math | CSV observations for span | Supplied CSV row parser feeding calculation creation |
| Explain/testing transfer | Tests and request traces | Different tests and batch/error traces |

Part 6 prepares processing a sequence of calculations and continuing after a failure. Supply exam row parsing and explicit format/behavior contracts so students are not assessed on a new parser they never practiced. Do not publish the exact exam solution as a teaching transfer exercise.

Provide all acceptance requirements in the assessment. Hidden tests vary values and published cases; they do not add unannounced rules. Keep the scope bounded enough for 90 minutes and pilot the workload. Supplied setup/parsing infrastructure and reused basics let students focus on decisions.

Assessment thinking should match lesson practice, as described by [Carnegie Mellon's alignment guidance](https://www.cmu.edu/teaching/assessment/basics/alignment.html). Students must rehearse deciding which component changes, not only reproducing that component's current code.

## Score different evidence honestly

| Evidence | Points |
| --- | ---: |
| Automated required behavior/adaptation | 60 |
| Meaningful student-written tests with justified cases | 20 |
| Request traces and design explanation | 20 |

Automated feedback reports only the behavior portion. Manual review establishes whether tests detect relevant bugs and whether traces explain construction, execution, state, and recovery. Do not equate an automated pass with demonstrated understanding or award test points for assertion count alone.

Announce the 90-minute limit, open notes/prior code, individual-work rules, no AI/communication during the attempt, access timing, setup expectations, deadline, and submission channel before release. Keep notification and integrity procedures out of student program flows.

Keep real-exam solutions and official grading in the instructor-owned workspace. Fork-owned feedback is provisional; official checks and review target the submitted commit. Before release, verify that the intended solution passes and that unchanged teaching/practice code fails the distinct adaptation requirements. A copy-resistance check cannot establish completion time; a student pilot can.

## Maintain course consistency

`main` is the course entry point and full textbook, and retains the canonical final application for maintenance. Each learning branch places its cumulative program, stage-relevant tests, and lesson material at the repository root. Maintain the direct ancestry from Part 1 through Part 6 so neighboring branch comparisons show one deliberate increment.

Edit canonical application/tests and branch-content transformations in `tools/build_stages.py`, and update lesson examples with the matching part's source. Check application freshness and ancestry on actual local/remote learning refs with `python tools/build_stages.py --check`; run `python tools/verify_course.py --full` from `main` for documentation and all six branch applications.

`python tools/build_lesson_branches.py --output-dir /tmp/calculator-lessons` prepares complete root trees with code/tests, cumulative lessons, setup/navigation, and each branch's README. It does not change Git. Review the export, then commit/update branches in order, preserving the direct parent-child progression. The application-only `build_stages.py --output-dir` export is not the complete publication content. Check current-part help text rather than advertising later features prematurely. Parts 1–4 declare pytest only; pandas first becomes required in Part 5.

The published branch set is `main` and the six current learning branches. The previous branch names have been replaced. Keep current branch names, linear ancestry, supporting explanations, assessment contracts, solutions, and rubric aligned. [Migration](migration.md) records intentional API changes; [navigation](branches.md) identifies switching and comparisons. Verify the sibling assessments after a change to shared concepts or contracts.
