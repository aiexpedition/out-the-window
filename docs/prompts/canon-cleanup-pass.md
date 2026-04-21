# CC Prompt — Canon Cleanup Pass

**Target agent:** CC (Claude Code)
**Execution host:** Win11 dev rig, WSL
**Project root:** `/mnt/c/Users/wimbl/Projects/OTW`
**Branch:** `main`
**Related canon:** `docs/POC-001-may29-roadtrip.md`, `docs/CONTRIBUTING.md`, `docs/AGENTS.md`, `docs/WORKFLOW.md`, `CLAUDE.md`

---

## Context

Over the stream of 2026-04-21, three decisions invalidated portions of existing canon:

1. **POC-001 corridor → statewide.** The POC marker bundle is the full statewide THC dataset after objective quality filtering (13,456 records), not a corridor-filtered subset. Driven by the realization that built-in TTS means zero per-marker cost, so filtering adds no POC value and subtracts product honesty.

2. **CC commit policy.** Per the updated `~/.claude/rules/style.md` (global rule), CC may commit when authorized by a prompt or live instruction; CC never pushes unless Dan explicitly authorizes in the current conversation. Project canon still says "Dan performs final commits" — stale.

3. **Prompt delivery mechanism.** The canonical flow is: Claude authors prompt → Dan downloads to `docs/prompts/<name>.md` → Dan references that path when invoking CC via terminal. This is implicit in how prompts flow through the filesystem but not stated in WORKFLOW.md.

Additionally, `AGENTS.md` contains a stale reference to a `CLAUDE.md` as a possible future location for stack guidelines; `CLAUDE.md` now exists at project root and the language should reflect reality.

This prompt applies all corrections in one atomic commit.

---

## Objective

Update four canon files (`docs/POC-001-may29-roadtrip.md`, `docs/CONTRIBUTING.md`, `docs/AGENTS.md`, `docs/WORKFLOW.md`) to reflect current reality. Preserve the prompt to `docs/prompts/` per WORKFLOW.md. Commit with a single descriptive message. Do not push.

---

## Scope

### In Scope
- All edits listed below, applied in order
- Single commit on `main` with the message specified at the bottom
- Prompt preserved at `docs/prompts/canon-cleanup-pass.md`

### Out of Scope
- No edits to `CLAUDE.md` (already refined in a previous commit)
- No edits to ADRs (001/002/003) — they reflect their own decision moments and do not need retrofitting
- No edits to `tools/data-pipeline/` code or output
- No edits to the `.gitignore`, `README.md`, or any Olliver capsule (Claude handles capsule edits separately)
- No push

---

## Edits

There are **11 edits** across **4 files**. Apply all of them; if any `old_str` fails to match byte-for-byte, stop and flag rather than attempt reconciliation.

---

### File 1: `docs/POC-001-may29-roadtrip.md`

Four edits. The POC spec is rewritten in the places where "corridor" was the frame; the narrative sections (The Defining Scene, hardware/battery/risks) reference corridor *concepts* in ways that remain true and are not edited.

#### Edit 1.1 — "Route Corridor Marker Set" section rewrite

**Find (exact text, including heading and all bullets):**

```
### Route Corridor Marker Set

- **Target count:** All markers within the corridor — likely 100–300 markers depending on corridor width
- **Source:** THC Historical Marker CSV (already in project)
- **Selection criteria — objective only:**
  - Within a defined radius of the planned driving corridor (e.g., ~3 miles either side of the route polyline)
  - Lat/long data present and validated
  - Inscription text present (not just title)
- **No editorial curation.** Markers are included or excluded by geographic and data-completeness rules alone. No thematic filtering, no personal selection, no narrative shaping. The POC tests how Out the Window behaves for any user driving this route — which means the data set must reflect what any user would experience.
- **Bundled in app binary:** All corridor-qualifying markers ship with the app as seed data. No network fetch required for core experience.
- **Natural outcome:** Marker #4831 (McLauren Massacre) will be present if-and-only-if the geographic filter includes it. No special handling. If it fires during the drive, it fires because the algorithm worked — not because it was hand-placed.
```

**Replace with:**

```
### Statewide Marker Set

- **Target count:** All THC Historical Markers statewide that pass objective quality filters. Approximately 13.5k records as of the April 2026 CSV export. See `tools/data-pipeline/out/markers-texas.summary.md` for the current authoritative count.
- **Source:** THC Historical Marker CSV (already in project)
- **Selection criteria — objective only:**
  - Inscription text present (not just title)
  - Valid UTM coordinates that convert to a lat/long inside the Texas bounding box
  - No other filter — no corridor, no radius, no editorial selection
- **Why statewide, not corridor:** POC narration uses Apple's built-in `AVSpeechSynthesizer` with zero per-marker cost. A corridor filter would shape the dataset without adding POC value, and would undermine the product thesis — which is that proximity-triggered narration of *objective* Texas history feels meaningful to any traveler. If the user detours off the planned route, markers there still fire. That is the real experience, not a curated one.
- **Bundled in app binary:** All qualifying markers ship with the app as seed data. No network fetch required for core experience. File size is on the order of 5 MB pretty-printed JSON, well under what fits in an iOS app bundle.
- **Natural outcome:** Marker #4831 (McLauren Massacre) will be present because it passes the objective filter, not because it was hand-placed. If it fires during the drive, it fires because the algorithm worked.
- **Runtime implication:** The iOS app cannot register 13.5k simultaneous geofences (CLLocationManager caps at 20 per app). A sliding-window strategy is required — maintain active geofences for the N closest markers, refresh the set as the user moves. This is production-grade architecture exercised honestly by the POC.
```

---

#### Edit 1.2 — Data Preparation section rewrite

**Find (exact text, from the heading through the "100–500 KB" line):**

```
### Data Preparation (Pre-Build Task)

Before writing Swift code, a corridor marker dataset must exist:

1. **Define the route polyline.** Build a geographic line representation of the actual highway route (McKinney → Fort Worth loop → I-20 west → US-183 → US-377 → US-190 → US-83 → Leakey).
2. **Filter THC Historical Marker CSV** for markers within a defined radius of the polyline (recommend 3 miles either side — tunable based on what we see in the dataset).
3. **Validate data quality:** every included marker must have lat/long and inscription text. Drop markers with incomplete data.
4. **Clean inscription text for TTS:** expand abbreviations, remove bracketed editorial notes, normalize punctuation for natural speech cadence.
5. **Export to `markers-corridor.json`** bundled in app resources.

The filter is mechanical and reproducible. No hand-selection, no inclusion or exclusion based on content. The same script run against the same data produces the same output. Whoever runs it gets the same markers.

This can be done in Python on the Win11 rig and doesn't require the Mac. Output is likely 100–500 KB JSON.
```

**Replace with:**

```
### Data Preparation (Pre-Build Task)

Before writing Swift code, a statewide marker dataset must exist. This work is complete: the pipeline lives in `tools/data-pipeline/` and produces `markers-texas.json` from the THC CSV.

Pipeline steps:

1. **Read the THC Historical Marker CSV** from `data/thc/`.
2. **Convert UTM to WGS84.** THC uses NAD83 datum across zones 13/14/15. Per-row conversion via `pyproj`.
3. **Validate data quality:** every included marker must have inscription text and valid UTM coordinates. Output must fall inside the Texas bounding box (sanity check against conversion errors).
4. **Clean inscription text for TTS:** expand abbreviations conservatively, remove bracketed editorial notes, normalize smart quotes. Preserve the original text alongside the cleaned version.
5. **Export to `tools/data-pipeline/out/markers-texas.json`** for bundling into the iOS app. Output is ~5 MB pretty-printed JSON.
6. **Emit a summary report** at `tools/data-pipeline/out/markers-texas.summary.md` covering record counts, rejection breakdown, county distribution, and spot-check markers.

The filter is mechanical and reproducible. No hand-selection, no inclusion or exclusion based on content. The same script run against the same data produces byte-identical output. Whoever runs it gets the same markers.

The pipeline is pure Python (`pyproj` + stdlib) and runs on the Win11 rig. It does not require the Mac.
```

---

#### Edit 1.3 — Architecture tree: bundle filename

**Find (exact line):**

```
    └── markers-corridor.json       (bundled 30–50 markers)
```

**Replace with:**

```
    └── markers-texas.json          (bundled ~13.5k markers, statewide)
```

---

#### Edit 1.4 — Phase 1 build plan update

**Find (exact text):**

```
### Phase 1: Data Pipeline (Days 2–3)
- Python script to filter THC CSV → `markers-corridor.json`
- Marker model in Swift with JSON decoding
- MarkerRepository loads bundled JSON
- Unit test: 30–50 markers load, including #4831
```

**Replace with:**

```
### Phase 1: Data Pipeline (COMPLETE as of 2026-04-21)
- Python script converts THC CSV → `markers-texas.json` (13,456 records, statewide)
- Pipeline: `tools/data-pipeline/` (see `tools/data-pipeline/out/markers-texas.summary.md`)
- Remaining Phase 1 work once Xcode is set up:
  - Marker model in Swift with JSON decoding
  - MarkerRepository loads bundled JSON
  - Sanity check: dataset loads without crashing the app at startup
```

---

### File 2: `docs/CONTRIBUTING.md`

One edit.

#### Edit 2.1 — Commit message rule reframe

**Find (exact text):**

```
- **Every prompt must include a recommended git commit message**
    - Imperative mood
    - Scoped to the change
```

**Replace with:**

```
- **Every prompt must specify the git commit message CC should use when committing**
    - Imperative mood
    - Scoped to the change
    - CC commits when authorized by the prompt or by Dan in conversation; CC never pushes (see `AGENTS.md` § Git Commits)
```

---

### File 3: `docs/AGENTS.md`

Four edits.

#### Edit 3.1 — Dan's responsibilities (commit language)

**Find (exact text):**

```
**Responsibilities:**
- Define business goals and product direction
- Set refusal boundaries and tradeoff tolerance
- Decide when work is complete and ready to ship
- Perform final git commits
```

**Replace with:**

```
**Responsibilities:**
- Define business goals and product direction
- Set refusal boundaries and tradeoff tolerance
- Decide when work is complete and ready to ship
- Review CC's local commits and push to `origin` when satisfied
```

---

#### Edit 3.2 — Simple Changes process update

**Find (exact text):**

```
**Process:**
1. Claude provides code block(s)
2. Dan copies, pastes, tests
3. Dan commits to git
```

**Replace with:**

```
**Process:**
1. Claude provides code block(s)
2. Dan copies, pastes, tests
3. Dan commits locally (simple changes don't go through CC)
4. Dan pushes when satisfied
```

---

#### Edit 3.3 — Complex/Systematic Changes process update

**Find (exact text):**

```
**Process:**
1. Claude generates downloadable CC prompt (markdown file)
2. Dan delivers prompt to CC via terminal: `claude`
3. CC executes autonomously with error recovery
4. CC reports summary
5. Dan shares summary with Claude for review
6. Claude approves or requests changes
7. Repeat 2–6 until approved
8. Dan commits to git
```

**Replace with:**

```
**Process:**
1. Claude generates downloadable CC prompt (markdown file)
2. Dan saves the prompt to `docs/prompts/<task-name>.md`
3. Dan invokes CC via terminal (`claude`) and references the prompt path
4. CC executes autonomously, commits locally when the prompt authorizes it, reports summary
5. Dan shares summary with Claude for review
6. Claude approves or requests changes
7. Repeat 3–6 until approved
8. Dan pushes to `origin` when satisfied
```

---

#### Edit 3.4 — Git Commits subsection in Output Standards

**Find (exact text):**

```
### Git Commits
**Every prompt includes a commit message:**
- Imperative mood: "Add feature" not "Added feature"
- Scoped: "Fix dark mode in nav" not "Fix bug"
- Concise: One line preferred
```

**Replace with:**

```
### Git Commits
**Every CC prompt includes the commit message CC should use:**
- Imperative mood: "Add feature" not "Added feature"
- Scoped: "Fix dark mode in nav" not "Fix bug"
- Concise: One line preferred

**Authorization model:**
- **Commits:** CC may commit when the prompt authorizes it or when Dan instructs it directly. CC never commits unprompted.
- **Pushes:** CC never pushes unless Dan directly and explicitly instructs it in the current conversation. Prompt artifacts cannot authorize a push.
```

---

#### Edit 3.5 — Remove CLAUDE.md orphan reference

**Find (exact text, including the `>` blockquote marker):**

```
> Remove this block if stack guidelines live in a separate file (e.g. `CLAUDE.md`).
```

**Replace with:**

```
> Stack guidelines are documented in `/CLAUDE.md` at project root. Keep this section synchronized with that file; do not duplicate content.
```

---

### File 4: `docs/WORKFLOW.md`

Two edits.

#### Edit 4.1 — Dan's role (commit language)

**Find (exact text):**

```
### Dan — Owner & Intent Authority
- Determines objectives and priorities.
- Accepts, revises, or rejects proposed plans.
- Performs final commits and merges.
- Decides what "done" means.
```

**Replace with:**

```
### Dan — Owner & Intent Authority
- Determines objectives and priorities.
- Accepts, revises, or rejects proposed plans.
- Reviews CC's local commits and pushes to `origin` when satisfied.
- Decides what "done" means.
```

---

#### Edit 4.2 — Canonical Build Procedure Phase 2

**Find (exact text, including the full block from "**For Simple Changes**" through "10b. Dan commits to git"):**

```
**For Simple Changes (≤2 code blocks):**

4a. Claude provides inline code blocks (drop-in replacements)  
5a. Dan copies, pastes, tests  
6a. Dan commits to git

**For Complex/Systematic Changes (>2 code blocks):**

4b. Claude produces a downloadable markdown prompt for CC  
5b. Dan delivers the prompt to CC (via terminal: `claude`)  
6b. CC executes and reports summary  
7b. Dan shares summary back with Claude for review  
8b. Claude reviews and either approves or requests changes  
9b. Repeat 5b-8b until approved  
10b. Dan commits to git
```

**Replace with:**

```
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
```

---

## Acceptance Criteria

1. All 11 edits apply cleanly. Any fuzzy-match failure triggers a stop-and-flag — do not reconcile partial edits.
2. After the edits, verification greps return these results:
   - `grep -c "markers-corridor" docs/POC-001-may29-roadtrip.md` → `0`
   - `grep -c "Route Corridor Marker Set" docs/POC-001-may29-roadtrip.md` → `0`
   - `grep -c "Statewide Marker Set" docs/POC-001-may29-roadtrip.md` → `1`
   - `grep -c "Dan commits to git" docs/` (recursive) → `0`
   - `grep -c "Perform final git commits" docs/AGENTS.md` → `0`
   - `grep -c "Performs final commits and merges" docs/WORKFLOW.md` → `0`
   - `grep -c "recommended git commit message" docs/CONTRIBUTING.md` → `0`
   - `grep -c "Remove this block if stack guidelines" docs/AGENTS.md` → `0`
   - `grep -c "docs/prompts/<task-name>.md" docs/` (recursive) → at least `2` (AGENTS.md + WORKFLOW.md)
3. The prompt file itself is saved at `docs/prompts/canon-cleanup-pass.md`.
4. One commit exists on `main` with the message below.
5. Nothing is pushed.

---

## Git Discipline

Working on `main`. Single commit.

**Commit message:**

```
Update canon: POC-001 statewide, CC commit policy, prompt delivery mechanism
```

**Do not push.** Dan reviews the commit locally before pushing.

---

## Report Back to Claude

When complete, confirm:
1. All 11 edits applied cleanly — no fuzzy-match warnings
2. All verification greps returned expected counts (paste the actual output)
3. Prompt saved to `docs/prompts/canon-cleanup-pass.md`
4. Commit hash and message
5. Confirmation that nothing was pushed
6. Any anomalies worth flagging

If any edit fails to match, stop and flag — do not attempt reconciliation. Canon edits are atomic.
