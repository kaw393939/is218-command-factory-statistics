# Record a prediction, a change, and its evidence

Keep a short entry for each checkpoint. The prerequisite already gave you a working design; record what each new requirement changes rather than describing every class as new.

| Prompt | Useful evidence |
| --- | --- |
| What do I already know here? | Earlier class/method/test that supplies the starting point |
| What do I predict? | Inputs, returned value/type, exception, or state before running |
| What happened? | Exact call or request and observed behavior |
| What assumption changed? | Explanation of the mismatch, if any |
| How does control move? | Values, calls, returns, ownership, and skipped statements |
| Why introduce this component? | Requirement it serves and extra complexity it adds |
| What stays valid? | Earlier behavior and regression assertion retained |
| What would a changed requirement affect? | First component to inspect and why |
| What do my tests establish? | Assertion and one relevant case still unverified |

## Retrieval prompts across the six parts

1. Compare a previous calculation subclass with a stored operation. Explain callable versus call.
2. Trace factory creation without performing math. Identify its returned object.
3. Expand one `*values` and one `**options` call by hand. Explain operand versus setting.
4. Trace a history action and a failed calculation. Explain why state differs.
5. Follow a CSV column into the same statistic as typed values. Name the missing-value policy.
6. Explain one adaptation without looking at the worked solution. Record the submitted commit and the checks for that revision.

A log saying only “tests passed” omits the claim. Write what the test established and how it would detect a plausible bug. Keep entries brief enough to revisit while studying.

Record the instructor reference branch you inspected and your own solution commit separately. Compare neighboring reference branches to identify the teaching increment; your solution history records how you implemented and tested that change.
