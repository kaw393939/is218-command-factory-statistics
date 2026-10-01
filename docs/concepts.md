# Python mechanisms at the point of use

You already used objects, inheritance, abstraction, encapsulation, exceptions, and tests in the [prerequisite calculator](https://github.com/kaw393939/is218-oop-calculator). This reference connects those ideas to the changes in the six parts. Read the relevant section when its syntax appears, then explain an actual call from your program.

## Part 1: Static math and stored behavior

An instance method receives `self`, the object on which it was called. The earlier `Add.get_result()` used `self.a` and `self.b`. The revised `Calculation.get_result()` uses its stored values and operation. It remains an instance method because different calculations hold different requests.

A static method receives only explicit arguments. `@staticmethod` makes the method accessible without Python inserting an instance argument. The arithmetic needs no `Operations` object:

```python
from calculator.operations import Operations

result = Operations.add(2, 3)
```

A decorator is applied to a function or class definition. `@staticmethod` describes method binding; `@abstractmethod` marks a requirement for subclasses. Static does not mean abstract, immutable, or automatically faster. Module-level functions would also be valid; this course groups related math in a class.

A callable is an object that can be invoked. A function is one example. These two lines do different work:

```python
operation = Operations.add
result = operation(2, 3)
```

The first saves a function reference. The second calls it and saves its returned number. Writing `operation = Operations.add(2, 3)` would save the result, so `operation` would no longer contain the function we intend to call later.

Composition means supplying or storing a collaborator. A calculation uses its operation callable. The previous subclass design and this composed design solve related requirements differently; neither relationship makes math execute during construction by itself.

## Part 2: Selection and construction

A dictionary maps keys to values. Our registry maps operation names to function references, without calling them. A class attribute holds that registry on `CalculationFactory`, rather than making a new registry inside each calculation.

Factory creation selects behavior, validates creation rules, and returns a calculation object. Execution happens when the caller asks for its result. An unknown name fails during selection; division by zero fails during execution. Keeping these moments distinct makes their errors understandable.

`__init__` initializes an instance's attributes. Type hints describe expected inputs and returns; they do not perform conversion or validate values at runtime. A `-> float` annotation alone does not guarantee a finite numerical result.

## Part 3: Arity, collection, and unpacking

Arity is the number of operands an operation requires. Addition needs two; square root needs one; sum can accept many. Flexible interfaces do not make incorrect operand counts valid.

Compare positional collection and unpacking:

```python
def total(*values):
    return sum(values)

numbers = (2, 3, 4)
result = total(*numbers)
```

In the definition, `*values` collects positional arguments into a tuple. At the call, `*numbers` unpacks a sequence into positional arguments. Calling `total(numbers)` supplies one tuple argument instead of three numeric arguments. Predict that distinction before running it.

The names `args` and `kwargs` are conventions, not special keywords. Our interface uses `*values` and `**options` because those names explain their roles.

A keyword-only setting must be named:

```python
from calculator.operations import Operations

result = Operations.power(3, exponent=4)
```

In `def power(value, *, exponent=2)`, the bare `*` requires `exponent` to be supplied by name. Its default is 2 when omitted. The setting describes how to perform the operation, while `value` supplies its operand.

Compare named collection and unpacking:

```python
def describe(**options):
    return options

settings = {"exponent": 4}
collected = describe(**settings)
```

In a signature, `**options` gathers named arguments into a dictionary. At a call, `**settings` passes dictionary entries as named arguments. Factory creation collects options, the calculation stores a copied mapping, and execution unpacks it into the selected operation. The factory still checks which settings that operation supports.

A tuple gives a calculation its own operand sequence. Changing the original list later does not change that stored sequence. Copying the options mapping has a similar purpose. Calculation attributes remain assignable, so we do not describe the whole object as immutable.

Numeric conversion belongs in `validation.py`. `float()` converts accepted inputs or raises an exception; `isfinite()` rejects NaN and infinity. The application separately specifies count and domain rules. A generator expression computes items as requested; an explicit loop is a useful first explanation before compact expressions.

## Part 4: Reuse abstraction for application actions

You already used `ABC` and `@abstractmethod` for calculation subclasses. Now ordinary concrete action classes first demonstrate their shared `execute()` behavior. The abstract `Command` then requires future concrete commands to provide that method.

An incomplete subclass cannot be instantiated while its abstract methods remain unimplemented. This checks implementation of the required method, not its correct behavior or annotated return type. Tests establish those additional claims.

Polymorphism means the CLI can call `execute()` on different commands through the same contract. Calculate returns formatted result text; history returns existing entries; clear changes session state. The CLI prints that text. Commands do not prompt for input.

Encapsulation remains important. `History._entries` owns successful `(calculation, result)` entries. A leading underscore communicates internal use by convention, not security. `get_history()` returns a shallow list copy; clearing the returned list cannot erase the owned entries. The calculation objects in that copy are still shared.

The session executes first and adds an entry only after success. Saving the result means displaying history does not run math again. This is a deliberate change from the prerequisite's live calculation display.

## Part 5: Tables, observations, and policy

A pandas `DataFrame` is a table. Selecting `frame["value"]` yields a `Series`, a one-dimensional column. `tolist()` supplies observations to the same factory used for typed values. Reading a file supplies data; it does not choose the mathematical implementation.

Standard deviation uses a denominator of `n - ddof`. Here, `ddof=1` selects sample deviation and `ddof=0` selects population deviation. The application's required counts and rejection of missing values are separate rules. Pandas defaults must be reviewed rather than assumed to match those rules.

For `[2, 4, 6]`, mean is 4 and squared deviations sum to 8. Sample deviation is `sqrt(8 / 2) = 2`; population deviation is `sqrt(8 / 3)`, approximately 1.6330.

## Part 6: Evidence and adaptation

`python -m calculator` runs the package's `__main__.py`. Imports load definitions from modules. Keep the entry point small so the same application objects remain usable from tests or another caller.

Tests provide evidence about specified behavior. A spy records calls to establish timing or delegation. Coverage measures executed code, not correctness. CI repeats checks for a particular revision and environment; the prerequisite already introduced that workflow.

A prepared sequence contains calculation objects before execution. Executing it one calculation at a time lets one expected failure be reported while later calculations still run. Trace the state after each item. This transfers the same construction, execution, and recovery ideas to another caller.

[Python classes](https://docs.python.org/3/tutorial/classes.html) · [Static methods](https://docs.python.org/3/library/functions.html#staticmethod) · [Abstract classes](https://docs.python.org/3/library/abc.html) · [Flexible arguments](https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists) · [Exceptions](https://docs.python.org/3/tutorial/errors.html)
