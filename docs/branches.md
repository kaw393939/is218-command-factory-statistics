# Navigate six cumulative references

The current course keeps six worked snapshots inside `examples/stages` in one checkout. No reference branch switching is required. Extend your own completed prerequisite solution separately; these folders contain finished examples.

| Part folder | Change from the preceding checkpoint |
| --- | --- |
| [01-refactoring](../examples/stages/01-refactoring/README.md) | Static math and a composed two-operand calculation; retain encapsulated history |
| [02-factory](../examples/stages/02-factory/README.md) | A name-to-operation calculation factory, still with two operands |
| [03-flexible-inputs](../examples/stages/03-flexible-inputs/README.md) | Unary/collection operations and positional/named argument forwarding |
| [04-commands](../examples/stages/04-commands/README.md) | Session actions and commands; reuse familiar abstraction and CLI concepts |
| [05-statistics-csv](../examples/stages/05-statistics-csv/README.md) | pandas statistics and a CSV observation source |
| [06-transfer](../examples/stages/06-transfer/README.md) | Prepared-sequence execution, transfer evidence, and CI review |

From the teaching repository root, inspect a reference:

```bash
cd examples/stages/02-factory
python -m calculator
python -m pytest -q
```

Use the already activated reference environment. Run tests from the snapshot root. Implement the lesson in your own solution, retaining earlier regressions; do not copy a whole snapshot over your project.

Parts contain smaller conceptual checkpoints even though there are only six main folders. The lesson explains what changed and why before linking the complete reference. Compare adjacent files and predict which existing behaviors should stay valid.

## Historical branches

The earlier `learn/01-statistics` through `learn/06-ci` branches in this repository describe the former statistics/command-factory curriculum. They remain historical references and do not match the revised APIs or assessments. The completed OOP calculator's own `learn/...` branches belong to that separate prerequisite course.

Use the current six snapshots and lesson names together. If an old link points to `01-operations`, `02-calculations`, `03-factory`, or `06-ci`, follow [the migration guide](migration.md) to the current progression. Do not combine old starter tests with a new contract.

Maintainers regenerate snapshots with `python tools/build_stages.py` and verify with `python tools/verify_course.py --full`. These utilities keep course references consistent; students demonstrate their own solution with application tests and CI.
