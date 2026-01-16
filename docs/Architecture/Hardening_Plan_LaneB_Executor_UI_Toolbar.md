# Lane B Hardening Plan (Executor + ui_toolbar)

## Why this exists
We recently had instability driven by:
- duplicated toolbar wiring
- UI code containing runner/INI logic
- ambiguous runner execution paths
- noisy redirect logs masking real deltas

This document defines the **bounded hardening plan** aligned with `docs/PIPELINE.md`.

## Non-negotiables (Guardrails)
- UI modules are UI-only (no INI writes, no subprocess runner execution).
- Runner execution goes through one canonical executor API (Single Source of Truth).
- MR discipline: DIAG → one APPLY → stop (no repair cascades).

## Definition of Done (DoD)
### Executor API
- Push and Purge both call the canonical executor.
- No other module spawns runners directly.
- Reports/exit codes are consistently captured.

### ui_toolbar modularization
- Exactly one Push button + one Purge button in code.
- No duplicate builders/handlers.
- Toolbar calls logic_actions → executor only.
- py_compile stays green.

### Redirect/Config hygiene
- Redirect warning becomes meaningful (log rotation already implemented via R3517).
- Troubleshooting snippet exists in docs.

