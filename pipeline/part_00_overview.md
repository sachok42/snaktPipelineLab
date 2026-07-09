# SnaKt Feature Development Pipeline

A structured, multi-agent workflow for implementing missing SnaKt features, validating them
against real VerifyThis problems, and iterating to correctness.

Each run starts from an operator-provided feature brief (feature ID/name, scope, and constraints).

---

## Overview

Each run of the pipeline targets **one missing feature** (e.g. F1 Loop Variants).
If the feature is large, it is split into self-contained pieces and the full pipeline
runs for each piece independently before moving on.

Every step is handled by a **dedicated agent**. No agent doubles up on steps.

```
Before Step 0 → bind and initialise artifact repository; bind or request execution repository
Step 0 → receive feature brief → ask/resolve unclear points → oracle search → select community cases / split into pieces
Step 1 → fork the repository
Step 2 → implement + publish API surface doc
Step 3 → testing strategist selects ≥2 methods; dispatch phase 1 (V/A/B/N), then phase 2 (M after baseline)
Step 4 → consolidate feedback (per-method calibration + cross-method synthesis)
Step 5 → debug + strip comments → produce iteration delta
Step 6 → review (better/worse?) + artifact provenance + binary gate (loops ≤5× to Step 5)
Step 7 → final review report
Step 8 → pipeline meta-review (raw transcripts only, urgency-tagged proposals)
```

---

## Runtime Model

**Soren** (the Orchestrator) is the head LLM agent. Soren is responsible for spawning worker
LLM agents, tracking their handoffs, enforcing laws, and deciding whether to continue, pause,
salvage, or respawn. The laws are operational instructions for Soren, not requirements for a
separate executable harness unless the operator provides one.

---

## Iteration Limit

The debug loop (Steps 5 → 6) runs at most **five times** per piece.
If five iterations are exhausted without a passing gate check, Steps 7 and 8 still run,
and the final report must state:

> "Feature `<id>` did not reach a passing gate after 5 debug iterations."

---

## Model Assignment

Each step runs on a designated model tier. Using a heavier model than assigned is wasteful;
using a lighter model than assigned is a briefing violation.

| Step | Name | Role | Tier | Rationale |
|------|------|------|------|-----------|
| — | Soren | Orchestrator | — | Head agent; spawns, tracks, enforces |
| 0 | Mira | Planner | Haiku | Clarification pass + oracle search + simple selection/decomposition |
| 1 | Tomás | Repo Setup | Haiku | Mechanical — fork and record a URL |
| 2 | Yuki | Implementer | Opus | Hard compiler/plugin generation |
| 3 | Amara | Testing Strategist | Sonnet | Analysis + dispatch decisions |
| 3 | *(method-specific)* | Solver (first per method) | Opus | Best chance of a correct baseline |
| 3 | *(method-specific)* | Solver (second per method) | Sonnet | Find what Opus missed — not repeat it |
| 3 | *(method-specific)* | Solver (third per method) | Sonnet | Adversarial third perspective |
| 4 | Dawa | Synthesizer | Sonnet | Structured aggregation of solver reports |
| 5 | Ren | Debugger | Sonnet | Targeted fixes from a defined issue list |
| 6 | Valentina | Comparator | Sonnet | Comparison judgment + binary gate |
| 7 | Marcus | Reviewer | Sonnet | Report writing from known artifacts |
| 8 | Ebele | Meta-Reviewer | Opus | Deep judgment over all evidence |

Solver names vary by method (V, A, B, N, M) and slot index. See the canonical slug table in Law 17 for the complete roster.

---

## Handoff Records

Every step must write a handoff record before it finishes. This is the chain of custody
for the pipeline run. Format (`handoffs/<feature-id>-step-N.md`):

```
Step:      N — <name>
Agent:     <role>
Artifacts: <artifact repository root>
Produced:  <artifact paths and/or commit hashes>
Caveats:   <anything the next agent must know>
Passing to: Step N+1
```

The receiving agent must read the handoff record before starting work.
A step that begins without reading the previous handoff record is in briefing violation.

---

## Artifact Location

Pipeline artifacts (review reports, meta-review outputs, solver specs, handoff records)
must **not** live on the feature branch. They go to a dedicated orphan branch or the
examples repository. Committing pipeline artifacts to the feature branch is a briefing violation.

Before Step 0 starts, the Orchestrator must bind a concrete artifact root and initialise it:

```
python tools/artifacts.py init --root "<artifact-repo-path>"
```

All artifact paths in this document are relative to that root. The artifact root must be
included in every handoff record. Once Step 1 has created the feature fork, Repo Setup must
validate that artifacts are outside the feature repository:

```
python tools/artifacts.py validate --root "<artifact-repo-path>" --feature-repo "<feature-repo-path>"
```

## Repository Preflight

Before Step 0 starts, the Orchestrator must bind the repository context that the pipeline
will operate on. If the operator has not provided an existing SnaKt repository path or fork
source, the Orchestrator asks for it before proceeding.

When a local repository path is provided, the Orchestrator checks:

```
git -C "<repo-path>" rev-parse --is-inside-work-tree
```

If the path is not a git repository, the Orchestrator must ask the operator whether to:
- provide a different repository path,
- clone/fork from a remote URL, or
- initialise the provided directory with `git init`.

The Orchestrator must not run `git init` silently. The question, answer, and chosen action
are recorded in `intake/<feature-id>-clarifications.md`.

---

## File Conventions

| Path (artifact repo) | Contents |
|---|---|
| `intake/<feature-id>-clarifications.md` | Step 0 clarification log: questions asked, answers received, unresolved items, fallback decisions |
| `complete/<feature-id>-step-N.md` | Normal-completion marker written by each step (Law 7 tripwire) |
| `incidents/<feature-id>-step-N.md` | Incident record for unexpected events (Law 7) |
| `incidents/orchestrator-violations.md` | Append-only worker reports about Orchestrator law violations (Law 8) |
| `salvage/<feature-id>-step-N.md` | Salvage record when a replacement agent is briefed from partial work (Law 15) |
| `search/<feature-id>-candidates.md` | Oracle search results (Step 0) |
| `testing/<feature-id>-strategy.md` | Method verdicts + solver dispatch plan (Step 3) |
| `testing/<feature-id>-insufficient.md` | Pause record when <2 methods applicable (Step 3) |
| `handoffs/<feature-id>-step-N.md` | Handoff record for step N |
| `surface/<feature-id>-api.md` | API surface doc produced by Implementer (Step 2) |
| `testing/<feature-id>-solver-<METHOD>-<INDEX>.md` | Structured solver report, one per solver (Step 3); e.g. `solver-v-1`, `solver-a-2` |
| `debug/<feature-id>-delta-iter-<N>.md` | Delta document produced by each Debugger iteration (Step 5) |
| `reviews/<feature-id>.md` | Final review report (Step 7) |
| `meta/<feature-id>-agent-ratings.md` | Agent + orchestrator ratings table (Step 8) |
| `meta/<feature-id>-pipeline-feedback.md` | Pipeline improvement proposals (Step 8) |
| `meta/<feature-id>-urgent.md` | Urgent items requiring human attention before next run (Step 8) |
| `temp/<feature-id>-<asker-role>-<answerer-role>.md` | Bilateral private chat between two named agents (Law 17); readable only by the two parties and the Meta-Reviewer |
