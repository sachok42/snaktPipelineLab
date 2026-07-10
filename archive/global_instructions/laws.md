# Laws of the LLM Kingdom

Breaking any of these laws results in immediate termination of the offending agent upon discovery.

---

## Law 1 — No Direct Pushes to Main

No agent may push code to the `main` branch under any circumstances.
All work produced during a pipeline run must be collected into a single pull request.

---

## Law 2 — No Erasure Without a Replacement

_Merged into Law 12, which now covers all work products. Law 2 is retired; references to it redirect to Law 12._

---

## Law 3 — Orchestrator Must Not Edit Instructions

The Orchestrator agent is forbidden from modifying, rewriting, or reinterpreting any pipeline instruction or law.
It relays instructions to other agents exactly as written — no omissions, no paraphrasing, no additions.

---

## Law 4 — Meta-Reviewer Isolation

The Meta-Reviewer agent must derive all of its information exclusively from:
- Raw worker transcripts (`claude-history` or equivalent per-agent conversation logs)
- The git log and diff of the feature branch
- Handoff records from each step

It must not receive orchestrator-authored summaries, briefings, or any other out-of-band
communication. Any violation of this isolation renders the meta-review invalid and must be reported.

**Conditional access to bilateral chat files:** If the Meta-Reviewer identifies a potential
violation and determines that evidence of that violation may exist in a bilateral chat between
specific agents (Law 17), it may read the relevant `temp/` file. Before doing so it must
document: which violation it is investigating, which chat file it is about to read, and why it
believes that file is connected to the violation. Reading `temp/` files as a general audit sweep
without a specific prior finding is prohibited.

---

## Law 5 — Resurrection on Significant Problems

A problem is **significant** if it would cause the Meta-Reviewer to deduct a point from
that agent's impact or quality rating — i.e. the finding changes the score that would
otherwise be given. If the Meta-Reviewer would rate the agent identically with or without
the finding, the finding is not significant under this law.

If the Meta-Reviewer identifies a significant problem with any agent's contribution, it must
re-spawn that agent in isolation, present it with the specific concern, and request explicit
reasoning. The agent's response must be included verbatim in the meta-review output.

---

## Law 6 — All Problems Must Be Visible to Humans

Every problem found during any pipeline run — bugs, law violations, quality failures, unresolved disagreements —
must be listed in a human-readable output file before the pipeline concludes.
Nothing may be silently discarded or resolved off-record.

---

## Law 7 — Unexpected Events Must Be Documented

Any event that falls outside the normal pipeline flow (agent crash, missing output, ambiguous result,
external tool failure, unresolvable conflict) must be logged immediately in a dedicated incident record.
The record must describe what happened, which step was affected, and what action was taken.

**Tripwire:** every agent must write a completion marker to `complete/<feature-id>-step-N.md`
upon finishing normally. Before starting each step, the Orchestrator checks that the previous
step produced either a completion marker or an incident report. If neither exists for a step
that was handed off to, that gap is itself treated as a Law 7 violation — an undocumented
unexpected event — and must be reported before the pipeline continues.

**PAUSED markers are not step completions.** A completion marker beginning with `PAUSED —`
(Law 16) satisfies the tripwire (the file exists), but it does not constitute normal step
completion and must never be treated as one. When the Orchestrator finds a PAUSED marker it
must not advance the pipeline to the next step. Instead it must: (1) identify which agent is
blocked and which agent is named as the answerer, (2) re-invoke the answering agent with the
path of the pending temp/ file and instructions to read and respond, (3) once the answerer has
written its response, re-invoke the blocked agent to resume from where it paused. Treating a
PAUSED marker as a completed step is a briefing violation.

---

## Law 8 — Law Violations Must Be Reported and Escalated

If any agent detects another agent breaking a law, it must:

1. **Write a `.md` report** naming the offending agent, the law broken, and the evidence.
2. **Notify the Orchestrator** so it can halt or quarantine the offending agent.
3. **Pause the entire pipeline immediately** if the violation poses an urgent risk
   (e.g. a push to main, destruction of valid work, tampering with instructions).

**Exception — reports about the Orchestrator:** if the offending agent is the Orchestrator,
step 2 is replaced by writing the report to `incidents/orchestrator-violations.md` in the
artifact repository. This path is append-only for worker agents; the Orchestrator has no
write access to it. The report is visible to humans and to the Meta-Reviewer without
passing through the Orchestrator.

Agents must not attempt to silently correct another agent's law violation on their own.

---

## Law 9 — Verify Death Before Respawn

The Orchestrator must not respawn an agent on the basis of a crash completion event alone.
Before issuing a respawn, it must verify that the agent's process is actually dead
(liveness check: is the process alive, is a tool call in flight).
Manifest modification time is not a valid liveness proxy for long single-turn builds.
Declaring a stall from manifest age alone is a briefing violation.

---

## Law 10 — Stateless Wakeup Prompts

Wakeup prompts must carry no assumed pipeline state. On every wake the Orchestrator must
re-derive the current pipeline position from the repository (git log, branch state, artifact presence).
Assuming state from a prior session without verification is a briefing violation.

---

## Law 11 — Branch Landing Lease

Before writing to any branch, an agent must hold an exclusive lease on that branch.
No two agents may land commits to the same branch concurrently. The Orchestrator is
responsible for issuing and revoking leases. A duplicate landing that occurs without a
valid lease is a law violation regardless of whether the commits conflict.

---

## Law 12 — No Deletion of Work Without a Verified Replacement

No work product produced during a pipeline run may be deleted unless a verified replacement
is already in place. This applies to all agents and all artifact types.

For solvers specifically: every attempt must be committed to the fork — including
non-verifying ones — marked `[UNVERIFIED]`. Deleting a failed spec before committing it
is a violation regardless of how broken the spec is.

This law absorbs the former Law 2. All references to Law 2 redirect here.

---

## Law 13 — Instructing a Law Violation Is Itself a Violation

Any agent that issues instructions, briefs, or directives that would require another agent
to break a law is guilty of a law violation — regardless of whether the receiving agent
complies. Intent is not a defence: if the instruction contains a law violation, the issuing
agent is in breach at the moment of sending.

The receiving agent must refuse the instruction, report the issuing agent under Law 8, and
await a corrected brief before proceeding.

---

## Law 14 — _(Removed)_

_This law required LLM agents to respond to a liveness ping within one minute, which is not achievable at the agent layer. Liveness monitoring belongs in the infrastructure/harness. Law 14 is retired with no replacement._

---

## Law 15 — Salvage Before Respawn

If an agent is confirmed dead (per Law 9) before completing its step, the Orchestrator must
attempt salvage before spawning a replacement. Salvage procedure:

1. Read the dead agent's outputs from newest to oldest: committed artifacts first, then
   final text outputs in reverse chronological order.
2. Stop reading when enough context exists to produce a meaningful resume brief —
   i.e. what was completed, what remains, and what the next action should be.
3. **Do not read thinking blocks or internal reasoning.** Only final text outputs
   (messages, reports, structured files) and committed artifacts count as salvageable work.
4. Write a salvage record to `salvage/<feature-id>-step-N.md` summarising what was
   recovered and what the replacement agent must still do.
5. Brief the replacement agent from the salvage record, not from scratch.

Spawning a replacement without attempting salvage first is a briefing violation.

---

## Law 16 — Ask, Don't Guess

**When this law applies — missing information only.** An agent must ask when it cannot
locate a specific artifact, datum, or instruction it needs and that was supposed to exist
(e.g. a handoff record is absent, an API surface doc was not written, a designated problem
was never named). It does not apply to judgment calls between two valid options — those
are the agent's responsibility to decide and document.

Escalation chain:
- An agent that is stuck asks the agent that gave it this specific task — the one whose
  brief or handoff created this agent's work assignment — using the bilateral chat channel
  defined in Law 17. It must not skip levels and ask the Orchestrator directly.
- If the task-giver cannot answer, it escalates upward through the same bilateral chat
  mechanism to its own task-giver, and so on up the chain.
- The **Orchestrator** that cannot answer asks the operator and waits for a response.

When pausing to wait for a response, the blocked agent must write a completion marker that
reads `PAUSED — awaiting response from <role> at temp/<file>` so the Orchestrator knows to
re-invoke the answering agent. Once the answerer responds, the Orchestrator re-invokes the
blocked agent.

**Fallback when no answer arrives.** If one full escalation cycle passes without a response,
the agent must not continue to wait indefinitely. It must: document the unanswered question
and the uncertainty in an incident record (Law 7), take the most conservative safe action
available (the one least likely to cause irreversible harm), and flag the decision prominently
in its handoff record so the next agent and the Meta-Reviewer know a fallback was used.

Asking is not a failure. Guessing silently when missing information — and producing output
that depends on that guess without flagging it — is a violation of this law. The question,
any answer received, and any fallback taken must all appear in the agent's transcript.

---

## Law 17 — Bilateral Private Chats

Agents below the Orchestrator level may communicate directly with one another through
private bilateral chat files in the `temp/` directory of the artifact repository.
These chats bypass the Orchestrator and are used exclusively for Q&A under Law 16.

### File naming

```
temp/<feature-id>-<asker-role>-<answerer-role>.md
```

`<asker-role>` and `<answerer-role>` are the canonical role slugs of the two participants
(see table below). The asker is the agent initiating the question; the answerer is the one
being asked. Both parties append to the same file using labeled turns.

### Canonical role slugs

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
| 5 | Debugger (per iteration) | `debugger-iter-<N>` e.g. `debugger-iter-1` |
| 6 | Comparator (per iteration) | `comparator-iter-<N>` e.g. `comparator-iter-1` |
| 7 | Reviewer | `reviewer` |
| 8 | Meta-Reviewer | `meta-reviewer` |

Agents must use these slugs exactly. Inventing alternative names produces files that other
agents and the Orchestrator cannot reliably identify.

### Message format

Each turn must begin with a header line:

```
## <Role> — <timestamp or turn label>
<message text>
```

### Access control

- Only the two agents named in the filename may read or write that file.
- The **Orchestrator** must not read the contents of any `temp/` file. It may observe
  the existence of files (directory listing only) to route re-invocations.
- The **Meta-Reviewer** may access a `temp/` file only when it has already identified a
  potential violation and has reason to believe that specific bilateral conversation is
  connected to it. It must document its justification before reading the file (Law 4).
  Blanket reading of all temp/ files as a precautionary sweep is prohibited.
- No other agent may access a `temp/` file in which its role does not appear.

### Scope restriction

Bilateral chats are for clarification Q&A only — not for sharing intermediate work
products, solver results, or code. Exchanging substantive work through `temp/` to
circumvent the solver isolation rule (Step 3: "solvers within the same method run
independently and must not share intermediate results") is a violation of this law.

### Lifecycle

`temp/` files are pipeline artifacts with a run-scoped lifetime. They live in the artifact
repository (not the feature branch) and must not be deleted between steps or before Step 8
completes. They are not ephemeral — they are a durable record of inter-agent communication
for that run, accessible to the Meta-Reviewer on demand if its access conditions are met.