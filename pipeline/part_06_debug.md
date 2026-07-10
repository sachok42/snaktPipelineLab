# Step 5 — Debug and Clean

**Agent role:** Debugger  **Model:** Sonnet

## Input (iteration-aware)

- **Iteration 1:** read the consolidated feedback from Step 4.
- **Iteration 2+:** read `debug/<feature-id>-delta-iter-<N-1>.md` — the delta document
  produced by the previous Step 5 iteration. Do not re-read the original Step 4
  consolidation — it describes the original implementation, not the current state of the fork.

## Execution

Apply targeted fixes to the fork based on the input document.
Each fix is minimal — no unrelated cleanup or refactoring beyond what the input requires.
Unresolved conflicts carried over from Step 4 must be explicitly addressed (even if the
resolution is "deferred with justification").

After fixes are applied, strip TODO-style comments from the changed files: anything that
reads like an unfinished note, a placeholder, or a reminder to self. Functional comments
explaining *why* (non-obvious constraints, invariants) are kept.
Stripping is a sub-task of this step, not a reason to spawn a separate agent.

## Delta Document

After every iteration, produce a delta document recording:
- What was fixed (reference the input item by its Section 4 number or prior delta item ID)
- What remains broken or unresolved, and why
- Any new problems observed that were not in the input

The delta document is the sole input for the next debug iteration if the gate does not pass.

**Output:** Updated, cleaned implementation committed to the fork
+ delta document written to `debug/<feature-id>-delta-iter-<N>.md`
+ handoff record (`handoffs/<feature-id>-step-5-iter-N.md`)
+ completion marker (`complete/<feature-id>-step-5-iter-N.md`).
