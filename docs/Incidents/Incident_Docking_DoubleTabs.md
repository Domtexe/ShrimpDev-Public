
# Incident: Docking Double Tabs on Startup
_added 2026-01-08 12:26 via R3147_

## Summary
- On startup, two different tabs were restored unexpectedly.

## Root Cause
- Persisted legacy state in `ShrimpDev.ini`.
- Multiple `.open = 1` flags from historic sessions.
- Docking restore logic worked correctly on inconsistent data.

## Resolution
- One-time normalization via R3144.
- Verified persist logic in `module_docking.persist_all()`.

## Result
- Deterministic docking restore.
- Only undocked tabs active at shutdown are restored.

## Lessons Learned
- Persisted state ≠ desired default.
- Defaults must not be enforced during persistence.
