# Mastermodus – Syntax- & Runner-Qualität

_Dokumentiert durch R2036 am 2025-12-09 09:00:56_

## Hintergrund

Auf Basis der Auswertung von Syntax-Scans (z. B. R2035) werden hier verbindliche
Regeln fuer die Qualitaet von Python-Code und Runner-Struktur im Mastermodus
festgehalten. Alte Runner werden nicht nachtraeglich repariert, dienen aber als
Fehlerarchiv und Lernmaterial.

## 1. Keine freien Textzeilen im Code

- Natuerliche Sprache, Bullet-Listen, Notizen und Spezifikationen duerfen nicht als
  „freie“ Zeilen im Code stehen.
- Stattdessen werden sie grundsaetzlich als Kommentare (`# ...`) oder als sauber
  geschlossene Docstrings (`"""..."""`) notiert.
- Es gibt keine Pseudo-Spezifikationen mehr, die syntaktisch wie Python aussehen,
  aber keine gueltigen Statements sind.

## 2. Triple-Strings immer sauber schliessen

- Triple-quoted Strings (`"""..."""`) werden nur verwendet, wenn sie vollstaendig
  in sich abgeschlossen sind.
- Lange Textbloecke werden entweder als Docstring oder als Kommentarblock realisiert.
- Es werden keine halbfertigen oder „abgeschnittenen“ Triple-Strings im Code
  hinterlassen (Gefahr: `unterminated triple-quoted string literal`).

## 3. Kein Batch-Code in Python-Dateien

- Batch-Kommandos wie `@echo off`, `pause`, `REM` etc. gehoeren ausschliesslich in
  `.cmd`- oder `.bat`-Dateien.
- Python-Dateien enthalten nur Python-Code, Kommentare und Docstrings.
- Die Standardstruktur fuer Runner bleibt bestehen:
  - `tools/Rxxxx.cmd` als Starter (Batch)
  - `tools/Rxxxx.py` als Logik (Python)

## 4. Saubere Zeichenwahl in Code-Zeilen

- In Code-Zeilen (ausserhalb von Strings/Kommentaren) werden nur uebliche ASCII-
  Zeichen verwendet.
- Typografische Sonderzeichen wie Gedankenstriche (`–`), Auslassungspunkte (`…`)
  oder „Smart Quotes“ werden nur in Strings oder Kommentaren eingesetzt.
- In f-Strings werden keine nackten `{}` verwendet. Platzhalter sind immer gueltige
  Ausdruecke oder werden mit `{{` / `}}` escaped.

## 5. Syntax-Selfcheck fuer neue Runner

- Jeder neue Runner, der Dateien erzeugt oder veraendert, fuehrt nach Abschluss
  des Patches einen Syntaxcheck mit `compile(text, filename, "exec")` auf die
  betroffenen Python-Dateien aus.
- Bei `SyntaxError` gilt:
  - Originaldatei bleibt erhalten oder wird aus einem Backup restauriert.
  - Der Fehler wird in einem Report unter `_Reports/Rxxxx_*.txt` dokumentiert.
  - Der Runner beendet sich mit einem Fehlercode ungleich 0.
- Ziel ist, dass aktive Module (z. B. `modules/`, `main_gui.py`, aktuelle Runner)
  jederzeit syntaktisch gueltig bleiben.

## 6. Alte Baustellen bleiben Archiv

- Ordner wie `_Trash`, `_OldStuff`, `Runners_Friedhof` und aehnliche Bereiche gelten
  als Archiv und Lernmaterial, nicht als aktiver Codebestand.
- Neue Runner veraendern grundsaetzlich nur den aktiven Kern (z. B. `modules`,
  `tools`, `main_gui.py`, produktive Runner-Generationen).
- Globale Scans (z. B. R2035 SyntaxScan) dienen vor allem der Diagnose und dem
  Lernen. Alte Runner muessen nicht rueckwirkend repariert werden.

## 7. Anwendung im Mastermodus

- Diese Regeln sind ab Dokumentationszeitpunkt fuer alle neuen Arbeiten im
  Mastermodus bindend.
- Neue Runner und Module muessen diese Vorgaben automatisch einhalten.
- Verstösse werden als Designfehler behandelt und bei naechster Gelegenheit in
  der aktiven Codebasis korrigiert, ohne historisches Material im Archiv
  zwangsweise anzupassen.

## Importierte Inhalte (Syntax-Qualität)

# Mastermodus – Syntax- & Runner-Qualität

_Dokumentiert durch R2036 am 2025-12-09 09:00:56_

## Hintergrund

Auf Basis der Auswertung von Syntax-Scans (z. B. R2035) werden hier verbindliche
Regeln fuer die Qualitaet von Python-Code und Runner-Struktur im Mastermodus
festgehalten. Alte Runner werden nicht nachtraeglich repariert, dienen aber als
Fehlerarchiv und Lernmaterial.

## 1. Keine freien Textzeilen im Code

- Natuerliche Sprache, Bullet-Listen, Notizen und Spezifikationen duerfen nicht als
  „freie“ Zeilen im Code stehen.
- Stattdessen werden sie grundsaetzlich als Kommentare (`# ...`) oder als sauber
  geschlossene Docstrings (`"""..."""`) notiert.
- Es gibt keine Pseudo-Spezifikationen mehr, die syntaktisch wie Python aussehen,
  aber keine gueltigen Statements sind.

## 2. Triple-Strings immer sauber schliessen

- Triple-quoted Strings (`"""..."""`) werden nur verwendet, wenn sie vollstaendig
  in sich abgeschlossen sind.
- Lange Textbloecke werden entweder als Docstring oder als Kommentarblock realisiert.
- Es werden keine halbfertigen oder „abgeschnittenen“ Triple-Strings im Code
  hinterlassen (Gefahr: `unterminated triple-quoted string literal`).

## 3. Kein Batch-Code in Python-Dateien

- Batch-Kommandos wie `@echo off`, `pause`, `REM` etc. gehoeren ausschliesslich in
  `.cmd`- oder `.bat`-Dateien.
- Python-Dateien enthalten nur Python-Code, Kommentare und Docstrings.
- Die Standardstruktur fuer Runner bleibt bestehen:
  - `tools/Rxxxx.cmd` als Starter (Batch)
  - `tools/Rxxxx.py` als Logik (Python)

## 4. Saubere Zeichenwahl in Code-Zeilen

- In Code-Zeilen (ausserhalb von Strings/Kommentaren) werden nur uebliche ASCII-
  Zeichen verwendet.
- Typografische Sonderzeichen wie Gedankenstriche (`–`), Auslassungspunkte (`…`)
  oder „Smart Quotes“ werden nur in Strings oder Kommentaren eingesetzt.
- In f-Strings werden keine nackten `{}` verwendet. Platzhalter sind immer gueltige
  Ausdruecke oder werden mit `{{` / `}}` escaped.

## 5. Syntax-Selfcheck fuer neue Runner

- Jeder neue Runner, der Dateien erzeugt oder veraendert, fuehrt nach Abschluss
  des Patches einen Syntaxcheck mit `compile(text, filename, "exec")` auf die
  betroffenen Python-Dateien aus.
- Bei `SyntaxError` gilt:
  - Originaldatei bleibt erhalten oder wird aus einem Backup restauriert.
  - Der Fehler wird in einem Report unter `_Reports/Rxxxx_*.txt` dokumentiert.
  - Der Runner beendet sich mit einem Fehlercode ungleich 0.
- Ziel ist, dass aktive Module (z. B. `modules/`, `main_gui.py`, aktuelle Runner)
  jederzeit syntaktisch gueltig bleiben.

## 6. Alte Baustellen bleiben Archiv

- Ordner wie `_Trash`, `_OldStuff`, `Runners_Friedhof` und aehnliche Bereiche gelten
  als Archiv und Lernmaterial, nicht als aktiver Codebestand.
- Neue Runner veraendern grundsaetzlich nur den aktiven Kern (z. B. `modules`,
  `tools`, `main_gui.py`, produktive Runner-Generationen).
- Globale Scans (z. B. R2035 SyntaxScan) dienen vor allem der Diagnose und dem
  Lernen. Alte Runner muessen nicht rueckwirkend repariert werden.

## 7. Anwendung im Mastermodus

- Diese Regeln sind ab Dokumentationszeitpunkt fuer alle neuen Arbeiten im
  Mastermodus bindend.
- Neue Runner und Module muessen diese Vorgaben automatisch einhalten.
- Verstösse werden als Designfehler behandelt und bei naechster Gelegenheit in
  der aktiven Codebasis korrigiert, ohne historisches Material im Archiv
  zwangsweise anzupassen.

## Regex/Replace-Regel für Runner-Patches

- Bei `re.sub` Replacements niemals unescaped Backslashes im Replacement verwenden.
- Immer: Replacement als Funktion (`def repl(m): ...`) oder `lambda m: ...`.
- Compile-Gate Pflicht: Patch nur übernehmen, wenn `py_compile` OK ist.

- **Logging/Debug:** siehe Regel in `MasterRules_Tech.md` (Marker: `MR-DEBUG-LOGGING-NO-NEW-VARS`).

<!-- SHRIMPDEV_RULE_FSTRING_SAFETY -->

## F-String Safety & Guard-Policy (CI-relevant)

**Warum:** Mehrfach gab es Crashes/CI-Fails durch f-strings mit **undefinierten Namen** (z. B. `name` statt `btn_name`)
oder durch **Backslashes in f-string expressions**.

### Regeln (verbindlich)
- In `f"..."` dürfen nur **sicher definierte** Namen verwendet werden (lokal, Parameter, `self.`-Attribute).
- **Nie** in f-string expressions `\` / `.replace("\\", ...)` o. ä. verwenden.
  → Vorher in eine Variable berechnen, dann in den f-string einfügen.
- Logging/Debug-Helper müssen **alle** verwendeten Variablen als Parameter bekommen
  (kein “ich greife mal schnell auf `name` zu”, wenn es nicht existiert).
- Nach jeder Änderung an UI/Toolbar/Runnern: **Smoke-Test / compile** lokal + CI muss grün sein.

### Guard (Empfehlung / Standard-Workflow)
- Vor Push: **Lint-Guard “unknown identifiers in f-strings”** laufen lassen (Runner R2867).
- Wenn Guard anschlägt: Fix **vor** Push. Kein “wird schon” mehr.

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
