# Part 1: Refactor the calculator you already built

[Course home](https://github.com/kaw393939/is218-command-factory-statistics) · [Branch navigation](docs/branches.md) · [Setup](docs/setup.md)

This branch contains the worked checkpoint for `learn/01-refactoring`. Its application
and tests are at the repository root. Start from your own completed
[OOP calculator](https://github.com/kaw393939/is218-oop-calculator) in a separate
solution repository; use this reference to examine and explain the change.

Separate stateless arithmetic from a calculation that stores two operands and a callable. Keep controlled History access and finite-number validation.

Read [this part's lesson](docs/lessons/01-refactoring.md) before comparing the complete
[calculation code](calculator). Predict the behavior, complete the guided change
in your own solution, test it, and explain the resulting flow.

## Run this checkpoint

Activate the reference environment described in [setup](docs/setup.md). Run
these commands from this branch's repository root:

```bash
python -m pip install -r requirements.txt
python -m calculator
python -m pytest -q
```

The demonstration prints `5.0`. `Calculation(2, 3, Operations.add)` stores two operands and a callable.

Parts 1–3 run small demonstrations. The interactive CLI begins in Part 4.
Parts 1–4 require pytest; Parts 5–6 add pandas. CI carries forward the testing
workflow from the prerequisite course.

## Explain and verify

[Request flow](docs/architecture.md) · [Testing requirements](docs/testing-guide.md)
· [Terms introduced so far](docs/glossary.md) · [Error handling](docs/error-handling.md)

Local lesson files cover Parts 1 through 1. Links to later parts open the
corresponding lesson branch. Broader reference readings live in the full textbook
on `main`; they do not add features to this checkpoint.

When you can explain the checkpoint, continue to [Part 2](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/02-factory):

```bash
git status
git switch learn/02-factory
python -m pip install -r requirements.txt
python -m pytest -q
```
