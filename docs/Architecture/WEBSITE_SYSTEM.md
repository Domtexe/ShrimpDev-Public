# Website System (Lane E)

## Ziel
- Aufbau eines SEO/Website-Portfolios als **isolierte Lane**.
- Schnelle Validierung, klare Kill/Scale-Entscheidungen, keine Core-Kollateralschäden.

## Isolation Contract
- **Kein Zugriff** auf ShrimpDev-Core-State (insb. `ShrimpDev.ini`, Docking/UI-State).
- Gemeinsame Tools nur als **stateless tooling** (Scanner/Generator/Reports).

## Lifecycle
1) Idee/Nische → 2) Decision → 3) MVP → 4) Beobachtung (KPIs) → 5) Kill/Scale

## Artefakte
- `docs/websites/<site>/DECISION.md`
- `docs/websites/<site>/KPI.md`
- `docs/websites/<site>/KILL_SCALE.md`

## Shared Tooling (erlaubt)
- Keyword-/SERP-Scanner
- Content-Generator (Templates)
- Report-Generator (KPI snapshots)
