# Pipeline Notes\n- [2025-12-13 20:12:31] R2118: Context-State Backbone (pure) angelegt.\n- [2025-12-13 20:21:14] R2119: Context wird bei Tabwechsel / Intake-Save / Runner-Start gefüttert.
- [2025-12-13 20:26:35] R2120: Agent nutzt Context für sichtbare Hinweise.
- [2025-12-13 20:32:32] R2121: Fix Agent-Refresh – Context-Block korrekt hinter lines-Init platziert.
- [2025-12-13 20:37:04] R2122: Agent schreibt echte Exception/Traceback nach _Reports/Agent_LastError.txt.
- [2025-12-13 20:41:35] R2123: Agent-Diagnose indent-sicher instrumentiert.
- [2025-12-13 20:51:07] R2124: Agent-Exceptions werden wieder zentral nach debug_output.txt geloggt.
- [2025-12-13 20:55:56] R2125: Settings-Tab in der GUI ans Ende verschoben.
- [2025-12-13 21:00:53] R2126: Settings-Tab ans Ende der Notebook-Tabs verschoben (robuster Patch).
- [2025-12-13 21:43:34] R2130: Agent priorisiert Empfehlungen (JETZT/DANACH/OPTIONAL) – stabiler Fix.
- [2025-12-13 21:52:40] R2131: Intake Service/SR Buttons inventarisiert (SR=[1352, 1922, 9997, 9998, 9999], Runner=[]).
- [2025-12-13 22:04:49] R2132: UI-Gruppierung für Intake Service-Buttons & SR-Info-Box hinzugefügt.
- [2025-12-13 22:06:34] R2132: UI-Gruppierung für Intake Service-Buttons & SR-Info-Box hinzugefügt.
- [2025-12-13 22:43:04] R2133: SR-Hilfe (Popup) im Intake + SR_Guide befüllt.
- [2025-12-13 23:09:12] R2134: Intake: SR Hilfe Button deterministisch in row2 eingefügt + Popup.
- [2025-12-13 23:58:32] R2135: build_toolbar_right: doppeltes row2 entfernt; SR Hilfe Button sicher ergänzt.
- [2025-12-14 00:09:40] R2136: Intake: Info-Button neben SR-Buttons (Popup SR-Erklärung) eingefügt.
- [2025-12-14 00:16:46] R2137: Crash-Fix: ui_toolbar.py aus Backup ui_toolbar.py.R2136_20251214_000940.bak restored (wegen NameError _sr_info_popup_r2136).
- [2025-12-14 07:52:43] R2137: Crash-Fix: ui_toolbar.py aus Backup ui_toolbar.py.R2136_20251214_000940.bak restored (wegen NameError _sr_info_popup_r2136).
- [2025-12-14 08:05:50] R2137: Crash-Fix: ui_toolbar.py aus Backup ui_toolbar.py.R2136_20251214_000940.bak restored (wegen NameError _sr_info_popup_r2136).

- [2025-12-14 09:24:27] R2138: Slim Snapshot OK: ShrimpDev_20251214_R2138_SLIM.zip (2174 Dateien)
2025-12-14 13:03:33 [R2143] Masterregeln sind nicht Teil der Todo-Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh).
2025-12-14 13:41:49 [R2143] Masterregeln sind nicht Teil der Todo-Pipeline: eigener GUI-Tab MasterRules (Viewer + Open/Refresh).
2025-12-14 14:08:49 [R2144] Hotfix: ui_masterrules_tab.py SyntaxError beseitigt, ShrimpDev startet wieder.
2025-12-14 15:50:35 [R2148] Log Auto-Tail implementiert (1s tick, nur wenn Tab sichtbar).
2025-12-14 16:59:50 [R2153] Pipeline: Done/Offen sichtbar + Auto-Reload stabilisiert.
2025-12-14 17:08:00 [R2154] Pipeline: Checkboxen klickbar + Save.
2025-12-14 17:17:03 [R2155] Pipeline-Tab UX verbessert (Treeview + Toggle + Filter + Summary).
2025-12-14 17:32:08 [R2156] Pipeline: Diagnose + robustes Parsing (*/- Checkboxen).
2025-12-14 17:59:24 [R2158] Pipeline: Recovery nach R2157 (IndentationError) + robust parsing.
2025-12-14 18:29:49 [R2162] HIGH: main_gui.py patched to install exception logging (R2159 fix).
2025-12-14 18:52:37 [R2165] HIGH: Runner-Guard als Standard eingeführt.
2025-12-14 19:38:54 [R2166] (A/MEDIUM) Pipeline-Tab besser lesbar/bedienbar (Search+Sort+Zebra).
2025-12-14 19:39:32 [R2166] (A/MEDIUM) Pipeline-Tab besser lesbar/bedienbar (Search+Sort+Zebra).
2025-12-14 20:03:32 [R2167a] Doku: Agent-Vertrag fixiert + module_agent_ui.py als Legacy markiert.
2025-12-14 20:11:21 [R2167] Doku: Tab-Verträge/TABS.md eingeführt/aktualisiert.
2025-12-14 20:21:25 [R2171] Pipeline: HIGH Intake Autosave nach Paste (Pfad=D:\ShrimpDev\docs\PIPELINE.md).
2025-12-14 20:49:18 [R2173] Agent: Empfehlungen klickbar (Run/Copy/Pipeline).
