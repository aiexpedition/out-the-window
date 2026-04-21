# POC-001: Out the Window — May 29 Road Trip Spec

**Status:** Accepted
**Date:** 2026-04-20
**Decision Authority:** Dan (Product Owner)
**Architectural Author:** Claude (Chief Architect)
**Related:** ADR-001 (Mobile Framework), ADR-002 (Development Environment)
**POC Target Date:** May 29, 2026

---

## Purpose

This document defines the **scope, success criteria, and technical approach** for the Out the Window proof-of-concept.

The POC is **functional proof, not launch product.** Its single job is to answer one question:

> *Does the core experience work — driving past a Texas historical marker, in a real vehicle, in real conditions, and having Out the Window deliver the narration at the right moment?*

If the answer is yes on May 29, the product thesis is validated and production work begins.
If the answer is no, we learn why and adjust.

---

## The Defining Scene

The POC succeeds when the core experience works on a real drive, with real data, under real conditions — not staged, not curated, not shaped toward any particular outcome.

The ideal form of that scene looks like this:

It is the afternoon of May 29, 2026. Dan is driving south on US-83 through Real County, approaching the turn-off for the Cooper Maxwell Ranch (29.746570, -99.749325 — about a mile east of Leakey). His iPhone is in a cradle on the dashboard. The truck radio is off or playing quietly.

Throughout the drive, the phone has spoken — dozens of times, in dozens of places, as the truck crossed an objectively-selected slice of Texas history along a specific highway corridor. Some of it was famous. Some of it was obscure. Some of it was about people Dan had never heard of; some of it was about country his family has lived in since the 1800s. None of it was curated to be meaningful. It was meaningful because it was there.

As the truck approaches a historical marker along US-83 — whichever marker the algorithm's geographic filter includes — the phone speaks. The narration plays. The truck passes. The narration fades. And the next marker is ahead somewhere.

**If that experience works across the full drive — not just at one anchor moment, but consistently, from McKinney through Fort Worth through the Hill Country to the ranch — the POC succeeded.**

The product thesis is: *this mechanism delivers meaningful history to drivers who didn't know the history was there.* Proving that thesis requires the data to be objective. Otherwise we're just proving that a hand-built experience feels good, which was never in doubt.

Everything in this spec exists to test that thesis honestly.

---

## Scope — What the POC Is

### Route

- **Origin:** McKinney, TX
- **Destination:** Cooper Maxwell Ranch (Real County) — entrance at **29.746570, -99.749325**, approximately 1 mile east of Leakey, TX
- **Approximate distance:** ~370 miles
- **Expected duration:** ~6.5 hours driving time

**Highway sequence (the actual route, not I-35):**

| Leg | Highway | Region |
|---|---|---|
| 1 | TX-121 southwest | Out of McKinney, through DFW northern suburbs |
| 2 | TX-121 / US-183 | Transition through mid-cities |
| 3 | I-820 | Fort Worth loop |
| 4 | I-30 west | Fort Worth → Weatherford area |
| 5 | I-20 west | Weatherford → Cisco / Eastland area |
| 6 | US-183 south | Turn off I-20, through central Texas |
| 7 | US-377 south | Brownwood area |
| 8 | US-190 | Central Texas crossing |
| 9 | US-83 south | Long run through the Hill Country into Real County |
| 10 | Ranch entrance road | Final mile into the ranch |

**Why this matters for marker curation:** This is a west-then-south route, not the direct I-35 path through Austin and San Antonio. The corridor passes through West Texas country with different marker density and different history than an I-35 route would — more Comanche frontier history, more Texas Ranger country (including McNelly territory), fewer urban markers.

The route passes near or through Real County's sister counties on the Edwards Plateau, crossing country where Dan's family history is written into the land itself.

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

### Proximity Detection Behavior

- **Approach radius:** 0.5 miles (≈800 meters) from marker coordinates
  - Triggers local notification when user enters the radius
  - Direction-agnostic: fires whether user is driving toward, away from, past, or parked near the marker
- **Notification cooldown:** Once a marker has fired a notification in a session, it does not fire again for 24 hours (prevents repeat firing on U-turns, return trips, or loop drives)
- **Speed filter:** Notifications suppressed when speed has been below 5 mph for more than 2 minutes (user is parked/stopped). Pre-existing notifications in the notification center remain tappable.

### Narration
- **POC approach:** AVSpeechSynthesizer (Apple's built-in TTS)
  - Default system voice
  - Rate and pitch tuned for clear comprehension at highway speeds
- **Content source:** THC marker `inscription` field, cleaned for TTS (remove bracketed notes, abbreviations expanded)
- **Audio session:** `.playback` category with `.duckOthers` option — ducks any concurrent audio (Apple Maps voice, music)
- **Not in POC:** Recorded voice narration, multiple voice options, custom narration scripts

### UI — Minimum Viable
- **Map View (primary screen):**
  - Full-screen MapKit map
  - User's current location (standard blue dot)
  - Pins for upcoming markers on the route
  - A "now approaching" card overlay when inside an approach radius
- **Marker Detail View:**
  - Marker title, county, inscription text, distance
  - "Read Aloud" button (manual trigger for narration)
- **Debug/Dev View (for road trip diagnostics):**
  - Current GPS coordinates
  - Speed and heading
  - Nearest marker + distance
  - Last geofence event log
  - Audio session status

### Platform
- **Target device:** Dan's iPhone (iOS 17+)
- **Installation:** Direct install via Xcode to device using Dan's Apple ID (free sideload, re-signed every 7 days as needed)
- **No App Store, no TestFlight, no paid Developer account required for POC**

---

## Scope — What the POC Is NOT

**Explicitly out of scope for May 29:**

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

These are not forgotten. They are deferred to production phase explicitly.

---

## Success Criteria

The POC is successful if, on May 29, 2026:

### Must-Pass
1. **The mechanism works.** Multiple markers along the route trigger narration at appropriate times as the truck approaches them. The specific markers are whatever the data contains; the test is that the triggering mechanism is correct and reliable.
2. **Reliability threshold:** At least 70% of markers that should trigger (based on drive path and marker proximity) do trigger. A single missed marker is acceptable; systematic failure is not.
3. **Narration quality is adequate for comprehension at 60–70 mph** — audible over road noise, clearly paced, ducks other audio properly.
4. **No crashes.** App runs continuously through the drive without force-quitting.
5. **Battery budget:** Phone remains usable at end of drive (not drained by background GPS). Vehicle charging allowed.

### Should-Pass
6. **Dead zone resilience:** When cell service drops (guaranteed in the Hill Country), narration continues from bundled data. App does not hang or error.
7. **Speed awareness:** App does not trigger narration when parked at a gas station near a marker for 20 minutes.
8. **Duplicate suppression:** Driving past the same marker twice (if route has a loop-back) does not re-trigger narration within the hour.
9. **Density handling:** In marker-dense areas (e.g., small towns with multiple markers within a mile), the app handles overlapping approach radii sensibly — no stacked narrations, no cut-offs mid-inscription.

### Nice-to-Have
10. **Map UI is useful in glance:** Dan can look at the phone for 1–2 seconds and understand what's ahead.
11. **Debug view is informative:** Dan can diagnose issues from the debug screen without needing Xcode.

### Explicitly Not Required
- Visual polish
- Empty state handling
- Error messaging design
- Smooth animations
- Tested on multiple iOS versions
- Tested on multiple devices

---

## Technical Approach

### Architecture (POC-scope)

```
OutTheWindow/
├── App/
│   ├── OutTheWindowApp.swift       (entry point)
│   └── RootView.swift              (map vs. detail vs. debug routing)
├── Features/
│   ├── Map/
│   │   ├── MapView.swift           (MapKit + overlays)
│   │   └── ApproachingCard.swift   (the "now approaching" overlay)
│   ├── MarkerDetail/
│   │   └── MarkerDetailView.swift
│   └── Debug/
│       └── DebugView.swift
├── Services/
│   ├── LocationService.swift       (CoreLocation wrapper)
│   ├── GeofenceService.swift       (region monitoring, approach/pass logic)
│   ├── NarrationService.swift      (AVSpeechSynthesizer + AVAudioSession)
│   └── MarkerRepository.swift      (loads bundled markers, queries by location)
├── Models/
│   └── Marker.swift                (core data model)
└── Resources/
    └── markers-corridor.json       (bundled 30–50 markers)
```

**Design principles:**
- Services are plain Swift classes with clear single responsibilities
- Views use `@Observable` classes for state (iOS 17+ Observation framework)
- No external dependencies — pure Apple frameworks only
- No persistence beyond bundled JSON — SwiftData is production-phase concern
- Logging via `os.Logger` to Console for road-trip diagnostics

### Data Preparation (Pre-Build Task)

Before writing Swift code, a corridor marker dataset must exist:

1. **Define the route polyline.** Build a geographic line representation of the actual highway route (McKinney → Fort Worth loop → I-20 west → US-183 → US-377 → US-190 → US-83 → Leakey).
2. **Filter THC Historical Marker CSV** for markers within a defined radius of the polyline (recommend 3 miles either side — tunable based on what we see in the dataset).
3. **Validate data quality:** every included marker must have lat/long and inscription text. Drop markers with incomplete data.
4. **Clean inscription text for TTS:** expand abbreviations, remove bracketed editorial notes, normalize punctuation for natural speech cadence.
5. **Export to `markers-corridor.json`** bundled in app resources.

The filter is mechanical and reproducible. No hand-selection, no inclusion or exclusion based on content. The same script run against the same data produces the same output. Whoever runs it gets the same markers.

This can be done in Python on the Win11 rig and doesn't require the Mac. Output is likely 100–500 KB JSON.

### The Proximity Detection Loop

Simplified pseudocode for the core experience:

```
On location update:
  For each marker in bundled corpus:
    distance = currentLocation.distance(to: marker.location)

    if distance < approach_radius AND marker not recently notified:
      if speed_filter_permits:
        send local notification: "Marker ahead: {title}"
        mark marker as "notified"

On notification tap:
  Route to MarkerDetailView for the tapped marker
  Begin narration automatically
  Configure audio session for .playback + .duckOthers

Speed filter:
  if speed < 5mph sustained for >2 minutes:
    suppress new notifications (user is parked/stopped)
  otherwise:
    permit notifications
```

**Direction-agnostic.** No heading check, no route-matching at runtime. Proximity is the only trigger.

**Implementation note:** CLLocationManager's region monitoring (geofences) is more battery-efficient than continuous distance calculation, but has a hard limit of 20 simultaneous regions per app. For a bundled corpus of 100–300 markers, a hybrid approach is needed: maintain an active geofence for the N closest markers, refreshing the set as the user moves. When a geofence fires, emit the notification.

### Battery Strategy

- Use `CLActivityType.automotiveNavigation` for location manager
- Use `significantLocationChanges` as the baseline wake trigger, with `startUpdatingLocation` during active narration windows
- Keep screen in low-power state — no animations, minimal rendering
- Dark mode default (OLED battery win)

---

## Resolved Design Decisions

These were open at draft; Dan resolved them on 2026-04-20.

### 1. Notification-first, user-initiated playback

**Decision:** When approaching a marker, the app sends a notification. The user taps the notification to hear narration. Narration does not auto-play on approach.

**Rationale:** The user decides what's interesting. Not every marker along a route will interest every traveler. Respecting user agency means offering, not imposing. This also eliminates a class of edge cases (speed awareness for narration triggering, duplicate suppression, mid-narration interruption handling).

**Implication:** The app needs reliable local notification delivery, even when backgrounded or screen-locked. Notification tap must deep-link into the app with the specific marker loaded and ready to play.

### 2. Manual "Start Trip" trigger

**Decision:** User explicitly taps "Start Trip" to begin marker detection. No auto-detection based on speed or movement patterns.

**Rationale:** Explicit, debuggable, simple. Auto-detection is a production-phase refinement.

**Implication:** App has a clear active/inactive state. When inactive, no location monitoring, no notifications. When active, full monitoring until user taps "End Trip" or closes the app.

### 3. Auto-play after notification tap

**Decision:** Tapping the notification launches the app into the Marker Detail view with narration already playing.

**Rationale:** Once the user has opted in by tapping, the narration should be immediate. No "tap to play" button adds friction without value at that point.

**Implication:** Notification handler must route directly to narration start, not just navigation to the marker view.

### 4. Portrait orientation only

**Decision:** App locks to portrait orientation for POC.

**Rationale:** Simplest layouts, fewer SwiftUI preview configurations, matches typical phone-cradle orientation. Landscape is a production-phase consideration.

### 5. Proximity-based POI detection (direction-agnostic)

**Decision:** The app detects markers based on proximity to current location, regardless of travel direction. A marker within the approach radius fires a notification whether the user is driving toward it, away from it, past it, or parked near it (subject to speed filter — see below).

**Rationale:** Mirrors how native iOS POI discovery works (Apple Maps, Find My). Simpler to implement than directional logic. More forgiving of real-world driving patterns (U-turns, detours, scenic loops). Matches user expectation: *"if a marker is near me, tell me about it."*

**Implication:** No route polyline matching at runtime. No heading-based filtering. The app maintains a set of markers and continuously evaluates proximity. Corridor polyline is used ONLY at data-prep time to decide which markers to bundle, not at runtime to decide which are relevant.

**Speed filter (still needed):** To avoid nuisance notifications while stopped at a gas station near a marker, the app suppresses new notifications when speed has been below ~5 mph for more than 2 minutes. Already-fired notifications remain tappable.

---

## Build Plan (High-Level Sequence)

This is the work breakdown. Each phase has a clear acceptance point.

### Phase 0: Environment Setup (Days 1–2)
- Xcode 16 installed on iMac Pro
- Apple ID signed in for device signing
- Empty Xcode project created, git initialized
- Hello World builds and runs in Simulator
- Hello World builds and runs on Dan's actual iPhone

### Phase 1: Data Pipeline (Days 2–3)
- Python script to filter THC CSV → `markers-corridor.json`
- Marker model in Swift with JSON decoding
- MarkerRepository loads bundled JSON
- Unit test: 30–50 markers load, including #4831

### Phase 2: Map + Markers (Days 4–6)
- MapView with current location
- Marker pins rendered from repository
- Tap pin → Marker Detail view
- Marker Detail shows title, county, inscription text

### Phase 3: Location Services (Days 7–9)
- LocationService with CoreLocation permissions
- GeofenceService with approach radius logic
- Debug view shows live GPS + nearest marker
- Test while driving around McKinney to validate geofence behavior

### Phase 4: Narration (Days 10–12)
- NarrationService using AVSpeechSynthesizer
- Audio session configured for `.playback` + `.duckOthers`
- Background audio entitlement enabled
- "Read Aloud" button on Marker Detail works
- Geofence entry triggers auto-narration

### Phase 5: Integration + Dogfood (Days 13–18)
- Start Trip button wires everything together
- Drive around DFW metro testing approach/pass behavior with nearby markers
- Fix bugs, tune geofence radii, refine TTS pacing
- Test with iPhone locked, in pocket, in cradle

### Phase 6: Dress Rehearsal (Days 19–25)
- Drive a shorter test route (e.g., McKinney → Waco → back)
- Fix whatever breaks at scale / speed / distance
- Battery budget validation on 3+ hour drives

### Phase 7: Road Trip (May 29)
- Execute the real McKinney → Leakey trip
- Collect feedback, log issues, note successes
- Take notes for post-POC review

**Timeline pressure:** Phases 0–5 consume ~3 weeks. Phases 6–7 consume ~1 week each. This assumes Dan working on Out the Window evenings/weekends alongside day job. If day job demands more time, Phases 5–6 compress first.

---

## Dependencies & Risks

### Dependencies
- iMac Pro remaining functional through May 29
- Dan's iPhone remaining functional and with enough free storage
- THC marker data remains as-is (commercial rights ONLY affect public distribution, not personal POC use — verified with Dan)
- Vehicle (truck) functional for the trip itself
- Favorable weather (not a hard dependency, but flooding on Hill Country roads is a real risk in late May)

### Risks

| Risk | Mitigation |
|---|---|
| Xcode 16 download fails on iMac Pro (unavailable via App Store) | Use Apple Developer Downloads portal to get Xcode 16.x directly |
| Geofencing accuracy poor in rural Texas | Fall back to distance polling; tune radii after test drives |
| TTS unintelligible at highway speed | Record backup audio for top 10 markers; validate in dress rehearsal |
| Battery drain unacceptable | Use significant-location-change + active window pattern; require vehicle charging |
| Cell service unavailable = app hang | All data bundled in app; no runtime network calls in POC |
| iPhone overheats in cradle in Texas sun | Ventilated cradle, sun shade, moderate GPS polling rate |
| Weather cancels the trip | POC deferred by 1–2 weeks — timeline slips but not lost |
| Apple Silicon Mac mini delay extends POC | Doesn't affect POC (iMac Pro carries it); only affects post-POC production |

### Non-Risks (Called Out Explicitly)
- **Commercial rights pending:** Does not block POC. THC marker data is publicly available and using it on a personal device for a personal road trip is not distribution. Commercial rights become a blocker for App Store launch, not POC.
- **CarPlay not ready:** Explicitly out of scope.
- **Liquid Glass design:** Explicitly out of scope.

---

## Post-POC Review

On or shortly after May 29, conduct a review:

1. **What worked?** Which aspects of the experience felt magical?
2. **What broke?** Crashes, missed narrations, timing issues.
3. **What felt wrong?** Narration too fast? Geofences too tight? Map unhelpful?
4. **What's the backlog for production?** Everything the POC deferred.
5. **Does the product thesis hold?** Is Out the Window worth building into production?

This review drives the next planning cycle and informs whether the M5 Mac mini purchase happens immediately after WWDC or waits.

---

## Git Commit Message

```
Add POC-001: May 29 road trip scope and success criteria
```
