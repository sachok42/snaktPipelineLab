# Step 2 — Implement the Feature

**Agent role:** Yuki (Implementer)  **Model:** Opus

Implement the feature on the fork. This includes:
- Compiler/plugin changes inside SnaKt as needed
- New Kotlin contract API surface (annotations, functions, DSL blocks)
- At minimum one working usage example

The implementation must compile cleanly via `./gradlew build`.

## API Surface Document

Before finishing, the Implementer must write an API surface document to the artifact
repository at `surface/<feature-id>-api.md`. It must enumerate:
- Every public annotation added, with its parameters and intended semantics
- Every public function or DSL entry point added, with its signature
- Any compiler/plugin behavior changes visible to callers

This document is the authoritative input for Amara's (Testing Strategist) solver dispatch
in Step 3. Solvers must not be briefed without it.

**Output:** Working implementation on the fork branch + `surface/<feature-id>-api.md`
+ handoff record (`handoffs/<feature-id>-step-2.md`)
+ completion marker (`complete/<feature-id>-step-2.md`).
