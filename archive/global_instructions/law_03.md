# Law 3 — Meta-Reviewer Sources

**Recipients:** Orchestrator, Meta-Reviewer

Derive all meta-review information exclusively from primary sources:
- Raw worker transcripts (`claude-history` or equivalent per-agent conversation logs)
- The git log and diff of the feature branch
- Handoff records from each step

**For the Orchestrator:** Pass these primary sources directly to the Meta-Reviewer. Send raw transcripts, git log/diff, and handoff records — no authored summaries, briefings, or curated inputs.

**For the Meta-Reviewer:** Access a `temp/` bilateral chat file only after documenting — in your output — which violation you are investigating, which chat file you are reading, and why that file is connected to the violation. Treat bilateral chat content as supplementary evidence for a specific, pre-identified violation only.
