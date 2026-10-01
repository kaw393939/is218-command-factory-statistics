# Locate failure through Part 1

[Branch home](../README.md) · [Part 1 lesson](lessons/01-refactoring.md)

EAFP attempts an operation and handles expected failure. LBYL checks a precondition before attempting. Expect common success? Consider EAFP. Expect frequent rejection? Consider a cheap, reliable check. Failure frequency and correctness matter more than unpredictable ordering.

| Situation present here | Deliberate choice |
| --- | --- |
| Convert numeric text | Attempt float conversion; handle its expected failure |
| Reject NaN/infinity | Check the explicit finite-number contract |
| Divide by zero | Let arithmetic report ZeroDivisionError during execution |

## Follow the skipped work

A zero-divisor calculation can be created, then fail in get_result(). If that call fails, assignment of its successful result and later history recording are skipped. Catch failure where the caller can respond; do not add a try block to every layer.

Catch specific expected exceptions; a broad catch can hide programming defects. Checks and exception handling both consume processor work and memory. Neither a dictionary nor removing Python if statements establishes faster execution. Measure equivalent workloads if performance matters.

[Optional full discussion](https://github.com/kaw393939/is218-command-factory-statistics/blob/main/docs/error-handling.md) is enrichment after you can explain the relevant failure path.
