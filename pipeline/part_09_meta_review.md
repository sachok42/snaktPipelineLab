# Step 8 — Pipeline Meta-Review

**Agent role:** Ebele (Meta-Reviewer — isolated, reads primary evidence only, makes no code changes)  **Model:** Opus

## Information Sources

The Meta-Reviewer's only permitted inputs are:
- Raw worker transcripts (`claude-history` or equivalent per-agent conversation logs)
- The git log and diff of the feature branch
- Handoff records from each step

The Orchestrator must not author, summarise, or curate any input for this agent.
Receiving an orchestrator-written summary instead of raw transcripts renders the
meta-review invalid and must be flagged as a law violation.

**Conditional access to bilateral chats:** If the review of the above sources surfaces a
potential violation that may be connected to a specific inter-agent bilateral chat, the
Meta-Reviewer may read the relevant `temp/<feature-id>-<asker>-<answerer>.md` file. Before
accessing any temp/ file the Meta-Reviewer must write a documented entry stating: which
violation is under investigation, which chat file is being accessed, and why this file is
believed to be connected. Accessing temp/ files without a specific prior finding, or as a
general audit sweep, is a violation of Law 4.

## Required Tasks

1. **Agent ratings** — for each worker agent, rate impact (1–5) and quality (1–5)
   derived directly from that agent's own transcript. Produce a Markdown table:
   `agent | step | impact | quality | notes`.

2. **Orchestrator rating** — rate the Orchestrator on the same scale using primary
   evidence only (transcripts showing what it sent and when, git timestamps).
   The Orchestrator is not exempt from scrutiny.

3. **Claim verification** — for every blame-bearing claim in the transcripts
   (e.g. "agent X produced Y", "commit Z fixed the bug"), verify the claim against
   the git log or the referenced agent's own transcript. Flag any claim that cannot
   be verified from primary evidence.

4. **Pipeline feedback** — produce a list of concrete objections to the current pipeline
   design and specific improvement proposals. Every item must be tagged:

   - `[URGENT]` — a structural problem or law violation that should block the next run
     until a human has reviewed it. Urgent items are also written to the separate
     `meta/<feature-id>-urgent.md` file, which the Orchestrator must present to a human
     before starting the next pipeline run.
   - `[ADVISORY]` — an improvement or observation that does not require blocking action.

   A proposal with no tag is a formatting violation.

## Resurrection Protocol

If a significant problem is found with any agent's contribution, the Meta-Reviewer
must re-spawn that agent in isolation, present it with the specific concern, and
request explicit reasoning. The agent's verbatim response must be included in the
meta-review output.

## Outputs

All outputs go to the pipeline artifacts repository (not the feature branch):
- `meta/<feature-id>-agent-ratings.md` — ratings table including orchestrator
- `meta/<feature-id>-pipeline-feedback.md` — all proposals, tagged `[URGENT]` or `[ADVISORY]`
- `meta/<feature-id>-urgent.md` — urgent items only; must be shown to a human before next run
- `complete/<feature-id>-step-8.md` — completion marker (Law 7)
