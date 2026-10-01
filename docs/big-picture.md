# Extend the calculator you already understand

This course continues [Learn OOP by Building a Calculator](https://github.com/kaw393939/is218-oop-calculator). You have already built `Add` and `Subtract` subclasses, an abstract calculation contract, an encapsulated `History`, an interactive loop, validation, tests, and CI. Keep that knowledge nearby. The next question is how the design changes when calculations accept different numbers of values and the application supports several kinds of action.

Before starting, explain how `Add(2, 3).get_result()` works, why clearing a list returned by `History.get_history()` does not clear the internal history, and how the loop accepts another request after an error. If one explanation is difficult, revisit that part of the prerequisite before adding a pattern.

## Six parts, one evolving application

| Part | Familiar starting point | New question |
| --- | --- | --- |
| [1. Refactor the math](lessons/01-refactoring.md) | Calculation subclasses and `get_result()` | Can a calculation store a stateless operation instead of inheriting its math? |
| [2. Create calculations](lessons/02-factory.md) | CLI name-to-class registry | Who should select the operation and construct its calculation? |
| [3. Support flexible inputs](lessons/03-flexible-inputs.md) | Two operands | How do one value, many values, and named settings share a creation interface? |
| [4. Represent application actions](lessons/04-commands.md) | History, REPL, and a familiar ABC | How can calculate, history, and clear share an execution contract? |
| [5. Add statistics and CSV](lessons/05-statistics-csv.md) | Collections and shared validation | Can terminal values and a file use the same mathematical policy? |
| [6. Explain and transfer](lessons/06-transfer.md) | Tests, error recovery, and CI | Can you adapt the design to a changed requirement and justify the change? |

Each part contains smaller checkpoints. Understand and test the change before reading the complete file. A full snapshot is a reference after a checkpoint, not the first explanation of it.

## Assign each responsibility deliberately

| Question | Component | What the separation permits |
| --- | --- | --- |
| How is the math performed? | `Operations` | Test math without prompts, files, or session state |
| Which math and inputs were requested? | `Calculation` | Store a request and execute it later |
| How is it constructed from a name? | `CalculationFactory` | Keep selection and construction rules in one place |
| Which application action should run? | A concrete `Command` | Invoke calculate, history, clear, or help through `execute()` |
| Where are successful entries owned? | `History` | Read a copy and change state through its methods |
| When should a result be recorded? | `CalculatorSession` | Compute first; record only success |
| Where do observations come from? | CLI or CSV reader | Supply inputs to the same factory and math |
| Who prints and recovers? | CLI | Keep interaction at the program boundary |

A feature says what a user can accomplish. A design assigns responsibilities. Python methods and pandas tables implement those choices. A static method is a language mechanism; it is not a design pattern.

The calculation factory configures one `Calculation` class with a selected callable. It is a Simple Factory helper, not the inheritance-based Factory Method pattern. Commands come later and represent application actions; the factory does not construct them.

More components add more calls and more code. Explain which requirement makes each component useful. Inheritance from the earlier course remains a valid design; this course explores composition because the new requirements make flexible operation configuration useful.

[Set up your workspace](setup.md) · [Follow a complete request](architecture.md) · [Compare the APIs](migration.md)
