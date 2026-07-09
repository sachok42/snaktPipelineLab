# Step 0 — Feature Selection

**Agent role:** Mira (Planner)  **Model:** Haiku

Before starting, verify that the Orchestrator has provided an artifact repository root
initialised by `tools/artifacts.py` and a repository context checked by the Repository
Preflight in the overview. All Step 0 outputs are written relative to the artifact root.

## 1 — Receive Feature Brief from Operator

Step 0 starts from a specific feature chosen by the operator before the run begins.
The brief must include at least:
- Feature ID/name
- Scope boundaries (what is in/out)
- Hard constraints (compatibility/performance/language constraints if any)

The Planner must not replace the feature with a different one.

## 2 — Clarification Pass (mandatory before proceeding)

Before any implementation planning or oracle search, the Planner must ask about every unclear
point that could change implementation or evaluation outcomes for this specific feature.

The clarification pass must produce `intake/<feature-id>-clarifications.md` containing:
- Questions asked
- Answers received
- Repository context selected by the operator
- Unresolved questions
- For unresolved questions: conservative fallback decision taken, with rationale

If a clarification is missing, follow Law 16 escalation and do not silently guess.

## 3 — Oracle Problem Search

Before any LLM reasoning about test cases, run the non-LLM oracle search tool:

```
python tools/search.py "<feature keywords>" --limit 10 --out search/<feature-id>-candidates.md
```

The tool queries GitHub Issues (JetBrains/Kotlin), Stack Overflow ([kotlin]), and JetBrains
YouTrack in parallel and produces a ranked candidate list with live URLs, scores, and dates.
The Planner must not fabricate or recall community problems from memory — every problem cited
in the output must appear in the oracle results file.

## 4 — Select Community Cases

From the oracle results, select 3–5 high-quality cases that directly relate to the limitation
this feature removes. Prefer cases with high community signal (votes, reactions, answer count).
Cap the search at 3–5 — exhaustive coverage is not the goal.

Each selected case must be cited by its exact URL from the oracle results file.

## 5 — Assemble the Step-0 Feature Brief

The output of this step is the feature brief passed to the Implementer. It must contain:
- Feature name + optional list of sub-pieces
- Clarification file path (`intake/<feature-id>-clarifications.md`)
- The oracle results file path (`search/<feature-id>-candidates.md`)
- The 3–5 selected community cases with URLs and a one-line description of each
- Any decomposition decisions and rationale

The selected community cases travel into Step 2 so the Implementer can ground the feature
contract in real usage patterns.

**Output:** Feature brief + `intake/<feature-id>-clarifications.md`
+ `search/<feature-id>-candidates.md` in the artifact repo
+ handoff record (`handoffs/<feature-id>-step-0.md`)
+ completion marker (`complete/<feature-id>-step-0.md`).
