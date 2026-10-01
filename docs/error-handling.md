# Locate failure before choosing how to handle it

You already used conversion checks and exception recovery in the OOP calculator. This course makes the policy explicit and traces failures across more components. Ask where an error originates, which state must remain unchanged, and which caller can respond usefully.

## EAFP and LBYL describe timing

EAFP means Easier to Ask Forgiveness than Permission: attempt an operation, then handle an expected exception. LBYL means Look Before You Leap: check a precondition before attempting. [Python defines both styles](https://docs.python.org/3/glossary.html#term-EAFP).

```python
# LBYL: check before division.
if b == 0:
    raise ValueError("Cannot divide by zero.")
result = a / b
```

```python
# EAFP: attempt division and translate its expected failure.
try:
    result = a / b
except ZeroDivisionError:
    raise ValueError("Cannot divide by zero.") from None
```

Our static divide operation simply returns `a / b`. Python already detects zero division, so the operation lets `ZeroDivisionError` propagate to a caller capable of recovery. Every layer need not add another `try` block. Raising reports the problem; catching responds to it.

Use this heuristic: **expect success, attempt the operation and handle expected failure; expect frequent rejection, consider a cheap and reliable check first.** Failure frequency matters more than whether inputs arrive in a predictable order. Correctness and clarity come first; measure if performance matters.

## Match the style to the rule

| Situation | Useful approach | Reason |
| --- | --- | --- |
| Convert numeric text | EAFP with `float()` | Conversion already understands its accepted grammar |
| Select a known operation | Narrow lookup `try`/`except KeyError` | A missing key identifies an unknown choice |
| Require one/two operands | LBYL count check | The required count is an application contract |
| Restrict named settings | Explicit validation | An unsupported setting should have a clear creation error |
| Read a file | Attempt the read and handle expected file/parser failure | Existence does not guarantee access or a later successful read |
| Preserve successful history | Execute before adding | An exception skips the state change |

An existence check can become outdated before the read. It also does not guarantee permissions or valid file content. Do not duplicate all possible read failures with checks.

Keep `try` blocks small and catch specific exceptions. Translate only the registry lookup's `KeyError`; do not place construction and execution in that same handler and mislabel their bugs as unknown names. `raise ... from error` preserves a causal exception; `from None` suppresses the displayed cause when the translated message is sufficient. Introduce that presentation choice after the basic propagation is understood.

Catching `Exception` around the whole application can hide a misspelled attribute or another programming bug. Expected input errors should permit recovery; an unexpected defect needs a useful traceback.

## Trace the state and skipped statements

For `divide 1 0`, factory creation succeeds. Command execution delegates to session calculation. Division raises; `get_result()` does not return; the session does not call `History.add()`; the command does not return successful display text. The CLI prints an error and accepts another line.

For unknown names, failure occurs during selection. For invalid numeric text, conversion fails during preparation/construction. For malformed CSV, reading fails before a calculation is prepared. These different origins can share a user-facing recovery boundary without being the same failure.

In Part 6, a prepared sequence needs a recovery boundary around each execution if later items should continue. Moving the handler around the whole loop would stop the sequence after the first failure. Trace valid, invalid, valid items and inspect history after each one.

Exercise: compare `text.isdigit()` with `float(text)` for `-2`, `3.5`, and `1e3`. Explain why a digit-only check is not equivalent validation for this application's numeric grammar.

## Optional performance discussion

LBYL is not exclusively a processor cost, and EAFP is not exclusively a memory cost. Checks take work; raising and handling exceptions takes work and can allocate exception/traceback objects. Which approach is faster depends on the operation, implementation, and failure frequency.

A Python `if` does not correspond one-to-one to a hardware branch. Dictionary lookup and exception machinery can branch internally too. Predictable branches can be inexpensive, and removing a branch can introduce other work. [Intel's optimization manual](https://cdrdv2-public.intel.com/821612/248966-Optimization-Reference-Manual-V1-050.pdf) discusses those tradeoffs. Registry selection is taught for organization, without a speed guarantee.

```bash
python tools/benchmark_errors.py
```

This optional experiment compares integer-string conversion at valid-input rates of 100%, 99%, 50%, and 0%. Its deliberately restricted unsigned ASCII grammar makes both implementations accept the same inputs; the LBYL scan duplicates some conversion work. Read the workload before interpreting timing. The experiment does not measure hardware mispredictions or establish a rule for all Python programs. See [timeit](https://docs.python.org/3/library/timeit.html).

Benchmarking is enrichment rather than an assessment requirement. First establish equivalent behavior and correct error handling.
