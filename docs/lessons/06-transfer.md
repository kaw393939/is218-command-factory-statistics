# Part 6: Integrate, explain, and adapt

[Course home](../../README.md) · [Worked reference](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/06-transfer/calculator) · [Concepts](../concepts.md)

[Previous part](05-statistics-csv.md)

You already learned tests, coverage, and CI in the previous course. Use them as evidence here. The new work is reading a requirement, locating the right responsibility, and adapting behavior without copying a whole reference application.

**Main new idea:** independent transfer using familiar contracts. **Carry forward:** all five previous parts. **Files:** add sequence.py/test_sequence.py for the guided example; retain CI and update your explanations/tests. Practice and exam will give formulas, input contracts, and parsing support, so success depends on applying the design rather than recalling library syntax.

## 6A — Retrieve the whole flow

Without looking at code, draw a successful power request and failed division. Label construction, execution, state changes, and error handling. Then verify against [architecture](../architecture.md).

Explain the relationship change from the earlier Add subclass to a stored static callable. Explain why the factory produces a Calculation while Command represents an application action. Describe the History copy's protection and its limit.

## 6B — Process a sequence of prepared calculations

So far a person submits one request per prompt. A new caller may supply several prepared Calculation objects. Each should run independently; failure should not prevent later work.

Before coding, decide: where does iteration belong, where is success recorded, and which errors should be caught? Keep session.calculate's successful-only rule. Do not move it into each caller.

<!-- reference: learn/06-transfer/calculator/sequence.py -->
```python
"""Guided transfer: process already prepared calculations independently.

CSV request parsing and batch-specific commands are assessment adaptations.
This example deliberately receives Calculation objects, not file rows.
"""


def execute_sequence(session, calculations):
    results = []
    errors = []
    for calculation in calculations:
        try:
            result = session.calculate(calculation)
        except (ValueError, ZeroDivisionError, OverflowError) as error:
            errors.append(str(error))
        else:
            results.append(result)
    return results, errors
```

The loop uses familiar statements. Each try block covers one item; catching outside the whole loop would stop later items. The else runs only after successful execution. results and errors describe the sequence outcome, while History still contains only successful calculations.

This helper accepts already prepared Calculation objects. It does not load request rows or define the exam's BatchCommand. Preparation failures require a different boundary because an invalid name can fail before a Calculation exists.

**Worked request:** add 2 3, divide 1 0, square 3. Predict results [5.0, 9.0], one error, and two history entries. Test later success after the error, not just the first successful result.

## 6C — Fade the support

Complete these in order, using notes but not the full reference answer:

1. Fill in the success-only result append in a partial sequence loop.
2. Adapt the loop to receive name/values/options requests and call the factory inside each item's try block. Explain why this catches preparation failures as well as execution failures.
3. Add an action reporting counts from saved successes and separately retained failures. Define whether clear resets both and test the rule.
4. Adapt a configured unary formula supplied by the instructor. Publish operand count, allowed option names, defaults, and failures before editing the registry.
5. Adapt an input reader to a supplied schema while leaving Operations free of file knowledge.

These activities rehearse categories of change. The timed practice/exam supply different formulas, actions, and input contracts. Naming changes and a different dataset are not enough to demonstrate transfer.

## 6D — Establish evidence

Run cumulative tests and a fresh-environment demonstration. Review the existing CI workflow: it checks a particular revision on supported interpreters. An old green check or complete line coverage does not prove the new requirements work.

```bash
python -m pytest -q
```

Course maintainers separately run `python tools/verify_course.py --full` from `main` to verify links, excerpts, and all six cumulative lesson branches. Students do not recreate that utility. Assessment maintainers also use tools/verify_assessments.py to confirm starters fail, references pass, unchanged copied code fails new requirements, and important regressions lose points.

For student tests, explain the requirement each assertion establishes. Good examples distinguish successful execution from construction, verify success after an earlier failure, and demonstrate that mutating a returned history list cannot alter internal state. Avoid merely repeating a supplied acceptance test or asserting the reference's source text.

## 6E — Prepare for open-notes application

The 90-minute practice asks you to adapt calibration operations, named settings, a latest-result action, CSV integration, and a deliberately faulty recording order. The real assessment applies the same ideas to multiple requests and summary reporting. Both supply familiar infrastructure and exact contracts. Their automated checks account for 60 points; student-written tests and short traces/design explanations account for the other 40 through instructor review.

Open notes and prior code are allowed under the announced assessment policy. Reusing a well-understood converter or calculation class is useful. Copying the entire teaching application unchanged does not satisfy the assessed adaptations. Explain what you reused, what changed, and why.

Checkpoint: complete an adaptation with tests, trace a failure, review the current CI revision, and record one limitation of your evidence. [Practice preparation](../practice-preparation.md) explains the next step.
