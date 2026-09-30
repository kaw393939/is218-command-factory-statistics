# Stage 2: Turn a request into a Command

[Previous lesson](01-statistics.md) · [Worked branch](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/02-command) · [Course home](https://github.com/kaw393939/is218-command-factory-statistics)

[Next lesson](03-csv.md)

## A new need: describe work now, run it later

The function from Stage 1 is useful directly. Suppose a caller needs to hold several requests and run them through the same interface. A function result records an answer; a request object can retain what should happen and the inputs it needs.

This is where Command becomes useful in our teaching example. We will not add a real background queue or undo system. We will demonstrate the underlying separation of request construction and execution.

**By the end:** you can identify stored request state, the execution contract, and the caller deciding when to execute.

## Guided reading

Read [Refactoring.Guru: Command](https://refactoring.guru/design-patterns/command), specifically Intent, Problem, Solution, and Structure. Do not implement its entire editor example.

Write answers before coding:

1. What information must a request retain?
2. Why does a common execution interface help different callers?
3. Which general roles will our small application combine or simplify?

Compare your answers with the mapping in [our architecture guide](../architecture.md). Our statistical function performs the receiver's work; no separate receiver class is required for this exercise.

## Files in this stage

| File | Action |
| --- | --- |
| calculator/commands.py | Create the contract and manual request |
| calculator/__main__.py | Replace the function demonstration with a Command demonstration |
| tests/test_commands.py | Create request/contract tests |
| Stage 1 application and tests | Keep |

## 2A — Compare a result with a request

These fragments illustrate the difference; they are not extra required files:

```python
result = standard_deviation([10, 20, 30, 40, 50])
```

The function runs immediately. result is a number.

```python
command = ManualStdDevCommand([10, 20, 30, 40, 50])
# Other work can happen here.
result = command.execute()
```

Construction saves the inputs. The calculation happens when execute() delegates to the function. Merely changing the method name from get_result() to execute() would not explain this relationship.

## 2B — Build the contract and one concrete request

Create calculator/commands.py:

<!-- reference: learn/02-command:calculator/commands.py -->
```python
"""Command objects package requests behind one execute() contract."""
from abc import ABC, abstractmethod
from calculator.statistics import standard_deviation


class Command(ABC):
    @abstractmethod
    def execute(self) -> float:
        """Return a numeric result or raise a useful input/file error."""


class ManualStdDevCommand(Command):
    def __init__(self, values):
        # Snapshot inputs so the request owns its values.
        self.values = list(values)

    def execute(self) -> float:
        return standard_deviation(self.values)
```

| Syntax | Meaning |
| --- | --- |
| Command(ABC) | Abstract base defining required behavior |
| @abstractmethod | Subclasses must supply execute() before they can be instantiated |
| ManualStdDevCommand(Command) | Concrete command shares that contract |
| self.values | State belonging to this request object |
| list(values) | Snapshot the incoming sequence |
| return standard_deviation(self.values) | Delegate the mathematical policy |

The docstring is a valid abstract method body. ABC prevents constructing an incomplete implementation; it cannot guarantee that a subclass returns the promised number. Read [Python's ABC documentation](https://docs.python.org/3/library/abc.html) if decorators and abstract classes are new.

The list is copied, but remains mutable through self.values. This design protects against changes to the caller's original list; it is not a fully immutable request.

## 2C — Change the caller, not the statistic

Replace calculator/__main__.py:

<!-- reference: learn/02-command:calculator/__main__.py -->
```python
from calculator.commands import ManualStdDevCommand
print(ManualStdDevCommand([10, 20, 30, 40, 50]).execute())
```

Run `python -m calculator`. Expect the same sample answer, approximately 15.8113883. The output did not change; the organization of the request did.

Trace the lines: constructor → saved values → execute() → shared function → returned float. No input() belongs inside the command; the caller already supplies its values.

## 2D — Test the relationship

Create tests/test_commands.py:

<!-- reference: learn/02-command:tests/test_commands.py -->
```python
import pytest
from calculator.commands import Command, ManualStdDevCommand


def test_contract_is_abstract():
    with pytest.raises(TypeError):
        Command()


def test_manual_request():
    command = ManualStdDevCommand([10, 20, 30, 40, 50])
    assert isinstance(command, Command)
    assert command.execute() == pytest.approx(15.811388300841896)


def test_request_snapshots_values():
    values = [1, 3]
    command = ManualStdDevCommand(values)
    values.clear()
    assert command.execute() == pytest.approx(2 ** .5)
```

The first test checks the abstract interface. The second checks the concrete result and subtype relationship. The third clears the caller's list after construction; the command must still retain its snapshot. `2 ** .5` is the square root of 2, the sample deviation of [1, 3].

Run `python -m pytest -q`. Expect eleven cumulative cases in the unextended reference. The eight earlier checks still matter because Command delegates to that function.

## Independent exercise: a list of requests

In a temporary experiment file in your solution, construct commands for [2, 4, 6] and [7, 7, 7]. Store the command objects in a list. Only then loop through the list and execute each. Predict results 2 and 0 before running.

Next, intentionally put a numeric result in the list instead of a command. Explain why the caller can no longer rely on execute(). Undo that experiment after recording what you learned; do not add broken data to the application.

<details>
<summary>Compare after you have tried</summary>

A uniform caller depends on the execution contract. A float has no execute() method. The useful distinction is request versus result, not simply class versus function.

</details>


## Common mistakes

| Mistake | Consequence |
| --- | --- |
| Calculate inside __init__ instead of storing inputs | Execution timing no longer matches our contract |
| Forget return in execute() | Caller receives None instead of a numeric result |
| Put input() in execute() | Tests and other callers depend on a terminal |
| Duplicate pandas calculation in the command | Mathematical policy can drift between requests |

## Explain the tradeoff

For one immediate calculation, calling the function is simpler. Request objects add value when a caller needs to store, pass, or invoke different requests uniformly. Be able to explain why we introduce this layer and what extra complexity it costs.

**Checkpoint:** tests pass, the statistical function is unchanged, and you can distinguish construction from execution. Commit and record the request's state and caller in your learning log.

[Continue to Stage 3](03-csv.md)
