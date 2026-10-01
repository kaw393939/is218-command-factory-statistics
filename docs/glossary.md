# Vocabulary introduced through Part 4

[Branch home](../README.md) · [Part 4 lesson](lessons/04-commands.md)

Use each definition to explain an actual call, value, or state change.

## Part 1: Static math and composed calculations

| Term | Meaning here |
| --- | --- |
| Operation / operand | Mathematical callable / value it acts on |
| Instance / self | One object / the implicit instance argument of an instance method |
| Static method | Method receiving only explicit arguments, with no implicit instance |
| Callable / call | Behavior that can be invoked / the act of invoking it |
| Function reference | The function itself, such as Operations.add without parentheses |
| Composition / delegation | Store or use a collaborator / ask it to perform work |
| State | Data stored on an object, such as operands and its selected operation |
| Finite | Neither NaN nor positive/negative infinity |
| Validation | Enforce the application's numeric and result rules |
| Encapsulation | Change owned state through its public methods |
| Shallow copy | A new collection containing references to the same contained objects |
| Saved result | Value stored with a calculation so reading an entry need not execute math |
| Exception propagation | Failure travels through callers until a suitable handler responds |
| EAFP / LBYL | Attempt and handle expected failure / check a precondition before attempting |
| Assertion / regression | Check an expected behavior / previously supported behavior broken by a change |
| Spy | Callable recording calls to establish timing or delegation |
| Refactoring | Reorganize code while preserving its intended observable behavior |
| CI / commit SHA | Automated checks for a revision / that revision's identity |

## Part 2: Selection and construction

| Term | Meaning here |
| --- | --- |
| Registry | Dictionary associating operation names with selected callables |
| Class attribute | Value held on the class, such as the shared operation registry |
| Normalization | Transform a name into the agreed lookup form, here strip/lower |
| Simple Factory / product | Creation helper / the configured Calculation it returns |
| Factory Method | Overridable creator method in an inheritance arrangement; not our helper |
| Construction / execution | Prepare and store a request / invoke its mathematical behavior |

## Part 3: Different inputs and settings

| Term | Meaning here |
| --- | --- |
| Arity | Number of operands required by an operation |
| Tuple / mapping | Positional sequence / association of names with values |
| *values | Gather positional arguments in a definition; unpack a sequence at a call |
| **options | Gather named arguments in a definition; unpack a mapping at a call |
| args / kwargs | Conventional names, not required Python keywords |
| Keyword-only setting | Argument requiring a name, such as exponent=4 after a bare * |
| Default | Setting used when the caller omits that named argument |
| Snapshot | Stored input collection independent of later edits to the original collection |
| Domain error | Mathematical inputs outside the supported domain, such as a negative real square root |

## Part 4: Application actions

| Term | Meaning here |
| --- | --- |
| Command | Object representing an application action with execute() |
| Abstract class / ABC | Contract that can prevent incomplete subclasses from being instantiated |
| abstractmethod | Marks a method that a concrete subclass must implement |
| Polymorphism | Invoke different actions through their common execute capability |
| Invoker / receiver | CLI invoking execute / session doing the stateful work |
| REPL | Read input, evaluate a request, print, and repeat |
| Side effect | Change beyond returning a value, such as recording or clearing history |
| Type hint | Expectation for readers/tools; not automatic runtime enforcement |
| Fixture / monkeypatch / capsys | Test resource / temporary replacement / captured output |

A shallow copy protects collection membership; it does not freeze contained objects. Static method binding is not a speed guarantee.
