# **Safe Code Generation Specification**


It incorporates all earlier **mitigation recommendations** and explicitly neutralizes each **tension point**.
This specification is intended to be used **as a control document for LLM-driven code generation**, ensuring the produced system matches the conceptual architecture, preserves invariants, and avoids collapse of semantic structures.

---

# **Safe Code Generation Specification (SCGS)**


This specification defines the **minimum safe constraints** that any automated code-generation system must follow when producing or modifying code in the project.
It ensures architectural integrity, prevents semantic-role drift, and enforces strict operational clarity.

The specification is **normative**: all generated code **MUST** satisfy these constraints.

---

# **1. Core Architectural Invariants**

## **1.1 Separation of Roles (CUNIT / PUNIT / FUNIT) MUST be preserved**

Generated code **must not** merge responsibilities of CUNIT, PUNIT, and FUNIT.

### Required structure:

```
class CUnitAgent(BaseAgent): ...
class PUnitAgent(BaseAgent): ...
class FUnitAgent(BaseAgent): ...
```

Each role must have:

* separate classes,
* separate method signatures,
* separate prompt rendering logic.

No class may contain behavior belonging to another role.

---

## **1.2 The Coordinator MUST be a thin orchestrator, not a monolithic object**

Coordinator structure must follow:

```
Coordinator.run_scenario(state)
Coordinator.run_phase(phase, state)
Coordinator.run_role(role, state)
```

Coordinator must not:

* perform reasoning,
* embed prompts,
* contain business logic,
* mutate state outside defined methods.

It only orchestrates the execution pipeline.

---

## **1.3 Prompts store**

All PromptUnits must be stored outside code, in a directory structure:

```
/prompts/<phase>/<role>/<prompt_name>
```

Generated code must not:

* inline prompt templates into Python,
* embed prompt text in logic,
* generate prompts dynamically in code.

All prompts must be loaded through a prompts loader class.

---

# **2. State Safety Requirements**

## **2.1 State MUST comply with a fixed schema**

Generated code must treat `state` as a strongly structured object.
No new keys may be invented without explicit schema change.

Example schema excerpt:

```
state.user_input
state.phases[phase_name].cunit_output
state.sql.questions[]
state.branches[branch_id]
state.trace[]
state.final_answer
```

### Requirements:

* No arbitrary dynamic keys.
* No nested mutations beyond defined structure.
* All state mutations go through a `StateManager`.

---

## **2.2 Traceability MUST be preserved**

Every role execution must log a trace entry:

```
trace_entry = {
    "phase": ...,
    "role": ...,
    "prompt_id": ...,
    "inputs_summary": ...,
    "outputs_summary": ...
}
```

Generated code must not generate silent or unlogged transitions.

---

# **3. Prompt Assembly Safety**

## **3.1 Prompt rendering MUST be deterministic**

Generated code must use:

```
render_prompt(template: str, variables: Dict[str, Any]) -> str
```

Variables must match a whitelisted set per role:

### Example:

CUNIT variables:

```
user_query, conversation_summary, previous_frames
```

PUNIT variables:

```
user_query, reframed_problem, conceptual_frames
```

FUNIT variables:

```
user_query, questions, conceptual_frames, state_summary
```

Prompts **must not** contain:

* dynamic Python-generated text,
* ad-hoc string concatenation,
* undefined variables.

---

## **3.2 PromptUnits MUST remain immutable at runtime**

Generated code must not modify PromptUnit templates.
Templates must be loaded, rendered, and executed without mutation.

---

# **4. Branching and Parallel Reasoning Requirements**

## **4.1 Branching MUST follow explicit lifecycle rules**

Generated code must implement:

```
BranchManager.create_branch(parent_state)
BranchManager.fork_state(state)
BranchManager.merge_candidates(branches)
BranchManager.prune(branch_id, reason)
```

Branches must be independent substates.

### Prohibited:

* Shared mutable state between branches
* Implicit branching
* Merging outside Responsibility phase

---

## **4.2 Branch limits MUST come from ScenarioConfig**

Generated code must not invent branching rules.

Only ScenarioConfig defines:

```
branching.enabled
branching.max_branches
branching.phases
```

---

# **5. Evaluator Safety Requirements**

## **5.1 Evaluators MUST follow a fixed protocol**

Generated evaluators must implement:

```
Evaluator.evaluate(candidate: CandidateAnswer) -> EvaluationResult
```

### EvaluationResult:

```
{
  "scores": { "ethics": float, "clarity": float, ... },
  "comments": str
}
```

Evaluators must not:

* modify candidate answers,
* directly write final answers,
* alter scenario configuration.

---

## **5.2 Aggregation MUST follow a deterministic rule**

Generated code must implement a clear, transparent algorithm:

```
best_candidate = select_best_candidate(all_evaluations)
final_answer = run_responsibility_funit(best_candidate, evaluations)
```

Not allowed:

* fuzzy selection,
* randomization,
* skipping evaluators,
* ad-hoc logic.

---

# **6. Question Graph Requirements (SQL)**

## **6.1 Questions MUST be structured as graph nodes**

Generated code must define:

```
class QuestionNode:
    id: str
    text: str
    dependencies: List[str]
    phase_origin: str
```

Not allowed:

* plain string arrays,
* unstructured lists,
* implicit question chains.

---

## **6.2 Graph operations MUST use a defined API**

```
sql.add_node(node)
sql.add_dependency(node_id, dependency_id)
sql.get_roots()
sql.to_dict()
```

Generated code must not manipulate the graph directly via arrays.

---

# **7. Responsibility Phase Safety**

## **7.1 Responsibility MUST be more than summarization**

Generated code must implement:

1. evaluator execution
2. candidate scoring
3. candidate selection
4. final synthesis via Responsibility FUNIT

Skipping any of these steps violates architecture.

---

## **7.2 Fragment merging must NOT be auto-generated without explicit specification**

Merging fragments from branches is optional, but if implemented, must follow explicit rules.

---

# **8. Metaphor Isolation Requirements**

Generated code must not:

* implement classes named after metaphors
  (e.g., “ResonanceField”, “SpiralUnfoldingEngine”),
* interpret conceptual terms as structural requirements.

Metaphors must be translated into explicit operational equivalents.

---

# **9. Dependency Safety Requirements**

To avoid recursive structures:

* No circular imports.
* No mutual class instantiation between agents.
* PromptsLoader, StateManager, Coordinator must be acyclic.

A dependency diagram must be respected:

```
Coordinator
 ├─ PhaseRunner
 ├─ RoleAgent (CUNIT/PUNIT/FUNIT)
 ├─ PromptsLoader
 ├─ StateManager
 └─ EvaluatorEngine
```

Agents must not reference Coordinator internally.

---

# **10. Code Generation Boundaries**

Generated code MUST:

* Respect ScenarioConfig as the governing structure.
* Keep all prompts external.
* Use strictly typed data structures.
* Preserve state schema.
* Maintain determinism in execution flow.
* Avoid speculative abstractions.
* Avoid expanding architecture unless explicitly instructed.

Generated code MUST NOT:

* invent new conceptual entities,
* collapse roles,
* flatten the spiral,
* rewrite prompts,
* introduce uncontrolled variability,
* bypass evaluators,
* alter state shape.

---

# **11. Required Supplementary Files (Autogenerated or Manual)**

To support safe code generation, the system must include:

1. `state_schema.json` — authoritative state schema
2. `promptunit_schema.json` — PromptUnit schema
3. `scenario_schema.json` — ScenarioConfig schema
4. `class_interfaces.py` — base classes & abstract methods
5. `dependency_map.md` — dependency graph
6. `tests/architecture_invariants/` — tests enforcing invariants

LLM-generated code must rely on these schemas and interfaces.

---

# **12. Code Generation Checklist (Hard Requirements)**

A code generation request is valid only if:

* [ ] Roles remain separated
* [ ] Coordinator remains thin
* [ ] Prompts repository is external and immutable
* [ ] State matches schema
* [ ] Graph API is used
* [ ] Branching follows lifecycle
* [ ] Evaluators follow protocol
* [ ] Responsibility executes full pipeline
* [ ] No metaphors appear in code
* [ ] All logic is deterministic

---

# **Conclusion**

This Safe Code Generation Specification establishes the **strict safety rails** required to maintain the integrity of the architecture when generating or updating code via LLMs.

It ensures:

* architectural clarity,
* role integrity,
* deterministic behavior,
* evaluative responsibility,
* separation of concerns,
* future extensibility,
* auditability and traceability.

---
