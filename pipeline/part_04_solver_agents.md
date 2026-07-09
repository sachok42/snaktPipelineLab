# Step 3 — Testing Strategy and Solver Dispatch

**Agent role:** Amara (Testing Strategist)  **Model:** Sonnet

## Testing Method Catalog

The Testing Strategist evaluates each method below against the feature at hand.
New methods may be added to this catalog by a human operator only — the Testing Strategist
must not invent methods outside this list.

### Method V — VerifyThis Problems
Applicable when there are open VerifyThis problems whose solution requires this feature.
Evidence must be explicit: specific problem names or oracle search results showing a connection.
Not applicable by default — requires positive evidence.

### Method A — Feature Contract
Applicable when the feature has well-defined behavioral properties expressible as testable
invariants (e.g. "programs of shape X must now compile", "invariant Y must always hold",
"interaction with feature Z must behave as follows").
Almost always applicable for language features with clear semantics.
The contract is derived from the API surface document (`surface/<feature-id>-api.md`).

### Method B — Community Cases
Applicable when the Step 0 oracle search produced at least one directly relevant result
(a reported limitation, a workaround pattern, or a pain point this feature removes).
Evidence: `search/<feature-id>-candidates.md` must contain relevant entries.
Not applicable if the oracle search returned no relevant results.

### Method N — Negative / Should-Fail Tests
Applicable to any feature that changes what the verifier accepts or rejects.
Solvers write programs that *intentionally* misuse the feature or violate its contracts,
then verify that the tool correctly rejects them. A method N pass means the verifier
catches the error; a method N fail means the verifier accepted something it should not —
a soundness gap. Almost always applicable for language features with well-defined
error conditions.

### Method M — Mutation Testing
Applicable when at least one passing verified program exists for this feature (produced
by any other method). Solvers introduce small semantic mutations into that program
(off-by-one, swapped operator, dropped invariant, weakened precondition) and check that
the verifier kills the mutant. A surviving mutant means the contracts are too weak to
detect the change. Applicable only after at least one other method has produced a
verified baseline — not applicable if no passing program exists yet.

---

## Applicability Analysis

The Testing Strategist reads the API surface document and the oracle search results, then
produces a written verdict for every method in the catalog:

- **Applicable** — with specific evidence (problem names, contract properties, community URLs)
- **Not applicable** — with justification

The verdict document is written to `testing/<feature-id>-strategy.md` before any solvers
are spawned. It must list every catalog method, not just the ones selected.

---

## Minimum Requirement and Pause Protocol

At least **two** methods must be applicable. If the analysis yields fewer than two:

1. Write `testing/<feature-id>-insufficient.md` listing every method evaluated and the
   reason each was rejected.
2. **Pause the pipeline** and surface the file to the operator.
3. Do not spawn any solver agents.
4. Resume only when the operator provides at least one additional method. The operator
   may either supply a new catalog entry (added to this step's catalog by amending the
   pipeline) or provide a one-off method brief directly in the resume instruction.

---

## Solver Dispatch

Solver dispatch is two-phase:

- **Phase 1:** run all applicable methods except M (`V`, `A`, `B`, `N`) in parallel.
- **Phase 2:** run method `M` only after at least one passing verified baseline exists from
  Phase 1.

For each applicable method, Amara spawns **2–3 independent solver agents** powered by
different models where possible. The first solver per method runs on Opus; the second and
third run on Sonnet. Each method has its own named trio:

| Method | 1st (Opus) | 2nd (Sonnet) | 3rd (Sonnet) |
|--------|-----------|-------------|-------------|
| V — VerifyThis | Aleksei | Selin | Nikos |
| A — Feature Contract | Finn | Priya | Lior |
| B — Community Cases | Ingrid | Jae | Mei |
| N — Negative Tests | Tariq | Zara | Mateus |
| M — Mutation Testing | Sofía | Kwame | Linh |

Each solver receives:

- `surface/<feature-id>-api.md` — what the feature exposes
- The method brief specific to their assigned method:
  - **V:** explicit problem assignment — unique primary problems per solver plus one
    shared calibration problem assigned to all V-solvers for cross-solver comparison
  - **A:** the full set of contract properties to exercise, adversarially where possible
  - **B:** the selected community case URLs and descriptions from Step 0
  - **N:** explicit negative-test plan including:
    - misuse classes to test (at least three, feature-specific)
    - expected failure mode per case (compile error and/or verifier rejection)
    - minimum number of should-fail programs the solver must produce
  - **M:** explicit mutation plan including:
    - exact baseline program commit hash chosen for mutation
    - allowed mutation operators for this run
    - maximum mutants to produce
    - required expectation: every mutant should fail verification

Phase 1 methods run in parallel.
Solvers within the same method run independently and must not share intermediate results.
Method M solvers run only in Phase 2 after a baseline is confirmed.

## Commit Policy

All solver agents must commit every attempt to the fork — including non-verifying ones —
marked `[UNVERIFIED]`. Deleting a failed spec before committing is a briefing violation (Law 12).

## Solver Report Schema

Every solver must write its report using exactly this structure. Free-form prose reports
are a briefing violation — the Synthesizer reads structured data, not narratives.

```
## Solver Report: <METHOD>-<INDEX>
Method:    <V | A | B | N | M>
Model:     <model id used>
Verified:  <count>
Unverified: <count>

### Issues
| ID | Description | Severity | Evidence |
|----|-------------|----------|---------|
| <method>-<index>-<n> | <one line> | critical / major / minor / info | <commit hash or file:line> |

### Verified Programs
- <commit hash> — <one-line description>

### Unverified Attempts
- <commit hash> [UNVERIFIED] — <one-line description> — <reason failed>

### Notes
<free-form, 150 words max>
```

Severity definitions:
- **critical** — soundness gap or verifier crash
- **major** — feature does not work for its primary use case
- **minor** — rough edge, workaround exists
- **info** — observation with no actionable fix yet

**Output:** `testing/<feature-id>-strategy.md` + one structured report per solver at
`testing/<feature-id>-solver-<METHOD>-<INDEX>.md` + all attempts committed
+ handoff record (`handoffs/<feature-id>-step-3.md`)
+ completion marker (`complete/<feature-id>-step-3.md`).

**Completion marker ownership:** Soren writes `complete/<feature-id>-step-3.md`, not Amara.
Amara's own work is done when the strategy document is written and solvers are dispatched,
but Step 3 is not complete until: (a) all Phase 1 solvers (V/A/B/N) have each written their
solver report, and (b) if Method M was applicable, all Phase 2 solvers have also written their
reports. Soren monitors for all expected `testing/<feature-id>-solver-*.md` files and writes
the step-3 completion marker only when every dispatched solver has delivered its report.
