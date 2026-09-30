# Concepts to keep nearby

Use this page as a reference after you encounter an idea in a lesson. It is not a substitute for the worked explanation.

| Concept | Meaning in this application | Evidence to point to |
| --- | --- | --- |
| Object | State and behavior belonging to an instance | A command with saved values |
| Abstraction | A contract callers can use without concrete details | execute() on Command |
| Polymorphism | Same request method, object-specific behavior | Manual and CSV execute() implementations |
| Delegation | Ask another component to do part of the work | Command calls standard_deviation() |
| Separation of concerns | Different reasons to change live in different components | Prompts in CLI; statistic in shared function |
| Dependency | A component relies on another's interface/behavior | Factory imports concrete commands |
| Contract | Inputs, outputs, and failure behavior callers can expect | Numeric result or useful input/file error |
| Simple Factory | Selection and construction in one creation helper | CommandFactory.create() |
| Invoker | Decides when a request runs | CLI's command.execute() call |

## Values, types, and validation

input() returns text. split() makes a list of text tokens. A pandas Series gives the values a one-dimensional data container. pd.to_numeric tries conversion. Validation rejects nonfinite values and insufficient observations. std(ddof=1) calculates the sample statistic. float() returns a Python number. The CLI formats that number for display.

A type hint documents an expectation; it is not automatic input validation in Python. ABC checks that required abstract methods are implemented, not whether their return values satisfy every promise. Tests and implementation enforce the behavioral contract.

## Distinguish the tools

Pandas handles data. Pytest checks claims about behavior. Git records versions. GitHub hosts repositories. Actions runs checks. Command and Simple Factory describe software organization. None replaces the others.

[Architecture](architecture.md) · [Pattern scenarios](patterns-and-features.md) · [Glossary](glossary.md)
