# Extend your OOP calculator: a six-part textbook

You have completed the [OOP calculator course](https://github.com/kaw393939/is218-oop-calculator): objects, an abstract calculation contract, encapsulated history, a CLI, tests, and CI. This sequel builds on that application to teach static operations, composition, a calculation factory, flexible inputs, application commands, and pandas data sources.

`main` is the course entry point and full textbook. Each `learn/...` branch contains the cumulative worked program for that part, with code and tests at the repository root. Read the explanation here, then inspect the matching branch while extending your own solution separately.

[Begin with the big picture](docs/big-picture.md) → [Prepare your sequel workspace](docs/setup.md) → [Part 1](docs/lessons/01-refactoring.md).

## The six parts

| Part and textbook lesson | Main question | Cumulative worked branch |
| --- | --- | --- |
| [1. Refactor the calculator you already built](docs/lessons/01-refactoring.md) | How can a calculation store its behavior? | [learn/01-refactoring](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/01-refactoring) |
| [2. Create calculations with a factory](docs/lessons/02-factory.md) | Who should select and construct the calculation? | [learn/02-factory](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/02-factory) |
| [3. One, two, and many operands](docs/lessons/03-flexible-inputs.md) | What if an operation needs one, two, or many inputs? | [learn/03-flexible-inputs](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/03-flexible-inputs) |
| [4. Turn application actions into commands](docs/lessons/04-commands.md) | How can different application actions share a contract? | [learn/04-commands](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/04-commands) |
| [5. Statistics and another input source](docs/lessons/05-statistics-csv.md) | Can different sources supply the same mathematical request? | [learn/05-statistics-csv](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/05-statistics-csv) |
| [6. Integrate, explain, and adapt](docs/lessons/06-transfer.md) | Can we adapt the design to a changed requirement? | [learn/06-transfer](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/06-transfer) |

The branches progress in order: Part 2 builds on Part 1, Part 3 builds on Part 2, and so on. Each keeps earlier behavior and adds the next change. Compare neighboring branches to see the increment. The first two interfaces use named operands; Part 3 introduces `*values` and `**options` when unary, collection, and configured operations justify them.

Each part has smaller checkpoints: retrieve prior knowledge → predict → examine a worked example → complete a partial example → run and explain → adapt independently. Study across several sessions. Tests and error reasoning accompany every part; setup and CI are reviewed from your earlier work.

## Run the matching worked branch

Use a separate reference clone, not your own solution folder:

```bash
git clone https://github.com/kaw393939/is218-command-factory-statistics.git calculator-reference
cd calculator-reference
git switch learn/01-refactoring
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m calculator
python -m pytest -q
```

Use [setup](docs/setup.md) for Windows commands. Run from the repository root. Parts 1–3 print demonstrations; Part 4 introduces the interactive loop; Part 5 adds pandas and CSV. Parts 1–4 require pytest for their tests, while Parts 5–6 add pandas.

Before moving to the next reference branch, check `git status` and save any intended experiments. Then switch and install that branch's requirements. [Branch navigation](docs/branches.md) explains fetching, switching, and comparisons. Your own solution can stay on its own working branch while you implement the lessons.

## Understand the final interaction

By Parts 5–6, the application supports requests such as:

```text
> add 2 3
Result: 5.0000
> power 3 exponent=4
Result: 81.0000
> divide 1 0
Error: float division by zero
> stddev 10 20 30 40 50
Result: 15.8114
> csv mean values.csv
Result: 30.0000
> clear
History cleared.
> history
History is empty.
> exit
Goodbye!
```

The factory constructs calculations; application commands calculate, show history, clear, and help. History preserves the earlier project's controlled collection boundary. Math returns numbers; commands return display text; the CLI prints it and handles expected failures.

## Read beside the code

[Architecture and request traces](docs/architecture.md) · [Python concepts](docs/concepts.md) · [EAFP/LBYL](docs/error-handling.md) · [Testing](docs/testing-guide.md) · [Glossary](docs/glossary.md) · [Reading guide](docs/reading-guide.md) · [Assignment](docs/assignment.md) · [Instructor guide](docs/instructor-guide.md) · [API migration](docs/migration.md).

A Simple Factory configures one product class here; it is not the inheritance-based Factory Method arrangement. The optional error-handling benchmark is an appendix experiment, not a rule that fewer conditionals guarantee faster code.

## Apply the ideas in assessments

[Practice](https://github.com/kaw393939/is218-statistics-practice) adapts the design to calibration and a latest-result action. The real assessment uses a different request-processing workflow. Both allow notes and prior code, supply familiar infrastructure, and require meaningful student tests and short design explanations. [Practice preparation](docs/practice-preparation.md) explains the policy and 60 automated plus 40 instructor-reviewed points.

## Maintain the course

`main` retains the canonical final application and branch-building/verification utilities for maintainers. Students use the branch for their current part; the final canonical code is not an unfinished starter.

From `main`, maintainers verify branch contents, textbook examples, and all six cumulative applications:

```bash
python tools/build_stages.py --check
python tools/verify_course.py --full
```

To prepare complete branch trees without changing Git:

```bash
python tools/build_lesson_branches.py --output-dir /tmp/calculator-lessons
```

That export includes each part's code, tests, cumulative lessons, and branch README. Review the trees, then commit/update the six learning branches in order so each part descends from the preceding part. `build_stages.py --output-dir` exports application files only; use the lesson-branch builder for publication. The verifier checks actual local/remote learning refs, including application freshness and ancestry.

With local assessment checkouts, also run `python tools/verify_assessments.py --mutations`. It verifies APIs/rubrics, passing solutions, expected starter failure, and the limits of copying unchanged course or practice code into another assessment.
