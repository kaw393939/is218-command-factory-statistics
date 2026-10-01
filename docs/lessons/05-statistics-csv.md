# Part 5: Statistics and another input source

[Course home](../../README.md) · [Worked reference](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/05-statistics-csv/calculator) · [Concepts](../concepts.md)

[Previous part](04-commands.md) · [Next part](06-transfer.md)

## Add a source without changing the mathematical request

A sum already showed that an operation can accept several values. Now add mean and standard deviation using pandas, then supply those same observations from a CSV. Source selection and operation selection are different responsibilities.

**Main new idea:** data-source adaptation into a shared calculation policy. **Carry forward:** flexible arguments, factory construction, commands, numeric validation, and recovery. **Files:** add statistics.py, inputs.py, values.csv and tests; extend Operations/factory/CLI/help. Learn the pandas collection in a small demonstration before integrating it with the application.

## 5A — Understand the policy before the API

For 2, 4, 6 the mean is 4. Deviations are -2, 0, 2; squared deviations total 8. Sample variance divides by n-1=2, giving 4; its square root is 2. Population variance divides by n=3, giving a deviation approximately 1.6330.

Pandas uses denominator n-ddof. Our default ddof=1 selects sample deviation; the optional setting ddof=0 selects population. This application's deviation contract requires at least two observations for either setting. Mean requires at least one. These are explicit application requirements, not assumptions supplied by pandas.

Predict the result for three identical values, and whether a single observation meets each contract.

## 5B — Use a Series directly

```python
import pandas as pd

numbers = pd.Series([2, 4, 6], dtype=float)
result = float(numbers.std(ddof=1))
```

A Series is a one-dimensional collection. dtype=float specifies numeric representation. std computes spread. The outer float gives the caller a Python float. Type hints do not perform this conversion.

Add mean and standard_deviation shared functions using the existing numeric_values converter. Validate before aggregation: pandas' default missing-value handling could otherwise discard an observation silently. Reject unsupported ddof, too few observations, missing/nonfinite inputs, and nonfinite results. Inspect statistics.py on this lesson branch after implementing a happy path and then one failure rule at a time.

Operations.mean/stddev delegate to those functions. Register their callables in the same calculation factory. stddev accepts ddof as a keyword-only setting. These are extensions of Part 3's mechanisms, not a new command hierarchy.

## 5C — A DataFrame supplies observations

Create values.csv:

```csv
value
10
20
30
40
50
```

```python
import pandas as pd

frame = pd.read_csv("values.csv")
values = frame["value"].tolist()
```

read_csv returns a DataFrame, a table. Selecting the value column produces a Series. tolist gives ordinary observations to the same factory used by typed inputs. Read first, construct second, execute later.

The reader's complete boundary is:

<!-- reference: learn/05-statistics-csv/calculator/inputs.py -->
```python
"""Read a CSV input source; choosing and performing math belong elsewhere."""
from pathlib import Path
import pandas as pd


def read_csv_values(path):
    frame = pd.read_csv(Path(path))
    if "value" not in frame.columns:
        raise ValueError("CSV must contain a column named value.")
    return frame["value"].tolist()
```

A missing/headerless/empty/malformed file fails during reading or structural checking. A quoted empty cell is a missing observation and fails numeric validation. Completely blank lines follow pandas' default skipping. Do not drop bad values to obtain an answer.

The CLI accepts csv mean/stddev PATH and optional stddev ddof. It reads observations during preparation and constructs an ordinary CalculateCommand. A file is not an operation.

## 5D — Compare sources and failures

```text
> stddev 10 20 30 40 50
Result: 15.8114
> csv stddev values.csv
Result: 15.8114
> mean 10 20 30 40 50
Result: 30.0000
> stddev 2 4 6 ddof=0
Result: 1.6330
```

Test equality between sources using another dataset too. Use tmp_path instead of rewriting the supplied file. Test structure, missing observations, numeric policy, and a failed file request followed by successful manual input.

Use EAFP for float conversion and file access: the operation already reports meaningful failures. Use explicit checks for the application's minimum count and header contract. Checking existence before reading cannot guarantee a later read will succeed. Correctness and clear error ownership matter before performance; optional benchmarking is in the appendix.

**Completion problem:** fill in the reader's delegation to the shared factory path. **Independent problem:** select a different documented CSV column while preserving the same numeric policy. Supply tests for the new header and a missing header. Explain which components should remain independent of file structure.

```bash
python -m pytest -q
python -m calculator
```

Checkpoint: draw DataFrame → Series → list → numeric tuple → stored operation → result. Explain why numeric math, file reading, construction, and display have separate homes. Commit.
