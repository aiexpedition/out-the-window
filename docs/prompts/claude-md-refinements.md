# CC Prompt — CLAUDE.md Refinements

**Target agent:** CC (Claude Code)
**Execution host:** Win11 dev rig, WSL
**Project root:** `/mnt/c/Users/wimbl/Projects/OTW`
**Branch:** `main`
**Related canon:** `CLAUDE.md` (project root)

---

## Context

CC reviewed the newly-added `CLAUDE.md` at project root and flagged three small drift risks. All three were accepted by Claude (Chief Architect). This prompt applies the agreed refinements.

No structural change, no new canon, no new behavior — just tightening CLAUDE.md so it ages well.

---

## Objective

Apply three surgical edits to `CLAUDE.md` at project root, commit the change, do not push.

---

## Scope

### In Scope
- Three `str_replace`-style edits to `CLAUDE.md` at project root
- One commit on `main` with the message specified below

### Out of Scope
- No other file edits
- No changes to `docs/` canon
- No changes to `tools/` or any code
- No push

---

## Edits

### Edit 1 — Soften the hard-coded marker count

**Location:** Section "Decisions That Change Behavior in Every Session," item 2.

**Find (exact text):**

```
2. **No curation of the POC marker set.** The POC ships all ~13,456 THC markers that pass objective quality filters (has inscription text + valid UTM coords). No corridor filter, no editorial selection, no family-history anchor markers. The product thesis being tested is *"proximity-triggered narration of objective Texas history feels meaningful"* — shaping the data set would invalidate the test.
```

**Replace with:**

```
2. **No curation of the POC marker set.** The POC ships all THC markers that pass objective quality filters (has inscription text + valid UTM coords) — roughly 13.5k records as of the April 2026 export. See `tools/data-pipeline/out/markers-texas.summary.md` for the current authoritative count. No corridor filter, no editorial selection, no family-history anchor markers. The product thesis being tested is *"proximity-triggered narration of objective Texas history feels meaningful"* — shaping the data set would invalidate the test.
```

**Rationale:** The hard-coded `~13,456` becomes stale if the CSV refreshes or filter rules change by a row. Soft reference + pointer to the summary report (the actual authoritative count) is drift-resistant.

---

### Edit 2 — Remove the `ios/` placeholder from the repo layout tree

**Location:** Section "Current Repository Layout," inside the fenced code block.

**Find (exact text, including tree characters):**

```
├── tools/                       Build-time tooling
│   └── data-pipeline/           Phase 1 — THC CSV → markers-texas.json
└── ios/                         iOS app (not yet scaffolded)
```

**Replace with:**

```
└── tools/                       Build-time tooling
    └── data-pipeline/           Phase 1 — THC CSV → markers-texas.json
```

**Rationale:** The `ios/` directory does not exist on disk. A reader running `ls` will see a mismatch. Per the Update Discipline section, CLAUDE.md is updated when a major subsystem comes online — `ios/` gets re-added when the iOS project is scaffolded, not before.

**Tree-character changes to note:**
- `├──` (branch) → `└──` (last entry) for `tools/`
- `│   └──` → `    └──` for `data-pipeline/` (parent is no longer a branch)

---

### Edit 3 — Add CLAUDE.md as first entry in Process canon

**Location:** Section "Canon Map," under the "**Process canon:**" heading.

**Find (exact text):**

```
**Process canon:**
- `docs/CONTRIBUTING.md` — agent roles and contribution rules
```

**Replace with:**

```
**Process canon:**
- `CLAUDE.md` — session orientation (this file), project root
- `docs/CONTRIBUTING.md` — agent roles and contribution rules
```

**Rationale:** Self-referential omission breaks any tool or session that scrapes the canon list. Adding the line makes the map complete.

---

## Acceptance Criteria

1. All three edits apply cleanly. No fuzzy matching — the `old_str` in each edit must match the current file byte-for-byte.
2. After the edits, `CLAUDE.md` contains:
   - No occurrence of the literal string `~13,456`
   - No occurrence of the literal string `└── ios/`
   - One occurrence of the line `` - `CLAUDE.md` — session orientation (this file), project root ``
3. The file is otherwise byte-identical to the pre-edit version.
4. One commit exists on `main` with the message specified below.
5. Nothing is pushed.

---

## Git Discipline

Working on `main`. Single commit after edits are applied.

**Commit message:**

```
Refine CLAUDE.md: soften marker count, remove ios/ placeholder, add self-reference to canon map
```

**Do not push.** Dan reviews the commit locally before pushing.

---

## Report Back to Claude

When complete, confirm:
1. All three edits applied — no fuzzy-match warnings
2. Verification grep results for the three acceptance criteria
3. Commit hash and message
4. Confirmation that nothing was pushed

If any edit failed to apply cleanly (e.g., because the file has already been partially edited), stop and flag — do not attempt a reconciliation. Canon edits should be atomic or not at all.
