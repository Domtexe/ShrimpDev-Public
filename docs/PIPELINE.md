<!-- PIPELINE_V1_START -->
# PIPELINE v1 — Lanes & Turnus (Source of Truth)

<!-- R9108:PIPELINE_INSERT:BEGIN -->

<!-- R9433_COMPLIANCE_GATE_BEGIN -->
## [P1] Runner Compliance Gate (Stabilität / Anti-Drift)

**Ziel:** Sicherstellen, dass Runner dauerhaft MR- und Pipeline-konform bleiben.

### Hintergrund
- R9432 liefert ersten DIAG-Scan (46 Runner, 0 FAIL, 2 WARN)
- Bedarf: systematische Hygiene-/Compliance-Prüfung
- Ergänzung zu R9417 (Gate), kein Ersatz

### Scope
- tools/R*.py + .cmd Struktur
- Report-/Backup-Konventionen
- gefährliche Patterns (destructive ops, silent exceptions)
- Basis-MR-Konformität

### Architektur
- DIAG-first (kein Auto-Fix)
- spätere Erweiterung möglich (Preflight / Soft-Enforcer)
- Nutzung bestehender Validator-Logik (R9417)

### DoD
- Compliance-Scan liefert reproduzierbaren Report
- keine Eingriffe in bestehende Runner
- klare Trennung: Diagnose vs. Fix

### Status
- R9432 implementiert (DIAG v1)
- weitere Iteration optional (R9433+)

### Nächster Schritt
- ggf. R9434: Erweiterter DIAG (tieferer MR-Check)
- optional später: kontrollierter Fix-Runner (nur sichere Fälle)

<!-- R9433_COMPLIANCE_GATE_END -->

# P0 — Codex Integration (PRIO 0, ganz vorne)
**Ziel:** Codex als kontrollierter Runner-Worker, der konsequent `DIAG → 1 Fix → Smoke → Report` erzwingt.

## TODOs (P0)
- [ ] Codex CLI installieren & Projekt-Trust setzen (lokal) + Basiskonfig (read-only default)
- [ ] Projekt-Konfig: .codex/config.toml im Repo (read-only → workspace-write nur für Fix-Runner)
- [ ] Runbook: docs/CODEX_RUNBOOK.md (No-Gos: keine Rewrites, DIAG first, max 1 Fix, Smoke Pflicht)
- [ ] Runner-Set (cmd+py): codex_readonly, codex_diag, codex_fix_one
- [ ] Smoke-Runner: smoke_min (Start/Import/GUI sanity, Exit-Codes, Report)
- [ ] Reports erweitern: Diff-Übersicht, betroffene Dateien, Tests, „Was wurde NICHT geändert“

---

# P0 — ShrimpDev Intake/Layout Stabilisierung (kein Raten mehr)
## TODOs (P0)
- [ ] Call-Site DIAG: echten Intake-Builder finden (Name/Ort/Signatur) + Call-Sites belegen
- [ ] Layout-Fix (nur 1 Patch): LEFT=Intake, RIGHT=Output+Toolbar+Tree (erst messen, dann fixen)
- [ ] Treeview leer: Datenquelle/Bindings/Refresh messen (Logs), dann minimal fixen
- [ ] Doppelte UI-Blöcke: erst entfernen, wenn neue Verdrahtung verifiziert ist (Smoke grün)

<!-- R9355_PIPELINE_BEGIN -->
## 2026-03-08 — Intake/Runner/Inbox Stabilisierung (Session R9355)

- DONE: Intake-Stabilisierung ergänzt:
  - `_build_intake()` mit Instanz-Guard gegen Mehrfachaufbau
  - Right-Stack bleibt `Output -> Toolbar -> Tree`
  - R9207-DIAG auf Endzustand ausgerichtet
- DONE: Runner Output Capture:
  - CMD-Runner `stdout/stderr` live in OutputDisplay
  - Spiegelung ins Log (debug/log tab Quelle)
- DONE: Tree/Run UX:
  - R9256-Methoden als echte `ShrimpDevApp`-Methoden
  - Run-End-to-End verifiziert
  - Tree-Suche + Runner-Counter/Trefferanzeige wieder aktiv
- DONE: Idea Inbox / Import-Orchestrierung:
  - Brainstorm-Inbox (`docs/IDEA_INBOX.md`, `docs/IDEA_INBOX_SPEC.md`) produktiv
  - Import-Flow vereinfacht auf `GUI -> R9341 -> interne Kette`
  - `NEW -> IMPORTED` nur bei vollständigem Erfolg
  - `R9418` dient als Feeder fuer `docs/IDEA_INBOX.md`; `docs/ideas/ideas_inbox_*.md` ist nur optionales Archiv
- DONE: Rechte Toolbar Actions repariert:
  - `_cmd_trash`, `_cmd_rename`
  - `action_autopush_both`, `action_purge_one`
  - `action_guard_futurefix_safe`, `action_r9998`, `action_r9999`
  - Delete konservativ via `tools/_trash/`
- DONE: Purge-Schutzlisten aktualisiert (SSOT):
  - `registry/tools_keep.txt`
  - `registry/runner_whitelist.txt`
  - relevante IDs: `R9325`, `R9326`, `R9331`, `R9332`, `R9333`, `R9341`
- DONE: Protected special runners erweitert:
  - geschuetzte IDs: `R9418`, `R9419`, `R9420`, `R9421`, `R9999`, `R1802`
  - GUI-Quick-Launch fuer `R9418` bis `R9421` im bestehenden Service-Bereich
  - Delete-Guard blockiert geschuetzte Runner im normalen Trash-Pfad

### Offene Folgepunkte (sauber markiert)
- [ ] Undo-System für Tree-Aktionen weiter ausbauen (persistenter/robuster Undo-Stack)
- [ ] Trash-Manager/Restore-Flow für `tools/_trash/` ergänzen
- [ ] Auto-Disable für Toolbar-Buttons bei fehlenden Preconditions (Selection/Runner-Presence)
- [ ] Import-Ideas-Button in den Tab `Pipeline` verschieben (minimal-invasiv, bestehende Handler/Flow beibehalten)

### Neu priorisiert (Intake/GUI/Stabilität)
1. [P1] Drift Radar for GUI Hooks / Runner Wiring
- [ ] Scan auf:
- [ ] Buttons ohne funktionale Zielaktion
- [ ] `ui_action_bridge` Wrapper ohne `logic_actions` Target
- [ ] erwartete App-Hooks, die `None` sind
- [ ] Methoden, die falsch verschachtelt statt Klassenmethoden sind
- [ ] Runner-Buttons mit fehlenden Preconditions / fehlender Selection-Logik
- [ ] erst Report-only
- [ ] Ziel: Drift früher erkennen, GUI-/Runner-Ausfälle vorbeugen
2. [P1] Intake Toolbar Smart Disable / Enable
- [ ] Buttons im rechten Intake-Kontext nur aktivieren, wenn Preconditions erfüllt sind
- [ ] Beispiele:
- [ ] Delete / Rename / Run nur bei Tree-Selection
- [ ] Undo nur bei verfügbarer Undo-History
- [ ] Push / Purge nur bei erfüllten Guard-/Repo-Preconditions
- [ ] Ziel: weniger Fehlklicks, klarere Zustände
3. [P1] Trash Manager / Restore for tools/_trash
- [ ] Restore-Flow für versehentlich verschobene Runner
- [ ] optional Empty Trash / Review-Liste
- [ ] Ziel: sicherer Delete-Workflow
4. [P2] Runner Favorites / Quick Launch
- [ ] häufig genutzte Runner direkt im GUI startbar
- [ ] optional mit Favoritenliste / zuletzt genutzt

## 2026-03-17 — Stabilisierungskonsolidierung nach Intake/Validator/Popup/T666-Block

- DONE: Validator-/Gate-Pfad differenziert stabilisiert:
  - `R9417` blockiert GUI-Runs nicht mehr stumpf wegen global dirty worktree
  - Meta-/Maintenance-Runner werden enger und bewusster bewertet
  - normale Runner kippen nicht mehr automatisch auf `FAIL`, wenn nur globaler Repo-Schmutz vorliegt
  - `tmp/`, `.git/`, `__pycache__/` zählen nicht als harte Zusatz-Zonen
- DONE: GUI-Runner-/Popup-Pfade konsolidiert:
  - Standard-GUI-Runner laufen ueber Executor + OutputDisplay
  - `Push` / `Purge` laufen popup-frei auf dem kanonischen Pfad
  - Output-Marker `RUNNER START` / `RUNNER END` sind sichtbar
- DONE: Intake-/TreeView-UX stabilisiert:
  - Sort-State persistent
  - Rebuild/Refresh deterministischer
  - Reentry-/Inflight-Probleme entschärft
  - Tree nutzt den INI-gebundenen Scope
  - Hybrid-Refresh + ruhigeres Restore von Selection/Scroll
  - Rechtsklick-Kontextmenue fuer den aktiven Runner-/Intake-Tree:
    - `Run`
    - `Copy Name`
    - `Copy Pfad`
    - `Datei öffnen`
    - `Im Explorer öffnen`
    - `Letzten Report öffnen`
    - `Auswahl in Suche übernehmen`
    - `Refresh`
- DONE: Nachsorge-/Diagnose-Runner verifiziert:
  - `R9425`
  - `R9341`
  - `R2693`
  - `R2224`
  - `R9419`
- DONE: `T666` konsolidiert:
  - wiederhergestellt
  - purge-geschützt
  - Universal Runner Engine mit `diag`, `smoke`, `filecheck <path>`, `echo <text>`
  - `T666.cmd` reicht `%*` durch
- DONE: Protected-Runner-Audit konservativ abgeschlossen:
  - keine unüberlegte Entschützung
  - keine Button-Entfernung ohne klar belegte Redundanz

### Statusbewertung
- Intake ist nicht mehr akute P0-Baustelle.
- Runner-/Popup-/Gate-Pfade sind aktuell stabil genug fuer regulaere Pipeline-Arbeit.
- Verbleibende Punkte sind Nachpflege/UX-Reste, keine Stop-the-line-Themen.

### Offene Restpunkte (bewusst offen)
- [ ] Tk-`after`-Callbacks beim GUI-Destroy weiter sauber beobachten/haerten
- [ ] Failure-Signal-Noise in `R9424` spaeter reduzieren
- [ ] Context-Menue/Tree-UX im Alltag beobachten, aber ohne neue Architektur

### Naechster sinnvoller Hauptfokus
1. [P1] Regulaere Pipeline-Arbeit auf stabilisierter GUI-/Runner-Basis fortsetzen
2. [P1] Runner-/Report-Hygiene und kleine Follow-up-Diagnosen statt weiterer Intake-Grundsatzumbauten
3. [P2] Nur noch gezielte UX-/Toolbar-Nachpflege, wenn echte Befunde vorliegen
<!-- R9355_PIPELINE_END -->

---

# P0 — Diagnose-Gates & Anti-Drift
## TODOs (P0)
- [ ] Diagnose zuerst erzwingen: Wenn Fix nicht beim 1. Versuch verifiziert → Diagnose-Runner Pflicht
- [ ] Anchor-Patch Prinzip: 1 Runner = 1 klarer Fehler, keine Multi-Patches
- [ ] Pre-Start Gate: Import/Syntax/Smoke vor GUI-Work (Reportpflicht)

---

# P1 — Purge/Whitelist SSOT finalisieren
## TODOs (P1)
- [ ] Purge strikt Whitelist (Exact-only), keine Patterns
- [ ] Schutz-Count normalisieren: Ursachen dauerhaft abstellen (Scan-Breite/Doku-Effekt)
- [ ] Kritische Runner absichern: Wiederherstellung + Schutzregeln (z. B. T666 & Co.)

---

# P1 — RUN/DirectRun/Compile-Gate Stabilität
## TODOs (P1)
- [ ] RUN soll ausführen, nicht Generator eskalieren (cmd+py Standard bleibt)
- [ ] RunnerExec/DirectRun Regeln dokumentieren + enforced

---

# P1 — Nachsorge Pflichtpaket (Runner-basiert)
## TODOs (P1)
- [ ] Nachsorge-Runner immer: Backups + Report + marker-basierte Docs-Updates

---

# P2 — Stabilitäts-Metriken (Crash-Ideen)
## TODOs (P2)
- [ ] Crash-Heatmap, Wiederholquote, Zeit-of-Pain
- [ ] Hot/Cold Modul-Matrix
- [ ] Stabilitäts-Score in GUI

<!-- R9108:PIPELINE_INSERT:END -->

<!-- SHRIMPDEV_AUTOGEN:R8476 PIPELINE START -->
## RUN Stabilisierung (Programm) — Direct Mode + RunnerExec Neubau

**Kurzfazit:** RUN ist P0-kritisch. Ziel: Kontrolle zurückholen → dann sauber neu aufbauen.

### Lane A — Stabilität / Start / Crash

- A-P0-01: RUN wieder funktionsfähig via Direct-Run Bypass
- DoD: RUN startet zuverlässig aus Tree-Selection, nicht Intake; vollständiger Run-Context; sichtbarer rc/Report.
- Runner-Sequenz: DIAG wiring → APPLY DirectRun (ein Einklinkpunkt) → DIAG End-to-End.

- A-P0-02: Compile-Gate blockierend vor RUN & APPLY (Code)
- DoD: Gate läuft automatisch; FAIL ⇒ rc=7; keine Folgepatches.

- A-P1-01: RunnerExec Clean-Rebuild (minimal, testbar)
- DoD: neu, klein, stabil: run(cmd, args, cwd) + logging + rc; optional threading sauber getrennt; Smoke-Tests.

- A-P1-02: Protected-Files Schutzglas (Infra-Runner only)
- DoD: Protected-Liste + Infra-Runner-Template (Backup/Diff/Gate/Smoke) + MR-Verweis.

### Lane B — Core-Funktionalität

- B-P1-01: SSOT-Refactor RUN (Selection-only)
- DoD: alle RUN-Actions holen Context aus Selection; Intake nur Preview/Defaults.

### Lane C — Tooling / Automationen

- C-P1-01: Legacy Sweep — BAT-Reste inventarisieren & neutralisieren
- DoD: Report: alle .bat + Referenzen; entfernen/archivieren; keine produktiven Callsites.

- C-P1-02: Report-Agent MVP (Reports → Todos → Priorisierung, read-only)
- DoD: Scan letzte Reports; dedup Root-Causes; Vorschläge Lane/Priority; kein Auto-Write.

### Lane D — Governance / Doku

- D-P1-01: MR-Update Block “Stop-the-line / Protected / SSOT / Bypass”
- DoD: MR-Kapitel mit H1–H7 + H2a (Docs-only Ausnahme).

- D-P1-02: PIPELINE-Schärfung für diese RUN-Stabi-Serie
- DoD: DoD & Runner-Sequenzen klar; P0 Lane A hat Vorrang.
<!-- SHRIMPDEV_AUTOGEN:R8476 PIPELINE END -->

- [x] (DONE) Agent-Tab Empfehlungen stabilisiert: R2086 baseline/delta + R1802 Stamp (Agent_LastDiag.json) + robust anchors (R3837–R3844).
## Tech Debt / Hygiene

<!-- R8526_PIPELINE_DEDUP_BEGIN -->
## R8526 — Pipeline Konsolidierungs-Index (Docs-only)

<!-- AUTO:PIPELINE_META -->

## Meta / Governance
- Änderungen müssen docs-konsistent sein (MasterRules, FILE_MAP, PIPELINE, SHORTCODES).
- .cmd ist Standard-Runnerformat (keine .bat).

- Stand: 2026-02-21 21:12:44
- Tasks gescannt (task-like): 241
- Normalisierte Keys gewertet: 223
- Potenzielle Dubletten (Keys mit >1 Vorkommen): 4

**Regel:** Dies ist eine *Hinweis-/Arbeitsliste*. Keine Einträge wurden gelöscht oder umsortiert.

### Cluster-Übersicht (heuristisch)
- Reports / Diagnose / Logs: 1
- Governance / MR / Pipeline: 2
- Other: 1

### Dubletten-Kandidaten (Top)
- todo implement logic here _(Vorkommen: 2)_
- L427 | Lane F: - [ ] (P3) [CORE] TODO: implement logic here (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L15280)
- L463 | Lane F: - [ ] (P3) [CORE] TODO: implement logic here (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_943_NewRunner.py:L49)
- todo list add a high priority item about tracebacks in log _(Vorkommen: 2)_
- L429 | Lane F: - [ ] (P3) [CORE] TODO: list: add a high-priority item about tracebacks in log. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19969)
- L442 | Lane F: - [ ] (P3) [CORE] TODO: list: add a high-priority item about tracebacks in log. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2144.py:L118)
- todo pipeline eigener gui tab masterrules viewer open refresh n _(Vorkommen: 2)_
- L395 | Lane F: - [x] (P1) [CORE] TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh).\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19950)- [ ] (P1) [CORE] TODO: ) Pipeline-Eintrag: Tracebacks wieder ins Log (HIGH) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19967)
- L399 | Lane F: - [ ] (P1) [CORE] TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh).\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2143.py:L250)
- todo pipeline sondern bekommen einen eigenen tab _(Vorkommen: 2)_
- L394 | Lane F: - [ ] (P1) [CORE] TODO: (Pipeline), sondern bekommen einen eigenen Tab. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19929)
- L398 | Lane F: - [ ] (P1) [CORE] TODO: (Pipeline), sondern bekommen einen eigenen Tab. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2143.py:L2)

### Empfehlung (manuell, später)
- Pro Dublette: 1 kanonischen Task definieren, Rest als Referenz/Archived markieren oder zusammenführen.
- Wenn Runner-Artefakte fehlen: Phantom/Archived taggen (bestehende Regel beibehalten).

<!-- R8526_PIPELINE_DEDUP_END -->

<!-- ACTIVE_TASK:START -->
- [ ] (LOW) Runner-WARN venv python not found / Template-Policy: WARN ist kosmetisch; Templates greifen nur bei Neugenerierung; optional später REQUIRE_VENV-Flag (WARN nur wenn explizit verlangt).
## ACTIVE_TASK
<!-- ACTIVE_TASK:END -->

<!-- LANE_OVERVIEW:CANONICAL -->
## 🧭 Pipeline-Lanes – Überblick (kanonisch)

| Lane | Zweck | Typische Tasks | Standard-Priorität |
|------|------|---------------|--------------------|
| **A** | Stabilität, Startfähigkeit, Crash/Import-Risiken, Safety | DIAG → APPLY, Guarding, Smoke-Tests | **P0/P1** |
| **B** | Core-Funktionalität ShrimpDev/ShrimpHub (UI/Features) | APPLY (modular), kleine Verbesserungen | **P1/P2** |
| **C** | Tooling & Automationen (Build/Patch/Push/Scans) | DIAG/APPLY, Hygiene, Automatisierung | **P1/P2** |
| **D** | Regeln, Doku, Governance, Konsistenz | DOCS-only, Pipeline-Schärfung | **P1/P2** |
| **E** | Websites/SEO/Monetarisierung (Shirimpi) | Ideen → Plan → Umsetzung | **P2/P3** |

**Turnus (Rotation):** A → B → C → D → E → repeat  
**Hard-Override:** Wenn in **Lane A** ein **P0** existiert, hat das Vorrang vor Rotation.  
**Arbeitsmodus:** *Diagnose zuerst*, dann **minimal-invasiver Fix**, immer mit Backup + Report.

---

## 2026-03-17 — Ideen-Konsolidierung / Pipeline Intake

Ziel dieses Blocks: neue Ideen kanonisch einsortieren, Dubletten bündeln und nur realistisch priorisierte Sammel-Tasks aufnehmen.

Status-Konvention in diesem Block:
- `PLANNED` = sinnvoller Kandidat fuer einen baldigen echten Arbeitslauf
- `IDEA` = valide Idee, aber noch nicht terminiert
- `LATER` = wertvoll, aber bewusst nachgelagert
- `PARKED` = Vision/Portfolio, aktuell nicht in aktiver Umsetzung

### Lane A — Stabilität / Diagnose / Drift-Vermeidung
- [ ] (P1) [PLANNED] Docs Consistency Check
  - Ausbau fuer `docs`-Konsistenz gegen `PIPELINE`, `FILE_MAP`, `MasterRules`, Runner-Reports
  - bündelt: `Docs Consistency Check`, `Docs-Update Pflichtcheck`, `MasterRules Drift Check`
  - Wert: Drift-/Fehlervermeidung, gute Runner-Kandidatur
- [ ] (P1) [PLANNED] Regression Radar
  - konservative Frühwarnung über Compile-/Report-/Runner-Signale
  - bündelt: `Regression Radar`, `Failure Memory System`, `Failure Pattern Detector`, `Runner Failure Pattern Analyzer`, `Fehlerchronik mit Ursachenclustern`
  - strategisch wichtig
- [ ] (P1) [PLANNED] GUI Binding / Self-Test Audit
  - prüft Buttons, Bindings, Auswahl-Preconditions und offensichtliche Dead-Callbacks
  - bündelt: `GUI Button Self-Test`, `Button Binding Audit`
- [ ] (P2) [LATER] Runner-Compliance-Ausbau (nur falls echter Bedarf belegt ist)
  - kein pauschaler Pflicht-Overhead fuer jeden Runner
  - nur gezielte Erweiterung bei realen Befunden aus Validator/Reports
  - R9432 bleibt als einfacher DIAG-Baustein verfuegbar
- [ ] (P2) [IDEA] Command Center View
  - Ausbau des bestehenden Health-/Dashboard-Gedankens
  - bündelt: `Command Center View`, `Pipeline Heatmap Cockpit`, `System Health Dashboard`, `Repo Time Machine` (nur read-only/report-orientiert)
  - strategisch wichtig, aber kein P0
- [ ] (P2) [IDEA] Output / Log Mirror Hardening
  - konsistente Sicht auf OutputDisplay, Logs und Runner-Reports
  - bündelt: `Output/Log Mirror`
  - strategisch wichtig


<!-- R9434_RUNNER_CLASSIFICATION_BEGIN -->
## 2026-03-17 — Runner-Klassifikation / risikobasierte Compliance

Ziel dieses Blocks: Runner nicht pauschal mit maximalem Overhead belasten, sondern nach Risiko- und Zweckklasse behandeln.

### Grundsatz
- Nicht jeder Runner braucht Backup + Report + Gate in voller Staerke.
- Es gilt: **risikobasiert statt pauschal**.
- Systemschutz erfolgt primaer ueber:
  - `R9417` Validator / Gate
  - Reports
  - gezielte DIAG-Runner
  - Pipeline-/MR-konforme Nachsorge bei echten Aenderungen

### Runner-Klassen
1. **CORE / APPLY Runner**
   - veraendern produktive Dateien, Governance, Struktur oder kritische Ablaufe
   - Pflicht: Backup, Report, klare Logs
   - je nach Risiko: Compile-/Import-Gate und/oder Validator sinnvoll

2. **DIAG Runner**
   - lesen/messen/analysieren nur
   - Pflicht: nachvollziehbarer Output, in der Regel Report
   - kein unnoetiger Backup-/Gate-Overhead

3. **UTILITY / FAST Runner**
   - kleine Hilfsrunner, Smoke/echo/filecheck/artige Kurzlaeufer
   - Pflicht: klarer Output
   - Report/Backup nur wenn der konkrete Zweck es verlangt

### Operative Regel
- **APPLY = streng**
- **DIAG = leicht**
- **UTILITY = minimal**

### Folge fuer die Pipeline
- Ein pauschaler Ausbau eines globalen Runner-Compliance-Gates fuer *alle* Runner ist aktuell **nicht** der naechste Anchor-Task.
- Stattdessen werden echte Befunde aus Validator, Reports und produktiven Vorfaellen gesammelt und nur dann gezielt nachgeschaerft.

### Status
- `R9432` bleibt als einfacher DIAG-Scan nuetzlich, aber ist kein Zwangs-Framework fuer jeden Runner.
- Der vorherige breit gedachte Compliance-Gate-Task wird bewusst nach hinten gestellt.
<!-- R9434_RUNNER_CLASSIFICATION_END -->


### Lane B — ShrimpDev Core / GUI / Workflow
- [ ] (P1) [PLANNED] Runner Explorer UX
  - bündelt: `Runner-Finder mit Filtern`, `Last Report Button`, `Protected IDs Übersicht`, `Recent Files Panel`
  - schneller GUI-/Produktivitäts-MVP
- [ ] (P2) [IDEA] Pipeline Quick Add
  - schneller Add-/Capture-Weg aus GUI oder Runner-Reports in die kanonische Pipeline
  - strategisch wichtig
- [ ] (P2) [IDEA] Dependency / Change Impact Viewer
  - bündelt: `Dependency Map Viewer`, `Change-Impact Viewer`, `Runner Dependency Map`
- [ ] (P2) [IDEA] NextFree-ID Wächter
  - kleine Guard-/Produktivitätsidee für Runner-/ID-Pflege
- [ ] (P3) [PARKED] Personal Ops / Knowledge Cluster
  - bündelt: `Personal Ops Dashboard`, `Simple Knowledge Vault`, `Offline SOP Viewer`, `Sticky Notes für Projekte`, `Idea-to-Project App`

### Lane C — Tooling / Automation / Governance-Tooling
- [ ] (P1) [PLANNED] Idea Inbox Normalizer
  - normalisiert/prüft Inbox-Einträge vor Import oder Review
  - bündelt: `Idea Inbox Normalizer`
  - strategisch wichtig
- [ ] (P1) [PLANNED] Codex Call Wrapper Standard
  - standardisierte Wrapper/Argumente/Report-Konventionen für Codex-Runner-Aufrufe
  - bündelt: `Codex-Call Wrapper Standard`, `Codex-Aufruf mit Standardargumenten`
- [ ] (P2) [IDEA] Prompt-to-Runner Engine
  - nachgelagerte Ausbaustufe auf Basis des Codex-Wrapper-Standards
  - bündelt: `Prompt-to-Runner Engine`
- [ ] (P2) [IDEA] Pipeline / Nachsorge Automation
  - bündelt: `Automatische Pipeline-Nachpflege`, `Docs-Sync nach Runner-Lauf`, `Fehlerfälle in Inbox eintragen`, `Ideen aus Chat in strukturierte Aufgaben überführen`, `Nachsorge-Assistent`
- [ ] (P2) [IDEA] Repo Hygiene Toolkit
  - bündelt: `Dead File Scanner`, `Repo-Aufräumläufe`, `Runner-Archivierung nach Regeln`, `Automatic Report-Ablage`
- [ ] (P3) [PARKED] ShrimpDev Platform / Intelligence Layer
  - bündelt: `ShrimpDev Auto-Medic`, `Runner Sandbox Mode`, `Runner Performance Tracker`, `Smart Runner Suggestions`, `Failure Memory System`, `Local Knowledge System`, `Personal Automation OS`, `Developer Automation Platform`
  - noch zu schärfen: klarer erster Scope statt Plattform-Großbegriff

### Lane E — Clarivoo / Websites / Monetarisierung
- [ ] (P1) [PLANNED] Clarivoo Factory
  - kanonischer Sammelpunkt für produktive Clarivoo-Skalierung
  - bündelt: `Clarivoo Factory`, `Clarivoo Vergleichsseiten-Automat`, `Nischen-Webseiten-Fabrik`, `AI Content Automation Engine`, `Website Content Factory`
  - strategisch wichtig
- [ ] (P2) [IDEA] Clarivoo Vertical Pages
  - bündelt: `Luftentfeuchter`, `Saugroboter`, `Airfryer`, `"Was lohnt sich wirklich?" Vergleichsportal`, `Tool-/Template-Download-Seite`
- [ ] (P2) [IDEA] Knowledge / Problem-Solver Verticals
  - bündelt: `Aquarium-/Shrimp-Wissen`, `Excel-/Office-Tool Hilfeseite`, `Zimmerpflanzen-Problemlöser`, `Arbeitsalltag / Teamlead-Ratgeber`
- [ ] (P2) [IDEA] Runner / Automation Toolkit (Product)
  - bündelt: `Runner/Automation Toolkit`, `Developer Utility Pack`, `Developer Productivity Toolkit`, `Fehlerdiagnose-Toolkit für Tkinter/VBA`
- [ ] (P2) [IDEA] Services / Productization Portfolio
  - bündelt: `ShrimpDev Lite für Einzelentwickler`, `Dokumentationspaket für kleine Firmen`, `Interne Tool-Migration Services`, `Automation Consulting`, `Script Marketplace`, `Developer Productivity Toolkit`
- [ ] (P3) [PARKED] Mobile / Companion App Portfolio
  - bündelt: `Mini-Planer für Schichtlogik`, `Aquarium Care Companion`, `Plant Watch Log`, `Routine Tracker`, `Batch/Script Starter Hub`, `Workday Helper für Teamleiter`
  - bewusste Parkposition: valide Ideen, aber derzeit nicht nah an der aktiven Repo-Pipeline

### Lane F — Excel / B2B / Rescue
- [ ] (P1) [PLANNED] Excel Rescue AI / Makro-Wiederbelebungs-Toolkit
  - bündelt: `Excel Rescue AI`, `Makro-/Excel-Wiederbelebungs-Toolkit`, `Excel-Rettungsservice`, `Legacy-Tool Stabilizer`
  - strategisch wichtig
- [ ] (P2) [IDEA] Dispo / ASM Productization Track
  - bündelt: `Dispo-Tool als B2B-Lösung`, `ASM/Fairness-Reporting`, `Interne Tool-Migration Services`
- [ ] (P2) [IDEA] SOP / Betriebswissen Toolkit
  - bündelt: `Dokumentationspaket für kleine Firmen`, `Interne Prozess-Landkarte für kleine Firmen`, `Betriebswissen-Sammler für kleine Teams`, `SOP-Generator für reale Arbeitsabläufe`

### Bewusst nicht als eigene Tasks aufgenommen
- Wilde, sehr breite Ideen ohne klaren ersten Scope wurden nur dann übernommen, wenn sie in einen bestehenden produktiven Cluster passten.
- Reine App-Ideen ohne direkte Repo-/Lane-Nähe wurden in Sammelcluster verschoben statt einzeln aufgeblasen.

---

## Lane A — Stabilität & Core
<!-- R9316_A_IDEAS_BEGIN -->
### Lane A — Stabilität / Core — ergänzt durch R9316

- [ ] (P1) [CORE] System Health Dashboard — Stabilitätsmetriken aus Logs, Reports und Crash-Signalen.
<!-- R9316_A_IDEAS_END -->
<!-- R3512_LANE_A_P0_START -->
**R3512 NOTE – Lane A P0 Clarification (post-phantom cleanup):**
- Only items that block app start or cause crashes in default flows remain P0.
- Historical/architectural items or feature hardening belong to P1/P2.
- Each remaining P0 must state a *crash/start symptom* and a *clear DoD*.

**Action:** Review the following Lane-A items and downgrade any that do not meet P0 criteria.

<!-- R3512_LANE_A_P0_END -->

<!-- R3511_NOTE_START -->

**R3511 NOTE (verified by R3510 recursive scan):**
- R2374 / R2375 / R2377 / R2378 are referenced historically (docs/pipeline), but no active runner files were found in the repo scan.
- R2379 exists as tools runner files, but other references are largely docs/reports.
- Treat these as ARCH/HISTORICAL unless we explicitly *materialize* missing runners.
- Rule: *Pipeline items with missing runner artifacts must be tagged as Phantom/Archived until materialized.*

<!-- R3511_NOTE_END -->

- [x] (P0) [CORE] (HIGHEST / BLOCKER) R2372 – Architektur: INI Single Writer (Design + API) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L122)

- [x] (DONE) APPLY: module_docking cfg.write(f) -> ini_writer.write() (R3354)

- [x] (DONE) APPLY: Fix: Runner-ID mismatch (py = cmd-1) (R3351)

- [x] (DONE) APPLY: config_loader INI writes -> ini_writer.write() (R3349)

- [x] (DONE) DIAG: INI write offenders scan (R3347) → Report_R3347_20260112_125757.md
- [x] (DONE) Docs: Runner Architecture – Lessons Learned (R3346)
- Pipeline-Markierung via R3348
- gesetzt am 2026-01-12 14:14

- [x] (P0) [CORE] (HIGHEST / BLOCKER) R2376 – Docking über Single Writer (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L141) — DONE (verified 2026-01-12 via R3378/R3379)
- [x] (P0) [CORE] main_gui.py Stabilität: Silent-Exceptions sichtbar gemacht (R3333; DIAG: R3331/R3332)
- [x] (P1) [CORE] INI Redirect Logging Noise gedrosselt (Callsite-Gating) (R3334)

<!-- R3316_PIPELINE_DOCKING_TASKS_INSERT -->
- [x] (P1) [CORE] Docking: Konsolidierung der Undock-Overrides (R3302–R3315) in eine kanonische Implementierung — DONE (verified) (Report_R3397_20260112_224300.md) (Report_R3398_20260112_225641.md)
- [x] (P1) [CORE] Docking: Verify-Runner für Undock/Restore/UI-Integration (inkl. Log-Tab Button-Row)
<!-- /R3316_PIPELINE_DOCKING_TASKS_INSERT -->

**Ziel:** Alle Themen (ShrimpDev/ShrimpHub/Website/Doku/Tooling) gleichmäßig voranbringen — ohne Chaos.  
**Regel:** Start-/Crash-Stabilität schlägt alles.

## Lanes (Themenbahnen)
- Lane A — Stabilität / Crash / Startfähigkeit (P0/P1)
- Lane B — Core Features (P1/P2)
- Lane C — Tooling / Automationen (P1/P2)
- Lane D — Doku / Regeln / Konsistenz (P1/P2)

<!-- R3569_LANE_D_GOV_TASKS_BEGIN -->
### Lane D — Governance-Schärfung (Docs-only)

<!-- PIPELINE_LANE_D_BEGIN -->
- [ ] (P1) Report-Agent: Reports-Auswertung → Todos ableiten → priorisieren → Pipeline-Einsortierung (MVP DIAG, optional APPLY) <!-- TASK_REPORT_AGENTR3755_NACHSORGE_RUNNER_PROTECT --> - Quelle/Referenz: R3755 (Agent-Report), R3753 (Output-Guard), Nachsorge-Regeln (MR-NG*) - MVP (DIAG / read-only):
- [ ] Reports/ scannen (z. B. letzte 30)
- [ ] FAIL/WARN/ExitCodes + Keywords clustern (Dedup)
- [ ] Priorität P0–P2 vergeben
- [ ] Empfehlung: Lane/Phase + nächster Runner-Typ (DIAG/APPLY)
- [ ] Ergebnis als Agent-Report schreiben (kein Auto-Schreiben in PIPELINE)
- Optional (kontrolliert, APPLY):
- [ ] „Übernimm Todo #X“ schreibt genau einen Pipeline-Eintrag (dedupe-sicher, Token Pflicht)
- Nachsorge-Plus: Runner-Schutz und modulare Ablösung
- [ ] Runner, die künftig wieder genutzt werden, müssen protected/whitelisted werden
- [ ] Wenn Funktion ersetzt wird: modularer Ersatz, Alt-Runner erst nach Stabilitätsnachweis aus der kritischen Nutzung nehmen

- [ ] (P1) Governance-Schärfung (R3568/R3569): Pipeline-SSOT, Diagnose-first (Enforcement), Runner Scope-Lock, Definition of Done, Stop-Kriterien
- [ ] MR-Block vorhanden (R3568) ✅
- [ ] Pipeline-Tasks vorhanden (R3569)
- [ ] Architektur-Prinzipien ergänzt (R3569)
- [ ] Report vorhanden (R3568 + R3569)

- [ ] (P2) Public/Private Repo Audit-Rhythmus definieren (z. B. alle 10 Runner oder wöchentlich): „was darf public / was nie“
- [ ] (P2) Decision-/Rejected-Ideas-Log minimal pflegen (1 Satz „warum nicht“ statt Vergessen)
<!-- R3569_LANE_D_GOV_TASKS_END -->

- Lane E — Website / SEO-Netzwerk (P2/P3)

## Turnus
1. **Hard Override:** Wenn es **P0 in Lane A** gibt → **immer zuerst**.
2. Sonst rotieren wir: **A → B → C → D → E → (repeat)**.
3. Pro Session: **1 Anchor-Task** aus der aktuellen Lane (optional Kleinkram max. 20%).

## Arbeitskonvention (kurz)

## Lane F — Excel / DISPO (P0)

- [ ] (P0) DISPO-Tool V1 stabilisieren (produktiver Einsatz)
- Ziel: V1.0 „daily usable“ ohne Workarounds
- stabile Datenstruktur / klare Tabellen
- Vorschlagslogik stabil (Primär/Sekundär) + reproduzierbar
- Tageswechsel sauber (Neuer Tag / Reset)
- Reset-Mechanismus für neue Mitarbeitende
- 1 Haupt-View (Einteilung), Rest in separaten Tabs
- keine #NAME? / Spill-Fehler / „schreibt sonstwo hin“
- reproduzierbare Ergebnisse (gleiches Input → gleiches Output)
- Bedienung im Alltag: „Klick-Workflow“ ohne Basteln

<!-- R9001_DISPO_BLOCK_BEGIN -->
- [ ] (P0) A: Fairness/Snapshot stabilisieren (Ursache final isolieren, kein Trial-&-Error)
- Frage: Warum werden Fairness-Punkte nicht gutgeschrieben, obwohl Snapshot gefüllt ist?
- Output/Check: Fairness-Delta muss deterministisch sein (gleiches Input → gleiches Ergebnis).
- Hinweis-Idee: Wenn Final (Name) gefüllt ist ⇒ MA ist geplant ⇒ 1 Punkt auf MA-ID (nur wenn Regel/Contract das so will).

- [ ] (P1) B: Assign/Override/Final-Flow konsolidieren + Orchestrator „Neue Planung“
- Ziel: 1 Klick-Workflow, klare Ownership, keine Side-Writes in Formelspalten.

- [ ] (P1) C: View/Mail finalisieren
- Umlaute/Encoding sauber
- Tasknamen statt IDs
- Layout final

- [x] (DONE) Intake/Intake.py / Runner-Thema fallen gelassen (Nutzerwunsch)
- Markiert am 2026-02-14 08:08:17
<!-- R9001_DISPO_BLOCK_END -->

## ShrimpDev Core – Diagnose & Stabilität (P1)

- [ ] (P1) DIAG-Standard vereinheitlichen (SOLL/IST, Ursachen, Next Steps, Pfadchecks)
- [ ] (P1) Runner-Preflight zentralisieren (python/venv/git/node/rights/root)
- [ ] (P1) FAIL-Report-Header standardisieren (Fail-Reason, Top-3 Ursachen, Next Runner)
- [ ] (P1) Report-Index (letzte Reports, OK/FAIL, Links)
- [ ] (P1) Last-Known-Good Marker nach grünem Smoke-Test

## Clarivoo – Content & Aktualisierung (P2)

- [ ] (P2) Hybrid-Seitenkonzept: plain + hochwertiger Mehrwert-Content (nicht nur Tabellen)
- [ ] (P2) Update-Routine: regelmäßige Content-Aktualisierung (Fälligkeiten, Sichtbarkeit „lebt“)
- [ ] (P2) Automatisierungskonzept: ShrimpDev-gestützt planen/tracken; später Trigger/Deploy prüfen (Hosting: netcup)

## Codex – Worker-Pilot (P3)

- [ ] (P3) Codex CLI Setup (Installation + local smoke: codex --version)
- [ ] (P3) Pilot: DIAG-only Worker (Workspace-Isolation, Diff/Report, kein Auto-Apply)
- [ ] (P3) Security/Controls: strikt nur im Workspace, Report-Gate, keine direkten Änderungen am Haupttree

- Tasks sind pro Lane gruppiert.
- Jede Änderung an Pipeline: Backup + Report.
<!-- SHRIMPDEV_AUTOGEN:R9049 NACH_SORGE START -->
## Nachsorge (Runner) — R9049

**Zweck:** Konsolidiert SSOT-Doku und Schutz/Integrity-Nacharbeiten nach Fixes.

**SSOT-Pfade (verbindlich):**
- docs/MasterRules.md
- docs/PIPELINE.md
- docs/SHORTCODES.md
- docs/templates/*
- docs/FILE_MAP.md, docs/SYSTEM_MAP.md (falls vorhanden)
- docs/CHANGELOG.md, docs/VERSION.txt

**No-Gos:** keine neuen Features; marker-basiert; Backups + Report.

**Sequenz:** RUN DIAG → RUN FIX → Nachsorge FINAL (dieser Runner).
<!-- SHRIMPDEV_AUTOGEN:R9049 NACH_SORGE END -->

<!-- PIPELINE_V1_END -->

---

## P0 – ui_toolbar.py entschärfen (Modularisierung + Stabilitäts-Guards)

<!-- R9142_CODEX_P0_INSERTED -->
### Codex Integration (Runner/GUI) — Stabilize
- DONE: R9140 Codex im Runner-Kontext ausführbar (rc=0, codex --version ok).
- DONE: R9141 MasterRules ergänzt (Windows CLI & Runner Standards).
- NEXT (P0): GUI-Integration Codex-Buttons über Anchors (kein main_gui Wild-Patching).
- NEXT (P0): Compile-Gate Pflicht bei jedem GUI-Patch (py_compile + Report).

- [ ] (P0) (AFTER DISPO V1.0) FIX: Push + Purge Buttons ohne Funktion (Verdrahtung/Action-Routing defekt)

<!-- R8608 BEGIN -->
### Update: P&P (Push/Purge) — DIAG verifiziert (R8603, 20260216_160709)

- ✅ P6P/P&P Buttons stabil (Push/Purge): Bridge→logic_actions→runner_exec, PP_DIAG entfernt. (Nachsorge: Report_R8651_20260216_233513.md)

**DIAG Ergebnis (R8603):**
- Compile OK: modules/ui_toolbar.py, modules/logic_actions.py, modules/toolbar_runner_exec.py, modules/module_runner_popup.py
- UI-Wiring ist vorhanden:
- Push ruft action_autopush_both (Autopush Both) auf
- Purge ruft action_purge_one auf
- Purge ist zur Laufzeit gated (bewusst): Button-Enablement hängt u. a. an tools/R2218.cmd|py und Busy-Guard / canonical keep-file checks.

**Schlussfolgerung (präzisiert):**
- Das Problem ist nicht primär „Verdrahtung fehlt“, sondern wahrscheinlicher:
- Runner-Presence / Pfad / Repo-Root / keep-file / Busy-Guard blockiert
- Exceptions werden best-effort geloggt, aber UX kann „wirkt tot“ aussehen

**Next (MR: Diagnose zuerst, dann minimal APPLY):**
- R8609: Trace-DIAG „Click → Dispatch → Runner resolve → subprocess → rc → Popup“
- Danach erst minimaler APPLY (nur der erste belegte Blocker, keine Rewrites)
<!-- R8608 END -->

- Symptom: Buttons *Push* und *Purge* reagieren nicht / keine Aktion.
- Hypothese: UI-Action Verdrahtung/Dispatch/Registry-Map zeigt ins Leere.
- DoD: Push & Purge lösen zuverlässig die korrekten Runner/Actions aus (inkl. Report-Popup gemäß Standard).

**Priorität:** P0 / superurgent  
**Problem:** `modules/ui_toolbar.py` ist import-kritisch und fragil (Indent/Scope/NameError). Kleine Änderungen können den App-Start crashen.  
**Ziel:** Startstabilität absichern + Risiko modular reduzieren, ohne Vollrewrite.

**Definition of Done**
- ui_toolbar.py wird deutlich dünner (Orchestrator)
- Repo/Registry/Action-Routing in eigene Module ausgelagert (testbar)
- Push/Purge bleiben funktional (keine Verluste)
- Smoke-Test/Import-Check Runner vorhanden

**Umsetzungsplan (MR: mehrere kleine Runner)**
<!-- R3382_UI_TOOLBAR_SUBTASKS_BEGIN -->

**Unterpunkte (geordnet, verifizierbar – kein Chaos)**
- P0.A Runner-Execution isolieren: Threading/Subprocess aus ui_toolbar.py hinter eine klare API; UI ruft nur noch Orchestrator auf. — DONE (verified) (Report_R3402_20260112_233849.md) (Report_R3403_20260112_234334.md)
- DoD: keine Runner-Startlogik direkt im UI; 1 definierte run_runner(...)-Entry; UI bleibt responsiv.
- P0.B Smoke/Crash-Schutz: Read-only Smoke-Runner vor APPLY-Stufen (Import + minimaler Toolbar-Aufbau wenn möglich). — DONE (verified via R3390 on 2026-01-12) (Verification: Report_R3390_20260112_210110.md)
- P0.C Central Dispatch Entry-Point: toolbar actions laufen über _dispatch_action(...) (minimaler Router-Einstieg, keine Behavior-Änderung). (Verification: Report_R3409_20260113_095743.md) — DONE (verified 2026-01-13)
- DoD: Smoke grün nach jedem APPLY; Report + Exitcodes.
- P1.A Popup/Report-Handling konsolidieren: ein kanonischer Pfad für Report-Anzeige (Push/Purge gemäß Standard). — DONE (verified) (Report_R3393_20260112_221547.md) (Report_R3394_20260112_222242.md)
- DoD: keine doppelten Popup-Overlays; konsistentes Verhalten.
- P1.B Import-Hygiene/Verantwortlichkeiten: redundante/verteile Imports reduzieren (nur minimal, ohne Semantikänderung).
- DoD: Top-level Imports sauber; keine überraschenden Side-Effects.
- P2 Nested-def Reduktion (nur wo nötig): kritische nested Worker/Callbacks testbarer machen (ohne Vollrewrite).
- DoD: weniger Tiefe im Runner-Cluster; Verhalten unverändert.

<!-- R3382_UI_TOOLBAR_SUBTASKS_END -->

1. **READ-ONLY Toolbar Map Report**
- listet Funktionen, nested helper, after()-ticks, referenced actions, risk lines
2. **Extract repo/registry helpers** → `modules/toolbar_helpers_repo.py`
- read_registry_path(), is_git_repo(), repo_pushable()
3. **Extract action router** → `modules/toolbar_action_router.py`
- call_action(app, name) robust + logging
4. **Extract Push/Purge section** → `modules/toolbar_sections/section_push_purge.py`
- Builder-Funktion, reduziert nested closures im Hauptfile
5. **ui_toolbar.py cleanup**
- nur Orchestrator-Aufrufe, keine Logikvermischung
6. **Smoke-Test Runner**
- python -c "import modules.ui_toolbar" (und optional GUI-smoke, wenn vorhanden)

**Risiko/Schutz**
- Jede Stufe: Backup + Report
- Keine Voll-Rewrites, keine radikalen Strukturänderungen
- Wenn Fix nicht direkt verifiziert: Diagnose zuerst (MR)

<!-- SHRIMPDEV_POLICY_REPO_LAYERS -->

### UI / Runner-Popup – Report-Link + Copy-to-Clipboard (NEW)

- Goal: Wenn Runner einen Report erzeugen, soll der Report im Runner-Popup direkt nutzbar sein.
- Why: Spart Zeit, verhindert „Report suchen“ und erleichtert Debug/Sharing.

**Acceptance Criteria**
- Parser erkennt Report-Pfade in Runner-Output, z. B. Report: / OK: Report: (absolute Pfade).
- Runner-Popup zeigt:
- Open Report (klickbarer Link, öffnet Datei via Default-App)
- Copy Report (kopiert den vollständigen Report-Text in die Zwischenablage)
- Wenn kein Report gefunden: UI-Elemente deaktiviert/ausgeblendet.
- Robust: keine Crashes bei leerem Output, Sonderzeichen, CRLF/LF.

**Implementation Notes**
- In modules/module_runner_popup.py:
- stdout/stderr nach bekannten Mustern scannen (Regex).
- Pfad normalisieren (Windows).
- Open: os.startfile(path) (Windows) / fallback.
- Copy: Tk clipboard (root.clipboard_clear(); root.clipboard_append(path)).

**Priority**
- P2 (UX/Workflow), nach Stabilität/CI-Blockern.

## Policy: Repo-Layers (Production vs Archive) & CI Scope

**New insight (R2652/R2653):** Dieses Repo enthält bewusst mehrere Schichten.

- Production layer (must be syntactically clean): modules/, main_gui.py (und nur ausdrücklich freigegebene Prod-Tools)
- Archive/Legacy layer (may be broken): _OldStuff/, _Trash/, tools/Archiv/, historische Runner/Friedhof

**Rule:** CI-/Syntax-Gates (compileall, Ruff E9) dürfen **nur** auf dem Production-Layer laufen.

**Reason:** Archive/Legacy enthält absichtlich kaputte/inkompatible Dateien (Syntax/Encoding/Indent), die nicht als Blocker gelten.

**Implementation standard:**

```text
python -m compileall -q main_gui.py modules
ruff check modules main_gui.py --select E9
```

**Exclude standard (lint/ci):** `_OldStuff/**`, `_Trash/**`, `tools/Archiv/**`, `modules/snippets/**`, Outputs (`Reports/**`, `_Archiv/**`, `_Exports/**`).

<!-- SHRIMPDEV_POLICY_CI_WORKFLOW_YAML -->
## Policy: CI-Workflow zuerst auf YAML-Validität prüfen

**Rule:** Wenn GitHub Actions **„Invalid workflow file“** oder **„You have an error in your yaml syntax“** meldet, wird **immer zuerst** die YAML-Struktur geprüft (Indentation/Mapping), bevor Tooling (ruff/compileall/etc.) debuggt wird.

**Reason:** Bei YAML-Parsefehlern werden **keine Steps** ausgeführt – Tool-Logs sind dann irrelevant.

**Quick checklist:**
- jobs: → darunter müssen Job-IDs eingerückt sein (z. B. lint:)
- runs-on: / steps: sind unter dem Job eingerückt
- Step-Listenpunkte beginnen mit - und sind korrekt eingerückt

<!-- SHRIMPDEV_PIPELINE_TASKS_BLOCK -->
## Pipeline Tasks

<!-- SHRIMPDEV_PIPELINE_IMPORTED_TASKS_START -->
### Imported Tasks (auto)

> Auto-importiert (Extended Scan: inkl. Markdown TODOs + Legacy). Bitte später konsolidieren.

- [x] (P0) [CORE] (HIGHEST / BLOCKER) Central Runner-Executor API (App ↔ logic_actions) — UI-Actions dürfen keine Runner-IDs kennen; 1 kanonischer Executor + Smoke-Test- [ ] (P0) [CORE] NOTE: that CI blockers were fixed via R2576. _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2576.py:L103)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L18)- [ ] (P0) (HIGHEST / BLOCKER) R2373 – Implementierung: zentraler INI-Writer (Merge + atomic) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/INI_WriteMap.md:L14478)- [ ] (P0) (HIGHEST / BLOCKER) R2371 – INI-WriteMap (READ-ONLY Diagnose) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L117)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) R2374 – config_manager Save konsolidieren (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L133)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) R2375 – Shims: config_loader.py / config_mgr.py (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L137)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) R2377 – Monkeypatch/Altlogik Quarantäne (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L148)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) R2378 – Restore Reihenfolge finalisieren (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L152)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) R2379 – Regression-Testplan (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L156)
- [ ] (P1) [CORE] Prüfen/Plan: modules/ui_toolbar.py modularisieren (Import-kritisch) — Ziel: kleine Module (builders/actions/hooks), weniger Seiteneffekte, bessere Testbarkeit
- [ ] (P1) [PROD] TODO: \n- File: {pipeline}\n- Backup: {backup}\n", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Archiv/Runner_Staging_2025-12-25/R2598.py:L59)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L24)
- [ ] (P1) [CORE] NOTE: Did not match expected 'run: uvx ruff ...' lines. Please verify ci.yml manually.", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2580.py:L109)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L25)
- [ ] (P1) [PROD] TODO: ][HIGH] Runner-Cleanup – Archivierung unbenutzter Runner _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Pipeline/Pipeline_R2016_RunnerCleanup_20251208_154653.txt:L1)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L27)
- [ ] (P1) [CORE] (P1) ... (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/ARCHITECTURE.md:L176)
- [ ] (P1) [CORE] TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh). (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Pipeline_Notes.md:L29)
- [ ] (P1) [CORE] TODO: (Pipeline), sondern bekommen einen eigenen Tab. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19929)
- [x] (P1) [CORE] TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh).\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19950)- [ ] (P1) [CORE] TODO: ) Pipeline-Eintrag: Tracebacks wieder ins Log (HIGH) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19967)
- [ ] (P1) [CORE] TODO: in der Pipeline-Datei. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L7958)
- [ ] (P1) [CORE] TODO: in docs/Master/Pipeline_Notes.md eintragen: (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L8944)
- [ ] (P1) [CORE] TODO: (Pipeline), sondern bekommen einen eigenen Tab. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2143.py:L2)
- [ ] (P1) [CORE] TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh).\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2143.py:L250)
- [ ] (P1) [CORE] TODO: ) Pipeline-Eintrag: Tracebacks wieder ins Log (HIGH) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2144.py:L9)
- [ ] (P1) [CORE] NOTE: for Docking incident and doc links (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2397.py:L2)
- [ ] (P1) [PROD] docs/Architecture_ProjectTab.md – Datenquellen/Contract (nur lesen: PIPELINE, Reports, SmokeTest) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2521.py:L76)
- [ ] (P2) [PROD] Incremental Refactor Plan: Schrittfolge ohne Vollrewrite (1 Modul pro Runner, jeweils compile+smoke) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L94)
- [ ] (P3) [PROD] TODO: (reports/ordner konsolidieren) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2596_20251225_111324.md:L4)
- [ ] (P3) [PROD] TODO: : False (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2655_20251225_200722.md:L84)
- [ ] (P3) [PROD] TODO: (reports/ordner konsolidieren)\n" _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Archiv/Runner_Staging_2025-12-25/R2596.py:L93)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L28)
- [x] (P3) [PROD] NOTE: btn_apply pack line not found (maybe already adjusted).") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2448.py:L138)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L31) (auto-closed R2854: obsolete)
- [x] (P3) [PROD] NOTE: btn_scan pack line not found (maybe already adjusted).") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2448.py:L148)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L32) (auto-closed R2854: obsolete)
- [x] (P3) [PROD] NOTE: {'patched' if c4 else 'no-op'}") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2576.py:L184)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L35) (auto-closed R2854: obsolete)
- [x] (P3) [PROD] NOTE: {'patched' if c3 else 'no-op'}") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2577.py:L174)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L36) (auto-closed R2854: obsolete)
- [ ] (P3) [PROD] TODO: ", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2655.py:L129)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L40)
- [ ] (P3) [PROD] TODO: /FIXME in code) _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.cmd:L5)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L41)
- [ ] (P3) [STRAT] TODO: markers _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.py:L107)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L42)
- [ ] (P3) [PROD] TODO: |FIXME|HACK|NOTE)\b[:]?\s*(?P<text>.*)$', re.IGNORECASE) _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.py:L26)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L43)
- [ ] (P3) [STRAT] TODO: /FIXME/HACK/NOTE markers in *.py/*.cmd/*.bat/*.ps1/*.yml/*.toml _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.py:L8)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L44)
- [ ] (P3) [STRAT] TODO: /FIXME Marker). Bitte bei Bedarf konsolidieren.\n\n") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2659.py:L108)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L45)
- [ ] (P3) [CORE] TODO: Flag/Policy). (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Architecture_DnD_FileOut.md:L21)
- [ ] (P3) [CORE] TODO: implement logic here (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L15280)
- [ ] (P3) [CORE] TODO: list: add a high-priority item about tracebacks in log. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19969)
- [ ] (P3) [CORE] TODO: (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L7989)
- [ ] (P3) [CORE] TODO: bereits vorhanden – uebersprungen.\n") (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L8918)
- [ ] (P3) [CORE] TODO: hinzugefuegt.\n") (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L8921)
- [x] (P3) [PROD] NOTE: Root tools_keep.txt exists but is obsolete. Canonical file is registry/tools_keep.txt (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2416_RegistryAndDocsFix_20251221_105138.md:L9) (auto-closed R2854: obsolete)
- [ ] (P3) [CORE] HACK: für on_sort (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R1301_IntakeV1_Install.py:L353)
- [ ] (P3) [CORE] TODO: actual UI factory if separate exists\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R1305_IntakeHardFix.py:L70)
- [ ] (P3) [CORE] TODO: list: add a high-priority item about tracebacks in log. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2144.py:L118)
- [ ] (P3) [CORE] (TOP/HIGH) Phase 2: Restore-Orchestrierung (pro Fenster-Key) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2375.py:L66)
- [ ] (P3) [CORE] (HIGH) Migration: Remaining Writers -> SingleWriter (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2375.py:L79)
- [ ] (P3) [PROD] (MED) Defactoring / Archivierung (nach erfolgreicher Umstellung) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2375.py:L83)
- [x] (P3) [CORE] NOTE: Root tools_keep.txt exists but is obsolete. " (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2416.py:L125) (auto-closed R2854: obsolete)
- [ ] (P3) [CORE] TODO: (optional): hier später Reflow/Anordnung implementieren. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_1171m_IntakeToolbarReflowFix.py:L47)
- [ ] (P3) [CORE] TODO: implement logic here (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_943_NewRunner.py:L49)
- [ ] (P3) [CORE] Define Actions Registry (Docs): Liste der erlaubten Actions + Labels (Copy Path/File/Text, Open, Folder, Restore gated) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L90)
- [ ] (P3) [CORE] Define Gating Rules (Docs): wann ist Restore sichtbar? wann ist File-Copy erlaubt? (Backup/Archiv-Only, Busy-State) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L91)
- [ ] (P3) [CORE] Central Helpers Plan (Docs): gemeinsame Helper-Funktionen (clipboard, file-copy-paste, restore-safe) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L92)
- [ ] (P3) [PROD] Per-Tab Audit: Artefakte (Tree/Preview), Intake, Runner Products etc. – Abweichungen dokumentieren (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L93)
- [ ] (P3) [CORE] Regression Checklist: Rechtsklick links/rechts, Selection behavior, busy-state, messageboxes (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L95)
- [ ] (P3) [CORE] docs/Architecture_ProjectTab.md – Definition + Non-Goals (keine Buttons, keine neue Logik) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2521.py:L75)
- [ ] (P3) [CORE] docs/Architecture_ProjectTab.md – Minimaler Anzeige-Contract/Wireframe (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2521.py:L77)
- [ ] (P3) [STRAT] TODO: markers (now also in .md) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2661.py:L218)
- [ ] (P3) [CORE] TODO: /FIXME/HACK/NOTE lines ALSO in Markdown (.md) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2661.py:L9)

<!-- SHRIMPDEV_PIPELINE_IMPORTED_TASKS_END -->

> **Hinweis:** Der Pipeline-Tab in ShrimpDev zeigt nur **Tasks** (z. B. `- [ ] …`).
> Policies/Regeln bleiben weiter oben im Dokument, aber ohne Tasks bleibt die GUI-Liste leer.

- [ ] (P1) [CORE] CI: Reports wieder als GitHub Actions Artefakte anzeigen (Runner R2656)
- [ ] (P1) [PROD] ShrimpDev: Artefakte-Tab prüfen/reaktivieren, falls Anzeige fehlt
- [ ] (P2) [CORE] LearningJournal Auto-Write: Diagnose + Guard (nach CI stabil)
- [x] (P0) [CORE] CI Syntax-Gate scoped + YAML valid (R2653/R2654)

## Autopush (Repo-only)
- Canonical autopush backend (OneDrive repo-only): tools/R2691 (Private), tools/R2692 (Public), tools/R2693 (Both).
- Deprecated: R2692/R2691 legacy autopush runners (workspace-bound). Do not wire GUI buttons to them.
- Autopush reports are generated locally under Reports/ and are not versioned in git.
- [P1] Autopush repo-only finalized: GUI uses R2691/R2692/R2693; legacy R2692/R2691 deprecated; gitignore ignores only Report_R269{1..3}_*.md.

---

## P3-Workspace-Deaktivieren-RepoRoots-Explizit

**Priority:** P3  
**Status:** Planned  
**Scope:** ShrimpDev (Private/Public Root Handling), UI Push Buttons, CI Hygiene

### Goal
Workspace ist ein Alt-Relikt und soll **deaktiviert** bleiben. Stattdessen werden Repo-Roots **explizit** geführt:
- Private Repo Root: per UI „…“-Button auswählbar, in INI gespeichert
- Public Root: automatisch ableitbar (z. B. ShrimpDev_REPO → ShrimpDev_PUBLIC_EXPORT), optional autocreate des Ordners
- Keine Heuristik über cwd, keine „guess roots“

### Tasks
- [ ] Workspace als Root-Quelle deaktivieren (UI/Logic dürfen workspace_root nicht mehr als Default verwenden)
- [ ] INI: [Repo] private_root, [Repo] public_root, [Repo] public_autocreate
- [ ] UI: „…“ Button zum Setzen von private_root
- [ ] Public Root ableiten; Ordner bei Bedarf anlegen; kein erzwungenes git init
- [ ] Audit: alle Code-Stellen, die workspace_* referenzieren → entfernen/migrieren
- [ ] Dokumentation: Architektur + MasterRules + Pipeline referenzieren

### Rationale
Verhindert Root-Fehlermatches (OneDrive/Startpfad), macht Push-Buttons deterministisch und reduziert CI/Repo-Chaos.

---

## R2854 Summary (auto)
- Date: 2025-12-28 23:08:17
- P3 items scanned: 69
- P3 NOTE converted to non-tasks: 31
- P3 OBSOLETE auto-closed: 6

<!-- SHRIMPDEV_PIPELINE_FSTRING_GUARD -->
(P1) TODO: (CI/Guard) Introduce/keep Lint-Guard for f-string unknown identifiers (Runner R2867) and run it before Push.
(P1) TODO: (UI) Add a toolbar button “Lint Guard (R2867)” near Push/Purge diagnostics; on click run R2867 and show latest report via popup helper.
(P1) TODO: (Docs) Canonical paths reminder: MasterRules live in docs/Master/*.md; pipeline is docs/PIPELINE.md. All doc-updates must target canonical files (no root MasterRules.md).

## Policy Updates

<!-- R3563_FOCUS_POLICY_BEGIN -->
### Fokus-Leitplanke: Basis vor Produkt (Thread-Entscheidung)

- Priorität: ShrimpDev-Stabilität + Reproduzierbarkeit + Doku gehen vor Monetarisierung.
- Regel: Solange relevante P0/P1 (Lane A/B) offen sind, werden keine neuen Produkte/Repros gestartet.
- Ideen dürfen existieren, aber nur als Doku/Parking (keine Umsetzung außerhalb der Pipeline).
- Verankerung: siehe MR-STRAT-FOCUS-01 in docs/MasterRules.md.
<!-- R3563_FOCUS_POLICY_END -->

### Public Repo Contract (export policy)

- The public repo is not a mirror. It is a curated export.
- Export must be allowlist-based (explicit include patterns).
- Forbidden in public: backups, reports, debug captures, registry/state, internal pipeline, internal master rules, internal journals.
- Export must write/update docs/Public_Contract.md in the public repo.
- Any policy breach triggers a repair runner that sanitizes the public repo.

### P2 – Log-Tab: Suche im Log
- Feature: Suchfeld im Log-Tab, das das Log (Textwidget) live/auf Enter durchsucht.
- UX: Treffer markieren + Next/Prev (F3 / Shift+F3), optional Case-Sensitive Toggle.
- Tech: keine Blockade im UI-Thread bei sehr großem Log (chunked search / after()).

### P2 – UI: Searchfield Clear-Button (✕)
- Feature: In Suchfeldern rechtsbündig ein ✕ zum Clear/Stop.
- UX: ✕ nur sichtbar wenn Text ≠ leer; Klick leert Feld + setzt Ergebnis/Filter zurück; Fokus bleibt im Feld.
- Shortcuts: Esc triggert denselben Clear/Stop; optional Tooltip “Clear”.
- Scope: Log-Tab (Suche), Pipeline-Tab, weitere Filterfelder nach Bedarf.

### P2 – LearningEngine Phase D: Runner-Vorschläge aus LearningJournal (read-only)
- Ziel: Aus LJ/Logs/Reports Vorschläge ableiten (Cluster/Häufigkeit/Impact), ohne Auto-Fix.
- Output: Vorschlagsliste als Report/JSON (z. B. Reports/LearningEngine/Suggestions_*.json) + kurzer Markdown-Report.
- Verwandtschaft: Agent-Tab konsumiert diese Vorschläge (anzeigen, filtern, erklären) und führt Runner nur opt-in aus.
- Sicherheit: Allowlist + Dry-Run/Preview; niemals destructive Runner ohne explizite Bestätigung.

### P2 – Agent-Tab: empfohlene Runner automatisch ausführen (prüfen)
- Idee: Agent-Tab, der auf Basis von Zustand/Logs/Reports Runner vorschlägt.
- Option: *Auto-Execute* nur opt-in.
- Sicherheit: Allowlist erlaubter Runner + Dry-Run/Preview + Abbruch/Undo.
- Regeln: niemals destructive Runner ohne explizite Bestätigung; keine Background-Exec.

---
### Inbox (auto-added 2026-01-04 17:53)
- Log-Tab Suche: Suchfeld im Log-Tab, das das Log (Text) durchsucht.
- Search-Clear-X: In Suchfeldern rechtsbündig ein X zum Beenden/Leeren der Suche.
- Agent-Tab: Empfohlene Runner automatisch vorschlagen und optional (bewusst) ausführen lassen; Sinn/Nutzen prüfen.

## Resolved: Docking Double Tabs
_added 2026-01-08 12:26 via R3147_

- Docking incident resolved (legacy INI state).
- No further action required.
- Area marked as stable.

## P1 – [STRAT] Website / SEO Portfolio

- [ ] (P1) [STRAT] Website-Portfolio: Scope definieren (viele kleine Sites, kein Monolith)
- [ ] (P1) [STRAT] Website-Portfolio: Domain-Strategie festlegen (1 Domain pro Nische)
- [ ] (P1) [STRAT] Website-Portfolio: Erfolgskriterien Phase 1 definieren (Indexierung/Impressions)
- [ ] (P1) [STRAT] Website: Ideenliste mit 20–30 konkreten Produkt-/Problem-Nischen erstellen
- [ ] (P1) [STRAT] Website: Suchlücken-Check (Suchintention + Konkurrenz grob bewerten)
- [ ] (P1) [STRAT] Website: Priorisierungsmatrix definieren (Volumen × Konkurrenz × Monetarisierung)
- [ ] (P1) [STRAT] Website: 1 MVP-Nische final auswählen und begründen

## P2 – [STRAT] Website MVP

- [ ] (P2) [STRAT] Website-MVP: Tech-Setup festlegen (Static/CMS/Hybrid – bewusst simpel)
- [ ] (P2) [STRAT] Website-MVP: Minimale Seitenstruktur definieren (Start + 1–3 Kernseiten)
- [ ] (P2) [STRAT] Website-MVP: SEO-Basics als Checkliste dokumentieren (URLs, H1/H2, interne Links)

## P3 – [STRAT] Website Beobachtung

- [ ] (P3) [STRAT] Website-MVP: Indexierung & Impressions beobachten (Search Console)
- [ ] (P3) [STRAT] Website-MVP: Entscheidung dokumentieren (skalieren oder verwerfen)

<!-- PIPELINE_LANE_D_END -->
## Lane E — Website / SEO-Netzwerk

### P3 — Neue Ideen (Auto-Intake 2026-02-26)

- [ ] (P3) [STRAT] DealRadar — echte Deals mit Preisverlauf + Affiliate
- [ ] (P3) [STRAT] FoodOptimizer — Zutaten → Rezept (Content + Affiliate)
- [ ] (P3) [STRAT] Was lohnt sich heute — Mikro-Entscheidungs-App (lokal + Affiliate)
- [ ] (P3) [STRAT] QuickSite Builder — 1-Klick Affiliate Seiten (Langfrist-Plattform)
- [ ] (P3) [STRAT] RealityCheck — ehrliche Zielbewertung (viral Potential)
- [ ] (P3) [STRAT] KidSignal — Kinderverhalten verstehen (Premium Content)

### P3 — Tools / System Ideen (Parken, kein Build)

- [ ] (P3) [CORE] JobHelper — Excel Automation Tools (Monetarisierung schnell möglich)
- [ ] (P3) [CORE] Digital Declutter — File Cleanup Tool (ShrimpDev Integration möglich)
- [ ] (P3) [CORE] AutoFix AI — Diagnose Tool (skalierbar, später)
- [ ] (P3) [CORE] SecondBrain Lite — Minimal Tracking (LJ Integration möglich)

 (P2/P3)

**Lane-E Contract (Isolation / Artefakte):**
- Isolation: keine Abhängigkeit zu ShrimpDev-Core-State (kein Zugriff auf ShrimpDev.ini, Docking/UI-State, Runner-Registry).
- Erlaubt: gemeinsame Tooling-Runner (Scanner/Generator/Reports) ohne Shared State.
- Artefakte: jede Site lebt unter docs/websites/<site>/... (Decision, MVP, KPIs, Kill/Scale).
- Kill/Scale Kriterien: müssen pro Site schriftlich definiert sein (kein "wird schon").

**Ziel:** Systematisches Portfolio aus Nischenwebsites (SEO-getrieben), monetarisierbar via Affiliate/Ads/Lead.  
**Strategie:** Weg von gesättigten Märkten (z. B. Sneaker) → hin zu klaren Nischen mit echter Suchintention.  
**Prinzip:** Produkte/Probleme statt breite Kategorien; Portfolio-Denken (viele kleine Sites).

### P2 — Setup & Entscheidungsgrundlagen
- [ ] (P2) WE-01: Marken-/Domain-Strategie festlegen (eine Marke vs. viele; Namenssystem)
- [ ] (P2) WE-02: Technik-Stack festlegen (Static/Hybrid/CMS; Generierungs-Workflow)
- [ ] (P2) WE-03: Nischen-Funnel definieren (Idee → Validierung → Content-Cluster → Launch)
- [ ] (P2) WE-04: “Suchlücken”-Validierungscheckliste (Suchintention, Konkurrenz, Monetarisierung, Aufwand)

### P2 — Erste Umsetzung (minimal, realistisch)
- [ ] (P2) WE-10: 10 Nischenideen sammeln (kurz, messbar)
- [ ] (P2) WE-11: Top 3 Nischen validieren (SERP-Check, Konkurrenz grob, Monetarisierungsweg)
- [ ] (P2) WE-12: Erste Site auswählen + Scope 1 (Start: 1 Thema, 1 Struktur)
- [ ] (P2) WE-13: Content-Cluster Plan (Pillar + 10 Supporting Posts)
- [ ] (P2) WE-14: Produktions-Template für Inhalte (vergleichbar/entscheidungshilfe-orientiert)

### P3 — Skalierung (später)
- [ ] (P3) WE-20: Multi-Site-Orchestrierung (Vorlagen, Deployment, Tracking)
- [ ] (P3) WE-21: KPI-Tracking (Impressions/Clicks/CTR/Revenue; wöchentliche Review)

---

## BUG: Docking state not persisted -> undocked tabs not restored

### Symptom
- ShrimpDev.ini [Docking] bleibt unverändert trotz undocked Tabs / App close.
- Nach Neustart werden undocked Tabs nicht wiederhergestellt.

### Root Cause (IST)
- modules/module_docking.py: DockManager.persist_all() führt keinen finalen Write/Commit aus (Legacy/Fragment; kein zuverlässiger Save).
- _persist_one() enthält try/except-Leichen; Writer-Pfad nicht robust/diagnostizierbar.

### Plan
1) Architektur & Single-Writer verbindlich dokumentieren: `docs/Architecture/Current/Docking_Persist_Current.md`
2) Code fix: `persist_all()` + `_persist_one()` auf Single-Writer konsolidieren, minimalen Diagnosepfad ergänzen
3) Regression-Test: undock->close main->verify INI changed->restart->tabs restored

## Abgeschlossene Themen

### Docking / INI / Persistenz
- Abschluss: 2026-01-11
- Begründung:
- Canonical Docking-Core (_r3321_) aktiv
- Single Writer etabliert
- Diagnose (R3327) ergab: kein gefahrlos löschbarer Code
- Weiterer Abbau = eigenes Refactoring-Projekt
- Letzte Runner: R3321–R3327, R3329

<!-- R3416 -->
### P1 · Docking

Status: DONE (core verified)

Der Docking-Core (Undock, Persist, Restore) ist stabilisiert und
durch Verify-Runner abgesichert.

Verifiziert:
- Undock / Redock: OK
- Persist (INI): OK
- Restore (Startup): OK
- Verify-Runner ohne Crash

#### P1.DOCKING.LOGTAB.BUTTON_ROW_DETECTION
Status: OPEN (non-blocking)

Der Finder `_r3315_find_log_button_row(...)` liefert aktuell None.
Dies erzeugt eine WARN-Meldung im Verify, jedoch keinen funktionalen Fehler.

Ursachenannahmen:
- Widget-Hierarchie
- ttk.Button vs. tk.Button
- abweichender Parent-Frame

Vorgehen:
- DIAG (read-only): Widget-Tree-Dump des Log-Tabs
- Danach: minimaler Finder-Fix

<!-- R3431 -->
### P1 · Docking – Verify FINAL

Status: VERIFIED (final)

Nach Abschluss der Fixes (Legacy-Aliases + Compile-Stabilität) läuft der
Docking-Verify Runner stabil und grün.

- Verify: R3413 Exit=0
- Referenz-Report: Reports/Report_R3413_20260113_160946.md

Hinweis:
Ältere Reports können noch historische FAILs enthalten (z. B. _r2339_ini_path),
sind aber durch den finalen Verify-Lauf überholt.

<!-- R3432 -->
### P1 · Docking (Parent)

Status: DONE (final, verified)

Alle Subtasks abgeschlossen:
- Verify FINAL dokumentiert (R3431)
- Verify-Lauf grün: R3413 (Exit 0)

Damit ist der gesamte P1-Docking-Komplex formal abgeschlossen.
### Lane A / Stability
- [ ] INI redirects -> trend to zero (canonical path: registry/ShrimpDev.ini, remove hardcoded root INI reads/writes)

<!-- R3518_LANE_B_START -->

## Lane B

- Lane B – DONE (Nachsorge & Hardening: R3770, R3772, R3773, R3774, R3775) — Hardening / Guardrails (post-P&P, post-R3510..R3517)

### P1 — Housekeeping-Konzept (Auto-Purge über Canonical Executor)
<!-- PURGE_ARCH_LINK:CANONICAL -->
- ARCH: Purge/Housekeeping Soll-Definition: docs/ARCH_Purge.md

- Ziel: Automatisches Housekeeping, insbesondere Purge wieder vollautomatisch (kein manueller R3106-Run).
- Prinzip: UI delegiert ausschließlich an modules/toolbar_runner_exec.py (Single Source of Truth).
- Safety: Guards/Confirm/Logging/Report-Popup (MR-konform, diagnose-first).
- Aktion: B2.1 Purge reaktivieren → Executor → R3106 (oder definierter Nachfolger).
- Public GitHub Referenz: https://github.com/Domtexe/ShrimpDev-Public

### B1 — Canonical Runner Executor API (Single Source of Truth)
- [ ] Define one canonical entrypoint (e.g. runner_exec.run_by_id(app, "R####") or app.run_runner_by_id("R####"))
- [ ] Replace any ad-hoc subprocess/runner wiring in UI code to call the executor only
- [ ] Executor responsibilities:
- [ ] validate runner id format
- [ ] resolve cmd path deterministically
- [ ] run in a robust way (cwd/root consistent)
- [ ] log report path and exit code (no Tk callback explosions)
- [ ] Push uses executor, Purge uses executor
- [ ] No UI module calls subprocess directly
- [ ] One place to change behavior (Single Source of Truth)

### B2 — ui_toolbar.py Modularisierung (UI-only)
- [ ] ui_toolbar becomes UI-only:
- [ ] no INI writes
- [ ] no runner wiring logic beyond calling logic_actions/executor
- [ ] no duplicate button builders
- [ ] Extract pure helper pieces if needed (icons/layout/widgets) into small modules
- [ ] One Push button + one Purge button in code (no duplicates)
- [ ] Buttons call logic_actions → executor
- [ ] py_compile green

### B3 — Redirect/Config Hygiene (Signal stays meaningful)
- [x] Rotate/truncate INI redirect log (R3517) so warnings represent real deltas
- [ ] Add a short “when this warning appears” troubleshooting snippet (docs-only)
- [ ] Warning indicates NEW redirects, not historical noise

### B4 — MR Guardrails (anti-kaskade)
- [ ] Explicitly enforce: DIAG → one APPLY → stop; no “runner fixes runner fixes runner”
- [ ] Phantom runner references: must be tagged/archived until materialized (already started)
- [ ] Reduced repair cascades; fixes are measured & bounded

<!-- R3518_LANE_B_END -->

<!-- R3541 BEGIN: Housekeeping Follow-ups -->
## Lane B – Hardening: Housekeeping (Follow-ups)

**Done (Housekeeping Baseline):**
- Purge/Housekeeping ist produktiv: räumt real auf (Archiv statt Delete), Relevanz-Policy aktiv (tools/ zählt nicht als runtime).

**Next Tasks (priorisiert):**
1) **Allowlist standardisieren & aktivieren**  
   Ziel: explizite Pinning-Möglichkeit für kritische Runner (Override unabhängig von Scan/Policy).

2) **Auto-Purge Strategy definieren**  
   Optionen: manuell (Button), zyklisch (z. B. wöchentlich), event-basiert (nach X Runner / vor Push).  
   Entscheidung + Doku + minimaler Implementationspfad.

3) **Noise-Source Hygiene**  
   `debug_output.txt` & ähnliche Artefakte: dauerhaft excluded/abtrennen, damit Diagnosen nicht „Referenzen“ aufblasen.

**Hinweis (Prozessregel):**
- Pipeline-Review ist verpflichtend, aber nicht chaotisch: Prioritäten werden angepasst, wenn Brisanz steigt/fällt.

<!-- R3541 END -->

---

## Lane E — Websites / SEO / Monetarisierung (Ideen-Dump)
**Hinweis:** Konsolidiert nach `## Lane E — Websites / SEO / Monetarisierung (konsolidiert)` durch R3555 (2026-01-17 23:39).
<!-- R9316_E_IDEAS_BEGIN -->
### Lane E — Websites / Monetarisierung — ergänzt durch R9316

- [ ] (P2) [STRAT] Review Analyzer — Vor- und Nachteile aus Bewertungen konsolidieren.
- [ ] (P3) [STRAT] Evergreen Content Scanner — Veraltete Content-Seiten identifizieren.
<!-- R9316_E_IDEAS_END -->
- Dump archiviert/ersetzt, um Dubletten zu vermeiden.

## Lane E — Websites / SEO / Monetarisierung (konsolidiert)

**Quelle:** R3555  
**Zeit:** 2026-01-17 23:39  
**Regel:** Konsolidiert = unique Items, keine Bewertung

### STRAT — Strategie / Grundsatz

- Website-Portfolio-Strategie (viele kleine vs. wenige große)
- Domain-Strategie (1 Domain = 1 Nische?)
- Naming- & Branding-System für Sites
- Vertrauens- & Ethik-Regeln (wann bewusst NICHT monetarisieren)
- Affiliate-Abhängigkeiten & Risiken
- Monetarisierungs-Reihenfolge (Affiliate → Own Product → Bundle)
- Kill-Kriterien für Websites (wann beenden?)
- Erfolgsdefinition Phase 1 (Indexierung, nicht Umsatz)
- Erfolgsdefinition Phase 2 (Conversion, nicht Traffic)
- Internationale Expansion (DE → EN?)
- Multi-Site-Orchestrierung vs. Single-Mega-Site

- Vergleichsseiten (v1, v2, vX)
- Alternativen-Seiten
- Buy-or-Skip-Seiten
- Hub-Seiten
- Übersichtsseiten
- Entscheidungs-PDFs
- Checklisten
- Templates
- Bundles

- Google Search Console Beobachtung
- Indexierungsstatus
- CTR von Titles
- Conversion pro Seitentyp
- Affiliate-Performance
- Update-Frequenz vs. Ranking
- Kill-Entscheidung dokumentieren
- Skalierungs-Trigger definieren
- priorisiert
- gesplittet
- gemerged
- auf skip gesetzt
- oder als obsolet markiert werden.

- Eigene PDFs (Decision Guides)
- Templates (Matrix, Checklisten)
- Produkt-Bundles
- Preis-Experimente
- Affiliate-Programme (Mapping)
- Risiko-Reduktion (nicht alles verlinken)
- Monetarisierung ohne Cookie-Hölle

- Static-Site-Ansatz evaluieren
- Generator/Exporter aus docs/websites/pages
- Build-Pipeline (Markdown → HTML)
- Frontmatter-Validator
- Broken-Link-Checker
- Sitemap-Generator
- Indexing-Helper
- QA-Runner für Veröffentlichungs-Gates
- Content-Skeleton-Generator
- Hub/Spoke-Autogenerator
- Multi-Domain-Deploy
- Page-Speed-Baseline
- Accessibility-Basics

- Vergleichsseiten-Template
- Alternativen-Seiten-Template
- Buy-or-Skip-Template
- Hub-Seiten-Template
- Content-Guidelines
- SEO-Guidelines
- Page-Metadata-Standard
- Release- & Update-Workflow
- Entscheidungs-Matrix-Vorlagen
- Monetarisierungs-Richtlinien
- Interne-Link-Standards
- Review-Checklisten

### DOC — Definitionen / Standards

### FEAT — Umsetzung / Technik

### CONTENT — Seiten & Assets

### MONETIZATION — Geld & Produkte

### OBS — Beobachtung / Messen

<!-- BAUSTEIN_SNIPPET_STANDARD:START -->
## Baustein-/Snippet-Standard fuer modulare Features (Core)

**Zweck:** Standardisierung neuer Funktionen und GUI-Elemente ueber wiederverwendbare Bausteine/Snippets mit definiertem Contract.  
**Ziel:** Stabilitaet, Skalierbarkeit, produktuebergreifende Wiederverwendung.  
**Regel:** **Neue Features = Baustein** (Bestand bleibt unangetastet, keine Voll-Rewrites).

### P0 – Definition (Docs-only)
- [ ] Baustein-/Snippet-Spec (1 Seite)
- [ ] Definition of Done (Baustein)
- [ ] No-Gos & Escape-Hatches (80/20, Fail-soft, kein Magie-Scanning ohne Whitelist)

### P1 – Referenz (Add-on, risikoarm)
- [ ] modules/baustein_contract.py (Result/Contract)
- [ ] modules/baustein_registry.py (Registry, fail-soft)
- [ ] 1 Referenz-Action-Baustein (Hello/Diag)
- [ ] Optional: 1 Referenz-GUI-Tab-Baustein (Notebook-Tab)

### P2 – Nutzungspflicht fuer Neues
- [ ] Pipeline-Eintraege fuer neue Features referenzieren eine Baustein-ID
- [ ] Keine Migration als Ziel (nur Standard fuer Neues)

### P3 – Opportunistische Anpassung
- [ ] Nur wenn bestehende Module ohnehin angefasst werden
- [ ] Adapter statt Rewrite (Mastermodus: minimal-invasiv, rueckbaubar)

### P4 – Produkt-Rollout
- [ ] ShrimpHub uebernimmt Baustein-Standard schrittweise per Produkt-Pipeline
- [ ] Weitere Produkte uebernehmen Standard nach Bedarf

<!-- BAUSTEIN_SNIPPET_GOVERNANCE -->
### Governance & Geltung

- Gilt ab: Runner R3561
- Regel: Neue Features und neue GUI-Elemente muessen als Baustein/Snippet umgesetzt werden.
- Nicht-Ziel: Keine Voll-Rewrites, keine Zwangsmigration bestehender Module.
- Vorgehen: Anpassung bestehender Module nur opportunistisch (wenn sie ohnehin angefasst werden).
- Prinzip: Add-on zuerst, Adapter statt Umbau, immer rueckbaubar.

### Explizite P0-Aufgabe (offen)
- [ ] Baustein-/Snippet-Spec (1 Seite) inkl. DoD, No-Gos, Escape-Hatches

<!-- BAUSTEIN_SNIPPET_STANDARD:END -->

<!-- R3566 BEGIN -->
- [x] Lane B: UI Purge Guard enforces canonical registry/tools_keep.txt (R3566).
<!-- R3566 END -->

## Lane E — Monetization (ACTIVE)
- Fokus: Vergleichsseiten (Affiliate/SEO)
- MVP: *Eine* Vergleichsseite
- KPI: Erste indexierte Seite (GSC sichtbar)
- Regel: Erst Proof, dann Skalierung
- Nächster Block: Docs/Strat (kein Code)

- ThreadCut (Pflicht)
  Jeder abgeschlossene Thread endet mit einem ThreadCut zur Verwertung
  von Regeln, Lernen, Dokumentation und Pipeline-Anpassungen.

## Backlog

<!-- BEGIN_R9316_IDEAS 2026-03-06 09:41:49 -->
## 🧠 Neue Ideen (auto-insert R9316, 2026-03-06 09:41:49)

> Eingesortiert & priorisiert (P0/P1/P2). Block ist marker-basiert und kann später manuell verschoben werden.

### General
- [P2] Clipboard History Manager Pro — Kategorie/Favoriten/Suche; offline.
- [P2] Folder/Repo Cleaner (Smart Folder Cleaner) — Findet Müll/alte Versionen; Archiv-Vorschläge.
- [P2] Log Analyzer Tool — Fehlercluster & Muster; hilfreich für Support/QA.
- [P2] PDF Toolkit / Bulk Image Optimizer — Klassische Utility-Bundles, gut verkaufbar.
- [P2] Shared Household Organizer (App) — Familienkalender + Aufgaben + Einkaufsliste.
- [P2] Subscription Tracker/Canceller (App) — Abo-Erkennung + Reminder vor Verlängerung.
- [P2] Universal Playlist Converter (App) — Playlist-Transfer zwischen Streamingdiensten.

### Lane A
- [P0] Doc–Code Drift Checker — Checks: Docs vs. Realität (Files/Module/Runner/Maps) + Report.
- [P0] Runner Simulation Mode (Dry-Run) — Runner laufen ohne echte Änderungen; reduziert Risiko/Drift.
- [P0] System Health Dashboard — Stabilitäts-Score aus Logs/Crashes/Runner-Reports; zentrale Ampel.
- [P1] Crash Replay / Crash Chain Analyzer — Crash-Ketten nachvollziehen, Wiederholungsquote, Hotspots.
- [P1] Module Ownership / Hot-Cold Matrix — Ownership + Risiko-Matrix für schnelle Diagnose.
- [P1] Runner Dependency Graph — Visualisiert Abhängigkeiten/Impact von Runnern.
- [P1] Silent Failure Detector — Findet „grüne“ Runs mit versteckten Fehlern/fehlenden Outputs.

### Lane D
- [P1] Affiliate Keyword Finder + Competitor Gap Finder — Keywords, Lücken, Priorisierung für neue Seiten.
- [P1] Auto Comparison Table Generator — Erzeugt Vergleichstabellen aus Produktdaten; Hugo-ready.
- [P1] Review Analyzer (Pros/Cons Extractor) — Aggregiert Reviews, extrahiert häufige Vor-/Nachteile.
- [P2] Auto FAQ Builder + Internal Linking Engine — FAQ/Interlinking automatisch; Evergreen-Refresh.
- [P2] Evergreen Content Scanner — Findet veraltete Artikel + Update-Vorschläge.

<!-- END_R9316_IDEAS -->
### Brainstorming 2026-02-23 (10 Ideen)
- [P2][IDEA] ShrimpDev AutoFix Engine (LearningJournal → Auto-Fix Vorschläge aus Logs/Patterns)
- [P2][IDEA] Clarivoo Money Radar (Trends/Suchintention → Content-Priorisierung)
- [P2][IDEA] ShrimpHub Storyboard → AutoVideo Pipeline (Script/Szenen/Prompts/VO/Struktur)
- [P2][IDEA] DISPO Reality Mode (Abwesenheiten/Änderungen simulieren → Replan Vorschläge)
- [P2][IDEA] ShrimpDev Crash Heatmap (häufigste Crashes nach Modul/Runner/Zeit)
- [P2][IDEA] Clarivoo Evergreen Engine (evergreen Kategorien identifizieren & priorisieren)
- [P2][IDEA] ShrimpDev Runner DNA System (Analyse erfolgreicher Runner-Strukturen → Best Practices)
- [P2][IDEA] DISPO Fairness Score 2.0 (Index über Wochen, schwere Aufgaben, Schichten)
- [P2][IDEA] ShrimpHub Asset Brain (Wiederverwendung: Assets/Skripte/VO intelligent matchen)
- [P2][IDEA] Clarivoo Conversion Booster Pages (Top3/Use-Case Seiten → höhere CTR/CVR)

- [ ] Intake: Button „Gate: R3677“ (Pipeline)
- Zweck: Ein-Klick-Ausführung von R3677 (Hugo build + interne Deadlink/Target-Prüfung).
- Scope: Planung (keine Implementierung in diesem Schritt).
- nutzt den kanonischen Runner-Executor
- zeigt nach Run den neuesten Report (Report-Viewer, kein Log-Popup)
- klar als Gate gekennzeichnet (protected/whitelisted)
- Klick startet R3677 mit korrektem Root
- Report wird angezeigt
- R3677 bleibt purge-protected

## Lane G – Monetarisierung (passiv, beobachtend)

### G1 – Artefakt-Extraktion aus bestehender Arbeit
Identifikation und Sammlung bereits existierender Artefakte (MasterRules, Pipeline-Patterns, ThreadCut-Struktur, Entscheidungslogik), die ohne Systemänderung extern nutzbar wären.
- Kein Bau neuer Produkte

### G2 – Produktionsmaschine für Affiliate- & Content-Projekte
Nutzung von ShrimpDev als interne Produktions- und Stabilitätsmaschine für Seiten wie Clarivoo und Folgeprojekte.
- Geld entsteht über Output, nicht über ShrimpDev
- Kein Einfluss auf Kernarchitektur

### G3 – Asynchrones Governance-/Audit-Modell (Marker)
Reines Denkmodell: Reports statt Calls, Diagnose statt Beratung.
- Nur als potenziell wertvolle Struktur markiert

### G4 – Read-only / Denkmodell-Abkömmlinge
Abstrakte Ableitungen (Read-only Tools, Denk-Frameworks), nur falls sie sich organisch ergeben.

## Nachsorge+ (2026-01-26) — Runner-IDs, Header-Fixes, Verifikation
### Ergebnis (Lane B abgeschlossen)
- Runner-ID-Migration in aktiven modules/-Dateien abgeschlossen → zentrale Nutzung über modules/runner_ids.py.
- Header-Fix-Pattern verifiziert: Wenn from future import annotations nicht „first statement“ ist → separater Header-Fix-Runner zuerst, dann eigentlicher Patch.

### Umgesetzt (Runner-Referenzen)
- Header-Fix: logic_tools.py (R8397)
- APPLY: logic_tools.py → runner_ids.* (R8398)
- APPLY: ui_toolbar.py → runner_ids.* (R8399)
- DIAG: Scan aktive 'R####' Literale (unfiltered) (R8400)
- Header-Fix: toolbar_runner_exec.py (R8402)
- APPLY: toolbar_runner_exec.py → runner_ids.* (R8401, OK-Lauf)
- APPLY: module_agent.py → runner_ids.* (R8403)
- DIAG: Finaler Filter-Scan (Artefakte ignoriert) (R8405) → keine aktiven Treffer (außer runner_ids.py als Definitionsquelle)

### Lessons Learned (dauerhaft)
- Diagnose zuerst, dann minimaler APPLY, dann Stop (kein Fix-Cascade).
- DOCS-Runner: keine festen Pfadannahmen für Pipeline-Dateien → bevorzugt docs/PIPELINE.md, sonst robust suchen.

### Offene Nachsorge+ Punkte (als nächste Runner)
- Artefakt-Hygiene: modules/*.pre_*, *.bak_*, *_FIXED_* aus modules/ nach Archiv verschieben oder offiziell dokumentiert ignorieren.
- Regression-Guard: DIAG-Runner als dauerhafte Prüfung „keine aktiven 'R####' Literale mehr“ (ohne runner_ids.py + ohne Artefakte).

### Lane A / P0 – Central Runner-Executor API (App ↔ logic_actions)

**Status:** DONE (Foundation)

**Ergebnis**
- Zentraler, minimaler Einstiegspunkt modules/runner_executor.py eingeführt
- Keine Migration bestehender Aufrufer (bewusst vertagt)
- Keine Verhaltensänderung, reine Entkopplung

**Nächster Schritt**
- Schrittweise Migration einzelner Aufrufer auf execute_runner()
- Separater Pipeline-Punkt, kein Bestandteil dieses P0

*(Dokumentiert nach APPLY R8415)*

### Lane A / P0 – Central Runner-Executor API (App ↔ logic_actions)

**Status:** DONE (Foundation + Smoke-Test)

**Ergebnis**
- Zentrale Executor-Schnittstelle vorhanden (modules/runner_executor.py)
- Smoke-Test GREEN (R8417)
- Keine Registry-/Allowlist-Annahmen (runner_ids = SSOT via Konstanten)

**Hinweis**
- Migration einzelner Aufrufer erfolgt als separater Pipeline-Punkt.

*(Dokumentiert: 2026-01-28 12:38, Runner R8418)*

- [ ] (P0) DISPO Mail: feste KPI finalisieren (View → Mail → fertig)
- Ziel: KPI immer in Mail (t_Status_Zahlen) + Zuteilungen aus t_DISPO_Slots
- No-Gos: keine optionalen KPI, keine stillen Fallbacks
- DoD: Compile grün + E2E Mail ok

- [2026-02-12 13:32] R8488: DISPO Layout manuell finalisiert (Nachsorge-Report: Report_R8488_20260212_133247.md)

<!-- R8590 AUTO-APPEND START -->
## [2026-02-15 00:57:01] R8590 – Nachsorge DISPO Mail/HTML (Nachlass-Block)

- Ursache: String/Concatenation-Brüche in BuildNachlassStatusTable (Insert/Patch Drift)
- SOLL: DMS + Mails als 2 Body-Zeilen direkt über Summe (Spalte 1)
- Next: Function-Replacement BuildNachlassStatusTable (1:1), danach visuelle Abnahme

<!-- R8590 AUTO-APPEND END -->

<!-- BEGIN:R8605 -->
## R8605 (Auto-Note) – DISPO Fairness / PlanDate / VBA Stabilität
- Date: 2026-02-16

### Learnings
- Fairness war leer, obwohl Planungen korrekt liefen (Status=OK, Final_ID gesetzt).
- Ursache: DISPO!C2 war optisch Datum, aber technisch Text → IsDate() schlägt fehl; robustes Parsing nötig.
- Fehlerklasse: 'Mehrdeutiger Name' durch doppelte Helper-Funktionen (ColIx/ColIxSafe/IsJa/IsWahr etc.).
- Fehlerklasse: Fehler 9 ('Index außerhalb des gültigen Bereichs') bei ListObject-Operationen mit Name-Lookup/Unlist/Delete → Loop-basierte Suche + lo.Delete ist stabiler.
- Fairness 'Cnt bleibt 1' ist für EINEN Tag plausibel; >1 entsteht erst über mehrere Tage oder mehrfach gleiche Aufgabe pro MA am selben Tag.

### TODO (Diagnose-first)
- Kumulierung über Tage verifizieren: PlanDate wirklich wechseln (>) und dann Fairness Totals prüfen (Cnt > 1 muss vorkommen).
- Diagnose-first: Fairness-Run soll 3 Zahlen loggen (Rows gelesen / Keys gezählt / PlanDate serial).
- Slot-Tabelle robust referenzieren (t_SLOTS vs t_DISPO_Slots) – keine harten Namen ohne Fallback.
- Abwesenheit (AbwesendHeute=Ja) → Button 'Replan (Safe)' triggert Replan + Delta-Update (Totals = Totals - Alt + Neu).
<!-- END:R8605 -->

<!-- R8602 BEGIN -->
## DISPO-Tool V1 (Freeze / Nachsorge)

**DONE (V1):**
- Planung stabil (Vorschlag/Override/Final), Final als Wahrheit
- Harte Regel: 1× Aufgabe pro MA/Tag (keine Doppelvergabe z. B. T08)
- Abwesenheit: Absent-Safe-Replan (nur betroffene Slots neu)
- Fairness Delta: t_Fairness_Day (Snapshot) → t_Fairness (Totals)
- Date-Serial-Fix: Value2-Dates robust geparst (kein Doppelcount)
- Fairness Reset: All-to-zero oder ab Stichtag (Rollback)

**NEXT (V1.1+):**
- Mail-Export ohne Outlook-Abhängigkeit (HTML-Datei/Entwurf)
- Optional: Outlook Classic Add-on (wenn Policy/Client passt)
- Diagnose „No candidate“ (Regelkonflikt/zu wenige qualifizierte MAs)
<!-- R8602 END -->
---

## 2026-02-17 — Nachsorge Lane B: Runner-SSOT (Popup) + DIAG-Kette R8652–R8659

**Abgeschlossen (Lane B / Core):**
- Popup-Runner delegiert Execution an modules/runner_executor.execute_runner (SSOT).
- Direct-Exec im Popup-Pfad entfernt (keine subprocess.Popen mehr in Popup-Flow).
- logic_actions.py direkte subprocess.run([cmd_path]) Blöcke bewusst nicht umgestellt: benötigt rc/out/err (Output-Capture); execute_runner ist fire-and-forget (siehe _r1851/_r1852).

**TechDebt / Tasks (in Pipeline aufnehmen):**
- [TD] Define return contract / capture-mode for runner execution:
- Option 1: New API execute_runner_capture(...) -> (rc, out, err) (or dict).
- Option 2: Extend execute_runner(..., capture=True) with explicit return type.
- [TD] Consolidate duplicated Output-Capture blocks in logic_actions.py (L1428/L1698) into one internal helper (no behavior change).
- [TD] Document SSOT boundary: UI-triggered runner starts must use SSOT; Output-Capture exec may stay local unless capture-API exists.

---

## Lane C Nachsorge (2026-02-17 10:56)

Status:
- Preflight-Modul vorhanden (modules/preflight_checks.py)
- Zentraler Hook NICHT gesetzt (bewusste Entscheidung nach DIAG)
- Keine Blind-Patches gemäß MasterRules

DIAG-Kette:
R8661–R8666

Entscheidung:
- Kein Risiko-Patch ohne eindeutigen Gatekeeper
- Zentraler Hook bleibt Tech-Debt Task

Tech-Debt:
- Global Runner Entry Mapping fehlt
- Preflight noch nicht SSOT-gekoppelt

Lane-C-Bewertung:
➡️ bearbeitet  
➡️ stabil  
➡️ nicht vollständig abgeschlossen

## ANCHOR — Run/Intake Stabilisierung
- Datum: 2026-02-18 23:45:04
- Snapshot: _Backups/R8724_20260218_234504
- Nachsorge-Report: Reports/Report_R8724_20260218_234504.md

### Status
- Run-Flow weiterhin instabil / no-op (GUI → Bridge/Logic → Executor unklar).
- Executor-Seite: cmd.exe-wrapper/timeout/cwd Themen bereits angefasst (siehe Snapshot/Reports).

### Nächster Einstieg
- DIAG-first: echten Run-Flow auflösen (welche Funktion wird vom Run-Button wirklich aufgerufen?).
- Danach 1 gezielter Fix (nur ein Layer).

### No-Gos
- Keine Mass-Patches/Regex über Core-Module.
- Keine Refactors (Popup/Output/Toolbar) ohne Plan.

<!-- SHRIMPDEV_AUTOGEN:R8486 NACHsorge START -->
## Nachsorge R8486 — RUN Stabilisierung / Legacy BAT

- R8485 Rollback/Restore (zu breite Änderungen; MR-H1/H7)
- Central BAT Guard (1 Chokepoint, rc=7 + Report), keine Massenedits
- Smoke-Test RUN (DirectRun + Compile-Gate)
- BAT-Entkopplung vervollständigen (nach Guard)
<!-- SHRIMPDEV_AUTOGEN:R8486 NACHsorge END -->

<!-- R8524_NACHSORGE_2026-02-21 -->

## P0 – Nachsorge Hardenings (2026-02-21)
- [P0] Purge auf Whitelist-SSOT umstellen (Exact-only) – Scan nur Diagnose
- [P0] R3106 entschärfen oder deaktivieren (kein Scan-driven Entscheidungs-Purge)
- [P0] Compile-Gate: zusätzlicher Guard “broken try/except/finally” (blockierend rc=7) – zentral, eine Stelle
- [P0] Smoke-Test Routine: (1) Import-Check (R8502) (2) GUI-Start (3) RUN (dry)

## P1 – Stabilisierung & UX
- [P1] Debug Output: SSOT root/debug_output.txt + GUI Log-Tab/View (statt Runner-Popup)
- [P1] Purge-Reports standardisieren (was bleibt/was geht/warum), ohne Docs/Reports als Referenzquelle

<!-- R8524_NACHSORGE_2026-02-21 -->

<!-- R8525_IDEA_POOL_BEGIN -->
## 🚀 IDEEN-POOL (AUTO-GENERIERT R8525)

### Lane B — Core / System (P1–P2)

- [ ] (P1) ShrimpCore: Command-System (plan/fix/build)
- [ ] (P1) State Engine + Session Snapshot
- [ ] (P1) ShrimpDev Brain (Decision + Pattern Recognition)
- [ ] (P2) LearningJournal 2.0 (Auto-Learn aus Fehlern)
- [ ] (P2) Anti-Chaos Engine (Fokus/Task-Lock)
- [ ] (P2) Execution Engine (Idee → Runner-Kette)
- [ ] (P2) System Health Score (Module/Runner Bewertung)

---

### Lane C — Tools / Automationen (P1–P2)
<!-- R9316_C_IDEAS_BEGIN -->
### Lane C — Tooling / Automationen — ergänzt durch R9316

- [ ] (P2) [CORE] Auto Changelog Generator — Commits/Reports in strukturierte Changelogs überführen.
- [ ] (P2) [CORE] Screenshot Organizer mit KI-Tags — Screenshots automatisch thematisch ordnen.
- [ ] (P2) [CORE] Local API Tester GUI — Leichtgewichtige lokale Test-GUI für APIs/Endpoints.
<!-- R9316_C_IDEAS_END -->

- [ ] (P1) Fix Engine (Scan → Analyse → Auto-Fix)
- [ ] (P1) Crash Analyzer (Logs clustern + Ursachen)
- [ ] (P1) Auto-Runner Generator (KI-basiert)
- [ ] (P2) Data Cleaner Tool
- [ ] (P2) Folder Organizer Tool
- [ ] (P2) Routine Builder
- [ ] (P2) Mail Automation Engine

---

### Lane D — Governance / Meta (P1–P2)

- [ ] (P1) Idea Incubator (Ideen sammeln + bewerten)
- [ ] (P1) Pipeline Auto-Optimizer
- [ ] (P1) Project DNA System (Ziel / Aufwand / ROI)
- [ ] (P2) Decision Log (Rejected Ideas Tracking)
- [ ] (P2) Feedback Loop System (Learnings → MR)

---

### Lane E — Websites / Monetarisierung (P2–P3)

- [ ] (P2) Clarivoo Content Factory (Batch Seiten)
- [ ] (P2) Decision Websites (Produktentscheidungen)
- [ ] (P2) Affiliate Funnel (Tool → Website → Conversion)
- [ ] (P3) Nischen-Wiki Systeme
- [ ] (P3) Local SEO Seiten

---

### Lane F — DISPO / Excel (P1–P2)

- [ ] (P1) DISPO Flexibilität (Config Fields + Regeln)
- [ ] (P1) Dynamische Views (Auto-Anpassung)
- [ ] (P2) Simulation Mode
- [ ] (P2) KPI Dashboard Ausbau
- [ ] (P2) Externe Produktversion vorbereiten

---

### Lane C/E Hybrid — KI Integration (P1–P2)

- [ ] (P1) Lokale KI Integration (Ollama API Bridge)
- [ ] (P1) KI Log Analyzer
- [ ] (P1) KI Code Fixer
- [ ] (P2) KI Content Generator
- [ ] (P2) KI Decision Engine

---

### Business Modelle (Meta → später zuweisen)

- [ ] (P2) Fix-as-a-Product (Mini Tools verkaufen)
- [ ] (P2) Decision Engines (Website + Tool Kombi)
- [ ] (P3) Tool Library (ShrimpLib Bundle)

<!-- R8525_IDEA_POOL_END -->

<!-- BEGIN:R8598 -->
## R8598 — P0 Stabilisierung (UI/Compile-Gate)

- [P0] Safe UI-Polish (Spacing/Alignment/Buttons) ohne große Block-Rewrites in main_gui.py
- [P0] Compile-Gate-Pflicht für UI-Patch-Runner (python -m py_compile ...)
- [P1] UI-Layout-Konsolidierung (pack/grid nicht mischen) — nur nach Diagnose + klarer Strategie
<!-- END:R8598 -->

R8601: Governance stabilized

### P0 — Intake SSOT (verbindlich, keine Interpretation)

#### Buttons

- Neu:
- Editor leeren
- neue Runner-ID vorbereiten
- Default-Zielpfad setzen
- LEDs reset

- Einfügen:
- Neu triggern
- Clipboard → Editor
- Erkennen triggern

- Erkennen:
- Name/Ext erkennen
- Runner-ID erkennen
- LEDs setzen
- KEINE Seiteneffekte

- Speichern:
- Datei → tools\
- Backup erstellen
- Report erstellen
- Liste refresh

- Undo:
- letzten Zustand wiederherstellen
- Backup-Fallback

- AOT:
- Mode togglen

- Restart:
- GUI neu starten

#### LEDs

- Syntax = Code valide
- Name/Ext = erkannt
- Datei = vorhanden
- Zielpfad = gültig
- AOT = aktiv

#### HARTE REGELN

- Einfügen = Clipboard ONLY (kein Datei-Load)
- UI enthält KEINE Logik → nur Bindings
- Alle Aktionen laufen über logic_actions (SSOT)
- Keine Runner patchen → neue Runner bauen

<!-- SHRIMPDEV_AUTOGEN:R9062 START -->
## Lane A — P0 (Autogen)

- [ ] Intake Build stabilisieren (keine geschluckten Exceptions).
- [ ] ui_project_tree.enable_* Calls: hasattr-guard oder entfernen.
- [ ] Left/Right (Paned) korrekt: paned.add(...), keine left/right.pack(...) Restlinien.
- [ ] Rechte Seite wieder aufbauen: Tree/Toolbar/OutputDisplay wieder einhängen.
- [ ] Danach: RUN Button wiring DIAG → 1 Fix → Funktionstest (cmd/py Dispatch).

_Quelle: Nachsorge R9062 (2026-02-25 23:51:06)_
<!-- SHRIMPDEV_AUTOGEN:R9062 END -->

<!-- IDEAS_INBOX_START -->

### 🧠 Auto-Imported Ideas (20260226_212126)

#### Funktionen
- Explain this UI Button
- Auto-Workflow Builder
- Undo Everything System
- Smart Notification Filter
- Cross-App Copy Engine
- Auto Documentation Generator
- Dead Feature Detector
- Sandbox Mode
- Error Explainer
- Workflow Memory

#### Tools
- Software Pain Scanner
- Mini CRM (Teamleiter)
- Excel Macro Visualizer
- Meeting → Task Converter
- File Chaos Cleaner
- Broken Process Detector
- Local AI Assistant
- Smart Screenshot Tool
- Affiliate Page Generator
- Plugin Marketplace

#### Monetarisierung
- Freemium
- Pay-per-Automation
- Team-Lizenzen
- White-Label
- Done-for-you Service
- Marketplace Revenue
- API Access
- Template Store
- Affiliate Einnahmen
- Consulting Bundle

#### Entwicklung / Strategie
- Problem first
- Nische statt Masse
- MVP in 2–4 Wochen
- Feedback Loop
- Reuse statt Neubau
- Eigene Workflows automatisieren
- Doku als Feature
- Modularität
- Monetarisierung pro Feature
- Workflow-Denken

<!-- IDEAS_INBOX_END -->

<!-- AUTO:IDEA_INTAKE_START -->
## Auto-Intake: Automatisierungs-Ideen (R9064)

| Prio | Bereich | Titel | Aufwand | Wert |
|---|---|---|---|---|
| P0 | ShrimpDev | Auto-PIPELINE Ingestor (Ideen → Tasks) | S | High |
| P0 | ShrimpDev | Runner Auto-Generator (Template Engine) | M | High |
| P0 | ShrimpDev | ShrimpDev Health Monitor | S | High |
| P1 | Clarivoo | Affiliate Link Manager | S | Med |
| P1 | Clarivoo | Clarivoo Content Auto-Builder | M | High |
| P1 | ShrimpDev | Auto-Diagnose System | M | High |
| P1 | ShrimpDev | Auto-Doc Sync Engine | M | High |
| P1 | ShrimpDev | Auto-Purge Intelligence | S | Med |
| P2 | Cross | Feature → Monetarisierung Mapper | S | Med |
| P2 | Cross | One-Click Productizer | L | Med |

### Reihenfolge
P0 → P1 → P2
<!-- AUTO:IDEA_INTAKE_END -->

## CLARIVOO – AUTO CONTENT & SCALING

### 🔴 P0 – FOUNDATION (MUST HAVE)
- Programmatic SEO (Template + Daten)
- Produktdaten SSOT (Zentrale DB)
- Content-Modularisierung (Bausteinsystem)

### 🟠 P1 – SCALING
- AI Content Pipeline (Keyword → AI → QC)
- Auto Vergleichstabellen Generator
- Automatische interne Verlinkung

### 🟡 P2 – OPTIMIZATION
- Evergreen Auto-Refresh (Preis/Verfügbarkeit)
- Performance-basierte Content-Optimierung
- Longtail Keyword Expansion

### 🔵 P3 – ADVANCED
- A/B Testing für Content
- Auto-Nischen-Finder (Trends + Nachfrage)

## Nachsorge
- 2026-02-28 00:21 Nachsorge R9107: Stabilisierung/Backups + SyntaxGate. Drift-Risiko bestätigt; nächster Schritt: Call-Site-DIAG für Intake-Builder (kein Raten nach _build_intake).

### 🟢 R9158 – Global Status System (ShrimpDev Übersicht)
- Eingetragen: 2026-03-01 08:20

**Ziel**
Zentrale Statusübersicht für das gesamte System

**Inhalt**
- Systemstatus (GUI, Runner, Compile, Git)
- Projektstatus (Dispo, ASM, Clarivoo, Apps)
- Pipeline-Fortschritt
- Tech-Debt / Risiken
- Monetarisierung

**Output**
- GUI Tab "Status"
- optional Report / CLI

**Begründung**
Verbesserte Übersicht und Steuerung, aber nicht betriebskritisch

---

# 🆕 R9067 – IDEA BATCH (Codex-Era Expansion)

## 🦐 ShrimpDev (P1–P2)
- Auto-DIAG Engine (Codex-driven)
- AST Guard System
- UI Layout Visualizer
- Runner Simulation Mode
- Auto-Fix Library
- Crash Replay System
- Pipeline Executor
- Dependency Map (visual)
- Multi-Agent Mode
- Self-Healing (LJ v2)

## 💻 Software (P2)
- Universal Config Sync
- Explain My Codebase
- Smart Changelog Generator
- Error Heatmap
- Clipboard Intelligence
- Local AI Dev Assistant
- Workflow Recorder
- File Intent Analyzer
- Bug Probability Scanner
- Refactor Engine

## 📱 Apps (P2–P3)
- Shared Smart Calendar
- AI Food Planner
- Micro Habit Tracker
- Voice-to-Task
- Money Visualizer
- Playlist Converter (HIGH POTENTIAL)
- Minimal Fitness
- Daily Reflection
- Chaos-to-Order
- Smart Buying Assistant

## 🌐 Clarivoo (P1)
- Auto-Content Engine (CRITICAL)
- Comparison Matrix Generator
- Affiliate Opportunity Scanner
- Auto-Update Bot
- SEO Gap Finder
- Review Synthesizer
- Top-10 Generator
- Niche Finder
- CTR Optimizer
- Bulk Page Creator

## 🌍 Webseiten (P2)
- Tool Comparison Platform
- Problem→Solution Finder
- App Comparison Hub
- Configurator Pages
- SaaS Landing Generator
- Job Tools Platform
- Prompt Library
- Fake Review Detector
- Price History Pages
- Alternatives Pages

## 💰 Monetarisierung (P0–P1)
- Clarivoo Affiliate (PRIMARY)
- Excel Tools Sales (DISPO/ASM)
- ShrimpDev (future SaaS)
- Micro-SaaS Tools
- Template Sales
- Automation Freelancing
- SEO Content Monetization
- Digital Products
- Tool Bundles
- B2B Internal Tools

## [R9300] Nachsorge abgeschlossen — 20260304_001527

- Zustand stabilisiert
- Offene Punkte priorisiert
- Architekturentscheidung dokumentiert (PanedWindow → Grid)
- Wiedereinstieg definiert (R9301)

# R9067 – Pipeline Idea Insert

## Lane A – Core / Stabilität

P0
- Runner Heatmap (Error/Run Frequency Analyse)
- Drift Scanner (UI + duplicate code detection)

P1
- Crash Timeline Analyzer
- Report Aggregator (Weekly Meta Reports)

P2
- Session Replay System
- Config Integrity Guard

## Lane B – Features

P0
- Treeview Sort Engine (Name / Date / Time)

P1
- Runner Sandbox Mode
- Dependency Graph Viewer

P2
- Patch Assistant (1-Fix Rule Enforcer)
- Stability Score Display

## Lane C – Vision / Research

P1
- LearningJournal AI Analyse Layer
- System Complexity Visualizer

P2
- Self-Healing Runner Generator
- Code Drift Prediction

## Lane D – Monetarisierung

P0
- DISPO Tool Produktisierung

P1
- Excel Automation Toolkit
- ShrimpHub Lite Distribution

P2
- Runner Template Marketplace
- Governance Toolkit

<!-- R9316_IDEA_INSERT_BEGIN -->

## ShrimpDev Stabilität Erweiterungen

- [ ] (P1) [CORE] System Health Dashboard — Stabilitätsmetriken aus Logs/Runner Reports
- [ ] (P1) [CORE] Runner Simulation Mode (Dry Run)
- [ ] (P1) [CORE] Doc-Code Drift Checker

## Tooling Erweiterungen

- [ ] (P2) [CORE] Log Analyzer Tool
- [ ] (P2) [CORE] Runner Dependency Graph
- [ ] (P2) [CORE] Crash Replay Analyzer

## Clarivoo Automatisierung

- [ ] (P2) [STRAT] Auto Comparison Table Generator
- [ ] (P2) [STRAT] Review Analyzer (Pros/Cons Extractor)
- [ ] (P3) [STRAT] Affiliate Keyword Finder

## App Ideen

- [ ] (P3) [STRAT] Universal Playlist Converter
- [ ] (P3) [STRAT] Shared Household Organizer
- [ ] (P3) [STRAT] Subscription Tracker

<!-- R9316_IDEA_INSERT_END -->

<!-- FEIERABEND_PIPELINE_BLOCK:START -->

### Inbox Import 20260307_220011

#### P0
- Arbeitszeit App für Schichtarbeiter
- Playlist Converter
- Runner Sandbox für ShrimpDev

#### P1
- Screenshot to Markdown Dokumentation Tool
- Shared Family Calendar
- Repo Health Dashboard

#### P2
- Aquarium Parameter Tracker
- Local AI Notes App
- Smart Backup Diff Tool

#### P3
- Niche Android Utilities
- Universal Clipboard Manager

<!-- FEIERABEND_PIPELINE_BLOCK:END -->

<!-- R9317:THREAD_IDEA_IMPORT:START -->

## Feierabend Thread-Ideen Import

_Automatisch importiert durch R9317 am 20260307_213929_

### Import-Regeln

- Priorisiert nach Wirkung, Umsetzbarkeit und strategischer Passung.
- Dedupe gegen bereits vorhandene Pipeline-Einträge.
- Fokus vorerst auf kostenarme bzw. kostenlose Infrastruktur.

### P0

#### Lane A / ShrimpDev

- [ShrimpDev] Automatic Drift Detector — Erkennt Änderungen außerhalb des Runner-Flows.
- [ShrimpDev] Idea to Pipeline Automation — Ideen automatisch in die bestehende Pipeline überführen.
- [ShrimpDev] Runner Failure Analyzer — Systematische Analyse fehlgeschlagener Runner.
- [ShrimpDev] Runner Risk Scanner — Bewertet Patch-Risiko vor Ausführung.
- [ShrimpDev] Runner-Sandbox-Modus — Dry-Run für Runner senkt Risiko und verhindert Fehlpatches.
- [ShrimpDev] Self-Repair Mode — Automatische Diagnose/Reparatur typischer Fehlerbilder.
- [ShrimpDev] System Stability Score — Messbarer Gesundheitswert für das Gesamtsystem.

#### Lane D / Apps

- [App] Arbeitszeit-Rechner für Schichtarbeit — Hohe reale Nachfrage, einfache MVP-Umsetzung, gutes App-Potenzial.
- [App] Playlist-Converter zwischen Musikdiensten — Starker Nutzerbedarf, hoher Nutzen, attraktives Tool/App-Thema.

#### Lane D / Clarivoo

- [Web] Affiliate Product Comparison Generator — Klarer Hebel für Content-Produktion und Monetarisierung.
- [Web] Content Aging Detector — Veraltete Inhalte automatisch identifizieren und priorisieren.
- [Web] Keyword Gap Finder — Hilft direkt bei SEO-Themenfindung und Skalierung.

### P1

#### Lane A / ShrimpDev

- [ShrimpDev] AI Code Review Runner — LLM/Codex-gestützte Vorprüfung von Änderungen.
- [ShrimpDev] Auto Cleanup Runner — Technische Schulden und Repo-Müll systematisch abbauen.
- [ShrimpDev] Auto Documentation Sync — Docs enger an den echten Code koppeln.
- [ShrimpDev] Auto Test Runner — Smoke-/Regressions-Checks standardisieren.
- [ShrimpDev] Automatischer Release Builder — Build/Release vereinheitlichen.
- [ShrimpDev] Automatisierte Release Notes — Stabiler Release-Prozess, weniger manuelle Last.
- [ShrimpDev] Bug Prediction System — Risikobereiche vor dem nächsten Fehler erkennen.
- [ShrimpDev] Codex Integration Manager — Codex-Nutzung strukturieren statt Bastelbude.
- [ShrimpDev] Development Timeline — Historie und Fortschritt nachvollziehbar machen.
- [ShrimpDev] Documentation Auto-Updater — Pflicht-Doku konsistent nachziehen.
- [ShrimpDev] Error Pattern Learning — Wiederkehrende Fehlerbilder automatisch erkennen.
- [ShrimpDev] GUI Crash Replay — Crashes reproduzierbar machen statt raten.
- [ShrimpDev] One-Click Branch Test — Tests in temporärem Clone ohne Hauptsystem-Risiko.
- [ShrimpDev] Pipeline Heatmap — Stau, Drift und tote Bereiche der Pipeline sichtbar machen.
- [ShrimpDev] Project Risk Scanner — Gefahren und Seiteneffekte früh markieren.
- [ShrimpDev] Repo Health Dashboard — Zentrale Übersicht zu Syntax, Docs, Pipeline und Konsistenz.
- [ShrimpDev] Runner Benchmark Tool — Runner-Laufzeiten und Flaschenhälse sichtbar machen.
- [ShrimpDev] Runner Generation AI — Runner nach Template schneller erzeugen.
- [ShrimpDev] Runner Impact Map — Welche Dateien besonders oft verändert werden.
- [ShrimpDev] Runner Registry Explorer — Runner-Bestand leichter durchsuchen und prüfen.
- [ShrimpDev] Runner Replay System — Ausführungen wiederholbar und diagnostizierbar machen.
- [ShrimpDev] Runner-Abhängigkeitsgraph — Zeigt Abhängigkeiten und Patch-Auswirkungen.
- [ShrimpDev] ShrimpDev Project Radar — Gesamtüberblick über Projekte, Status und Risiken.

#### Lane D / Apps

- [App] Einfacher Shared-Family-Kalender — Breit verständlicher Nutzen, gute Alltagstauglichkeit.
- [App] Parkplatz-Timer — Einfacher Nutzen, schneller MVP.
- [App] Scan to Excel — Praktisch für Arbeit und Alltag.
- [App] Shopping Price Tracker — Preisbeobachtung ist massentauglich.
- [App] Subscription Tracker — Viele Nutzer, klarer Schmerzpunkt.

#### Lane D / Clarivoo

- [Web] Affiliate-Link Manager — Monetarisierung robuster verwalten.
- [Web] AI-FAQ Generator — FAQ-Blöcke schnell ausrollen.
- [Web] Amazon Bestseller Scraper — Produktquellen für Vergleiche und Seitenideen.
- [Web] Auto Update Produktdaten — Pflegeaufwand senken, Aktualität erhöhen.
- [Web] Automatische Pros/Cons Generator — Skalierbare Content-Bausteine.
- [Web] Preis-Historie-Charts — Starker Mehrwert für Vergleichsseiten.
- [Web] Produkt-Schema Generator — SEO-Struktur verbessern.

#### Lane D / Tools

- [Tool] Git Repo Cleaner — Praktischer Utility-Charakter für viele Projekte.
- [Tool] Log File Analyzer — Passt direkt zu Diagnose/Dev-Workflows.
- [Tool] Meeting Recorder to Task Extractor — Direkter Produktivitätsgewinn.
- [Tool] Project Dependency Visualizer — Nützlich im Dev- und Analyse-Kontext.
- [Tool] Screenshot to Markdown Dokumentation Tool — Doku aus Screenshots erzeugen spart Zeit.

### P2

#### Lane A / ShrimpDev

- [ShrimpDev] Automatisches Refactoring Tool — Nützlich, aber riskanter als Diagnose-Tools.
- [ShrimpDev] Code Metrics System — Hilfreich, aber nicht der erste Schmerzpunkt.
- [ShrimpDev] Developer Knowledge Base — Wertvoll für Langzeitwissen.
- [ShrimpDev] Pipeline Drift Detector — Nützlich nach Basis-Stabilisierung.
- [ShrimpDev] ShrimpDev Plugin System — Spannend, aber architekturell schwerer.
- [ShrimpDev] Unified Project Map — Großer Nutzen, aber etwas mehr Strukturarbeit.

#### Lane D / Apps

- [App] Aquarium Parameter Tracker — Sehr passend, aber eher Nischenprodukt.
- [App] Daily Notes Timeline — Guter Use-Case, aber nicht dringend.
- [App] Idea Capture App Offline First — Passt zu deinem Stil, aber kein Top-Schmerzpunkt.
- [App] Local AI Notes App — Spannend, aber deutlich größerer Aufwand.
- [App] Minimal Habit Tracker — Einfach, aber stark besetzter Markt.
- [App] Minimalist To-Do App ohne Cloud — Klares Versprechen, aber viele Wettbewerber.
- [App] Plant Care Reminder — Nische, aber passend zu deinen Themen.
- [App] Receipt Scanner and Budget — Nützlich, aber umkämpfter Bereich.
- [App] Screenshot Organizer — Praktisch, aber mittlere Priorität.
- [App] Work Break Timer — Schneller MVP, aber kein Monsterhebel.

#### Lane D / Monetarisierung

- [Business] AI Generated Product Comparison Sites — Starker Hebel für Clarivoo-ähnliche Systeme.
- [Business] Automation Consulting für kleine Firmen — Sinnvoll, wenn Kernprodukte sauber vorzeigbar sind.
- [Business] Automation Scripts Store — Kann gut zu Runnern/Utilities passen.
- [Business] Excel Tools Marketplace — Sehr passend, braucht aber Angebotsreife.
- [Business] Micro SaaS Shared Calendar — Interessant, aber größerer Support-/Hosting-Scope.
- [Business] ShrimpDev Pro Version — Monetarisierung nach stärkerer Produktreife.
- [Business] Subscription Dev Tools Bundle — Später interessant als Paket-Angebot.
- [Business] Template Packs — Naheliegend mit deinem Runner/Tool-Wissen.

#### Lane D / Tools

- [Tool] AI-Code Explain Tool — Praktisch für Analyse und Onboarding.
- [Tool] Auto Folder Organizer — Guter Nutzen, mittlere Priorität.
- [Tool] Codebase Search AI — Wertvoll, aber komplexer.
- [Tool] CSV to Dashboard Generator — Praktisch, besonders im Office-Kontext.
- [Tool] Desktop Automation Builder — Potent, aber größerer Scope.
- [Tool] Folder Size Visualizer — Praktischer Utility-Fall.
- [Tool] Local AI Knowledge Base — Großes Potenzial für Suche und Wissen.
- [Tool] Local File Search AI — Starkes Tool, aber höherer Aufwand.
- [Tool] Local Prompt Library Manager — Hilfreich für KI-Workflows.
- [Tool] Offline Notes mit Git Sync — Interessant, aber nicht oberste Baustelle.
- [Tool] Screenshot to Code Extractor — Nützlich, aber fehleranfällig.
- [Tool] Simple Local Wiki Server — Wissensablage lokal und schlicht.
- [Tool] Smart Backup Diff Tool — Passt direkt zu deinem Arbeitsstil.
- [Tool] Terminal Command History Search — Hilfreich für Dev-Workflows.
- [Tool] Universal Config Manager — Nützlich für Power-User.

### P3

#### Lane D / Apps

- [App] Niche Android Utilities — Breiter Sammelbegriff, später konkretisieren.

#### Lane D / Tools

- [Tool] Universal Clipboard Manager — Solider Utility-Fall, aber nicht vorn.

### Import-Notiz

- Übersprungen, da schon außerhalb dieses Managed-Blocks in der Pipeline vorhanden: 0

<!-- R9317:THREAD_IDEA_IMPORT:END -->

---

# PIPELINE STRUCTURE

## IDEAS

<!-- R9325:PRIORITY_IMPORT:START -->

### Priority Import (R9325)

_Automatisch importiert am 20260317_212556 aus `Idea_Priority_Report_20260307_224453.md`._

**Regeln**

- Marker-basierter Managed-Block
- Top priorisierte Ideen aus dem letzten Priority-Report
- Keine Änderungen außerhalb dieses Blocks

#### HIGH_POTENTIAL

- [HIGH_POTENTIAL][FAST_MVP][WEBSITE_PLAY] Affiliate Opportunity Scanner
- [HIGH_POTENTIAL][FAST_MVP][SHRIMPDEV_CORE] Erlaubt: gemeinsame Tooling-Runner (Scanner/Generator/Reports) ohne Shared State.
- [HIGH_POTENTIAL][WEBSITE_PLAY] Affiliate Einnahmen
- [HIGH_POTENTIAL][WEBSITE_PLAY] Affiliate Funnel (Tool → Website → Conversion)
- [HIGH_POTENTIAL][WEBSITE_PLAY] Affiliate Keyword Finder
- [HIGH_POTENTIAL][WEBSITE_PLAY] Affiliate Keyword Finder + Competitor Gap Finder
- [HIGH_POTENTIAL][WEBSITE_PLAY] Affiliate Page Generator
- [HIGH_POTENTIAL][WEBSITE_PLAY] Affiliate Product Comparison Generator
- [HIGH_POTENTIAL][WEBSITE_PLAY] Affiliate-Abhängigkeiten & Risiken
- [HIGH_POTENTIAL][WEBSITE_PLAY] Affiliate-Link Manager
- [HIGH_POTENTIAL][WEBSITE_PLAY] Affiliate-Performance
- [HIGH_POTENTIAL][WEBSITE_PLAY] Affiliate-Programme (Mapping)
- [HIGH_POTENTIAL][WEBSITE_PLAY] Auto Comparison Table Generator
- [HIGH_POTENTIAL][SHRIMPDEV_CORE] Auto-Runner Generator (KI-basiert)
- [HIGH_POTENTIAL][WEBSITE_PLAY] Clarivoo Affiliate (PRIMARY)
- [HIGH_POTENTIAL][WEBSITE_PLAY] Comparison Matrix Generator
- [HIGH_POTENTIAL][WEBSITE_PLAY] Content-Skeleton-Generator
- [HIGH_POTENTIAL][WEBSITE_PLAY] Fokus: Vergleichsseiten (Affiliate/SEO)
- [HIGH_POTENTIAL][WEBSITE_PLAY] KI Content Generator
- [HIGH_POTENTIAL][WEBSITE_PLAY] Monetarisierungs-Reihenfolge (Affiliate → Own Product → Bundle)

#### FAST_MVP

- [FAST_MVP][SHRIMPDEV_CORE] A-P1-01: RunnerExec Clean-Rebuild (minimal, testbar)
- [FAST_MVP][SHRIMPDEV_CORE] Diagnose zuerst, dann minimaler APPLY, dann Stop (kein Fix-Cascade).
- [FAST_MVP][WEBSITE_PLAY] Evergreen Content Scanner
- [FAST_MVP][SHRIMPDEV_CORE] P0.B Smoke/Crash-Schutz: Read-only Smoke-Runner vor APPLY-Stufen (Import + minimaler Toolbar-Aufbau wenn möglich).

#### WEBSITE_PLAY

- [WEBSITE_PLAY][IDEA] [IDEA] Clarivoo Money Radar (Trends/Suchintention → Content-Priorisierung)
- [SHRIMPDEV_CORE][WEBSITE_PLAY] AI Content Pipeline (Keyword → AI → QC)

#### SHRIMPDEV_CORE

- [SHRIMPDEV_CORE][IDEA] [IDEA] ShrimpDev AutoFix Engine (LearningJournal → Auto-Fix Vorschläge aus Logs/Patterns)
- [SHRIMPDEV_CORE][IDEA] [IDEA] ShrimpDev Crash Heatmap (häufigste Crashes nach Modul/Runner/Zeit)
- [SHRIMPDEV_CORE][IDEA] [IDEA] ShrimpDev Runner DNA System (Analyse erfolgreicher Runner-Strukturen → Best Practices)
- [SHRIMPDEV_CORE][IDEA] [IDEA] ShrimpHub Storyboard → AutoVideo Pipeline (Script/Szenen/Prompts/VO/Struktur)

<!-- R9325:PRIORITY_IMPORT:END -->

## APPS

## TOOLS

## WEBSITES

## SHRIMPDEV TECH

## MONETIZATION

## ARCHIVE

<!-- R9326:TASKS:START -->

### Priority Tasks (R9326)
_Generated 20260317_212557_

#### Lane X – Misc

- P1: Markerbasierter ManagedBlock
- P1: Top priorisierte Ideen aus dem letzten PriorityReport
- P1: Keine Änderungen außerhalb dieses Blocks

#### Lane D – Clarivoo

- P1: Affiliate Opportunity Scanner
- P1: Affiliate Einnahmen
- P1: Affiliate Funnel (Tool → Website → Conversion)
- P1: Affiliate Keyword Finder
- P1: Affiliate Keyword Finder + Competitor Gap Finder
- P1: Affiliate Page Generator
- P1: Affiliate Product Comparison Generator
- P1: AffiliateAbhängigkeiten & Risiken
- P1: AffiliateLink Manager
- P1: AffiliatePerformance
- P1: AffiliateProgramme (Mapping)
- P1: Auto Comparison Table Generator
- P1: Clarivoo Affiliate (PRIMARY)
- P1: Comparison Matrix Generator
- P1: ContentSkeletonGenerator
- P1: Fokus: Vergleichsseiten (Affiliate/SEO)
- P1: KI Content Generator
- P1: MonetarisierungsReihenfolge (Affiliate → Own Product → Bundle)
- P1: Evergreen Content Scanner
- P1: Clarivoo Money Radar (Trends/Suchintention → ContentPriorisierung)
- P1: AI Content Pipeline (Keyword → AI → QC)

#### Lane A – ShrimpDev Core

- P1: Erlaubt: gemeinsame ToolingRunner (Scanner/Generator/Reports) ohne Shared State.
- P1: AutoRunner Generator (KIbasiert)
- P1: AP101: RunnerExec CleanRebuild (minimal, testbar)
- P1: Diagnose zuerst, dann minimaler APPLY, dann Stop (kein FixCascade).
- P1: P0.B Smoke/CrashSchutz: Readonly SmokeRunner vor APPLYStufen (Import + minimaler ToolbarAufbau wenn möglich).
- P1: ShrimpDev AutoFix Engine (LearningJournal → AutoFix Vorschläge aus Logs/Patterns)
- P1: ShrimpDev Crash Heatmap (häufigste Crashes nach Modul/Runner/Zeit)
- P1: ShrimpDev Runner DNA System (Analyse erfolgreicher RunnerStrukturen → Best Practices)
- P1: ShrimpHub Storyboard → AutoVideo Pipeline (Script/Szenen/Prompts/VO/Struktur)

<!-- R9326:TASKS:END -->















<!-- R9330:PROJECTS:START -->

## Projects (Generated R9330)

### PROJECT: ShrimpDev Stability Suite

- L429 | Lane F: - [ ] (P3) [CORE] TODO: list: add a high-priority item about tracebacks in log. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19969)
- L442 | Lane F: - [ ] (P3) [CORE] TODO: list: add a high-priority item about tracebacks in log. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2144.py:L118)
- L399 | Lane F: - [ ] (P1) [CORE] TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh).\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2143.py:L250)
- L394 | Lane F: - [ ] (P1) [CORE] TODO: (Pipeline), sondern bekommen einen eigenen Tab. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19929)
- L398 | Lane F: - [ ] (P1) [CORE] TODO: (Pipeline), sondern bekommen einen eigenen Tab. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2143.py:L2)
- [x] (P0) [CORE] (HIGHEST / BLOCKER) R2372 – Architektur: INI Single Writer (Design + API) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L122)
- [x] (P0) [CORE] (HIGHEST / BLOCKER) R2376 – Docking über Single Writer (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L141) — DONE (verified 2026-01-12 via R3378/R3379)
- [x] (P1) [CORE] Docking: Verify-Runner für Undock/Restore/UI-Integration (inkl. Log-Tab Button-Row)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) R2374 – config_manager Save konsolidieren (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L133)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) R2375 – Shims: config_loader.py / config_mgr.py (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L137)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) R2377 – Monkeypatch/Altlogik Quarantäne (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L148)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) R2378 – Restore Reihenfolge finalisieren (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L152)
- [ ] (P0) [CORE] (HIGHEST / BLOCKER) R2379 – Regression-Testplan (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L156)
- [ ] (P1) [PROD] TODO: \n- File: {pipeline}\n- Backup: {backup}\n", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Archiv/Runner_Staging_2025-12-25/R2598.py:L59)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L24)
- [ ] (P1) [CORE] NOTE: Did not match expected 'run: uvx ruff ...' lines. Please verify ci.yml manually.", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2580.py:L109)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L25)
- [ ] (P1) [PROD] TODO: ][HIGH] Runner-Cleanup – Archivierung unbenutzter Runner _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Pipeline/Pipeline_R2016_RunnerCleanup_20251208_154653.txt:L1)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L27)
- [ ] (P1) [CORE] (P1) ... (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/ARCHITECTURE.md:L176)
- [ ] (P1) [CORE] TODO: (Pipeline), sondern bekommen einen eigenen Tab. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19929)
- [ ] (P1) [CORE] TODO: in der Pipeline-Datei. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L7958)
- [ ] (P1) [CORE] TODO: in docs/Master/Pipeline_Notes.md eintragen: (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L8944)
- [ ] (P1) [CORE] TODO: (Pipeline), sondern bekommen einen eigenen Tab. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2143.py:L2)
- [ ] (P1) [CORE] TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh).\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2143.py:L250)
- [ ] (P1) [CORE] TODO: ) Pipeline-Eintrag: Tracebacks wieder ins Log (HIGH) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2144.py:L9)
- [ ] (P1) [CORE] NOTE: for Docking incident and doc links (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2397.py:L2)
- [ ] (P1) [PROD] docs/Architecture_ProjectTab.md – Datenquellen/Contract (nur lesen: PIPELINE, Reports, SmokeTest) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2521.py:L76)
- [ ] (P3) [PROD] TODO: (reports/ordner konsolidieren) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2596_20251225_111324.md:L4)
- [ ] (P3) [PROD] TODO: : False (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2655_20251225_200722.md:L84)
- [ ] (P3) [PROD] TODO: (reports/ordner konsolidieren)\n" _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/_Archiv/Runner_Staging_2025-12-25/R2596.py:L93)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L28)
- [ ] (P3) [PROD] TODO: ", _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2655.py:L129)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L40)
- [ ] (P3) [PROD] TODO: /FIXME in code) _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.cmd:L5)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L41)
- [ ] (P3) [STRAT] TODO: markers _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.py:L107)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L42)
- [ ] (P3) [PROD] TODO: |FIXME|HACK|NOTE)\b[:]?\s*(?P<text>.*)$', re.IGNORECASE) _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.py:L26)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L43)
- [ ] (P3) [STRAT] TODO: /FIXME/HACK/NOTE markers in *.py/*.cmd/*.bat/*.ps1/*.yml/*.toml _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2658.py:L8)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L44)
- [ ] (P3) [STRAT] TODO: /FIXME Marker). Bitte bei Bedarf konsolidieren.\n\n") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2659.py:L108)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L45)
- [ ] (P3) [CORE] TODO: Flag/Policy). (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Architecture_DnD_FileOut.md:L21)
- [ ] (P3) [CORE] TODO: list: add a high-priority item about tracebacks in log. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19969)
- [ ] (P3) [CORE] TODO: (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L7989)
- [ ] (P3) [CORE] TODO: bereits vorhanden – uebersprungen.\n") (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L8918)
- [ ] (P3) [CORE] TODO: hinzugefuegt.\n") (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L8921)
- [ ] (P3) [CORE] HACK: für on_sort (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R1301_IntakeV1_Install.py:L353)
- [ ] (P3) [CORE] TODO: actual UI factory if separate exists\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R1305_IntakeHardFix.py:L70)
- [ ] (P3) [CORE] TODO: list: add a high-priority item about tracebacks in log. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2144.py:L118)
- [ ] (P3) [CORE] (TOP/HIGH) Phase 2: Restore-Orchestrierung (pro Fenster-Key) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2375.py:L66)
- [ ] (P3) [CORE] (HIGH) Migration: Remaining Writers -> SingleWriter (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2375.py:L79)
- [ ] (P3) [PROD] (MED) Defactoring / Archivierung (nach erfolgreicher Umstellung) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2375.py:L83)
- [ ] (P3) [CORE] TODO: (optional): hier später Reflow/Anordnung implementieren. (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_1171m_IntakeToolbarReflowFix.py:L47)
- [ ] (P3) [CORE] Regression Checklist: Rechtsklick links/rechts, Selection behavior, busy-state, messageboxes (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L95)
- [ ] (P3) [CORE] docs/Architecture_ProjectTab.md – Definition + Non-Goals (keine Buttons, keine neue Logik) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2521.py:L75)
- [ ] (P3) [CORE] docs/Architecture_ProjectTab.md – Minimaler Anzeige-Contract/Wireframe (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2521.py:L77)
- [ ] (P3) [STRAT] TODO: markers (now also in .md) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2661.py:L218)
- [ ] (P3) [CORE] TODO: /FIXME/HACK/NOTE lines ALSO in Markdown (.md) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2661.py:L9)
- Canonical autopush backend (OneDrive repo-only): tools/R2691 (Private), tools/R2692 (Public), tools/R2693 (Both).
- Public Root: automatisch ableitbar (z. B. ShrimpDev_REPO → ShrimpDev_PUBLIC_EXPORT), optional autocreate des Ordners
- Export must write/update docs/Public_Contract.md in the public repo.
- Isolation: keine Abhängigkeit zu ShrimpDev-Core-State (kein Zugriff auf ShrimpDev.ini, Docking/UI-State, Runner-Registry).
- ShrimpDev.ini [Docking] bleibt unverändert trotz undocked Tabs / App close.
- [ShrimpDev] Self-Repair Mode — Automatische Diagnose/Reparatur typischer Fehlerbilder.
- [ShrimpDev] Auto Cleanup Runner — Technische Schulden und Repo-Müll systematisch abbauen.
- [ShrimpDev] Auto Documentation Sync — Docs enger an den echten Code koppeln.
- [ShrimpDev] Repo Health Dashboard — Zentrale Übersicht zu Syntax, Docs, Pipeline und Konsistenz.
- [Tool] Log File Analyzer — Passt direkt zu Diagnose/Dev-Workflows.
- [ShrimpDev] Automatisches Refactoring Tool — Nützlich, aber riskanter als Diagnose-Tools.

### PROJECT: ShrimpDev Stability Suite

- Compile OK: modules/ui_toolbar.py, modules/logic_actions.py, modules/toolbar_runner_exec.py, modules/module_runner_popup.py
- P0.C Central Dispatch Entry-Point: toolbar actions laufen über _dispatch_action(...) (minimaler Router-Einstieg, keine Behavior-Änderung). (Verification: Report_R3409_20260113_095743.md) — DONE (verified 2026-01-13)
- Runner-Popup zeigt:
- In modules/module_runner_popup.py:
- [ ] (P1) [CORE] Prüfen/Plan: modules/ui_toolbar.py modularisieren (Import-kritisch) — Ziel: kleine Module (builders/actions/hooks), weniger Seiteneffekte, bessere Testbarkeit
- Regeln: niemals destructive Runner ohne explizite Bestätigung; keine Background-Exec.
- [ ] Define one canonical entrypoint (e.g. runner_exec.run_by_id(app, "R####") or app.run_runner_by_id("R####"))
- [ ] Buttons call logic_actions → executor
- Runner-ID-Migration in aktiven modules/-Dateien abgeschlossen → zentrale Nutzung über modules/runner_ids.py.
- Zentraler, minimaler Einstiegspunkt modules/runner_executor.py eingeführt
- Zentrale Executor-Schnittstelle vorhanden (modules/runner_executor.py)
- Popup-Runner delegiert Execution an modules/runner_executor.execute_runner (SSOT).
- Direct-Exec im Popup-Pfad entfernt (keine subprocess.Popen mehr in Popup-Flow).
- Consolidate duplicated Output-Capture blocks in logic_actions.py (L1428/L1698) into one internal helper (no behavior change).
- Document SSOT boundary: UI-triggered runner starts must use SSOT; Output-Capture exec may stay local unless capture-API exists.
- [ ] (P2) System Health Score (Module/Runner Bewertung)
- Alle Aktionen laufen über logic_actions (SSOT)

### PROJECT: Auto / Reports / Shrimpdev Cluster

- DoD: Scan letzte Reports; dedup Root-Causes; Vorschläge Lane/Priority; kein Auto-Write.
- [x] (DONE) DIAG: INI write offenders scan (R3347) → Report_R3347_20260112_125757.md
- [ ] Reports/ scannen (z. B. letzte 30)
- [ ] (P1) Report-Index (letzte Reports, OK/FAIL, Links)
- [x] (P3) [PROD] NOTE: btn_apply pack line not found (maybe already adjusted).") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2448.py:L138)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L31) (auto-closed R2854: obsolete)
- [x] (P3) [PROD] NOTE: btn_scan pack line not found (maybe already adjusted).") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2448.py:L148)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L32) (auto-closed R2854: obsolete)
- [x] (P3) [PROD] NOTE: {'patched' if c4 else 'no-op'}") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2576.py:L184)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L35) (auto-closed R2854: obsolete)
- [x] (P3) [PROD] NOTE: {'patched' if c3 else 'no-op'}") _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2577.py:L174)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L36) (auto-closed R2854: obsolete)
- [x] (P3) [PROD] NOTE: Root tools_keep.txt exists but is obsolete. Canonical file is registry/tools_keep.txt (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2416_RegistryAndDocsFix_20251221_105138.md:L9) (auto-closed R2854: obsolete)
- [x] (P3) [CORE] NOTE: Root tools_keep.txt exists but is obsolete. " (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2416.py:L125) (auto-closed R2854: obsolete)
- [ ] (P2) [CORE] LearningJournal Auto-Write: Diagnose + Guard (nach CI stabil)
- Ziel: Aus LJ/Logs/Reports Vorschläge ableiten (Cluster/Häufigkeit/Impact), ohne Auto-Fix.
- [P2][IDEA] ShrimpDev AutoFix Engine (LearningJournal → Auto-Fix Vorschläge aus Logs/Patterns)
- [ ] (P2) [CORE] Auto Changelog Generator — Commits/Reports in strukturierte Changelogs überführen.
- [ ] (P1) Fix Engine (Scan → Analyse → Auto-Fix)
- [IDEA] ShrimpDev AutoFix Engine (LearningJournal → Auto-Fix Vorschläge aus Logs/Patterns)

### PROJECT: Runner / Apply / Diag Cluster

- Runner-Sequenz: DIAG wiring → APPLY DirectRun (ein Einklinkpunkt) → DIAG End-to-End.
- [x] (DONE) APPLY: Fix: Runner-ID mismatch (py = cmd-1) (R3351)
- [ ] Empfehlung: Lane/Phase + nächster Runner-Typ (DIAG/APPLY)
- [ ] (P3) Pilot: DIAG-only Worker (Workspace-Isolation, Diff/Report, kein Auto-Apply)
- R8609: Trace-DIAG „Click → Dispatch → Runner resolve → subprocess → rc → Popup“
- [ ] Replace any ad-hoc subprocess/runner wiring in UI code to call the executor only
- [ ] no runner wiring logic beyond calling logic_actions/executor
- [ ] Explicitly enforce: DIAG → one APPLY → stop; no “runner fixes runner fixes runner”
- APPLY: logic_tools.py → runner_ids.* (R8398)
- APPLY: ui_toolbar.py → runner_ids.* (R8399)
- APPLY: toolbar_runner_exec.py → runner_ids.* (R8401, OK-Lauf)
- APPLY: module_agent.py → runner_ids.* (R8403)
- DIAG: Finaler Filter-Scan (Artefakte ignoriert) (R8405) → keine aktiven Treffer (außer runner_ids.py als Definitionsquelle)
- Regression-Guard: DIAG-Runner als dauerhafte Prüfung „keine aktiven 'R####' Literale mehr“ (ohne runner_ids.py + ohne Artefakte).

### PROJECT: ShrimpDev Stability Suite

- [ ] Codex CLI installieren & Projekt-Trust setzen (lokal) + Basiskonfig (read-only default)
- [ ] Projekt-Konfig: .codex/config.toml im Repo (read-only → workspace-write nur für Fix-Runner)
- C-P1-02: Report-Agent MVP (Reports → Todos → Priorisierung, read-only)
- Only items that block app start or cause crashes in default flows remain P0.
- [ ] (P1) Report-Agent: Reports-Auswertung → Todos ableiten → priorisieren → Pipeline-Einsortierung (MVP DIAG, optional APPLY) <!-- TASK_REPORT_AGENTR3755_NACHSORGE_RUNNER_PROTECT --> - Quelle/Referenz: R3755 (Agent-Report), R3753 (Output-Guard), Nachsorge-Regeln (MR-NG*) - MVP (DIAG / read-only):
- [ ] (P3) Codex CLI Setup (Installation + local smoke: codex --version)
- DONE: R9141 MasterRules ergänzt (Windows CLI & Runner Standards).
- P0.B Smoke/Crash-Schutz: Read-only Smoke-Runner vor APPLY-Stufen (Import + minimaler Toolbar-Aufbau wenn möglich). — DONE (verified via R3390 on 2026-01-12) (Verification: Report_R3390_20260112_210110.md)
- [x] (P0) [CORE] (HIGHEST / BLOCKER) Central Runner-Executor API (App ↔ logic_actions) — UI-Actions dürfen keine Runner-IDs kennen; 1 kanonischer Executor + Smoke-Test- [ ] (P0) [CORE] NOTE: that CI blockers were fixed via R2576. _(src: C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2576.py:L103)_ (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/Reports/Report_R2658_20251225_202537.md:L18)- [ ] (P0) (HIGHEST / BLOCKER) R2373 – Implementierung: zentraler INI-Writer (Merge + atomic) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/INI_WriteMap.md:L14478)- [ ] (P0) (HIGHEST / BLOCKER) R2371 – INI-WriteMap (READ-ONLY Diagnose) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/R2370.py:L117)
- DIAG (read-only): Widget-Tree-Dump des Log-Tabs
- Default-Zielpfad setzen
- P0.B Smoke/Crash-Schutz: Read-only Smoke-Runner vor APPLY-Stufen (Import + minimaler Toolbar-Aufbau wenn möglich).

### PROJECT: Docs / Masterrules / Repo Cluster

- Änderungen müssen docs-konsistent sein (MasterRules, FILE_MAP, PIPELINE, SHORTCODES).
- L395 | Lane F: - [x] (P1) [CORE] TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh).\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19950)- [ ] (P1) [CORE] TODO: ) Pipeline-Eintrag: Tracebacks wieder ins Log (HIGH) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19967)
- docs/MasterRules.md
- docs/SHORTCODES.md
- docs/FILE_MAP.md, docs/SYSTEM_MAP.md (falls vorhanden)
- jobs: → darunter müssen Job-IDs eingerückt sein (z. B. lint:)
- [ ] (P1) [CORE] TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh). (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Pipeline_Notes.md:L29)
- [x] (P1) [CORE] TODO: -Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh).\n" (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19950)- [ ] (P1) [CORE] TODO: ) Pipeline-Eintrag: Tracebacks wieder ins Log (HIGH) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L19967)
- [ ] (P3) [CORE] Define Actions Registry (Docs): Liste der erlaubten Actions + Labels (Copy Path/File/Text, Open, Folder, Restore gated) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L90)
- [ ] (P3) [CORE] Central Helpers Plan (Docs): gemeinsame Helper-Funktionen (clipboard, file-copy-paste, restore-safe) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L92)
- Verankerung: siehe MR-STRAT-FOCUS-01 in docs/MasterRules.md.
- Kill/Scale Kriterien: müssen pro Site schriftlich definiert sein (kein "wird schon").

### PROJECT: ShrimpDev Stability Suite

- [ ] Doppelte UI-Blöcke: erst entfernen, wenn neue Verdrahtung verifiziert ist (Smoke grün)
- [ ] (LOW) Runner-WARN venv python not found / Template-Policy: WARN ist kosmetisch; Templates greifen nur bei Neugenerierung; optional später REQUIRE_VENV-Flag (WARN nur wenn explizit verlangt).
- [ ] Wenn Funktion ersetzt wird: modularer Ersatz, Alt-Runner erst nach Stabilitätsnachweis aus der kritischen Nutzung nehmen
- Hinweis-Idee: Wenn Final (Name) gefüllt ist ⇒ MA ist geplant ⇒ 1 Punkt auf MA-ID (nur wenn Regel/Contract das so will).
- Das Problem ist nicht primär „Verdrahtung fehlt“, sondern wahrscheinlicher:
- DoD: Smoke grün nach jedem APPLY; Report + Exitcodes.
- Wenn Fix nicht direkt verifiziert: Diagnose zuerst (MR)
- Pipeline-Review ist verpflichtend, aber nicht chaotisch: Prioritäten werden angepasst, wenn Brisanz steigt/fällt.
- Fairness 'Cnt bleibt 1' ist für EINEN Tag plausibel; >1 entsteht erst über mehrere Tage oder mehrfach gleiche Aufgabe pro MA am selben Tag.
- logic_actions.py direkte subprocess.run([cmd_path]) Blöcke bewusst nicht umgestellt: benötigt rc/out/err (Output-Capture); execute_runner ist fire-and-forget (siehe _r1851/_r1852).
- P0.B Smoke/CrashSchutz: Readonly SmokeRunner vor APPLYStufen (Import + minimaler ToolbarAufbau wenn möglich).

### PROJECT: Dann / Toolbar / Tree Cluster

- [ ] Layout-Fix (nur 1 Patch): LEFT=Intake, RIGHT=Output+Toolbar+Tree (erst messen, dann fixen)
- [ ] Treeview leer: Datenquelle/Bindings/Refresh messen (Logs), dann minimal fixen
- DoD: RUN startet zuverlässig aus Tree-Selection, nicht Intake; vollständiger Run-Context; sichtbarer rc/Report.
- [ ] (P3) [PROD] Per-Tab Audit: Artefakte (Tree/Preview), Intake, Runner Products etc. – Abweichungen dokumentieren (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L93)
- Regel: Erst Proof, dann Skalierung
- Header-Fix: toolbar_runner_exec.py (R8402)
- Diagnose zuerst, dann minimaler APPLY, dann Stop (kein Fix-Cascade).
- Keine Refactors (Popup/Output/Toolbar) ohne Plan.
- [ ] Left/Right (Paned) korrekt: paned.add(...), keine left/right.pack(...) Restlinien.
- [ ] Rechte Seite wieder aufbauen: Tree/Toolbar/OutputDisplay wieder einhängen.
- Patch Assistant (1-Fix Rule Enforcer)

### PROJECT: Push / Purge / Action Cluster

- [ ] (P0) (AFTER DISPO V1.0) FIX: Push + Purge Buttons ohne Funktion (Verdrahtung/Action-Routing defekt)
- Push ruft action_autopush_both (Autopush Both) auf
- Purge ruft action_purge_one auf
- Symptom: Buttons *Push* und *Purge* reagieren nicht / keine Aktion.
- Hypothese: UI-Action Verdrahtung/Dispatch/Registry-Map zeigt ins Leere.
- Repo/Registry/Action-Routing in eigene Module ausgelagert (testbar)
- Push/Purge bleiben funktional (keine Verluste)
- [ ] Push uses executor, Purge uses executor
- [ ] One Push button + one Purge button in code (no duplicates)
- Slot-Tabelle robust referenzieren (t_SLOTS vs t_DISPO_Slots) – keine harten Namen ohne Fallback.

### PROJECT: Smoke / Runner / Start Cluster

- [ ] Smoke-Runner: smoke_min (Start/Import/GUI sanity, Exit-Codes, Report)
- [ ] Pre-Start Gate: Import/Syntax/Smoke vor GUI-Work (Reportpflicht)
- DoD: Protected-Liste + Infra-Runner-Template (Backup/Diff/Gate/Smoke) + MR-Verweis.
- Smoke-Test/Import-Check Runner vorhanden
- python -c "import modules.ui_toolbar" (und optional GUI-smoke, wenn vorhanden)
- [ ] (P2) [PROD] Incremental Refactor Plan: Schrittfolge ohne Vollrewrite (1 Modul pro Runner, jeweils compile+smoke) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L94)
- [P0] Smoke-Test Routine: (1) Import-Check (R8502) (2) GUI-Start (3) RUN (dry)
- [P1] Debug Output: SSOT root/debug_output.txt + GUI Log-Tab/View (statt Runner-Popup)
- Systemstatus (GUI, Runner, Compile, Git)
- [ShrimpDev] Auto Test Runner — Smoke-/Regressions-Checks standardisieren.

### PROJECT: Auto / Generator / Comparison Cluster

- [P1] Auto Comparison Table Generator — Erzeugt Vergleichstabellen aus Produktdaten; Hugo-ready.
- [ ] (P2) LearningJournal 2.0 (Auto-Learn aus Fehlern)
- [ ] (P1) Auto-Runner Generator (KI-basiert)
- Auto Documentation Generator
- Auto Vergleichstabellen Generator
- Comparison Matrix Generator
- [ ] (P2) [STRAT] Auto Comparison Table Generator
- [Web] Auto Update Produktdaten — Pflegeaufwand senken, Aktualität erhöhen.
- Auto Comparison Table Generator
- Auto-Runner Generator (KI-basiert)

### PROJECT: Shrimpdev / System / Runner Cluster

- [P2][IDEA] ShrimpDev Runner DNA System (Analyse erfolgreicher Runner-Strukturen → Best Practices)
- [ ] (P1) Project DNA System (Ziel / Aufwand / ROI)
- [ShrimpDev] Runner Failure Analyzer — Systematische Analyse fehlgeschlagener Runner.
- [ShrimpDev] Runner Generation AI — Runner nach Template schneller erzeugen.
- [ShrimpDev] Runner Replay System — Ausführungen wiederholbar und diagnostizierbar machen.
- [ShrimpDev] Code Metrics System — Hilfreich, aber nicht der erste Schmerzpunkt.
- [ShrimpDev] ShrimpDev Plugin System — Spannend, aber architekturell schwerer.
- [IDEA] ShrimpDev Runner DNA System (Analyse erfolgreicher Runner-Strukturen → Best Practices)
- ShrimpDev Runner DNA System (Analyse erfolgreicher RunnerStrukturen → Best Practices)

### PROJECT: Todo / Implement / Logic Cluster

- todo implement logic here _(Vorkommen: 2)_
- L427 | Lane F: - [ ] (P3) [CORE] TODO: implement logic here (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L15280)
- L463 | Lane F: - [ ] (P3) [CORE] TODO: implement logic here (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_943_NewRunner.py:L49)
- todo list add a high priority item about tracebacks in log _(Vorkommen: 2)_
- todo pipeline eigener gui tab masterrules viewer open refresh n _(Vorkommen: 2)_
- todo pipeline sondern bekommen einen eigenen tab _(Vorkommen: 2)_
- [ ] (P3) [CORE] TODO: implement logic here (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/docs/Report_R2383_Docking_Diagnose_20251219_101914.md:L15280)
- [ ] (P3) [CORE] TODO: implement logic here (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/Archiv/Runner_943_NewRunner.py:L49)

### PROJECT: Runner / Docs / Files Cluster

- [ ] Nachsorge-Runner immer: Backups + Report + marker-basierte Docs-Updates
- R2374 / R2375 / R2377 / R2378 are referenced historically (docs/pipeline), but no active runner files were found in the repo scan.
- R2379 exists as tools runner files, but other references are largely docs/reports.
- [x] (DONE) Docs: Runner Architecture – Lessons Learned (R3346)
- Nachsorge-Plus: Runner-Schutz und modulare Ablösung
- [P0] Doc–Code Drift Checker — Checks: Docs vs. Realität (Files/Module/Runner/Maps) + Report.
- DOCS-Runner: keine festen Pfadannahmen für Pipeline-Dateien → bevorzugt docs/PIPELINE.md, sonst robust suchen.

### PROJECT: Diag / First / Codex Cluster

- [ ] Runbook: docs/CODEX_RUNBOOK.md (No-Gos: keine Rewrites, DIAG first, max 1 Fix, Smoke Pflicht)
- [ ] Runner-Set (cmd+py): codex_readonly, codex_diag, codex_fix_one
- [ ] Diagnose zuerst erzwingen: Wenn Fix nicht beim 1. Versuch verifiziert → Diagnose-Runner Pflicht
- Header-Fix-Pattern verifiziert: Wenn from future import annotations nicht „first statement“ ist → separater Header-Fix-Runner zuerst, dann eigentlicher Patch.
- DIAG-first: echten Run-Flow auflösen (welche Funktion wird vom Run-Button wirklich aufgerufen?).
- [ ] Danach: RUN Button wiring DIAG → 1 Fix → Funktionstest (cmd/py Dispatch).
- Auto-DIAG Engine (Codex-driven)

### PROJECT: Productivity App Suite

- [P2] Subscription Tracker/Canceller (App) — Abo-Erkennung + Reminder vor Verlängerung.
- [ ] (P3) [STRAT] Subscription Tracker
- [App] Shopping Price Tracker — Preisbeobachtung ist massentauglich.
- [App] Subscription Tracker — Viele Nutzer, klarer Schmerzpunkt.
- [App] Aquarium Parameter Tracker — Sehr passend, aber eher Nischenprodukt.
- [App] Minimal Habit Tracker — Einfach, aber stark besetzter Markt.
- [App] Plant Care Reminder — Nische, aber passend zu deinen Themen.

### PROJECT: ShrimpDev Stability Suite

- Sicherheit: Allowlist + Dry-Run/Preview; niemals destructive Runner ohne explizite Bestätigung.
- Sicherheit: Allowlist erlaubter Runner + Dry-Run/Preview + Abbruch/Undo.
- Verify-Runner ohne Crash
- [P0] Runner Simulation Mode (Dry-Run) — Runner laufen ohne echte Änderungen; reduziert Risiko/Drift.
- Keine Registry-/Allowlist-Annahmen (runner_ids = SSOT via Konstanten)
- Runner Heatmap (Error/Run Frequency Analyse)
- [ ] (P1) [CORE] Runner Simulation Mode (Dry Run)

### PROJECT: Strat / Portfolio / Definieren Cluster

- [ ] (P1) [STRAT] Website-Portfolio: Scope definieren (viele kleine Sites, kein Monolith)
- [ ] (P1) [STRAT] Website-Portfolio: Domain-Strategie festlegen (1 Domain pro Nische)
- [ ] (P1) [STRAT] Website-Portfolio: Erfolgskriterien Phase 1 definieren (Indexierung/Impressions)
- [ ] (P1) [STRAT] Website: Priorisierungsmatrix definieren (Volumen × Konkurrenz × Monetarisierung)
- [ ] (P2) [STRAT] Website-MVP: Minimale Seitenstruktur definieren (Start + 1–3 Kernseiten)
- Website-Portfolio-Strategie (viele kleine vs. wenige große)

### PROJECT: Repo / Public / Runner Cluster

- [ ] (P2) Public/Private Repo Audit-Rhythmus definieren (z. B. alle 10 Runner oder wöchentlich): „was darf public / was nie“
- Runner-Presence / Pfad / Repo-Root / keep-file / Busy-Guard blockiert
- Private Repo Root: per UI „…“-Button auswählbar, in INI gespeichert
- [ ] INI: [Repo] private_root, [Repo] public_root, [Repo] public_autocreate
- The public repo is not a mirror. It is a curated export.
- Any policy breach triggers a repair runner that sanitizes the public repo.

### PROJECT: Standard / Soll / Bleibt Cluster

- [ ] RUN soll ausführen, nicht Generator eskalieren (cmd+py Standard bleibt)
- DoD: neu, klein, stabil: run(cmd, args, cwd) + logging + rc; optional threading sauber getrennt; Smoke-Tests.
- .cmd ist Standard-Runnerformat (keine .bat).
- [ ] (P1) DIAG-Standard vereinheitlichen (SOLL/IST, Ursachen, Next Steps, Pfadchecks)
- DoD: keine Runner-Startlogik direkt im UI; 1 definierte run_runner(...)-Entry; UI bleibt responsiv.
- Diagnose-first: Fairness-Run soll 3 Zahlen loggen (Rows gelesen / Keys gezählt / PlanDate serial).

### PROJECT: Crash / Analyzer / Replay Cluster

- [P1] Crash Replay / Crash Chain Analyzer — Crash-Ketten nachvollziehen, Wiederholungsquote, Hotspots.
- [ ] (P1) Crash Analyzer (Logs clustern + Ursachen)
- Crash Replay System
- Crash Timeline Analyzer
- [ ] (P2) [CORE] Crash Replay Analyzer
- [ShrimpDev] GUI Crash Replay — Crashes reproduzierbar machen statt raten.

### PROJECT: Runner / Wenn / Archived Cluster

- Wenn Runner-Artefakte fehlen: Phantom/Archived taggen (bestehende Regel beibehalten).
- Rule: *Pipeline items with missing runner artifacts must be tagged as Phantom/Archived until materialized.*
- Goal: Wenn Runner einen Report erzeugen, soll der Report im Runner-Popup direkt nutzbar sein.
- [ ] (P1) [CORE] CI: Reports wieder als GitHub Actions Artefakte anzeigen (Runner R2656)
- [ ] Phantom runner references: must be tagged/archived until materialized (already started)
- [ ] Nur wenn bestehende Module ohnehin angefasst werden

### PROJECT: Local AI Tool Suite

- [ ] (P3) [CORE] Digital Declutter — File Cleanup Tool (ShrimpDev Integration möglich)
- [ ] (P3) [CORE] SecondBrain Lite — Minimal Tracking (LJ Integration möglich)
- [ShrimpDev] Codex Integration Manager — Codex-Nutzung strukturieren statt Bastelbude.
- [ShrimpDev] Runner Benchmark Tool — Runner-Laufzeiten und Flaschenhälse sichtbar machen.
- [Tool] Local File Search AI — Starkes Tool, aber höherer Aufwand.

### PROJECT: Clarivoo Affiliate Engine

- [ ] (P3) [STRAT] DealRadar — echte Deals mit Preisverlauf + Affiliate
- [ ] (P3) [STRAT] FoodOptimizer — Zutaten → Rezept (Content + Affiliate)
- [ ] (P3) [STRAT] Was lohnt sich heute — Mikro-Entscheidungs-App (lokal + Affiliate)
- [ ] (P3) [STRAT] QuickSite Builder — 1-Klick Affiliate Seiten (Langfrist-Plattform)
- [ ] (P3) [STRAT] Affiliate Keyword Finder

### PROJECT: ShrimpDev Stability Suite

- [ ] Anchor-Patch Prinzip: 1 Runner = 1 klarer Fehler, keine Multi-Patches
- Prinzip: UI delegiert ausschließlich an modules/toolbar_runner_exec.py (Single Source of Truth).
- [P0] Compile-Gate-Pflicht für UI-Patch-Runner (python -m py_compile ...)
- [ShrimpDev] Runner Risk Scanner — Bewertet Patch-Risiko vor Ausführung.
- [ShrimpDev] Runner-Abhängigkeitsgraph — Zeigt Abhängigkeiten und Patch-Auswirkungen.

### PROJECT: Auto / Engine / Evergreen Cluster

- [P2] Auto FAQ Builder + Internal Linking Engine — FAQ/Interlinking automatisch; Evergreen-Refresh.
- [P2][IDEA] Clarivoo Evergreen Engine (evergreen Kategorien identifizieren & priorisieren)
- Auto-Workflow Builder
- Evergreen Auto-Refresh (Preis/Verfügbarkeit)
- Auto-Content Engine (CRITICAL)

### PROJECT: Converter / Playlist / Universal Cluster

- [P2] Universal Playlist Converter (App) — Playlist-Transfer zwischen Streamingdiensten.
- Playlist Converter (HIGH POTENTIAL)
- [ ] (P3) [STRAT] Universal Playlist Converter
- Playlist Converter
- [App] Playlist-Converter zwischen Musikdiensten — Starker Nutzerbedarf, hoher Nutzen, attraktives Tool/App-Thema.

### PROJECT: Compile / Gate / Blockierend Cluster

- A-P0-02: Compile-Gate blockierend vor RUN & APPLY (Code)
- NEXT (P0): Compile-Gate Pflicht bei jedem GUI-Patch (py_compile + Report).
- [ ] log report path and exit code (no Tk callback explosions)
- Smoke-Test RUN (DirectRun + Compile-Gate)
- [P0] Compile-Gate: zusätzlicher Guard “broken try/except/finally” (blockierend rc=7) – zentral, eine Stelle

### PROJECT: Tool / Smart / Screenshot Cluster

- Smart Screenshot Tool
- Screenshot to Markdown Dokumentation Tool
- Smart Backup Diff Tool
- [Tool] Screenshot to Code Extractor — Nützlich, aber fehleranfällig.
- [Tool] Smart Backup Diff Tool — Passt direkt zu deinem Arbeitsstil.

### PROJECT: Fairness / Snapshot / Final Cluster

- [ ] (P0) A: Fairness/Snapshot stabilisieren (Ursache final isolieren, kein Trial-&-Error)
- Frage: Warum werden Fairness-Punkte nicht gutgeschrieben, obwohl Snapshot gefüllt ist?
- Fairness war leer, obwohl Planungen korrekt liefen (Status=OK, Final_ID gesetzt).
- Fairness Delta: t_Fairness_Day (Snapshot) → t_Fairness (Totals)

### PROJECT: Local AI Tool Suite

- [ ] (P2) [CORE] Local API Tester GUI — Leichtgewichtige lokale Test-GUI für APIs/Endpoints.
- [ ] (P1) Lokale KI Integration (Ollama API Bridge)
- [Tool] Local AI Knowledge Base — Großes Potenzial für Suche und Wissen.
- [Tool] Local Prompt Library Manager — Hilfreich für KI-Workflows.

### PROJECT: Excel Productivity Suite

- [ ] (P3) [CORE] JobHelper — Excel Automation Tools (Monetarisierung schnell möglich)
- Excel Tools Sales (DISPO/ASM)
- Excel Automation Toolkit
- [Business] Excel Tools Marketplace — Sehr passend, braucht aber Angebotsreife.

### PROJECT: ShrimpDev Stability Suite

- [ ] Crash-Heatmap, Wiederholquote, Zeit-of-Pain
- [P2][IDEA] ShrimpDev Crash Heatmap (häufigste Crashes nach Modul/Runner/Zeit)
- [IDEA] ShrimpDev Crash Heatmap (häufigste Crashes nach Modul/Runner/Zeit)
- ShrimpDev Crash Heatmap (häufigste Crashes nach Modul/Runner/Zeit)

### PROJECT: Runner / Actions / Push Cluster

- [ ] Kritische Runner absichern: Wiederherstellung + Schutzregeln (z. B. T666 & Co.)
- DoD: DoD & Runner-Sequenzen klar; P0 Lane A hat Vorrang.
- ✅ P6P/P&P Buttons stabil (Push/Purge): Bridge→logic_actions→runner_exec, PP_DIAG entfernt. (Nachsorge: Report_R8651_20260216_233513.md)
- DoD: Push & Purge lösen zuverlässig die korrekten Runner/Actions aus (inkl. Report-Popup gemäß Standard).

### PROJECT: Productivity App Suite

- [App] Idea Capture App Offline First — Passt zu deinem Stil, aber kein Top-Schmerzpunkt.
- [App] Minimalist To-Do App ohne Cloud — Klares Versprechen, aber viele Wettbewerber.
- [App] Receipt Scanner and Budget — Nützlich, aber umkämpfter Bereich.
- [Tool] Offline Notes mit Git Sync — Interessant, aber nicht oberste Baustelle.

### PROJECT: Runner / Graph / Dependency Cluster

- [P1] Runner Dependency Graph — Visualisiert Abhängigkeiten/Impact von Runnern.
- Dependency Graph Viewer
- [ ] (P2) [CORE] Runner Dependency Graph
- [ShrimpDev] Runner Impact Map — Welche Dateien besonders oft verändert werden.

### PROJECT: Shared / Organizer / Household Cluster

- [P2] Shared Household Organizer (App) — Familienkalender + Aufgaben + Einkaufsliste.
- [ ] (P3) [STRAT] Shared Household Organizer
- [App] Einfacher Shared-Family-Kalender — Breit verständlicher Nutzen, gute Alltagstauglichkeit.
- [App] Screenshot Organizer — Praktisch, aber mittlere Priorität.

### PROJECT: Clarivoo / Radar / Money Cluster

- [P2][IDEA] Clarivoo Money Radar (Trends/Suchintention → Content-Priorisierung)
- [ ] (P2) Clarivoo Content Factory (Batch Seiten)
- [IDEA] Clarivoo Money Radar (Trends/Suchintention → Content-Priorisierung)
- Clarivoo Money Radar (Trends/Suchintention → ContentPriorisierung)

### PROJECT: Analysis & Insight Toolkit

- [Tool] Project Dependency Visualizer — Nützlich im Dev- und Analyse-Kontext.
- [Tool] AI-Code Explain Tool — Praktisch für Analyse und Onboarding.
- [Tool] CSV to Dashboard Generator — Praktisch, besonders im Office-Kontext.
- [Tool] Terminal Command History Search — Hilfreich für Dev-Workflows.

### PROJECT: Agent / Runner / R1802 Cluster

- [x] (DONE) Agent-Tab Empfehlungen stabilisiert: R2086 baseline/delta + R1802 Stamp (Agent_LastDiag.json) + robust anchors (R3837–R3844).
- Verwandtschaft: Agent-Tab konsumiert diese Vorschläge (anzeigen, filtern, erklären) und führt Runner nur opt-in aus.
- Idee: Agent-Tab, der auf Basis von Zustand/Logs/Reports Runner vorschlägt.
- Agent-Tab: Empfohlene Runner automatisch vorschlagen und optional (bewusst) ausführen lassen; Sinn/Nutzen prüfen.

### PROJECT: Write / Docking / Writer Cluster

- [x] (DONE) APPLY: module_docking cfg.write(f) -> ini_writer.write() (R3354)
- [x] (DONE) APPLY: config_loader INI writes -> ini_writer.write() (R3349)
- Docking incident resolved (legacy INI state).
- modules/module_docking.py: DockManager.persist_all() führt keinen finalen Write/Commit aus (Legacy/Fragment; kein zuverlässiger Save).

### PROJECT: Main / Buttons / Exceptions Cluster

- [x] (P0) [CORE] main_gui.py Stabilität: Silent-Exceptions sichtbar gemacht (R3333; DIAG: R3331/R3332)
- NEXT (P0): GUI-Integration Codex-Buttons über Anchors (kein main_gui Wild-Patching).
- Production layer (must be syntactically clean): modules/, main_gui.py (und nur ausdrücklich freigegebene Prod-Tools)
- [P0] Safe UI-Polish (Spacing/Alignment/Buttons) ohne große Block-Rewrites in main_gui.py

### PROJECT: Clarivoo Content Engine

- Artefakte: jede Site lebt unter docs/websites/<site>/... (Decision, MVP, KPIs, Kill/Scale).
- Kill-Kriterien für Websites (wann beenden?)
- Generator/Exporter aus docs/websites/pages
- [ ] (P2) Decision Websites (Produktentscheidungen)

### PROJECT: Clarivoo Content Engine

- Content-Skeleton-Generator
- [ ] (P2) KI Content Generator
- [Web] Automatische Pros/Cons Generator — Skalierbare Content-Bausteine.
- KI Content Generator

### PROJECT: Runner / Mode / Execution Cluster

- Define return contract / capture-mode for runner execution:
- [ ] (P2) Execution Engine (Idee → Runner-Kette)
- Runner Simulation Mode
- Runner Sandbox Mode

### PROJECT: Clarivoo Affiliate Engine

- Monetarisierungs-Reihenfolge (Affiliate → Own Product → Bundle)
- [Web] Affiliate Product Comparison Generator — Klarer Hebel für Content-Produktion und Monetarisierung.
- Affiliate Product Comparison Generator
- MonetarisierungsReihenfolge (Affiliate → Own Product → Bundle)

### PROJECT: Clarivoo Affiliate Engine

- Naming- & Branding-System für Sites
- [P2] Log Analyzer Tool — Fehlercluster & Muster; hilfreich für Support/QA.
- [ShrimpDev] System Stability Score — Messbarer Gesundheitswert für das Gesamtsystem.
- [Business] AI Generated Product Comparison Sites — Starker Hebel für Clarivoo-ähnliche Systeme.

### PROJECT: Shrimpdev / Doku / Monetarisierung Cluster

- Priorität: ShrimpDev-Stabilität + Reproduzierbarkeit + Doku gehen vor Monetarisierung.
- [ShrimpDev] Bug Prediction System — Risikobereiche vor dem nächsten Fehler erkennen.
- [ShrimpDev] Documentation Auto-Updater — Pflicht-Doku konsistent nachziehen.
- [Business] ShrimpDev Pro Version — Monetarisierung nach stärkerer Produktreife.

### PROJECT: Konkurrenz / Suchlücken / Check Cluster

- [ ] (P1) [STRAT] Website: Suchlücken-Check (Suchintention + Konkurrenz grob bewerten)
- [ ] (P2) WE-04: “Suchlücken”-Validierungscheckliste (Suchintention, Konkurrenz, Monetarisierung, Aufwand)
- [ ] (P2) WE-11: Top 3 Nischen validieren (SERP-Check, Konkurrenz grob, Monetarisierungsweg)

### PROJECT: Review / Analyzer / Strat Cluster

- [ ] (P2) [STRAT] Review Analyzer — Vor- und Nachteile aus Bewertungen konsolidieren.
- [P1] Review Analyzer (Pros/Cons Extractor) — Aggregiert Reviews, extrahiert häufige Vor-/Nachteile.
- [ ] (P2) [STRAT] Review Analyzer (Pros/Cons Extractor)

### PROJECT: Shrimpdev / Prüfen / Planen Cluster

- [ ] (P2) Automatisierungskonzept: ShrimpDev-gestützt planen/tracken; später Trigger/Deploy prüfen (Hosting: netcup)
- [ ] (P1) [PROD] ShrimpDev: Artefakte-Tab prüfen/reaktivieren, falls Anzeige fehlt
- [ShrimpDev] Runner Registry Explorer — Runner-Bestand leichter durchsuchen und prüfen.

### PROJECT: Statt / Rejected / Decision Cluster

- [ ] (P2) Decision-/Rejected-Ideas-Log minimal pflegen (1 Satz „warum nicht“ statt Vergessen)
- [ ] Adapter statt Rewrite (Mastermodus: minimal-invasiv, rueckbaubar)
- [ ] (P2) Decision Log (Rejected Ideas Tracking)

### PROJECT: Folder / Tool / Organizer Cluster

- [ ] (P2) Folder Organizer Tool
- [Tool] Auto Folder Organizer — Guter Nutzen, mittlere Priorität.
- [Tool] Folder Size Visualizer — Praktischer Utility-Fall.

### PROJECT: Call / Site / Diag Cluster

- [ ] Call-Site DIAG: echten Intake-Builder finden (Name/Ort/Signatur) + Call-Sites belegen
- call_action(app, name) robust + logging
- 2026-02-28 00:21 Nachsorge R9107: Stabilisierung/Backups + SyntaxGate. Drift-Risiko bestätigt; nächster Schritt: Call-Site-DIAG für Intake-Builder (kein Raten nach _build_intake).

### PROJECT: Clipboard / Manager / Universal Cluster

- [P2] Clipboard History Manager Pro — Kategorie/Favoriten/Suche; offline.
- Universal Clipboard Manager
- [Tool] Universal Clipboard Manager — Solider Utility-Fall, aber nicht vorn.

### PROJECT: Shrimphub / Storyboard / Autovideo Cluster

- [P2][IDEA] ShrimpHub Storyboard → AutoVideo Pipeline (Script/Szenen/Prompts/VO/Struktur)
- [IDEA] ShrimpHub Storyboard → AutoVideo Pipeline (Script/Szenen/Prompts/VO/Struktur)
- ShrimpHub Storyboard → AutoVideo Pipeline (Script/Szenen/Prompts/VO/Struktur)

### PROJECT: 20260112 / Verified / R3302 Cluster

- [x] (P1) [CORE] Docking: Konsolidierung der Undock-Overrides (R3302–R3315) in eine kanonische Implementierung — DONE (verified) (Report_R3397_20260112_224300.md) (Report_R3398_20260112_225641.md)
- P0.A Runner-Execution isolieren: Threading/Subprocess aus ui_toolbar.py hinter eine klare API; UI ruft nur noch Orchestrator auf. — DONE (verified) (Report_R3402_20260112_233849.md) (Report_R3403_20260112_234334.md)
- P1.A Popup/Report-Handling konsolidieren: ein kanonischer Pfad für Report-Anzeige (Push/Purge gemäß Standard). — DONE (verified) (Report_R3393_20260112_221547.md) (Report_R3394_20260112_222242.md)

### PROJECT: Arbeitszeit / Schichtarbeiter / Schichtarbeit Cluster

- Arbeitszeit App für Schichtarbeiter
- [App] Arbeitszeit-Rechner für Schichtarbeit — Hohe reale Nachfrage, einfache MVP-Umsetzung, gutes App-Potenzial.
- [App] Scan to Excel — Praktisch für Arbeit und Alltag.

### PROJECT: Automation Toolkit

- Bundles
- Produkt-Bundles
- Tool Bundles

### PROJECT: Minimaler / Apply / Danach Cluster

- Danach erst minimaler APPLY (nur der erste belegte Blocker, keine Rewrites)
- Danach: minimaler Finder-Fix
- Diagnose zuerst, dann minimaler APPLY, dann Stop (kein FixCascade).

### PROJECT: Autopush / R2692 / Deprecated Cluster

- Deprecated: R2692/R2691 legacy autopush runners (workspace-bound). Do not wire GUI buttons to them.
- Autopush reports are generated locally under Reports/ and are not versioned in git.
- [P1] Autopush repo-only finalized: GUI uses R2691/R2692/R2693; legacy R2692/R2691 deprecated; gitignore ignores only Report_R269{1..3}_*.md.

### PROJECT: Only / Docs / Ausnahme Cluster

- DoD: MR-Kapitel mit H1–H7 + H2a (Docs-only Ausnahme).
- [ ] (P3) [CORE] Define Gating Rules (Docs): wann ist Restore sichtbar? wann ist File-Copy erlaubt? (Backup/Archiv-Only, Busy-State) (src:C:/Users/rasta/OneDrive/ShrimpDev_REPO/tools/R2519.py:L91)
- [ ] Add a short “when this warning appears” troubleshooting snippet (docs-only)

### PROJECT: Drift / Code / Scanner Cluster

- Drift Scanner (UI + duplicate code detection)
- Code Drift Prediction
- [ ] (P1) [CORE] Doc-Code Drift Checker

### PROJECT: Clear / Stop / Rechtsbündig Cluster

- Feature: In Suchfeldern rechtsbündig ein ✕ zum Clear/Stop.
- Shortcuts: Esc triggert denselben Clear/Stop; optional Tooltip “Clear”.
- Search-Clear-X: In Suchfeldern rechtsbündig ein X zum Beenden/Leeren der Suche.

### PROJECT: Suchfeld / Durchsucht / Suche Cluster

- Feature: Suchfeld im Log-Tab, das das Log (Textwidget) live/auf Enter durchsucht.
- Scope: Log-Tab (Suche), Pipeline-Tab, weitere Filterfelder nach Bedarf.
- Log-Tab Suche: Suchfeld im Log-Tab, das das Log (Text) durchsucht.

### PROJECT: State / Reports / Scanner Cluster

- Forbidden in public: backups, reports, debug captures, registry/state, internal pipeline, internal master rules, internal journals.
- Erlaubt: gemeinsame Tooling-Runner (Scanner/Generator/Reports) ohne Shared State.
- Erlaubt: gemeinsame ToolingRunner (Scanner/Generator/Reports) ohne Shared State.

### PROJECT: Werden / Markiert / Obsolet Cluster

- oder als obsolet markiert werden.
- Regel: Neue Features und neue GUI-Elemente muessen als Baustein/Snippet umgesetzt werden.
- Nur als potenziell wertvolle Struktur markiert

### PROJECT: Option / Execute / Runner Cluster

- Option: *Auto-Execute* nur opt-in.
- Option 1: New API execute_runner_capture(...) -> (rc, out, err) (or dict).
- Option 2: Extend execute_runner(..., capture=True) with explicit return type.

### PROJECT: Tools / Purge / Keep Cluster

- Purge ist zur Laufzeit gated (bewusst): Button-Enablement hängt u. a. an tools/R2218.cmd|py und Busy-Guard / canonical keep-file checks.
- Purge/Housekeeping ist produktiv: räumt real auf (Archiv statt Delete), Relevanz-Policy aktiv (tools/ zählt nicht als runtime).
- [x] Lane B: UI Purge Guard enforces canonical registry/tools_keep.txt (R3566).

### PROJECT: Path / Repo / Registry Cluster

- read_registry_path(), is_git_repo(), repo_pushable()
- [ ] INI redirects -> trend to zero (canonical path: registry/ShrimpDev.ini, remove hardcoded root INI reads/writes)
- [Tool] Git Repo Cleaner — Praktischer Utility-Charakter für viele Projekte.

### PROJECT: ShrimpDev Stability Suite

- Reports / Diagnose / Logs: 1
- [ ] (P1) [CORE] System Health Dashboard — Stabilitätsmetriken aus Logs, Reports und Crash-Signalen.
- [ ] (P1) [CORE] System Health Dashboard — Stabilitätsmetriken aus Logs/Runner Reports

### PROJECT: Clarivoo Affiliate Engine

- SEO Gap Finder
- [Web] Keyword Gap Finder — Hilft direkt bei SEO-Themenfindung und Skalierung.
- Affiliate Keyword Finder + Competitor Gap Finder

### PROJECT: Calendar / Shared / Smart Cluster

- Shared Smart Calendar
- Shared Family Calendar
- [Business] Micro SaaS Shared Calendar — Interessant, aber größerer Support-/Hosting-Scope.
- [ ] Reports erweitern: Diff-Übersicht, betroffene Dateien, Tests, „Was wurde NICHT geändert“
- [ ] Purge strikt Whitelist (Exact-only), keine Patterns
- [ ] Schutz-Count normalisieren: Ursachen dauerhaft abstellen (Scan-Breite/Doku-Effekt)
- [ ] RunnerExec/DirectRun Regeln dokumentieren + enforced
- [ ] Hot/Cold Modul-Matrix
- [ ] Stabilitäts-Score in GUI
- A-P0-01: RUN wieder funktionsfähig via Direct-Run Bypass
- DoD: Gate läuft automatisch; FAIL ⇒ rc=7; keine Folgepatches.
- A-P1-01: RunnerExec Clean-Rebuild (minimal, testbar)
- A-P1-02: Protected-Files Schutzglas (Infra-Runner only)
- B-P1-01: SSOT-Refactor RUN (Selection-only)
- DoD: alle RUN-Actions holen Context aus Selection; Intake nur Preview/Defaults.
- C-P1-01: Legacy Sweep — BAT-Reste inventarisieren & neutralisieren
- DoD: Report: alle .bat + Referenzen; entfernen/archivieren; keine produktiven Callsites.
- D-P1-01: MR-Update Block “Stop-the-line / Protected / SSOT / Bypass”
- D-P1-02: PIPELINE-Schärfung für diese RUN-Stabi-Serie
- Stand: 2026-02-21 21:12:44
- Tasks gescannt (task-like): 241
- Normalisierte Keys gewertet: 223
- Potenzielle Dubletten (Keys mit >1 Vorkommen): 4
- Governance / MR / Pipeline: 2
- Other: 1
- Pro Dublette: 1 kanonischen Task definieren, Rest als Referenz/Archived markieren oder zusammenführen.
- Historical/architectural items or feature hardening belong to P1/P2.
- Each remaining P0 must state a *crash/start symptom* and a *clear DoD*.
- Treat these as ARCH/HISTORICAL unless we explicitly *materialize* missing runners.
- Pipeline-Markierung via R3348
- gesetzt am 2026-01-12 14:14
- [x] (P1) [CORE] INI Redirect Logging Noise gedrosselt (Callsite-Gating) (R3334)
- Lane A — Stabilität / Crash / Startfähigkeit (P0/P1)
- Lane B — Core Features (P1/P2)
- Lane C — Tooling / Automationen (P1/P2)
- Lane D — Doku / Regeln / Konsistenz (P1/P2)
- [ ] FAIL/WARN/ExitCodes + Keywords clustern (Dedup)
- [ ] Priorität P0–P2 vergeben
- [ ] Ergebnis als Agent-Report schreiben (kein Auto-Schreiben in PIPELINE)
- Optional (kontrolliert, APPLY):
- [ ] „Übernimm Todo #X“ schreibt genau einen Pipeline-Eintrag (dedupe-sicher, Token Pflicht)
- [ ] Runner, die künftig wieder genutzt werden, müssen protected/whitelisted werden
- [ ] (P1) Governance-Schärfung (R3568/R3569): Pipeline-SSOT, Diagnose-first (Enforcement), Runner Scope-Lock, Definition of Done, Stop-Kriterien
- [ ] MR-Block vorhanden (R3568) ✅
- [ ] Pipeline-Tasks vorhanden (R3569)
- [ ] Architektur-Prinzipien ergänzt (R3569)
- [ ] Report vorhanden (R3568 + R3569)
- Lane E — Website / SEO-Netzwerk (P2/P3)
- [ ] (P0) DISPO-Tool V1 stabilisieren (produktiver Einsatz)
- Ziel: V1.0 „daily usable“ ohne Workarounds
- stabile Datenstruktur / klare Tabellen
- Vorschlagslogik stabil (Primär/Sekundär) + reproduzierbar
- Tageswechsel sauber (Neuer Tag / Reset)
- Reset-Mechanismus für neue Mitarbeitende
- 1 Haupt-View (Einteilung), Rest in separaten Tabs
- keine #NAME? / Spill-Fehler / „schreibt sonstwo hin“
- reproduzierbare Ergebnisse (gleiches Input → gleiches Output)
- Bedienung im Alltag: „Klick-Workflow“ ohne Basteln
- Output/Check: Fairness-Delta muss deterministisch sein (gleiches Input → gleiches Ergebnis).
- [ ] (P1) B: Assign/Override/Final-Flow konsolidieren + Orchestrator „Neue Planung“
- Ziel: 1 Klick-Workflow, klare Ownership, keine Side-Writes in Formelspalten.
- [ ] (P1) C: View/Mail finalisieren
- Umlaute/Encoding sauber
- Tasknamen statt IDs
- Layout final
- [x] (DONE) Intake/Intake.py / Runner-Thema fallen gelassen (Nutzerwunsch)
- Markiert am 2026-02-14 08:08:17
- [ ] (P1) Runner-Preflight zentralisieren (python/venv/git/node/rights/root)
- [ ] (P1) FAIL-Report-Header standardisieren (Fail-Reason, Top-3 Ursachen, Next Runner)
- [ ] (P1) Last-Known-Good Marker nach grünem Smoke-Test
- [ ] (P2) Hybrid-Seitenkonzept: plain + hochwertiger Mehrwert-Content (nicht nur Tabellen)
- [ ] (P2) Update-Routine: regelmäßige Content-Aktualisierung (Fälligkeiten, Sichtbarkeit „lebt“)
- [ ] (P3) Security/Controls: strikt nur im Workspace, Report-Gate, keine direkten Änderungen am Haupttree
- Tasks sind pro Lane gruppiert.
- Jede Änderung an Pipeline: Backup + Report.
- docs/PIPELINE.md
- docs/templates/*
- docs/CHANGELOG.md, docs/VERSION.txt
- DONE: R9140 Codex im Runner-Kontext ausführbar (rc=0, codex --version ok).
- UI-Wiring ist vorhanden:
- Exceptions werden best-effort geloggt, aber UX kann „wirkt tot“ aussehen
- ui_toolbar.py wird deutlich dünner (Orchestrator)
- DoD: keine doppelten Popup-Overlays; konsistentes Verhalten.
- Große Cluster zuerst zu echten Projekten zusammenziehen.
- Danach für jeden Cluster einen P0/P1 Sammelpunkt in der Pipeline anlegen.
- Einzelkandidaten später separat priorisieren.

<!-- R9330:PROJECTS:END -->
## Dispo-Tool Release Status

### DONE / RELEASED

`Dispo-Tool 2.0`  
Status: `RELEASE`  
Datum: `2026-03-16`  
Beschreibung: stabile operative Planung

### DONE

- Historienbasis vorbereitet
- SQLite DB erstellt
- Dispo-Tool 3.0 compile stabilisiert

### PAUSED

- Decision History
- Explainability
- Analysefunktionen
- Dispo-Tool 3.0 Ausbau


---

## R9426 Nachsorge

**2026-03-16 22:54:26 – Nachsorge via R9426**

Abgeschlossen / bestätigt:
- Runner-System stabilisiert
- OutputDisplay-Standardpfad aktiv
- Gate-Verhalten transparent
- Purge repariert
- Protected Runner eingeführt
- Intake/Ini-Rebind aktiv
- TreeView Smooth Refresh bestätigt

Nächste sinnvolle Schritte:
1. Tk-after Cleanup
2. R9424 Noise reduzieren
3. optional Gate-UX polish

## R9425 Nachsorge (2026-03-17 14:28:31)

### Stabilisiert
- Runner-Startpfad ist vereinheitlicht.
- `run_by_id(...)` ist zentrale GUI-Startschicht.
- Inflight-Guard blockiert Mehrfachstarts desselben Runners.
- Standard-GUI-Runner laufen popup-frei ins zentrale OutputDisplay.
- Purge-Standardpfad wurde auf den passenden Apply-Runner korrigiert.
- Protected Runner sind zentral definiert und gegen Standard-Purge/Delete abgesichert.

### Neue/aktive Diagnose-Runners
- `R9421` RunnerGuard
- `R9423` SystemHealth
- `R9424` RunnerFailureWatch

### Offene Punkte / nächste sinnvolle Schritte
1. Tk-`after`-Cleanup beim GUI-Destroy sauber machen.
2. R9424 Failure-Signale entrauschen (historische Reports konservativer auswerten).
3. Intake-Auto-Refresh gezielt im echten Dateitest verifizieren.

### Wiedereinstieg
Neuer Fokus-Thread:
**ShrimpDev – Tk-after-Cleanup + R9424 Signal-Noise reduzieren**

---

## 2026-03-17 — Ideensammlung → Pipeline Integration (append-only)

Quelle:
- aktueller Chat-Thread (ShrimpDev / Tools / Automation / Monetization)

Bewertungslogik:
- Impact: 1–5
- Effort: 1–5
- Risk: 1–5
- Priorität:
  - `P0` = hoher Hebel, niedriger bis mittlerer Aufwand, direkt anschlussfähig
  - `P1` = hoher Nutzen, aber etwas breiter oder mit Vorarbeit
  - `P2` = längerfristig / experimentell / später zu schärfen

### Core ShrimpDev

[SD-001] Docs Consistency Check
- Category: Core ShrimpDev
- Priority: P0
- Status: Planned
- Impact / Effort / Risk: 5 / 2 / 2
- Description: Prüft Konsistenz zwischen `PIPELINE`, `FILE_MAP`, `MasterRules`, relevanten Reports und markanten SSOT-Dokumenten.
- Expected Outcome: Weniger Doku-Drift, sauberere Nachsorge, weniger widersprüchliche Arbeitsgrundlagen.
- Next Action: Read-only DIAG-Runner definieren, der nur Abweichungen meldet.

[SD-002] Regression Radar
- Category: Core ShrimpDev
- Priority: P0
- Status: Planned
- Impact / Effort / Risk: 5 / 3 / 2
- Description: Früherkennung für Runner-/GUI-/Compile-/Report-Regressionsmuster.
- Expected Outcome: Wiederkehrende Fehler werden schneller sichtbar und clusterbar.
- Next Action: Auf Basis vorhandener Reports und `R9424` einen konservativen Radar-Report aufsetzen.

[SD-003] Patch / Runner Compliance Gate
- Category: Core ShrimpDev
- Priority: P0
- Status: Planned
- Impact / Effort / Risk: 5 / 3 / 2
- Description: Bündelt Validator-/Compliance-Checks wie Patch-ZIP-Validierung, Template-Compliance, Report-Fehlt-Warnung und verbotene Muster.
- Expected Outcome: Weniger Drift, weniger riskante Runner-/Patch-Ausnahmen.
- Next Action: Bestehende Gate-/Validator-Logik inventarisieren und einen klaren DIAG-Teil definieren.

[SD-004] Idea Inbox Normalizer
- Category: Core ShrimpDev
- Priority: P0
- Status: Planned
- Impact / Effort / Risk: 4 / 2 / 1
- Description: Normalisiert Inbox-Einträge vor Review/Import und reduziert Format-/Statusrauschen.
- Expected Outcome: Sauberere Idee-zu-Pipeline-Verwertung.
- Next Action: `docs/IDEA_INBOX.md` + Spec read-only analysieren und Normalisierungsregeln sammeln.

[SD-005] Codex Call Wrapper Standard
- Category: Core ShrimpDev
- Priority: P0
- Status: Planned
- Impact / Effort / Risk: 4 / 2 / 2
- Description: Standardisiert Codex-Aufrufe, Argumente, Report-Konventionen und Nachsorge-Anbindung.
- Expected Outcome: Weniger Sonderfälle bei Codex-/Runner-Aufrufen.
- Next Action: bestehenden `codex exec`-Einsatz und Runner-Konventionen in einen kleinen Wrapper-Standard überführen.

[SD-006] Runner Explorer UX
- Category: Core ShrimpDev
- Priority: P1
- Status: Idea
- Impact / Effort / Risk: 4 / 3 / 2
- Description: Bündelt Runner-Finder, Last-Report-Zugriff, Protected-ID-Übersicht und ähnliche GUI-Verbesserungen.
- Expected Outcome: Schnellere Navigation im Runner-Bestand.
- Next Action: UI-MVP für Filter + Last-Report-Zugriff abgrenzen.

[SD-007] Pipeline Quick Add
- Category: Core ShrimpDev
- Priority: P1
- Status: Idea
- Impact / Effort / Risk: 4 / 3 / 2
- Description: Schneller Weg aus Thread/Report/Inbox zu einem sauberen Pipeline-Eintrag.
- Expected Outcome: Weniger manuelle Pipeline-Nachpflege.
- Next Action: minimalen Add-Flow definieren, der append-only bleibt.

[SD-008] Command Center View
- Category: Core ShrimpDev
- Priority: P1
- Status: Idea
- Impact / Effort / Risk: 5 / 4 / 3
- Description: Oberflächen-Cluster für Health, Pipeline-Hitze, Runner-Zustand und wichtige Diagnose-Signale.
- Expected Outcome: Höhere Systemtransparenz.
- Next Action: vorhandene Health-/Guard-/Failure-Runner als Datenquellen inventarisieren.

### Tools

[TL-001] Dependency / Change Impact Viewer
- Category: Tools
- Priority: P1
- Status: Idea
- Impact / Effort / Risk: 4 / 3 / 2
- Description: Visualisiert Datei-/Runner-Abhängigkeiten und grobe Change-Impact-Signale.
- Expected Outcome: Sicherere Patches und bessere Scope-Einschätzung.
- Next Action: bestehende Dependency-Ideen und vorhandene Maps bündeln.

[TL-002] Repo Hygiene Toolkit
- Category: Tools
- Priority: P1
- Status: Idea
- Impact / Effort / Risk: 4 / 3 / 2
- Description: Bündelt Dead File Scanner, Runner-Archivierungsregeln und Report-Ablage-/Repo-Hygiene.
- Expected Outcome: Weniger Repo-Rauschen, besserer Überblick.
- Next Action: klare read-only Diagnose-Unterpunkte definieren.

[TL-003] NextFree-ID Wächter
- Category: Tools
- Priority: P1
- Status: Idea
- Impact / Effort / Risk: 3 / 2 / 1
- Description: Prüft freie Runner-IDs und verhindert Kollisionen.
- Expected Outcome: Sicherere Runner-Erstellung.
- Next Action: vorhandene Runner-ID-SSOT und Tools-Scan koppeln.

[TL-004] Output / Log Mirror Hardening
- Category: Tools
- Priority: P1
- Status: Idea
- Impact / Effort / Risk: 4 / 3 / 2
- Description: Konsolidiert Anzeige und Spiegelung zwischen OutputDisplay, Logs und Reports.
- Expected Outcome: Weniger Diagnose-Lücken.
- Next Action: vorhandene Output-Sinks inventarisieren.

### Automation

[AU-001] Pipeline / Nachsorge Automation
- Category: Automation
- Priority: P1
- Status: Idea
- Impact / Effort / Risk: 4 / 3 / 2
- Description: Bündelt automatische Pipeline-Nachpflege, Docs-Sync, Fehlerfälle in Inbox und Thread-zu-Task-Überführung.
- Expected Outcome: Weniger manuelle Nachsorgearbeit.
- Next Action: einen klaren read-only Vorstufen-Runner definieren.

[AU-002] Prompt-to-Runner Engine
- Category: Automation
- Priority: P2
- Status: Later
- Impact / Effort / Risk: 4 / 4 / 3
- Description: Ausbaustufe auf Basis des Codex-Wrapper-Standards.
- Expected Outcome: Schnellere Übersetzung von Anweisungen in Runner-Ketten.
- Next Action: erst nach `SD-005` weiter schärfen.

[AU-003] GUI Binding / Self-Test Audit
- Category: Automation
- Priority: P0
- Status: Planned
- Impact / Effort / Risk: 5 / 2 / 2
- Description: Prüft Buttons, Bindings, Precondition-Fehler und tote GUI-Actions.
- Expected Outcome: Weniger „Button tut nichts“-Regressionsfälle.
- Next Action: read-only Audit-Runner für GUI-Handler und Tree-/Toolbar-Wiring aufsetzen.

### Monetization

[MO-001] Clarivoo Factory
- Category: Monetization
- Priority: P1
- Status: Planned
- Impact / Effort / Risk: 5 / 4 / 3
- Description: Kanonischer Sammelpunkt für produktive Clarivoo-Skalierung und Content-/Vergleichsseiten-Automation.
- Expected Outcome: Klarer Ausbaupfad für Website-/Affiliate-Hebel.
- Next Action: bestehende Clarivoo-Blöcke als einen produktionsnahen Arbeitsstrang konsolidieren.

[MO-002] Excel Rescue AI / Makro-Wiederbelebungs-Toolkit
- Category: Monetization
- Priority: P1
- Status: Planned
- Impact / Effort / Risk: 5 / 4 / 3
- Description: Produkt-/Service-Cluster rund um Excel-/Makro-Rettung und Legacy-Stabilisierung.
- Expected Outcome: Starker B2B-/Service-Hebel mit Anschluss an vorhandene Repo-Kompetenz.
- Next Action: Service-, Toolkit- und Runner-Komponenten als einen realen Angebotsstrang beschreiben.

[MO-003] Services / Productization Portfolio
- Category: Monetization
- Priority: P2
- Status: Later
- Impact / Effort / Risk: 4 / 4 / 3
- Description: Bündelt ShrimpDev Lite, Dokumentationspakete, Migration Services und Toolkit-Angebote.
- Expected Outcome: Späterer Produkt-/Service-Baukasten.
- Next Action: erst nach klareren Kernprodukten schärfen.

### Experimental

[EX-001] ShrimpDev Platform / Intelligence Layer
- Category: Experimental
- Priority: P2
- Status: Parked
- Impact / Effort / Risk: 5 / 5 / 4
- Description: Sammelpunkt für Auto-Medic, Smart Suggestions, Platform-/OS-/Knowledge-System-Ideen.
- Expected Outcome: Visionärer Ausbaupfad ohne aktuelle Überlastung der Pipeline.
- Next Action: vor echter Planung einen engen ersten Scope definieren.

[EX-002] Mobile / Companion App Portfolio
- Category: Experimental
- Priority: P2
- Status: Parked
- Impact / Effort / Risk: 3 / 4 / 3
- Description: Bündelt die App-/Companion-Ideen aus dem Thread.
- Expected Outcome: Ideen bleiben erhalten, ohne die Kernpipeline zu verstopfen.
- Next Action: erst bei klarer Kapazität oder Produktstrategie schärfen.

### Runner-Kandidaten für P0
- `SD-001` Docs Consistency Check -> Diagnose-Runner
- `SD-002` Regression Radar -> Diagnose-Runner
- `SD-003` Patch / Runner Compliance Gate -> Diagnose-/Gate-Runner
- `SD-004` Idea Inbox Normalizer -> Diagnose-/Normalizer-Runner
- `SD-005` Codex Call Wrapper Standard -> kleiner infra-/wrapper-Runner
- `AU-003` GUI Binding / Self-Test Audit -> Diagnose-Runner

---

## 2026-03-17 — Ideensammlung aus aktuellem Thread (append-only)

### P0

**Docs Consistency Check**
- Kategorie: Core ShrimpDev
- Priorität: P0
- Kurzbeschreibung: Prüft wichtige SSOT-Dokumente und markante Projektpfade auf erkennbare Widersprüche oder fehlende Nachpflege.
- Erwarteter Nutzen: Weniger Doku-Drift und klarere Arbeitsgrundlagen.
- Nächster sinnvoller Schritt: Read-only Prüfumfang und klare Vergleichsquellen definieren.

**GUI Consistency Checker**
- Kategorie: Core ShrimpDev
- Priorität: P0
- Kurzbeschreibung: Prüft zentrale GUI-Bindings, Buttons, Tree-/Output-Zustände und offensichtliche Verdrahtungsdrift.
- Erwarteter Nutzen: Frühere Erkennung von UI-/Wiring-Fehlern.
- Nächster sinnvoller Schritt: Kanonische GUI-Hotspots und erwartete Handlerlisten festlegen.

**Report Aggregator**
- Kategorie: Tools
- Priorität: P0
- Kurzbeschreibung: Bündelt wichtige Reports in einer nutzbaren Übersicht mit Status- und Trendfokus.
- Erwarteter Nutzen: Schnellere Lagebeurteilung und weniger Report-Suche.
- Nächster sinnvoller Schritt: Minimalen Aggregationsumfang und Zielansicht festlegen.

**Runner Health Dashboard**
- Kategorie: Automation
- Priorität: P0
- Kurzbeschreibung: Verdichtet Runner-Zustand, Compile-/Gate-Signale und grobe Failure-Hinweise in einer kompakten Health-Sicht.
- Erwarteter Nutzen: Höhere Transparenz über den Zustand des Runner-Systems.
- Nächster sinnvoller Schritt: Vorhandene Diagnose-Runner und ihre Signale als Datenquellen inventarisieren.

**Pipeline Auto-Priorizer**
- Kategorie: Automation
- Priorität: P0
- Kurzbeschreibung: Hilft dabei, neue Ideen oder Befunde anhand einfacher Heuristiken priorisiert in die Pipeline zu überführen.
- Erwarteter Nutzen: Weniger manuelle Priorisierungsarbeit und konsistentere Pipeline-Einträge.
- Nächster sinnvoller Schritt: Kleine Scoring-Regeln für Impact / Aufwand / Risiko definieren.

### P1

**Runner Impact Preview**
- Kategorie: Tools
- Priorität: P1
- Kurzbeschreibung: Gibt vor einem Runner-Lauf einen groben Eindruck, welche Bereiche/Artefakte wahrscheinlich betroffen sind.
- Erwarteter Nutzen: Bessere Scope-Klarheit vor riskanteren Läufen.
- Nächster sinnvoller Schritt: Bestehende Runner-Metadaten und Reports auf wiederverwendbare Signale prüfen.

**Error Pattern Finder**
- Kategorie: Automation
- Priorität: P1
- Kurzbeschreibung: Sucht in Reports und Ausgaben nach wiederkehrenden Fehlermustern.
- Erwarteter Nutzen: Schnellere Clusterung häufiger Probleme.
- Nächster sinnvoller Schritt: Einfache, konservative Pattern-Liste definieren.

**Quick Restore Tool**
- Kategorie: Tools
- Priorität: P1
- Kurzbeschreibung: Unterstützt schnelle Wiederherstellung aus klar definierten Sicherungs-/Restore-Pfaden.
- Erwarteter Nutzen: Weniger Reibung bei kleinen Rücknahmen.
- Nächster sinnvoller Schritt: Tatsächlich vorhandene Backup-/Restore-Quellen sauber inventarisieren.

**Task -> Runner Generator**
- Kategorie: Automation
- Priorität: P1
- Kurzbeschreibung: Leitet aus gut formulierten Aufgaben einen standardisierten Runner-Startpunkt oder Runner-Stub ab.
- Erwarteter Nutzen: Schnellere Operationalisierung wiederkehrender Aufgaben.
- Nächster sinnvoller Schritt: Minimalen Zielumfang für generierbare Runner-Strukturen definieren.

**Repo Cleaner Pro**
- Kategorie: Tools
- Priorität: P1
- Kurzbeschreibung: Erweiterte Repo-Hygiene für Altdateien, Reports, Runner-Reste und ähnliche Aufräumfälle.
- Erwarteter Nutzen: Weniger Repo-Rauschen und besserer Überblick.
- Nächster sinnvoller Schritt: Klaren read-only Diagnose-Modus als erste Stufe definieren.

### P2

**Digital Twin**
- Kategorie: Experimental
- Priorität: P2
- Kurzbeschreibung: Gedankliches Modell eines beobachtbaren Spiegelbilds des Systems für Zustands- und Strukturtransparenz.
- Erwarteter Nutzen: Langfristig bessere Übersicht über komplexe Zusammenhänge.
- Nächster sinnvoller Schritt: Erst einen sehr kleinen beobachtbaren Kern-Scope definieren.

**Auto-Healer**
- Kategorie: Experimental
- Priorität: P2
- Kurzbeschreibung: Vision für automatisierte, konservative Selbstheilungs- oder Korrekturvorschläge.
- Erwarteter Nutzen: Langfristig weniger manuelle Nachsorge.
- Nächster sinnvoller Schritt: Zuerst nur Diagnose-/Vorschlagsmodus statt Auto-Fix denken.

**Local AI Brain**
- Kategorie: Experimental
- Priorität: P2
- Kurzbeschreibung: Lokaler Wissens- und Entscheidungskontext für Repo, Runner, Reports und Ideen.
- Erwarteter Nutzen: Langfristig bessere Wiederverwendung von Repo-Wissen.
- Nächster sinnvoller Schritt: Bestehende lokale Wissensquellen und minimalen Nutzenfall benennen.

**Code-zu-Geld-Mapper**
- Kategorie: Monetization
- Priorität: P2
- Kurzbeschreibung: Verknüpft technische Assets, Runner oder Tools mit realistischen Monetarisierungswegen.
- Erwarteter Nutzen: Klarere Brücke zwischen Technik und Produkt-/Service-Hebel.
- Nächster sinnvoller Schritt: Einfache Mapping-Kategorien für Tool / Service / Produkt / Website definieren.

**Dead Code Reanimator**
- Kategorie: Experimental
- Priorität: P2
- Kurzbeschreibung: Idee für konservative Wiederbelebung oder Neubewertung stillgelegter, aber potenziell wertvoller Artefakte.
- Erwarteter Nutzen: Nützliche Altteile gehen seltener verloren.
- Nächster sinnvoller Schritt: Klare Grenze zwischen Archiv, Restore und produktivem Re-Use definieren.
