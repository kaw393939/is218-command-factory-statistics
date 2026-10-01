# Vocabulary for the evolving calculator

Use these definitions after following a concrete example. Explain the term using a call or state change rather than memorizing the wording.

## Math and data

| Term | Meaning here |
| --- | --- |
| Operation | Function performing math using supplied inputs |
| Operand | Value the operation acts on |
| Arity | Required number of operands |
| Keyword-only setting | Argument that must be named, such as `exponent=4` |
| Finite | Neither NaN nor positive/negative infinity |
| Sample deviation | Spread using `n - 1`; `ddof=1` |
| Population deviation | Spread using `n`; `ddof=0` |
| DataFrame | pandas table |
| Series | One-dimensional pandas collection, such as a selected column |
| Validation | Enforcing the application's input, option, and result rules |

## Objects and calls

| Term | Meaning here |
| --- | --- |
| Class / instance | Definition for constructing objects / one particular object |
| State | Data stored on an object |
| `self` | Instance received by an instance method |
| Static method | Method receiving no implicit instance argument |
| Callable | Object that can be invoked; a function is one example |
| Function reference / call | Selected function itself / invocation producing a result |
| Composition | Storing or using another object or callable |
| Delegation | Asking a collaborator to perform work |
| Snapshot | Copied input sequence or mapping, independent of later edits to its original collection |
| Shallow copy | New collection containing references to the same contained objects |
| Side effect | Change beyond returning a result, such as recording history or printing |
| Refactoring | Reorganizing code while preserving intended observable behavior |

`*values` collects positional arguments in a definition and unpacks a sequence at a call. `**options` collects named arguments in a definition and unpacks a mapping at a call. `args` and `kwargs` are conventional names.

## Contracts and responsibilities

| Term | Meaning here |
| --- | --- |
| Abstraction | Useful behavior exposed without details the caller does not need |
| Abstract class | Class whose required methods can prevent incomplete subclasses from being instantiated |
| `ABC` / `abstractmethod` | Python helpers for expressing and enforcing that requirement |
| Inheritance | Relationship between a subclass and its base class |
| Polymorphism | Different objects used through a common behavior |
| Duck typing | Using supported behavior without requiring a particular inheritance relationship |
| Encapsulation | Controlled access to owned state through a component's interface |
| Type hint | Expectation for readers/tools; not automatic runtime validation |
| Simple Factory | Creation helper selecting/configuring a product |
| Factory Method | Product creation through an overridable creator method; not this implementation |
| Product | Configured `Calculation` returned by our factory |
| Command | Object representing an application action |
| Invoker / receiver | CLI calling `execute()` / session doing stateful application work |
| Strategy | Interchangeable algorithm; callable composition illustrates the relationship here |

## Errors and verification

| Term | Meaning here |
| --- | --- |
| EAFP | Attempt an operation and handle its expected failure |
| LBYL | Check a precondition before attempting |
| Exception propagation | A raised exception travels through callers until handled |
| Traceback | Call information useful for locating failure |
| Race condition | State can change between checking it and acting |
| REPL | Read, evaluate, print, and repeat |
| Assertion | Test statement checking expected behavior |
| Fixture | Test-provided setup or resource |
| Spy | Function/object recording calls to check delegation or timing |
| Regression | Previously supported behavior broken by a change |
| Coverage | Measurement of executed code; not proof of correctness |
| CI | Automated checks of a particular revision in configured environments |
| Commit SHA | Identity of the revision being tested or submitted |
| Benchmark | Measurement of a workload under specified conditions |
| Branch prediction | Processor prediction of control flow; Python `if` count is not a speed measurement |

## Design principles as questions

| Principle | Question | Example and limit |
| --- | --- | --- |
| Single responsibility | Which changes belong together? | File reading and math have separate homes; they still collaborate |
| DRY | Where is shared knowledge maintained? | Both sources use one numeric policy; similar test inputs can verify different behavior |
| KISS | What is the clearest design meeting the requirement? | A direct operation call is enough when no stored request is needed |
| YAGNI | Is the extra feature required now? | Persistent history and undo are not course requirements |
| Cohesion | Do these methods serve a coherent purpose? | History owns reading and changing its entry collection |
| Coupling | How much internal detail does a caller need? | History commands use `get_history()`, not `_entries` |
| Dependency injection | Can a collaborator be supplied? | A calculation receives its operation callable |
| Explicit contract | Are timing, inputs, results, and failures stated? | Factory returns an unexecuted calculation; command returns display text |

SOLID is a set of design questions, not a required class count. Liskov substitution asks concrete commands to honor the shared contract; interface segregation keeps it focused. Open/closed encourages useful extension boundaries, although registration and tests still change here. Dependency inversion considers useful abstractions; adding an ABC alone does not establish it throughout an application.

Misconception check: explain why static does not mean faster, abstract does not mean static, a registry does not eliminate hardware branches, a factory need not execute its product, and green CI does not establish understanding.
