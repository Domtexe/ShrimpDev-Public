
<!-- MR_INDEX_BEGIN -->
## MasterRules Index

| MR-ID | Status | Scope | Owner |
|---|---|---|---|
| `MR-PIPELINE-SSOT-01` | ACTIVE | ShrimpDev/ShrimpHub (alle Lanes) | Assistent |
| `MR-DIAG-FIRST-ENFORCED-01` | ACTIVE | ShrimpDev/ShrimpHub (alle Lanes) | Assistent |
| `MR-RUNNER-SCOPE-LOCK-01` | ACTIVE | ShrimpDev/ShrimpHub (alle Lanes) | Assistent |
| `MR-DOD-01` | ACTIVE | ShrimpDev/ShrimpHub (alle Lanes) | Assistent |
| `MR-STOP-CRITERIA-01` | ACTIVE | ShrimpDev/ShrimpHub (alle Lanes) | Assistent |
<!-- R3568_MR_INDEX_PATCH_BEGIN -->
<!-- R3568_MR_INDEX_PATCH_END -->
| `MR-STRAT-FOCUS-01` | ACTIVE | ShrimpDev/ShrimpHub (alle Lanes) | Assistent |
| `MR-DCK-01` | ACTIVE | TBD | TBD |
| `MR-DCK-02` | ACTIVE | TBD | TBD |
| `MR-DOC-ALL-01` | ACTIVE | TBD | TBD |
| `MR-WEB-01` | ACTIVE | TBD | TBD |
| `MR-WEB-02` | ACTIVE | TBD | TBD |

> Hinweis: Scope/Owner werden schrittweise präzisiert. Status ist aus Überschrift abgeleitet.<!-- MR_INDEX_END -->



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


<!-- R3564_MR_STRAT_FOCUS_01_BEGIN -->
## MR-STRAT-FOCUS-01 — Basis vor Produkt (Fokusregel)

**Ziel:** Monetarisierungsdruck darf das Fundament nicht destabilisieren. ShrimpDev bleibt zuerst.

**Regeln**
1. **Pipeline first:** Arbeitsthemen werden pipeline-getrieben gewählt (siehe `MR-PIPELINE-REVIEW-01`).
2. **Kein neues Produkt/Repo**, solange relevante **P0/P1 in Lane A/B** offen sind.
3. **Ideen sind erlaubt**, aber nur als **Parking/Doku** (kein Implementations-Scope außerhalb Pipeline).
4. **Assistentenpflicht:** Wenn der Nutzer deutlich abweicht, sachlich auf Pipeline + diese Regel verweisen.
5. **Ausnahme nur explizit:** Neue Produktarbeit nur bei ausdrücklicher Freigabe *und* dokumentierter Risikoabwägung.

**Bezug:** Thread-Entscheidung „erst ShrimpDev fertigstellen, dann monetarisieren“.
<!-- R3564_MR_STRAT_FOCUS_01_END -->
**Geltungsbereich:** Assistent (verbindlich)

**Regel:**
- Die Pipeline ist die primäre Entscheidungs- und Priorisierungsinstanz.
- Der Assistent hat die Pflicht, während der Arbeit eine kontinuierliche Pipeline-Review durchzuführen.
- Ändern sich Risiko, Brisanz oder Wirkung eines Themas, muss die Priorisierung neu bewertet werden.
- Prioritätsänderungen sind zu begründen und in der Pipeline zu dokumentieren.
- Es erfolgt keine permanente Umsortierung, aber bewusste Anpassung bei relevanten Veränderungen.
- Die Wahl des nächsten Themas erfolgt pipeline-getrieben, nicht gesprächsgetrieben.

<!-- R3568_GOVERNANCE_GUARDRAILS_BEGIN -->
## MR-PIPELINE-SSOT-01 — Pipeline ist Single Source of Truth (SSOT)

**Scope:** ShrimpDev + ShrimpHub (alle Lanes)  
**Owner:** Assistent

**Regel**
- `docs/PIPELINE.md` ist die **primäre** Entscheidungs- und Priorisierungsinstanz.
- **Was nicht in der Pipeline steht, existiert nicht** (Ideen/Chat/Logs sind kein Arbeitsauftrag).
- Umsetzung außerhalb Pipeline ist **Regelverstoß** (Ausnahme nur mit expliziter Freigabe + Doku).

## MR-DIAG-FIRST-ENFORCED-01 — Diagnose vor Fix (Enforcement)

**Scope:** ShrimpDev + ShrimpHub (alle Lanes)  
**Owner:** Assistent

**Regel**
- Vor jedem APPLY-Fix muss der IST-Zustand **messbar** gemacht werden (mind. Log/Trace/py_compile/kleiner DIAG-Runner).
- Fix ohne belegte Ursache gilt als **ungültig**.
- Wenn ein Fix nicht beim ersten Versuch verifiziert funktioniert: **sofort Diagnose-Modus** (Instrumentierung + minimaler DIAG-Runner), keine Trial-&-Error-Kaskade.

## MR-RUNNER-SCOPE-LOCK-01 — Runner Scope-Lock (Anti-Scope-Leak)

**Scope:** ShrimpDev + ShrimpHub (alle Lanes)  
**Owner:** Assistent

**Regel**
- Jeder Runner hat einen klaren Scope. Änderungen außerhalb dieses Scopes sind verboten.
- Keine stillen Rewrites, keine verdeckten Funktionsentfernungen.
- Wenn Anchor/Match unsicher ist: **ABORT** (kein “best effort” Patch auf produktiven Dateien).
- Report muss nennen: Ziele, Deltas, betroffene Dateien, Nebenwirkungen.

## MR-DOD-01 — Definition of Done (global)

**Scope:** ShrimpDev + ShrimpHub (alle Lanes)  
**Owner:** Assistent

Ein Task gilt nur als **DONE**, wenn:
- Doku/Pipeline/Code sind synchron (oder bewusst “Docs not needed” begründet).
- Ein Report existiert (Runner-ID, Ergebnis, Pfade).
- Verifikation passt zum Scope (mind. py_compile bei Runtime-Änderungen; bei Docs-only: Marker/Anchors ok).
- Keine offenen Nebenwirkungen / TODO-Ketten ohne Pipeline-Eintrag.

## MR-STOP-CRITERIA-01 — Bewusst beenden statt Zombie-Themen

**Scope:** ShrimpDev + ShrimpHub (alle Lanes)  
**Owner:** Assistent

**Regel**
- Abbruch/Stop ist erlaubt, aber muss **explizit** dokumentiert werden (Pipeline: `skip` / `obsolet` / “archived” + kurzer Grund).
- “Liegen lassen” ohne Status ist verboten.

<!-- R3568_GOVERNANCE_GUARDRAILS_END -->

## MR-RUNNER-SAFE-INGEST-01 — Syntax-sichere Runner-Erstellung

### Motivation
ShrimpDev speichert **keine Python-Dateien mit Syntaxfehlern**.
Patch-Runner auf nicht gespeicherte oder nicht kompilierbare Dateien sind logisch unmöglich.

### Verbindliche Regeln
1. **Jeder neue Runner muss syntax-sicher sein, bevor er gespeichert wird.**
   - Keine riskanten Konstrukte beim Erstellen (z. B. f-Strings mit `{}` im eingebetteten Template).
2. **Code-Templates dürfen niemals als f-string implementiert werden**, wenn sie selbst `{}` oder `\` enthalten.
   - Stattdessen: Triple-Quoted-Strings + String-Konkatenation  
     oder `.format()` mit **escaped braces**.
3. **Wenn ein Runner wegen Syntax nicht speicherbar ist:**
   - ❌ Kein Patch-Runner
   - ✅ Immer vollständige, reparierte `.py`-Datei 1:1 ausliefern
4. **Ein Runner gilt nur als geliefert, wenn `py_compile` erfolgreich ist**
   **und der Exit-Code = 0**.

### Kurzfassung
> Templates nie als f-string, wenn `{}` vorkommt.  
> Nicht speicherbarer Runner ⇒ komplette, lauffähige Datei liefern.

<!-- R3511_MR_RULE -->
## Regel: Phantom-Runner-IDs (Pipeline/Docs) dürfen keinen Fix-Loop auslösen
- Wenn eine Runner-ID in Pipeline/Docs auftaucht, aber keine aktiven Runner-Dateien existieren (cmd/py), ist das ein **Phantom**.
- Vorgehen: zuerst rekursiv scannen (z. B. R3510), dann **entweder** materialisieren **oder** Pipeline-Eintrag archivieren/downgraden.
- Keine Reparatur-Kaskaden ohne belegte Existenz der betroffenen Artefakte.
<!-- R3511_MR_RULE -->


## MR: INI Canonical Path + SingleWriter
- Canonical INI is `registry/ShrimpDev.ini`.
- No new code may hardcode root `ShrimpDev.ini` paths.
- UI modules must not write INI directly; only via central writer/merge API.
- If config/restore issues appear: run a DIAG runner first, then one minimal APPLY.

<!-- R3539 BEGIN: MasterRules Housekeeping/Purge -->
## MasterRules – Housekeeping / Purge (verbindlich)

1. **Housekeeping ist ein System, kein Einmal-Fix.**  
   Purge/Prune muss dauerhaft stabil laufen und die Runner-Liste klein halten.

2. **Runtime-Relevanz Policy:**  
   `tools/` ist **keine** Runtime-Reference-Quelle. Runner-Querverweise zählen nicht als „operativ gebraucht“.  
   Runtime-Relevanz kommt aus `modules/` (Entry-Graph/Executor/Core) und `registry/` (Allowlist/Registry) plus Schutzmechanismen (last-N).

3. **Kein Patch ohne sicheren Anchor:**  
   Wenn ein Apply-Runner keinen eindeutigen Patch-Anker findet → **ExitCode 21** + **DIAG-Runner** bauen.  
   Kein Trial-&-Error im Blindflug.

4. **Purge archiviert, löscht nicht.**  
   Verschieben ins Archiv ist Standard (voll reversibel). Deletes nur mit expliziter Zustimmung.

<!-- R3539 END -->

<!-- R3566 BEGIN -->
### Purge Guard: canonical tools_keep

- Purge entrypoint in UI MUST ensure canonical keep file exists:
  - `registry/tools_keep.txt` (ONLY)
- If missing/unreadable: Purge is blocked (MR-safe).
<!-- R3566 END -->


## Runner-ID, Templates und NextFree (verbindlich)

- **Runner-ID wird ausschließlich aus dem Dateinamen abgeleitet**
  (`R####.cmd` + `R####.py`).
- **Mismatch cmd ↔ py oder ungültiger Dateiname ⇒ ABORT.**
- **Template-Pflicht**: Neue Runner dürfen nur aus
  `tools/templates/` erstellt werden.
- **Keine manuelle ID-Vergabe** im Code, keine Fallbacks.


## MasterRule – ThreadCut (verbindlich)

Ein **ThreadCut** ist ein verpflichtender Abschlussmechanismus für ShrimpDev-Threads.

**Regeln**
- Ein ThreadCut markiert das Ende eines Threads.
- Nach einem ThreadCut werden keine neuen Inhalte mehr diskutiert.
- Alle verwertbaren Erkenntnisse werden explizit überführt in:
  - MasterRules
  - Pipeline
  - Dokumentation
  - Lernsystem (LearningJournal / Reports)
- Ein neuer Thread muss ohne Kontextverlust startfähig sein.

**Grundsatz**
> Ein ThreadCut beendet Denken und beginnt Ordnung.
> Was danach existiert, ist klar, dokumentiert und reproduzierbar.
