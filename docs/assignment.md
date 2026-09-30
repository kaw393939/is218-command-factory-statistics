# Assignment and completion criteria

## Your task

Recreate the six worked stages in your own project and explain each change. Retain earlier tests and commit each checkpoint.

## Required final behavior

| Request | Acceptance criterion |
| --- | --- |
| manual | Accept whitespace-separated values and show sample standard deviation |
| csv | Read values.csv with pandas, using only its value column |
| exit | End the session cleanly |

Both sources use the same standard_deviation(values) function and require at least two finite numeric values. Reject blank or nonnumeric cells, NaN, infinity, insufficient values, and nonfinite results. Show four decimal places in the CLI. Expected input and file errors must not crash the session. No filename/column selection, history, removal, extra arithmetic, Facade, GUI, or undo is required.

## Architecture

Command is abstract and exposes execute() -> float. ManualStdDevCommand and CsvStdDevCommand implement it. CommandFactory.create(name, values=None) returns a command without executing it. The CLI delegates creation to that factory and invokes execute(). This is a Simple Factory, not formal Factory Method.

## Evidence

Supply application code, requirements.txt, meaningful tests, pytest configuration, a passing GitHub Actions workflow, and a README covering setup and responsibilities. Explain why the collection interface differs from the old two-operand calculator. Tutorial completion has no 100% coverage gate.

## Timed practice

The practice exam is 90 minutes and starts from supplied skeletons. Its grading script awards 100 automated feedback points. The exam changes a small bounded requirement; the practice is not an exact copy. Instructor review confirms the pattern responsibilities. Automated feedback alone is not proof of design understanding.
