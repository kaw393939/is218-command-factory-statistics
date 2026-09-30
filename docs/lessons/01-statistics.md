# Stage 1: From two operands to a collection

[Start with the big picture](../big-picture.md) · [Worked branch](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/01-statistics) · [Course home](https://github.com/kaw393939/is218-command-factory-statistics)

[Next lesson](02-command.md)

## The problem you are solving

Your old operations accepted exactly two operands. A dataset can contain two values or two thousand. Before introducing patterns, give the calculation a contract that fits its input: a collection of numbers produces a numeric statistic, or raises a useful error.

**By the end:** you can explain the statistic, construct a pandas Series, validate values, and test a shared calculation function.

Complete [workspace setup](../setup.md) first. Keep your previous OOP calculator nearby for comparison, but build this application in your separate solution folder.

## Files in this stage

| File | Action | Reason |
| --- | --- | --- |
| calculator/statistics.py | Create | Shared validation and calculation |
| calculator/__main__.py | Create | Demonstrate the function through python -m calculator |
| tests/test_statistics.py | Create | Check the calculation contract |
| Supporting files from setup | Retain | Environment, package, pytest settings, and supplied CSV |

## 1A — Understand the answer before writing code

Standard deviation describes the spread of values around their mean. Equal values have no spread. For [2, 4, 6], the mean is 4. The deviations are -2, 0, 2; their squares are 4, 0, 4. The sum is 8. Sample variance divides by n-1, which is 2: 8/2 = 4. Taking the square root gives sample standard deviation 2.

Pandas uses the denominator n-ddof. This tutorial explicitly uses ddof=1 for the sample statistic. It does not ask you to implement the formula from scratch. Read the opening description and ddof parameter in [pandas Series.std](https://pandas.pydata.org/docs/reference/api/pandas.Series.std.html). The course installs pandas 2.x; the latest documentation may describe a newer release, so use the documented shared behavior and test it locally.

Predict: what is the deviation of [7, 7, 7]? Why does one observation fail our sample contract?

## 1B — Run the simplest valid calculation

Create calculator/statistics.py with this temporary first version:

```python
import pandas as pd


def standard_deviation(values) -> float:
    numbers = pd.Series(values, dtype=float)
    return float(numbers.std(ddof=1))
```

This version handles the happy path only. pd is the conventional alias for pandas. A Series is a one-dimensional container. dtype=float requests numeric values. std() calculates spread; float() gives callers a Python float. The return annotation documents that expectation without enforcing it at runtime.

Create calculator/__main__.py:

<!-- reference: learn/01-statistics:calculator/__main__.py -->
```python
from calculator.statistics import standard_deviation
print(standard_deviation([10, 20, 30, 40, 50]))
```

Run:

```bash
python -m calculator
```

Expected: approximately 15.811388300841896. The last printed digit can differ with floating-point arithmetic. `-m calculator` runs the package's __main__.py; it is not a filename passed to Python.

Now create a first test in tests/test_statistics.py:

```python
import pytest
from calculator.statistics import standard_deviation


def test_known_sample():
    assert standard_deviation([10, 20, 30, 40, 50]) == pytest.approx(15.811388300841896)
```

Run `python -m pytest -q`. Expect one passing test. You have evidence for one input, not complete validation.

## 1C — Make the contract explicit

Your CLI will eventually supply strings, and a CSV may contain missing or nonnumeric cells. Pandas' default missing-value behavior can hide a bad observation. Replace the temporary statistics.py with the complete version:

<!-- reference: learn/01-statistics:calculator/statistics.py -->
```python
"""One shared calculation policy, independent of terminal and file input."""
from math import isfinite
import pandas as pd


def standard_deviation(values) -> float:
    """Return sample standard deviation; require two or more finite numbers."""
    try:
        numbers = pd.to_numeric(pd.Series(list(values), dtype="object"), errors="raise")
    except (TypeError, ValueError) as error:
        raise ValueError("Values must be numeric.") from error
    if len(numbers) < 2:
        raise ValueError("Enter at least two values.")
    if not all(isfinite(float(value)) for value in numbers):
        raise ValueError("Values must be finite numbers.")
    # ddof=1 divides by n-1: this is the sample statistic.
    result = float(numbers.astype(float).std(ddof=1))
    if not isfinite(result):
        raise ValueError("Result is outside the supported range.")
    return result
```

Read it in four steps:

| Step | Expression | Why it belongs here |
| --- | --- | --- |
| Normalize/convert | Series(list(values), dtype="object"), then to_numeric | Accept a collection, including numeric strings; reject failed conversion |
| Check count | len(numbers) < 2 | Enforce the shared minimum |
| Check each value | all(isfinite(float(value)) for value in numbers) | Reject missing, infinite, and NaN values |
| Calculate/check result | std(ddof=1), then isfinite(result) | Apply the chosen statistic and reject unsupported numeric overflow |

list(values) materializes the incoming collection. dtype="object" temporarily retains mixed input types until conversion. errors="raise" requests an exception rather than silent coercion. The except block translates conversion failures into this function's ValueError contract; `raise ... from error` preserves the original cause for debugging.

The expression inside all() is a generator: check each number, then require every check to be true. The count check matters because all() over an empty collection is true. isfinite() rejects both infinity and NaN. astype(float) supplies a consistent floating-point Series for calculation.

Errors are raised here, not printed here. A future caller chooses whether to display an error, return an HTTP response, or handle it another way.

## 1D — Test valid results and rejected inputs

Replace the first test file with the cumulative reference tests:

<!-- reference: learn/01-statistics:tests/test_statistics.py -->
```python
import pytest
from calculator.statistics import standard_deviation


def test_known_sample():
    assert standard_deviation([10, 20, 30, 40, 50]) == pytest.approx(15.811388300841896)


def test_constant_values():
    assert standard_deviation([7, 7, 7]) == 0


@pytest.mark.parametrize("values", [[], [1], [1, "x"], [1, None], [1, float("inf")], [1, float("nan")]])
def test_reject_invalid_values(values):
    with pytest.raises(ValueError):
        standard_deviation(values)
```

pytest.raises expects an exception from its block. mark.parametrize runs the invalid-input test six times. Together with the two valid-result tests, the reference has eight cases. See [the testing guide](../testing-guide.md) if these tools are unfamiliar.

```bash
python -m pytest tests/test_statistics.py -q
python -m calculator
```

Expected: eight passing cases and the same numeric demonstration as before. Count is an orientation aid; additional meaningful exercise tests are welcome.

## Diagnose before changing code

| Symptom | Check |
| --- | --- |
| Result is approximately 14.1421 | Did you use ddof=0 instead of the required 1? |
| One observation returns NaN | Did you add the count check? |
| A missing observation disappears | Did you validate before std(), which skips missing values by default? |
| Numeric strings fail immediately | Did you retain the temporary float-only implementation rather than final conversion policy? |

## Independent exercise

Before running anything, predict the relationship between the deviations of [2, 4, 6], [12, 14, 16], and [4, 8, 12]. Add a test for each. Explain why adding a constant differs from multiplying every observation.

<details>
<summary>Compare after you have tried</summary>

The first two have sample deviation 2. Adding a constant moves the mean and each observation together, preserving deviations. The third has sample deviation 4 because multiplying every value by 2 doubles spread. Use approximate assertions, and keep the original tests.

</details>


## Explain your design

Why is this a function rather than a subclass of the earlier Calculation(a, b)? Why keep keyboard input and file reading out of it? Which parts are pandas usage, which are statistical policy, and which are application validation?

**Checkpoint:** the final tests pass, you can trace text-to-number conversion, and your learning log explains one corrected prediction. Commit your solution files with a descriptive Stage 1 message.

[Continue to Stage 2](02-command.md)
