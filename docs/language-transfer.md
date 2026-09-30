# Use design vocabulary to learn another language

When you read code in an unfamiliar language, start with relationships: what does this object represent, what can callers ask it to do, what state does it hold, and when does execution happen?

Patterns give you a useful hypothesis. Verify it against the code rather than trusting class names.

## One design, different language mechanisms

| Design idea | Python here | Java / C# questions | TypeScript / Go questions |
| --- | --- | --- | --- |
| Execution contract | ABC with abstract execute() | Interface or abstract base class? What return type and visibility? | Interface? Structural typing or implicit satisfaction? |
| Stored request | self.values / self.path | Fields, constructors, mutability rules? | Object properties or struct fields? |
| Concrete behavior | Subclass overrides execute() | implements / extends or corresponding C# declaration? | Class method or method on a concrete type? |
| Uniform caller | command.execute() | How is the contract type referenced? | How is interface satisfaction checked? |
| Creation helper | Static create() selects a command | Static method or supplied factory object? | Factory function or method? |
| Expected failure | Raised exceptions | Which exception conventions apply? | Thrown exceptions or returned errors? |

These are investigation questions, not promises that every language uses the same inheritance structure. Dynamic typing, structural typing, and explicit interfaces can all support a common behavioral contract.

## Compare tiny interfaces

These snippets show the contract only; they are not complete applications.

```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self) -> float:
        pass
```

```java
interface Command {
    double execute();
}
```

```typescript
interface Command {
    execute(): number;
}
```

The shared meaning is “a caller can ask this request to execute and receive a numeric result.” Python's annotation does not enforce the return type at runtime. Java and TypeScript use different checking rules, and TypeScript's types do not remain runtime validation after compilation. You still need to learn the target language's actual behavior.

## What patterns cannot teach you automatically

You still need syntax, standard libraries, package installation, testing tools, runtime error rules, memory/ownership rules where relevant, and numeric/data-processing libraries. A Java Command cannot call pandas just because the design resembles the Python version.

Use official language documentation to answer those questions. Start with [Python classes](https://docs.python.org/3/tutorial/classes.html), [Java interfaces](https://dev.java/learn/interfaces/), [C# interfaces](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/interfaces), [TypeScript interfaces](https://www.typescriptlang.org/docs/handbook/interfaces.html), or [Go interfaces](https://go.dev/tour/methods/9).

## Transfer exercise

Choose one language you have not used much. Find its official documentation and write a short plan, not a whole port:

1. Express an execution contract.
2. Store a request's values.
3. Select a concrete request using a creation helper.
4. Explain how the caller receives errors.
5. Identify a numeric library or calculation approach to investigate.

Label which design ideas you already understand and which language facts you verified. Your goal is a disciplined learning method, not memorizing translations of Python keywords.
