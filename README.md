# Part 4: Turn application actions into commands

[Course home](https://github.com/kaw393939/is218-command-factory-statistics) · [Branch navigation](docs/branches.md) · [Setup](docs/setup.md)

This branch contains the worked checkpoint for `learn/04-commands`. Its application
and tests are at the repository root. Start from your own completed
[OOP calculator](https://github.com/kaw393939/is218-oop-calculator) in a separate
solution repository; use this reference to examine and explain the change.

Add a session receiver, calculate/history/clear/help commands, and an interactive caller. Save results only after successful execution.

Read [this part's lesson](docs/lessons/04-commands.md) before comparing the complete
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

Try `add 2 3`, `divide 1 0`, `history`, `clear`, and `exit`. The failed division does not enter history. Saved successes remain available.

Parts 1–3 run small demonstrations. The interactive CLI begins in Part 4.
Parts 1–4 require pytest; Parts 5–6 add pandas. CI carries forward the testing
workflow from the prerequisite course.

## Explain and verify

[Request flow](docs/architecture.md) · [Testing requirements](docs/testing-guide.md)
· [Terms introduced so far](docs/glossary.md) · [Error handling](docs/error-handling.md)

Local lesson files cover Parts 1 through 4. Links to later parts open the
corresponding lesson branch. Broader reference readings live in the full textbook
on `main`; they do not add features to this checkpoint.

Compare this part with the previous one:

```bash
git fetch origin
git diff origin/learn/03-flexible-inputs..origin/learn/04-commands -- calculator tests requirements.txt
```

The changes are cumulative. Part 3 deliberately replaces the fixed-operand API;
read its migration explanation before combining examples from different parts.

When you can explain the checkpoint, continue to [Part 5](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/05-statistics-csv):

```bash
git status
git switch learn/05-statistics-csv
python -m pip install -r requirements.txt
python -m pytest -q
```
