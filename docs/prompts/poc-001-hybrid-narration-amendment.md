# CC Prompt — POC-001 Amendment (Hybrid Narration + Presentation Curation)

**Target agent:** CC (Claude Code)
**Execution host:** Win11 dev rig, WSL
**Project root:** `/mnt/c/Users/wimbl/Projects/OTW`
**Branch:** `main`
**Related canon:** `docs/POC-001-may29-roadtrip.md`

---

## Context

During the 2026-04-21 cleanup stream, Dan and Claude worked through the narration architecture in depth. Two decisions emerged that require amendment to POC-001:

1. **Decision 9** (captured in the architectural-decisions-v4 Olliver capsule) — POC narration is now hybrid: AVSpeechSynthesizer statewide, plus ~30–50 hand-curated pre-recorded narrations for markers along the May 29 route. This is a family-buy-in measure that respects Dan's "no data curation" rule (Decision 8) by curating at the presentation layer only, not the data layer.

2. **Fallback chain architecture** — `NarrationService` implements a three-tier fallback: cached recorded audio → dynamically fetched audio (production only) → AVSpeechSynthesizer. POC uses tiers 1 and 3; production adds tier 2 triggered by web-to-phone route queuing from the companion site.

Additionally, the "Does Not Need for POC" list has two stale lines: "Coverage beyond the McKinney→Leakey corridor" (contradicted by Decision 8's statewide bundle) and "Recorded voice narration" (contradicted by Decision 9's hybrid approach).

This prompt applies all POC-001 corrections in one atomic commit.

---

## Objective

Apply five surgical edits to `docs/POC-001-may29-roadtrip.md` reflecting Decision 9 and its consequences. Commit with the message below. Do not push.

---

## Scope

### In Scope
- Five `str_replace`-style edits to `docs/POC-001-may29-roadtrip.md`
- One commit on `main`

### Out of Scope
- No other file edits
- No changes to ADRs, CONTRIBUTING, AGENTS, WORKFLOW, or CLAUDE.md
- No changes to `tools/` or code
- No Olliver capsule edits (Claude handles those directly)
- No push

---

## Edits

Five edits. Apply in order. Any `old_str` failing byte-for-byte match triggers a stop-and-flag — do not reconcile.

---

### Edit 1 — Narration section rewrite

**Location:** "Scope — What the POC Is" → "Narration" subsection.

**Find (exact text):**

```
### Narration
- **POC approach:** AVSpeechSynthesizer (Apple's built-in TTS)
  - Default system voice
  - Rate and pitch tuned for clear comprehension at highway speeds
- **Content source:** THC marker `inscription` field, cleaned for TTS (remove bracketed notes, abbreviations expanded)
- **Audio session:** `.playback` category with `.duckOthers` option — ducks any concurrent audio (Apple Maps voice, music)
- **Not in POC:** Recorded voice narration, multiple voice options, custom narration scripts
```

**Replace with:**

```
### Narration (Hybrid — see Decision 9)
- **POC approach:** Hybrid two-tier `NarrationService` with a universal fallback chain
  - **Tier 1 — Cached recorded audio:** For ~30–50 markers along the May 29 route that Dan hand-curates (presentation curation only — the data layer stays fully statewide per Decision 8). Audio generated once via commercial TTS (ElevenLabs or similar), stored as `marker-{markerNum}.m4a`, bundled in the app binary at `Resources/narrations/`.
  - **Tier 3 — AVSpeechSynthesizer fallback:** Every marker not in the curated set. Rate and pitch tuned for highway-speed comprehension. Uses iOS 17+ premium system voices where available.
  - (Tier 2 — dynamically fetched audio — is production only, triggered by web-to-phone route queuing from the companion site. Not in POC scope.)
- **Lookup logic:** `if audioFile(for: marker.markerNum) exists → play it; else → speak(marker.narrationText)`. Clean seam between tiers.
- **Content source:** THC marker `markerText` field, cleaned for TTS (whitespace normalization, conservative abbreviation expansion, bracketed-note removal, smart-quote normalization). Cleaned text is stored as `narrationText` in the bundled JSON; pipeline already produced this.
- **Audio session:** `.playback` category with `.duckOthers` option — ducks any concurrent audio (Apple Maps voice, music). Background audio entitlement enabled.
- **Curation discipline:** Data curation (shaping which markers exist or fire) is prohibited. Presentation curation (which markers get recorded narration vs. TTS fallback) is permitted and expected. Every marker can still fire notifications; every notification can still be tapped.
- **Not in POC:** Dynamic audio fetch, companion site integration, user-selectable voices, server-side push, CarPlay narration routing.
```

---

### Edit 2 — "Does Not Need for POC" list cleanup

**Location:** "Scope — What the POC Is NOT" → the bulleted exclusion list.

**Find (exact text):**

```
- ❌ CarPlay integration (production phase)
- ❌ Liquid Glass / iOS 26 design (production phase — POC is iOS 17+ SDK)
- ❌ User accounts, authentication, or sync with companion site
- ❌ Subscription flow, StoreKit, paywall logic
- ❌ Android build
- ❌ Coverage beyond the McKinney→Leakey corridor
- ❌ Premium features: voice selection, genealogy, bookmarks sync
- ❌ Companion TALL website integration
- ❌ Push notifications server-side
- ❌ Analytics, crash reporting, telemetry beyond on-device logs
- ❌ App Store submission readiness
- ❌ Marketing/onboarding/polish
- ❌ Recorded voice narration
- ❌ Multi-language support
- ❌ Accessibility beyond what SwiftUI gives us for free
```

**Replace with:**

```
- ❌ CarPlay integration (production phase)
- ❌ Liquid Glass / iOS 26 design (production phase — POC is iOS 17+ SDK)
- ❌ User accounts, authentication, or sync with companion site
- ❌ Subscription flow, StoreKit, paywall logic
- ❌ Android build
- ❌ Premium features: user-selectable voices, genealogy, bookmarks sync
- ❌ Companion TALL website (including route planning & queuing — this is the production-grade trigger for recorded-narration downloads; POC hand-bakes the curated route set into the app binary instead)
- ❌ Dynamic audio fetch (tier 2 of the NarrationService fallback chain — production only)
- ❌ Push notifications server-side
- ❌ Analytics, crash reporting, telemetry beyond on-device logs
- ❌ App Store submission readiness
- ❌ Marketing/onboarding/polish
- ❌ Multi-language support
- ❌ Accessibility beyond what SwiftUI gives us for free
```

---

### Edit 3 — Phase 4 build plan update

**Location:** "Build Plan (High-Level Sequence)" → "Phase 4: Narration".

**Find (exact text):**

```
### Phase 4: Narration (Days 10–12)
- NarrationService using AVSpeechSynthesizer
- Audio session configured for `.playback` + `.duckOthers`
- Background audio entitlement enabled
- "Read Aloud" button on Marker Detail works
- Geofence entry triggers auto-narration
```

**Replace with:**

```
### Phase 4: Narration (Days 10–14)
- NarrationService with two-tier fallback chain (cached recorded audio → AVSpeechSynthesizer)
- Audio session configured for `.playback` + `.duckOthers`
- Background audio entitlement enabled
- "Read Aloud" button on Marker Detail works
- Geofence entry triggers auto-narration
- **Curation sub-phase:**
  - Build a small Python tool (`tools/route-preview/`) that filters `markers-texas.json` to the ~200–400 markers within 3 miles of the May 29 route polyline
  - Dan reviews the output and picks ~30–50 markers to narrate
  - ElevenLabs account setup, voice selection (consider voice cloning for emotional weight)
  - Batch audio generation: `marker-{markerNum}.m4a` for each curated marker
  - Audio files bundled in Xcode under `Resources/narrations/`
- Both tiers verified end-to-end before moving to Phase 5
```

---

### Edit 4 — Success criteria refinement

**Location:** "Success Criteria" → "Must-Pass" list, item about narration quality.

**Find (exact text):**

```
3. **Narration quality is adequate for comprehension at 60–70 mph** — audible over road noise, clearly paced, ducks other audio properly.
```

**Replace with:**

```
3. **Narration quality is adequate for comprehension at 60–70 mph** — audible over road noise, clearly paced, ducks other audio properly. Curated recorded narrations (tier 1) should feel materially warmer than AVSpeech fallback (tier 3) — the hybrid approach is only worth the effort if the family notices the difference on the drive.
```

---

### Edit 5 — Technical Approach architecture tree update

**Location:** "Technical Approach" → "Architecture (POC-scope)" code block, where the Resources subtree is listed.

**Find (exact text):**

```
└── Resources/
    └── markers-texas.json          (bundled ~13.5k markers, statewide)
```

**Replace with:**

```
└── Resources/
    ├── markers-texas.json          (bundled ~13.5k markers, statewide)
    └── narrations/                 (bundled recorded audio for ~30-50 curated markers)
        ├── marker-4831.m4a         (example: one curated file per markerNum)
        └── marker-{markerNum}.m4a
```

---

## Acceptance Criteria

1. All 5 edits apply cleanly. Any fuzzy-match failure triggers stop-and-flag.
2. Verification greps:
   - `grep -c "Hybrid two-tier" docs/POC-001-may29-roadtrip.md` → `1`
   - `grep -c "Coverage beyond the McKinney→Leakey corridor" docs/POC-001-may29-roadtrip.md` → `0`
   - `grep -c "Recorded voice narration" docs/POC-001-may29-roadtrip.md` → `0` (the specific `❌ Recorded voice narration` exclusion line, which is no longer true)
   - `grep -c "marker-{markerNum}.m4a" docs/POC-001-may29-roadtrip.md` → at least `2` (narration section + architecture tree)
   - `grep -c "presentation curation" docs/POC-001-may29-roadtrip.md` → at least `1`
   - `grep -c "Phase 4: Narration (Days 10–14)" docs/POC-001-may29-roadtrip.md` → `1`
3. One commit on `main` with the message below.
4. Nothing pushed.

---

## Git Discipline

Working on `main`. Single commit.

**Commit message:**

```
Amend POC-001 with hybrid narration and presentation curation
```

**Do not push.** Dan reviews locally before pushing.

---

## Report Back to Claude

When complete, confirm:
1. All 5 edits applied cleanly — no fuzzy-match warnings
2. All verification greps returned expected counts (paste actual output)
3. Commit hash and message
4. Confirmation that nothing was pushed
5. Any anomalies worth flagging

If any edit fails to match, stop and flag. Canon edits are atomic.
