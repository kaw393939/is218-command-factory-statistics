# Vocabulary with evidence

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
| ABC | Abstract base class declaring required behavior | Command(ABC) |
| Constructor | Initialization of a new object | __init__ stores request inputs |
| Snapshot | Copy taken at a particular time | list(values) |
| DataFrame | Two-dimensional pandas table | CSV after read_csv() |
| Series | One-dimensional pandas collection | frame["value"] |
| ddof | Adjustment in the variance denominator n-ddof | ddof=1 for sample deviation |
| NaN | A special nonfinite numeric value, often marking missing data | Rejected input |
| Fixture | Test setup/tool supplied by pytest | tmp_path |
| Parametrization | Run one test with several inputs | Invalid-value cases |
| Mock/patch | Replace a dependency for a controlled test | Fake input() |
| REPL | Read–evaluate–print loop | Interactive CLI |
| CI | Repeat automated checks in a fresh environment | GitHub Actions workflow |
| Commit SHA | Identity of a Git commit | Submitted version |

A word alone is not proof of a design. Explain the relationship it describes and point to its implementation.
