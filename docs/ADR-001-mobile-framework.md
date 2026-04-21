# ADR-001: Mobile Framework Selection

**Status:** Accepted
**Date:** 2026-04-20
**Decision Authority:** Dan (Product Owner)
**Architectural Author:** Claude (Chief Architect)

---

## Decision

**Out the Window will be built as a native iOS application using Swift and SwiftUI.**

- **Language:** Swift 5.10+
- **UI Framework:** SwiftUI (with UIKit bridges where required — notably CarPlay)
- **Minimum iOS Version:** iOS 17+
- **Android:** Deferred to a future project. Not in scope for POC or v1 launch.

---

## Context

Out the Window is a GPS-aware mobile companion for Texas historical markers, designed to narrate history to road-trippers as they approach points of interest. The product requires:

- Continuous background location tracking while driving
- Geofencing and proximity-triggered notifications
- Offline map tiles and marker data (rural Texas cell coverage is unreliable)
- Text-to-speech narration with voice selection
- Audio playback with mixing/ducking for road environments
- Route preload (corridor-based marker caching)
- Local storage for bookmarks, cached narration, user data
- Subscription billing ($24.99/6-month, $39.99/year)
- Sync with TALL-stack companion website
- **CarPlay integration (product-defining feature in roadmap)**

Dan is a solo operator working with Claude (Chief Architect) and CC (Execution Agent). POC target is May 29, 2026 (McKinney → Leakey road trip).

---

## Options Considered

### 1. Flutter (Dart)
**Strengths:** Single codebase covers iOS and Android. Strong location and mapping packages. Dart is approachable. Excellent performance.

**Weaknesses:** CarPlay integration is poor — community packages are sparse, unofficial, and lag Apple's annual updates. StoreKit integration adds a bridging layer. iOS polish ceiling is lower than native.

### 2. React Native (Expo)
**Strengths:** JavaScript/TypeScript ecosystem. Expo dev experience is excellent for solo devs. EAS handles builds and submissions.

**Weaknesses:** Background location historically finicky. CarPlay support is even weaker than Flutter. Native module debugging is painful. Dropped after confirming CarPlay is in the product vision.

### 3. Swift / SwiftUI Native (**SELECTED**)
**Strengths:** Best-in-class integration with CoreLocation, MapKit, AVFoundation, StoreKit 2, BackgroundTasks, and CarPlay. Apple's geofencing APIs are purpose-built for this use case. Cleanest path to App Store approval and CarPlay entitlement. Highest iOS quality ceiling.

**Weaknesses:** Android becomes a full rewrite (3–5 months of solo work) when that milestone comes. No code sharing across platforms.

### 4. Hybrid (Capacitor/Ionic)
**Rejected outright.** Background GPS and offline performance are exactly where hybrid frameworks fail. Not a serious contender for a driving app.

---

## Rationale

The decision hinges on three factors:

### 1. CarPlay is the product's defining moment
CarPlay is not a nice-to-have — it is the magic moment that justifies a $24.99 subscription. Phone in the cradle, narration through truck speakers, glanceable marker information on the dashboard. CarPlay uses UIKit-based templates (`CPListTemplate`, `CPMapTemplate`, `CPPointOfInterestTemplate`, `CPNowPlayingTemplate`) that native Swift apps integrate naturally. Flutter and React Native must bridge these through platform channels using unofficial, community-maintained packages that lag Apple's annual iOS releases.

Apple also gates CarPlay entitlements through a review process. A native Swift app with clean CarPlay integration has a materially better shot at approval than a bridged implementation.

### 2. The US market and target demographic skew iOS
- iOS holds ~60% of the US smartphone market
- iPhone users skew higher-income, higher-education, and spend ~7× more on apps than Android users
- The App Store captures ~67% of global app spending
- Suburban Texas road-trippers — the actual target — index even higher toward iPhone

iOS-only launch addresses an estimated 75–80% of the addressable *revenue* opportunity, not 60%.

### 3. Write it once, properly
Dan's stated preference: the POC codebase becomes the production codebase. Native Swift delivers the highest-quality iOS experience, with no framework tax on platform-specific capabilities. Android, when it comes, will be a separate focused project — not a retrofitted compromise.

---

## Consequences

### Accepted Costs
- **Android is a full rewrite later.** Estimated 3–5 months of solo work to reach parity when the time comes. This is an acknowledged and accepted cost.
- **No code sharing between platforms.** Business logic, UI, and platform integration will live only in the Swift codebase. `/docs` canon, data schemas, and TALL backend API contracts remain platform-agnostic and carry over.
- **Apple Developer Program:** $99/year (required regardless of framework choice).

### Gained Benefits
- Best-possible iOS app experience for a GPS/audio/driving use case
- Clean path to CarPlay entitlement and implementation
- Faster App Store review cycle
- Native StoreKit 2 for subscriptions (no bridging layer)
- SwiftUI's declarative model maps cleanly to Dan's existing Livewire mental model
- Smaller binary, faster cold start, better battery behavior

### Deferred Questions
- Android timeline — to be revisited after iOS v1 ships and has subscriber traction
- Cross-platform shared layer (e.g., Rust/Kotlin Multiplatform for business logic) — not worth architecting speculatively; revisit if/when Android work begins

---

## Technical Stack (Initial)

| Concern | Choice | Notes |
|---|---|---|
| Language | Swift 5.10+ | |
| UI | SwiftUI | UIKit bridges for CarPlay and anything SwiftUI can't reach natively |
| Minimum iOS | iOS 17+ | Gives us modern SwiftUI, MapKit improvements, Observation framework |
| Location | CoreLocation | Significant-location-change and region monitoring |
| Maps | MapKit | Revisit MapLibre if we need custom tile sources |
| Offline tiles | MapKit native offline (iOS 17+) | MBTiles via MapLibre as fallback |
| TTS | AVSpeechSynthesizer | Premium voices via AVFoundation |
| Audio | AVFoundation | Mixing, ducking, background audio |
| Local data | SwiftData | GRDB as fallback if we need more control |
| Networking | URLSession + async/await | Sync with TALL backend |
| IAP/Subscriptions | StoreKit 2 | Native, no bridging |
| CarPlay | CarPlay framework | Deferred to post-POC |
| Background | BackgroundTasks framework | For sync and route preload |
| Build/Distribution | Xcode Cloud or Fastlane | TestFlight → App Store |

---

## Non-Goals

- Cross-platform code sharing
- Android parity
- Web-based mobile experience (the TALL companion website is separate and complementary, not a mobile substitute)

---

## Revisit Conditions

This decision should be revisited if any of the following occur:

1. CarPlay is removed from the product vision
2. Android launch becomes urgent (shifting timeline or market evidence)
3. Apple fundamentally changes the CarPlay entitlement process in a way that nullifies the native advantage
4. A cross-platform framework ships first-class CarPlay support with Apple's endorsement

---

## Related Canon

- `CONTRIBUTING.md` — agent roles and collaboration model
- `WORKFLOW.md` — build procedure and interaction modes
- `AGENTS.md` — execution boundaries for CC

---

## Git Commit Message

```
Add ADR-001: Mobile framework selection (Swift/SwiftUI native, iOS-first)
```
