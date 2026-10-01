# Understand the API changes before changing files

This course continues the completed [OOP calculator](https://github.com/kaw393939/is218-oop-calculator). The six parts deliberately preserve familiar ideas while changing the responsibilities needed for flexible math and application actions.

## From your completed OOP calculator

| Earlier design | Revised design | Why it changes |
| --- | --- | --- |
| `Add`/`Subtract` subclasses implement math | Static `Operations` methods supplied to a composed `Calculation` | Select stateless behavior without a calculation subclass for every formula |
| `Calculation(ABC)` stores `a` and `b` | A concrete calculation stores a callable, then a tuple of values/options | Begin with two operands; generalize only when unary/collection requests arrive |
| CLI maps names to classes | `CalculationFactory` maps names to operations and constructs calculations | Give selection and creation an explicit home |
| History stores calculation objects and display calls their math | History stores `(calculation, result)` after success | Display the recorded result without executing again |
| `History` owns its private collection | `History._entries` remains private; reads return a shallow copy | Preserve encapsulation through the refactoring |
| CLI performs each application action directly | Commands delegate calculate/history/clear to a session | Give different actions a shared execution contract |
| Separate prompts collect two operands | Final CLI accepts a single line such as `add 2 3` | Support different operand counts and named settings |
| Tests and CI already exist | Retain regressions and extend the evidence | A new architecture should not erase verified behavior |

The final APIs are `Calculation(values, operation, **options)` and `CalculationFactory.create(name, *values, **options)`. Parts 1–2 intentionally begin with simpler two-operand forms. Do not import the final flexible signature into the first checkpoint before explaining the requirement that motivates it.

`History.add(calculation, result)` records success, `get_history()` returns a shallow list copy, and `clear()` changes the owned entries. `CalculatorSession` owns a `History`, exposes `get_history()` and `clear()`, and calculates before calling `add()`. No caller edits a public session-history list.

Changing an API or terminal protocol requires updating tests that specify that interface. Retain the behavior claims—correct arithmetic, independent history, successful-only recording, and recovery—and explain intentional differences. Refactoring is not a reason to discard regression evidence.

## From older versions of this statistics course

The former `CommandFactory`, `ManualStdDevCommand`, and `CsvStdDevCommand` are replaced by a calculation factory and distinct application commands. CSV is an input source, not a separate mathematical command. Commands return display text, while operations and calculations return numbers.

The earlier local snapshot names map to the revised progression:

| Earlier folder/lesson | Current part |
| --- | --- |
| `01-operations` and the start of `02-calculations` | [1. Refactoring](lessons/01-refactoring.md) |
| Fixed-arity portion of `03-factory` | [2. Factory](lessons/02-factory.md) |
| Flexible calculation/factory portions | [3. Flexible inputs](lessons/03-flexible-inputs.md) |
| `04-commands` | [4. Commands](lessons/04-commands.md) |
| `05-statistics-csv` | [5. Statistics and CSV](lessons/05-statistics-csv.md) |
| `06-ci` | [6. Transfer](lessons/06-transfer.md) |

Shared finite-number conversion now lives in `calculator/validation.py`; `statistics.py` owns statistical behavior. Factory option validation uses explicit steps so the first explanation does not depend on set subtraction or `zip`.

Practice and exam now require different adaptations of the same ideas. A population-default change is no longer the exam's distinguishing task. Read each assessment's own published contracts, resource rules, and scoring. The automated portion is 60 points, followed by 20 points for student tests and 20 for traces/design explanation.

Maintainers update source, snapshots, lessons, assessment starters/solutions, and grading contracts together. `tools/verify_assessments.py` checks local sibling assessment repositories without distributing a real-exam solution as teaching code.
