# Law 10 — Acquire Branch Lease Before Landing

**Recipients:** Orchestrator, Repo Setup, Implementer, Debugger, Comparator, all solvers

Obtain an exclusive lease from the Orchestrator before landing any commit to a branch.
Hold the lease for the duration of your write, then return it.
The Orchestrator issues and revokes all leases.
Wait for the current lease holder to finish before requesting a lease on a branch that is already held.
