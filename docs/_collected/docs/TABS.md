# ShrimpDev Tabs – Vertrag & Zuständigkeiten

Stand: 2025-12-14 20:11:21

Regel: Was hier nicht dokumentiert ist, gilt als nicht vorhanden.

## Tab-Mapping

| Tab | Builder-Modul | Builder-Funktion | Vertrag |
|---|---|---|---|
| Intake | (siehe main_gui / Intake-Builder) | _build_intake(parent) | Haupt-Tool. Keine Umgehung. |
| Log | modules.ui_log_tab | build_log_tab(parent, app) (oder äquivalent) | Auto-Tail + Anzeige debug_output.txt |
| LearningJournal | modules.module_learningjournal | build_learningjournal_tab(parent, app) | Journal UI + Filter |
| Pipeline | modules.ui_pipeline_tab | build_pipeline_tab(parent, app) | PIPELINE.md anzeigen/steuern |
| Agent | modules.module_agent | build_agent_tab(parent, app) | SAFE load, keine Auto-Aktionen |
| Project | (siehe main_gui) | (siehe main_gui) | Projekt-Funktionen |
| Settings | modules.ui_settings_tab | build_settings_tab(parent, app) (oder äquivalent) | Konfiguration |

## Agent-Vertrag (aus main_gui bestätigt)

- Detected in main_gui.py: YES
- Erwartet: modules.module_agent / build_agent_tab(parent, app)

Snippet (relevant lines):

```
            from modules import module_agent
            if hasattr(module_agent, 'build_agent_tab'):
                module_agent.build_agent_tab(self.tab_agent, self)
                _tk.Label(self.tab_agent, text='Agent: build_agent_tab fehlt.').pack(anchor='w', padx=8, pady=8)
```

