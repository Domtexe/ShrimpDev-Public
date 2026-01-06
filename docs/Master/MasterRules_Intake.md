# MasterRules_Intake – Intake / Paste / Detect

_Automatisch generiert oder aktualisiert durch R2037 am 2025-12-09 09:39:55_

## 1. Sicheres Einfügen

- Intake/Paste zerstört keine Originaldateien, sondern arbeitet mit Kopien
  oder klar definierten Zielen.

## 2. Detect-Logik

- Erkennung von Python/Bat/anderen Typen basiert auf robusten Heuristiken
  und wird zentral in der Detect-Engine gepflegt.

## 3. LearningEngine

- Intake-Events können in der LearningEngine protokolliert werden, ohne den
  Ablauf zu stören.

## Importierte Intake-Guides

# Intake_Paste_Guide.md

# ShrimpDev – Code-Intake Schnellstart

**So erkennt der Intake den Dateinamen (beste Variante zuerst):**

1. Header-Kommentar:
   - `# file: tools/Runner_960.py`
   - `// path: modules/module_shcut_mapper.py`

2. Fenced Code-Block:
   - ``` ```python filename=tools/Runner_960.py ``` ```

3. Front-Matter:
   - YAML
     ```
     ---
     filename: tools/Runner_960.py
     ---
     ```
   - JSON
     ```json
     { "filename": "modules/module_xyz.py" }
     ```

4. Inline-Marker:
   - `@@file=tools/Runner_960.py@@`

5. Pragmas:
   - `REM FILE tools\Runner_960.bat`
   - `; FILE tools/Runner_960.cmd`

6. Heuristik:
   - `Runner_*` ⇒ `tools\`
   - `module_*` ⇒ `modules\`
   - sonst `.py` ⇒ `modules\snippets\`
   - Endungen aus Inhalt (py/bat/json/md)

> Tipp: Immer **Variante 1** benutzen – die ist am klarsten.

- (Neu) Detect: FILE/Path-Header hat Vorrang vor erster R####-ID im Text.

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
