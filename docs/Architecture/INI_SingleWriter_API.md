# INI Single Writer – API

## Öffentliche Methoden (Entwurf)

### get(section, key, fallback=None)
- Liefert Wert oder Fallback

### set(section, key, value, source=None)
- Setzt einzelnen Wert im In-Memory-Model
- `source` wird geloggt (z. B. `docking`, `settings`)

### update_many(section, dict_values, source=None)
- Setzt mehrere Keys atomar im Model

### save_merge()
- Merged In-Memory-Model in bestehende `ShrimpDev.ini`
- Kein Löschen fremder Sections

### snapshot()
- Liefert Diagnose-Snapshot (für Diagnose-Runner)
