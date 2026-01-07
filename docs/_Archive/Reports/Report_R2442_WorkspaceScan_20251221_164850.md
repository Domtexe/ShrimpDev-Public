[R2442] READ-ONLY: Workspace sources scan
Time: 2025-12-21 16:48:49
Root: C:\Users\rasta\OneDrive\ShrimpDev

## Hits (filtered)
### Priority
C:\Users\rasta\OneDrive\ShrimpDev\main_gui.py:464: [WORKSPACE_ROOT] # R2030: Fallback zuerst auf workspace_root/snippets, dann auf cwd/snippets
C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py:7: [WORKSPACE_ROOT] - workspace_root
C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py:64: [WORKSPACE_ROOT] if "workspace_root" not in settings:
C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py:65: [WORKSPACE_ROOT] settings["workspace_root"] = str(project_root)
C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py:153: [WORKSPACE_ROOT] Liefert den aktuellen workspace_root als Path.
C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py:156: [WORKSPACE_ROOT] raw = self.get_value("workspace_root", None)
C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py:161: [WORKSPACE_ROOT] self.set_value("workspace_root", raw, auto_save=True)
C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py:166: [WORKSPACE_ROOT] Setzt den workspace_root.
C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py:168: [WORKSPACE_ROOT] self.set_value("workspace_root", str(path), auto_save=auto_save)
C:\Users\rasta\OneDrive\ShrimpDev\modules\logic_actions.py:1582: [WORKSPACE_ROOT] """Liefert den workspace_root fuer Dateioperationen in logic_actions.
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_settings_ui.py:11: [WORKSPACE_ROOT] if not CFG.exists(): return {"workspace_root": r"D:\ShrimpHub", "quiet_mode": True}
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_settings_ui.py:13: [WORKSPACE_ROOT] except Exception: return {"workspace_root": r"D:\ShrimpHub", "quiet_mode": True}
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_settings_ui.py:22: [WORKSPACE_LABEL] ttk.Label(frm, text="Workspace Root:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_settings_ui.py:23: [WORKSPACE_ROOT] var_ws = tk.StringVar(value=conf.get("workspace_root", r"D:\ShrimpHub"))
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_settings_ui.py:26: [WORKSPACE_LABEL] d = filedialog.askdirectory(title="Workspace wählen", initialdir=str(Path(var_ws.get() or r"D:\\")))
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_settings_ui.py:32: [WORKSPACE_ROOT] conf["workspace_root"] = var_ws.get().strip() or r"D:\ShrimpHub"
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_project_tree.py:68: [WORKSPACE_LABEL] # Workspace-Auswahl (dynamisch: INI + Auto-Scan)
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_project_tree.py:116: [WORKSPACE_LABEL] tk.Label(row_workspace, text="Workspace:", bg=bg).pack(side="left")
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_project_tree.py:167: [WORKSPACE_LABEL] # Basis: aktueller Workspace aus workspace_var, sonst ShrimpDev
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_project_tree.py:207: [WORKSPACE_LABEL] # Markierte Datei im Explorer, sonst Workspace-Root
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_project_tree.py:242: [WORKSPACE_LABEL] # Versuche, ShrimpDev/Workspace neu zu starten
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_settings_tab.py:5: [WORKSPACE_ROOT] - workspace_root anzeigen/ändern
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_settings_tab.py:40: [WORKSPACE_ROOT] # Row 0: workspace_root Label + Entry + Button
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_settings_tab.py:41: [WORKSPACE_LABEL] lbl_root = ttk.Label(frame, text="Workspace-Root:")
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_settings_tab.py:53: [WORKSPACE_LABEL] title="Workspace-Root wählen",
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_settings_tab.py:59: [WORKSPACE_LABEL] title="Workspace-Root wählen",
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_settings_tab.py:86: [WORKSPACE_ROOT] f"workspace_root:\n{new_root}\n"
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:703: [WORKSPACE_LABEL] # R2441: Workspace dropdown (active workspace)
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:709: [WORKSPACES_JSON] rp = Path(getattr(app, "project_root", "")) / "registry" / "workspaces.json"
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:711: [WORKSPACES_JSON] rp = Path(__file__).resolve().parent.parent / "registry" / "workspaces.json"
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:764: [WORKSPACE_ROOT] app.workspace_root = Path(str(ws[name].get("path",""))).resolve()
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:813: [WORKSPACE_LABEL] # 2) app.public_export_root (if later wired from workspace/config)
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:2: [WORKSPACE_LABEL] Workspace Registry API (READ-ONLY)
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:4: [WORKSPACES_JSON] Registry file: registry/workspaces.json
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:31: [WORKSPACES_JSON] REGISTRY_REL = Path("registry") / "workspaces.json"
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:118: [WORKSPACES_JSON] """Write registry/workspaces.json. Returns True on success."""
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:129: [WORKSPACE_LABEL] """Set active workspace by name and persist."""

### Other
C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py:41: [PROJECT_ROOT] def ensure_loaded(self, project_root: Optional[Path] = None) -> None:
C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py:49: [PROJECT_ROOT] if project_root is None:
C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py:50: [PROJECT_ROOT] project_root = self._get_default_project_root()
C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py:51: [PROJECT_ROOT] self._project_root = project_root
C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py:65: [PROJECT_ROOT] settings["workspace_root"] = str(project_root)
C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py:80: [PROJECT_ROOT] self.ensure_loaded(project_root=self._project_root if hasattr(self, "_project_root") else None)
C:\Users\rasta\OneDrive\ShrimpDev\modules\exception_logger.py:30: [PROJECT_ROOT] def configure(project_root: str | Path) -> None:
C:\Users\rasta\OneDrive\ShrimpDev\modules\exception_logger.py:32: [PROJECT_ROOT] _ROOT = Path(project_root).resolve()
C:\Users\rasta\OneDrive\ShrimpDev\modules\exception_logger.py:97: [PROJECT_ROOT] def install(project_root: str | Path) -> None:
C:\Users\rasta\OneDrive\ShrimpDev\modules\exception_logger.py:101: [PROJECT_ROOT] configure(project_root)
C:\Users\rasta\OneDrive\ShrimpDev\modules\ini_writer.py:149: [PROJECT_ROOT] def ini_path(project_root: Path) -> Path:
C:\Users\rasta\OneDrive\ShrimpDev\modules\ini_writer.py:150: [PROJECT_ROOT] return (project_root / "ShrimpDev.ini").resolve()
C:\Users\rasta\OneDrive\ShrimpDev\modules\ini_writer.py:157: [PROJECT_ROOT] def merge_write_ini(project_root: Path,
C:\Users\rasta\OneDrive\ShrimpDev\modules\ini_writer.py:165: [PROJECT_ROOT] path = ini_path(project_root)
C:\Users\rasta\OneDrive\ShrimpDev\modules\learning_engine.py:12: [PROJECT_ROOT] - Journal: <project_root>/learning_journal.json
C:\Users\rasta\OneDrive\ShrimpDev\modules\learning_engine.py:63: [PROJECT_ROOT] # modules/learning_engine.py -> modules -> project_root
C:\Users\rasta\OneDrive\ShrimpDev\modules\logic_actions.py:969: [HARDCODE_PATH] _r1848_mb.showerror("Explorer", "Pfad existiert nicht mehr:\n" + path)
C:\Users\rasta\OneDrive\ShrimpDev\modules\logic_actions.py:975: [HARDCODE_PATH] _r1848_mb.showerror("Explorer", "Fehler beim Oeffnen:\n" + repr(exc))
C:\Users\rasta\OneDrive\ShrimpDev\modules\logic_actions.py:1332: [HARDCODE_PATH] msg = "Runner-Datei nicht gefunden:\n" + cmd_path
C:\Users\rasta\OneDrive\ShrimpDev\modules\logic_actions.py:1551: [HARDCODE_PATH] msg = "Runner-Datei nicht gefunden:\n" + cmd_path
C:\Users\rasta\OneDrive\ShrimpDev\modules\logic_actions.py:2370: [HARDCODE_PATH] #             _r1846_show_popup(label, "Fehler beim Ausführen:\n" + repr(exc))
C:\Users\rasta\OneDrive\ShrimpDev\modules\logic_actions.py:2384: [HARDCODE_PATH] #                 _r1846_mb.showerror(label, "Runner-Datei nicht gefunden:\n" + cmd_path)
C:\Users\rasta\OneDrive\ShrimpDev\modules\logic_actions.py:2491: [HARDCODE_PATH] #             _r1847_show_popup(label, "Fehler beim Ausführen:\n" + repr(exc))
C:\Users\rasta\OneDrive\ShrimpDev\modules\logic_actions.py:2503: [HARDCODE_PATH] #         msg = "Runner-Datei nicht gefunden:\n" + cmd_path
C:\Users\rasta\OneDrive\ShrimpDev\modules\logic_actions.py:2640: [HARDCODE_PATH] #                     _r1849_mb.showinfo("Gespeichert", "Datei gespeichert unter:\n" + path)
C:\Users\rasta\OneDrive\ShrimpDev\modules\logic_actions.py:2821: [HARDCODE_PATH] _r2066_mb.showerror("Rename", "Fehler beim Umbenennen:\n" + repr(exc))
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_agent.py:105: [HARDCODE_PATH] f"Traceback:\n{tb}\n",
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_agent.py:133: [HARDCODE_PATH] f"Traceback:\n{tb}\n",
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_gate_smoke.py:11: [HARDCODE_PATH] def _log(msg, dbg_path=r"C:\Users\rasta\OneDrive\ShrimpDev\debug_output.txt"):
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_learningjournal.py:69: [HARDCODE_PATH] return None, "Keine learning_journal.json gefunden. Erwartet unter:\n - {}\n - {}".format(
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_learningjournal.py:295: [HARDCODE_PATH] return "Fehler beim Formatieren des Eintrags:\n{}\n\nRohdaten:\n{}".format(
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_learningjournal.py:338: [COMBOBOX] combo_filter = ttk.Combobox(
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_patch_release.py:8: [HARDCODE_PATH] ROOT = Path(r"C:\Users\rasta\OneDrive\ShrimpDev")
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_patch_release.py:28: [HARDCODE_PATH] try: messagebox.showinfo("ShrimpDev", f"Export:\n{target}")
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_patch_release.py:36: [HARDCODE_PATH] try: messagebox.showerror("ShrimpDev", f"Patch/Release Fehler:\n{ex}")
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_preflight.py:8: [HARDCODE_PATH] ROOT = Path(r"C:\Users\rasta\OneDrive\ShrimpDev")
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_preflight.py:43: [HARDCODE_PATH] try: messagebox.showerror("ShrimpDev", f"Preflight Fehler:\n{ex}")
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_project_scan.py:7: [HARDCODE_PATH] HUB = Path(r"D:\ShrimpHub")
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_project_scan.py:8: [HARDCODE_PATH] OUT = Path(r"C:\Users\rasta\OneDrive\ShrimpDev\Reports\ProjectMap"); OUT.mkdir(parents=True, exist_ok=True)
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_registry.py:7: [HARDCODE_PATH] ROOT = Path(r"C:\Users\rasta\OneDrive\ShrimpDev")
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_registry.py:8: [REGISTRY] REG  = ROOT / "registry" / "module_registry.json"
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_runner_board.py:7: [HARDCODE_PATH] ROOT = Path(r"C:\Users\rasta\OneDrive\ShrimpDev")
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_runner_board.py:36: [HARDCODE_PATH] try: messagebox.showerror("ShrimpDev", f"Startfehler:\n{ex}")
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_runner_board.py:45: [HARDCODE_PATH] try: messagebox.showerror("ShrimpDev", f"Runner Board Fehler:\n{ex}")
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_runner_popup.py:141: [HARDCODE_PATH] text_widget.after(0, fn, "Fehler beim Starten des Runners:\n{}\n".format(exc))
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_settings_ui.py:7: [HARDCODE_PATH] ROOT = Path(r"C:\Users\rasta\OneDrive\ShrimpDev")
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_settings_ui.py:11: [HARDCODE_PATH] if not CFG.exists(): return {"workspace_root": r"D:\ShrimpHub", "quiet_mode": True}
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_settings_ui.py:13: [HARDCODE_PATH] except Exception: return {"workspace_root": r"D:\ShrimpHub", "quiet_mode": True}
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_settings_ui.py:23: [HARDCODE_PATH] var_ws = tk.StringVar(value=conf.get("workspace_root", r"D:\ShrimpHub"))
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_settings_ui.py:26: [HARDCODE_PATH] d = filedialog.askdirectory(title="Workspace wählen", initialdir=str(Path(var_ws.get() or r"D:\\")))
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_settings_ui.py:32: [HARDCODE_PATH] conf["workspace_root"] = var_ws.get().strip() or r"D:\ShrimpHub"
C:\Users\rasta\OneDrive\ShrimpDev\modules\module_settings_ui.py:43: [HARDCODE_PATH] try: messagebox.showerror("ShrimpDev", f"Settings Fehler:\n{ex}")
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_project_tree.py:117: [COMBOBOX] combo_workspace = ttk.Combobox(
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py:304: [COMBOBOX] cmb_type = ttk.Combobox(f, textvariable=var_type, values=["All", "Report", "Doc", "Backup", "File"], width=10, state="readonly")
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_settings_tab.py:86: [HARDCODE_PATH] f"workspace_root:\n{new_root}\n"
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_settings_tab.py:93: [HARDCODE_PATH] f"Fehler beim Speichern der Einstellungen:\n{exc}",
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:8: [HARDCODE_PATH] SR_HELP_TEXT_R2134 = 'Service Runner (SR) – Kurzüberblick\n\nSR9997 – FutureFix:\n  Sammel-Button für zukünftige Fixes / Reparaturketten (schnell, experimenteller).\n\nSR1352 – FutureFix Safe:\n  Wie FutureFix, aber konservativer: weniger Risiko, mehr Checks.\n\nSR9998 – Build Tools:\n  Werkzeuge/Build-Helfer (Build/Patch/Tools vorbereiten).\n\nSR9999 – Diagnose:\n  Diagnose-Läufe/Checks (Fehleranalyse, Status, Problemstellen finden).\n\nSR1922 – Systemcheck:\n  System-/Projekt-Check (Struktur, Konsistenz, Basischecks).'
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:17: [HARDCODE_PATH] SR_TEXT_R2133 = 'Service Runner (SR) – Kurzüberblick\n\nSR9997 – FutureFix:\n  Sammel-Button für zukünftige Fixes / Reparaturketten (schnell, experimenteller).\n\nSR1352 – FutureFix Safe:\n  Wie FutureFix, aber konservativer: weniger Risiko, mehr Checks.\n\nSR9998 – Build Tools:\n  Werkzeuge/Build-Helfer (z. B. Tools sammeln, patch/build vorbereiten).\n\nSR9999 – Diagnose:\n  Diagnose-Läufe/Checks (typisch: Fehleranalyse, Status, Problemstellen finden).\n\nSR1922 – Systemcheck:\n  System-/Projekt-Check (Grundgesundheit: Struktur, Dateien, Konsistenz, Basischecks).'
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:709: [REGISTRY] rp = Path(getattr(app, "project_root", "")) / "registry" / "workspaces.json"
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:709: [PROJECT_ROOT] rp = Path(getattr(app, "project_root", "")) / "registry" / "workspaces.json"
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:711: [REGISTRY] rp = Path(__file__).resolve().parent.parent / "registry" / "workspaces.json"
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:745: [COMBOBOX] cb_ws = ttk.Combobox(row_ws, values=_names, width=18, state="readonly", textvariable=app._workspace_name_var)
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:812: [REGISTRY] # 1) registry/public_export_root.txt (one line path)
C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:816: [REGISTRY] reg_file = _PRIVATE_ROOT / "registry" / "public_export_root.txt"
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:2: [REGISTRY] Workspace Registry API (READ-ONLY)
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:4: [REGISTRY] Registry file: registry/workspaces.json
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:31: [REGISTRY] REGISTRY_REL = Path("registry") / "workspaces.json"
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:38: [PROJECT_ROOT] def _project_root(project_root: Optional[str | Path] = None) -> Path:
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:39: [PROJECT_ROOT] if project_root:
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:40: [PROJECT_ROOT] return Path(project_root).resolve()
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:45: [PROJECT_ROOT] def registry_path(project_root: Optional[str | Path] = None) -> Path:
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:46: [PROJECT_ROOT] return _project_root(project_root) / REGISTRY_REL
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:49: [PROJECT_ROOT] def load_registry(project_root: Optional[str | Path] = None) -> Dict[str, Any]:
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:50: [PROJECT_ROOT] rp = registry_path(project_root)
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:53: [PROJECT_ROOT] return {"active": "default", "workspaces": {"default": {"path": str(_project_root(project_root)), "type": "project", "valid": True, "last_seen": _now_iso()}}}
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:58: [PROJECT_ROOT] data = {"active": "default", "workspaces": {"default": {"path": str(_project_root(project_root)), "type": "project", "valid": True, "last_seen": _now_iso()}}}
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:79: [PROJECT_ROOT] data["workspaces"] = {"default": {"path": str(_project_root(project_root)), "type": "project", "valid": True, "last_seen": _now_iso()}}
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:84: [PROJECT_ROOT] def list_workspaces(project_root: Optional[str | Path] = None) -> List[Tuple[str, Path, bool]]:
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:85: [PROJECT_ROOT] data = load_registry(project_root)
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:93: [PROJECT_ROOT] def get_active_workspace_root(project_root: Optional[str | Path] = None) -> Path:
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:94: [PROJECT_ROOT] data = load_registry(project_root)
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:100: [PROJECT_ROOT] return _project_root(project_root)
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:104: [PROJECT_ROOT] def get_active_name(project_root: Optional[str | Path] = None) -> str:
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:105: [PROJECT_ROOT] data = load_registry(project_root)
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:109: [PROJECT_ROOT] def explain_active(project_root: Optional[str | Path] = None) -> str:
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:110: [PROJECT_ROOT] data = load_registry(project_root)
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:117: [PROJECT_ROOT] def save_registry(data: Dict[str, Any], project_root: Optional[str | Path] = None) -> bool:
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:118: [REGISTRY] """Write registry/workspaces.json. Returns True on success."""
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:120: [PROJECT_ROOT] rp = registry_path(project_root)
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:128: [PROJECT_ROOT] def set_active_workspace(name: str, project_root: Optional[str | Path] = None) -> bool:
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:131: [PROJECT_ROOT] data = load_registry(project_root)
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:137: [PROJECT_ROOT] _ = load_registry(project_root)  # normalize once
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:138: [PROJECT_ROOT] data = load_registry(project_root)
C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py:140: [PROJECT_ROOT] return save_registry(data, project_root)
