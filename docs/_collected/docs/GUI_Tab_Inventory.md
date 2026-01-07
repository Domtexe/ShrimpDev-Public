# GUI Tab Inventory – ShrimpDev

Stand: 2025-12-14 23:00:32

READ-ONLY Inventar: Tabs & Buttons aus dem Sourcecode extrahiert (statisch).
Ziel: Tab-für-Tab entscheiden (KEEP/REMOVE/REWORK/MOVE).

## modules/common_tabs.py

### Tabs (Notebook.add text=...)

| Zeile | Kontext | Tab-Text |
|---:|---|---|
| 25 | ensure_tab | title |

_Keine Buttons erkannt._

## modules/logic_actions.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 1232 | _r1851_show_popup | 'Schliessen' | _on_close |
| 1457 | _r1852_show_popup | 'Schliessen' | _on_close |

## modules/module_agent.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 717 | build_agent_tab | 'Aktualisieren' | _refresh |
| 718 | build_agent_tab | 'Ausfuehren' | _run_selected |
| 719 | build_agent_tab | 'Pfad kopieren' | _copy_selected_path |
| 720 | build_agent_tab | 'In Pipeline' | _add_to_pipeline |

## modules/module_learningjournal.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 318 | build_learningjournal_tab | 'Neu laden' |  |
| 321 | build_learningjournal_tab | 'Diagnose (R1802)' |  |
| 352 | build_learningjournal_tab | 'Reset' |  |
| 354 | build_learningjournal_tab | 'Scans' |  |

## modules/module_learningjournal_ui_ext.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 82 | build_learningjournal_panel | 'Neu laden' |  |
| 85 | build_learningjournal_panel | 'JSON öffnen' |  |

## modules/module_patch_release.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 30 | _build_tab | 'Build ZIP' | build |

## modules/module_preflight.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 36 | _build_tab | 'Run Checks' | run |

## modules/module_runner_board.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 21 | _build_tab | 'Refresh' | lambda |

## modules/module_runner_popup.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 173 | run_runner_with_popup | 'Schließen' | top.destroy |
| 271 | run_runner_with_popup | 'Text kopieren' | copy_output |
| 274 | run_runner_with_popup | 'Kopieren und schließen' | copy_and_close |
| 277 | run_runner_with_popup | 'Schließen' | close_popup |

## modules/module_runnerbar.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 52 | build_runnerbar | label | lambda |

## modules/module_settings_ui.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 28 | _build_tab | '...' | _pick |
| 37 | _build_tab | 'Speichern' | _save_btn |

## modules/ui_buttons.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 8 | create_buttons | 'Scan Project' | lambda |
| 9 | create_buttons | 'Syntax Check' | lambda |
| 10 | create_buttons | 'Reload Modules' | lambda |
| 11 | create_buttons | 'Run Runner...' | lambda |
| 12 | create_buttons | 'Open Logs' | lambda |

## modules/ui_left_panel.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 203 | build_left_panel | '...' | lambda |

## modules/ui_log_tab.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 146 | build_log_tab | 'Neu laden' | lambda |
| 153 | build_log_tab | 'Markiertes kopieren und zurück' | lambda |
| 160 | build_log_tab | 'Sichtbares kopieren und zurück' | lambda |
| 167 | build_log_tab | 'Gesamtes Log kopieren und zurück' | lambda |
| 174 | build_log_tab | 'Zurück zu Intake' | lambda |

## modules/ui_pipeline_tab.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 48 | build_pipeline_tab | 'X' | lambda |
| 52 | build_pipeline_tab | 'Neu laden' |  |
| 55 | build_pipeline_tab | 'Im Explorer' |  |

## modules/ui_project_tree.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 257 | build_tree | 'Ordner' | _btn_open_root |
| 258 | build_tree | 'Tools' | _btn_open_tools |
| 259 | build_tree | 'Reports' | _btn_open_reports |
| 260 | build_tree | 'Snapshots' | _btn_open_snapshots |
| 261 | build_tree | 'Explorer' | _btn_open_explorer |

## modules/ui_settings_tab.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 64 | build_settings_tab | '...' | on_browse_root |
| 97 | build_settings_tab | 'Einstellungen speichern' | on_save |

## modules/ui_theme_classic.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 47 | Button |  |  |

## modules/ui_toolbar.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 99 | _make_button | text | command |
| 417 | _action_show_log | 'Ältere laden' | _load_older |
| 420 | _action_show_log | 'Inhalt kopieren' | _copy_content |
| 423 | _action_show_log | 'Kopieren & schließen' | _copy_and_close |
| 426 | _action_show_log | 'Schließen' | _close |

## modules/ui_toolbar_dev.py

### Buttons

| Zeile | Kontext | Text | command |
|---:|---|---|---|
| 76 | _make_button | text | command |

