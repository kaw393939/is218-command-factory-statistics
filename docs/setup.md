# Set up a workspace you can explain

There are two separate workflows. **Build your own solution** is the learning path. **Run a worked reference** is a quick way to inspect an example. The practice exam has its own forkable starter; use that after the tutorial.

## A. Build your own solution

Create an empty folder named statistics-solution using your editor or file manager. Open that folder in your editor and terminal. You will type the files from the lessons there, keeping one cumulative solution. Do not switch reference branches inside this folder.

Check your interpreter before installing anything:

```bash
python3 --version
```

Use Python 3.11–3.14. On Windows use `py --version`. If neither command exists, install Python using [the official downloads](https://www.python.org/downloads/) or your course setup instructions, then reopen your terminal.

### macOS / Linux

From inside statistics-solution:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip --version
```

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip --version
```

If PowerShell blocks activation, use `.venv\Scripts\python.exe` wherever a lesson says python; activation is a convenience, not a requirement. On macOS/Linux the equivalent direct interpreter is `.venv/bin/python`.

### Create the supporting files

Create these directories and files in your editor. No application code is needed yet.

```text
statistics-solution/
├── .gitignore
├── requirements.txt
├── pytest.ini
├── values.csv
├── calculator/
│   └── __init__.py
└── tests/
```

Type requirements.txt:

```text
pandas>=2.2,<3.0
pytest>=8.3,<9.0
```

Pandas is a runtime dependency; pytest is a development/testing dependency. The bounds keep this worked course on compatible major versions. Installing through `python -m pip` uses the pip associated with that Python interpreter.

Type pytest.ini:

```ini
[pytest]
pythonpath = .
testpaths = tests
addopts = -ra
```

This adds the repository root to pytest's import path, tells pytest where tests live, and requests a concise report of unsuccessful outcomes. It does not award marks or enforce a coverage percentage.

Type .gitignore:

```gitignore
.venv/
__pycache__/
.pytest_cache/
*.egg-info/
```

Create calculator/__init__.py with this docstring:

```python
"""My statistics calculator."""
```

Type values.csv, including its header:

```csv
value
10
20
30
40
50
```

Install and check the packages:

```bash
python -m pip install -r requirements.txt
python -c "import pandas, pytest; print('Packages ready')"
```

Expected final line: `Packages ready`. Do not run `python -m calculator` yet; Stage 1 creates its entry point. Before tests exist, pytest will report that it collected no tests, which is not a completed checkpoint.

Initialize Git once in this solution folder:

```bash
git init -b main
git add .gitignore requirements.txt pytest.ini values.csv calculator
git commit -m "Set up statistics learning workspace"
```

If this folder is already a Git repository, skip initialization. If Git asks for your name/email, configure the identity you use for course commits. Keep the virtual environment out of Git. Use `git status` before committing.

**Setup checkpoint:** packages import, the files above exist, and you know which folder contains your own work. [Begin Stage 1](lessons/01-statistics.md).

## B. Inspect a worked reference

Use a separate folder. These commands obtain the first stage of the instructor's reference:

```bash
git clone https://github.com/kaw393939/is218-command-factory-statistics.git statistics-reference
cd statistics-reference
git switch learn/01-statistics
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m calculator
python -m pytest
```

Use the Windows environment commands from above when applicable. Expect a number approximately 15.8113883 and eight passing tests. A fresh clone starts on main, which contains course readings rather than application code. Switch to the desired learn branch before installing or running the reference.

You can also read all lessons on GitHub without cloning. Return to your statistics-solution folder to type your implementation.

## Troubleshoot the environment

| Symptom | Inspect | Next step |
| --- | --- | --- |
| requirements.txt not found | Terminal's current folder | Change into the solution root or a worked reference branch |
| No module named pandas / pytest | Which interpreter installed packages? | Use the environment's Python to install and run |
| No module named calculator | Folder and file structure | Run from the project root; ensure calculator/ exists |
| calculator has no __main__ | Current checkpoint | Create Stage 1's __main__.py first |
| CSV file not found | Current working directory | Run from the folder containing values.csv |
| Command text appears inside a file | Which instructions were shell commands? | Keep terminal commands out of Python source |

Close the session with `deactivate` when finished. Reactivate the environment when you return. A new terminal does not automatically inherit the old terminal's activation.
