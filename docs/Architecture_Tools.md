# Architecture – Tools & Cleanup Policy

**Last updated:** 2026-01-12 18:37:16

## tools/
- Contains **active, executable runners**
- Guard-relevant
- Must be production-quality

## tools/templates/
- Contains **non-executable templates**
- Source for new runners
- Not scanned by Guard

## _Archiv/
- Historical runners, backups, legacy code
- Never executed
- Guard ignores this directory

## _Temp/ and _Scratch/
- Experimental or transient artifacts
- Allowed to be broken
- Guard ignores these directories

## Cleanup Definition
The system is considered **clean** when:
- Guard reports **0 forbidden hits**
- Remaining issues are only in ignored paths
- New runners follow the standard CMD template

## No-Gos
- No mass refactors
- No “just cleaning up” actions
- No moving productive code without explicit decision

