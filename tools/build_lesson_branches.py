"""Materialize the complete contents of six cumulative lesson branches.

This writes files to a separate directory. It never commits, updates Git refs,
pushes, or deletes branches. Publish reviewed trees in order, then verify them
with verify_course.py --full from main.
"""
import argparse
import os
from pathlib import Path
import re

from branch_notes import supporting_notes
from build_stages import ROOT, STAGES, stage_files

REPOSITORY = "https://github.com/kaw393939/is218-command-factory-statistics"
TITLES = (
    "Refactor the calculator you already built",
    "Create calculations with a factory",
    "One, two, and many operands",
    "Turn application actions into commands",
    "Statistics and another input source",
    "Integrate, explain, and adapt",
)
CHANGES = (
    "Separate stateless arithmetic from a calculation that stores two operands and a callable. Keep controlled History access and finite-number validation.",
    "Add a factory that selects an operation by name and constructs a calculation. Construction still does not execute arithmetic.",
    "Change the operand interface to a stored collection. Add unary and collection operations, *values gathering, argument unpacking, and **options forwarding.",
    "Add a session receiver, calculate/history/clear/help commands, and an interactive caller. Save results only after successful execution.",
    "Add pandas mean and standard deviation, then adapt a CSV observation source to the same calculation factory.",
    "Process prepared calculations independently, continue after failures, and use tests and traces to adapt the design to a changed requirement.",
)
DEMONSTRATIONS = (
    "The demonstration prints `5.0`. `Calculation(2, 3, Operations.add)` stores two operands and a callable.",
    "The demonstration prints `5.0`. `CalculationFactory.create(\"add\", 2, 3)` constructs the calculation; `get_result()` executes it.",
    "The demonstration prints `5.0` and `81.0`. `CalculationFactory.create(\"power\", 3, exponent=4)` shows a unary operation with a named setting.",
    "Try `add 2 3`, `divide 1 0`, `history`, `clear`, and `exit`. The failed division does not enter history. Saved successes remain available.",
    "Try `stddev 10 20 30 40 50` and `csv stddev values.csv`. Both print `Result: 15.8114`. The default deviation uses `ddof=1`.",
    "The interactive application still works. Read `calculator/sequence.py` and its test: a failed prepared calculation does not stop the next item or enter successful history.",
)


def branch_readme(index):
    stage = STAGES[index - 1]
    previous = STAGES[index - 2] if index > 1 else None
    next_stage = STAGES[index] if index < len(STAGES) else None
    compare = ""
    if previous:
        compare = f"""Compare this part with the previous one:

```bash
git fetch origin
git diff origin/learn/{previous}..origin/learn/{stage} -- calculator tests requirements.txt
```

The changes are cumulative. Part 3 deliberately replaces the fixed-operand API;
read its migration explanation before combining examples from different parts.

"""
    if next_stage:
        onward = f"""When you can explain the checkpoint, continue to [Part {index + 1}]({REPOSITORY}/tree/learn/{next_stage}):

```bash
git status
git switch learn/{next_stage}
python -m pip install -r requirements.txt
python -m pytest -q
```
"""
    else:
        onward = f"""Continue with [practice preparation]({REPOSITORY}/blob/main/docs/practice-preparation.md)
and the [practice repository](https://github.com/kaw393939/is218-statistics-practice).
The assessment asks you to adapt these responsibilities to different requirements.
"""
    return f"""# Part {index}: {TITLES[index - 1]}

[Course home]({REPOSITORY}) · [Branch navigation](docs/branches.md) · [Setup](docs/setup.md)

This branch contains the worked checkpoint for `learn/{stage}`. Its application
and tests are at the repository root. Start from your own completed
[OOP calculator](https://github.com/kaw393939/is218-oop-calculator) in a separate
solution repository; use this reference to examine and explain the change.

{CHANGES[index - 1]}

Read [this part's lesson](docs/lessons/{stage}.md) before comparing the complete
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

{DEMONSTRATIONS[index - 1]}

Parts 1–3 run small demonstrations. The interactive CLI begins in Part 4.
Parts 1–4 require pytest; Parts 5–6 add pandas. CI carries forward the testing
workflow from the prerequisite course.

## Explain and verify

[Request flow](docs/architecture.md) · [Testing requirements](docs/testing-guide.md)
· [Terms introduced so far](docs/glossary.md) · [Error handling](docs/error-handling.md)

Local lesson files cover Parts 1 through {index}. Links to later parts open the
corresponding lesson branch. Broader reference readings live in the full textbook
on `main`; they do not add features to this checkpoint.

{compare}{onward}"""


def rewrite_links(content, filename, available):
    """Keep local readings valid without copying future lessons into a branch."""
    directory = (ROOT / filename).parent

    def replace(match):
        target = match.group(2)
        if re.match(r"[a-zA-Z]+:", target) or target.startswith("#"):
            return match.group(0)
        path, separator, anchor = target.partition("#")
        relative = os.path.relpath((directory / path).resolve(), ROOT)
        lesson = Path(relative).stem
        if relative.startswith("docs/lessons/") and lesson in STAGES:
            new_target = f"{REPOSITORY}/blob/learn/{lesson}/{relative}"
        elif relative not in available:
            new_target = f"{REPOSITORY}/blob/main/{relative}"
        else:
            return match.group(0)
        return f"[{match.group(1)}]({new_target}{separator}{anchor})"

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace, content)


def lesson_tree(index):
    if not 1 <= index <= len(STAGES):
        raise ValueError("Choose a lesson number from 1 through 6.")
    files = stage_files(index)
    files[".gitignore"] = (ROOT / ".gitignore").read_text()
    files["README.md"] = branch_readme(index)
    files.update(supporting_notes(index))
    copied = ["docs/setup.md", "docs/branches.md"]
    copied += [f"docs/lessons/{stage}.md" for stage in STAGES[:index]]
    for path in copied:
        files[path] = (ROOT / path).read_text()
    available = set(files) | {str(Path(path).parent) for path in files}
    for path in copied:
        files[path] = rewrite_links(files[path], path, available)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="empty directory outside the teaching checkout")
    output = parser.parse_args().output_dir.resolve()
    if output == ROOT or ROOT in output.parents:
        parser.error("Write outside the teaching checkout.")
    if output.exists() and any(output.iterdir()):
        parser.error("Choose an empty output directory.")
    for index, stage in enumerate(STAGES, 1):
        for path, content in lesson_tree(index).items():
            target = output / stage / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
    print(f"Six complete lesson trees written to {output}. No Git refs changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
