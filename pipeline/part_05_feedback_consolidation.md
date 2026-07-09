# Step 4 — Feedback Consolidation

**Agent role:** Dawa (Synthesizer)  **Model:** Sonnet

Reads all structured solver reports from Step 3 (grouped by testing method) and produces a
single consolidated feedback document. Reports are labelled by method and solver index
(e.g. V-1, V-2, A-1, A-2, B-1). The Synthesizer works from the structured report schema
defined in Step 3 — it must not require or request free-form prose from solvers.

---

## Section 1 — Per-Method Calibration Analysis

For each testing method that was used, compare the results of the solvers within that method:
- What approach did each solver take?
- Where did their findings agree and where did they diverge?
- For Method V only: compare all V-solvers on the shared calibration problem specifically —
  did the same problem verify differently across models, and why?

Each method gets its own subsection. One-line summaries are not acceptable — the analysis
must be substantive enough for the Debugger to understand the quality of the evidence.

---

## Section 2 — Cross-Method Synthesis

Compare findings across methods. The same bug or gap found by multiple methods independently
is stronger evidence than one found by only one method. Flag:
- Findings corroborated by more than one method (high confidence)
- Findings unique to one method (lower confidence, note which)
- Contradictions between methods (flag explicitly and attempt to resolve)

---

## Section 3 — Conflicting Observations

Observations where solvers disagree — within or across methods. For each conflict:
- What each solver claimed
- Why the claims conflict
- Which is more likely correct (with reasoning), or "unresolved" if it cannot be determined

Unresolved conflicts are passed to the Debugger as open questions, not silently dropped.

---

## Section 4 — Prioritised Issue List

Aggregate all issues from all solver reports into a single deduplicated table, ordered
by severity then by corroboration count. Use the solver report issue IDs as canonical
references — do not rename or renumber them.

| ID(s) | Description | Severity | Methods | Solvers |
|-------|-------------|----------|---------|---------|

Items appearing in multiple methods' reports are stronger evidence and rank above
single-method findings of equal severity.

---

**Output:** Consolidated feedback document + handoff record (`handoffs/<feature-id>-step-4.md`)
+ completion marker (`complete/<feature-id>-step-4.md`).
