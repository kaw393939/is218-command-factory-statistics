# Retain behavior evidence while changing the design

The prerequisite already introduced pytest, fixtures, meaningful assertions, coverage, and CI. Use them throughout this course. When a public interface intentionally changes, adapt the relevant test and retain the behavior it was checking.

A test has setup, an action, and an assertion. State the claim in its name, then use values that would distinguish the intended behavior from a plausible bug.

```python
import pytest
from calculator.operations import Operations


def test_divide_returns_fraction():
    result = Operations.divide(7, 2)
    assert result == pytest.approx(3.5)


def test_divide_rejects_zero():
    with pytest.raises(ZeroDivisionError):
        Operations.divide(7, 0)
```

`pytest.approx` handles floating-point differences. `pytest.raises` fails if the expected exception is absent or a different type is raised. First explain one case; then use parametrization when several cases test the same behavior. More rows alone do not establish a stronger claim.

## Match each part to a behavioral claim

| Part/component | Evidence that distinguishes correct behavior |
| --- | --- |
| 1: static operations | Math works without an `Operations` instance or terminal input |
| 1: composed calculation | Constructor stores a callable; an operation spy has not been called yet |
| 1–4: history | Different owners have independent entries; clearing a returned read list cannot clear owned state |
| 2: factory | Name selects the intended operation and returns a calculation without executing it |
| 3: flexible inputs | Unary/binary counts differ; values and named settings are forwarded correctly |
| 3: snapshots | Caller mutation of the original list/options does not alter stored inputs |
| 4: session/actions | Success records a saved result; failure records nothing; display does not recalculate |
| 5: statistics | Known sample/population results and count/missing/nonfinite policies |
| 5: CSV | Valid observations reach shared math; structural/numeric failures remain visible |
| 4–6: recovery | A failed request/item followed by a valid one still permits the valid result |

A spy is a small callable recording its calls. It tests timing or delegation through observable behavior, rather than matching source formatting. For deferred execution, assert no calls immediately after construction, then assert one call and its arguments after `get_result()`.

A history test should read through `get_history()`, not `_entries` or `_history`. If the test clears the returned list, then another read should still contain the saved entry. This proves collection protection; it does not prove contained objects are deeply immutable.

## Reuse your familiar test resources

`tmp_path` supplies a temporary location for a CSV. `monkeypatch` temporarily replaces a collaborator or changes environment state. `capsys` captures printed output. Use a named fake input before compressing it into a lambda:

```python
from calculator.cli import run


def test_terminal_recovers_after_division_failure(monkeypatch, capsys):
    answers = iter(["divide 1 0", "add 2 3", "exit"])

    def fake_input(prompt):
        return next(answers)

    monkeypatch.setattr("builtins.input", fake_input)
    run()
    output = capsys.readouterr().out
    assert "Error:" in output
    assert "Result: 5.0000" in output
    assert "Goodbye!" in output
```

Each call to `input()` consumes an answer. Exhausting the fake unexpectedly raises `StopIteration`, generally exposing a mismatch with the interaction protocol. Do not hide it as an expected user error.

For CSV, create the file inside `tmp_path` rather than modifying the supplied example. Test a different dataset from the README's demonstration. Compare typed and CSV results under the same option, and include one missing observation that must not be silently discarded.

## Select tests that detect likely errors

| Plausible mistake | Discriminating case |
| --- | --- |
| Subtraction implemented as addition | Unequal nonzero operands with a negative expected difference |
| Factory executes during construction | A spy, or construct division by zero without yet asking for a result |
| Options stored but not forwarded | Power with a nondefault exponent |
| Every operation treated as binary | Successful square root plus an extra-operand rejection |
| Session records before execution | Fail division and inspect empty successful history |
| History recomputes results | A callable whose next call would fail; display must use the saved result |
| Population/sample policy mixed | `[2, 4, 6]` produces distinct deviations |
| Sequence stops after one failure | Valid, invalid, valid prepared calculations, with two successful results |

In Part 6, tests for a prepared sequence should establish both continued execution and successful-only history. Tests for an assessment adaptation should target the new contract rather than repeating an unchanged course test.

## Diagnose before broadening checks

Read the failed assertion and its inputs. Determine whether the expectation or implementation disagrees with the published contract. Fix that cause, rerun the focused test, then run the accumulated suite.

```bash
python -m pytest tests/test_operations.py -q
python -m pytest -q
```

Coverage measures which lines/branches ran, not whether the assertions explain correctness. The teaching extension does not add a new exact coverage requirement; retain the prerequisite's setup when useful. Assessments have their own published rubric and do not award student-test credit solely for test count or coverage percentage.

Course maintainers also run `python tools/verify_course.py --full` to check documentation and snapshots. Students need not implement that utility. A green CI run verifies its checked revision; inspect the run corresponding to your submitted commit.

[pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) · [monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html) · [approx](https://docs.pytest.org/en/stable/reference/reference.html#pytest-approx)
