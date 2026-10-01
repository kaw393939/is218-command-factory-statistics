# Diagnose the boundary before changing code

Record the exact command, working folder, interpreter, expected result, and traceback. Read the last exception first, then follow the relevant calls. Use [architecture](architecture.md) to separate selection, construction, execution, recording, and display.

| Symptom | Inspect | Next step |
| --- | --- | --- |
| No module named pandas/pytest | Active interpreter | Install requirements using that interpreter's `-m pip` |
| No module named calculator | Current directory | Run from your solution root or the selected reference branch's repository root |
| Reference displays features from a later part | Current branch | Check `git branch --show-current`; select your matching `learn/...` checkpoint |
| Learning branch is not found | Remote references | Fetch in the reference clone; use a tracking branch as explained in navigation |
| Entry point shows an earlier demonstration | Part/checkpoint | Parts 1–3 demonstrate math; Part 4 introduces the interactive loop |
| Old tests import `Add`/`Subtract` after refactoring | Intentional API change | Preserve their behavior claim through static operations/composed calculation |
| `CommandFactory` import fails | Which curriculum the code came from | Use current `CalculationFactory`; consult migration |
| Cannot instantiate an abstract class | Missing required method | Implement the concrete command's `execute()`; compare the earlier ABC lesson |
| A float object is not callable | Stored operation | Save `Operations.add`, not `Operations.add(2, 3)` |
| Wrong number of positional arguments | Collection/unpacking and arity | Expand `*values` by hand; distinguish one tuple from several operands |
| Power uses default despite supplied setting | Option path | Trace collection, copied mapping, and `**options` forwarding |
| Negative square root fails | Mathematical domain | Expected real-domain failure belongs to execution, not an unknown-name handler |
| Clearing a read list does not clear history | Encapsulation | Call session/history `clear()` to change owned state |
| Failed calculation appears in history | Statement order | Compute successfully before recording |
| History display runs math again | Saved result | Format the entry's stored result rather than calling `get_result()` |
| Sample/population answers differ | `ddof` and published policy | Sample uses 1; population uses 0; do not infer an exam contract from old notes |
| Missing CSV | Current directory/path argument | Use a path relative to the caller's directory or an appropriate absolute path |
| CSV observations silently disappear | Reader and validation | Reject missing observations before aggregation |
| Fake terminal input runs out | Number/protocol of `input()` calls | Match the test's answers to the current single-line grammar |
| Later sequence item never executes | Location of recovery handler | Recover per item when the contract requires continuation |
| Unexpected traceback disappears | Broad catch | Restore specific expected handlers and fix the exposed bug |
| Automated assessment score is below total rubric | Which portion was measured | Automated behavior is 60 points; student tests and explanations need review |

After fixing the cause, rerun the focused test and the accumulated suite. Do not alter a requirement or catch every exception merely to make a traceback disappear.

[Setup](setup.md) · [Branch navigation](branches.md) · [API migration](migration.md) · [Test evidence](testing-guide.md)
