# Follow the program through Part 6

[Branch home](../README.md) · [Part 6 lesson](lessons/06-transfer.md)

Read this alongside the current code. Label stored state, calls, returned values, and statements skipped after failure.

## Responsibilities present on this branch

| File | Responsibility |
| --- | --- |
| [operations.py](../calculator/operations.py) | Stateless arithmetic using explicit operands |
| [validation.py](../calculator/validation.py) | Convert values to finite floats or report failure |
| [calculation.py](../calculator/calculation.py) | Store operands and a callable; execute in get_result() |
| [history.py](../calculator/history.py) | Own successful calculation/result entries; return a shallow read copy |
| [__main__.py](../calculator/__main__.py) | Start the interactive application |
| [factory.py](../calculator/factory.py) | Select a callable by name and construct a calculation without executing it |
| [session.py](../calculator/session.py) | Execute first, then record success through History |
| [commands.py](../calculator/commands.py) | Represent calculate/history/clear/help actions; return display text |
| [cli.py](../calculator/cli.py) | Prepare actions, invoke execute(), print, and recover from expected errors |
| [statistics.py](../calculator/statistics.py) | Apply the observation/count/deviation policy using pandas |
| [inputs.py](../calculator/inputs.py) | Read the value column from CSV without performing math |
| [sequence.py](../calculator/sequence.py) | Execute already prepared calculations independently; collect results and errors |

## Trace one successful request

```python
from calculator.cli import prepare_command
from calculator.session import CalculatorSession

session = CalculatorSession()
command = prepare_command("power 3 exponent=4", session)
assert session.get_history() == []
assert command.execute() == "Result: 81.0000"
assert len(session.get_history()) == 1
```

Preparation separates the operation name, string operand, and named setting.
The factory returns a calculation holding `(3.0,)` and `{"exponent": 4.0}`.
`CalculateCommand` stores that calculation and the session; construction changes
no history. Its `execute()` delegates to `session.calculate()`, which calls
`get_result()` and records the returned `81.0` only after success. The command
formats a string; the interactive caller prints it.

## Trace one failed request

For `divide 1 0`, preparation succeeds. The command delegates to the
session, and division raises `ZeroDivisionError` inside `get_result()`. Control
leaves before `History.add()`, so no successful entry is recorded. The command
does not return result text. The interactive loop prints `Error:` and accepts
the next request. A failed conversion or unknown name happens earlier, during
preparation, and likewise records nothing.

## Read and change history deliberately

`History.add(calculation, result)` stores an entry. `get_history()` returns
a new list containing the same calculation objects and saved results. Clearing
that returned list cannot clear the owner's entries; `History.clear()` changes
the owned collection. The copy protects list membership, not every attribute
of the contained calculations. Save the result to avoid running math merely
to inspect an entry.

`HistoryCommand` reads through `session.get_history()` and formats saved
results. `ClearHistoryCommand` calls `session.clear()`. Those actions bypass
the calculation factory because they do not construct mathematical requests.
The CLI is the invoker; the session is the receiver. Commands return text and
do not prompt or print.

## Another source, the same calculation

`csv stddev values.csv` follows reader → DataFrame → value Series → list →
factory → calculation → calculate action → session → statistic → saved result.
The reader owns file structure; shared validation owns finite numeric inputs;
statistics owns minimum counts and `ddof`. Typed and CSV observations use the
same policy. Reading occurs during preparation, before calculation execution.
Sample deviation defaults to `ddof=1`; `ddof=0` explicitly requests population
deviation. Both require at least two observations here.

## A caller processing prepared requests

`execute_sequence(session, calculations)` receives calculation objects that
already exist. For addition, zero division, and square, it returns successful
results `[5.0, 9.0]` and one error message. History lengths progress from 0 to
1, remain 1 after the failure, then become 2. Recovery sits inside the loop so
later items run. Errors are returned separately; this helper does not add a
failure collection to the session or parse raw input rows.

An unknown operation can fail before a calculation exists. A caller accepting
raw requests must put factory construction inside its per-item error boundary
when the requirement is to continue after preparation failures too.
