# Recognize patterns through problems

| Category | Question | Familiar example |
| --- | --- | --- |
| Creational | How should objects be constructed? | Factory selects/configures a Calculation from a name |
| Structural | How should components fit together? | Adapter wraps an external API to match an expected interface |
| Behavioral | How should actions and communication work? | Command gives calculate/history/clear a common execution contract |

Our Simple Factory creates one Calculation product class with varying callable configuration. Formal Factory Method delegates product creation through an overridable method in a creator hierarchy; we do not implement that hierarchy. A dictionary alone is not a pattern: explain the construction responsibility it serves.

Calculation composes a selected callable; this resembles Strategy's varying algorithm. Commands represent application actions and use the session as their receiver. The CLI is an invoker and also prepares requests. Distinct responsibilities matter more than matching every box in a textbook diagram.

Observer could notify displays when history changes; Adapter could normalize another data source; Facade could provide a simple interface to a larger subsystem. These are recognition examples, not assignment requirements. Ask whether a function or direct call would solve the actual problem more simply.

[Classification](https://refactoring.guru/design-patterns/classification) · [Factory comparison](https://refactoring.guru/design-patterns/factory-comparison) · [Command](https://refactoring.guru/design-patterns/command) · [Reading guide](reading-guide.md)
