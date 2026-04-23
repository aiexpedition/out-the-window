# Out the Window — Project Memory

Brief orientation for any Claude session working on this project. This file loads automatically at the start of every Claude Code session. Read it, then follow the references to fuller canon as needed.

---

## Project Snapshot

**Out the Window** is a GPS-aware iOS app that narrates Texas historical markers to road-trippers.

- **Publisher:** The AI Expedition LLC
- **Platform:** iOS native (Swift / SwiftUI), iOS 17+ for POC, iOS 26+ for production
- **Product-defining moment:** CarPlay (deferred to production phase)
- **POC target date:** May 29, 2026 — a drive from McKinney, TX to Real County via TX-121 / I-820 / I-30 / I-20 / US-183 / US-377 / US-190 / US-83
- **Current status:** Pre-POC. Phase 1 (statewide marker data pipeline) complete. iOS app not yet scaffolded.

---

## Roles

- **Dan Maxwell** — Product Owner. Defines intent and acceptance criteria. Pushes to `origin`.
- **Claude** (claude.ai, this file's audience when mounted there) — Chief Architect. Owns architecture, canon integrity, workflow orchestration. Authors CC prompts.
- **CC (Claude Code)** — Execution Agent. Implements Claude's prompts on the filesystem. Commits when authorized. Never pushes unprompted.

Full role definitions: see `docs/AGENTS.md` and `docs/CONTRIBUTING.md`.

---

## Canon Map

Canon lives in `/docs`. **Code reflects decisions; it does not define them.** If something matters tomorrow, it belongs in `/docs`.

**Process canon:**
- `CLAUDE.md` — session orientation (this file), project root
- `docs/CONTRIBUTING.md` — agent roles and contribution rules
- `docs/WORKFLOW.md` — build procedure, interaction modes (Discovery / Dev / Debug / Didactic), delivery format rules
- `docs/AGENTS.md` — execution boundaries for AI agents

**Architectural decisions (ADRs):**
- `docs/ADR-001-mobile-framework.md` — Swift/SwiftUI native, iOS-first, Android deferred
- `docs/ADR-002-dev-environment.md` — phased (Intel iMac Pro POC → Apple Silicon Mac mini production post-WWDC 2026)
- `docs/ADR-003-ownership-legal-structure.md` — The AI Expedition LLC as publisher, Apple Developer Organization account

**Product spec:**
- `docs/POC-001-may29-roadtrip.md` — May 29 road trip POC scope and success criteria

**Preserved AI prompts:**
- `docs/prompts/` — CC prompts saved as markdown artifacts (per WORKFLOW.md)

**Context capsules** (Olliver environment: `out-the-window`):
- Foundational durable context lives in Olliver capsules, separately from `/docs`. Mount as needed per session.

---

## Working Rules

### Commits and pushes
- **Commits:** CC may commit when instructed — either in conversation or in a CC prompt's Git Discipline section. CC never commits unprompted.
- **Pushes:** CC never pushes unless Dan directly and explicitly instructs it in the current conversation. Prompt artifacts cannot authorize a push. The push is the irreversible boundary.
- Commit messages: imperative mood, scoped, concise.

### Delivery format
- **Simple changes (≤2 code blocks):** Claude provides inline code blocks for Dan to paste.
- **Complex/systematic changes (>2 code blocks):** Claude produces a downloadable markdown prompt. Dan saves it to `docs/prompts/<task-name>.md` and references that path when invoking CC.
- **Default to CC for efficiency** — autonomous execution preferred over manual copy/paste.

### Interaction modes
Dan may declare a mode at any time. Defaults inferred from context. Modes: **Discovery** (expansive brainstorming), **Dev** (concise, action-oriented — the default for building), **Debug** (methodical, checkpoint-based), **Didactic** (teaching-oriented, full context). See `docs/WORKFLOW.md` for full descriptions.

---

## Tech Stack

### iOS App (Swift / SwiftUI native)
- Apple frameworks only — no third-party dependencies without ADR justification
- Services are plain Swift classes (`final class`); models are `struct`
- Views and state holders use `@Observable` (iOS 17+ Observation framework)
- No persistence beyond bundled JSON for POC; SwiftData for production
- Logging via `os.Logger`, subsystem `com.theaiexpedition.OutTheWindow`, category per component (`data`, `location`, `narration`, etc.)
- Xcode 16 synchronized folder groups: files added under `OutTheWindow/` and `OutTheWindowTests/` directories auto-register to their targets — no manual `project.pbxproj` edits needed for source files

Full rationale: `docs/ADR-001-mobile-framework.md`

### Data Pipeline (Python, build-time)
- Lives in `tools/data-pipeline/`
- Python 3.11+, `pyproj` for UTM→WGS84 conversion, stdlib otherwise
- No pandas — keeps the tool small and auditable
- Output: `markers-texas.json` + `markers-texas.summary.md` (gitignored, reproducible from source)
- Runs on Win11 dev rig (WSL)

### Companion Website (TALL stack, production phase)
- Tailwind 4, Alpine.js, Laravel 11, Livewire 3
- Not built for POC
- Hosts user accounts, bookmark sync, AI-enriched deep dives
- Will monitor the THC ArcGIS REST API via agents to detect marker changes upstream (the iOS app never calls the THC API directly — offline-first invariant)

---

## Current Repository Layout

```
OTW/
├── .git/
├── .gitignore
├── README.md
├── CLAUDE.md                    (this file)
├── docs/                        Canon — ADRs, POC spec, workflow
│   ├── ADR-001-mobile-framework.md
│   ├── ADR-002-dev-environment.md
│   ├── ADR-003-ownership-legal-structure.md
│   ├── AGENTS.md
│   ├── CONTRIBUTING.md
│   ├── POC-001-may29-roadtrip.md
│   ├── WORKFLOW.md
│   └── prompts/                 Preserved CC prompts
├── data/thc/                    Texas Historical Commission source CSVs (April 2026 export)
└── tools/                       Build-time tooling
    └── data-pipeline/           Phase 1 — THC CSV → markers-texas.json
```

---

## Decisions That Change Behavior in Every Session

These are material enough to repeat here rather than force a cross-reference:

1. **Offline-first is an invariant.** The iOS app never makes runtime network calls for core experience. All marker data ships bundled. Rural Texas cell coverage is unreliable and the product must work anyway.

2. **No curation of the POC marker set.** The POC ships all THC markers that pass objective quality filters (has inscription text + valid UTM coords) — roughly 13.5k records as of the April 2026 export. See `tools/data-pipeline/out/markers-texas.summary.md` for the current authoritative count. No corridor filter, no editorial selection, no family-history anchor markers. The product thesis being tested is *"proximity-triggered narration of objective Texas history feels meaningful"* — shaping the data set would invalidate the test.

3. **POC narration is Apple's `AVSpeechSynthesizer`.** No recorded audio, no cloud TTS, no per-marker cost. Recorded "campfire voice" narration is deferred to production as a premium feature.

4. **THC commercial licensing is POC-gated.** POC uses THC marker data under personal/fair use on Dan's own device. Commercial licensing conversation is held until Dan decides post-POC whether the product is worth building.

5. **Canon is the source of truth.** When a prompt and canon disagree, canon wins. CC should flag the discrepancy and stop rather than invent behavior.

---

## When Stuck

1. Check this file — it's meant to orient, not answer every question.
2. Follow the reference to the most specific canon file (`docs/ADR-*`, `docs/POC-001*`, etc.).
3. Check Olliver capsules in the `out-the-window` environment for foundational context.
4. If uncertainty remains, stop and ask Dan rather than guess.

---

## Update Discipline

This file is orientation, not a changelog. Update it when:
- A new canon file is added to `/docs/`
- A working rule materially changes (commit policy, interaction model, etc.)
- A new major subsystem comes online (the `ios/` directory gets scaffolded; a new `tools/` subproject appears)

Do **not** update it when:
- A single ADR changes wording
- A bug is fixed
- A feature ships

Keep it short enough to skim in under a minute.
