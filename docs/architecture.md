# Follow the program through Part 1

[Branch home](../README.md) · [Part 1 lesson](lessons/01-refactoring.md)

Read this alongside the current code. Label stored state, calls, returned values, and statements skipped after failure.

## Responsibilities present on this branch

| File | Responsibility |
| --- | --- |
| [operations.py](../calculator/operations.py) | Stateless arithmetic using explicit operands |
| [validation.py](../calculator/validation.py) | Convert values to finite floats or report failure |
| [calculation.py](../calculator/calculation.py) | Store operands and a callable; execute in get_result() |
| [history.py](../calculator/history.py) | Own successful calculation/result entries; return a shallow read copy |
| [__main__.py](../calculator/__main__.py) | Run this part's demonstration |

## Trace one successful request

```python
from calculator.calculation import Calculation
from calculator.operations import Operations

calculation = Calculation("2", "3", Operations.add)
result = calculation.get_result()
assert result == 5.0
```

Construction converts the two strings to `self.a == 2.0` and `self.b == 3.0`,
then stores `Operations.add` without calling it. `get_result()` calls that
function with the stored operands and returns a finite float. The demonstration
caller prints the number.

## Trace one failed request

`Calculation("1", "0", Operations.divide)` can be constructed: zero is a valid finite operand. When the caller asks for `get_result()`, division raises `ZeroDivisionError` and no result returns. Construction and execution are different failure boundaries.

A caller saving history must place `History.add(calculation, result)` after successful execution. `History.add()` does not run math itself.

## Read and change history deliberately

`History.add(calculation, result)` stores an entry. `get_history()` returns
a new list containing the same calculation objects and saved results. Clearing
that returned list cannot clear the owner's entries; `History.clear()` changes
the owned collection. The copy protects list membership, not every attribute
of the contained calculations. Save the result to avoid running math merely
to inspect an entry.
