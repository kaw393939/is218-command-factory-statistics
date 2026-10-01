# Keep your work separate from the worked references

You have completed [the OOP calculator](https://github.com/kaw393939/is218-oop-calculator). Start with your own completed solution, not an empty project. Keep its submission commit available while you extend the design. The teaching repository contains worked answers and course-maintenance utilities; you do not need to recreate those utilities.

## Check the prerequisite checkpoint

From your own completed calculator's root, run its tests and a session with addition, subtraction, history, an invalid request, and exit. Explain the object and state changes before continuing. Revisit a prerequisite lesson if the behavior is unclear.

Commit any intended local work before starting a new learning branch:

```bash
git status
git switch -c calculator-extension
```

Use a new branch name if that one already exists. This branch is in your own solution repository; no instructor branch switching is needed. A separate copy of your completed solution is also reasonable if your instructor requires a new submission repository.

Use Python 3.11–3.14. Check `python3 --version` on macOS/Linux or `py --version` on Windows. Consult [Python's installation page](https://www.python.org/downloads/) if an interpreter is missing.

## Reuse or create a virtual environment

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Reuse your existing environment when appropriate. If activation is unavailable, run `.venv/bin/python` on macOS/Linux or `.venv\Scripts\python.exe` on Windows wherever these instructions say `python`. Reactivate the environment in a new terminal.

Keep the prerequisite's testing configuration and dependencies. Add the course's pandas dependency for Part 5; the reference dependency bounds are:

```text
pandas>=2.2,<3.0
pytest>=8.3,<9.0
```

These bounds describe the reference's dependencies, not a command to delete other tools your completed solution already needs. Install the resulting requirements with the same interpreter that runs your code:

```bash
python -m pip install -r requirements.txt
python -m pytest
```

Keep `.venv/`, `__pycache__/`, and `.pytest_cache/` out of Git. `python -m pip` avoids accidentally installing into another interpreter. Parts 1–4 need no pandas calculation; installing the declared final dependencies earlier is harmless.

## Obtain the complete examples separately

```bash
git clone https://github.com/kaw393939/is218-command-factory-statistics.git calculator-reference
cd calculator-reference
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cd examples/stages/01-refactoring
python -m calculator
python -m pytest -q
```

Use the Windows environment commands above when applicable. Run from a snapshot root so imports and fixture paths belong to that part. Parts 1–3 print a demonstration; Part 4 supplies the interactive application. Part 5 introduces `values.csv`.

Read a checkpoint's explanation before using the full snapshot to compare. Return to your own solution to make the change and retain your earlier tests. `main` in this teaching repository also contains the complete reference, so it is not an unfinished assessment starter.

Checkpoint: your prerequisite tests run, you can identify your solution and reference folders, and you can explain the initial request flow. See [navigation](branches.md), [migration](migration.md), and [troubleshooting](troubleshooting.md) before [Part 1](lessons/01-refactoring.md).
