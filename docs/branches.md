# Work through branches without losing your solution

main is the course home and contains all lesson readings. Each learn branch is a complete cumulative application snapshot. You do not combine branch folders. You build one solution in a separate folder and consult the matching snapshot when needed.

| Branch | New responsibility | Reference test cases |
| --- | --- | ---: |
| learn/01-statistics | Shared validation and calculation | 8 |
| learn/02-command | Manual request object | 11 |
| learn/03-csv | File request object | 14 |
| learn/04-factory | Central construction choice | 18 |
| learn/05-repl | Interactive invocation and recovery | 22 |
| learn/06-ci | CI and design reflection | 22 |

Counts include parametrized cases. Your independent exercises may add tests; an exact count is not your grading target.

## At each stage

1. Open the lesson and write your predictions in a learning log.
2. Create/change only the files listed in its change table.
3. Run each small checkpoint before completing the final snapshot.
4. Compare your files with the worked branch if you are stuck.
5. Run earlier tests too; a new feature must preserve their behavior.
6. Explain the design, complete an independent exercise, and commit in your solution repository.

Use `git switch learn/02-command` only inside statistics-reference to inspect the next snapshot. A virtual environment is an ignored local folder, so switching branches does not rebuild it; reinstall requirements if they change. If Git refuses to switch because you changed tracked files, inspect `git diff` and save the experiment on your own branch before switching. Do not discard work just to follow a reading link.

## Compare neighboring stages

GitHub Compare shows the application changes between two stage branches. Documentation may also differ; focus first on calculator/ and tests/.

```bash
git diff learn/02-command..learn/03-csv -- calculator tests
```

The two dots compare the branch tips. This is a reading command inside the reference checkout, not an instruction to overwrite your solution.

## Tutorial versus assessment

The tutorial branches contain worked examples. The practice repository main branch contains TODO skeletons and acceptance tests. Its solution branch is for review after your timed attempt. The real test will vary a bounded requirement; exact requirements are provided with the test.
