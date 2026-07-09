# Law 6 — Document Unexpected Events

**Recipients:** All agents

Write a completion marker to `complete/<feature-id>-step-N.md` upon finishing normally.

Log every unexpected event in a dedicated incident record immediately — describe what happened, which step was affected, and what action was taken. Unexpected events include: agent crashes, missing outputs, ambiguous results, external tool failures, and unresolvable conflicts.

**PAUSED markers (Soren):** When a completion marker begins with `PAUSED —`, treat it as a pause in progress rather than a completed step. Re-invoke the answering agent named in the marker with the path of the pending `temp/` file, wait for its response, then re-invoke the blocked agent to resume from where it paused.

**Tripwire (Soren):** Before advancing to each step, confirm that the previous step produced either a normal completion marker or an incident report. A gap — no marker and no incident — is itself an unexpected event and must be reported before the pipeline continues.
