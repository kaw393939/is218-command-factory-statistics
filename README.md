# Learn design patterns by building a statistics calculator

You already built an OOP calculator. Now learn how to organize requests, separate responsibilities, and explain your code using a vocabulary that carries into other programs and languages.

The project is small: calculate **sample standard deviation** from typed values or a supplied CSV using pandas. The lessons make the design visible: **Command** represents the requests, a **Simple Factory** constructs them, and the CLI decides when to execute them.

## Begin with the question, not the code

[Start here: the big picture](docs/big-picture.md) → [Set up your own solution](docs/setup.md) → [Stage 1](docs/lessons/01-statistics.md).

**main is the course home, not a runnable application.** All lesson readings are available here. The learn branches contain cumulative working snapshots. [Branch instructions](docs/branches.md) explain how to inspect references while building your own solution separately.

## See what you will build

```text
> manual
Enter values separated by spaces: 10 20 30 40 50
Standard deviation: 15.8114
> csv
Standard deviation: 15.8114
> exit
Goodbye!
```

## Your learning journey

| Stage | Lesson | Worked reference |
| --- | --- | --- |
| 1 | [From two operands to a collection](docs/lessons/01-statistics.md) | [Cumulative code](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/01-statistics) |
| 2 | [Turn a request into a Command](docs/lessons/02-command.md) | [Cumulative code](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/02-command) |
| 3 | [Give a CSV request the same contract](docs/lessons/03-csv.md) | [Cumulative code](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/03-csv) |
| 4 | [Move construction into a Simple Factory](docs/lessons/04-factory.md) | [Cumulative code](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/04-factory) |
| 5 | [Make the CLI an invoker](docs/lessons/05-repl.md) | [Cumulative code](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/05-repl) |
| 6 | [Publish, investigate, and explain your design](docs/lessons/06-ci.md) | [Cumulative code](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/06-ci) |

Each lesson starts with a problem, asks for predictions, introduces small coding checkpoints, explains unfamiliar tools, and ends with an independent exercise. Follow **predict → type → run → explain → change one thing**. This tutorial is preparation over multiple study sessions; the practice exam is a separate 90-minute attempt.

## Understand the wider design landscape

- [Pattern categories and familiar features](docs/patterns-and-features.md): creation, structure, behavior, and examples beyond calculators.
- [Architecture and request traces](docs/architecture.md): follow construction, execution, data conversion, and display.
- [Guided Refactoring.Guru readings](docs/reading-guide.md): focused sections with questions and calculator mappings.
- [Learning other languages](docs/language-transfer.md): transfer design understanding while learning syntax, libraries, and runtime rules.

## Keep nearby as you work

[Assignment criteria](docs/assignment.md) · [Testing guide](docs/testing-guide.md) · [Troubleshooting](docs/troubleshooting.md) · [Concepts](docs/concepts.md) · [Glossary](docs/glossary.md) · [Learning log](docs/learning-log.md) · [Instructor guide](docs/instructor-guide.md)

A short function-based solution could meet the feature requirements. We deliberately practice request objects and centralized construction so you can explain when they help and what complexity they add. You only implement Command and Simple Factory; the other patterns are recognition and transfer examples.

## Rehearse after learning

Read [practice preparation](docs/practice-preparation.md), then fork [the practice starter](https://github.com/kaw393939/is218-statistics-practice). It includes environment instructions and 100-point Actions feedback. Review its separate solution branch after your attempt.

**The real test will not be exactly the same.** Expect a bounded change to the calculation or requirements. Learn to trace and adapt your design rather than memorize a particular answer.
