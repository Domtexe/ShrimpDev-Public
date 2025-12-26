# MasterRules – Gesamtüberblick

_Automatisch generiert durch R2037 am 2025-12-09 09:39:55_

Dieses Dokument ist der Einstiegspunkt für alle Mastermodus-Regeln.
Die eigentlichen Detailregeln sind in getrennte Kapitel ausgelagert.

## Dokumente nur per Runner

- **Kanon-Dokumente** (insb. `docs/PIPELINE.md` und `docs/Master/MasterRules.md`) werden **niemals manuell** editiert.
- Änderungen erfolgen ausschließlich per **R####-Runner** mit:
  - Backup nach `_Archiv/`
  - Report nach `docs/Report_R####_*.md`
- Wenn ein Doc-Fix nötig ist: erst **kleiner Doc-Runner**, kein Misch-Runner mit UI/Logic.

## Kapitelübersicht

- [MasterRules_Core](MasterRules_Core.md): Grundprinzipien, Pfade, Sicherheit,
  Backups, Nicht-Destruktiv-Regeln.
- [MasterRules_Syntax](MasterRules_Syntax.md): Syntax- und Codequalitätsregeln,
  inklusive Erkenntnisse aus SyntaxScans.
- [MasterRules_Runners](MasterRules_Runners.md): Aufbau, Benennung, Backups,
  Reports und Exit-Codes der Runner.
- [MasterRules_GUI](MasterRules_GUI.md): GUI-Standards für ShrimpDev/ShrimpHub,
  Layout, Dark-Mode, Statusanzeigen.
- [MasterRules_Intake](MasterRules_Intake.md): Regeln für Intake, Paste,
  Detect, Snippets und LearningEngine-Integration.
- [MasterRules_Tech](MasterRules_Tech.md): Architektur-Grundsätze, Module,
  Schnittstellen zwischen ShrimpDev und ShrimpHub.

Weitere Dokumente unter `docs/Guides` und `docs/Architecture` enthalten
spezialisierte Beschreibungen, Deltas und Designs.

## Globale Arbeitsprinzipien – Sorgfalt, Sideeffects, Bugfix-Pflicht

- **Sorgfalt vor Aktionismus:** Erst verstehen, dann ändern. Änderungen schrittweise, modular, rückbaubar.
- **Sideeffects-Pflicht:** Vor jedem Patch Abhängigkeiten/Seiteneffekte prüfen (GUI, Runner-Pfade, Logging, Config).
- **Bugfix-Pflicht:** Erkannte Bugs werden behoben. Wenn der Fix nicht minimal oder risikobehaftet ist: als Pipeline-Task mit Priorität + Risiko-Notiz eintragen.
- **Dokumentationspflicht:** Jede Änderung aktualisiert relevante Dokus (Architektur, Pipeline-Status, Übersichten).
- **SEO/Klarheit:** Benennungen, Texte und Dokus so schreiben, dass sie auffindbar und eindeutig sind.

## Ergänzungen durch R2058 (Stand 2025-12-09)

### Umgang mit alten Runnern

- Alte Runner werden nicht massenhaft repariert; vorhandene Fehler dienen als Lernmaterial.
- Alte Runner dürfen angepasst werden, wenn Systemänderungen es erfordern (z. B. neue Architektur, Logging, Sicherheitsregeln).
- Alte Runner sind im Normalfall nicht mehr aktiv, außer sie sind als SonderRunner (SR) an Buttons in der GUI gekoppelt.
- Wenn ein alter Runner als SR aktiv genutzt wird, gelten für ihn die aktuellen Standards (Backups, Logging, Exit-Codes).
- Es werden keine stillen „Schönheitsreparaturen“ an alten Runnern vorgenommen; Änderungen erfolgen nur durch explizite Aufträge oder zwingende Systemanforderungen.

### Umgang mit blockierenden Regeln

- Wenn eine Masterregel einen Auftrag blockiert, wird der Auftrag nicht still abgebrochen.
- Stattdessen wird der Nutzer aktiv darauf hingewiesen, welche Regel im Weg steht.
- Der Assistent fragt nach, wie weiter vorzugehen ist (z. B. Ausnahme zulassen, Regel anpassen oder Auftrag ändern).

### Multi-Select und Dateioperationen

- Die TreeView im Intake/Projektbereich unterstützt Mehrfachauswahl (Shift/Strg) und Lasso-/Drag-Selektieren.
- Dateioperationen (Löschen, Umbenennen, Verschieben) nutzen Mehrfachauswahl nur mit begleitendem Journal/Undo.
- Es werden keine destruktiven Massenoperationen ohne vorherige Sicherung (Backup/Snapshot) durchgeführt.

## Regel 11 – Triple-Quotes-Verbot (R2061)

Triple-Quoted-Strings sind in allen ShrimpDev- und ShrimpHub-Modulen verboten.

### 11.1 Verbotene Konstrukte
- """ ... """
- ''' ... '''

Sie duerfen nicht in generiertem Code, Modulen, Runnern oder Tools erscheinen.

### 11.2 Begruendung
- Fuehrt zu Syntaxfehlern im Intake
- Bricht ShrimpDev-Python-Parser
- Zerstoert Code-Erkennung im Detect-System
- Kollisionen mit JSON, Markdown, Platzhaltern

### 11.3 Erlaubte Alternativen
- Zeilen-Arrays (['A', 'B', ...])
- Mehrfaches f.write()
- String-Konkatenation
- Raw-Strings ohne Triple-Quotes

### 11.4 Geltungsbereich
- Alle Runner
- Alle Module
- Alle KI-generierten Dateien
- Alle Spezifikations-Tools

### 11.5 Ausnahmen
Keine. Triple-Quotes sind vollstaendig untersagt.


## Dokumentationspflicht (global)
- Jede Änderung umfasst: Code + passende Doku/Changelog/Pipeline-Update.
- Keine UI-Patches ohne vorherige Code-Analyse des echten Widget-Typs (z. B. Treeview vs Listbox).
- Keine Injektion in offene try/except-Scopes; nur an sicheren, geprüften Anchors.
- (Ergänzt durch R2303)


## Runner-Produkte: interner Viewer (READ-ONLY)
- Reports/Docs/Logs werden bevorzugt intern angezeigt (Read-Only), extern nur als Fallback.
- UI-Änderungen nur an geprüften Anchors; keine Injektion in offene try/except Scopes.
- (Ergänzt durch R2304)

## Runner-Lifecycle

- **Alte Runner** werden **nicht repariert** und **nicht gelöscht**.
- Alte Runner werden **ins Archiv verschoben**.
- Das **Archiv ist ein gültiger Arbeitsraum** für:
  - Scan
  - Learning
  - Diagnose
- Der Ordner `tools/` enthält **nur Runner mit aktiver Funktion**, z. B.:
  - Button-Runner
  - SonderRunner
  - produktiv genutzte Diagnose- oder Fix-Runner
- **Langfristiges Ziel**:
  - Separate Ablage für Button-/SonderRunner,
    um versehentliche Löschungen zu verhindern.



## Canonical Paths
Zeitpunkt: 2025-12-23 23:26:41

## Kanonische Pfade (verbindlich)
- **Reports/** → alle Reports (einziger Zielort)
- **docs/PIPELINE.md** → ShrimpDev-Pipeline
- **docs/pipelines/** → Produktpipelines (ShrimpHub, ShrimpBridge, …)
- **docs/Architecture/** → Architektur & Systemdesign
- **tools/** → Runner
- **modules/** → Runtime-Code

## Nicht-kanonisch (Legacy / Archiv)
- `_Reports/`
- `docs/Report_*`
- `_Pipeline/`
- `_Archiv/`
- `_Snapshots/`

Nicht-kanonische Pfade dürfen existieren, werden aber **nicht mehr aktiv beschrieben oder ausgewertet**.
