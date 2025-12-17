# Semantic Vector–Driven LLM Research Engine

## Overview

This project is an experimental **LLM-based research engine** designed to explore how complex questions can be unfolded, examined, and refined through **graded semantic vectors** rather than rigid pipelines or domain-specific agents.

The core idea is simple:

> **Instead of hard‑coding logic for each domain, we operate an invariant core that guides inquiry through semantic structure.**

This allows the same engine to be applied across regulatory analysis, research, knowledge exploration, or other domains with **minimal or no changes to the codebase**.

---

## Key Concepts

### Semantic Vector Gradation

Requests are not treated as single prompts, but as **semantic trajectories** that move through different aspects of understanding (e.g. scope, structure, relations, implications).

These semantic vectors:

* guide how the model explores a question,
* determine which perspectives are activated,
* control how results are refined and connected.

The vectors act as *directions of attention*, not as fixed rules.

---

### Invariant Core

At the heart of the system is an **invariant execution core** that:

* remains independent of the application domain,
* does not encode business logic or regulatory specifics,
* orchestrates the research cycle purely through semantic control.

This core:

* manages the inquiry lifecycle,
* coordinates context expansion and refinement,
* maintains consistency across iterations.

Domain adaptation happens **at the semantic level**, not in the engine logic.

---

### Semantic Configuration over Code Changes

Customization is achieved by:

* adjusting semantic vectors,
* redefining question perspectives,
* tuning how concepts are unfolded and connected.

As a result:

* the same codebase can serve multiple domains,
* new use cases do not require rewriting agents or pipelines,
* experimentation focuses on meaning, not mechanics.

---

## Why This Matters

Traditional LLM systems often scale by adding:

* new agents,
* new prompt graphs,
* new domain‑specific pipelines.

This approach quickly leads to:

* brittle architectures,
* duplicated logic,
* exponential maintenance cost.

This project explores an alternative:

> **A stable, minimal core with flexible semantic optics.**

The system evolves by changing *how it looks*, not *how it is built*.

---

## Status

This repository represents a **research and demonstration prototype**.
It focuses on:

* semantic orchestration patterns,
* invariant LLM execution architecture,
* exploration of domain‑agnostic research flows.

It is intentionally minimal and exploratory.

---

## Disclaimer

This project is not a finished product and does not claim production readiness.
It is a **research artifact** intended to explore architectural ideas around LLM‑driven inquiry, semantic control, and maintainable agent systems.

---

## Example

An example of a system run output is available at:

dumps/dialog/1.json
