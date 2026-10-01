# Part 3: One, two, and many operands

[Course home](../../README.md) · [Worked reference](../../examples/stages/03-flexible-inputs/README.md) · [Concepts](../concepts.md)

[Previous part](02-factory.md) · [Next part](04-commands.md)

## Let a requirement change the interface

Square and square root need one operand. Addition needs two. A sum needs a collection. Our fixed Calculation(a, b, operation) now forces an awkward second operand for some requests and cannot represent others.

**Main new idea:** flexible positional inputs, followed by named configuration. **Carry forward:** stored callable, factory selection, explicit operation contracts. **Files:** expand operations.py, calculation.py, factory.py and tests. The interface changes are deliberate; this part's tests replace assumptions of exactly two stored fields.

## 3A — Introduce a collection before the star syntax

Start by changing Calculation to store a sequence:

```python
class Calculation:
    def __init__(self, values, operation):
        self.values = tuple(values)
        self.operation = operation
```

A tuple snapshots the supplied collection membership and values. It does not freeze the whole object: attributes can still be reassigned. The shared validator later converts each value to a finite float.

How do we call a two-argument function using that tuple? Compare:

```python
values = (2, 3)
result = Operations.add(values[0], values[1])
```

```python
values = (2, 3)
result = Operations.add(*values)
```

At a call site, * unpacks the collection into positional arguments. It does not perform arithmetic or change the function's contract.

## 3B — Gather one, two, or many positional arguments

```python
def gather(*values):
    return values
```

Predict gather(2), gather(2, 3), and gather(2, 3, 4). In a signature, *values collects positional arguments into a tuple. The name args is conventional, not required.

Add square(value), sqrt(value), and sum(*values). Require at least one value for this application's sum, even though Python's built-in sum can return zero for an empty collection. Explain that a library behavior and an application's contract can differ.

The factory now exposes create(name, *values). Its operation registry still selects a callable. A second registry maps fixed-arity operations to operand counts: square/sqrt require one; arithmetic requires two. Collection operations enforce their own minimum. Flexible syntax does not mean arbitrary inputs are accepted.

**Checkpoint:** test square, sqrt, sum, wrong operand counts, and delayed domain errors. A negative real square root fails during execution.

## 3C — Add named settings only after positional inputs work

Power provides a reason for configuration:

```python
from math import pow


def power(value, *, exponent=2):
    return pow(value, exponent)
```

The bare * marks exponent as keyword-only. Call power(3, exponent=4); calling power(3, 4) is invalid. The default exponent is 2.

Now learn the two uses of ** separately:

```python
def gather_options(**options):
    return options
```

```python
options = {"exponent": 4}
result = power(3, **options)
```

The definition gathers named arguments into a dictionary; the call unpacks a dictionary as named arguments. kwargs is the conventional name. First predict these tiny examples; only then forward both inputs through Calculation:

```python
class Calculation:
    def __init__(self, values, operation, **options):
        self.values = tuple(values)
        self.operation = operation
        self.options = dict(options)

    def get_result(self):
        return self.operation(*self.values, **self.options)
```

The final reference adds the established numeric and finite-result checks. It does not introduce a new validation policy. The public constructor is now Calculation(values, operation, **options); a caller's values list is passed as one collection here.

## 3D — Forward arguments without abandoning contracts

```python
from calculator.factory import CalculationFactory

values = [3]
options = {"exponent": 4}
calculation = CalculationFactory.create("power", *values, **options)
result = calculation.get_result()
```

The factory gathers these values and options, checks allowed option names, converts numeric settings, and constructs the object. It still never executes math. Inspect factory.py in the worked reference after implementing those responsibilities; its loops are explicit so each check can be traced.

| Boundary | Positional data | Named data |
| --- | --- | --- |
| Factory call | *values unpacks the list | **options unpacks the dict |
| Factory signature | *values gathers a tuple | **options gathers a dict |
| Calculation constructor | One values collection | **options gathers configuration |
| Operation call | *self.values supplies operands | **self.options supplies settings |

Trace power(3, exponent=4) through every row. No step should accidentally evaluate the callable early.

**Completion problem:** fill in the unpacking in get_result. **Independent problem:** add a unary configured operation with a supplied formula (for example value divided by factor), a default setting, and a zero-factor error. Test one success, one option failure, and one domain failure.

```bash
python -m pytest -q
python -m calculator
```

The reference prints 5.0 and 81.0. Explain why the old a/b interface changed, why factories still need validation, and which use of * or ** gathers versus unpacks. Commit.
