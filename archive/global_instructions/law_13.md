# Law 13 — Ask When Information Is Missing

**Recipients:** All agents

This law applies when you cannot locate a specific artifact, datum, or instruction that was supposed to exist — for example, a missing handoff record, an unwritten API surface doc, or a problem that was never named. It does not apply to judgment calls between two valid options — those are yours to decide and document.

**Escalation chain:**
- Ask the agent that gave you this specific task, using the bilateral chat channel (Law 14). Do not skip levels and ask the Orchestrator directly.
- If they cannot answer, they escalate upward through the same mechanism to their own task-giver, and so on.
- The Orchestrator that cannot answer asks the operator and waits for a response.

When pausing to wait: write a completion marker reading `PAUSED — awaiting response from <role> at temp/<file>`.

**If one full escalation cycle passes without a response:** document the unanswered question in an incident record (Law 6), take the most conservative safe action available, and flag the decision prominently in your handoff record.

State the question, any answer received, and any fallback taken in your transcript.
