# Law 8 — Respawn Protocol

**Recipients:** Orchestrator

When an agent appears dead, follow these steps in order before spawning a replacement:

**Step 1 — Verify the agent is actually dead.** Run a liveness check: confirm whether the process is alive and whether a tool call is in flight. Base the decision on a direct check only — manifest modification time is not a valid proxy for long single-turn builds.

**Step 2 — Attempt salvage.** Read the dead agent's outputs from newest to oldest: committed artifacts first, then final text outputs in reverse chronological order. Stop reading when you have enough context for a meaningful resume brief — what was completed, what remains, and what the next action should be. Read only final text outputs (messages, reports, structured files) and committed artifacts — skip thinking blocks and internal reasoning. Write a salvage record to `salvage/<feature-id>-step-N.md`.

**Step 3 — Brief the replacement from the salvage record.**
