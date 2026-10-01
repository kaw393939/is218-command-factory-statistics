# Extend your OOP calculator: a six-part textbook

You have completed the [OOP calculator course](https://github.com/kaw393939/is218-oop-calculator): objects, an abstract calculation contract, encapsulated history, a CLI, tests, and CI. This sequel builds on that application to teach static operations, composition, a calculation factory, flexible inputs, application commands, and pandas data sources.

[Begin with the big picture](docs/big-picture.md) → [Prepare your sequel workspace](docs/setup.md) → [Part 1](docs/lessons/01-refactoring.md).

## The six parts

| Part | Main question | Worked reference |
| --- | --- | --- |
| [1. Refactor the calculator you already built](docs/lessons/01-refactoring.md) | How can a calculation store its behavior? | [Snapshot](examples/stages/01-refactoring/README.md) |
| [2. Create calculations with a factory](docs/lessons/02-factory.md) | Who should select and construct the calculation? | [Snapshot](examples/stages/02-factory/README.md) |
| [3. One, two, and many operands](docs/lessons/03-flexible-inputs.md) | What if an operation needs one, two, or many inputs? | [Snapshot](examples/stages/03-flexible-inputs/README.md) |
| [4. Turn application actions into commands](docs/lessons/04-commands.md) | How can different application actions share a contract? | [Snapshot](examples/stages/04-commands/README.md) |
| [5. Statistics and another input source](docs/lessons/05-statistics-csv.md) | Can different sources supply the same mathematical request? | [Snapshot](examples/stages/05-statistics-csv/README.md) |
| [6. Integrate, explain, and adapt](docs/lessons/06-transfer.md) | Can we adapt the design to a changed requirement? | [Snapshot](examples/stages/06-transfer/README.md) |

Each part has small checkpoints: retrieve prior knowledge → predict → examine a worked example → complete a partial example → run and explain → adapt independently. Study across several sessions. Tests and error reasoning accompany every part; setup/CI are reviewed from your earlier work.

The first two snapshots deliberately use two named operands. Part 3 changes the interface to *values/**options when unary, collection, and configured operations justify it. Read [migration](docs/migration.md) before combining code from different stages. Historical learn branches are previous-course references; these six snapshots live in one checkout.

## Run the complete reference

This checkout is complete worked code, not the timed starter. Build your own solution separately following [setup](docs/setup.md).

```bash
python -m pip install -r requirements.txt
python -m calculator
python -m pytest -q
python tools/verify_course.py --full
```

```text
> add 2 3
Result: 5.0000
> square 3
Result: 9.0000
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

The factory constructs Calculations; application commands calculate, show history, clear, and help. History preserves the earlier project's controlled collection boundary. Math returns numbers; commands return display text; CLI prints it and handles expected failures.

## Read beside the code

[Architecture and request traces](docs/architecture.md) · [Python concepts](docs/concepts.md) · [EAFP/LBYL](docs/error-handling.md) · [Testing](docs/testing-guide.md) · [Glossary](docs/glossary.md) · [Reading guide](docs/reading-guide.md) · [Assignment](docs/assignment.md) · [Instructor guide](docs/instructor-guide.md).

The optional error-handling benchmark is an appendix experiment, not a rule that fewer conditionals guarantee faster code. A Simple Factory configures one product class here; it is not the inheritance-based Factory Method arrangement.

## Apply the ideas in assessments

[Practice](https://github.com/kaw393939/is218-statistics-practice) adapts the design to calibration and a latest-result action. The real assessment uses a different request-processing workflow. Both are open-notes/code adaptations with supplied familiar infrastructure, meaningful student tests, and short design explanations. [Practice preparation](docs/practice-preparation.md) explains the policy and 60 automated +40 instructor-reviewed points.

For maintainers with local assessment checkouts:

```bash
python tools/verify_assessments.py --mutations
```

It verifies aligned APIs and rubrics, passing solutions, expected starter failure, and the limits of copying unchanged teaching or practice code into another assessment.
