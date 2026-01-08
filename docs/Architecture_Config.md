
## R2345 (Compat Shims)
- modules/config_loader.py und modules/config_mgr.py sind Aliase auf modules/config_manager.py
- Zweck: alte Imports nicht brechen, bis Refactor gezielt geplant ist.
\n## R2346 (Compat API Restore)\n- modules/config_loader.py und modules/config_mgr.py stellen wieder load()/save() bereit.\n- Lesen/Schreiben: Projektroot/ShrimpDev.ini (konservativ, ohne neue Abhängigkeiten).\n
## R2348 (Merge Save robust)
- config_loader.save()/config_mgr.save() ersetzen jetzt robust die save()-Funktion (Type-Hints egal).
- Speichern erfolgt als Merge, damit [Docking] nicht überschrieben wird.

## R2350 (Merge Save)
- config_loader.save()/config_mgr.save() schreiben INI jetzt als Merge (bestehende Sections bleiben erhalten, z.B. [Docking]).

### Doku-Notiz (R3154, 2026-01-08 17:27:15)
- MR-REF (Refactoring/Cleanup) ergänzt: Obsoleter Code darf raus, **aber Funktion bleibt**; belegt entfernen; minimal-invasive Runner; Backup+Report+Smoke-Test; keine riskanten Auto-Edits in Funktionskörpern.

