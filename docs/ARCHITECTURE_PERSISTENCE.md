# ShrimpDev — Persistence Architecture (INI)

## Canonical Rule
- **Single Source of Truth:** `registry/ShrimpDev.ini`
- **Backup:** `registry/ShrimpDev.ini.bak`
- **Root-INI ist verboten** (nur Migration / Altlast).

## Runtime Enforcement (R3244)
- Beim Start wird der Canonical-Pfad gesetzt:
  - ENV: `SHRIMPDEV_INI_CANONICAL=<absoluter Pfad zu registry/ShrimpDev.ini>`
- Jeder Altzugriff wird:
  - **umgeleitet** auf den Canonical-Pfad
  - **geloggt** nach `Reports/INI_REDIRECT.log`

## Redirect Log
Zweck: Transparenz & Migrationsgrundlage.

Format:
```
[timestamp] caller=<module>
  old=<legacy path>
  new=<canonical path>
```

## Verantwortlichkeiten
- `modules/config_loader.py`
  - einzige Instanz, die den Canonical-Pfad definiert
  - setzt ENV + Redirect-Logger
- `main_gui.py`
- `modules/module_docking.py`
- `modules/logic_actions.py`
  - dürfen **keine eigenen INI-Pfade** mehr festlegen
  - müssen den ENV-Override respektieren

## No-Gos (verbindlich)
- ❌ Kein Schreiben/Lesen von `ShrimpDev.ini` im Repo-Root
- ❌ Kein zweiter „Single Writer“
- ❌ Kein stilles Failen bei Persistenz
- ❌ Kein Bypass von `config_loader`

## Diagnose & Qualitätssicherung
- **R3241** — Beweis, ob `save()` beim Close aufgerufen wird
- **R3243** — Scan auf Hardcodings (`ShrimpDev.ini`)
- **R3244** — Runtime Redirect (Single Source of Truth)
- **R3245** — Redirect-Frequenz-Report

## Migrationsstrategie
1. Stabilität via Redirect (R3244)
2. Messung via Redirect-Frequenz (R3245)
3. Gezieltes Entfernen von Altpfaden (modulweise)
4. Zielzustand: `INI_REDIRECT.log` bleibt leer
