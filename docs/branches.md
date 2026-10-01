# Follow six cumulative learning branches

`main` is the course entry point and full textbook. The worked programs live on six ordered `learn/...` branches. Each has its own README, stage-relevant lesson material, application code, and tests at the repository root. Extend your completed prerequisite solution in a separate project while using these branches as references.

| Branch | Change from the preceding checkpoint |
| --- | --- |
| [learn/01-refactoring](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/01-refactoring) | Static math and a composed two-operand calculation; retain encapsulated history |
| [learn/02-factory](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/02-factory) | A name-to-operation calculation factory, still with two operands |
| [learn/03-flexible-inputs](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/03-flexible-inputs) | Unary/collection operations and positional/named argument forwarding |
| [learn/04-commands](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/04-commands) | Session actions and commands; reuse familiar abstraction and CLI concepts |
| [learn/05-statistics-csv](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/05-statistics-csv) | pandas statistics and a CSV observation source |
| [learn/06-transfer](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/06-transfer) | Prepared-sequence execution, transfer evidence, and CI review |

Each branch builds directly on the previous part's commit, so the ancestry and differences follow the teaching sequence. Earlier lessons remain available cumulatively. `main` contains all six textbook lessons; use it when you want to read ahead. The published course branch set is `main` plus these six learning branches.

## Inspect a reference locally

Use your separate reference clone:

```bash
git fetch origin
git switch learn/01-refactoring
python -m pip install -r requirements.txt
python -m calculator
python -m pytest -q
```

Activate the reference environment first and run from the repository root. Parts 1–3 print demonstrations; Parts 4–6 accept interactive requests. Statistics and CSV begin in Part 5. Parts 1–4 need pytest only; Parts 5–6 add pandas.

Before changing a reference branch:

```bash
git status
git switch learn/02-factory
python -m pip install -r requirements.txt
python -m pytest -q
```

Save any intended local experiments before switching. Git may carry compatible changes across branches or refuse a switch when changes conflict. Keep your implementation and ongoing work in your own solution repository rather than using the instructor's reference as a starter.

If a learning branch is missing locally, fetch and explicitly create its tracking branch:

```bash
git fetch origin
git switch --track origin/learn/02-factory
```

Use that form only when the local branch does not already exist. `git switch main` returns to the full textbook and course-maintenance files.

## Read the change between parts

Before running the next part, predict which existing behaviors should still pass. Compare code and tests:

```bash
git diff origin/learn/01-refactoring..origin/learn/02-factory -- calculator tests
```

The [GitHub comparison](https://github.com/kaw393939/is218-command-factory-statistics/compare/learn/01-refactoring...learn/02-factory) shows the same first increment. Change both branch names to compare later neighbors. Part 3 intentionally changes operand interfaces; explain that requirement rather than treating the changed signature as an accidental regression.

The former course branches have been replaced by this chain. Old branch URLs and instructions for the previous organization are no longer the current navigation. Consult [migration](https://github.com/kaw393939/is218-command-factory-statistics/blob/main/docs/migration.md) for API changes and use [setup](setup.md) for separate solution/reference environments.

## For maintainers

`main` holds the canonical final application, lessons, and utilities that verify the six branch contents. `python tools/build_stages.py --check` checks the actual local/remote learning refs for application freshness and linear ancestry; `python tools/verify_course.py --full` verifies documentation and runs each branch's application/tests from its root.

Prepare complete branch trees without changing Git:

```bash
python tools/build_lesson_branches.py --output-dir /tmp/calculator-lessons
```

The export contains code, tests, cumulative lessons, setup/navigation, and a part-specific README. Review those trees, then commit/update learning branches sequentially so each new part descends from the previous part. The application-only `build_stages.py --output-dir` export does not provide the full lesson-branch contents. Keep publication and ancestry aligned with the teaching sequence; consult utility help before changing the export workflow.
