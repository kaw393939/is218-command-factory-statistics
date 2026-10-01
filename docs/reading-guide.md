# Read with a question and a known example

Revisit the [prerequisite calculator](https://github.com/kaw393939/is218-oop-calculator) when the relationship is familiar but the syntax is unclear. Do the small course example before widening the discussion to a whole pattern catalogue.

| Part | Focused reading | Question to answer using this application |
| --- | --- | --- |
| 1 | [Static methods](https://docs.python.org/3/library/functions.html#staticmethod); [Python class and instance objects](https://docs.python.org/3/tutorial/classes.html) | Why does math need explicit arguments while a calculation needs stored state? |
| 2 | [Factory comparison](https://refactoring.guru/design-patterns/factory-comparison), Simple Factory and Factory Method sections | Which responsibility moved out of the CLI, and does our creator use inheritance? |
| 3 | [Arbitrary arguments](https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists); [unpacking](https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists); [special parameters](https://docs.python.org/3/tutorial/controlflow.html#special-parameters) | When does `*` collect and when does it unpack? Why name a setting? |
| 4 | [Command](https://refactoring.guru/design-patterns/command), intent and structure; [abc](https://docs.python.org/3/library/abc.html) | How does a stored application action differ from stored math? What does ABC enforce? |
| 5 | [Series.std](https://pandas.pydata.org/docs/reference/api/pandas.Series.std.html); [read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) | Which defaults need an explicit application policy? |
| 6 | [Exceptions](https://docs.python.org/3/tutorial/errors.html); [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) | Where can a caller recover, and what test establishes continuation? |
| After the examples | [What is a pattern?](https://refactoring.guru/design-patterns/what-is-pattern); [classification](https://refactoring.guru/design-patterns/classification) | Is the problem about creation, structure, or behavior? |

Use the reading's original diagrams for comparison, then draw your own request trace. Write problem → responsibilities → application example → benefit → cost. Pattern sources are supplementary comparisons; official Python/pandas documentation defines language and library behavior.

Documentation can describe a newer version than your installed package. Check the course dependency bounds and reproduce a behavior locally before relying on a default. Use [error handling](error-handling.md) for the optional benchmark discussion and [language transfer](language-transfer.md) after the application is familiar.
