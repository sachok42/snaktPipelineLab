# Pipeline Agent Roster

## Orchestrator

| Role | Model |
|------|-------|
| Orchestrator | — |

## Step Agents

| Step | Role | Model |
|------|------|-------|
| 0 | Planner | Haiku |
| 1 | Repo Setup | Haiku |
| 2 | Implementer | Opus |
| 3 | Testing Strategist | Sonnet |
| 4 | Synthesizer | Sonnet |
| 5 | Debugger | Sonnet |
| 6 | Comparator | Sonnet |
| 7 | Reviewer | Sonnet |
| 8 | Meta-Reviewer | Opus |

## Solvers (Step 3)

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
| M — Mutation Testing | 1 | Opus | `solver-m-1` |
| M — Mutation Testing | 2 | Sonnet | `solver-m-2` |
| M — Mutation Testing | 3 | Sonnet | `solver-m-3` |
