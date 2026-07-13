# Pipeline Agent Roster

## Orchestrator

| Role | Model |
|------|-------|
| Orchestrator | — |

## Step Agents

| Step | Role | Model |
|------|------|-------|
| 1 | Planner | Haiku |
| 2 | Implementer | Opus |
| 3 | Testing Strategist | Sonnet |
| 4 | Solver Dispatcher | Sonnet |
| 5 | Synthesizer | Sonnet |
| 6 | Debugger | Sonnet |
| 7 | Comparator | Sonnet |
| 8 | Reviewer | Sonnet |
| 9 | Meta-Reviewer | Opus |

## Solvers (Step 4)

First solver per method runs on Opus; second and third run on Sonnet.
Solvers within the same method must not share intermediate results.

| Method | Index | Model | Slug |
|--------|-------|-------|------|
| V — VerifyThis Problems | 1 | Opus | `solver-v-1` |
| V — VerifyThis Problems | 2 | Sonnet | `solver-v-2` |
| V — VerifyThis Problems | 3 | Sonnet | `solver-v-3` |
| A — Feature Contract | 1 | Opus | `solver-a-1` |
| A — Feature Contract | 2 | Sonnet | `solver-a-2` |
| A — Feature Contract | 3 | Sonnet | `solver-a-3` |
| B — Community Cases | 1 | Opus | `solver-b-1` |
| B — Community Cases | 2 | Sonnet | `solver-b-2` |
| B — Community Cases | 3 | Sonnet | `solver-b-3` |
| N — Negative Tests | 1 | Opus | `solver-n-1` |
| N — Negative Tests | 2 | Sonnet | `solver-n-2` |
| N — Negative Tests | 3 | Sonnet | `solver-n-3` |
