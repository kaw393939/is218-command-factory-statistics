# Stage 4: Move construction into a Simple Factory

[Previous lesson](03-csv.md) · [Worked branch](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/04-factory) · [Course home](https://github.com/kaw393939/is218-command-factory-statistics)

[Next lesson](05-repl.md)

## First see the decision that will move

You now have two concrete requests with different constructors. A caller could choose directly:

```python
if name == "manual":
    command = ManualStdDevCommand(values)
elif name == "csv":
    command = CsvStdDevCommand()
else:
    raise ValueError("Unknown command")

result = command.execute()
```

This illustrative fragment works, but makes the caller responsible for concrete construction details. If another caller needs the same selection rules, those rules may be repeated. We will move them into one creation helper.

**By the end:** you can describe what the factory centralizes, what it returns, and how Simple Factory differs from Factory Method.

## Guided reading

Read [Refactoring.Guru: Factory Comparison](https://refactoring.guru/design-patterns/factory-comparison), section 4 on Simple Factory. Briefly compare section 5 on Factory Method.

Answer: Does our design require a creator subclass overriding a creation method? Where is the conditional selecting the concrete class? Use these answers to name the design accurately.

## Files in this stage

| File | Action |
| --- | --- |
| calculator/factory.py | Create central construction selection |
| calculator/__main__.py | Demonstrate factory then execution |
| tests/test_factory.py | Add selection and rejection checks |
| Existing commands/statistics/tests | Retain |

## 4A — Extract selection into a Simple Factory

Create calculator/factory.py:

<!-- reference: learn/04-factory:calculator/factory.py -->
```python
"""Simple Factory: centralize which concrete command to construct."""
from calculator.commands import Command, CsvStdDevCommand, ManualStdDevCommand


class CommandFactory:
    @staticmethod
    def create(name: str, values=None) -> Command:
        name = name.strip().lower()
        if name == "manual":
            if values is None:
                raise ValueError("Manual command requires values.")
            return ManualStdDevCommand(values)
        if name == "csv":
            return CsvStdDevCommand()
        raise ValueError(f"Unknown command: {name}")
```

| Line/concept | Reason |
| --- | --- |
| @staticmethod | No factory instance state is needed for this helper |
| name.strip().lower() | Accept surrounding spaces and mixed case |
| values is None | Distinguish absent manual inputs from a provided empty list |
| return ManualStdDevCommand(values) | Construct the appropriate request |
| return CsvStdDevCommand() | Use the documented default CSV path |
| Final ValueError | Reject unsupported request names |

An empty list is not None. The factory can construct its manual request; the shared calculation will reject insufficient values when it executes. Keeping those two checks separate makes each responsibility visible.

The return annotation says Command because callers depend on that contract, even though the returned instance has a concrete type. Python does not enforce the annotation at runtime.

## 4B — Create now, execute afterward

Replace calculator/__main__.py:

<!-- reference: learn/04-factory:calculator/__main__.py -->
```python
from calculator.factory import CommandFactory
print(CommandFactory.create("csv").execute())
```

Run `python -m calculator`. Expect the same CSV sample result. The creation decision moved; the CSV loading and statistic did not.

```mermaid
sequenceDiagram
    participant C as Caller
    participant F as Factory
    participant R as Concrete request
    C->>F: create(name, inputs)
    F->>R: construct
    F-->>C: request object
    Note over C,R: Construction has finished; calculation has not run
    C->>R: execute()
    R-->>C: numeric result
```

If create() returned execute()'s numeric answer, callers could not retain an unexecuted request. “Factory creates; invoker executes” is a useful review sentence for this program.

## 4C — Test creation decisions

Create tests/test_factory.py:

<!-- reference: learn/04-factory:tests/test_factory.py -->
```python
import pytest
from calculator.commands import CsvStdDevCommand, ManualStdDevCommand
from calculator.factory import CommandFactory


def test_factory_creates_manual():
    assert isinstance(CommandFactory.create("manual", [1, 2]), ManualStdDevCommand)


def test_factory_creates_csv():
    assert isinstance(CommandFactory.create(" CSV "), CsvStdDevCommand)


@pytest.mark.parametrize("name,values", [("other", None), ("manual", None)])
def test_factory_rejects_invalid_request(name, values):
    with pytest.raises(ValueError):
        CommandFactory.create(name, values)
```

isinstance checks the selected kind of object. The normalization test uses a spaced uppercase name. Parametrization checks two rejected construction requests. Run `python -m pytest -q`; the reference now has eighteen cases.

## Independent exercise: construction must not execute

Write a test that temporarily replaces ManualStdDevCommand.execute with a function that raises AssertionError. Then call CommandFactory.create("manual", [2, 4, 6]). Creation should succeed and return the command without triggering the replacement.

Use monkeypatch.setattr as explained in [the testing guide](../testing-guide.md). The replacement accepts self because it stands in for an instance method. Keep the patch inside the test; pytest restores it.

<details>
<summary>Compare after you have tried</summary>

The test checks a boundary, not a numeric result. If it fails because execute() ran during create(), return the constructed object instead. The invoker is responsible for deciding when to run it.

</details>


## Say precisely which factory you mean

This is a Simple Factory: one helper selects and constructs concrete objects. It is not formal Factory Method, which introduces an overridable creation method in a creator hierarchy. Calling a static method create() is not evidence of that different pattern.

There is a cost: one more abstraction to read. There is a benefit: construction rules have one home and callers use the returned execution contract. New request types still require updating selection and tests.

## Change-planning exercise

Suppose a JSON request is added later. Do not implement it yet. List the changes: new request implementation, factory choice, CLI input preparation if needed, and tests. Explain why existing callers that merely execute a command do not need its parsing details.

**Checkpoint:** factory tests and earlier tests pass, construction does not execute, and your explanation names Simple Factory accurately. Commit the stage and record which responsibility moved out of the caller.

[Continue to Stage 5](05-repl.md)
