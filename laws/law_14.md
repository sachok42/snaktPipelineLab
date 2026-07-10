# Law 14 — Use Bilateral Chat for Direct Q&A

**Recipients:** All agents

Agents may communicate directly with one another through bilateral chat files in the `temp/` directory of the artifact repository. These chats bypass the Orchestrator and are for Q&A under Law 13 only.

## File Naming

    temp/<feature-id>-<asker-role>-<answerer-role>.md

`<asker-role>` and `<answerer-role>` are the canonical role slugs below. The asker initiates the question; the answerer is the one being asked. Both parties append to the same file using labeled turns.

## Canonical Role Slugs

| Step | Role | Slug |
|------|------|------|
| — | Orchestrator | `orchestrator` |
| 0 | Planner | `planner` |
| 1 | Repo Setup | `repo-setup` |
| 2 | Implementer | `implementer` |
| 3 — strategist | Testing Strategist | `strategist` |
| 3 — V-1 | Solver V first | `solver-v-1` |
| 3 — V-2 | Solver V second | `solver-v-2` |
| 3 — V-3 | Solver V third | `solver-v-3` |
| 3 — A-1 | Solver A first | `solver-a-1` |
| 3 — A-2 | Solver A second | `solver-a-2` |
| 3 — A-3 | Solver A third | `solver-a-3` |
| 3 — B-1 | Solver B first | `solver-b-1` |
| 3 — B-2 | Solver B second | `solver-b-2` |
| 3 — B-3 | Solver B third | `solver-b-3` |
| 3 — N-1 | Solver N first | `solver-n-1` |
| 3 — N-2 | Solver N second | `solver-n-2` |
| 3 — N-3 | Solver N third | `solver-n-3` |
| 3 — M-1 | Solver M first | `solver-m-1` |
| 3 — M-2 | Solver M second | `solver-m-2` |
| 3 — M-3 | Solver M third | `solver-m-3` |
| 4 | Synthesizer | `synthesizer` |
| 5 | Debugger (per iteration) | `debugger-iter-<N>` |
| 6 | Comparator (per iteration) | `comparator-iter-<N>` |
| 7 | Reviewer | `reviewer` |
| 8 | Meta-Reviewer | `meta-reviewer` |

Use these slugs exactly. Inventing alternative names produces files that other agents cannot reliably identify.

## Message Format

Each turn must begin with:

    ## <Role> — <timestamp or turn label>
    <message text>

## Access Rules

- Read and write only the bilateral chat files in which your role slug appears as asker or answerer.
- **Orchestrator:** observe `temp/` file existence only (directory listing) to route re-invocations. Read no file contents.

## Scope

Use bilateral chats for clarification Q&A only. Sharing intermediate work products, solver results, or code through `temp/` to circumvent solver isolation is a violation.

## Lifecycle

`temp/` files are pipeline artifacts scoped to a single run. Keep them in the artifact repository until Step 8 completes.
