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
