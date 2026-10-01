# Vocabulary introduced through Part 2

[Branch home](../README.md) · [Part 2 lesson](lessons/02-factory.md)

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

A shallow copy protects collection membership; it does not freeze contained objects. Static method binding is not a speed guarantee.
