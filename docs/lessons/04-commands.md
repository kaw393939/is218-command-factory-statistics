# Part 4: Turn application actions into commands

[Course home](../../README.md) · [Worked reference](../../examples/stages/04-commands/README.md) · [Concepts](../concepts.md)

[Previous part](03-flexible-inputs.md) · [Next part](05-statistics-csv.md)

## Refactor the actions in the familiar CLI

Your earlier calculator already accepts math requests, history, help, and exit. We will represent application actions as objects, while the calculation factory continues to construct mathematical calculations.

**Main new idea:** Command gives distinct actions a common execution contract. **Carry forward:** History encapsulation, polymorphism, ABC, REPL, and exception recovery. **Files:** add session.py and commands.py; adapt cli.py and its tests. The supplied parser is infrastructure for this part; understand its input/output boundary before studying every parsing detail.

## 4A — Give successful execution and recording a receiver

Earlier, the CLI called get_result and then History.add. Move those two statements together so another caller cannot accidentally record a failed calculation:

<!-- reference: examples/stages/04-commands/calculator/session.py -->
```python
"""Execute calculations and record successful results through History."""
from calculator.history import History


class CalculatorSession:
    def __init__(self):
        self._history = History()

    def calculate(self, calculation) -> float:
        result = calculation.get_result()
        self._history.add(calculation, result)
        return result

    def get_history(self):
        return self._history.get_history()

    def clear(self) -> None:
        self._history.clear()
```

A receiver performs work requested by an action. This session owns a History, executes calculations, and exposes controlled reading/clearing. Its get_history returns a copy through History; it does not expose a public mutable list.

Predict what happens if get_result raises: control leaves before add. Saved results make history display stable without recalculation. History remains a shallow copy of entries containing shared Calculation objects; it is not a deep immutable receipt system.

**Checkpoint:** test successful recording, failure leaving history unchanged, clearing, and independent sessions. Mutate the returned history list and check the internal history remains intact.

## 4B — Write concrete actions first

Start without inheritance:

```python
class CalculateCommand:
    def __init__(self, session, calculation):
        self.session = session
        self.calculation = calculation

    def execute(self):
        result = self.session.calculate(self.calculation)
        return f"Result: {result:.4f}"
```

```python
class ClearHistoryCommand:
    def __init__(self, session):
        self.session = session

    def execute(self):
        self.session.clear()
        return "History cleared."
```

These actions do different work. They share execute(), returning display text. Neither prompts or prints. Constructing CalculateCommand also does not perform math: it stores the receiver and calculation.

Run a small list of concrete commands:

```python
for command in commands:
    print(command.execute())
```

The caller needs only the shared capability. This is polymorphism through behavior before explicit abstract enforcement. Write HistoryCommand using saved entries and HelpCommand returning syntax text. Inspect their completed bodies in commands.py afterward.

## 4C — Reconnect abstract classes to the previous project

Your earlier abstract Calculation required get_result. Here an abstract Command requires execute:

```python
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self) -> str:
        """Perform an action and return display text."""
```

Add (Command) to the concrete class definitions. ABC and @abstractmethod prevent instantiation of subclasses missing the required implementation. They do not prove numerical correctness or enforce the hinted return type. Verify the mechanism with an incomplete subclass, then implement execute and try again.

| Contract | Purpose | Successful return |
| --- | --- | --- |
| Calculation.get_result | Mathematical request | float |
| Command.execute | Application action | str |

A factory does not become a Command because it creates objects. Here it constructs calculations; the CLI directly prepares action commands. The session is the receiver and the CLI is the invoker.

## 4D — Integrate with the CLI in small steps

First prepare one CalculateCommand without input. Then call the supplied prepare_command("add 2 3", session), examine the returned object, and invoke it. Add history/clear/help. Finally add the familiar loop and recovery boundary.

The revised single-line grammar makes operation, operands, and options visible:

```text
add 2 3
power 3 exponent=4
history
clear
exit
```

prepare_command splits text into positional values and key=value settings, then calls the factory and wraps the calculation. Duplicate option names fail before construction. This parser is supplied so learning Command does not require writing a new grammar simultaneously. Paths containing spaces are outside the deliberately small protocol.

Open the snapshot's cli.py once you can explain this boundary. Its run loop reads, prepares, invokes, prints, and repeats. It catches expected errors and ends cleanly on EOF/Ctrl+C. Exit is loop control, not a mathematical operation.

## 4E — Trace success and failure

For add 2 3, trace CLI → factory → Calculation construction → CalculateCommand construction → execute → session → get_result → Operations.add → saved result → display text → print.

For divide 1 0, mark where the exception originates, which statements are skipped, which except block handles it, and why the next prompt still appears. Revisit [EAFP/LBYL](../error-handling.md) at those boundaries, not as a claim about universal performance.

```bash
python -m pytest -q
python -m calculator
```

**Completion problem:** implement clear using only the receiver's public method. **Independent problem:** add a count action reporting the number of saved successful calculations. Include a failed calculation in its test and explain why count belongs to application actions rather than mathematical Operations.

Checkpoint: four actions work, controlled history is retained, tests establish recovery, and you can contrast a static operation, instance calculation, and abstract action contract. Commit.
