# Troubleshoot by locating the responsibility

| Symptom | Likely area | Evidence to inspect |
| --- | --- | --- |
| Import fails before a test runs | Setup / package structure | Interpreter, working folder, spelling, __init__.py |
| Sample answer is about 14.1421 for 10–50 | Statistical policy | ddof: population uses 0; tutorial requires 1 |
| CSV and manual disagree for identical values | Source preparation / shared policy | Header, selected values, missing cells, duplicated math |
| Blank values disappear | Parsing / validation | read_csv skips blank lines; quoted empty cells become missing values |
| Factory returns a number | Creation/execution boundary | Return the command, not command.execute() |
| Command object printed instead of result | Invoker | Call execute() before formatting |
| Invalid request ends the program | CLI recovery | Exceptions handled around prompts, factory, and execution |
| Tests raise StopIteration | Fake input or unexpected loop behavior | Number/order of input() calls |
| CI fails but local tests pass | Environment or submitted files | Dependencies, case-sensitive filenames, committed files, Python version |
| Starter's Actions run is red | Incomplete practice implementation | Score summary; red is expected below full rubric points |

A missing CSV line and a missing CSV cell are not the same. By default read_csv ignores completely blank lines. An empty quoted cell is parsed as missing and this application's function rejects it. Do not describe the default parser as counting every physical line as an observation.

When asking for help, provide the command you ran, the first useful error, your current branch/checkpoint, and the behavior you expected. Never paste credentials.
