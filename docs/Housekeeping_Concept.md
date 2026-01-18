# Housekeeping-Konzept (ShrimpDev)

Stand: 2026-01-16

## Ziel
ShrimpDev soll sich **selbst stabil halten**: weniger manuelle Handgriffe, weniger Drift, weniger Chaos.
Kern: **Automatische Purge-Funktion** (kein manueller Workaround wie „R3106 bitte von Hand“).

## Prinzipien (MR-konform)
- **Single Source of Truth**: Runner-Ausführung über `modules/toolbar_runner_exec.py`.
- **Diagnose zuerst**: Wenn etwas nicht beim ersten Versuch verifiziert läuft → Instrumentierung/DIAG vor Fix.
- **Minimal-invasive Änderungen**: kein Voll-Rewrite, klar umrissene Schritte, je Runner ein Thema.
- **Sicher & nachvollziehbar**: Backup, Logs, Reports, Report-Popup.

## Scope (P1)
### 1) Purge wieder automatisieren
- Toolbar-Button **Purge** startet die Purge-Sequenz **über den Canonical Executor**.
- Runner-Ziel:
  - Primär: `R3106` (oder definierter Nachfolger)
- Kein direktes `subprocess/os.system` in `ui_toolbar.py`.

### 2) Guards & UX
- Busy-Guard (nicht parallel starten)
- Confirm-Dialog (Purge ist destruktiv)
- Einheitliches Logging + Report-Popup (bestehender Standard `_r1851_show_popup`/Reportanzeige)

## Out of scope (jetzt)
- Zeitgesteuertes Auto-Purge (Cron-like)
- Erweiterte Heuristiken/Heatmaps/Automated Cleanup über Purge hinaus

## Referenzen
- Public GitHub: https://github.com/Domtexe/ShrimpDev-Public

## Purge – Orphaned/Missing Runner IDs (Historie)

Stand: `20260116_230836` (Quelle: `Reports/Report_R3532_20260116_225118.md`)

Diese Runner-IDs tauchen noch als Textreferenzen auf, aber es existieren keine Standard-Runner-Dateien mehr in `tools/` (z. B. `R####.py/.cmd`).
Sie gelten als **historisch/orphaned** und sind kein Purge-Ziel (weil es nichts zu verschieben gibt).

**Missing IDs:**
```
R269, R1243, R3251, R3252, R3253, R3254, R3255, R3256, R3257, R3260, R3290, R3297, R3303, R3304, R3306, R3307, R3308, R3318, R3337
```

**Zuletzt tatsächlich archiviert (R3532):**
```
R3471: tools/R3471.py -> tools/_Archiv/auto_tools_only/20260116_225118/R3471.py
R3471: tools/R3471.cmd -> tools/_Archiv/auto_tools_only/20260116_225118/R3471.cmd
R3478: tools/R3478.py -> tools/_Archiv/auto_tools_only/20260116_225118/R3478.py
R3478: tools/R3478.cmd -> tools/_Archiv/auto_tools_only/20260116_225118/R3478.cmd
R3503: tools/R3503.py -> tools/_Archiv/auto_tools_only/20260116_225118/R3503.py
R3503: tools/R3503.cmd -> tools/_Archiv/auto_tools_only/20260116_225118/R3503.cmd
R3504: tools/R3504.py -> tools/_Archiv/auto_tools_only/20260116_225118/R3504.py
R3504: tools/R3504.cmd -> tools/_Archiv/auto_tools_only/20260116_225118/R3504.cmd
R3505: tools/R3505.py -> tools/_Archiv/auto_tools_only/20260116_225118/R3505.py
R3505: tools/R3505.cmd -> tools/_Archiv/auto_tools_only/20260116_225118/R3505.cmd
```

<!-- R3538 BEGIN: Housekeeping/Purge Lessons -->
## Housekeeping / Purge – Status & Policy (Final)

**Status:** Housekeeping ist produktiv und verifiziert (Purge verschiebt real Dateien ins Archiv, kein Delete).

**Kern-Policy (verbindlich):**
- `tools/` ist **keine** Runtime-Reference-Quelle. Runner-Textreferenzen untereinander dürfen das Keep-Set nicht aufblasen.
- Runtime-Relevanz kommt aus **`modules/`** (Entry-Graph/Executor/Core) und **`registry/`** (Allowlist/Registry) plus Schutzmechanismen.

**Schutzmechanismen:**
- **last-N** Schutz (z. B. letzte 30 Runner bleiben)
- **Allowlist** als Override (derzeit ggf. leer; Mechanismus bleibt vorgesehen)
- **Archivieren statt Löschen** (voll reversibel)
- **Single-Run/Busy-Guard**: verhindert Parallelstarts/Double-Click Chaos

**Lessons / Vorgehen (MR-konform):**
- „Textuelle Referenz“ ≠ „operative Relevanz“.
- Heuristik ohne sicheren Anchor → **Exit 21 + DIAG-Runner** (kein Blind-Apply).
- Erst Diagnose (Quelle/Anker), dann minimaler Patch.

<!-- R3538 END -->
