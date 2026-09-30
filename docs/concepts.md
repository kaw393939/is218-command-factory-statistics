# Core concepts

An object combines state and behavior. A command stores the information needed for a request and exposes execute(). Polymorphism lets the invoker use the same method on either input source. An abstract base class states the required contract.

A Simple Factory chooses and constructs a concrete object. The CLI asks for one without importing every command class. Creation and execution remain separate.

A pandas DataFrame represents the CSV table; a Series represents its value column. Sample standard deviation divides by n-1. Specify ddof explicitly so the statistical policy is visible. Validate first: pandas otherwise skips missing values by default.

Keep one shared calculation function. Both commands delegate to it. The CLI owns prompting and formatting; commands own requests; the factory owns selection. Tests should assert observable results, rejected input, correct command types, and recovery after errors.
