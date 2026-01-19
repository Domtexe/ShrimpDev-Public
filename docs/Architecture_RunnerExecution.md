# Runner Execution Architecture (Single Source of Truth)

## Zweck
Diese Architektur definiert **verbindlich**, wie Runner in ShrimpDev ausgeführt werden dürfen.
Ziel ist **Stabilität, Nachvollziehbarkeit und Governance** – nicht sofortige Vereinheitlichung.

---

## Kanonischer Ausführungspfad (verbindlich)
**UI / Logic → Executor → Optionales Popup → Runner**

- UI-Einstieg:
  - `modules/ui_toolbar.py`
  - `modules/ui_project_tree.py`
- Executor (kanonisch):
  - `modules/toolbar_runner_exec.py`
- Popup / UX (optional):
  - `modules/module_runner_popup.py`
- Runner:
  - `.cmd` + `.py` (nummeriert `R####`)

**Neue Runner-Ausstöße müssen diesen Pfad verwenden.**

---

## Erlaubte Ausnahmen
- `os.startfile()`:
  - Öffnen von Dateien/Ordnern (Explorer)
  - Neustart der App (best-effort)
- Legacy-Intake-/Tool-Runner:
  - Bestehende direkte `subprocess`-Nutzung bleibt **unangetastet**
  - Änderungen **nur bei echtem Bug**, nicht präventiv

---

## Verbotene Muster (ab jetzt)
- Neue direkte `subprocess.Popen/run`-Aufrufe aus UI-Modulen
- Neue direkte `.cmd`/`.bat`-Aufrufe außerhalb des Executors
- Umgehung von `toolbar_runner_exec` ohne Begründung

---

## Migrationsregel (Zukunft)
- Keine globale Bereinigung.
- Migration **nur anlassbezogen** (Bugfix, Sicherheitsproblem).
- Immer: Diagnose → minimaler Patch → Dokumentation aktualisieren.

---

## Status
- Dokumentation ist **verbindlich**.
- Code bleibt bewusst heterogen, aber **regiert**.
