# Architecture – Guard & Single-Writer Policy

**Last updated:** 2026-01-12 18:37:16  
**Source of truth since:** R3376 (hardened guard)

## Purpose
The Guard ensures that **no productive code writes INI files directly**.
All persistence must go through **modules.ini_writer** (Single-Writer rule).

## What the Guard checks
- Real executable code only (tokenize-based)
- Detects `cfg.write(` calls in live code paths

## What the Guard ignores (by design)

- Ignore policy: filenames containing 'manuell' are treated as non-production and excluded from scans (e.g. config_loader manuell …).
- Comments and strings
- Template code blocks
- Non-productive paths:
  - `_Temp/`
  - `_Scratch/`
  - `_Archiv/`
  - `__pycache__/`
  - `.git/`, `.venv/`, `venv/`
- File markers:
  - `_FIXED_`
- Directory prefixes:
  - `_manuell*`

## Exit Codes
- **0** – Clean (no forbidden writes)
- **2** – Forbidden writes detected (must fix)

## No-Gos
- No regex-based scanning
- No direct INI writes outside `modules.ini_writer`
- No retro-patching of legacy runners

