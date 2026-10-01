# Retain behavior evidence through Part 6

[Branch home](../README.md) · [Part 6 lesson](lessons/06-transfer.md)

You already know pytest and CI from the prerequisite. A changed public interface requires adapted calls, while its existing behavioral claims remain regression requirements.

## Read a test as a claim

Identify setup, action, and assertion. `pytest.approx` compares floating-point results; `pytest.raises` checks a specific failure. A spy records whether a collaborator was called and with which arguments. For deferred execution, assert no calls immediately after construction, then one call after `get_result()`.

| Required behavior | Supplied evidence |
| --- | --- |
| Binary and unary operations preserve their math contracts | [tests/test_operations.py](../tests/test_operations.py): `test_arithmetic / test_unary_operations` |
| A collection operation supports several values and rejects empty input | [tests/test_operations.py](../tests/test_operations.py): `test_sum_accepts_a_collection` |
| Construction defers execution and snapshots the values | [tests/test_calculation.py](../tests/test_calculation.py): `test_construction_defers_execution_and_snapshots_inputs` |
| Execution rejects a nonfinite result | [tests/test_calculation.py](../tests/test_calculation.py): `test_reject_nonfinite_result` |
| Factory selects behavior but does not execute it | [tests/test_factory.py](../tests/test_factory.py): `test_factory_configures_calculation / test_factory_does_not_execute` |
| Positional counts and named settings follow explicit rules | [tests/test_factory.py](../tests/test_factory.py): `test_argument_counts_and_named_options / test_reject_invalid_argument_contract` |
| History reads protect membership and remain shallow | [tests/test_history.py](../tests/test_history.py): `test_history_copy_protects_collection_membership / test_history_objects_are_shared_by_the_shallow_copy` |
| Incomplete action classes cannot be instantiated | [tests/test_commands.py](../tests/test_commands.py): `test_contract_is_abstract` |
| Execution failure records no successful entry | [tests/test_commands.py](../tests/test_commands.py): `test_failure_is_not_recorded` |
| Sessions own independent history | [tests/test_history.py](../tests/test_history.py): `test_sessions_have_independent_history` |
| An invalid request permits a later successful request | [tests/test_cli.py](../tests/test_cli.py): `test_recovers_after_invalid_input` |
| EOF and Ctrl+C end the loop cleanly | [tests/test_cli.py](../tests/test_cli.py): `test_input_ends_cleanly` |
| Statistics obey known results and observation rules | [tests/test_statistics.py](../tests/test_statistics.py): `test_known_sample / test_reject_invalid_values / test_reject_invalid_ddof` |
| CSV and typed values share mathematical policy | [tests/test_csv.py](../tests/test_csv.py): `test_sources_share_calculation_policy` |
| A missing observation is rejected, not discarded | [tests/test_csv.py](../tests/test_csv.py): `test_missing_observation_is_rejected` |
| A failed source request permits later terminal work | [tests/test_cli.py](../tests/test_cli.py): `test_recovers_from_csv_failures` |
| A prepared sequence continues and records only success | [tests/test_sequence.py](../tests/test_sequence.py): `test_sequence_continues_after_failure_and_records_only_success` |
| An empty sequence changes no state | [tests/test_sequence.py](../tests/test_sequence.py): `test_empty_sequence_changes_no_state` |

## Preserve the earlier contracts

Keep arithmetic, finite input/result, deferred execution, and History ownership evidence when adding features. History reads must use `get_history()`. Clear the returned list, then read again to prove its membership was protected. Also check independent History owners and that an entry preserves its saved result without asking its calculation to execute again.

Part 3 changes `Calculation(a, b, operation)` to `Calculation(values, operation, **options)`. Adapt the earlier History tests to the collection constructor instead of deleting their claims. Test the default and a nondefault setting, unsupported/nonfinite options, and positional/named forwarding.

For terminal recovery, `monkeypatch` supplies input and `capsys` captures
output. Include invalid input followed by a valid request and exit. Check both
the error and later result. A fake input running out is a test/protocol mismatch,
not an expected user failure to conceal.

Use `tmp_path` for test CSV files. Choose a dataset different from the supplied
example, and include bad structure or a missing observation. Do not rewrite
the repository's example file or silently discard bad data.

## Run from this branch's repository root

```bash
python -m pytest -q
```

Read a failed assertion before widening the checks. Fix its cause, run that focused test, then the accumulated suite. The retained GitHub Actions workflow runs this branch's tests on its revision; an old green run is not evidence for a new commit. Parts 1–4 require pytest; pandas joins the requirements in Part 5. Coverage shows executed code, not correctness or understanding.
