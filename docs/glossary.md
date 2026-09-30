# Glossary of terms, principles, and design ideas

Use this page while reading the lessons and when explaining your code. Each idea includes evidence from this calculator. A principle guides a decision; a pattern describes an arrangement; a language feature implements part of that arrangement.

## Principles: questions to ask about your design

| Idea | Plain meaning | Calculator example | Avoid this misunderstanding |
| --- | --- | --- | --- |
| Separation of concerns (SoC) | Keep distinct concerns in components that can be understood and changed separately | CLI handles interaction; commands represent requests; the shared function validates and calculates | It does not require a separate class for every line or forbid components from collaborating |
| Don't Repeat Yourself (DRY) | Give each piece of knowledge or policy one authoritative home | Both commands call standard_deviation() instead of maintaining two copies of the statistical policy | Similar-looking lines are not always duplicated knowledge; unrelated logic should not be forced into one abstraction |
| Single Responsibility Principle (SRP) | Group behavior that changes for the same reason; separate different reasons to change | A prompt change belongs in the CLI, while a mathematical-policy change belongs in statistics.py | It does not mean a class can have only one method; it is related to SoC but focuses on responsibility and reasons to change |
| Keep It Simple (KISS) | Prefer the clearest design that meets the actual requirements | A small conditional Simple Factory selects two request types | The fewest lines are not necessarily the easiest code to understand |
| You Aren't Gonna Need It (YAGNI) | Avoid building speculative features before they are required | We do not add undo, plugin loading, or persistent history | It does not mean skipping required validation or tests |
| High cohesion | Keep closely related behavior together | Shared numeric validation and statistical policy live together | More methods in one file do not automatically mean better cohesion |
| Low coupling | Limit how much a component depends on another's internal details | CLI invokes execute() without reading each command's stored fields | Coupling is reduced, not eliminated: the factory still knows concrete constructors |
| Program to an interface | Let callers depend on an agreed capability rather than concrete implementation details | A caller asks either Command to execute() | An interface can be a behavioral agreement; not every language needs an explicit interface keyword |
| Composition | Build behavior by combining collaborating parts | CLI uses a factory and a returned command; commands use a shared function | Reusing behavior does not always require inheritance |
| Encapsulation | Put state and behavior behind a boundary that controls access appropriately | Commands own request inputs and expose execute() | Our public values list is not fully protected or immutable; list(values) only isolates it from the caller's original list |
| Explicit contracts | State accepted inputs, outputs, and failure behavior | At least two finite values produce a float; invalid values raise ValueError | Type annotations alone do not enforce the full contract |
| Testability | Make behavior observable with controllable inputs and dependencies | Command inputs are supplied through constructors rather than keyboard prompts | Testability does not mean replacing all real behavior with mocks |

### DRY is about knowledge, not merely text

If manual and CSV commands each contain the same sample-deviation formula, changing the policy requires two coordinated edits. That is duplicated knowledge. Our shared function gives that decision one home.

Two tests can legitimately contain the same dataset because they verify different paths. Two components can also have similar code for unrelated rules. Before extracting a helper, ask whether those lines represent the same decision and should change together.

### Separation of concerns and SRP work together

Separation of concerns helps you distinguish input, construction, execution, calculation, and display. SRP helps you ask which responsibilities change for different reasons. Neither promises that every component has exactly one tiny task: the shared function's validation and calculation jointly define its statistical contract.

## SOLID: a vocabulary for evaluating relationships

SOLID groups five design principles. Use them as questions, not as a checklist claiming this tiny application perfectly implements everything.

| Principle | Question | Evidence and limitation here |
| --- | --- | --- |
| S — Single Responsibility | Are different reasons to change separated? | Prompt wording and statistical policy have different homes |
| O — Open/Closed | Can an extension reuse stable behavior without rewriting it? | A new command can reuse an execute() caller; the factory and CLI input choices may still need edits |
| L — Liskov Substitution | Can an implementation honor the contract expected of its abstraction? | Both Commands promise a numeric result or useful input/file failure; unexpectedly returning display text would break callers |
| I — Interface Segregation | Are callers forced to depend on methods they do not need? | The execution contract does not require unrelated printing or history methods |
| D — Dependency Inversion | Do important policies depend on abstractions rather than concrete details? | A caller can rely on Command; the factory deliberately imports concrete classes, and the statistic directly depends on pandas. Do not claim complete dependency inversion |

Dependency injection is a related technique: supply a dependency from outside rather than construct it internally. Passing a calculation service into a command would be an example. Passing numeric values is ordinary input, not by itself evidence that the design follows Dependency Inversion. This course does not require a dependency-injection framework.

## Patterns and their categories

| Term | Plain meaning | Example here |
| --- | --- | --- |
| Algorithm | Procedure for obtaining a result | Standard-deviation calculation |
| Design pattern | Reusable arrangement addressing a recurring design problem | Command |
| Creational | Concerned with construction | Factory-style selection |
| Structural | Concerned with arranging components | Adapter, discussed as a transfer example |
| Behavioral | Concerned with actions/responsibilities/communication | Command |
| Command | Object representing a request | ManualStdDevCommand(values) |
| Invoker | Caller initiating execution | CLI |
| Receiver | Component performing delegated work in the general pattern | Shared function fills the work role in our simplified design |
| Simple Factory | Selects and constructs a concrete object | CommandFactory.create() |
| Factory Method | Creation delegated through an overridable creator method | A different design, not implemented here |

## Objects, contracts, and Python

| Term | Plain meaning | Example here |
| --- | --- | --- |
| ABC | Abstract base class declaring required behavior | Command(ABC) |
| Constructor | Initialization of a new object | __init__ stores request inputs |
| Snapshot | Copy taken at a particular time | list(values) |
| Abstraction | Describe useful behavior without exposing every implementation detail | Command exposes execute() |
| Polymorphism | Make the same request and get implementation-specific behavior | Either concrete command handles execute() |
| Inheritance | Establish a subtype relationship | ManualStdDevCommand inherits from Command |
| Delegation | Ask another component to perform part of the work | Command delegates mathematics to standard_deviation() |
| State | Information belonging to an object at a point in time | Saved values or CSV path |
| Side effect | Observable change beyond returning a result | Printing output or writing a file |
| Immutability | State cannot change after creation | Not guaranteed by our public list attribute |
| Type hint | Annotation describing expected types | execute() -> float; not runtime validation |
| API / interface | The operations a component makes available to callers | create() and execute() contracts |
| Refactoring | Reorganize implementation while preserving intended observable behavior | Extract construction selection into the factory |

## Data and numerical behavior

| Term | Plain meaning | Example here |
| --- | --- | --- |
| DataFrame | Two-dimensional pandas table | CSV after read_csv() |
| Series | One-dimensional pandas collection | frame["value"] |
| ddof | Adjustment in the variance denominator n-ddof | ddof=1 for sample deviation |
| NaN | A special nonfinite numeric value, often marking missing data | Rejected input |
| Validation | Check that input meets the application contract | Reject fewer than two finite values |
| Floating-point precision | Finite representation can introduce rounding differences | Compare calculated results with pytest.approx |
| Formatting | Convert a value into presentation text | result:.4f displays four decimal places without changing the function result |

## Testing and workflow

| Term | Plain meaning | Example here |
| --- | --- | --- |
| Fixture | Test setup/tool supplied by pytest | tmp_path |
| Parametrization | Run one test with several inputs | Invalid-value cases |
| Mock/patch | Replace a dependency for a controlled test | Fake input() |
| REPL | Read–evaluate–print loop | Interactive CLI |
| CI | Repeat automated checks in a fresh environment | GitHub Actions workflow |
| Commit SHA | Identity of a Git commit | Submitted version |
| Regression test | Check that earlier behavior still works after changes | Retain Stage 1 tests when adding CSV input |
| Unit / integration testing | Test a focused component / cooperating components | Shared function checks / CLI session checks |
| Reproducibility | Another environment can repeat setup and obtain the expected behavior | Fresh clone, declared requirements, and CI |

## Practice using the vocabulary

For each claim, identify the relevant idea and point to code that supports or contradicts it:

1. “Both commands should maintain their own copy of the formula.”
2. “The CSV command should ask the user which file to read.”
3. “Adding a command means no other file can ever change.”
4. “The factory returns the calculated result.”
5. “A type hint guarantees execute() returns a float.”

<details>
<summary>Compare after explaining</summary>

1. DRY: share the mathematical policy.
2. Separation of concerns: input belongs in the caller; this assignment uses a fixed filename.
3. Open/Closed has limits: factory selection and input preparation may still change.
4. Creation and execution are distinct responsibilities; the factory returns a Command.
5. Python annotations do not enforce the behavioral contract at runtime.

</details>

A word alone is not proof of a design. Explain the relationship it describes, point to the implementation, and acknowledge its limitations.

[Big picture](big-picture.md) · [Architecture](architecture.md) · [Patterns and features](patterns-and-features.md) · [Testing guide](testing-guide.md)
