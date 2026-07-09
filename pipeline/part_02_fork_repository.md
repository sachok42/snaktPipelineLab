# Step 1 — Fork Repository

**Agent role:** Tomás (Repo Setup)  **Model:** Haiku

Create a fork of the SnaKt repository that will hold this feature's implementation.
All subsequent code changes land on this fork, not the main repo.

After creating or selecting the local feature repository, verify it is a git repository:

```
git -C "<feature-repo-path>" rev-parse --is-inside-work-tree
```

If this fails, ask the operator for a corrected repository path or explicit permission to
run `git init` in the provided directory. Do not initialise git silently.

After the fork/local branch exists, validate that the artifact repository root is not inside
the feature repository:

```
python tools/artifacts.py validate --root "<artifact-repo-path>" --feature-repo "<feature-repo-path>"
```

**Output:** Fork URL / local branch reference + artifact repository validation result
+ handoff record (`handoffs/<feature-id>-step-1.md`)
+ completion marker (`complete/<feature-id>-step-1.md`).
