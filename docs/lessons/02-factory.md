# Part 2: Create calculations with a factory

[Course home](../../README.md) · [Worked reference](https://github.com/kaw393939/is218-command-factory-statistics/tree/learn/02-factory/calculator) · [Concepts](../concepts.md)

[Previous part](01-refactoring.md) · [Next part](03-flexible-inputs.md)

## Begin with a familiar decision

Your previous CLI had a dictionary mapping names to Add and Subtract classes. Here the dictionary will select static operation callables and a creation helper will configure a Calculation. You know dictionary lookup; the new responsibility is giving construction one home.

**Main new idea:** a factory constructs a product without running it. **Carry forward:** fixed two-operand Calculation and static arithmetic. **Files:** add factory.py and its tests; change the demonstration entry point. No unary inputs, keyword options, or pandas yet.

## 2A — Identify repeated creation knowledge

Imagine a CLI and a test harness both accepting an operation name. If each decides how to create the Calculation, they each carry the same mapping and normalization rules. Changes now require coordinated edits.

Start with a helper supporting just add:

```python
from calculator.calculation import Calculation
from calculator.operations import Operations


def create_add(a, b):
    return Calculation(a, b, Operations.add)
```

Predict its return type. It returns an object, not 5.0. The caller still chooses when to call get_result(). Add a test that constructs divide with zero without executing it; this makes the distinction observable.

## 2B — Select the operation by name

```python
operations = {
    "add": Operations.add,
    "subtract": Operations.subtract,
}
```

These values have no calling parentheses. A class in the earlier registry was also callable, but calling it constructed a product. Calling one of these functions performs math. Here we save the function inside a Calculation instead of calling it immediately.

Use the full creation helper after explaining the two-choice version:

<!-- reference: learn/02-factory/calculator/factory.py -->
```python
"""A factory centralizes construction; it does not execute math."""
from calculator.calculation import Calculation
from calculator.operations import Operations


class CalculationFactory:
    operations = {
        "add": Operations.add,
        "subtract": Operations.subtract,
        "multiply": Operations.multiply,
        "divide": Operations.divide,
    }

    @staticmethod
    def create(name, a, b):
        name = name.strip().lower()
        try:
            operation = CalculationFactory.operations[name]
        except KeyError:
            raise ValueError(f"Unknown operation: {name}") from None
        return Calculation(a, b, operation)
```

The registry is a class attribute: one set of construction choices shared through CalculationFactory. create is static because it requires no factory-instance state. strip/lower normalize the supplied name. Only the lookup sits inside try. If it raises KeyError, the factory reports an unknown operation as ValueError. An unrelated error during construction must not be mislabeled as a lookup failure.

This is EAFP for dictionary selection. Your earlier program used explicit conditions for some input rules. Both styles remain useful. The goal here is centralized knowledge, not a claim that a dictionary removes hardware branches.

## 2C — Trace a complete request

```python
from calculator.factory import CalculationFactory

calculation = CalculationFactory.create(" ADD ", "2", "3")
result = calculation.get_result()
```

| Step | Value or action |
| --- | --- |
| Normalize name | "add" |
| Select registry value | Operations.add callable |
| Construct Calculation | Convert operands and store callable |
| Return from create | Calculation object; math has not run |
| Caller invokes get_result | Operation receives 2.0 and 3.0 |
| Return from get_result | 5.0 |

Predict which step reports an unknown name and which reports zero division. Write one test for each, and one that proves creation never executes.

## Understand the factory's scope

This Simple Factory configures one Calculation product class. It does not select among a product subclass hierarchy. Formal Factory Method uses an overridable creator method; we are not implementing that arrangement. The useful feature here is centralized creation, not a pattern label on a dictionary. See [the reading guide](../reading-guide.md).

The cost is an extra call and another place to read. The benefit is a clear boundary shared by callers. It does not mean every future extension will require zero edits elsewhere.

**Completion problem:** add multiply to a two-entry registry and predict the unchanged caller. **Independent problem:** add a new binary operation, write normalization/unknown-name tests, and identify where its construction policy lives.

```bash
python -m pytest -q
python -m calculator
```

Expect 5.0 and all accumulated tests passing. Explain creation versus execution without using the words factory or pattern, then commit.
