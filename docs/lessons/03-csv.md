# Stage 3: Give a CSV request the same contract

[Previous lesson](02-command.md) · [Worked branch](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/03-csv) · [Course home](https://github.com/kaw393939/is218-command-factory-statistics)

[Next lesson](04-factory.md)

## A second source should not create a second mathematical policy

A user has a CSV instead of a typed list. Its preparation differs: a file must be read and a column selected. The result contract stays the same. The caller should still be able to ask a request to execute.

**By the end:** you can explain DataFrame versus Series, when a file is read, how path-based requests work, and why both commands share one calculation function.

## Files in this stage

| File | Action |
| --- | --- |
| calculator/commands.py | Add CSV imports and CsvStdDevCommand |
| calculator/__main__.py | Demonstrate the CSV request |
| tests/test_csv.py | Add file-input checks |
| values.csv | Retain the supplied value header and dataset |
| Earlier files/tests | Keep |

## 3A — Inspect the data shape first

The supplied file contains:

```csv
value
10
20
30
40
50
```

The first line is a column header, not an observation. Pandas reads a table and selects the value column:

```python
import pandas as pd

frame = pd.read_csv("values.csv")
values = frame["value"]
print(type(frame).__name__)
print(type(values).__name__)
print(values.tolist())
```

Run this in a temporary experiment file from your solution root. Expected output:

```text
DataFrame
Series
[10, 20, 30, 40, 50]
```

A DataFrame holds the table; a Series holds one column. We select by its fixed name because the assignment does not ask users to choose columns. Read the filepath, header, and skip_blank_lines parameters in [pandas.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html).

## 3B — Package the file request

Update commands.py to this cumulative version; retain the earlier Command and ManualStdDevCommand:

<!-- reference: learn/03-csv:calculator/commands.py -->
```python
"""Command objects package requests behind one execute() contract."""
from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from calculator.statistics import standard_deviation


class Command(ABC):
    @abstractmethod
    def execute(self) -> float:
        """Return a numeric result or raise a useful input/file error."""


class ManualStdDevCommand(Command):
    def __init__(self, values):
        # Snapshot inputs so the request owns its values.
        self.values = list(values)

    def execute(self) -> float:
        return standard_deviation(self.values)


class CsvStdDevCommand(Command):
    def __init__(self, path="values.csv"):
        self.path = Path(path)

    def execute(self) -> float:
        frame = pd.read_csv(self.path)
        if "value" not in frame.columns:
            raise ValueError("CSV must contain a column named value.")
        # Do not silently drop missing values: both sources follow the same policy.
        return standard_deviation(frame["value"])
```

The new imports add pathlib.Path and pandas. Path represents a filesystem path, not file contents. The constructor stores a path. execute() reads the file, verifies the required column, and passes its values to the existing function.

The default path is values.csv relative to the current working directory. It is not automatically relative to commands.py. The optional path supports tests and programmatic callers; the eventual CLI uses the default without asking the user.

Missing files raise an OSError subclass. Bad columns raise our ValueError. Empty or malformed CSVs can raise pandas parsing errors. The future CLI will catch expected failures; the command should not swallow them and return a misleading number.

## 3C — Prove that the caller can use the same method

Replace calculator/__main__.py:

<!-- reference: learn/03-csv:calculator/__main__.py -->
```python
from calculator.commands import CsvStdDevCommand
print(CsvStdDevCommand().execute())
```

Run `python -m calculator` from your root. The expected number is again approximately 15.8113883.

Constructing CsvStdDevCommand() does not read the file. Execution does. Predict what happens if the file changes after construction but before execution. The command holds a path, not a frozen copy of the dataset.

## 3D — Give tests their own files

Create tests/test_csv.py:

<!-- reference: learn/03-csv:tests/test_csv.py -->
```python
import pytest
from calculator.commands import CsvStdDevCommand


def test_csv_matches_manual(tmp_path):
    path = tmp_path / "values.csv"
    path.write_text("value\n10\n20\n30\n40\n50\n")
    assert CsvStdDevCommand(path).execute() == pytest.approx(15.811388300841896)


def test_missing_column(tmp_path):
    path = tmp_path / "values.csv"
    path.write_text("wrong\n1\n2\n")
    with pytest.raises(ValueError, match="value"):
        CsvStdDevCommand(path).execute()


def test_missing_file(tmp_path):
    with pytest.raises(OSError):
        CsvStdDevCommand(tmp_path / "missing.csv").execute()
```

Pytest supplies tmp_path as a temporary directory unique to the test. The `/` operator joins paths. write_text() creates the test file; escaped `\n` characters make real newlines in its contents. These tests do not depend on your repository's CSV remaining unchanged.

The test named test_csv_matches_manual checks the same known dataset and expected answer used by manual tests. It does not call the manual command directly; the shared expectation connects the two paths. An independent exercise below compares them directly.

Run `python -m pytest -q`. The reference has fourteen cumulative cases.

## Missing lines versus missing observations

A completely blank physical line is skipped by read_csv's default settings. A quoted empty cell is parsed as missing data:

```csv
value
10
""
30
```

Our function rejects that missing value. It does not silently drop it to calculate a result from fewer observations. Explain this distinction before describing the application's validation policy.

## Independent exercise: the file changes

Create a test that constructs a CSV command for a temporary path, writes [2, 4, 6] to the file, executes it, changes the file to [7, 7, 7], and executes the same command again. Predict both answers. Then add a direct comparison between a manual command and CSV command for identical values.

<details>
<summary>Compare after you have tried</summary>

The results are 2 and 0. Each CSV execute() reads the path again. This differs from the manual command construction-time list snapshot. Both should match manual requests containing the same observations.

</details>


## Diagnose the right layer

| Symptom | Responsibility to inspect |
| --- | --- |
| File not found | Working directory and stored path |
| value column missing | Header and column validation |
| CSV result differs for the same values | Selected column, parsing, or duplicated calculation |
| Tests change your supplied CSV | Test isolation; use tmp_path |

**Checkpoint:** earlier tests pass, a file request has the same execute() contract, and you can describe when its data is loaded. Commit your changes and record the CSV-to-result trace.

[Continue to Stage 4](04-factory.md)
