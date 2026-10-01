"""Generate cumulative supporting notes for the six learning-branch roots.

The builder supplies the branch README, setup/navigation, and lessons. These
pages describe only code present by the selected part; they do not depend on
the final application being copied into an early branch.
"""

STAGES = (
    "01-refactoring", "02-factory", "03-flexible-inputs",
    "04-commands", "05-statistics-csv", "06-transfer",
)
TEXTBOOK = "https://github.com/kaw393939/is218-command-factory-statistics/blob/main/docs"


def _navigation(index):
    return (
        f"[Branch home](../README.md) · "
        f"[Part {index} lesson](lessons/{STAGES[index - 1]}.md)\n\n"
    )


def _architecture(index):
    rows = [
        ("operations.py", "Stateless arithmetic using explicit operands"),
        ("validation.py", "Convert values to finite floats or report failure"),
        ("calculation.py", "Store operands and a callable; execute in get_result()"),
        ("history.py", "Own successful calculation/result entries; return a shallow read copy"),
        ("__main__.py", "Run this part's demonstration" if index < 4 else "Start the interactive application"),
    ]
    if index >= 2:
        rows.append(("factory.py", "Select a callable by name and construct a calculation without executing it"))
    if index >= 4:
        rows.extend([
            ("session.py", "Execute first, then record success through History"),
            ("commands.py", "Represent calculate/history/clear/help actions; return display text"),
            ("cli.py", "Prepare actions, invoke execute(), print, and recover from expected errors"),
        ])
    if index >= 5:
        rows.extend([
            ("statistics.py", "Apply the observation/count/deviation policy using pandas"),
            ("inputs.py", "Read the value column from CSV without performing math"),
        ])
    if index >= 6:
        rows.append(("sequence.py", "Execute already prepared calculations independently; collect results and errors"))
    table = "| File | Responsibility |\n| --- | --- |\n"
    table += "".join(f"| [{name}](../calculator/{name}) | {purpose} |\n" for name, purpose in rows)

    if index == 1:
        success = '''```python
from calculator.calculation import Calculation
from calculator.operations import Operations

calculation = Calculation("2", "3", Operations.add)
result = calculation.get_result()
assert result == 5.0
```

Construction converts the two strings to `self.a == 2.0` and `self.b == 3.0`,
then stores `Operations.add` without calling it. `get_result()` calls that
function with the stored operands and returns a finite float. The demonstration
caller prints the number.
'''
    elif index == 2:
        success = '''```python
from calculator.factory import CalculationFactory

calculation = CalculationFactory.create(" ADD ", "2", "3")
result = calculation.get_result()
assert result == 5.0
```

The factory normalizes the name to `add`, selects the callable, and constructs
`Calculation(a, b, operation)`. The calculation stores `2.0`, `3.0`, and
`Operations.add`; addition has not happened when the factory returns. The
caller executes `get_result()` and prints its returned number.
'''
    elif index == 3:
        success = '''```python
from calculator.factory import CalculationFactory

calculation = CalculationFactory.create("power", "3", exponent="4")
result = calculation.get_result()
assert result == 81.0
```

The factory collects positional values and named options, validates their
contracts, and converts numeric text. `Calculation` stores `(3.0,)`, a callable,
and `{"exponent": 4.0}`. Its constructor receives one values collection.
Execution expands that collection and mapping into `Operations.power(3.0,
exponent=4.0)`. The caller receives a number; creation has not performed math.
'''
    else:
        success = '''```python
from calculator.cli import prepare_command
from calculator.session import CalculatorSession

session = CalculatorSession()
command = prepare_command("power 3 exponent=4", session)
assert session.get_history() == []
assert command.execute() == "Result: 81.0000"
assert len(session.get_history()) == 1
```

Preparation separates the operation name, string operand, and named setting.
The factory returns a calculation holding `(3.0,)` and `{"exponent": 4.0}`.
`CalculateCommand` stores that calculation and the session; construction changes
no history. Its `execute()` delegates to `session.calculate()`, which calls
`get_result()` and records the returned `81.0` only after success. The command
formats a string; the interactive caller prints it.
'''

    creation = (
        'Calculation("1", "0", Operations.divide)'
        if index == 1 else 'CalculationFactory.create("divide", "1", "0")'
    )
    failed = (
        f"`{creation}` can be constructed: zero is a valid finite operand. "
        "When the caller asks for `get_result()`, division raises "
        "`ZeroDivisionError` and no result returns. Construction and execution "
        "are different failure boundaries.\n\n"
        "A caller saving history must place `History.add(calculation, result)` "
        "after successful execution. `History.add()` does not run math itself.\n"
    ) if index < 4 else '''For `divide 1 0`, preparation succeeds. The command delegates to the
session, and division raises `ZeroDivisionError` inside `get_result()`. Control
leaves before `History.add()`, so no successful entry is recorded. The command
does not return result text. The interactive loop prints `Error:` and accepts
the next request. A failed conversion or unknown name happens earlier, during
preparation, and likewise records nothing.
'''

    history = '''`History.add(calculation, result)` stores an entry. `get_history()` returns
a new list containing the same calculation objects and saved results. Clearing
that returned list cannot clear the owner's entries; `History.clear()` changes
the owned collection. The copy protects list membership, not every attribute
of the contained calculations. Save the result to avoid running math merely
to inspect an entry.
'''
    if index >= 4:
        history += '''
`HistoryCommand` reads through `session.get_history()` and formats saved
results. `ClearHistoryCommand` calls `session.clear()`. Those actions bypass
the calculation factory because they do not construct mathematical requests.
The CLI is the invoker; the session is the receiver. Commands return text and
do not prompt or print.
'''
    extra = ""
    if index >= 5:
        extra += '''
## Another source, the same calculation

`csv stddev values.csv` follows reader → DataFrame → value Series → list →
factory → calculation → calculate action → session → statistic → saved result.
The reader owns file structure; shared validation owns finite numeric inputs;
statistics owns minimum counts and `ddof`. Typed and CSV observations use the
same policy. Reading occurs during preparation, before calculation execution.
Sample deviation defaults to `ddof=1`; `ddof=0` explicitly requests population
deviation. Both require at least two observations here.
'''
    if index >= 6:
        extra += '''
## A caller processing prepared requests

`execute_sequence(session, calculations)` receives calculation objects that
already exist. For addition, zero division, and square, it returns successful
results `[5.0, 9.0]` and one error message. History lengths progress from 0 to
1, remain 1 after the failure, then become 2. Recovery sits inside the loop so
later items run. Errors are returned separately; this helper does not add a
failure collection to the session or parse raw input rows.

An unknown operation can fail before a calculation exists. A caller accepting
raw requests must put factory construction inside its per-item error boundary
when the requirement is to continue after preparation failures too.
'''
    return (
        f"# Follow the program through Part {index}\n\n" + _navigation(index)
        + "Read this alongside the current code. Label stored state, calls, "
          "returned values, and statements skipped after failure.\n\n"
        + "## Responsibilities present on this branch\n\n" + table
        + "\n## Trace one successful request\n\n" + success
        + "\n## Trace one failed request\n\n" + failed
        + "\n## Read and change history deliberately\n\n" + history + extra
    )


def _testing(index):
    if index <= 2:
        claims = [
            ("Static arithmetic works without constructing Operations", "tests/test_refactoring.py", "test_math_without_an_instance"),
            ("Construction stores behavior without calling it", "tests/test_refactoring.py", "test_construction_does_not_call_math"),
            ("Clearing a read copy preserves owned history", "tests/test_refactoring.py", "test_history_copy_protects_membership"),
            ("A domain failure occurs during execution", "tests/test_refactoring.py", "test_execution_reports_zero_division"),
        ]
        if index == 2:
            claims += [
                ("Normalized name selects the requested calculation", "tests/test_factory.py", "test_factory_constructs_selected_calculation"),
                ("Factory construction does not execute math", "tests/test_factory.py", "test_factory_never_executes"),
                ("Unknown names fail at selection", "tests/test_factory.py", "test_factory_reports_unknown_name"),
            ]
    else:
        claims = [
            ("Binary and unary operations preserve their math contracts", "tests/test_operations.py", "test_arithmetic / test_unary_operations"),
            ("A collection operation supports several values and rejects empty input", "tests/test_operations.py", "test_sum_accepts_a_collection"),
            ("Construction defers execution and snapshots the values", "tests/test_calculation.py", "test_construction_defers_execution_and_snapshots_inputs"),
            ("Execution rejects a nonfinite result", "tests/test_calculation.py", "test_reject_nonfinite_result"),
            ("Factory selects behavior but does not execute it", "tests/test_factory.py", "test_factory_configures_calculation / test_factory_does_not_execute"),
            ("Positional counts and named settings follow explicit rules", "tests/test_factory.py", "test_argument_counts_and_named_options / test_reject_invalid_argument_contract"),
        ]
    if index >= 3:
        claims.append(
            ("History reads protect membership and remain shallow", "tests/test_history.py", "test_history_copy_protects_collection_membership / test_history_objects_are_shared_by_the_shallow_copy")
        )
    if index >= 4:
        claims += [
            ("Incomplete action classes cannot be instantiated", "tests/test_commands.py", "test_contract_is_abstract"),
            ("Execution failure records no successful entry", "tests/test_commands.py", "test_failure_is_not_recorded"),
            ("Sessions own independent history", "tests/test_history.py", "test_sessions_have_independent_history"),
            ("An invalid request permits a later successful request", "tests/test_cli.py", "test_recovers_after_invalid_input"),
            ("EOF and Ctrl+C end the loop cleanly", "tests/test_cli.py", "test_input_ends_cleanly"),
        ]
    if index >= 5:
        claims += [
            ("Statistics obey known results and observation rules", "tests/test_statistics.py", "test_known_sample / test_reject_invalid_values / test_reject_invalid_ddof"),
            ("CSV and typed values share mathematical policy", "tests/test_csv.py", "test_sources_share_calculation_policy"),
            ("A missing observation is rejected, not discarded", "tests/test_csv.py", "test_missing_observation_is_rejected"),
            ("A failed source request permits later terminal work", "tests/test_cli.py", "test_recovers_from_csv_failures"),
        ]
    if index >= 6:
        claims += [
            ("A prepared sequence continues and records only success", "tests/test_sequence.py", "test_sequence_continues_after_failure_and_records_only_success"),
            ("An empty sequence changes no state", "tests/test_sequence.py", "test_empty_sequence_changes_no_state"),
        ]
    table = "| Required behavior | Supplied evidence |\n| --- | --- |\n"
    table += "".join(
        f"| {claim} | [{path}](../{path}): `{names}` |\n"
        for claim, path, names in claims
    )
    commands = "" if index < 4 else '''
For terminal recovery, `monkeypatch` supplies input and `capsys` captures
output. Include invalid input followed by a valid request and exit. Check both
the error and later result. A fake input running out is a test/protocol mismatch,
not an expected user failure to conceal.
'''
    files = "" if index < 5 else '''
Use `tmp_path` for test CSV files. Choose a dataset different from the supplied
example, and include bad structure or a missing observation. Do not rewrite
the repository's example file or silently discard bad data.
'''
    return (
        f"# Retain behavior evidence through Part {index}\n\n" + _navigation(index)
        + "You already know pytest and CI from the prerequisite. A changed "
          "public interface requires adapted calls, while its existing "
          "behavioral claims remain regression requirements.\n\n"
        + "## Read a test as a claim\n\n"
          "Identify setup, action, and assertion. `pytest.approx` compares "
          "floating-point results; `pytest.raises` checks a specific failure. "
          "A spy records whether a collaborator was called and with which "
          "arguments. For deferred execution, assert no calls immediately "
          "after construction, then one call after `get_result()`.\n\n"
        + table
        + "\n## Preserve the earlier contracts\n\n"
          "Keep arithmetic, finite input/result, deferred execution, and "
          "History ownership evidence when adding features. History reads "
          "must use `get_history()`. Clear the returned list, then read again "
          "to prove its membership was protected. Also check independent "
          "History owners and that an entry preserves its saved result "
          "without asking its calculation to execute again.\n"
        + ("\nPart 3 changes `Calculation(a, b, operation)` to "
           "`Calculation(values, operation, **options)`. Adapt the earlier "
           "History tests to the collection constructor instead of deleting "
           "their claims. Test the default and a nondefault setting, "
           "unsupported/nonfinite options, and positional/named forwarding.\n"
           if index >= 3 else "")
        + commands + files
        + "\n## Run from this branch's repository root\n\n"
          "```bash\npython -m pytest -q\n```\n\n"
          "Read a failed assertion before widening the checks. Fix its cause, "
          "run that focused test, then the accumulated suite. The retained "
          "GitHub Actions workflow runs this branch's tests on its revision; "
          "an old green run is not evidence for a new commit. Parts 1–4 "
          "require pytest; pandas joins the requirements in Part 5. Coverage "
          "shows executed code, not correctness or understanding.\n"
    )


def _glossary(index):
    groups = [
        (1, "Static math and composed calculations", [
            ("Operation / operand", "Mathematical callable / value it acts on"),
            ("Instance / self", "One object / the implicit instance argument of an instance method"),
            ("Static method", "Method receiving only explicit arguments, with no implicit instance"),
            ("Callable / call", "Behavior that can be invoked / the act of invoking it"),
            ("Function reference", "The function itself, such as Operations.add without parentheses"),
            ("Composition / delegation", "Store or use a collaborator / ask it to perform work"),
            ("State", "Data stored on an object, such as operands and its selected operation"),
            ("Finite", "Neither NaN nor positive/negative infinity"),
            ("Validation", "Enforce the application's numeric and result rules"),
            ("Encapsulation", "Change owned state through its public methods"),
            ("Shallow copy", "A new collection containing references to the same contained objects"),
            ("Saved result", "Value stored with a calculation so reading an entry need not execute math"),
            ("Exception propagation", "Failure travels through callers until a suitable handler responds"),
            ("EAFP / LBYL", "Attempt and handle expected failure / check a precondition before attempting"),
            ("Assertion / regression", "Check an expected behavior / previously supported behavior broken by a change"),
            ("Spy", "Callable recording calls to establish timing or delegation"),
            ("Refactoring", "Reorganize code while preserving its intended observable behavior"),
            ("CI / commit SHA", "Automated checks for a revision / that revision's identity"),
        ]),
        (2, "Selection and construction", [
            ("Registry", "Dictionary associating operation names with selected callables"),
            ("Class attribute", "Value held on the class, such as the shared operation registry"),
            ("Normalization", "Transform a name into the agreed lookup form, here strip/lower"),
            ("Simple Factory / product", "Creation helper / the configured Calculation it returns"),
            ("Factory Method", "Overridable creator method in an inheritance arrangement; not our helper"),
            ("Construction / execution", "Prepare and store a request / invoke its mathematical behavior"),
        ]),
        (3, "Different inputs and settings", [
            ("Arity", "Number of operands required by an operation"),
            ("Tuple / mapping", "Positional sequence / association of names with values"),
            ("*values", "Gather positional arguments in a definition; unpack a sequence at a call"),
            ("**options", "Gather named arguments in a definition; unpack a mapping at a call"),
            ("args / kwargs", "Conventional names, not required Python keywords"),
            ("Keyword-only setting", "Argument requiring a name, such as exponent=4 after a bare *"),
            ("Default", "Setting used when the caller omits that named argument"),
            ("Snapshot", "Stored input collection independent of later edits to the original collection"),
            ("Domain error", "Mathematical inputs outside the supported domain, such as a negative real square root"),
        ]),
        (4, "Application actions", [
            ("Command", "Object representing an application action with execute()"),
            ("Abstract class / ABC", "Contract that can prevent incomplete subclasses from being instantiated"),
            ("abstractmethod", "Marks a method that a concrete subclass must implement"),
            ("Polymorphism", "Invoke different actions through their common execute capability"),
            ("Invoker / receiver", "CLI invoking execute / session doing the stateful work"),
            ("REPL", "Read input, evaluate a request, print, and repeat"),
            ("Side effect", "Change beyond returning a value, such as recording or clearing history"),
            ("Type hint", "Expectation for readers/tools; not automatic runtime enforcement"),
            ("Fixture / monkeypatch / capsys", "Test resource / temporary replacement / captured output"),
        ]),
        (5, "Statistics and sources", [
            ("DataFrame / Series", "pandas table / one-dimensional collection or selected column"),
            ("Input adapter", "Read a source's structure and supply values to shared math"),
            ("Observation", "A value supplied to a statistic; missing values are errors here"),
            ("ddof", "Setting for the deviation denominator n - ddof"),
            ("Sample / population deviation", "Spread using n - 1 (ddof=1) / n (ddof=0)"),
            ("tmp_path", "Temporary test directory for isolated input files"),
            ("Race condition", "State can change between checking a file and acting on it"),
        ]),
        (6, "Evidence and adaptation", [
            ("Prepared sequence", "Calculation objects supplied before item-by-item execution"),
            ("Recovery boundary", "Specific handler around the work allowed to fail independently"),
            ("Transfer", "Adapt understood responsibilities to a different published requirement"),
            ("Coverage", "Measurement of executed code, not proof of correct assertions"),
        ]),
    ]
    text = f"# Vocabulary introduced through Part {index}\n\n" + _navigation(index)
    text += "Use each definition to explain an actual call, value, or state change.\n"
    for stage, title, terms in groups:
        if stage <= index:
            text += f"\n## Part {stage}: {title}\n\n| Term | Meaning here |\n| --- | --- |\n"
            text += "".join(f"| {term} | {meaning} |\n" for term, meaning in terms)
    text += "\nA shallow copy protects collection membership; it does not freeze contained objects. Static method binding is not a speed guarantee.\n"
    return text


def _errors(index):
    rows = [
        ("Convert numeric text", "Attempt float conversion; handle its expected failure"),
        ("Reject NaN/infinity", "Check the explicit finite-number contract"),
        ("Divide by zero", "Let arithmetic report ZeroDivisionError during execution"),
    ]
    if index >= 2:
        rows.append(("Select an operation", "Catch KeyError only around the dictionary lookup; report an unknown name"))
    if index >= 3:
        rows.extend([
            ("Enforce operand count", "Check the operation's published arity during creation"),
            ("Restrict named settings", "Validate supported names and finite numeric settings"),
        ])
    if index >= 4:
        rows.append(("Preserve successful history", "Execute first; an exception skips the following add"))
    if index >= 5:
        rows.extend([
            ("Read a source", "Attempt the read; expected file/parser failures reach the capable caller"),
            ("Require a header/minimum count", "Check the application's explicit structural/observation rule"),
        ])
    table = "| Situation present here | Deliberate choice |\n| --- | --- |\n"
    table += "".join(f"| {situation} | {choice} |\n" for situation, choice in rows)
    propagation = (
        "A zero-divisor calculation can be created, then fail in get_result(). "
        "If that call fails, assignment of its successful result and later "
        "history recording are skipped. Catch failure where the caller can "
        "respond; do not add a try block to every layer.\n"
        if index < 4 else
        "For divide 1 0, creation succeeds. During execution, the exception "
        "travels through the calculation, session, and action to the CLI. "
        "History.add and successful formatting are skipped. The CLI catches "
        "the expected error, reports it, and accepts another request.\n"
    )
    if index >= 5:
        propagation += "\nChecking file existence cannot guarantee later access or valid contents. Attempt the read and handle the documented failures. Missing observations must not silently disappear before the statistic runs.\n"
    if index >= 6:
        propagation += "\nFor execute_sequence, handle expected failure around each item, so later calculations run. Its inputs are already prepared: handling raw-request construction failures requires moving that work inside the caller's per-item boundary too.\n"
    return (
        f"# Locate failure through Part {index}\n\n" + _navigation(index)
        + "EAFP attempts an operation and handles expected failure. LBYL "
          "checks a precondition before attempting. Expect common success? "
          "Consider EAFP. Expect frequent rejection? Consider a cheap, "
          "reliable check. Failure frequency and correctness matter more "
          "than unpredictable ordering.\n\n"
        + table + "\n## Follow the skipped work\n\n" + propagation
        + "\nCatch specific expected exceptions; a broad catch can hide "
          "programming defects. Checks and exception handling both consume "
          "processor work and memory. Neither a dictionary nor removing "
          "Python if statements establishes faster execution. Measure "
          "equivalent workloads if performance matters.\n\n"
        + f"[Optional full discussion]({TEXTBOOK}/error-handling.md) is "
          "enrichment after you can explain the relevant failure path.\n"
    )


def supporting_notes(index: int) -> dict[str, str]:
    """Return cumulative supporting pages for an integer part from 1 to 6."""
    if type(index) is not int or not 1 <= index <= len(STAGES):
        raise ValueError("Part index must be an integer from 1 to 6.")
    return {
        "docs/architecture.md": _architecture(index),
        "docs/testing-guide.md": _testing(index),
        "docs/glossary.md": _glossary(index),
        "docs/error-handling.md": _errors(index),
    }
