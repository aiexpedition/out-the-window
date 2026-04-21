# ADR-002: Development Environment & Hardware Strategy

**Status:** Accepted
**Date:** 2026-04-20
**Decision Authority:** Dan (Product Owner)
**Architectural Author:** Claude (Chief Architect)
**Related:** ADR-001 (Mobile Framework Selection)

---

## Decision

**Out the Window will be built in two toolchain phases:**

1. **POC Phase (now through May 29, 2026):** iMac Pro (2017) running macOS Sequoia 15 with Xcode 16 and iOS 18 SDK. Target iOS 17+ minimum deployment. Focus: functional proof of GPS / proximity / narration / offline marker retrieval during the McKinney → Leakey road trip.

2. **Production Phase (post-WWDC 2026 through launch):** Apple Silicon Mac mini (M5 expected, purchased after WWDC 2026 announcement) running macOS Tahoe 26+ with Xcode 26 and iOS 26 SDK. Target iOS 26+ minimum deployment. Focus: Liquid Glass adoption, CarPlay integration, subscription flow, App Store submission readiness.

---

## Context

### Hardware Constraints

Dan's available Apple hardware:
- **iMac Pro (2017):** 10-core Intel Xeon W, 32 GB RAM, Radeon Pro Vega 56, Samsung NVMe. Running macOS Sequoia 15.7.4. Workstation-class machine, capable but aging.
- **MacBook Air (Apple Silicon):** Used for RustDesk into Win11 dev rig today. Minor role.
- **Win11 dev rig:** Ryzen 7 5700X, 64 GB RAM, RTX 3090, NVMe. Primary daily driver for chat with Claude.

### macOS and Xcode Runway on iMac Pro

- iMac Pro (2017) **cannot run macOS Tahoe 26** — officially dropped by Apple
- Sequoia 15 is the final macOS supported on this hardware
- Xcode 16 is the latest Xcode compatible with Sequoia 15
- **Xcode 26 requires Tahoe 26.2+** — unreachable on this hardware

### App Store Submission Requirement

Apple has confirmed a hard deadline:

> **Starting April 28, 2026, apps and games uploaded to App Store Connect must be built with Xcode 26 or later using an SDK for iOS 26, iPadOS 26, tvOS 26, visionOS 26, or watchOS 26.**

The iMac Pro cannot submit to the App Store after April 28, 2026. The POC does not require App Store submission (installed via Xcode direct-to-device for the road trip), so this hardware remains viable for POC phase only.

### Mac mini M4 Availability Crisis (as of April 20, 2026)

Mac mini M4 supply is severely constrained:
- Base $599 M4 model: ~1 month shipping delay
- 32 GB RAM configs: currently unavailable, no ship estimate
- M4 Pro 64 GB configs: 16–18 weeks, or unavailable
- Dual drivers: global DRAM shortage (AI server demand) + Apple winding down M4 production ahead of M5

### WWDC 2026 Timing

WWDC 2026 is confirmed for the week of June 8, 2026 — roughly 10 days after the POC road trip. M5 Mac mini announcement is widely expected at this event, with shipping likely in summer 2026.

### Ecosystem Forcing Function

iOS 26 introduces Liquid Glass as the system-wide design language. Apps rebuilt on Xcode 26 automatically adopt Liquid Glass for standard controls. Apple has stated the opt-out will be removed in iOS 27, making full adoption effectively mandatory for any serious product shipping in late 2026 or beyond.

---

## Rationale

### Why Not Buy Mac mini M4 Now

1. **Supply crisis.** Even the base $599 model ships in ~1 month — may arrive after May 29 POC deadline.
2. **M5 imminent.** Buying M4 in April means paying for soon-to-be-superseded silicon. WWDC 2026 is 10 days after POC.
3. **No POC benefit.** The POC is functional proof, not design polish. iOS 18 SDK on Xcode 16 exercises every technical capability the POC needs to prove.
4. **Dan's own guidance:** UI polish is secondary to functional correctness.

### Why iMac Pro Suffices for POC

The POC's technical requirements are fully served by iOS 18 SDK on Xcode 16:
- CoreLocation, significant-location-change, region monitoring
- MapKit and offline tile loading
- AVSpeechSynthesizer and AVFoundation audio mixing
- BackgroundTasks for sync and preload
- Local storage (SwiftData available iOS 17+)
- URLSession for backend sync with the TALL companion site

None of the blocking POC capabilities require iOS 26-specific APIs.

### Why Commit to M5 Mac mini for Production

1. **CarPlay is Out the Window's defining feature** (ratified by Dan, 2026-04-20). CarPlay requires native Swift; native Swift requires current Xcode; current Xcode requires current macOS; current macOS requires Apple Silicon.
2. **Liquid Glass adoption is non-negotiable for a late-2026 launch.** Apps shipping against iOS 18 SDK in late 2026 will feel dated on day one.
3. **Foundation Models framework** becomes available for premium features (on-device narration refinement, marker Q&A, trip summaries) at zero inference cost — substantial for a $24.99 subscription product.
4. **Longest software runway.** M5 silicon bought in summer 2026 should receive Apple software support through 2032+ — covers the full v1 through v5 arc of Out the Window.

### Why Not an M2/M3 Refurbished Intermediate

Considered and rejected for this context:
- Saves ~$100–300 vs. new M5
- Loses 1–2 years of software support runway at the end
- Still requires a purchase decision now, during supply crisis
- Doesn't meaningfully accelerate the POC (POC works on iMac Pro)
- Introduces a migration event before the M5 migration — two hardware transitions instead of one

For a project with a multi-year runway, buy the best silicon available at the decision point. The decision point is post-WWDC 2026, not today.

---

## The Migration Event

Between POC and production launch, a deliberate migration occurs. This is **an accepted cost**, not a surprise.

### What Migrates Trivially
- All Swift source code (language is source-stable across SDK versions)
- Business logic, models, networking
- CoreLocation, MapKit, AVFoundation usage (APIs are additive)
- Data schemas and persistence
- Git history and project structure

### What Requires Active Rework
- **UI layer adoption of Liquid Glass** — custom views may need `glassEffect` modifiers, visual refresh against new system materials
- **Minimum deployment target raise** — iOS 17+ → iOS 26+, removing backward-compatibility branches
- **Adoption of iOS 26-only APIs** — Foundation Models, new SwiftUI primitives, `@Animatable` macro, rich text editing, SwiftUI WebView
- **CarPlay integration** — wholly new work, not migration
- **StoreKit 2 subscription flow** — can be built on iMac Pro, but subscription testing is easier on current tooling

### Migration is a Project Milestone, Not a Risk
The migration is scheduled work with clear boundaries. It is not:
- A rewrite
- A risk to canon or architecture
- A reason to rethink the framework decision (ADR-001)
- A reason to regret the POC phase on older tooling

---

## Consequences

### Accepted Costs
- **Two-phase toolchain.** Project moves from Xcode 16 → Xcode 26 once, with planned migration work.
- **POC is not launch-ready code.** The POC codebase is architectural scaffolding, not production. Core services (GPS, narration, data layer) carry forward; UI is rebuilt.
- **CarPlay is deferred to production phase.** Not in scope for May 29 road trip.
- **Hardware spend deferred, not avoided.** M5 Mac mini purchase expected summer 2026. Estimated $599–$999 depending on config.

### Gained Benefits
- **Unblocks POC work today** without waiting for hardware availability
- **Avoids buying into M4 tail end** during active supply crisis
- **Hardware purchase informed by WWDC announcements** — Dan sees the M5 line before spending
- **iMac Pro's useful life gets one more productive chapter** before retirement as family machine
- **Production build lands on current Apple silicon and current Apple design language** — strongest possible launch position

### Deferred Decisions
- Exact Mac mini M5 configuration (RAM, storage) — decide when Apple announces pricing and specs
- Whether to add a display to the Mac mini setup, or keep it purely headless + HP S430c PIP
- When to stop developing on iMac Pro and fully migrate (likely mid-June 2026)

---

## Impact on ADR-001

ADR-001 specified "iOS 17+ minimum deployment target" as a conservative default. This ADR refines that to a **phased deployment target**:

| Phase | Deployment Target | Rationale |
|---|---|---|
| POC (through May 29, 2026) | iOS 17+ | Broadest device coverage for internal testing; uses Xcode 16 SDK |
| Production (late 2026 / early 2027 launch) | iOS 26+ | Liquid Glass adoption, Foundation Models, current SwiftUI APIs |

All other decisions in ADR-001 stand unchanged: Swift/SwiftUI native, iOS-first, Android deferred, CarPlay as defining feature.

---

## Revisit Conditions

Revisit this ADR if:

1. **M5 Mac mini is not announced at WWDC 2026** or is announced at a price/spec that makes M4 the better buy — revise to "buy M4 Mac mini when available"
2. **Mac mini supply crisis worsens into Q3 2026** — may need to consider MacBook Pro or iMac Apple Silicon as production machine
3. **iMac Pro hardware fails during POC phase** — forces immediate hardware decision under pressure
4. **Apple announces a surprise policy change** extending iOS 18 SDK submission support (highly unlikely)
5. **POC reveals architectural assumptions that force framework reconsideration** — triggers ADR-001 revisit, not this one

---

## Related Canon

- `ADR-001-mobile-framework.md` — framework selection
- `CLAUDE.md` — project overview (needs update to reference this ADR)
- `WORKFLOW.md` — interaction modes and delivery rules
- `AGENTS.md` — agent role boundaries

---

## Git Commit Message

```
Add ADR-002: Phased development environment strategy (iMac Pro POC → M5 Mac mini production)
```
