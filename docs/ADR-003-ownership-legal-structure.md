# ADR-003: Ownership & Legal Structure

**Status:** Accepted
**Date:** 2026-04-20
**Decision Authority:** Dan (Product Owner)
**Architectural Author:** Claude (Chief Architect)
**Related:** ADR-001 (Mobile Framework), ADR-002 (Development Environment), POC-001 (May 29 Road Trip)

---

## Decision

**Out the Window will be published, owned, and operated by The AI Expedition LLC.**

- **Publisher entity:** The AI Expedition LLC (active, EIN obtained)
- **App Store developer name:** The AI Expedition LLC
- **Apple Developer Program enrollment:** Organization account
- **Sibling DBAs (informational):** compINSITE, Larascapes (separate products, not relevant to Out the Window)
- **Project status under the LLC:** Direct project, not a separate DBA

Out the Window is an LLC-owned product from inception. Dan Maxwell is the sole operator and Product Owner, but the product itself belongs to the company.

---

## Context

### The AI Expedition LLC

The AI Expedition is an active Texas LLC wholly owned by Dan Maxwell. It serves as the parent entity for Dan's software development work. Current known activities under the LLC:

- **compINSITE** — production software product (separate project, on slow-burn maintenance)
- **Larascapes** — web development services
- **Out the Window** — this project

All three share the LLC as parent but are operationally independent. No cross-project data, canon, context capsules, or agent history is shared.

### Why an LLC-owned Product Matters

Out the Window is a subscription product ($24.99 / 6-month, $39.99 / year). Subscription products have specific operational requirements that benefit from clean entity ownership:

1. **Subscription state is difficult to migrate between Apple Developer accounts.** Getting the account type right from the start is materially easier than fixing it later.
2. **Revenue flow should route to business banking** under the LLC's EIN for clean accounting and tax treatment.
3. **Liability shield** should apply from day one — subscriber disputes, regulatory questions, and competitor complaints are aimed at the LLC, not at Dan personally.
4. **Commercial licensing** (e.g., THC marker data agreement) must be entity-to-entity. An LLC licensing data while an individual publishes the app creates legal asymmetry.
5. **CarPlay entitlement approval** is more credible from an established LLC than from an individual developer.
6. **Future optionality** — investors, partners, acquirers, employees all expect clean entity structures.

### The Organization Apple Developer Account

The Organization account differs from Individual in ways directly relevant to Out the Window:

| Dimension | Individual | Organization |
|---|---|---|
| Developer name on App Store | "Dan Maxwell" | "The AI Expedition LLC" |
| Legal counterparty to Apple | Dan Maxwell personally | The AI Expedition LLC |
| D-U-N-S number required | No | Yes |
| Setup timeline | 24–48 hours | 2–4 weeks |
| Team member permissions | No | Yes |
| Subscription transfer if wrong choice | Complex, potentially lossy | Not applicable |

The 2-4 week enrollment timeline is acceptable because no Apple Developer account is required for the POC itself. POC installation uses free sideloading to Dan's own iPhone.

---

## Rationale

### Why Direct Project, Not a New DBA

Considered: registering Out the Window as a new DBA under The AI Expedition (e.g., "The AI Expedition DBA Out the Window").

**Rejected because:**
- DBAs add paperwork without legal benefit
- The product name "Out the Window" is strong enough to stand as a product brand without needing DBA formalization
- App Store listings can have a product name distinct from the developer name — the listing can say "Out the Window" as the app title while "The AI Expedition LLC" is the developer
- DBAs complicate banking, contracts, and tax filings
- If Out the Window grows enough to warrant its own entity, spinning it out as a separate LLC (or subsidiary) is cleaner than promoting a DBA

### Why Organization Over Individual

The case for Organization is strong and the case against is weak:

**For Organization:**
- Subscription product benefits massively from correct account type at launch
- The LLC infrastructure already exists; D-U-N-S is a free formality
- Professional presentation matters for a paid subscription
- CarPlay entitlement review benefits from entity credibility
- Liability shield applies from day one
- No meaningful timeline cost (POC doesn't need the account; production work has 2-4 weeks of runway after POC)

**Against Organization:**
- 2-4 week setup is longer than Individual's 24-48 hours — but this does not block the POC
- D-U-N-S requires an external application to Dun & Bradstreet — but this is free and routine

The rejected Individual path would save roughly 2 weeks of setup time at the cost of weeks-to-months of subscription migration work later, plus ongoing legal and branding asymmetry. Not a reasonable trade.

---

## Consequences

### Accepted Costs

- **D-U-N-S application required** before Apple Developer Program enrollment. Free, ~1-4 weeks processing. To be started in May 2026.
- **Apple Developer Program enrollment: 2-4 weeks** after D-U-N-S is active. Target: start enrollment by early June 2026, have account active by late June / early July 2026 for post-POC production work.
- **All contracts, agreements, and commercial licenses must be executed in the LLC's name** — including the pending THC commercial rights agreement.
- **Revenue flows to LLC banking** — not to Dan's personal accounts. Tax reporting is LLC-level.

### Gained Benefits

- Clean entity ownership of the product from inception
- Liability shield from day one
- Professional App Store presentation
- Stronger CarPlay entitlement application
- Clean commercial licensing posture with THC
- No future migration work required as the product scales
- Future optionality for investors, co-founders, contractors, acquirers
- Clear separation from compINSITE and Larascapes operations

### Deferred Decisions

- **D-U-N-S number:** Verify whether The AI Expedition LLC already has one (from prior compINSITE or Larascapes work). If yes, skip to Apple enrollment. If no, apply at dnb.com.
- **Company bank account specifically for Apple revenue:** Use existing LLC operating account or open a product-specific sub-account. Not urgent.
- **Apple Developer team structure:** Dan as Account Holder. Team member roles (Admin, Developer, Marketing, etc.) TBD as the project grows. For POC and v1 launch, Dan is the only role.
- **Eventual Out the Window spin-out:** If the product grows to the point where it warrants its own LLC or becomes a subsidiary of The AI Expedition, that's a future decision — not relevant now.

---

## Impact on Other Canon

### POC-001
No changes required. POC uses free sideloading under Dan's personal Apple ID. No Apple Developer account involved in the POC execution.

### ADR-001 (Framework)
No changes required. Framework decision is independent of ownership structure.

### ADR-002 (Dev Environment)
No changes required. Hardware decisions are independent of ownership structure.

### Future CarPlay ADR
Must reference this ADR. CarPlay entitlement application will be submitted under The AI Expedition LLC, not under Dan Maxwell personally.

### Future THC Data Licensing
Commercial rights agreement with THC must be executed between The AI Expedition LLC and THC. The pending email to THC should be signed as Dan Maxwell, Manager of The AI Expedition LLC, with the LLC identified as the licensing entity.

### Future Subscription Pricing & Terms
Legal terms of service and privacy policy must identify The AI Expedition LLC as the operator. App Store subscription metadata (developer name, support contact, legal entity) must reflect the LLC.

---

## Action Items

The following are unblocked by this decision and should be sequenced after POC delivery on May 29:

1. **Verify or obtain D-U-N-S number** for The AI Expedition LLC. Check existing records first at dnb.com/duns-number/lookup before applying new. (May 2026, parallelizable with POC work)
2. **Open or designate LLC business bank account** for App Store revenue. Ensure it's ready before Apple Developer enrollment.
3. **Apply for Apple Developer Program as Organization** under The AI Expedition LLC. (Target: early June 2026)
4. **Draft and send THC commercial rights inquiry** signed from The AI Expedition LLC. (Currently open, not yet sent)
5. **Draft standard LLC-branded Terms of Service and Privacy Policy** for Out the Window. (Later in production phase, not urgent)

---

## Revisit Conditions

Revisit this ADR if:

1. **The AI Expedition LLC is dissolved or restructured.** Ownership of Out the Window must be reassigned.
2. **Out the Window outgrows the parent LLC** and warrants its own entity (subsidiary, separate LLC, or spin-out). Re-examine structure.
3. **An acquisition or investment offer** requires changing the ownership entity.
4. **Apple changes Developer Program rules** in a way that makes Organization enrollment significantly more burdensome or Individual enrollment significantly more capable.
5. **A co-founder or equity partner joins Out the Window** — triggers a new ADR about ownership allocation and may require LLC operating agreement updates.

---

## Related Canon

- `ADR-001-mobile-framework.md` — Swift/SwiftUI native, iOS-first
- `ADR-002-dev-environment.md` — Phased dev environment
- `POC-001-may29-roadtrip.md` — May 29 POC scope
- `CONTRIBUTING.md` — agent roles
- `WORKFLOW.md` — build procedure

---

## Git Commit Message

```
Add ADR-003: Ownership and legal structure (The AI Expedition LLC as publisher)
```
