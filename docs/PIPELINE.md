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
- [ ] Runner-Produkte-Tab: Kontextmenü (Copy Path, Copy Content, Open Folder)
- [ ] Filter/Sort (Dateityp, Datum, Runner-ID)
- [ ] Preview (Text/MD/JSON) Read-only

## Pipeline / Prozess
- [ ] Pipeline-Tab in GUI (READ-ONLY) → zeigt `docs/PIPELINE.md` + “aktueller Fokus”
- [ ] Kurzer Workflow: “Aktueller Fokus” oben pflegen (1–3 Tasks max)

## Intake / Qualität
- [ ] Intake: Autosave nach Paste **wenn Syntax OK**
- [ ] Runner-Ausführung: Policy-Popup (wo wird geloggt, was passiert, wo sind Outputs)
- [ ] LearningEngine: Products READ-ONLY scannen (Index + Findings) + Report

---

# P3 — Später / Nice-to-have
- [ ] Komfort-Popups: “Quelle kopieren”, “Pfad kopieren”, kleine UX-Verbesserungen ohne Risiko
- [ ] Weitere kleine GUI-Polish-Aufgaben nach Bedarf

---

# Done / Archive
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
