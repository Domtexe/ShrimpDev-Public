
## Canonical INI (R3514)
- Canonical INI path is `registry/ShrimpDev.ini`.
- Redirects were logged as `old=<repo_root>/ShrimpDev.ini` -> `new=<repo_root>/registry/ShrimpDev.ini` (caller=main_gui).
- Goal: redirect log should trend to **zero**.

## SingleWriter rule (already established by earlier work like R2379 references)
- Exactly one authorized writer for the INI merge/write pipeline (ini_writer).
- UI modules (e.g. ui_toolbar) must not perform direct `configparser.write()` or full-overwrite writes.
- Config path resolution must be unified: readers/writers use the canonical path resolver (no hardcoded root `ShrimpDev.ini`).

## Implementation intent
- Prefer: `config_loader` exposes a canonical path helper OR delegates to a single central resolver.
- Any leftover hardcoded `"ShrimpDev.ini"` references should be migrated to the canonical resolver.
