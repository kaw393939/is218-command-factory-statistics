# Locate failure through Part 5

[Branch home](../README.md) · [Part 5 lesson](lessons/05-statistics-csv.md)

EAFP attempts an operation and handles expected failure. LBYL checks a precondition before attempting. Expect common success? Consider EAFP. Expect frequent rejection? Consider a cheap, reliable check. Failure frequency and correctness matter more than unpredictable ordering.

| Situation present here | Deliberate choice |
| --- | --- |
| Convert numeric text | Attempt float conversion; handle its expected failure |
| Reject NaN/infinity | Check the explicit finite-number contract |
| Divide by zero | Let arithmetic report ZeroDivisionError during execution |
| Select an operation | Catch KeyError only around the dictionary lookup; report an unknown name |
| Enforce operand count | Check the operation's published arity during creation |
| Restrict named settings | Validate supported names and finite numeric settings |
| Preserve successful history | Execute first; an exception skips the following add |
| Read a source | Attempt the read; expected file/parser failures reach the capable caller |
| Require a header/minimum count | Check the application's explicit structural/observation rule |

## Follow the skipped work

For divide 1 0, creation succeeds. During execution, the exception travels through the calculation, session, and action to the CLI. History.add and successful formatting are skipped. The CLI catches the expected error, reports it, and accepts another request.

Checking file existence cannot guarantee later access or valid contents. Attempt the read and handle the documented failures. Missing observations must not silently disappear before the statistic runs.

Catch specific expected exceptions; a broad catch can hide programming defects. Checks and exception handling both consume processor work and memory. Neither a dictionary nor removing Python if statements establishes faster execution. Measure equivalent workloads if performance matters.

[Optional full discussion](https://github.com/kaw393939/is218-command-factory-statistics/blob/main/docs/error-handling.md) is enrichment after you can explain the relevant failure path.
