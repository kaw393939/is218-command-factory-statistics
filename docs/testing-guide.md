# Retain behavior evidence through Part 1

[Branch home](../README.md) · [Part 1 lesson](lessons/01-refactoring.md)

You already know pytest and CI from the prerequisite. A changed public interface requires adapted calls, while its existing behavioral claims remain regression requirements.

## Read a test as a claim

Identify setup, action, and assertion. `pytest.approx` compares floating-point results; `pytest.raises` checks a specific failure. A spy records whether a collaborator was called and with which arguments. For deferred execution, assert no calls immediately after construction, then one call after `get_result()`.

| Required behavior | Supplied evidence |
| --- | --- |
| Static arithmetic works without constructing Operations | [tests/test_refactoring.py](../tests/test_refactoring.py): `test_math_without_an_instance` |
| Construction stores behavior without calling it | [tests/test_refactoring.py](../tests/test_refactoring.py): `test_construction_does_not_call_math` |
| Clearing a read copy preserves owned history | [tests/test_refactoring.py](../tests/test_refactoring.py): `test_history_copy_protects_membership` |
| A domain failure occurs during execution | [tests/test_refactoring.py](../tests/test_refactoring.py): `test_execution_reports_zero_division` |

## Preserve the earlier contracts

Keep arithmetic, finite input/result, deferred execution, and History ownership evidence when adding features. History reads must use `get_history()`. Clear the returned list, then read again to prove its membership was protected. Also check independent History owners and that an entry preserves its saved result without asking its calculation to execute again.

## Run from this branch's repository root

```bash
python -m pytest -q
```

Read a failed assertion before widening the checks. Fix its cause, run that focused test, then the accumulated suite. The retained GitHub Actions workflow runs this branch's tests on its revision; an old green run is not evidence for a new commit. Parts 1–4 require pytest; pandas joins the requirements in Part 5. Coverage shows executed code, not correctness or understanding.
