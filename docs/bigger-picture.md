# Connect new patterns to familiar design

A design pattern describes a recurring problem and an arrangement of responsibilities. It gives us a vocabulary for discussing choices. It does not replace learning Python, mathematical rules, or library behavior.

The earlier calculator selected `Add` or `Subtract`, constructed an object, and used its inherited contract. The revised calculator selects a function, places it inside a calculation, and calls the function through that object. Both preserve the caller's idea of asking a calculation for a result.

## Inheritance and composition answer different questions

| Relationship | Earlier calculator | Revised calculator |
| --- | --- | --- |
| Inheritance: IS A | `Add` is a `Calculation` | `HistoryCommand` is a `Command` |
| Composition: HAS or USES | `History` has calculation objects | `Calculation` has an operation callable; session has a `History` |
| Common behavior | `get_result()` selects the subclass implementation | `execute()` selects the concrete action implementation |

Composition is useful when behavior should be supplied as a collaborator. Inheritance is useful when related objects should honor a common contract. Neither relationship is automatically better. Identify the requirement, the caller's expectations, and the cost of changing the design.

## Recognize the patterns in this application

A Simple Factory centralizes creation. Here, a name and inputs produce a configured `Calculation`. A registry alone is just a dictionary; its role in constructing the product is what makes it part of the factory.

Command represents an application action as an object. The CLI invokes `execute()`, and a command can ask the session to calculate, read history, or clear it. These are different actions even when they share one method name.

Storing interchangeable operation callables resembles Strategy's use of replaceable behavior. A separate hierarchy of strategy classes would add machinery this application does not need. Use the comparison to explain composition rather than adding another required pattern.

Read [patterns and features](patterns-and-features.md) after the concrete examples. Additional patterns are recognition examples, not implementation requirements.

## Principles are questions to investigate

Single responsibility asks which changes belong together. A different CSV header should affect input handling, while a different mathematical formula should affect operations. Components still cooperate; separation does not mean isolation.

Encapsulation means controlled access to state. `History.get_history()` returns a shallow list copy, and `clear()` changes the owned collection. Copying the list protects membership, not the mutable calculation objects inside it.

DRY asks where shared knowledge is maintained. Both input sources should use the same numerical policy. Similar-looking tests can remain separate when they establish different behavior.

Open/closed suggests useful extension boundaries. Adding an operation still changes registration, help, and tests here. An abstract class does not automatically make every part of a program satisfy SOLID.

## Performance belongs in a measured discussion

Centralizing selection makes responsibilities easier to maintain. It does not establish that dictionary lookup is faster than a conditional or that exception handling costs only memory. Review [error handling](error-handling.md) for the optional benchmark and its limits after you can trace the program correctly.

[Request traces](architecture.md) · [Language transfer](language-transfer.md) · [Reading guide](reading-guide.md)
