# Patterns behind familiar program features

Patterns suggest ways to arrange a solution. A feature does not prove that an application uses a particular pattern. These are teaching scenarios you can reason about, not descriptions of specific products.

## Creation: choose or configure an object

| Scenario | Candidate | Why it may help | Tradeoff |
| --- | --- | --- | --- |
| Choose a manual or file request from a command name | Simple Factory | Put selection and construction in one place | That selection still needs updating for new request types |
| Different subclasses of an importer construct different reader implementations | [Factory Method](https://refactoring.guru/design-patterns/factory-method) | Let subclasses supply a creation decision | Adds a creator hierarchy |
| Build a report with optional title, sections, and export settings | [Builder](https://refactoring.guru/design-patterns/builder) | Make staged construction explicit | Can be unnecessary for a few constructor arguments |
| Create matching controls for different UI families | [Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory) | Create related objects that belong together | Adds several collaborating abstractions |

Read [Factory Comparison](https://refactoring.guru/design-patterns/factory-comparison), section 4, before equating a class named Factory with Factory Method. Our create() uses conditional selection; subclasses do not override a creator method.

## Structure: make components cooperate

| Scenario | Candidate | Why it may help | Tradeoff |
| --- | --- | --- | --- |
| A vendor API exposes different method names and data shapes | [Adapter](https://refactoring.guru/design-patterns/adapter) | Translate the vendor interface to the one your application expects | Translation must be maintained as either interface changes |
| Add logging or caching around an existing service interface | [Decorator](https://refactoring.guru/design-patterns/decorator) | Wrap behavior while preserving the interface | Wrapper order and behavior can become harder to trace |
| A checkout screen needs several subsystem calls | [Facade](https://refactoring.guru/design-patterns/facade) | Offer a convenient entry point that coordinates those calls | The facade can accumulate too many responsibilities |

A shared helper function is not automatically a Facade. In this course, standard_deviation() is the shared calculation policy; we do not add a Facade class.

## Behavior: organize requests, choices, and notifications

| Scenario | Candidate | Why it may help | Tradeoff |
| --- | --- | --- | --- |
| Buttons and shortcuts trigger the same action, or jobs wait for execution | [Command](https://refactoring.guru/design-patterns/command) | Represent each request behind an execution contract | Adds request objects and indirection |
| Several interested components react when a model changes | [Observer](https://refactoring.guru/design-patterns/observer) | Publish changes to registered subscribers | Notification order, lifecycle, and unwanted subscriptions need care |
| Select a shipping-cost or route algorithm at runtime | [Strategy](https://refactoring.guru/design-patterns/strategy) | Give a context interchangeable implementations | Simple alternatives may only require functions |

Command can support undo when requests also preserve or reverse state changes. execute() alone does not implement undo. Our calculator reads data and returns a number; it does not reverse actions.

Command and Strategy can look similar. Ask what is represented: a specific request with its arguments, or an interchangeable way to perform a task within a context? In our program the objects represent requests, and their stored inputs are part of those requests.

## Practice choosing, not naming

For each scenario, identify the changing responsibility, suggest a candidate, and explain one simpler alternative:

1. Three screens need to invoke the same “export report” request.
2. A dashboard must update a chart, table, and status message after new data arrives.
3. A service must use either a fixed-rate or distance-based shipping calculation.
4. A new library returns fields whose names differ from your application's interface.
5. A two-line script needs to add two numbers once.

<details>
<summary>Compare your reasoning</summary>

Command can represent export requests; Observer can distribute change notifications; Strategy can represent alternate shipping algorithms; Adapter can translate the library interface. The tiny one-time script may need none of these. Accept another choice when the student explains its responsibilities and costs coherently.

</details>

## A shared vocabulary for teams

“We use a Command so the CLI can execute either request uniformly” tells a reviewer what relationship to inspect. “We use a factory” is too vague until you explain the creation mechanism. Follow every pattern name with evidence: which object, which contract, which caller, which changing responsibility?

Use [language transfer](language-transfer.md) to practice describing the same arrangement outside Python.
