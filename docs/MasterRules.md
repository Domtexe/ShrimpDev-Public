
<!-- MR_INDEX_BEGIN -->
## MasterRules Index

| MR-ID | Status | Scope | Owner |
|---|---|---|---|
| `MR-DCK-01` | ACTIVE | TBD | TBD |
| `MR-DCK-02` | ACTIVE | TBD | TBD |
| `MR-DOC-ALL-01` | ACTIVE | TBD | TBD |
| `MR-WEB-01` | ACTIVE | TBD | TBD |
| `MR-WEB-02` | ACTIVE | TBD | TBD |

> Hinweis: Scope/Owner werden schrittweise präzisiert. Status ist aus Überschrift abgeleitet.
<!-- MR_INDEX_END -->



## MR-ERGÄNZUNG: Diagnose-Pflicht & Scope-Lock

- Diagnose **vor** jedem Fix
- Kein Scope-Leak
- GUI-Fail-Open verpflichtend
- Dokumentation Teil jedes Fixes

## UI Governance – Diagnosepflicht & Output Ownership (Patch R3086)

**Regel: Diagnose zuerst (Pflicht).**  
Bei UI-/Runner-Problemen wird **zuerst** der Datenfluss (Klick → Handler → Runner → Output → Popup) gemessen/geloggt.  
Fixes ohne belegte Ursache gelten als Regelverstoß.

**Regel: Output Ownership.**  
Wenn ein Runner ein nicht-standardisiertes Output-Format nutzt (z. B. TXT in `_Reports`), dann bekommt die UI dafür **ein eigenes Anzeige-Modul/Popup**.  
Zentrale Popups (z. B. r1851) werden **nicht** verbogen, nur weil ein Runner “anders” ausgibt.

**Regel: Keine stillen Popup-Fehler.**  
Popup-Aufrufe müssen Exceptions sichtbar loggen (debug_output.txt) und im Fehlerfall eine klare MessageBox zeigen.

<!-- MR_SAFE_REWRITE_AND_POPUP_GOVERNANCE -->

## Governance: Diagnose, Safe-Rewrite, Popup-Qualität

### Diagnosepflicht (Anti-Chaos)
- **Diagnose vor Fix** ist Standard: bevor Code geändert wird, muss der IST-Zustand messbar gemacht werden (mind. Trace/Log/py_compile/kleiner Diag-Runner).
- Wenn ein Fix nicht beim ersten Versuch verifiziert funktioniert: **Diagnose-Modus sofort** (Instrumentierung + minimaler Diagnose-Runner), bevor weiter gepatcht wird.

### Safe Rewrite Exception (nur unter Bedingungen erlaubt)
Ein Rewrite (größerer Block/Datei) ist **ausnahmsweise erlaubt**, wenn **alle** Bedingungen erfüllt sind:
1. **Keine unbeabsichtigten Änderungen** am Verhalten (Feature-Parität).
2. **Keine gewollten Funktionen entfernt** (Buttons/Flows/Runner-Hooks bleiben erhalten).
3. **Keine neuen Fehler**: py_compile/Smoke/RC0 muss wieder bestehen.
4. **Abhängigkeiten & Zusammenhänge** sind geprüft (Imports, Call-Signatures, UI-Bindings).

### Popup-UX Mindeststandard
- Popups dürfen **nicht** silent scheitern (kein `except: pass` ohne Log+Fallback).
- Report-Popups müssen **mindestens** zeigen:
  - Runner-ID
  - Ergebnis/Status (OK/FAIL)
  - Pfade zu relevanten Outputs (Reports/ oder _Reports/)
  - bei Purge: echte `_Reports\R2224_*.txt` Inhalte oder ein klarer Link/Pfad dahin.

### Archiv-Regel: Runner-Kollisionen (Pflicht)
- Wenn ein Runner (`R####.py`/`R####.cmd`) archiviert werden soll und im `tools\Archiv\` bereits eine Datei gleichen Namens existiert,
  **muss** der Runner **versioniert** und **trotzdem archiviert** werden.
- **Nie** in `tools\` belassen, nur weil im Archiv bereits eine Version liegt.
- Zulässige Namensschemata (Beispiel): `R2691__01.py` / `R2691__02.cmd` oder Timestamp-Variante.
- Ziel: `tools\` bleibt schlank, kein Leichenfeld.

## Docking Rules
_added 2026-01-08 12:26 via R3147_

### MR-DCK-01 — Docking Persistence
- Persist **only actual runtime state**.
- Never enforce defaults during save.

### MR-DCK-02 — Defaults vs Persistence
- Defaults are applied only at first-run or via explicit reset runner.
- Persistence must be state-faithful.

## R3172 — SingleWriter erzwingen (config_loader.save)
- `modules/config_loader.py::save()` darf **ShrimpDev.ini nie direkt** via `cfg.write()` schreiben.
- Delegation: `config_manager.get().save()` (Fallback: `ini_writer.write_configparser_atomic`).
- Ziel: **eine** zentrale Schreibstelle für `ShrimpDev.ini`.

## [R3175] Docking-Persistenz: immer zentrale INI-Quelle
Marker: R3175-DOCKING-CFG-MERGE

- `module_docking` darf keinen separaten ConfigParser “privat” speichern, den der Restore nicht liest.
- Regel: Docking-State wird in den zentralen ConfigParser (aus `config_manager.get()`) **gemerged** und anschließend ausschließlich via `config_manager.save()` persistiert.
- Fallback (nur bei Fehler): `ini_writer.write_configparser_atomic(path, cfg)` — aber niemals `cfg.write(open(...,'w'))`.

## MR-DOC-ALL-01 — Contract-first Documentation

**Scope:** ShrimpDev + ShrimpHub (alle Lanes)

**Prinzip:** Dokumentiere alles, was **Verhalten/Verträge** ändert – nicht jede lokale Variable.

**Dokupflicht, wenn mindestens eins zutrifft:**
1) **Public/Shared Contract** (öffentliche Funktionen, modulübergreifende APIs)
2) **Persistenz & State** (INI-Schema, Keys/Defaults/Semantik, Restore/Persist, Side-Effects)
3) **Architektur/Ownership** (Zuständigkeiten, Abhängigkeiten, Single-Writer/SSOT)

**Minimalformat pro Change:**
- Was / Warum / Impact (Module/Keys/Trigger) / Bezug (Runner+Report)

**Enforcement:**
- Jeder APPLY-Runner muss Doc-Änderungen enthalten **oder** im Report begründen: `Docs not needed`.
- Fehlt beides → Runner gilt als MR-Verstoß.

## MR-WEB-01 — Website Isolation Contract

**Scope:** Lane E (Websites)

**Regel:** Websites sind **isoliert** vom ShrimpDev-Core.

**Verboten:**
- Zugriff auf `ShrimpDev.ini` / Core-Config-State
- Nutzung von Docking/UI-Persistenz als Website-State
- Side-Effects im Core (Dateien verschieben/überschreiben außerhalb Website-Artefakte)

**Erlaubt:**
- gemeinsame Tooling-Runner (Scanner/Generator/Reports), solange **kein Shared State** geschrieben wird.
- Nutzung allgemeiner Diagnose/MR-Prinzipien (MR-DIAG-*, MR-DOC-ALL-01).

## MR-WEB-02 — Website Decision Documentation

**Scope:** Lane E (Websites)

**Regel:** Jede Site braucht eine schriftliche Entscheidung + Kriterien.

**Pflicht-Dateien pro Site:**
- `docs/websites/<site>/DECISION.md` (Nische, Monetarisierung, Zielgruppe, Suchintention, Risiko)
- `docs/websites/<site>/KPI.md` (Traffic, CTR, RPM/Revenue, Costs)
- `docs/websites/<site>/KILL_SCALE.md` (Kill/Scale Kriterien + Stichtage)

**Kein MVP ohne DECISION.md.**

## MR-IMPORT-STABILITY-01 — Modul-Integrität & Import-Verifikation (P0)

**Ziel:** Es darf nie wieder passieren, dass ein Fix syntaktisch „ok“ wirkt,
aber die App wegen Import-/File-Drift nicht startet.

**Regeln**
1. **Jede Änderung an `modules/` (neu, Rename, Restore, Replace) benötigt einen Import-Smoketest**
   - `python -c "from modules import <modulname>"` muss grün sein
   - Bei `from modules import X` muss `modules/X.py` existieren **oder**
     `X` explizit in `modules/__init__.py` exportiert werden
2. **Compile-Pflicht**
   - Vor jedem APPLY: `python -m py_compile <datei>`
   - Für Startmodule zusätzlich Import-Smoketest
3. **Keine Pattern-/Regex-Patches an produktiv geladenen Modulen**
   - Kein eindeutiger Match → **ABORT**
   - Fehler nach Patch → **sofortiger Rollback**
4. **Dateinamen sind API**
   - `config_loader.py` darf nicht als `*_FIXED.py` verbleiben
   - Windows-Falle: niemals `.py.txt`

**Akzeptanzkriterien**
- `py_compile` grün  
- `python -c "from modules import config_loader"` grün  
- GUI startet sichtbar

## MR-INI-MIGRATION-02 — Redirects sind temporär, nicht dauerhaft (P0)

**Ziel:** Redirect-Logging (`INI_REDIRECT.log`) ist nur für Migration erlaubt. Im Dauerbetrieb muss es leer bleiben.

**Regeln**
1. **Redirect-Logging ist ausschließlich für Migration zulässig**
   - `INI_REDIRECT.log` dient als Beweis/Telemetry, nicht als Normalzustand.
2. **Module, die den Canonical-Pfad kennen, dürfen nicht mehr als „legacy“ laufen**
   - Wenn Canonical bekannt: direkte Nutzung, kein Redirect-Auslösen.
3. **Nach erfolgreicher Migration gilt: neue Redirects sind Regression**
   - Neue Einträge in `INI_REDIRECT.log` nach Stichtag/Commit → Diagnosepflicht.
4. **Kein Pfad-Orakel in Feature-Modulen**
   - INI-Pfad kommt aus `modules/config_loader.py` (Single Source of Truth).
   - Feature-Module (z. B. Docking) dürfen keine eigene INI-Pfad-Logik pflegen.

**Akzeptanzkriterien**
- App-Start: `INI_REDIRECT.log` bleibt leer  
- Undock/Restore: `INI_REDIRECT.log` bleibt leer  
- Access-Profiling zeigt nur Canonical-Zugriffe (`registry/ShrimpDev.ini`)

## MR-INI-CONTENT-01 — INI-Content hat Owner, Trigger und Vollständigkeit (P0)

**Ziel:** Die INI ist nicht „irgendwo ein Dump“, sondern ein definierter Vertrag. Jede Sektion wird vollständig und deterministisch geschrieben.

**Regeln**
1. **Jede INI-Section hat genau einen Owner**
   - Pro Section ist exakt ein Modul/Subsystem verantwortlich (z. B. Docking → `module_docking`, Filter → `ui_filters`).
2. **Owner schreibt vollständig beim definierten Trigger**
   - Keine inkrementellen Zufallsschreibungen über die App verteilt.
   - „Partial persist“ ohne klaren Vertrag ist verboten.
3. **Fehlende Sections/Keys sind ein Bug**
   - Wenn Code eine Section/Key erwartet, muss der Owner sie zuverlässig schreiben (inkl. Defaults).
4. **Single Source of Truth**
   - INI-Pfad bleibt canonical (`registry/ShrimpDev.ini`) und wird nur über `config_loader`/`ini_writer` geschrieben.
5. **Verifikation ist Pflicht**
   - Für jede Owner-Section existiert mindestens ein Verify (py_compile + deterministische Key-Präsenzprüfung).

**Akzeptanzkriterien**
- Für jede INI-Section existiert ein definierter Owner und Trigger
- `registry/ShrimpDev.ini` enthält die erwarteten Sections/Keys nach dem Trigger
- Keine „mystery writes“ (Schreiber/Callsites sind bekannt & begrenzt)


## MR-PIPELINE-REVIEW-01 — Adaptive Pipeline-Priorisierung

**Geltungsbereich:** Assistent (verbindlich)

**Regel:**
- Die Pipeline ist die primäre Entscheidungs- und Priorisierungsinstanz.
- Der Assistent hat die Pflicht, während der Arbeit eine kontinuierliche Pipeline-Review durchzuführen.
- Ändern sich Risiko, Brisanz oder Wirkung eines Themas, muss die Priorisierung neu bewertet werden.
- Prioritätsänderungen sind zu begründen und in der Pipeline zu dokumentieren.
- Es erfolgt keine permanente Umsortierung, aber bewusste Anpassung bei relevanten Veränderungen.
- Die Wahl des nächsten Themas erfolgt pipeline-getrieben, nicht gesprächsgetrieben.
