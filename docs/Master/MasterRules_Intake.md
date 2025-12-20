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
