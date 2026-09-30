# The bigger picture

Your earlier calculator packaged two operands and a calculation. Here a command packages a request with a variable-length collection or a file path. The CLI is an explicit invoker. Queues, undo, and a separate receiver object are possible Command extensions, not requirements for this small exercise.

Simple Factory makes selection visible and centralized. It does not become formal Factory Method merely because its method is called create(). Choose terminology that matches the actual relationship.

Single responsibility keeps input, calculation, construction, and presentation separate. A shared execute() contract supports substitution only when both implementations honor the promised behavior: numeric output or useful input/file errors. The factory still changes when a new input source is added; do not claim the entire application is closed to modification.

The old History display assumed a and b. A variable-length statistic cannot satisfy that assumption unchanged. Design transfer includes recognizing contracts that need revision, not forcing new features into old classes.

Explain how you would add a JSON input command. Identify changes to construction, prompts, and tests. Then explain how the same objects could be called by a web interface without putting terminal input inside commands.
