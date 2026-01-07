# MasterRules_Core – Grundprinzipien

_Automatisch generiert oder aktualisiert durch R2037 am 2025-12-09 09:39:55_

## 1. Nicht-destruktive Änderungen

- Es werden keine produktiven Dateien ohne Backup geändert.
- Runner legen vor strukturellen Änderungen Backups an (z. B. unter `_Archiv`).
- Alte Versionen bleiben rekonstruierbar; neue Versionen sind minimal invasiv.

## 2. Modulprinzip

- Funktionen werden in klar getrennten Modulen implementiert.
- ShrimpDev und ShrimpHub arbeiten mit expliziten Imports, ohne versteckte
  exec/Reflection-Tricks.

## 3. Pfade & Umgebung

- Standardpfad ist immer der Projekt-Root, in dem das Skript ausgeführt wird.
- Keine harten Laufwerks-Pfade im Code; Runner arbeiten relativ zum Projekt.

## 4. Logging & Reports

- Wichtige Operationen erzeugen Reports unter `_Reports/`.
- Fehler werden nicht verschwiegen, sondern nachvollziehbar protokolliert.

## Patch-Rollback-Pflicht

- **Ziel:** Kein fehlerhafter Patch bleibt im Arbeitsstand liegen.
- **Trigger:** Wenn ein Runner-Patch
  - mit Exit-Code != 0 endet, oder
  - einen Syntax- oder Compile-Check nicht besteht, oder
  - einen definierten Smoke-Test nicht besteht,
  muss ein **Rollback** auf den letzten sicheren Stand erfolgen.
- **Pflichtablauf (Runner):**
  - Vor Patch: Backup der betroffenen Dateien nach `_Archiv/`.
  - Patch anwenden.
  - Validierung (mindestens Syntax/Compile, optional Smoke-Test).
  - Bei Fehler: automatisch Dateien aus Backup wiederherstellen.
  - Report in `Reports/` muss enthalten:
    - Grund des Rollbacks (SOLL/IST),
    - betroffene Dateien,
    - verwendete Backup-Dateien,
    - naechster Schritt (Diagnose-first, falls wiederholt).
- **No-Go:** Manuelles Liegenlassen eines kaputten Zustands oder Folge-Patches ohne Diagnose.

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
