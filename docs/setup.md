# Workspace setup

The teaching repository is a reference. Create your own solution repository or use the practice starter. The course home has no application or requirements file; the worked branches do. To run a worked example, clone this course and run `git switch learn/06-ci` before installing.


## Set up your workspace

Use Python 3.11–3.14. Fork the repository on GitHub, then clone **your fork** and change into its folder. Replace YOUR-USERNAME and REPOSITORY below.

```bash
git clone https://github.com/YOUR-USERNAME/REPOSITORY.git
cd REPOSITORY
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell use `py -m venv .venv` and `.venv\Scripts\Activate.ps1` instead. If activation is restricted, use `.venv\Scripts\python.exe -m pip install -r requirements.txt` and that interpreter for the commands below. On macOS/Linux you can likewise use `.venv/bin/python` without activation.

```bash
python -m calculator
python -m pytest
```

Run from the repository root: `csv` reads `values.csv` in the current working directory. Use `deactivate` when finished. Do not commit `.venv`.
