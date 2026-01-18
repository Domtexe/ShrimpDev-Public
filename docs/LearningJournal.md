# LearningJournal (LJ) — Architektur-Notiz

Generated: 2026-01-18T23:36:12

## Zweck (SOLL)
LearningJournal ist der **Lern- und Beobachtungsmechanismus** von ShrimpDev:
- Erfasst Ereignisse (Events) aus realen Nutzungsflüssen (z. B. `intake_save`, `app_start`, …).
- Dient als **Systemsensor** für Stabilität/Regressionen.
- Soll perspektivisch eine **„kleine KI / Learning-Engine“** speisen:
  - erkennt entstehende Fehler-/Crash-Muster
  - priorisiert Pain Points
  - schlägt Fixes vor (später: Auto-Fix/Runner-Kandidaten, mit Guardrails)

## Ist-Zustand (IST, Stand heute)
- Event-Erfassung läuft (wachsende Diagnosen/Counts).
- **R1802** erzeugt Diagnose/Export-Artefakte: `LearningJournal_Diagnose_R1802_*.json/.txt`.
- **R1252** existiert als `R1252.py`, ist aber aktuell **wirkungslos/no-op** (ExitCode 0, keine Artefakte, kein Output).
- UI-Entry-Points waren inkonsistent (fehlende `.cmd` Wrapper wurden wiederhergestellt).

## Runner-Rollen (Normativ ab jetzt)
- **R1802 = LJ Diagnose / Analyse / Export (offizieller Diagnose-Runner)**
- **R1252 = LJ Tool-Entry (historisch), derzeit deprecated/no-op**
- UI: „LearningJournal“-Tool soll **auf R1802 zeigen**, bis R1252 einen echten, dokumentierten Zweck hat.

## Zukunft: Learning-Engine (Roadmap in Stichpunkten)
1. Minimal: „Anomalie-Sensor“
   - z. B. Peaks bei `app_start`, Fehlerhäufung, wiederkehrende Offender
2. Nächster Schritt: „Auto-Triage“
   - Cluster, Häufigkeit, Impact, Regression vs. Baseline
3. Später: „Fix-Vorschläge“
   - nur Vorschlag, keine Auto-Änderung ohne Runner/Review
4. Später: „Self-heal (Guarded)“
   - nur für klar begrenzte, verifizierbare Fixes (z. B. Restore Missing Runner Wrapper)

## No-Gos / Guardrails
- Keine stillen Auto-Edits in Produktivcode.
- Jeder Fix nur per Runner, rückbaubar, mit Report.
- Diagnose zuerst, Hypothesen belegen, dann minimaler Fix.
