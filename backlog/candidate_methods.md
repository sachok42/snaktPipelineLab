# Candidate Testing Methods — Not Yet Active

These methods have been considered but are not part of the current pipeline catalog.
To activate one, move its definition into the Testing Method Catalog in
`pipeline/part_04_solver_agents.md` and add any required applicability criteria.

---

## Method X — Cross-Backend Validation

Applicable when SnaKt supports more than one verification backend (e.g. different SMT
solvers or verification engines). Run the same specifications against all available
backends and flag any disagreement in outcome. Two backends disagreeing on the same
spec is a guaranteed bug or soundness gap without requiring a human to adjudicate —
the backends are each other's oracle.

**Activation condition:** confirm SnaKt has at least two independently configured
backends that can be invoked on the same input.

---

## Method R — Reference Tool Comparison

Applicable when the feature being tested overlaps with a capability in an established
formal verification tool (Dafny, Why3, JML, Viper, KeY). Solvers express the equivalent
specification in the reference tool and compare outcomes with SnaKt. Useful for checking
SnaKt does not accept something the reference tool rejects (unsoundness) or rejects
something the reference tool accepts (unnecessary incompleteness).

**Activation condition:** identify a specific reference tool whose feature set overlaps
meaningfully with the SnaKt feature under test, and confirm solvers have access to it.
