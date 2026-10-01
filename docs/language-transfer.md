# Transfer relationships before syntax

The prerequisite used an inheritance relationship: `Add` IS A `Calculation`. This course also uses composition: a calculation HAS an operation callable and a session HAS a history. Those relationships can transfer even when another language expresses them differently.

| Design idea | Python here | Question in another language |
| --- | --- | --- |
| Stateless operation | `@staticmethod` | Static method, module function, or package function? |
| Configurable calculation | Stored tuple and callable | Function pointer, delegate, closure, or strategy object? |
| Creation helper | `CalculationFactory.create()` | Factory function or static helper? |
| Flexible operands/settings | `*values`, `**options` | Sequence parameter, variadic arguments, or explicit options object? |
| Action contract | ABC with `execute() -> str` | Interface, abstract class, or structural contract? |
| Encapsulated history | Private-by-convention list; shallow read copy | Which access, ownership, and copying rules apply? |
| Expected failure | Exceptions handled by a capable caller | Exceptions or explicit error result? |

Patterns describe relationships. They do not automatically transfer numeric-library defaults, argument syntax, package tools, memory ownership, or runtime type enforcement.

## Compare a familiar contract

```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self) -> str:
        pass
```

```java
interface Command {
    String execute();
}
```

```typescript
interface Command {
    execute(): string;
}
```

These examples express a common capability, but their checking and runtime rules differ. Python's annotation alone does not prevent a method from returning a number. Consult the language's official documentation rather than assuming syntax and enforcement are identical.

Transfer task: choose a language and plan a calculation factory plus an action that reads successful history. Identify where conversion, state, and error handling belong. Label the relationships you already know separately from language rules you verify. Do not add a whole application before the smaller contract is clear.

[Java interfaces](https://dev.java/learn/interfaces/) · [C# interfaces](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/interfaces) · [TypeScript interfaces](https://www.typescriptlang.org/docs/handbook/interfaces.html) · [Go interfaces](https://go.dev/tour/methods/9)
