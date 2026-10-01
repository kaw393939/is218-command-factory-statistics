# Part 1: Refactor the calculator you already built

[Course home](../../README.md) · [Worked reference](../../examples/stages/01-refactoring/README.md) · [Concepts](../concepts.md)

[Next part](02-factory.md)

## Start from a completed project

You have already built Add and Subtract subclasses of an abstract Calculation, an encapsulated History, an interactive loop, tests, and CI. Open that solution beside this lesson. This sequel explores another arrangement of the same responsibilities; it does not replace your earlier work or imply inheritance was wrong.

Before reading further, trace Add(2, 3).get_result(). Identify the constructor, stored operands, method implementation, and returned value. Explain why editing a copied History list does not change its internal membership. If either explanation is difficult, revisit the earlier lesson before adding new mechanisms.

**Main new idea:** an object can store a function to choose its behavior. **Carry forward:** get_result(), finite numeric values, controlled history, and tests. **Files:** create operations.py and validation.py, revise calculation.py/history.py, and retain a demonstration entry point. Keep your earlier solution separately; work in a sequel folder so the two designs remain comparable.

## 1A — Separate math from the calculation object

In the earlier Add.get_result(), arithmetic uses self.a and self.b. Begin by moving only that arithmetic into a function:

```python
def add(a, b):
    return a + b
```

Call add(2, 3). Predict 5, then run it. No object state is required because the two arguments contain everything the operation needs.

Now group the operation under a class:

```python
class Operations:
    @staticmethod
    def add(a, b):
        return a + b
```

The decorator @staticmethod means Python does not insert an instance as an argument. Call Operations.add(2, 3) without constructing Operations. Contrast that with calculation.get_result(), which receives the calculation instance as self. Static describes the method binding; it does not mean faster, abstract, or automatically pure. A module function would also be valid; this course uses the class to group mathematical operations explicitly.

**Checkpoint:** add a direct assertion for Operations.add. Add subtract, then multiply and divide. Division reports ZeroDivisionError when its divisor is zero; recovery remains a caller's responsibility.

## 1B — A function reference is different from a result

```python
operation = Operations.add
result = operation(2, 3)
```

The first line stores behavior. The second line runs it. Parentheses are the visible difference. Predict what these variables contain before running: operation is callable; result is a number.

Temporarily keep the original Add class and delegate its method:

```python
class Add:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_result(self):
        return Operations.add(self.a, self.b)
```

This version shows delegation without changing object creation yet. Explain what moved and what stayed. Then consider why Add and Subtract need separate get_result implementations if the only difference is their selected arithmetic function.

## 1C — Store the selected operation

Write this small version first:

```python
class Calculation:
    def __init__(self, a, b, operation):
        self.a = a
        self.b = b
        self.operation = operation

    def get_result(self):
        return self.operation(self.a, self.b)
```

```python
calculation = Calculation(2, 3, Operations.add)
result = calculation.get_result()
```

Construction stores three pieces of state. It does not call the operation. get_result invokes the saved callable later. A second object can hold Operations.subtract without needing a new subclass.

| Earlier relationship | This relationship |
| --- | --- |
| Add is a Calculation subclass | Calculation has an operation callable |
| Overridden get_result selects arithmetic | Stored operation selects arithmetic |
| Caller asks get_result | Caller still asks get_result |

This is composition of behavior. The tradeoff is that a plain callable has no explicit abstract product-class relationship. Both approaches can be useful; explain the requirement motivating a choice.

## 1D — Keep the numeric and history contracts

The earlier CLI already converted text and rejected infinity/NaN. Extract that known policy so direct callers get it too. Read validation.py in the snapshot: an explicit loop attempts float conversion, checks isfinite, and returns a tuple. There is no generator expression to learn here. Errors are raised so a caller can choose its response.

The completed two-operand Calculation is:

<!-- reference: examples/stages/01-refactoring/calculator/calculation.py -->
```python
"""Store two operands and a callable; run math only in get_result."""
from math import isfinite
from calculator.validation import numeric_values


class Calculation:
    def __init__(self, a, b, operation):
        numbers = numeric_values([a, b])
        self.a = numbers[0]
        self.b = numbers[1]
        self.operation = operation

    def get_result(self):
        result = float(self.operation(self.a, self.b))
        if not isfinite(result):
            raise ValueError("Result is outside the supported range.")
        return result
```

The History boundary is preserved. Its entries now contain both the calculation and its successful result. Saving the result allows display without rerunning mathematics. get_history() returns a shallow list copy: callers cannot erase internal entries by clearing that copy, but the calculation objects are still shared.

Do not call get_result inside History.add. Execution and recording remain separate responsibilities. Part 4 will give that sequence a dedicated session receiver.

## Predict, test, and explain

Use a spy function that appends its received operands to a list. Assert the list is empty after constructing Calculation; call get_result and assert exactly one recorded call. This test establishes execution timing, not merely a numerical answer.

```bash
python -m pytest -q
python -m calculator
```

The worked snapshot prints 5.0. Retain arithmetic and history-copy tests. A zero-divisor calculation can be constructed, then fail during execution.

**Completion problem:** fill in get_result for a stored subtract callable before looking at the reference. **Independent problem:** add an operation that calculates the absolute difference of two values and compare the edits required by inheritance and composition. The exercise is about extension choices, not memorizing one formula.

**Self-check:** What does self refer to? Why is Operations static? What has happened immediately after construction? What has not happened? Why store a successful result with its calculation? Record one corrected prediction and commit this checkpoint.
