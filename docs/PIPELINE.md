# ShrimpDev Pipeline (KANONISCH)

> Diese Datei ist die **Single Source of Truth** für alle offenen Aufgaben.
> Regeln:
> - Neue Tasks **nur hier** eintragen.
> - Jede Aufgabe hat Priorität: **P0 (Blocker)**, **P1 (High)**, **P2 (Medium)**, **P3 (Später)**.
> - “Done” nur im Abschnitt **Done/Archive** führen.
> - Wenn etwas doppelt erscheint: **nur hier konsolidieren**, nicht parallel in Notes/Reports pflegen.

---

## Status
- Aktueller Root (kanonisch): `C:\Users\rasta\OneDrive\ShrimpDev`
- D:\ShrimpDev bleibt als Ablage/Altbestand bestehen, **aber nicht** als Arbeitsbasis.

---

# P0 — Blocker / Highest

## EPIC: INI Single Writer (BLOCKER)
**Ziel:** 1 Writer/Entry-Point, stabile WriteMap, deterministisches Schreiben, keine Seiteneffekte.

**Phase 1 — Diagnose / Read-only**
- [ ] R2371: WriteMap-Report (READ-ONLY)
- [ ] Konsolidierungs-Report(s) prüfen: `docs/INI_WriteMap.md` / relevante Reports

**Phase 2 — Architektur/Design**
- [ ] R2372: Architecture INI Single Writer (Designfinalisierung)

**Phase 3 — Implementierung**
- [ ] R2373: INI Writer implementieren
- [ ] R2374: Final Save Replacement / Umstellung der Call-Sites
- [ ] R2375: Nacharbeiten/Absicherung (Fallbacks, Logs, Edge Cases)

**Phase 4 — Docking / UI State**
- [ ] R2376: Docking-Fix (Persist/Restore) – nur falls noch offen
- [ ] R2377: Docking Audit / Startstate
- [ ] R2378: Docking Recovery / Regression-Schutz

**Phase 5 — Verifikation**
- [ ] R2379: Testplan ausführen + “SOLL/IST” dokumentieren (Logs/Report)

> Hinweis: Frühere doppelte “INI SingleWriter Konsolidierung (TOP-PRIO)” ist hier integriert.

---

## Logging/Tracebacks wieder “sicher sichtbar”
- [ ] Sicherstellen: Exceptions/Tracebacks werden **immer** in `debug_output.txt` erfasst (Run-Button/Runner/GUI)
- [ ] Zentraler Exception-Logger (ein Weg), keine verstreuten Print-Fallen
- [ ] Diagnose-First MR: Bei Nicht-Reproduzierbarkeit sofort instrumentieren (Logs/Report), kein Trial&Error

---

# P1 — High

## GUI / Status-Systemik
- [ ] Status-Events zentralisieren (z. B. `module_status.py`/Event-Bus-Konzept)
- [ ] LED-Mapping standardisieren (klarer Vertrag: welche LED bedeutet was)
- [ ] “Runner-Produkte” Tab als **Read-Only** Artefaktzentrale (klarer Zweck, keine Side-Effects)
- [ ] `docs/GUI_Decisions.md` als Single Source of Truth (was bleibt/was fliegt/warum)

## Tools / Self-Purge Absicherung
- [ ] Self-Purge: Schutzmechanismus (KEEP/Whitelist/Anchor)
- [ ] KEEP-Runner in eigenen Ordner + Purge respektiert KEEP (rekursiv, vorsichtig)
- [ ] Purge schreibt Report: “was wurde warum verschoben/gelöscht” (ideal: nur verschieben)

---

# P2 — Medium

## Runner-Produkte / Artefakte UX

- [ ] (P1) Artefakte - Tab: Treeview auto-refresh, wenn Tab aktiv wird
  - Trigger: NotebookTabChanged -> Artefakte
  - Prefer: refresh_runner_products_tab() falls vorhanden
  - Fallback: Tab-Inhalt neu aufbauen (safe rebuild)
- [ ] Runner-Produkte-Tab: Kontextmenü (Copy Path, Copy Content, Open Folder)
- [ ] Filter/Sort (Dateityp, Datum, Runner-ID)
- [ ] Preview (Text/MD/JSON) Read-only

## Pipeline / Prozess
- [ ] Pipeline-Tab in GUI (READ-ONLY) → zeigt `docs/PIPELINE.md` + “aktueller Fokus”
- [ ] Kurzer Workflow: “Aktueller Fokus” oben pflegen (1–3 Tasks max)

## Intake / Qualität

- [ ] (P1) GitHub-Update-Indikator an Push-Buttons (Private/Public)
  - Visual: kleiner Wimpel/Badge/Punkt am Button; sehr schwach rosa -> zunehmend rot je nach Dringlichkeit
  - Dringlichkeit (Heuristik): Zeit seit letztem Push ODER Anzahl unpushed Commits (oder kombiniert)
  - Datenquelle: git log origin/main..HEAD (unpushed count) + Zeitstempel aus letztem Push-Report/Registry
  - Polling: UI after()-Loop (30–60s), respektiert Busy-Flag (pausiert während Runner läuft)
  - Reset: nach erfolgreichem Push zurück auf „frisch“
  - Architektur: READ-ONLY Status -> registry/push_status.json; UI rendert nur (keine Git-Logik im UI)
- [ ] Intake: Autosave nach Paste **wenn Syntax OK**

- [ ] (P1) Intake UI: Right-Panel global alignment (oben/rechts bündig, vertikal gestapelt; keine geerbten Padding/Inserts)
  - Push/Link/Purge-Stack exakt an obere rechte Kante (flush), aber weiterhin untereinander wie jetzt
  - Workspace + Suche + Tree-Area: rechts bündig/sauber, ohne Drift bei Resize
- [ ] (P1) Intake UI: Tree-Action-Row (Run/Löschen/Rename/Undo) linksbündig direkt über der Treeview platzieren
  - visuell als „Tree-Toolbar“ erkennbar (nicht im Header-Stack)
- [ ] (P1) Intake UI: Purge-Buttons sauber ausrichten (rechte Kante, gleiche Spaltenbreite wie Push-Row; Reihen/Abstände konsistent)
- [ ] Runner-Ausführung: Policy-Popup (wo wird geloggt, was passiert, wo sind Outputs)
- [ ] LearningEngine: Products READ-ONLY scannen (Index + Findings) + Report

---

# P3 — Später / Nice-to-have
- [ ] Komfort-Popups: “Quelle kopieren”, “Pfad kopieren”, kleine UX-Verbesserungen ohne Risiko
- [ ] Weitere kleine GUI-Polish-Aufgaben nach Bedarf

---

# Done / Archive
- [x] R2453: Docking offiziell geschlossen (Runner R2453, 20251221_234813)

- [x] R2453: Docking-Thema offiziell geschlossen (inhaltlich abgeschlossen; jetzt kanonisch in der Pipeline markiert)

- [x] Docking Restore Bug resolved (R2395) — nur hier führen
- [x] (weitere erledigte Items hier sammeln, nicht im Backlog lassen)

---

# Notizen (nur Kontext, keine Task-Duplikate)
- Reports in `docs/Report_R23xx_*.md` sind Belege/History, keine zweite Pipeline.
- Wenn etwas unklar ist: erst Diagnose-Runner, dann Fix.

### Registry / Public Export
- **P0 (done):** Public Whitelist System (R2411)
- **P1:** Private Push SAFE (R2412)
- **P1:** GUI Autopush Buttons + Toggle
- **P1:** Registry- & Purge-Integration Fix (R2416)
- **P1 (done):** GUI Autopush Buttons (Private/Public) + Toggle (R2413) + Combo Runner (R2414)
- **P2:** Purge Buttons sauber ausrichten (rechter Toolbar-Bereich, sauberes Spacing)
- **P1:** Workspace-Manager: Workspaces hinzufügen/löschen + Dropdown-Auswahl (keine Hardcodes auf alte Ordner)


## Prio / P0

- [ ] (HIGH) UI: Entferne doppeltes Workspace-Dropdown in Push-Zone (oben rechts). Push-Zone nur für Push/Purge.

## P1 – Architektur & Stabilität
- Enable/Disable-Logik für Purge-Buttons (Basis: R2218 / R2224, dokumentiert in Architecture_Purge_Actions.md)
- Architekturregel: `logic_actions` ist die Quelle der Wahrheit für Button ↔ Runner-Zuordnung
- Diagnose-Runner verpflichtend, wenn ein Fix nicht sofort verifiziert ist

## P2 – Runner-Lifecycle & Ordnung
- Runner-Lifecycle explizit:
  - Alte Runner → Archiv (nicht reparieren, nicht löschen)
  - Archiv = gültig für Scan / Learning / Diagnose
  - `tools/` enthält nur Runner mit aktiver Funktion
- Langfristig: separater Ordner für Button-/SonderRunner

## P3 – Cleanup (geparkt)
- Falsch erzeugte `*_UPDATED_*.md` Dateien
  - Entfernung ausschließlich per Cleanup-Runner
  - **Nicht jetzt**, nur vorgemerkt

## P1 – Performance: Artefakte schlank halten
- **Artefakte: Purge-Button** (verworfen) im Artefakte-Tab
  - Ziel: Output-/Artefakt-Daten reduzieren, Performance stabilisieren
  - Purge-Scope klar definieren (keine Kanon-Dokus, keine Rules/Pipeline)
  - Optional: Dry-Run/Preview + Report vor Apply
  - Logging/Report verpflichtend (welche Dateien/Ordner betroffen)



## Architektur-Referenzen
- `docs/Architecture_Actions_and_Gating.md`
- `docs/Architecture_Lessons_Learned.md`

## Abandoned
- **Artefakte: Purge-Button** (verworfen)
  - Begründung: Löschen/Purge ist nicht der richtige Ansatz für Performance/Schlankheit.
  - Alternative: gezielte Archiv-/Rotation-Strategien (später, falls nötig), aber kein Purge-Button.

## P1 – UX: Kontextmenüs & Bedienkomfort
- Kontextmenü (Tree/Explorer): **Datei kopieren**
- Kontextmenü (Tree/Explorer): **Backup wiederherstellen** (nur wenn selektiertes Item ein Backup ist)
- Preview: Kontextmenü + Buttonleiste darunter (übliche Standardaktionen)
- Refresh-Button: Position **oben rechts → unten rechts**

## P2 – UX/Layout: Scrollbars & Splitter
- Beide Hauptfenster: Scrollbars **rechts und unten**
- Splitter zwischen Bereichen **schiebbar** (Resizable Panes)

