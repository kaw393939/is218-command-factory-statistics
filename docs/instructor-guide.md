# Teach the decisions, not just the files

## Start from the previous assignment

Students already built the [OOP calculator](https://github.com/kaw393939/is218-oop-calculator). Ask them to trace construction, get_result(), and history display. Then introduce a variable-length dataset and ask which assumptions no longer fit. Let them identify the contract change before showing the new architecture.

Use [the big picture](big-picture.md) before Stage 1. Distinguish feature, design, and implementation. Introduce categories through familiar scenarios, then focus implementation on Command and Simple Factory. Do not turn the overview into an obligation to code every pattern.

## Suggested instructional rhythm

| Stage | Pause for a prediction | Evidence of understanding | Likely misconception |
| --- | --- | --- | --- |
| 1 | Equal values / one observation | Explain sample statistic and validation | Pandas automatically enforces our input policy |
| 2 | Change original list after construction | Distinguish request from result | execute() naming alone establishes Command |
| 3 | Change file before a second execution | Trace DataFrame → Series → shared policy | CSV constructor freezes file contents |
| 4 | Create without executing | Identify selection and construction | Simple Factory equals Factory Method |
| 5 | Invalid request followed by valid request | Trace recovery and invoker roles | Factory should also prompt and calculate |
| 6 | Local environment absent on CI | Read the useful failure evidence | An old green run verifies current work |

Teach across multiple sessions; the tutorial is not timed. Smaller numbered checkpoints allow a student to run one change before absorbing the next. Independent exercises intentionally go beyond supplied tests.

## Use Refactoring.Guru actively

Assign exact sections rather than whole catalogs. Before reading, give a question; afterward, map roles to this application and discuss a tradeoff. Use [the reading guide](reading-guide.md). Link to the original site for diagrams and detailed examples; our lessons provide original calculator examples and explanations, not copied chapters or illustrations.

Ask students to explain how our receiver work is represented by a function and how the CLI combines setup and invocation in this small design. They should recognize the adaptation rather than claim a literal match to every diagram box.

## Teach tests with the code

Demonstrate one direct assertion and one expected exception before parametrization. Introduce tmp_path during CSV testing. Before showing the CLI tests, expand the reference lambda into a named fake_input function and walk each iterator answer against an input() call. See [testing guide](testing-guide.md).

Keep older checks. Do not make coverage percentage a substitute for correct assertions. The exam does not impose a 100% coverage threshold.

## Discussion prompts and review activities

- Explain which component changes when prompt text changes, then when the statistic changes.
- Show create() returning execute() and ask which contract it breaks.
- Give an Observer or Adapter scenario and ask for a simpler alternative too.
- Ask a student to explain a pattern without using its name, then identify it.
- Have students review a README from a fresh clone and improve one ambiguous instruction.
- Use [language transfer](language-transfer.md) to identify known design relationships and unknown language rules.

Suggested assessment: behavior 30%, design explanation 25%, meaningful tests 20%, reproducible workflow 15%, transfer reflection 10%. This tutorial rubric is distinct from the practice exam's published automated categories; adjust and announce your course grading before assigning it.

## Prepare for the 90-minute practice

Use [is218-statistics-practice](https://github.com/kaw393939/is218-statistics-practice). Students should already have practiced environment setup and GitHub access. The timed attempt includes setup, reading, implementation, checks, and submission. The public solution branch is available; instruct students to consult it after their rehearsal if you want an unaided first attempt.

The real test stays a familiar structure with a bounded variation. Do not reveal the exact private exam plan in public teaching commits. The local instructor kit holds that plan, solution, and immutable-commit grader. Confirm the exam resource policy, release access, deadline, and submission channel before release.

Public fork-owned Actions scores are feedback. Official grading uses instructor-owned checks against the submitted SHA and a short responsibility review. A student can alter tests in their fork, so a green fork workflow alone cannot establish official correctness.

## Maintain the course

All branches carry the revised shared readings; their application snapshots remain cumulative. Embedded complete-file examples are checked against the matching branch. Run `python tools/verify_course.py --full` from a reference checkout with requirements installed and all branches fetched. The main-branch Course checks workflow verifies documentation and the six application snapshots.

When changing application code, update its matching lesson and downstream snapshots deliberately. When only explanation changes, preserve application behavior and keep the branch references accurate.
