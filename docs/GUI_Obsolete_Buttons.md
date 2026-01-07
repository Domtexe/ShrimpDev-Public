# GUI Obsolete Buttons – Analyse

Stand: 2025-12-14 22:24:21

Dieses Dokument ist ein READ-ONLY Report. Es wurden keine GUI-Elemente entfernt.
Heuristik: Buttons ohne command, command=None, disabled, oder unklarer Platzhalter (lambda) werden markiert.

## Legende
- NO_COMMAND: Button hat keinen command-Handler
- COMMAND_NONE: command=None
- COMMAND_LAMBDA_REVIEW: command=lambda (prüfen ob Placeholder)
- COMMAND_NAME_NOT_DEFINED_HERE: command=Name, aber Funktion in dieser Datei nicht definiert (kann extern sein)
- STATE_DISABLED: Button ist disabled (kann bewusst sein, aber oft Altlast)

## Funde pro Datei

### modules/module_learningjournal.py

| Zeile | Kontext | Text | Gründe |
|---:|---|---|---|
| 318 | build_learningjournal_tab | Neu laden | NO_COMMAND |
| 321 | build_learningjournal_tab | Diagnose (R1802) | NO_COMMAND |
| 352 | build_learningjournal_tab | Reset | NO_COMMAND |
| 354 | build_learningjournal_tab | Scans | NO_COMMAND |

### modules/module_learningjournal_ui_ext.py

| Zeile | Kontext | Text | Gründe |
|---:|---|---|---|
| 82 | build_learningjournal_panel | Neu laden | NO_COMMAND |
| 85 | build_learningjournal_panel | JSON öffnen | NO_COMMAND |

### modules/module_runner_board.py

| Zeile | Kontext | Text | Gründe |
|---:|---|---|---|
| 21 | _build_tab | Refresh | COMMAND_LAMBDA_REVIEW |

### modules/module_runnerbar.py

| Zeile | Kontext | Text | Gründe |
|---:|---|---|---|
| 52 | build_runnerbar | label | COMMAND_LAMBDA_REVIEW |

### modules/ui_buttons.py

| Zeile | Kontext | Text | Gründe |
|---:|---|---|---|
| 8 | create_buttons | Scan Project | COMMAND_LAMBDA_REVIEW |
| 9 | create_buttons | Syntax Check | COMMAND_LAMBDA_REVIEW |
| 10 | create_buttons | Reload Modules | COMMAND_LAMBDA_REVIEW |
| 11 | create_buttons | Run Runner... | COMMAND_LAMBDA_REVIEW |
| 12 | create_buttons | Open Logs | COMMAND_LAMBDA_REVIEW |

### modules/ui_left_panel.py

| Zeile | Kontext | Text | Gründe |
|---:|---|---|---|
| 203 | build_left_panel | ... | COMMAND_LAMBDA_REVIEW |

### modules/ui_log_tab.py

| Zeile | Kontext | Text | Gründe |
|---:|---|---|---|
| 146 | build_log_tab | Neu laden | COMMAND_LAMBDA_REVIEW |
| 153 | build_log_tab | Markiertes kopieren und zurück | COMMAND_LAMBDA_REVIEW |
| 160 | build_log_tab | Sichtbares kopieren und zurück | COMMAND_LAMBDA_REVIEW |
| 167 | build_log_tab | Gesamtes Log kopieren und zurück | COMMAND_LAMBDA_REVIEW |
| 174 | build_log_tab | Zurück zu Intake | COMMAND_LAMBDA_REVIEW |

### modules/ui_pipeline_tab.py

| Zeile | Kontext | Text | Gründe |
|---:|---|---|---|
| 48 | build_pipeline_tab | X | COMMAND_LAMBDA_REVIEW |
| 52 | build_pipeline_tab | Neu laden | NO_COMMAND |
| 55 | build_pipeline_tab | Im Explorer | NO_COMMAND |

### modules/ui_theme_classic.py

| Zeile | Kontext | Text | Gründe |
|---:|---|---|---|
| 47 | Button |  | NO_COMMAND |

### modules/ui_toolbar.py

| Zeile | Kontext | Text | Gründe |
|---:|---|---|---|
| 99 | _make_button | text | COMMAND_NAME_NOT_DEFINED_HERE |

### modules/ui_toolbar_dev.py

| Zeile | Kontext | Text | Gründe |
|---:|---|---|---|
| 76 | _make_button | text | COMMAND_NAME_NOT_DEFINED_HERE |

