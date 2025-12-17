# **Phase Roles & Prompt Types – Semantic Projection Table**

This artifact describes:

* **What each phase *does*** in the semantic spiral
* **How CUNIT, PUNIT, and FUNIT behave inside each phase**
* **What each type of prompt is semantically responsible for**
* **Which artifacts each prompt type produces**

It is structured to serve simultaneously as:

* a conceptual guide,
* an implementation specification,
* and a grounding document for safe code generation.

---

# **1. High-Level Summary Table**

The table below shows the **semantic objective** of each phase and the **role-specific responsibilities** of CUNIT, PUNIT, and FUNIT within that phase.

---

# **2. Detailed Phase × Role Table**

### **Legend**

* **CUNIT** → shapes semantic space
* **PUNIT** → shapes semantic intention (question topology)
* **FUNIT** → executes semantic action (generation / analysis / retrieval)

---

## **Phase Overview Table**

| **Phase**             | **Semantic Purpose**                                                         | **CUNIT Function**                                            | **PUNIT Function**                                | **FUNIT Function**                                      | **Core Artifacts**                                 |
| --------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------- |
| **1. Learn**          | Establish conceptual space and reframe the problem                           | Define conceptual frames, constraints, lenses                 | Identify initial questions and gaps across frames | Produce structured problem summary                      | frames, reframed problem, initial question set     |
| **2. Understand**     | Reveal what the model considers relevant through explicit question formation | Shape interpretive boundaries (what matters / what doesn’t)   | Generate deeper diagnostic questions              | Produce refined understanding of problem domain         | clarified question graph, dependencies             |
| **3. Connection**     | Establish relationships between concepts, questions, and structures          | Choose relational frames (causal, temporal, logical, ethical) | Identify which relations to explore               | Generate semantic network / connection maps             | concept graph, dependency map                      |
| **4. Service**        | Explore hidden or implicit aspects; reveal blind spots and alternatives      | Enable exploration modes, alternative frames                  | Formulate probing, discovery-oriented questions   | Generate expanded interpretations and missing details   | enriched concept map, new questions                |
| **5. Knowledge**      | Retrieve grounded knowledge using structured questions                       | Select retrieval schemas and constraints                      | Choose retrieval questions and priorities         | Execute RAG/retrieval and synthesize relevant knowledge | knowledge snippets, citations, validated facts     |
| **6. Evolution**      | Explain reasoning path, internal steps, and conceptual transitions           | Choose reflective lens (meta-cognitive frame)                 | Generate self-reflective questions about process  | Produce reasoning summary and evolution trace           | reasoning path, self-assessment, evolution summary |
| **7. Responsibility** | Produce final answer with evaluation, integrity, and synthesis               | Set ethical and contextual constraints                        | Generate evaluative questions across candidates   | Produce final synthesized answer                        | final answer, evaluator scores, integrated output  |

---

# **3. Deep-Dive Table: Phase-by-Phase Role Semantics**

Below is a **fully detailed** mapping of semantic responsibilities for each role inside each phase.

---

## **1. Learn Phase – Establishing Semantic Space**

| **Role**  | **Semantic Task**                                                    | **Prompt Task**                                         | **Produced Artifacts**              |
| --------- | -------------------------------------------------------------------- | ------------------------------------------------------- | ----------------------------------- |
| **CUNIT** | Define the conceptual space in which the problem will be interpreted | Introduce conceptual frames, domain lenses, constraints | conceptual frames, reframed problem |
| **PUNIT** | Identify primary interpretive intentions                             | Generate initial questions across all frames            | initial question graph              |
| **FUNIT** | Create a structured understanding of the problem                     | Synthesize frames + questions into a coherent summary   | problem_summary, key aspects        |

---

## **2. Understand Phase – Extracting Internal Interpretive Vectors**

| Role      | Semantic Task                          | Prompt Task                                               | Produced Artifacts           |
| --------- | -------------------------------------- | --------------------------------------------------------- | ---------------------------- |
| **CUNIT** | Configure boundaries of interpretation | Define scope, assumptions, relevance criteria             | interpretive boundaries      |
| **PUNIT** | Extract deeper diagnostic questions    | Generate clarifying questions model needs to resolve      | refined questions            |
| **FUNIT** | Produce refined understanding          | Provide explicit articulation of emerging interpretations | deeper problem understanding |

---

## **3. Connection Phase – Building Semantic Structure**

| Role      | Semantic Task                                         | Prompt Task                            | Artifacts                     |
| --------- | ----------------------------------------------------- | -------------------------------------- | ----------------------------- |
| **CUNIT** | Select relationship types (causal, temporal, logical) | Define relational frames               | relational frames             |
| **PUNIT** | Shape intention to explore specific connections       | Generate targeted connection questions | dependency questions          |
| **FUNIT** | Build conceptual network                              | Produce graphs, maps, dependencies     | concept graph, dependency map |

---

## **4. Service Phase – Revealing Blind Spots and Hidden Structures**

| Role      | Semantic Task                                        | Prompt Task                                      | Artifacts             |
| --------- | ---------------------------------------------------- | ------------------------------------------------ | --------------------- |
| **CUNIT** | Open exploration space                               | Allow alternative interpretations, shadow frames | alternative frames    |
| **PUNIT** | Ask probing questions that explore hidden dimensions | Generate discovery-oriented questions            | exploratory questions |
| **FUNIT** | Reveal new insights                                  | Produce expanded interpretations                 | enriched concept map  |

---

## **5. Knowledge Phase – Retrieval & Grounding**

| Role      | Semantic Task                 | Prompt Task                              | Artifacts                     |
| --------- | ----------------------------- | ---------------------------------------- | ----------------------------- |
| **CUNIT** | Define retrieval schemas      | Select which retrieval modes are allowed | retrieval constraints         |
| **PUNIT** | Formulate retrieval questions | Generate specific RAG queries            | retrieval question set        |
| **FUNIT** | Perform retrieval & synthesis | Execute RAG/tooling + summarize          | grounded knowledge, citations |

---

## **6. Evolution Phase – Meta-Cognitive Reflection**

| Role      | Semantic Task                           | Prompt Task                                          | Artifacts                        |
| --------- | --------------------------------------- | ---------------------------------------------------- | -------------------------------- |
| **CUNIT** | Define reflective lens                  | Select introspective, temporal, or structural frames | reflection frame                 |
| **PUNIT** | Generate meta-questions about reasoning | Ask: “Why was this path chosen?” “What changed?”     | meta-question graph              |
| **FUNIT** | Produce reasoning path explanation      | Summarize evolution of reasoning                     | evolution trace, insight summary |

---

## **7. Responsibility Phase – Evaluation, Integrity, and Final Answer**

| Role      | Semantic Task                              | Prompt Task                                              | Artifacts                                  |
| --------- | ------------------------------------------ | -------------------------------------------------------- | ------------------------------------------ |
| **CUNIT** | Establish ethical + contextual constraints | Define requirements for responsible final output         | responsibility constraints                 |
| **PUNIT** | Generate evaluative comparisons            | Ask questions for evaluators across branches             | evaluation questions                       |
| **FUNIT** | Produce final answer                       | Integrate candidates, apply evaluator scores, synthesize | final output, rationale, integrity markers |

---

# **4. Cross-Phase Summary: CUNIT / PUNIT / FUNIT Semantics**

| **Role**  | **Core Semantic Objective** | **Abstract Behavior**                         | **Operational Projection**                    |
| --------- | --------------------------- | --------------------------------------------- | --------------------------------------------- |
| **CUNIT** | Shape semantic space        | Choose conceptual frames, constraints, lenses | Builds structured prompt environment          |
| **PUNIT** | Shape semantic intention    | Generate structured questions and priorities  | Produces question graphs (SQL)                |
| **FUNIT** | Execute semantic action     | Produce artifacts from space + intention      | Generates phase outputs, retrievals, analyses |

---

# **5. Artifact Outputs Per Role**

| **Phase**      | **CUNIT Artifacts** | **PUNIT Artifacts**    | **FUNIT Artifacts**     |
| -------------- | ------------------- | ---------------------- | ----------------------- |
| Learn          | Frames, reframing   | Initial questions      | Problem summary         |
| Understand     | Boundaries          | Deep questions         | Clarified understanding |
| Connection     | Relational frames   | Relationship questions | Concept graph           |
| Service        | Alternative frames  | Exploratory questions  | New insights            |
| Knowledge      | Retrieval schemas   | Retrieval questions    | Factual knowledge       |
| Evolution      | Reflective frame    | Meta-questions         | Reasoning path          |
| Responsibility | Constraints         | Evaluation questions   | Final answer            |

---

# **6. Intended Use of This Artifact**

This document serves as:

* a **semantic specification** for system designers,
* a **blueprint for PrompUnit creation**,
* a **reference for code generation systems**,
* a **control artifact** ensuring safety and invariants across implementations,
* a **canon of phase-role semantics** for all future extensions,
* an **alignment map** between conceptual architecture and executable logic.

It eliminates ambiguity and provides a unified reference for all contributors and automated systems.

---
