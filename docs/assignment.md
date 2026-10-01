# Extend your completed calculator through six parts

Start from the [prerequisite OOP calculator](https://github.com/kaw393939/is218-oop-calculator) you already completed. Build one cumulative extension through all six lessons and retain regression evidence. This is a textbook assignment over study sessions; the separate practice and exam each have a 90-minute limit.

## Final teaching application behavior

| Request | Example result/action |
| --- | --- |
| `add 2 3` | `Result: 5.0000` |
| `subtract 2 3` | `Result: -1.0000` |
| `multiply 2 3` | `Result: 6.0000` |
| `divide 7 2` | `Result: 3.5000` |
| `square 3` | `Result: 9.0000` |
| `sqrt 9` | `Result: 3.0000` |
| `power 3 exponent=4` | `Result: 81.0000` |
| `sum 2 3 4` | `Result: 9.0000` |
| `mean 2 4 6` | `Result: 4.0000` |
| `stddev 10 20 30 40 50` | `Result: 15.8114` |
| `csv mean values.csv` | Read the `value` column and apply the same mean policy |
| `csv stddev values.csv` | Read the `value` column and apply the same deviation policy |
| `history` | List successful requests and saved results in order |
| `clear` | Remove session history; report `History cleared.` |
| `help` | Describe supported syntax |
| `exit` | Print `Goodbye!` and stop |

Binary arithmetic requires exactly two finite operands; square/sqrt/power require one. Power accepts a named `exponent` setting, default 2. Sum and mean need at least one observation. Standard deviation needs at least two for both supported settings: default `ddof=1`, or explicit `ddof=0` for population. Mathematical libraries may accept different counts; these minimums are this application's published rules.

Reject nonnumeric/nonfinite inputs, nonfinite results, invalid counts, unsupported/duplicate settings, and missing CSV observations. Negative real square roots fail during execution. Completely blank CSV lines follow pandas' default skipping; quoted empty cells are missing observations and fail validation. The small whitespace grammar does not support paths containing spaces.

Unknown requests, invalid syntax, zero division, and expected file/CSV failures report `Error:` and permit another request. EOF/Ctrl+C exit cleanly. Failed calculations never enter history. History is in memory for one session; persistence, undo, GUI, and individual removal are not requirements of this extension.

## Responsibilities to explain

`Operations` provides static math. `Calculation` stores operands and a callable, and invokes that callable in `get_result()`. `CalculationFactory` selects/configures a calculation without executing it. Part 3 generalizes its interface to `create(name, *values, **options)`.

`History` owns a private entry list and exposes `add`, `get_history`, and `clear`. The session computes first, then records `(calculation, result)`. Commands use the session's methods rather than editing internal history. Concrete actions implement the abstract `execute() -> str` contract; the CLI prints their text and handles interaction.

CSV reading supplies observations. Shared validation and statistical functions apply the same policy to typed/file values. In Part 6, execute a prepared sequence through the session, report expected failures, and permit later calculations to run. Do not put sequence orchestration inside mathematical operations.

## Completion evidence

Provide incremental commits, meaningful tests, CI, reproducible setup instructions, and a [learning log](learning-log.md). Explain:

- What changed from calculation subclasses to callable composition, and why inheritance remains useful for commands.
- Static versus instance methods; callable versus call; operands versus named settings; collection versus unpacking.
- Factory construction versus command execution, including one successful and one failed trace.
- Why history owns its collection, why a shallow copy has limits, and why saved results are not recalculated for display.
- Your EAFP/LBYL decisions and the sample/population policy.
- One independent adaptation and the components it affects.

Use tests to establish a claim rather than only listing a pass count. Retain earlier behavioral checks; adapt tests that explicitly depend on an intentionally changed API or terminal protocol, and explain that change. Run the final suite in a clean environment and inspect CI for the submitted revision.

The practice and real exam supply infrastructure and require different adaptations. Their exact APIs, behavior, and rubrics live in their own repositories. [Prepare for those assessments](practice-preparation.md).
