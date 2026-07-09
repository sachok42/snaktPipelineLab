# Step 6 — Review and Gate Check

**Agent role:** Valentina (Comparator)  **Model:** Sonnet

## Part A — Better or Worse? (skipped on fast-path)

**Fast-path:** run Part C first. If all binary checks pass, skip Part A entirely and
emit a one-line acceptance record: `Accepted: all gate criteria passed at iteration N.`
Part A is only required when at least one criterion fails and a revert decision is needed.

When Part A runs: compares the post-debug implementation against the pre-debug version.
Decides which is strictly better. If the debugged version is better, it becomes the
new main version on the fork. If not, the pre-debug version is restored.

## Part B — Artifact Provenance

Before issuing a pass, verify that every published artifact (jar, compiled output, etc.)
was built from the current branch tip commit. Record the artifact's build commit hash and
the branch tip hash. If they differ, the diff between the two commits must be proven
behavior-free before a pass can be issued. A gap here is a gate failure.

## Part C — Binary Gate Check (max 5 iterations) — run first

The gate uses only hard binary criteria. "Meaningful" or subjective assessments are not
gate criteria — if it cannot be checked by a tool exit code, it does not belong here.

Required checks — all must pass:

1. **Build:** `./gradlew build` exits 0.
2. **Verifier:** if Method V (VerifyThis) was used in Step 3, the designated VerifyThis
   problem exits 0 under the project's verifier — the Orchestrator must name it in the
   run brief. If Method V was not used, this criterion is replaced by: at least one
   verified program from Method A or Method B exits 0 under the project's verifier.
3. **Regression:** every VerifyThis problem that passed in a prior iteration still passes.
   A newly failing previously-passing problem is an automatic gate failure regardless of
   other results.
4. **Negative checks (Method N):** if Method N was used in Step 3, no N-designated
   should-fail program may be accepted. Any accepted should-fail case is an automatic gate fail.
5. **Mutation checks (Method M):** if Method M was used in Step 3, mutant kill rate must be
   at least 80%. If Method M was deemed not applicable in the strategy document, the gate
   record must cite that verdict explicitly.
6. **Provenance:** artifact build commit equals branch tip (or diff proven behavior-free
   per Part B).

Gate decision:
- **All checks pass:** proceed to Step 7.
- **Any fail and iteration count < 5:** go back to Step 5. Append the gate failure record
  to `debug/<feature-id>-delta-iter-<N>.md` so Ren reads it as part of the delta input.
- **Any fail and iteration count = 5:** proceed to Step 7 with a convergence-failure flag.

**Output:** Decision (accepted / reverted) + provenance record + gate check results (per criterion)
+ iteration count + handoff record (`handoffs/<feature-id>-step-6-iter-N.md`)
+ completion marker (`complete/<feature-id>-step-6-iter-N.md`).
