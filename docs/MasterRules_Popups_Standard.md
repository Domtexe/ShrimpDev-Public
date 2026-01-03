
## UI Popups – Single Source of Truth (verbindlich)

**Regel: UI erzeugt niemals Popups.**
- Kein `*_show_popup` / kein Popup-Wrapper in `ui_*.py`.
- UI darf nur Aktionen auslösen (Callbacks), aber keine Ausgabefenster bauen.

**Popups werden ausschließlich in `modules/logic_actions.py` erzeugt.**
- Zentraler Mechanismus: `_r1851_run_tools_runner(...)` + `_r1851_show_popup(...)`.

### Purge Standard (verbindlich)
- Purge Scan: Runner `R2218`
- Purge Apply: Runner `R2224`
- Popup-Inhalt kommt aus `Reports\R2218_*.txt` bzw. `Reports\R2224_*.txt` (neuestes mtime).
- Markdown-Bridge-Dateien sind **keine** Anzeigequelle.

### Signatur-Regel (nicht raten!)
`_r1851_run_tools_runner(app, runner_id, label)`  
- `label` ist positional Pflichtparameter.
- Keine erfundenen kwargs wie `title=` oder `subtitle=` ohne echte Signaturprüfung.

### Runner-Auslieferungsregel
- Vor Auslieferung eines Fix-Runners: **Compile-Gate** (`py_compile`) auf alle geänderten Python-Dateien.
- Keine „OK trotz FAIL“ in `.cmd`: Exitcode muss korrekt durchgereicht werden.

### Patch-Disziplin (kritische Module)
- Kein Regex-basiertes Ersetzen ganzer Funktionsblöcke in kritischen Dateien (z. B. `logic_tools.py`, `ui_toolbar.py`) ohne strukturierte Parser/Bounds.
- Minimal-invasive Änderungen + Backups + Rollback bei Compile-Fail.
