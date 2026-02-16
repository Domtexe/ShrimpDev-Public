
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

> Hinweis: Scope/Owner werden schrittweise präzisiert. Status ist aus Überschrift abgeleitet.
| `MR-EXCEL-DISPO-CORE-01` | ACTIVE | Excel / DISPO Tool | Assistent |
| `MR-EXCEL-LANE-00` | ACTIVE | Excel Lane | Assistent |
| `MR-EXCEL-DISPO-ASSIGN-02` | ACTIVE | Excel / DISPO | Assistent |
| `MR-ANCHOR-POLICY-01` | ACTIVE | Governance | Assistent |
| `MR-SYSTEM-MAP-01` | ACTIVE | Governance | Assistent |
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

## Websites / Content-Systeme (Static Sites, Hugo, Clarivoo)

### Geltungsbereich
Dieser Abschnitt gilt für alle Website-/Content-Systeme, insbesondere:
- Clarivoo
- Hugo / Static Sites
- Vergleichs-, Wissens- und Affiliate-Websites

Er gilt ausdrücklich **nicht** für:
- ShrimpDev Core (App/Runner-System)
- ShrimpHub GUI/Tools (Desktop-App-Logik)

### Grundprinzipien
1. **Struktur vor Content**: Informationsarchitektur (IA) hat Vorrang vor Textproduktion.
2. **Content vor Branding**: Visuelle Marken-/Designarbeit erst, wenn Inhalte Tiefe/Traktion haben.
3. **Manuelle IA-Entscheidung vor Automation**: Top-Level, Pfade und Seitentypen werden zuerst bewusst festgelegt.
4. **Deadlinks sind zulässig, wenn bewusst**: Unresolved Links sind kein Bug, solange sie als Struktur-Delta verstanden werden.

### Runner-Regeln für Websites
Runner im Website-Kontext sind **Struktur-Tools**, keine Content-Generatoren.

**Runner dürfen:**
- Navigation und Menüs konsolidieren (nur nach klarer IA-Vorgabe)
- `_index.md`/Index-Seiten synchronisieren und konsistent halten
- bestehende Pfade/Slugs angleichen, wenn Zielstruktur explizit definiert ist
- Deadlink-/Unresolved-Reports erzeugen (ohne automatische „Heilung“)

**Runner dürfen NICHT:**
- neue Inhalte „raten“ oder generieren, um Links zu befriedigen
- Seiten automatisch anlegen, nur um Unresolved Targets zu eliminieren
- Strukturentscheidungen implizit treffen (Top-Level/Taxonomie/Pfade)
- Branding/Layout/Design ohne expliziten Auftrag verändern

### ExitCode-Semantik (Website-spezifisch)
Im Website-/Content-Kontext bedeutet ein ABORT/ExitCode **nicht automatisch** einen Systemfehler.

- **ExitCode 2 = Struktur-Unsicherheit / IA nicht final**
- ABORT ist korrekt, wenn:
  - Zielpfade semantisch/inhaltlich unklar sind
  - die IA (Top-Level, Slugs, Index-only vs Content) noch nicht entschieden ist
  - ein Runner sonst raten müsste (verboten)

### Phasenmodell (Websites)
1. **IA-Phase (manuell)**: Top-Level, Seitenarten, Slugs, Index-only vs Content festlegen.
2. **Struktur-Runner (gezielt, einzeln)**: Navigation + `_index.md` konsistent machen, ohne Content zu schreiben.
3. **Content-Phase**: Artikel erstellen/erweitern, interne Verlinkung bewusst aufbauen.
4. **Skalierung/Automatisierung**: Serien, Templates, Massenpflege, Vergleichslogik ausrollen.

**Regel:** Keine Runner-Stapelung vor Abschluss von Phase 1.

### No-Gos (verbindlich)
- Keine weiteren „Fix-Runner“, solange die IA nicht klar entschieden ist.
- Kein automatisches Link-Raten oder „autofill“ fehlender Ziele.
- Kein Branding-Tuning vor Content-Tiefe.

## Templates

- Für **wiederkehrende** Dinge werden **Templates** unter `docs/templates/` angelegt und gepflegt (Runner-CMD/PY, DIAG/APPLY Patterns, Checklisten, ThreadCut, Halt-Stop, etc.).
- Ziel: weniger Fehler, schnellere Umsetzung, konsistente MR-konforme Ausgaben.

## Python Policy

- **Python gilt als verfügbar (PATH)**, solange kein Messbeweis das Gegenteil zeigt.
- Runner geben **keine WARN** aus, nur weil kein venv vorhanden ist.
- Runner dürfen **nur failen**, wenn Python **nicht lauffähig** ist (Messung via `python -c ...`).


## Erweiterungen – Runner / Architektur (2026-01)

### MR-A1: Central Runner Executor (Pflicht)
Alle Runner (.cmd / .bat / .py) dürfen ausschließlich über:
`modules/module_runner_exec.run(...)`
gestartet werden. Direkte subprocess-/os.system-Aufrufe sind verboten.

### MR-A2: Bypass-Beseitigung – Ablauf zwingend
DIAG (read-only) → APPLY (1 Datei / 1 Stelle) → Test → Report → ThreadCut.

### MR-A3: Single-Writer-Prinzip
Für jede schreibende Ressource existiert genau ein Owner.
Lesen ist frei, Schreiben ausschließlich über den Owner.

### MR-A4: Projekt-Threads fixen keine Blocker
Core-Blocker (Runner, INI, Start/Crash, Pipeline) gehören immer in die Pipeline.

### MR-A5: Diagnose schlägt Aktion
Unsicherheit erzwingt Diagnose. Vermutungsfixes sind unzulässig.

## Nachsorge & Guards (Anti-Regression)

### MR-NG1: Guards beobachten, nicht erzwingen
Guards (z. B. Output-Guard) dienen zur Messung und Transparenz.
Hohe Fail-Zahlen bei Altbestand sind zulässig, solange sie nicht weiter steigen.

### MR-NG2: Stichtagsregel (Neuzeit)
Als Stichtag für den Output-Standard gilt: **R3752**.
- Runner **ab R3752** müssen Template-/Output-Standard einhalten.
- Runner **vor R3752** gelten als Altbestand.

### MR-NG3: Opportunistische Modernisierung
Wenn ein Alt-Runner ohnehin geändert wird, muss er dabei auf Output-Standard gebracht werden
(CMD-Banner/ExitCode/Report-Hinweis; PY: Report schreiben + Report-Pfad printen).

### MR-NG4: Regression-Trigger
Wenn Guard-Metriken schlechter werden (z. B. steigende Fail-Zahlen bei Neuzeit-Runnern),
wird automatisch **Nachsorge** ausgelöst (Regeln/Doku/Pipeline-Nachsorge).

### MR-NG5: Codewort „Nachsorge“
Das Codewort **Nachsorge** löst aus:
- Regeln ableiten (allgemein + projektspezifisch)
- Doku konsolidieren (Docs-only, per Runner)
- MasterRules ggf. ergänzen
- Pipeline-Status nachziehen
- Nachsorge-Report erzeugen
- optional ThreadCut, wenn Übergabe/Abschluss sinnvoll ist

### Referenzen
- Output-Guard: **R3753**
- Output-Standardisierung/Templates: **R3752** (`docs/templates`)


<!-- MR_EXCEL_DISPO_CORE_01_BEGIN -->
## MR-EXCEL-DISPO-CORE-01 — DISPO-Tool: Single-Module Core + Anti-Chaos (Excel Lane)

**Zweck:** Dauerhaft stabile Planung ohne Code-Chaos, Nebenlogiken oder Datenkorruption.  
**Scope:** Excel / DISPO Tool  
**Owner:** Assistent  
**Status:** ACTIVE

### MR-D1 — Single Source of Code
- Es existiert **genau ein** fachliches VBA-Modul als Wahrheitsquelle: `m_DISPO_Core`.
- **Jede** fachliche Logik und **jeder** Button-Entry-Point liegt dort.
- Andere Fachmodule sind **verboten**.

**Verstoß → Maßnahme:** Fremdmodule entfernen oder in `m_DISPO_Core` integrieren.

### MR-D2 — Single Source of Truth (Daten)
- `t_DISPO_Slots` ist die **einzige Wahrheit** für Slots/Planung.
- Keine Parallelberechnungen in anderen Sheets.

**Verstoß → Maßnahme:** Fremdlogik löschen, nur noch Lesen aus Slots.

### MR-D3 — Spaltennamen sind API
- Zugriff ausschließlich über **Headernamen** (Header-Mapping).
- Keine festen Spaltennummern.

**Verstoß → Maßnahme:** Code an Header-Mapping anpassen.

### MR-D4 — Harte Schreibverbote
Makros dürfen **nie** schreiben in:
- `Final`
- `Final_ID`
- `Status`

Diese Spalten sind **Formelspalten**.

**Verstoß → Maßnahme:** Code sofort korrigieren; Formeln wiederherstellen.

### MR-D5 — Erlaubte Schreibfelder
Makros dürfen nur schreiben:
- Slot-Definition (BuildSlots)
- `Vorschlag` (Assign)

`Override` ist manuell.

**Verstoß → Maßnahme:** Schreibzugriff entfernen.

### MR-D6 — Klare Ownership
- **BuildSlots:** erzeugt Slots aus `t_Aufgaben` (und nur das).
- **Assign:** schreibt nur Vorschläge (`Vorschlag`).
- **Reset:** leert nur `Vorschlag` und `Override`.
- **EnsureFormulas:** stellt Formelspalten sicher (`Final`/`Final_ID`/`Status`), ohne Werte zu hardcoden.

Keine Überschneidungen.

**Verstoß → Maßnahme:** Verantwortlichkeiten trennen.

### MR-D7 — Button-Disziplin
- Jeder Button ruft genau **ein** `BTN_*` Makro.
- `BTN_*` enthält keine Fachlogik, nur Orchestrierung.

**Verstoß → Maßnahme:** Button neu zuweisen.

### MR-D8 — Namenskonvention
- Public: `BTN_*`
- Private: `p_*`, `v_*`, `x_*`
- Keine generischen Namen (Test, Neu, Macro1).

**Verstoß → Maßnahme:** Umbenennen.

### MR-D9 — Keine Duplikate
- Keine zweite Version derselben Funktion.
- Alte Varianten werden gelöscht, nicht geparkt.

**Verstoß → Maßnahme:** Bereinigen.

### MR-D10 — Stabilitäts-Gate (Pflichttest)
Nach Änderungen:
1) BuildSlots  
2) Assign  
3) Reset  
Formeln prüfen.

**Fehler → Maßnahme:** Rollback + Diagnose.

### MR-D11 — Logging-Pflicht
- Jede BTN-Aktion schreibt Log (Debug oder Sheet).
- Fehler werden mit Ursache + Kontext ausgegeben.

**Verstoß → Maßnahme:** Logging ergänzen.

### MR-D12 — Kontrolliertes Löschen
- Aufräumen erst nach stabilem Testlauf.
- Vorher Backup.

**Verstoß → Maßnahme:** Backup nachholen.

### MR-D13 — Formeln bleiben Formeln
- Keine Werte-only in Formelspalten.
- Code setzt Formeln nur wieder ein.

**Verstoß → Maßnahme:** Formelstruktur reparieren.

### MR-D14 — Views sind Read-Only
- Views lesen nur `Final`/`Final_ID`.
- Keine Rückschreibungen.

**Verstoß → Maßnahme:** Schreibzugriffe entfernen.

### MR-D15 — Strukturänderungen = Codepflicht
- Jede Tabellenänderung erfordert Code-Update + Gate-Test.

**Verstoß → Maßnahme:** Mapping aktualisieren.

---

## Enforcement (Sofortmaßnahmen)
> **Ein Modul. Eine Wahrheit. Klare Zuständigkeiten.**

Regelverstoß ⇒ **Rollback/Backup**, dann Diagnose.  
Jede Rückschreib- oder Formel-Zerstörung gilt als **P0**.

<!-- MR_EXCEL_DISPO_CORE_01_END -->



<!-- MR_EXCEL_LANE_00_BEGIN -->
# Excel Lane — MasterRules

**Scope:** Excel-Projekte (z. B. DISPO Tool)  
**Prinzip:** Stabilität vor Feature-Ausbau. Kein Makro-Chaos.

## Excel-Regelwerke (Index)
- `MR-EXCEL-LANE-00` — diese Sammelsektion (Excel Lane)
- `MR-EXCEL-DISPO-CORE-01` — DISPO Tool: Single-Module Core + Anti-Chaos

## Grundsätze
- **Single Source of Truth**: Tabellen sind Datenquelle; keine Parallel-Wahrheiten in Views.
- **Single Source of Code**: Fachlogik zentralisiert (projektabhängig, i. d. R. `m_*_Core`).
- **Formelspalten sind tabu**: Makros dürfen Formelspalten nicht überschreiben.
- **Button-Disziplin**: Buttons rufen eindeutige Entry-Points auf (`BTN_*`).

## Enforcement
- Verstöße gelten als **P0** → Rollback/Backup + Diagnose.

<!-- MR_EXCEL_LANE_00_END -->


<!-- MR_EXCEL_DISPO_ASSIGN_02_BEGIN -->
## MR-EXCEL-DISPO-ASSIGN-02 — DISPO: Assign-Algorithmus (Prio-Pässe, Tie-Breaker, Cap)

**Zweck:** Verhindert „MA-Spam“, Tabellenreihenfolge-Bias und Silent-Fails.  
**Scope:** DISPO Tool / Excel Lane  
**Status:** ACTIVE

### A02-1 — SkillReq-Datenvertrag (Mapping-Pflicht)
- `t_DISPO_Slots[SkillReq]` darf `Skill_XX` enthalten **nur wenn** ein Mapping existiert:
  `Skill_XX -> Spaltenname in t_MA_Skills` (z. B. Aufgaben-Spalten `Mozart`, `ASM`, …).
- Wenn Skill-Spalte fehlt oder Mapping nicht möglich:
  - Assign darf **nicht** komplett blockieren,
  - `Hinweis` wird gesetzt (z. B. `SKILLCOL_MISSING`), Candidate-Check wird „soft“.

### A02-2 — Prio-Pässe sind Pflicht
- Assign verarbeitet Slots strikt in Durchgängen:
  1) Prio=1
  2) Prio=2
  3) Prio=3
- Andere Reihenfolgen sind **nicht zulässig**.

### A02-3 — Tie-Breaker ist Pflicht (Run-Load)
- Score muss mindestens enthalten:
  - Fairness (historisch, aus `t_Fairness`)
  - Run-Load (wie oft der MA im aktuellen Lauf schon vergeben wurde)
- Ohne Run-Load führt Gleichstand zu „erster in Tabelle gewinnt“ ⇒ **Regelverstoß**.

### A02-4 — Hardcap pro Lauf
- Maximal **3 Slots pro MA** pro Assign-Lauf (Standard).
- Cap darf ausschließlich über `Vorschlag`/`Hinweis` gesteuert werden.
- **Nie** schreiben in: `Final`, `Final_ID`, `Status` (siehe MR-D4).

### A02-5 — Kein Silent-Fail
- Wenn kein Kandidat gefunden oder Cap blockt:
  - `Vorschlag` bleibt leer,
  - `Hinweis` wird gesetzt (z. B. `CAP_OR_NO_MATCH`).
- Ursachen müssen dadurch sichtbar bleiben.

### A02-6 — Determinismus & Reproduzierbarkeit
- Ergebnis darf nicht von Zufall abhängen.
- Änderungen am Algorithmus erfordern Gate-Test:
  BuildSlots → EnsureFormulas → Assign → Reset.

<!-- MR_EXCEL_DISPO_ASSIGN_02_END -->



## MR-EXCEL-VBA-COMPILE-GATE-01 — VBA: Compile-Gate ist Pflicht (Excel Lane)
**Scope:** Excel / DISPO Tool  
**Status:** ACTIVE  
**Owner:** Assistent

### Regel
- Nach strukturellen VBA-Änderungen: **Debuggen → VBAProject kompilieren**.
- Arbeiten auf rotem Compile-Status ist verboten.

### Enforcement
- Compile nicht grün ⇒ Rollback + Diagnose.


## MR-EXCEL-VBA-PARSER-BYPASS-01 — VBA: Parser-Bypass bei „gelbem Funktionskopf“
**Scope:** Excel / DISPO Tool  
**Status:** ACTIVE  
**Owner:** Assistent

### Regel
- Bei 2× identischem Syntaxfehler mit gelbem Funktionskopf:
  - Modul sichern
  - Modul leeren
  - Minimal-Sub kompilieren
  - Logik als Single-Sub inline herstellen
  - Erst danach modularisieren

### No-Gos
- Keine Mini-Flicks am Funktionskopf.


## MR-EXCEL-MAIL-SSOT-01 — DISPO: Mail ist SSOT-tabellenbasiert
**Scope:** Excel / DISPO Tool  
**Status:** ACTIVE  
**Owner:** Assistent

### Regel
- Mail liest nur aus:
  - `t_DISPO_Slots`
  - `t_Status_Zahlen`
- VIEW ist Anzeige, nicht Datenquelle.

### KPI Pflicht
- KPI immer enthalten.
- Fehlende Tabelle/Spalten ⇒ harter Fehler.

<!-- MR_RESUME_ANCHOR_POLICY_BEGIN -->
## MR — Resume-Anchor Pflicht (Pipeline-Anker)

Bei Kontextwechsel oder Pause ist ein Resume-Anchor Pflicht.

### Mindestinhalt
- letzter stabiler Runner
- aktive Lane
- nächster Schritt
- nächste Runner-ID

### Enforcement
Ohne Anchor kein neuer Runner.

<!-- MR_RESUME_ANCHOR_POLICY_END -->

<!-- SHRIMPDEV_CURRENT_ANCHOR_BEGIN -->
=== RESUME ANCHOR ===
Anchor-ID: ANCHOR-PRE-EXCEL-2026-02
Runner: R8421 (last stable pre-Excel core work)
Lane: B — Boundary/Härtung
Context: UI ↔ logic_actions Entkopplung + Boundary-Regeln (pre-Excel)
Next: DIAG Boundary Drift (active UI scan)
Next Runner: R8432
=====================
<!-- SHRIMPDEV_CURRENT_ANCHOR_END -->



<!-- MR_ANCHOR_POLICY_01_BEGIN -->
## MR-ANCHOR-POLICY-01 — Resume-Anchor Pflicht (Pipeline-Anker)

**Zweck:** Wiedereinstieg ohne Kontextverlust, Drift vermeiden.

### Regel
- Bei **jedem Kontextwechsel**, **Lane-Wechsel** oder **Pause** wird ein **Resume-Anchor** gesetzt.
- Anchor wird **per Runner** geschrieben (DOCS-only), nicht manuell.

### Mindestinhalt
1. Letzter stabiler Runner (ID + Kurz-Zweck)
2. Aktive Lane
3. Nächster Schritt (genau 1 Task)
4. Nächste freie Runner-Nummer

### Enforcement
- **Ohne Anchor kein neuer Runner-Start.**
- Anchor wird bei relevanten Änderungen aktualisiert.

<!-- MR_ANCHOR_POLICY_01_END -->

<!-- MR_PROTECT_R8433_BEGIN -->
## MR — Protected Runner: R8433 (Quality Gate)

**R8433 ist geschützt.**
- Nicht löschen, nicht umbenennen, nicht ersetzen.
- R8433 ist der Standard-Gatekeeper für UI-Boundary-Drift.

### Pflicht-Ausführung
Nach jeder Änderung an:
- `modules/ui_*.py`
- `modules/logic_actions*.py`
- Bridge/Adapter im UI↔Logic Umfeld

### Gate-Regel
- R8433 ExitCode **2** (P0) ⇒ **SOFORT STOP**
- Erst weiter, wenn **P0=0**.

### Zielzustand
- Minimum akzeptiert: **YELLOW** (P1/P2 = Technikschuld)
- Pflicht: **P0=0**

<!-- MR_PROTECT_R8433_END -->

---

## MR-SYSTEM-MAP-01: System Map ist Pflicht (Living Map)

**Ziel:** Wir verhindern dauerhaft „Drölf-Module-Chaos“ durch eine **aktuelle, zentrale Map** des Systems.

### Regel
- Für **jedes Projekt** existiert eine **System Map** als Markdown (living doc).
- Die Map wird **primär per Runner** erzeugt/aktualisiert (kein manuelles Rumgefummel).
- Jede Änderung an **Sheets, Tabellen, Modulen, Entry-Points, Contracts** muss in der Map reflektiert sein (automatisch oder im Nachgang sofort).

### Mindestinhalt einer System Map
- **Workbook/Surface:** Sheets (Name + CodeName), Buttons/Entry-Points, Ereignisse.
- **Datenmodell:** alle relevanten **ListObjects** inkl. Spalten-Contract (Headernamen), Schlüssel, Statusfelder.
- **Code:** Module + Public Entry-Points + wichtigste Helper; grober Call-Flow (Neuer Tag / Tagesabschluss / Planung / Mail).
- **Risiko-Zonen:** bekannte Kollisionen (Mehrdeutige Namen), kritische Abhängigkeiten, Smoke-Checks.

### Ablage
- Repo-weit: `docs/FILE_MAP.md` enthält einen Index/Links.
- Projekt-Map: z. B. `Excel-Projekte/<Projekt>/SYSTEM_MAP.md`.

### Gate
- Neue Features/Fixes dürfen **nur** gemergt werden, wenn:
  - Runner „Map Refresh“ erfolgreich ist (Report + Diff),
  - und keine Mehrdeutigkeits-/Compile-Fehler durch neue Namen entstehen.

## System Map Pflicht (Excel-Projekte / DISPO)

### Zweck
Damit keine “Mehrdeutiger Name / Sub nicht definiert / Variable nicht definiert”-Hölle mehr entsteht,
gibt es eine zentrale, maschinenlesbare System Map pro Excel-Projekt.

### Artefakt
- Datei: `Excel-Projekte/Dispo-Tool/SYSTEM_MAP.md`
- Inhalt (Minimum):
  - Sheets (CodeName ↔ Blattname)
  - ListObjects (Tabellen) + Spaltenreihenfolge (Header-Contract)
  - Module + Public Entry Points (Buttons/Runner-Entry)
  - Known Hotspots (z. B. Namenskollisionen)
  - Optional: Named Ranges / Buttons / Shape-Makros

### Regeln (verbindlich)
1. **Jede Änderung** an:
   - Tabellen (Name/Spalten/Reihenfolge),
   - VBA-Modulen,
   - Public Subs/Functions,
   - PlanDate-/Fairness-Logik,
   muss **sofort** in der System Map reflektiert werden.
2. Updates erfolgen **nur** über den Runner `SystemMap_Update` (kein Handpflegen).
3. Vor jedem “größeren” Fix gilt: **Map aktualisieren → Compile prüfen → erst dann Patch**.

### Routine
- Bei jedem Runner, der VBA/Tabellen verändert:
  - am Ende automatisch `SystemMap_Update` ausführen
  - Reportlink im jeweiligen Runner-Report vermerken


<!-- R9002_RULES_BEGIN -->
## MR-DISPO-01 — Produktionsmaßstab DISPO
„Fertig“ bedeutet reproduzierbar + alltagstauglich, nicht nur funktionsfähig.

## MR-FOCUS-01 — Ein Hauptthema pro Session
Bei komplexen Systemen wird pro Session genau ein Kernziel verfolgt. Nebenthemen werden geparkt.

## MR-CONTENT-01 — Clarivoo Qualitätsregel
Qualität vor Seitenanzahl. Jede Seite braucht echten Mehrwert.

## MR-ROTATION-01 — Lane-Disziplin
Rotation erst nach erreichter Minimal-Stabilität im aktuellen Lane-Thema.
<!-- R9002_RULES_END -->

## XCL / Excel-Projekte

**Arbeitsordner (Root)**
- `C:\Users\rasta\OneDrive\ShrimpDev_REPO\Excel-Projekte\`

**Projektstruktur**
- Jedes XCL-Projekt liegt als eigener Unterordner unter `Excel-Projekte\`
- **Reports sind zentral** (nicht projektbezogen) und liegen ausschließlich in:
  - `C:\Users\rasta\OneDrive\ShrimpDev_REPO\Excel-Projekte\Reports`

**Reports (verbindlicher Zielpfad)**
- Alle XCL-Runner-/Diagnose-/Export-Reports schreiben nach:
  - `C:\Users\rasta\OneDrive\ShrimpDev_REPO\Excel-Projekte\Reports`

**SYSTEM_MAP (Ort / Governance)**
- `SYSTEM_MAP.md` ist **projektbezogen** und liegt im jeweiligen Projektordner:
  - `Excel-Projekte\<Projekt>\SYSTEM_MAP.md`


<!-- R8590 AUTO-APPEND START -->
## R8590 (Nachsorge) – Regeln für VBA-HTML-Patches (2026-02-15 00:57:01)

- Bei `"<...>" & _`-HTML-Verkettung: **keine Insert-Trial-&-Error**.
- Änderungen bevorzugt als **kompletter Function-Replacement (1:1)** oder minimaler Patch mit stabilen Anchors.
- **Diagnose zuerst:** Zielblock sichern, dann nur 1 Änderung, sofort testen.
- Debug-Marker nicht als Plain-Text in HTML ausgeben (nur Comment/Report).

<!-- R8590 AUTO-APPEND END -->

<!-- BEGIN:R8605 -->
## R8605 Beobachtungen (noch nicht als neue MR finalisiert)
- PlanDate kann als Text vorliegen → Parsing/Setzung prüfen.
- Doppelte Funktionsnamen in VBA verursachen 'Mehrdeutiger Name' → konsistente Prefix-Strategie.
- ListObject-Delete/Lookup robust per Loop statt Name-Lookup+Unlist.
<!-- END:R8605 -->

