# Keep your solution separate from the worked branches

You have completed [the OOP calculator](https://github.com/kaw393939/is218-oop-calculator). Start your extension from your own completed solution. Keep its submission commit available. Use a separate clone of this teaching repository to inspect the instructor's six worked branches.

`main` contains the full textbook and canonical final code for course maintenance. Switch the reference to your current `learn/...` branch before running examples; this keeps the code and tests aligned with what you have learned.

## Check your prerequisite checkpoint

From your own completed calculator's root, run its tests and a session with addition, subtraction, history, an invalid request, and exit. Explain the object and state changes before continuing. Revisit a prerequisite lesson if the behavior is unclear.

Commit any intended local work before starting an extension branch in your own repository:

```bash
git status
git switch -c calculator-extension
```

Use another name if that branch already exists. Your solution can stay on this working branch as you implement all six parts. The reference clone is where you switch between instructor checkpoints. If your instructor requires a new submission repository, a separate copy of your completed solution is also reasonable.

Use Python 3.11–3.14. Check `python3 --version` on macOS/Linux or `py --version` on Windows. Consult [Python's installation page](https://www.python.org/downloads/) if an interpreter is missing.

## Prepare the reference clone

On macOS/Linux:

```bash
git clone https://github.com/kaw393939/is218-command-factory-statistics.git calculator-reference
cd calculator-reference
git switch learn/01-refactoring
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m calculator
python -m pytest -q
```

On Windows PowerShell, after cloning, entering the folder, and selecting the branch:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m calculator
python -m pytest -q
```

If activation is unavailable, use `.venv/bin/python` on macOS/Linux or `.venv\Scripts\python.exe` on Windows wherever these instructions say `python`. Reactivate the environment in each new terminal.

Run from the reference repository root. Part 1 prints `5.0`; Part 2 prints `5.0`; Part 3 prints `5.0` and `81.0`. Part 4 introduces the interactive application, and Part 5 introduces `values.csv` and pandas.

## Install what the selected part needs

| Parts | Reference dependencies |
| --- | --- |
| 1–4 | `pytest>=8.3,<9.0` for tests; application math uses the standard library |
| 5–6 | `pytest>=8.3,<9.0` plus `pandas>=2.2,<3.0` for statistics and CSV |

Install the selected branch's `requirements.txt` after switching, particularly when advancing to Part 5. `python -m pip` installs through the interpreter that runs the program. A previously installed pandas package can remain in your environment when inspecting an earlier part; those parts do not require it.

For your own solution, retain the prerequisite's useful testing configuration and dependencies. Add pandas when you reach Part 5 rather than deleting tools your existing tests need. Keep `.venv/`, `__pycache__/`, and `.pytest_cache/` out of Git.

## Move to the next checkpoint

In the reference clone:

```bash
git status
git fetch origin
git switch learn/02-factory
python -m pip install -r requirements.txt
python -m pytest -q
```

Save any intended experiments before switching. Read the matching branch's README and lesson, then return to your own solution to implement the change and retain earlier behavior tests. Each new branch builds on the previous one; [navigation](branches.md) explains comparisons and tracking branches.

Checkpoint: your prerequisite tests run, you can identify your solution and reference folders, and you can explain the initial request flow. See [migration](migration.md) and [troubleshooting](troubleshooting.md) before [Part 1](lessons/01-refactoring.md).
