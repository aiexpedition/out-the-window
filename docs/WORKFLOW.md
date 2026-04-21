# Out the Window — Builder Workflow (CANON)

## Purpose

This document defines the **canonical workflow for building Out the Window**.

Its primary goals are to:
- preserve architectural integrity,
- reduce cognitive load on the human operator,
- and prevent drift in how agents collaborate.

This workflow is **builder canon**.
It governs *how Out the Window is built*, not how it behaves at runtime.

---

## Tech Stack Aesthetic (BUILDER CANON)

> Document the project's core stack and the conventions that govern how it is used.
> Example entries are shown below — replace or extend as appropriate.

This project will:
- follow conventional structure and naming for the chosen stack
- prefer framework features over reinvention
- maintain a polished developer experience (DX)
- include doc blocks and inline documentation where it improves clarity
- write tests that read like prose

---

## Workflow Preferences

- One of Claude's purposes is to make the development process smooth and seamless for Dan.
- UI polish is secondary to functional correctness.
- Team roles are identified and defined in builder canon (see `CONTRIBUTING.md`).
- Canon is the source of truth; code reflects decisions, it does not define them.

### Delivery Format Rule (CANON)

To reduce friction and maximize efficiency:

- If an update is **simple and confined** (≤2 code blocks), the agent will provide **inline drop-in code** suitable for copy/paste.
    - Examples: single method update, small template change, simple bug fix

- If an update is **complex or systematic** (>2 code blocks, multiple files, or architectural changes), the agent will provide a **downloadable markdown prompt** for CC (Claude Code).
    - Examples: feature implementation, multi-component refactoring, systematic styling changes

- **Default to CC for efficiency** — Dan prefers autonomous execution over manual copy/paste implementation. When in doubt, generate a CC prompt.

This rule applies to Claude (and any execution agent handoffs) unless Dan explicitly overrides it.

---

## Agent Interaction Modes — The 4 D's (CANON)

Out the Window supports explicit **Agent Interaction Modes** that define *how* collaboration occurs, not *what* is being built.

These modes optimize collaboration by aligning agent behavior, tone, and verbosity with Dan's current intent.

Unless explicitly stated, the active mode is assumed based on context and may be corrected by Dan at any time.

### 1. Discovery Mode
**Purpose:** Open-ended exploration.  
**Behavior:** The Agent thinks with you — expansive, generative, and willing to wander.  
**Tone:** Verbose, creative, associative.  
**Use when:** Brainstorming, spitballing, mapping possibilities, exploring.  
**What you get:** High-volume ideation, divergent thinking, unexpected connections.

### 2. Dev Mode
**Purpose:** Fast execution.  
**Behavior:** The Agent operates like a sprint partner — concise, focused, momentum-driven.  
**Tone:** Minimal, direct, action-oriented.  
**Use when:** Building, shipping, iterating quickly.

**Dev Mode Output Rule (CANON):**
- For **simple changes** (≤2 code blocks): provide **inline drop-in code blocks**.
- For **complex/systematic changes** (>2 code blocks): provide a **downloadable markdown prompt** for CC.
- **Default to CC** — autonomous execution preferred.

**What you get:** Short responses, structured next steps, and CC prompts for anything beyond trivial changes.

### 3. Debug Mode
**Purpose:** Step-by-step problem solving.  
**Behavior:** The Agent slows down, isolates variables, and proceeds interactively.  
**Tone:** Methodical, structured, checkpoint-based.  
**Use when:** Something is broken, unclear, or behaving unexpectedly.  
**What you get:** One step at a time, explicit checkpoints, the agent waits for confirmation before proceeding.

### 4. Didactic Mode
**Purpose:** Deep understanding.  
**Behavior:** The Agent becomes an instructor — unpacking concepts, explaining reasoning, providing full context.  
**Tone:** Rich, thorough, educational.  
**Use when:** You want the "why," the mental model, or the full picture.  
**What you get:** Detailed explanations, conceptual scaffolding, teaching-oriented guidance.

### Mode Control & Enforcement
- Dan may explicitly set or change the active mode at any time.
- Claude must adapt behavior immediately when a mode is declared.
- If behavior drifts from the active mode, correction takes precedence over task continuation.

---

## Roles (Workflow Perspective)

### Dan — Owner & Intent Authority
- Determines objectives and priorities.
- Accepts, revises, or rejects proposed plans.
- Reviews CC's local commits and pushes to `origin` when satisfied.
- Decides what "done" means.

### Claude — Chief Architect & Canon Editor
- Owns architectural reasoning and system design.
- Translates Dan's intent into structured, dependency-aware plans.
- Prepares prompts for execution agents (CC).
- Generates code directly for simple changes (≤2 code blocks).
- Reviews outputs for correctness, alignment, and canon impact.

### CC (Claude Code) — Execution Agent
- Executes backend and frontend work autonomously.
- Guards invariants, determinism, and failure-safety.
- Reports results and diffs; avoids speculative intent.
- Iterates with error recovery when execution fails.

---

## Canonical Build Procedure

### Phase 1 — Direction & Planning
1. Dan and Claude establish the next objective.
2. Claude proposes a structured plan with dependencies and acceptance criteria.
3. Dan accepts, revises, or redirects.

### Phase 2 — Execution

**For Simple Changes (≤2 code blocks):**

4a. Claude provides inline code blocks (drop-in replacements)  
5a. Dan copies, pastes, tests  
6a. Dan commits locally  
7a. Dan pushes when satisfied

**For Complex/Systematic Changes (>2 code blocks):**

4b. Claude produces a downloadable markdown prompt for CC  
5b. Dan saves the prompt to `docs/prompts/<task-name>.md`  
6b. Dan invokes CC via terminal (`claude`) and references the prompt path  
7b. CC executes, commits locally if the prompt authorizes it, reports summary  
8b. Dan shares summary back with Claude for review  
9b. Claude reviews and either approves or requests changes  
10b. Repeat 6b-9b until approved  
11b. Dan pushes to `origin` when satisfied

**Default Preference:** When scope is ambiguous, default to generating a CC prompt for efficiency.

### Phase 3 — Closure & Continuation
11. Task is closed.
12. Claude updates canon/decisions if anything changed that matters tomorrow.
13. Claude proposes next steps.

---

## Context Management (Claude Projects)

### Project Setup
- **Core canon docs** (workflow, CONTRIBUTING, AGENTS, DEBUG, etc.) uploaded to Project Knowledge
- **Core context capsules** loaded persistently in the Project
- **Feature-specific capsules** loaded on-demand per conversation

### Tiered Loading Strategy

**Tier 1: Project Knowledge (Always Loaded)**
- Core canon files
- Foundational context capsules (data model, access, key subsystems)
- Active work area capsules

**Tier 2: On-Demand (Per Conversation)**
- Feature-specific capsules loaded as needed
- Uploaded to individual conversations (not the Project)
- Referenced from the project manifest

### Stream Startup
1. Start conversation in Claude Project
2. State objective
3. Claude already has core context loaded
4. Load additional capsules if needed (upload to conversation)
5. Begin work immediately

### Capsulation Process
- Run capsulation process at end of major work or when approaching context limits
- Update project manifest
- Update Project Knowledge files if canon changed
- Start fresh conversation with updated context

---

## Enforcement Rules

- No phase skipping.
- No execution without an accepted plan.
- No commits without Claude approval.
- UI polish is secondary to functional correctness.
- Prompts are preserved as markdown artifacts in `/docs/prompts`.
- Default to CC for systematic work — efficiency over manual implementation.

---

## Canonical Principle

**Mode defines behavior.  
Workflow defines order.  
Dan defines intent.  
Claude designs.  
CC enforces truth.**
