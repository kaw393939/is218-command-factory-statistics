# Learn what a test actually claims

A passing test supports a particular claim under its tested conditions. It does not prove every possible input works or establish that your design is sensible.

## Start with one known result

```python
assert standard_deviation([2, 4, 6]) == pytest.approx(2.0)
```

The claim is about the sample deviation of these values. pytest.approx allows small floating-point differences; it does not excuse a different mathematical policy. [Pytest approximate comparisons](https://docs.pytest.org/en/stable/reference/reference.html#pytest-approx)

## Check a promised failure

```python
with pytest.raises(ValueError):
    standard_deviation([2])
```

The block passes only if the promised error occurs. Printing an error while returning an incorrect value does not satisfy that function contract. The CLI later catches the exception and chooses how to display it.

## Use fixtures when a real dependency needs controlled setup

| Tool | Purpose | What our tests control |
| --- | --- | --- |
| tmp_path | A fresh temporary pathlib.Path for each test | A CSV independent of a user's file |
| monkeypatch.chdir(path) | Temporarily change working directory | Where a default values.csv is found |
| monkeypatch.setattr(...) | Temporarily replace a dependency | What input() returns |
| capsys | Capture printed output | Result and recovery messages |
| pytest.mark.parametrize | Repeat one test for multiple cases | Invalid values or termination signals |

Pytest supplies a fixture when you name it as a test argument and restores its changes afterward. You do not call tmp_path() or create monkeypatch yourself. Read [temporary paths](https://docs.pytest.org/en/stable/how-to/tmp_path.html), [monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html), and [capturing output](https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html) as each tool appears.

## Unpack a fake input stream

```python
answers = iter(["manual", "2 4 6", "exit"])

def fake_input(prompt):
    return next(answers)

monkeypatch.setattr("builtins.input", fake_input)
```

iter() produces an iterator; next() consumes one answer per call. The prompt parameter keeps the same calling shape as input(). A lambda in the reference is the shorter equivalent of this fake_input function. If the list runs out, next() raises StopIteration; that usually means your test supplied too few responses or your loop asked an unexpected question.

Keep the test focused: assert a successful result after invalid input, not only that an error printed. Recovery is a separate behavior.

## Diagnose a failure before editing code

1. Identify the first failing test and its input.
2. State the expected behavior from the requirement.
3. Compare expected and actual values or exceptions.
4. Decide whether the application or the assertion is wrong.
5. Run just that test, then run the full suite after the fix.

```bash
python -m pytest tests/test_statistics.py -q
python -m pytest -k constant -q
python -m pytest
```

Do not change an expectation merely to make the check green. Do not exclude failing application code from checks. This course uses meaningful behavior tests without a 100% coverage gate.
