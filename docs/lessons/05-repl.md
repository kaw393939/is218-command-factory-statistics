# Stage 5: Make the CLI an invoker

[Previous lesson](04-factory.md) · [Worked branch](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/05-repl) · [Course home](https://github.com/kaw393939/is218-command-factory-statistics)

[Next lesson](06-ci.md)

## Bring the user into the design

The commands and factory work without a terminal. Now add a caller that reads a request, collects source-specific inputs, obtains a command, executes it, and displays the answer. This CLI is the invoker.

**By the end:** you can trace both input routes, explain recovery and termination, and test an interactive session without typing during tests.

## Files in this stage

| File | Action |
| --- | --- |
| calculator/cli.py | Create interactive loop |
| calculator/__main__.py | Replace demo with reusable run() entry point |
| tests/test_cli.py | Add sessions, recovery, and termination tests |
| Existing requests/factory/statistic/tests | Retain |

## 5A — Trace a successful request before coding

Write the expected sequence for manual followed by 10 20 30 40 50:

1. input() returns the command text; normalize it.
2. Ask for values and split whitespace-separated tokens.
3. Factory creates a ManualStdDevCommand containing those tokens.
4. CLI calls execute(); shared policy converts and validates.
5. CLI formats the returned number to four decimal places.

For csv, skip the value prompt and use the default file request. For exit, end the loop; it is session control rather than a calculation request.

Review [the architecture trace](../architecture.md). Ask which component would change if the prompt wording changed. Then ask which would change if the statistic changed. They should be different components.

## 5B — Build the happy-path invoker

Start calculator/cli.py with this temporary version:

```python
from calculator.factory import CommandFactory


def run() -> None:
    while True:
        name = input("> ").strip().lower()
        if name == "exit":
            break
        values = None
        if name == "manual":
            values = input("Enter values separated by spaces: ").split()
        command = CommandFactory.create(name, values)
        result = command.execute()
        print(f"Standard deviation: {result:.4f}")
    print("Goodbye!")
```

Replace calculator/__main__.py with the final entry point:

<!-- reference: learn/05-repl:calculator/__main__.py -->
```python
from calculator.cli import run

if __name__ == "__main__":
    run()
```

The guard means run() is called when this module is executed as the entry point. Tests can import run from cli.py without automatically launching the session.

Run `python -m calculator` and try manual, a valid list, csv, exit. Both calculations should display 15.8114 using the supplied observations. Invalid input can still end this temporary version; do not treat that as the completed application.

## 5C — Make failure behavior part of the contract

Replace the temporary cli.py with this complete version:

<!-- reference: learn/05-repl:calculator/cli.py -->
```python
"""The invoker collects text, creates a request, and executes it."""
import pandas as pd
from calculator.factory import CommandFactory


def run() -> None:
    print("Statistics Calculator\nCommands: manual, csv, exit")
    while True:
        try:
            name = input("> ").strip().lower()
            if name == "exit":
                break
            values = None
            if name == "manual":
                values = input("Enter values separated by spaces: ").split()
            command = CommandFactory.create(name, values)
            result = command.execute()
            print(f"Standard deviation: {result:.4f}")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except (ValueError, OSError, pd.errors.ParserError, pd.errors.EmptyDataError) as error:
            print(f"Error: {error}")
    print("Goodbye!")
```

The try block includes command prompting, value prompting, construction, and execution. Expected input and file errors print Error: and return to the next iteration. EOF and Ctrl+C terminate cleanly. `break` exits the loop; the Goodbye! line runs afterward.

| Failure | Origin | CLI response |
| --- | --- | --- |
| Unknown name | Factory | Error, then next prompt |
| Invalid numeric token / too few values | Shared function | Error, then next prompt |
| Missing file / wrong column / parse error | CSV request or pandas | Error, then next prompt |
| End of input / Ctrl+C | Any input prompt | End session cleanly |

No blanket except Exception is needed. Catch expected failures; unexpected programming bugs should remain visible for debugging.

The CLI still branches to collect manual values. Patterns do not remove all conditionals. The factory owns concrete construction; the invoker owns user interaction and timing.

## 5D — Make a manual acceptance run

```text
Statistics Calculator
Commands: manual, csv, exit
> manual
Enter values separated by spaces: 10 20 30 40 50
Standard deviation: 15.8114
> csv
Standard deviation: 15.8114
> exit
Goodbye!
```

Also try an unknown command and a manual request containing a word. You should receive an error and remain able to calculate afterward. The exact exception text can differ by input; the prefix Error: and recovery behavior are stable requirements.

## 5E — Test sessions with controlled input

Create tests/test_cli.py:

<!-- reference: learn/05-repl:tests/test_cli.py -->
```python
import pytest
from calculator.cli import run


def test_interactive_session(monkeypatch, capsys, tmp_path):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "values.csv").write_text("value\n10\n20\n30\n40\n50\n")
    answers = iter(["manual", "10 20 30 40 50", "csv", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    run()
    output = capsys.readouterr().out
    assert output.count("Standard deviation: 15.8114") == 2
    assert "Goodbye!" in output


def test_recovers_after_invalid_input(monkeypatch, capsys):
    answers = iter(["unknown", "manual", "one two", "manual", "1 3", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    run()
    output = capsys.readouterr().out
    assert output.count("Error:") == 2
    assert "Standard deviation: 1.4142" in output


@pytest.mark.parametrize("error", [EOFError, KeyboardInterrupt])
def test_input_ends_cleanly(monkeypatch, capsys, error):
    def stop(prompt):
        raise error()
    monkeypatch.setattr("builtins.input", stop)
    run()
    assert "Goodbye!" in capsys.readouterr().out
```

Before typing, read [the testing guide](../testing-guide.md), especially fake input streams. The lambda is a one-line replacement function: it accepts the prompt and returns the next answer. capsys captures output. tmp_path supplies the file directory, and monkeypatch.chdir makes the default path resolve there. Pytest restores the patched function and working directory afterward.

The session test checks both routes. The recovery test checks a valid calculation after errors, which is stronger than merely checking an error message. The termination test raises each input-ending signal deliberately.

Run `python -m pytest -q`. Expect twenty-two cumulative cases in the reference.

## Independent exercise: recovery from a missing file

Write a test using a temporary directory with no values.csv. Feed csv, then manual with valid values, then exit. Assert that an error is shown, a later result is shown, and the session ends normally. Keep the file missing throughout this test; it should prove another request still works.

Optional second exercise: a factory-produced fake command returns 42. Test that the invoker calls its execute() method and prints 42.0000. This isolates invocation from the mathematical calculation.

## Debug an input mismatch

If a test raises StopIteration, trace each input() call against your supplied answers. Did you accidentally prompt for a filename? Did exit fail to break? Did a command prompt consume a numeric line? Write the sequence before adding more answers to hide the mismatch.

**Checkpoint:** successful sessions, invalid-input recovery, and termination work; earlier tests still pass; you can identify the CLI's invocation and client-setup roles. Commit and record one complete execution trace.

[Continue to Stage 6](06-ci.md)
