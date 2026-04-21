# Out the Window

A GPS-aware iOS app that narrates Texas historical markers to road-trippers.

Published by **The AI Expedition LLC**.

---

## Status

Pre-POC. Target POC date: **May 29, 2026** (McKinney → Cooper Maxwell Ranch road trip).

## Canon

All architectural and process decisions live in [`docs/`](./docs):

- [`CONTRIBUTING.md`](./docs/CONTRIBUTING.md) — agent roles and contribution rules
- [`WORKFLOW.md`](./docs/WORKFLOW.md) — build procedure, interaction modes
- [`AGENTS.md`](./docs/AGENTS.md) — execution boundaries for AI agents
- [`ADR-001`](./docs/ADR-001-mobile-framework.md) — Swift/SwiftUI native, iOS-first
- [`ADR-002`](./docs/ADR-002-dev-environment.md) — Phased dev environment (iMac Pro POC → M5 production)
- [`ADR-003`](./docs/ADR-003-ownership-legal-structure.md) — The AI Expedition LLC as publisher
- [`POC-001`](./docs/POC-001-may29-roadtrip.md) — May 29 road trip scope

## Layout
OTW/
├── docs/                  Canon (ADRs, POC spec, workflow)
├── data/thc/              Texas Historical Commission source CSVs (April 2026 export)
├── tools/                 Build-time tooling (data pipeline, etc.)
└── ios/                   iOS app (not yet scaffolded)

## License

Source code: TBD (post-POC decision).
THC marker data: used under non-commercial fair use for POC development.
Commercial use authorization is gated on post-POC viability decision.
