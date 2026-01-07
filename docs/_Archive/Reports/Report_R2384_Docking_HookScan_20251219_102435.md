# Report R2384 – Docking Hook-Scan (READ-ONLY)

- Timestamp: 2025-12-19 10:24:35
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- Files scanned (preferred set): 83
- Files mentioning keys: 38

## Fokus-Keys
- `runner_products`
- `log`
- `pipeline`

## main_gui.py
### Key mentions
- line 9: `from modules import ui_menus, ui_toolbar, ui_filters, ui_project_tree, ui_left_panel, ui_leds, ui_theme_classic, config_manager, ui_settings_tab, ui_pipeline_tab, ui_runner_products_tab, exception_logger, module_docking`
- line 11: `# --- R2296: Import-Pfade beim Start in debug_output.txt loggen (Guard gegen "anderes Root / falscher Import") ---`
- line 12: `def _r2296_log_import_paths_once() -> None:`
- line 19: `            from modules import logic_actions as _la`
- line 20: `            parts.append(f"logic_actions={getattr(_la, '__file__', '?')}")`
- line 22: `            parts.append(f"logic_actions=ERR:{e}")`
- line 34: `            from modules import exception_logger as _elog`
- line 35: `            parts.append(f"exception_logger={getattr(_elog, '__file__', '?')}")`
- line 37: `            parts.append(f"exception_logger=ERR:{e}")`
- line 45: `_r2296_log_import_paths_once()`
- line 54: `from modules import config_loader, ui_log_tab`
- line 90: `            from modules.logic_actions import _learning_log_event`
- line 91: `            _learning_log_event(self, 'app_start', {})`
- line 98: `                    from modules.logic_actions import _learning_log_event`
- line 100: `                    _learning_log_event(self, 'tab_change', {'tab': tab})`
- line 165: `        # R2053: Log-Tab als 2. Tab`
- line 166: `        self.tab_log = tk.Frame(self.nb, bg=ui_theme_classic.BG_MAIN)`
- line 167: `        self.nb.add(self.tab_log, text="Log")`
- line 169: `            ui_log_tab.build_log_tab(self.tab_log, self)`
- line 179: `        # R2099: Pipeline-Tab (Read-Only Viewer fuer docs/PIPELINE.md)`
- line 180: `        self.tab_pipeline = tk.Frame(self.nb, bg=ui_theme_classic.BG_MAIN)`
- line 181: `        self.nb.add(self.tab_pipeline, text="Pipeline")`
- line 183: `            ui_pipeline_tab.build_pipeline_tab(self.tab_pipeline, self)`
- line 189: `        self.tab_runner_products = tk.Frame(self.nb, bg=ui_theme_classic.BG_MAIN)`
- line 190: `        self.nb.add(self.tab_runner_products, text="Artefakte")`
- line 192: `            ui_runner_products_tab.build_runner_products_tab(self.tab_runner_products, self)`
- line 198: `            # Phase-1: nur Read-Only Tabs (Pipeline/Runner-Produkte/Log) als Extra-Viewer`
- line 264: `        """Status-Bridge für logic_actions."""`
- line 282: `            from modules import config_loader, ui_log_tab`
- line 350: `            from modules import config_loader, ui_log_tab`
- line 440: `        # Zielordner als StringVar - wird von logic_actions defensiv gelesen (geladen aus INI)`
- line 475: `                from modules import logic_actions`
- line 476: `                logic_actions.action_detect(self)`
- line 670: `    exception_logger.install(ROOT)`

### Docking module refs
- line 9: `from modules import ui_menus, ui_toolbar, ui_filters, ui_project_tree, ui_left_panel, ui_leds, ui_theme_classic, config_manager, ui_settings_tab, ui_pipeline_tab, ui_runner_products_tab, exception_logger, module_docking`
- line 196: `        # R2322: Dock/Undock Context-Menu (Read-Only Tabs) BEGIN`
- line 199: `            module_docking.install_notebook_context_menu(self, self.nb)`
- line 202: `        # R2322: Dock/Undock Context-Menu (Read-Only Tabs) END`
- line 621: `        # Oberes Grid fuer die Toolbars + darunter PanedWindow fuer Panels`
- line 642: `        # PanedWindow nur fuer die Panels (unterhalb der Toolbars)`
- line 646: `        # Linker/ rechter Panelbereich im Splitter`
- line 653: `        # Panels`
- line 654: `        left = ui_left_panel.build_left_panel(left_frame, self)`
- line 707: `        dm = getattr(app, "_dock_manager", None)`

### Restore/startup
- line 589: `            # Intake erzeugt hier keine eigenen AOT/Restart-Buttons mehr.`
- line 592: `            self._btn_restart = None`
- line 704: `# R2369_CALL_PERSIST_ON_RESTART`

### Close hooks
- line 258: `            self._init_close_protocol()`
- line 400: `    def _init_close_protocol(self) -> None:`
- line 402: `        def _on_close() -> None:`
- line 408: `                self.destroy()`
- line 415: `            self.protocol("WM_DELETE_WINDOW", _on_close)`

### Geometry/centering
- line 109: `        self.geometry("1300x780")`
- line 310: `                self.geometry(geo)`
- line 374: `                    geo = self.winfo_geometry()`
- line 680: `def _r2368_apply_main_geometry(app):`
- line 697: `                app.geometry(geo)`

### INI calls
- line 9: `from modules import ui_menus, ui_toolbar, ui_filters, ui_project_tree, ui_left_panel, ui_leds, ui_theme_classic, config_manager, ui_settings_tab, ui_pipeline_tab, ui_runner_products_tab, exception_logger, module_docking`
- line 128: `                _cfg_top.save(cfg)`
- line 396: `            config_loader.save(cfg)`
- line 452: `                from modules import config_manager as _cfg_mgr`


## modules\context_state.py
### Key mentions
- line 5: `- Zentrale, kleine Zustands-Sammlung für ShrimpDev (UI / Agent / Pipeline).`
- line 54: `    """Persistiert Context als JSON (optional, Debug/Pipeline)."""`


## modules\exception_logger.py
### Key mentions
- line 1: `# exception_logger.py - central exception logging (no triple-quotes)`
- line 36: `def log_exception(exc: BaseException, context: str = '') -> None:`
- line 112: `# Central Log API (R2226)`
- line 114: `# debug_output.txt schreibt. Bestehendes Exception-Logging bleibt unverändert.`
- line 123: `def log_event(source: str, message: str, level: str = 'INFO') -> None:`
- line 132: `def log_runner_start(runner_id: str, label: str = '') -> None:`
- line 136: `    log_event('RUNNER', msg, 'INFO')`
- line 138: `def log_runner_end(runner_id: str, exit_code: int) -> None:`
- line 140: `    log_event('RUNNER', f'Runner END rid={rid} exit={exit_code}', 'INFO')`
- line 142: `def log_runner_output(runner_id: str, text: str, stream: str = 'STDOUT') -> None:`
- line 150: `    # Split into lines to keep log readable; preserve order.`
- line 152: `        log_event('RUNNER', f'{rid} {st}: {ln}', 'INFO')`
- line 154: `# === RUNNER_LOG_API_BEGIN ===`
- line 158: `def _runner_log_path() -> _Path:`
- line 160: `    # __file__ = ...\modules\exception_logger.py`
- line 169: `    p = _runner_log_path()`
- line 184: `def log_runner_start(runner_id: str, label: str = '') -> None:`
- line 190: `def log_runner_output(runner_id: str, text: str, stream: str = 'STDOUT') -> None:`
- line 199: `def log_runner_end(runner_id: str, exit_code: int | str = 0) -> None:`
- line 203: `# === RUNNER_LOG_API_END ===`


## modules\ini_writer.py
### Key mentions
- line 5: `# - source logging`
- line 13: `    def __init__(self, ini_path=None, logger=None):`
- line 15: `        self._logger = logger`
- line 31: `    def _log(self, msg):`
- line 33: `            if self._logger:`
- line 34: `                self._logger(msg)`
- line 57: `            self._log('set ' + section + '.' + str(key) + ' source=' + str(source))`
- line 68: `            self._log('update_many ' + section + ' keys=' + str(len(dict_values)) + ' source=' + str(source))`
- line 118: `                self._log('save_merge_atomic ok path=' + path + ' source=' + str(source))`
- line 126: `                self._log('save_merge_atomic FAILED ' + repr(e) + ' source=' + str(source))`

### Docking module refs
- line 144: `PRESERVE_SECTIONS_DEFAULT = {"Docking"}`
- line 168: `    if "Docking" not in updates and base.has_section("Docking"):`
- line 169: `        docking_items = dict(base.items("Docking"))`
- line 177: `    if "Docking" not in updates and 'docking_items' in locals():`
- line 178: `        if not base.has_section("Docking"):`
- line 179: `            base.add_section("Docking")`
- line 180: `        for k, v in docking_items.items():`
- line 181: `            base.set("Docking", k, v)`

### INI calls
- line 1: `# ini_writer.py`
- line 157: `def merge_write_ini(project_root: Path,`


## modules\learning_engine\__init__.py
### Key mentions
- line 3: `from .action_logger import ActionLogger`


## modules\learning_engine\action_logger.py
### Key mentions
- line 1: `# action_logger.py`
- line 4: `class ActionLogger:`
- line 8: `    def log(self, event_type: str, payload: dict):`


## modules\learning_engine\engine_core.py
### Key mentions
- line 4: `from .action_logger import ActionLogger`
- line 12: `        self.logger = ActionLogger(self.persistence)`
- line 17: `    def log(self, event_type: str, payload: dict):`
- line 18: `        self.logger.log(event_type, payload)`


## modules\learning_engine.py
### Key mentions
- line 74: `def _get_debug_log_path() -> Path:`
- line 76: `    Liefert den Pfad zur zentralen Debug-Logdatei.`
- line 82: `# Logging`
- line 86: `def _log_debug(message: str) -> None:`
- line 89: `    Fehler beim Loggen dürfen niemals das Programm abbrechen.`
- line 92: `        log_path = _get_debug_log_path()`
- line 93: `        log_path.parent.mkdir(parents=True, exist_ok=True)`
- line 96: `        with log_path.open("a", encoding="utf-8") as f:`
- line 99: `        # Niemals Exceptions durch Logging nach außen lecken`
- line 104: `# Journal-Lade-/Speicherlogik`
- line 122: `        _log_debug("Journal nicht gefunden - neue Struktur wird angelegt.")`
- line 138: `        _log_debug(f"Journal-Laden fehlgeschlagen: {exc!r} - verwende leere Struktur.")`
- line 167: `        _log_debug(f"Journal-Speichern fehlgeschlagen: {exc!r}")`
- line 268: `    _log_debug(f"learn_from_event: {entry.event} id={entry.id} payload_keys={list(entry.payload.keys())}")`
- line 303: `    _log_debug(f"update_journal: {entry.event} id={entry.id}")`


## modules\logic_actions.py
### Key mentions
- line 3: `# logic_actions.py - FULL RESTORE VERSION (R1514)`
- line 22: `def log_debug(msg: str):`
- line 30: `        do_log = cfg.get_logging_bool("gui_debug", True)`
- line 31: `        use_ts = cfg.get_logging_bool("timestamps", True)`
- line 33: `        if not do_log:`
- line 39: `        log_path = root / "debug_output.txt"`
- line 40: `        # R2045: Logrotation`
- line 42: `            max_size_mb = int(cfg._config.get("logging", "max_size_mb", fallback="5"))`
- line 46: `            rotations = int(cfg._config.get("logging", "rotations", fallback="5"))`
- line 54: `        def _rotate_log(path, max_mb, max_rot):`
- line 73: `        _rotate_log(log_path, max_size_mb, rotations)`
- line 74: `        with open(log_path, "a", encoding="utf-8") as f:`
- line 499: `# R1827: LearningEngine-Logging-Hook (defensiv, Zusatz)`
- line 501: `def _learning_log_event(app, event_type: str, payload: Optional[dict] | None = None) -> None:`
- line 502: `    # R2082: Sicheres Logging-Hook fuer LearningEngine und LearningJournal.`
- line 533: `        lj_handler = getattr(_lj, 'learning_log_event', None)`
- line 563: `            # LearningJournal-Logging ist diagnostisch – Fehler werden geschluckt`
- line 566: `        # LJ-Logging darf ebenfalls niemals Intake/Runner crashen`
- line 708: `        _learning_log_event(app, "intake_new", "ok")  # type: ignore[name-defined]`
- line 721: `            _learning_log_event(app, "intake_save", "no_widgets")  # type: ignore[name-defined]`
- line 770: `            _learning_log_event(app, "intake_save", "ok")  # type: ignore[name-defined]`
- line 776: `            _learning_log_event(app, "intake_save", "error")  # type: ignore[name-defined]`
- line 791: `            _learning_log_event(app, "intake_undo", "ok")  # type: ignore[name-defined]`
- line 799: `    """Startet die aktuell gespeicherte Intake-Datei IMMER über module_runner_exec (zentraler Log-Pfad)."""`
- line 834: `            _learning_log_event(app, "intake_run", "ok_central")  # type: ignore[name-defined]`
- line 840: `            _learning_log_event(app, "intake_run", "error")  # type: ignore[name-defined]`
- line 1278: `            # Immer ins Log schreiben, Popup nur wenn Flag == True`
- line 1279: `            # Zentraler Runner-Log (exception_logger)`
- line 1281: `                from . import exception_logger as _elog  # type: ignore`
- line 1294: `                    _elog.log_runner_start(runner_id, label)`
- line 1299: `                        _elog.log_runner_output(runner_id, _trunc(out), "STDOUT")`
- line 1304: `                        _elog.log_runner_output(runner_id, _trunc(err), "STDERR")`
- line 1308: `                    _elog.log_runner_end(runner_id, proc.returncode)`
- line 1582: `    """Liefert den workspace_root fuer Dateioperationen in logic_actions.`
- line 1834: `#     from tkinter import simpledialog as _r1840_simpledialog`
- line 1838: `#     _r1840_simpledialog = None`
- line 1841: `# def _r1840_log(msg):`
- line 1842: `#     """Lokales Logging fuer Toolbar-Aktionen (R1840)."""`
- line 1847: `#         log_path = _r1840_os.path.join(root_dir, "debug_output.txt")`
- line 1849: `#         with open(log_path, "a", encoding="utf-8") as f:`
- line 1862: `#     _r1840_log("INFO [" + str(title) + "]: " + str(text))`
- line 1872: `#     _r1840_log("ERROR [" + str(title) + "]: " + str(text))`
- line 1881: `#     _r1840_log("ASK-YESNO [" + str(title) + "]: " + str(text) + " -> fallback=True")`
- line 1886: `#     if _r1840_simpledialog is not None:`
- line 1888: `#             return _r1840_simpledialog.askstring(title, prompt, initialvalue=initial)`
- line 1891: `#     _r1840_log("ASK-STRING [" + str(title) + "]: " + str(prompt) + " (kein Dialog verfuegbar)")`
- line 2006: `#         _r1840_log("Delete: " + path + " -> " + trash)`
- line 2047: `#         _r1840_log("Rename: " + path + " -> " + new_path)`
- line 2072: `#                     _r1840_log("Undo Delete: " + trash + " -> " + orig)`
- line 2086: `#                     _r1840_log("Undo Rename: " + new_path + " -> " + old_path)`
- line 2137: `#     # Fallback: nur Log (falls vorhanden)`
- line 2139: `#         from modules.logic_actions import log_debug as _r1841_log_debug  # type: ignore`
- line 2140: `#         _r1841_log_debug("[R1841-INFO] " + str(title) + ": " + str(text))`
- line 2153: `#         from modules.logic_actions import log_debug as _r1841_log_debug  # type: ignore`
- line 2154: `#         _r1841_log_debug("[R1841-ERROR] " + str(title) + ": " + str(text))`
- line 2167: `#         from modules.logic_actions import log_debug as _r1841_log_debug  # type: ignore`
- line 2168: `#         _r1841_log_debug("[R1841-ASK-YESNO] " + str(title) + ": " + str(text) + " -> fallback=True")`
- line 2678: `    from tkinter import simpledialog as _r2066_sd`

### Docking module refs
- line 1169: `            win = _r1851_tk.Toplevel(app)`
- line 1171: `            win = _r1851_tk.Toplevel()`
- line 1430: `            if isinstance(app, _r1852_tk.Tk) or isinstance(app, _r1852_tk.Toplevel):`
- line 1437: `        win = _r1852_tk.Toplevel(parent)`
- line 2328: `#         win = _r1846_tk.Toplevel()`
- line 2430: `#         win = _r1847_tk.Toplevel()`
- line 2587: `#         win = _r1849_tk.Toplevel()`

### Create/show window
- line 1169: `            win = _r1851_tk.Toplevel(app)`
- line 1171: `            win = _r1851_tk.Toplevel()`
- line 1188: `            win.lift()`
- line 1437: `        win = _r1852_tk.Toplevel(parent)`
- line 1445: `            win.lift()`
- line 2328: `#         win = _r1846_tk.Toplevel()`
- line 2430: `#         win = _r1847_tk.Toplevel()`
- line 2587: `#         win = _r1849_tk.Toplevel()`

### Restore/startup
- line 3: `# logic_actions.py - FULL RESTORE VERSION (R1514)`

### Close hooks
- line 1231: `        def _on_close():`
- line 1237: `                win.destroy()`
- line 1241: `        btn_close = _r1851_tk.Button(ctrl, text="Schliessen", command=_on_close)`
- line 1484: `        def _on_close():`
- line 1490: `                win.destroy()`
- line 1494: `        btn_close = _r1852_tk.Button(ctrl, text="Schliessen", command=_on_close)`

### Geometry/centering
- line 1173: `        win.geometry("900x600")`
- line 1174: `        # R2213: center+topmost runner popup (existing popup, no new UI)`
- line 1177: `            sw = win.winfo_screenwidth()`
- line 1178: `            sh = win.winfo_screenheight()`
- line 1183: `            win.geometry(f"{w}x{h}+{x}+{y}")`
- line 1439: `        win.geometry("900x600")`
- line 2330: `#         win.geometry("700x600")`
- line 2432: `#         win.geometry("900x600")`
- line 2589: `#         win.geometry("900x600")`

### INI calls
- line 713: `def action_save(app) -> None:`
- line 1127: `    '''ShrimpDev.ini ueber modules.config_loader.save() speichern.'''`
- line 1133: `        _r1851_cfg.save(cfg)`
- line 1387: `    """ShrimpDev.ini ueber modules.config_loader.save() speichern."""`
- line 1393: `        _r1852_cfg.save(cfg)`
- line 1579: `from modules import module_runner_exec, config_manager as _cfg_actions`


## modules\logic_tools.py
### Key mentions
- line 2: `SonderRunner-Logik - als modulare Funktionen, auf Buttons verdrahtet.`


## modules\module_agent.py
### Key mentions
- line 76: `def _debug_log(msg: str) -> None:`
- line 77: `    """Zentraler Debug-Log: schreibt nach debug_output.txt im Projekt-Root."""`
- line 563: `    def _pipeline_path() -> Path:`
- line 564: `        return _project_root() / "docs" / "PIPELINE.md"`
- line 566: `    def _insert_pipeline_item(line: str) -> bool:`
- line 567: `        p = _pipeline_path()`
- line 655: `            _debug_log("Agent-Update Exception: " + repr(e))`
- line 673: `            _debug_log("Agent run_selected failed: " + repr(exc))`
- line 694: `    def _add_to_pipeline() -> None:`
- line 705: `            ok = _ui_msg(app, 'ask', "Pipeline", "In docs/PIPELINE.md eintragen?\n\n" + line)`
- line 710: `        if _insert_pipeline_item(line):`
- line 711: `            _ui_msg(app, 'info', "Pipeline", "Eingetragen.")`
- line 713: `            _ui_msg(app, 'info', "Pipeline", "Konnte nicht eintragen (PIPELINE.md fehlt/gesperrt).")`
- line 720: `    ttk.Button(btnrow, text="In Pipeline", command=_add_to_pipeline).pack(side="left", padx=(8, 0))`

### Restore/startup
- line 365: `    # Restart-Loop Verdacht`
- line 371: `        warnings.append('WARN: Viele app_start in 5 Min ({}). Verdacht: Restart-Loop.'.format(app_starts_5m))`

### Geometry/centering
- line 11: `# UI_POPUP_CENTER_R2174`
- line 535: `    tree.column("exists", width=45, stretch=False, anchor="center")`


## modules\module_code_intake.py
### Key mentions
- line 15: `    # FINAL FIX: Intake-Run MUSS Runner-ID verwenden (Logging garantiert)`


## modules\module_docking.py
### Key mentions
- line 224: `        # key: 'pipeline' | 'runner_products' | 'log'`
- line 238: `        # R2355_DOCK_DIAG: log INI + restore decision (no behavior change)`
- line 466: `            from modules import ui_pipeline_tab`
- line 467: `            mapping['pipeline'] = ('Pipeline', ui_pipeline_tab.build_pipeline_tab)`
- line 471: `            from modules import ui_runner_products_tab`
- line 472: `            mapping['runner_products'] = ('Artefakte', ui_runner_products_tab.build_runner_products_tab)`
- line 476: `            from modules import ui_log_tab`
- line 477: `            mapping['log'] = ('Log', ui_log_tab.build_log_tab)`
- line 524: `            from modules import ui_pipeline_tab`
- line 525: `            targets.append(('Pipeline', 'pipeline', ui_pipeline_tab.build_pipeline_tab))`
- line 529: `            from modules import ui_runner_products_tab`
- line 530: `            targets.append(('Artefakte', 'runner_products', ui_runner_products_tab.build_runner_products_tab))`
- line 534: `            from modules import ui_log_tab`
- line 535: `            targets.append(('Log', 'log', ui_log_tab.build_log_tab))`
- line 640: `            from . import exception_logger`
- line 641: `            exception_logger.log(f"[DOCK_DIAG] {msg}")`
- line 892: `# - keys: main, log, pipeline, runner_products (Artefakte)`
- line 894: `# - Diagnose-Prints (werden im Log-Tab sichtbar)`
- line 1004: `        # 2) Log-Window (best-effort: häufige Attribute)`
- line 1005: `        log_win = None`
- line 1006: `        for name in ("log_window","_log_window","log_toplevel","_log_toplevel","win_log","_win_log"):`
- line 1010: `                    log_win = cand`
- line 1014: `        if log_win is not None:`
- line 1016: `                geo_log = _r2369_safe_geo(log_win)`
- line 1017: `                _r2369_set_record(cfg, "log", True, False, geo_log)`
- line 1019: `                    print("[Docking][R2369] persist log geo=", geo_log)`
- line 1026: `            _r2369_set_record(cfg, "log", False, False, "")`

### Docking module refs
- line 1: `# module_docking.py`
- line 2: `# Dock/Undock Manager (Phase-1): Read-Only Tabs als Extra-Viewer`
- line 53: `# R2339_DOCKING_PERSIST_V1`
- line 54: `# Persist/Restore undocked windows in INI (w/h/x/y). Center only on first open.`
- line 185: `class DockManager:`
- line 188: `        self._wins = {}  # key -> Toplevel`
- line 194: `            return 'Undocked'`
- line 223: `    def undock_readonly(self, key, title, builder_func, restore_geometry=None):`
- line 237: `        w = tk.Toplevel(self.app)`
- line 238: `        # R2355_DOCK_DIAG: log INI + restore decision (no behavior change)`
- line 242: `            sec = 'Docking'`
- line 250: `            _r2355_diag(self.app, f"undock key={key} ini={ini} keys={keys} open={op} geo={geo} w={ww} h={hh} x={xx} y={yy} restore_in={restore_geometry}")`
- line 258: `                sec2 = 'Docking'`
- line 282: `        w.title(self._safe_title(title) + ' (Undocked)')`
- line 287: `            geo = cfg.get("Docking", f"{key}.geometry", fallback="")`
- line 345: `                tk.Label(body, text='Undock-Fehler: ' + repr(exc), anchor='w').pack(anchor='w', padx=8, pady=8)`
- line 363: `            print('[Docking] INI path:', ini)`
- line 367: `        sec = 'Docking'`
- line 399: `            print('[Docking] INI path:', ini)`
- line 403: `        sec = 'Docking'`
- line 423: `            docked_v = str(_r2339_cfg_get(cfg, sec, key + '.docked', '0')).strip()`
- line 425: `            open_v, docked_v = '1', '0'`
- line 426: `        if open_v != '1' or docked_v == '1':`
- line 454: `            print('[Docking] INI path:', ini)`
- line 458: `        sec = 'Docking'`
- line 504: `            self.undock_readonly(key, lab, builder, restore_geometry=restore_geo)`
- line 510: `    # Right-click context menu on tabs for undock (Phase-1: read-only tabs only)`
- line 511: `    dm = getattr(app, '_dock_manager', None)`
- line 513: `        dm = DockManager(app)`
- line 514: `        app._dock_manager = dm`
- line 563: `        menu.add_command(label='Undock', command=lambda: dm.undock_readonly(key, label, builder))`
- line 565: `            menu.add_command(label='Dock (Fenster schließen)', command=lambda: dm.close(key))`
- line 636: `# R2355_DOCK_DIAG`
- line 641: `            exception_logger.log(f"[DOCK_DIAG] {msg}")`
- line 645: `        print(f"[DOCK_DIAG] {msg}")`
- line 651: `# R2367_DOCKING_PERSIST_HARDFIX`
- line 653: `# - garantiertes Schreiben von [Docking] nach ShrimpDev.ini (MERGE-write)`
- line 707: `        print("[Docking][R2367] persist_one key=", key, "ini=", ini)`
- line 712: `    sec = "Docking"`
- line 730: `    cfg.set(sec, key + ".docked", "0")`
- line 750: `        print("[Docking][R2367] persist_all ini=", ini)`
- line 768: `# Monkeypatch in DockManager`
- line 770: `    DockManager._persist_one = _r2367_persist_one`
- line 771: `    DockManager.persist_all = _r2367_persist_all`
- line 777: `# R2368_DOCKING_RESTORE_HARDFIX`
- line 779: `# - Restore aus ShrimpDev.ini [Docking] <key>.geometry (WxH+X+Y)`
- line 832: `    if not cfg.has_section("Docking"):`
- line 835: `    geo = cfg.get("Docking", key + ".geometry", fallback="").strip()`
- line 865: `            print("[Docking][R2368] offscreen -> center key=", key, "geo=", geo)`
- line 873: `            print("[Docking][R2368] restore key=", key, "geo=", geo)`
- line 883: `    DockManager._restore_one = _r2368_restore_one`
- line 889: `# R2369_DOCKING_STATE_V2`
- line 890: `# Docking State v2:`
- line 891: `# - pro Fenster 1 Datensatz: open/docked/geometry/ts`
- line 944: `def _r2369_set_record(cfg, key, open_flag, docked_flag, geo):`
- line 945: `    sec = "Docking"`
- line 949: `    cfg.set(sec, key + ".docked", "1" if docked_flag else "0")`
- line 975: `def _r2369_persist_one(self, key, win, docked_flag=False):`
- line 979: `    _r2369_set_record(cfg, key, True, bool(docked_flag), geo)`
- line 982: `        print("[Docking][R2369] persist key=", key, "geo=", geo, "ts=", cfg.get("Docking", key + ".ts", fallback=""))`
- line 991: `    # 1) Main window (Shrimpi) – falls DockManager app kennt`
- line 998: `                print("[Docking][R2369] persist main geo=", geo_main)`
- line 1006: `        for name in ("log_window","_log_window","log_toplevel","_log_toplevel","win_log","_win_log"):`
- line 1019: `                    print("[Docking][R2369] persist log geo=", geo_log)`
- line 1028: `    # 3) Undocked windows aus _wins`
- line 1039: `                print("[Docking][R2369] persist undocked key=", key, "geo=", geo)`
- line 1051: `    if not cfg.has_section("Docking"):`
- line 1053: `            print("[Docking][R2369] restore key=", key, "no [Docking]")`
- line 1060: `        geo = cfg.get("Docking", key + ".geometry", fallback="").strip()`
- line 1073: `        print("[Docking][R2369] restore key=", key, "geo=", geo, "applied=", applied, "ts=", cfg.get("Docking", key + ".ts", fallback=""))`
- line 1080: `    DockManager.persist_all = _r2369_persist_all`
- line 1081: `    DockManager._persist_one = _r2369_persist_one`
- line 1082: `    DockManager._restore_one = _r2369_restore_one`

### Create/show window
- line 230: `                    w.deiconify()`
- line 231: `                    w.lift()`
- line 237: `        w = tk.Toplevel(self.app)`
- line 305: `                w.deiconify()`

### Restore/startup
- line 54: `# Persist/Restore undocked windows in INI (w/h/x/y). Center only on first open.`
- line 223: `    def undock_readonly(self, key, title, builder_func, restore_geometry=None):`
- line 238: `        # R2355_DOCK_DIAG: log INI + restore decision (no behavior change)`
- line 250: `            _r2355_diag(self.app, f"undock key={key} ini={ini} keys={keys} open={op} geo={geo} w={ww} h={hh} x={xx} y={yy} restore_in={restore_geometry}")`
- line 253: `        # R2352_RESTORE_FIX: ensure restore_geometry from INI x/y/w/h when caller passes None`
- line 255: `            if not restore_geometry:`
- line 272: `                            restore_geometry = str(ww)+'x'+str(hh)+'+'+str(xx)+'+'+str(yy)`
- line 274: `                        restore_geometry = str(ww)+'x'+str(hh)+'+'+str(xx)+'+'+str(yy)`
- line 277: `        # R2352_RESTORE_FIX: removed buggy call (cfg/sec undefined)`
- line 283: `        # R2339: center only on first open; restore geometry if provided`
- line 284: `        _r2355_diag(self.app, f"restore_branch key={key} restore_geometry={restore_geometry!r}")`
- line 285: `        if restore_geometry:`
- line 290: `                restore_geometry = False`
- line 299: `                    w.after_idle(lambda g=str(restore_geometry): w.geometry(g))`
- line 301: `                    w.geometry(str(restore_geometry))`
- line 420: `    def _restore_window_from_ini(self, cfg, sec, key, lab, builder, sw, sh):`
- line 435: `        restore_geo = None`
- line 440: `                    restore_geo = geo`
- line 442: `                restore_geo = None`
- line 444: `        if restore_geo is None and ww > 1 and hh > 1 and sw > 0 and sh > 0:`
- line 446: `                restore_geo = str(ww) + 'x' + str(hh) + '+' + str(xx) + '+' + str(yy)`
- line 448: `        self._restore_window_from_ini(cfg, sec, key, lab, builder, sw, sh)`
- line 451: `    def restore_from_ini(self):`
- line 500: `            restore_geo = None`
- line 503: `                    restore_geo = str(ww) + 'x' + str(hh) + '+' + str(xx) + '+' + str(yy)`
- line 504: `            self.undock_readonly(key, lab, builder, restore_geometry=restore_geo)`
- line 516: `            dm.restore_from_ini()`
- line 633: `# R2352_RESTORE_FIX`
- line 777: `# R2368_DOCKING_RESTORE_HARDFIX`
- line 779: `# - Restore aus ShrimpDev.ini [Docking] <key>.geometry (WxH+X+Y)`
- line 829: `def _r2368_restore_one(self, key, win):`
- line 873: `            print("[Docking][R2368] restore key=", key, "geo=", geo)`
- line 881: `# Monkeypatch: restore hook verfügbar machen`
- line 883: `    DockManager._restore_one = _r2368_restore_one`
- line 1048: `def _r2369_restore_one(self, key, win):`
- line 1053: `            print("[Docking][R2369] restore key=", key, "no [Docking]")`
- line 1073: `        print("[Docking][R2369] restore key=", key, "geo=", geo, "applied=", applied, "ts=", cfg.get("Docking", key + ".ts", fallback=""))`
- line 1082: `    DockManager._restore_one = _r2369_restore_one`

### Close hooks
- line 215: `                w.destroy()`
- line 293: `                w.withdraw()`
- line 321: `                # R2342_FORCE_PERSIST_ON_CLOSE`
- line 349: `        def _on_close():`
- line 353: `            w.protocol('WM_DELETE_WINDOW', _on_close)`
- line 580: `# R2342_FORCE_PERSIST_ON_CLOSE`

### Geometry/centering
- line 11: `def _center_window(win, width, height, parent=None):`
- line 30: `                sw = int(win.winfo_screenwidth())`
- line 31: `                sh = int(win.winfo_screenheight())`
- line 35: `            sw = int(win.winfo_screenwidth())`
- line 36: `            sh = int(win.winfo_screenheight())`
- line 47: `        win.geometry(str(width) + 'x' + str(height) + '+' + str(x) + '+' + str(y))`
- line 54: `# Persist/Restore undocked windows in INI (w/h/x/y). Center only on first open.`
- line 132: `# R2340_WM_GEOMETRY_FIX`
- line 266: `                        sw = _r2339_safe_int(self.app.winfo_screenwidth(), 0)`
- line 267: `                        sh = _r2339_safe_int(self.app.winfo_screenheight(), 0)`
- line 283: `        # R2339: center only on first open; restore geometry if provided`
- line 289: `                win.geometry(geo)`
- line 299: `                    w.after_idle(lambda g=str(restore_geometry): w.geometry(g))`
- line 301: `                    w.geometry(str(restore_geometry))`
- line 310: `                _center_window(w, 900, 700, parent=self.app)`
- line 379: `            g = w.wm_geometry()`
- line 484: `            sw = _r2339_safe_int(self.app.winfo_screenwidth(), 0)`
- line 485: `            sh = _r2339_safe_int(self.app.winfo_screenheight(), 0)`
- line 584: `def _r2351_apply_ini_geometry(w, cfg, sec, key, center_fn=None):`
- line 586: `    Priority: <key>.geometry, else build from w/h/x/y. Center only if nothing usable or offscreen.`
- line 607: `                w.geometry(geo)`
- line 610: `            # offscreen guard (single monitor): clamp to visible area, else center`
- line 613: `                sx = w.winfo_screenwidth(); sy = w.winfo_screenheight()`
- line 616: `                    if center_fn:`
- line 617: `                        center_fn(w)`
- line 621: `            if center_fn:`
- line 622: `                center_fn(w)`
- line 624: `        if center_fn:`
- line 626: `                center_fn(w)`
- line 654: `# - Persist aus wm_geometry() (WxH+X+Y)`
- line 722: `        geo = str(win.wm_geometry())`
- line 780: `# - Offscreen-Schutz -> fallback center`
- line 817: `        sw = int(win.winfo_screenwidth())`
- line 818: `        sh = int(win.winfo_screenheight())`
- line 851: `        # fallback center (nur dann!)`
- line 853: `            if hasattr(self, "_center_window"):`
- line 854: `                self._center_window(win)`
- line 856: `                # fallback center minimal`
- line 857: `                sw = int(win.winfo_screenwidth())`
- line 858: `                sh = int(win.winfo_screenheight())`
- line 861: `                win.geometry(str(w) + "x" + str(h) + "+" + str(nx) + "+" + str(ny))`
- line 865: `            print("[Docking][R2368] offscreen -> center key=", key, "geo=", geo)`
- line 871: `        win.geometry(geo)`
- line 971: `        return str(win.wm_geometry())`
- line 1067: `            win.geometry(geo)`


## modules\module_gate_smoke.py
### Key mentions
- line 11: `def _log(msg, dbg_path=r"C:\Users\rasta\OneDrive\ShrimpDev\debug_output.txt"):`
- line 24: `        _log(f"SMOKE OK: {path}")`
- line 27: `        _log(f"SMOKE FAIL: {path} :: {e}")`
- line 34: `        _log(f"IMPORT OK: {fullname}")`
- line 39: `        _log(f"IMPORT FAIL: {fullname}\n{buf.getvalue()}")`


## modules\module_learningjournal.py
### Key mentions
- line 17: `- Fehler (keine Datei, JSON-Fehler, etc.) werden im UI angezeigt und geloggt.`
- line 34: `LOG_FILE_NAME = "debug_output.txt"`
- line 37: `def _log(message: str) -> None:`
- line 46: `        with (ROOT / LOG_FILE_NAME).open("a", encoding="utf-8") as f:`
- line 49: `        # Logging darf die GUI nicht zerstoeren`
- line 123: `        _log("learning_journal.json nicht gefunden.")`
- line 131: `        _log(msg)`
- line 135: `    _log("LearningJournal geladen: {} Eintraege aus {}".format(len(entries), path))`
- line 141: `def learning_log_event(event_type: str, message: str, data: Optional[Dict[str, Any]] = None) -> None:`
- line 148: `    Die Funktion ist defensiv implementiert: Fehler werden geloggt,`
- line 154: `        # Pfad bestimmen (bestehende Logik wiederverwenden)`
- line 165: `                _log(`
- line 166: `                    f"learning_log_event: Fehler beim Lesen von {path}: {exc} - neues Journal wird angelegt."`
- line 224: `            _log(f"learning_log_event: Fehler beim Schreiben von {path}: {exc}")`
- line 232: `        _log(f"Learning-Eintrag geschrieben: type={event_type}, id={entry['id']}")`
- line 234: `        _log(f"learning_log_event: unerwarteter Fehler: {exc}")`
- line 491: `                _log('R1802.cmd nicht gefunden unter ' + str(cmd_path))`
- line 497: `            _log('run_diagnose: Fehler: ' + repr(exc))`
- line 525: `    _log('LearningJournal-Tab (Filter/Suche) gebaut und initial geladen.')`

### Docking module refs
- line 302: `    root = parent.winfo_toplevel()`

### Create/show window
- line 302: `    root = parent.winfo_toplevel()`


## modules\module_runner_exec.py
### Key mentions
- line 6: `- Nicht-blockierend (Thread), zentrale Logs + Reportdatei`
- line 15: `from modules.exception_logger import (`
- line 16: `    log_runner_start,`
- line 17: `    log_runner_end,`
- line 18: `    log_runner_output,`
- line 24: `LOGFILE = os.path.join(ROOT, "debug_output.txt")`
- line 29: `def _log(msg: str) -> None:`
- line 30: `    os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)`
- line 31: `    with open(LOGFILE, "a", encoding="utf-8", newline="") as f:`
- line 80: `        _log(f"[RunnerExec] {_ts()} BAT erzeugt: { _norm_rel(bat_abs) }")`
- line 82: `        _log(f"[RunnerExec] {_ts()} BAT vorhanden: { _norm_rel(bat_abs) }")`
- line 111: `        _log(f"[RunnerExec] {_ts()} START { _norm_rel(bat_abs) } (timeout={timeout_sec}s)")`
- line 112: `        log_runner_start(base, title or '')`
- line 114: `        log_runner_output(base, res.get('output',''))`
- line 117: `        _log(f"[RunnerExec] {_ts()} ENDE RC={res['rc']} Dauer={res['duration']:.2f}s Report={_norm_rel(report_path)}")`
- line 118: `        log_runner_end(base, res.get('rc', -1))`
- line 125: `# R1167g: safe _log wrapper (append, no-replace)`
- line 126: `# Diese Neudefinition überschreibt die vorherige _log()-Funktion sicher.`
- line 127: `def _log(msg: str) -> None:  # noqa: F811 (absichtliche Neudefinition)`
- line 129: `        # Sicherstellen, dass LOGFILE-Verzeichnis existiert, Fehler still tolerieren`
- line 131: `            os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)`
- line 136: `            with open(LOGFILE, "a", encoding="utf-8", newline="") as f:`
- line 143: `# R2249_CENTRAL_RUNNER_LOGGING`
- line 153: `def _r2249_log_end(runner_id: str, title: str, exit_code: int, stdout_tail: str = '') -> None:`
- line 157: `        if hasattr(exception_logger, 'log_runner_end'):`
- line 158: `            exception_logger.log_runner_end(runner_id, title, exit_code, stdout_tail)`


## modules\module_runner_popup.py
### Key mentions
- line 241: `        # Logging`
- line 243: `            from modules import exception_logger as _elog`
- line 245: `            _elog = None`
- line 269: `        def _log_start():`
- line 271: `                if _elog is not None:`
- line 272: `                    _elog.log_runner_start(str(rid), base)`
- line 276: `        def _log_line(line: str):`
- line 278: `                if _elog is not None:`
- line 279: `                    _elog.log_runner_output(str(rid), str(line).rstrip("\n"), "STDOUT")`
- line 283: `        def _log_end(rc: int):`
- line 285: `                if _elog is not None:`
- line 286: `                    _elog.log_runner_end(str(rid), int(rc))`
- line 291: `            _log_line(msg)`
- line 307: `            _log_end(rc)`
- line 345: `        _log_start()`

### Docking module refs
- line 76: `def _center_window(win: tk.Toplevel) -> None:`
- line 78: `    Zentriere ein Toplevel über seinem Master (oder Bildschirm).`
- line 180: `        win = tk.Toplevel(master)`

### Create/show window
- line 32: `    CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)`
- line 34: `    CREATE_NO_WINDOW = 0`
- line 138: `                creationflags=CREATE_NO_WINDOW,`
- line 180: `        win = tk.Toplevel(master)`
- line 184: `                win.transient(master)  # zentral über ShrimpDev`
- line 188: `            win.lift()`

### Close hooks
- line 231: `                win.destroy()`
- line 239: `        win.protocol("WM_DELETE_WINDOW", _close)`

### Geometry/centering
- line 76: `def _center_window(win: tk.Toplevel) -> None:`
- line 91: `            mw = win.winfo_screenwidth()`
- line 92: `            mh = win.winfo_screenheight()`
- line 96: `        mw = win.winfo_screenwidth()`
- line 97: `        mh = win.winfo_screenheight()`
- line 107: `    win.geometry("+{}+{}".format(x, y))`
- line 194: `            win.geometry("1000x650")`
- line 349: `            _center_window(win)`


## modules\module_runnerbar.py
### Key mentions
- line 10: `LOG = ROOT / "debug_output.txt"`
- line 12: `def _log(msg: str) -> None:`
- line 14: `    LOG.parent.mkdir(exist_ok=True, parents=True)`
- line 15: `    with LOG.open("a", encoding="utf-8", newline="") as f:`
- line 20: `        _log(f"SKIP: {cmd_path.name} nicht gefunden.")`
- line 23: `        _log(f"START: {cmd_path}")`
- line 28: `        _log(f"ERROR: {ex!r}")`


## modules\module_settings_ui.py
### Key mentions
- line 3: `from tkinter import ttk, messagebox, filedialog`
- line 26: `        d = filedialog.askdirectory(title="Workspace wählen", initialdir=str(Path(var_ws.get() or r"D:\\")))`

### INI calls
- line 15: `def _save(conf: dict):`
- line 34: `        _save(conf)`


## modules\move_journal.py
### Key mentions
- line 179: `# fuer sicheres Logging und Delete-Operationen dar.`


## modules\snippets\logger_snippet.py
### Key mentions
- line 26: `def write_log(prefix: str, message: str) -> None:`
- line 27: `    """Zentraler Logger mit Fallback & einfacher Rotation."""`


## modules\snippets\runner_template.py
### Key mentions
- line 2: `from modules.snippets.snippet_log_runner import log_runner`
- line 4: `    log_runner(f"[{RUNNER_ID}] Runner gestartet")`
- line 6: `    log_runner(f"[{RUNNER_ID}] Runner beendet")`


## modules\snippets\snippet_dev_intake_toolbar.py
### Key mentions
- line 6: `- Buttons: Analyse / Master-Sanity / Gate-Check / Logs / Runner`
- line 56: `        ("Logs aktualisieren", "_restart_tail", "Log-Tail-Handler fehlt in diesem Intake."),`

### Restore/startup
- line 56: `        ("Logs aktualisieren", "_restart_tail", "Log-Tail-Handler fehlt in diesem Intake."),`


## modules\snippets\snippet_file_ops.py
### Key mentions
- line 13: `LOG  = os.path.join(ROOT, "debug_output.txt")`
- line 15: `def _log(msg: str):`
- line 18: `        with open(LOG, "a", encoding="utf-8") as f:`
- line 73: `    _log(f"Move OK: {src} -> {dst}")`

### INI calls
- line 45: `    def _save(self, data):`
- line 52: `        self._save(data)`
- line 58: `        self._save(data)`


## modules\snippets\snippet_log_runner.py
### Key mentions
- line 2: `# R2044 – Logging Snippet fuer neue Runner`
- line 7: `def log_runner(msg: str):`
- line 11: `        do_log = cfg.get_logging_bool("runner_debug", True)`
- line 12: `        use_ts = cfg.get_logging_bool("timestamps", True)`
- line 14: `        if not do_log:`
- line 20: `        log_path = root / "debug_output.txt"`
- line 21: `        # R2045: Logrotation`
- line 23: `            max_size_mb = int(cfg._config.get("logging", "max_size_mb", fallback="5"))`
- line 27: `            rotations = int(cfg._config.get("logging", "rotations", fallback="5"))`
- line 35: `        def _rotate_log(path, max_mb, max_rot):`
- line 54: `        _rotate_log(log_path, max_size_mb, rotations)`
- line 55: `        with open(log_path, "a", encoding="utf-8") as f:`


## modules\snippets\snippet_syntax_guard.py
### Key mentions
- line 60: `        logical = line.rstrip("\n")`
- line 69: `                    line_text=logical,`
- line 80: `                    line_text=logical,`
- line 84: `        if logical.rstrip(" ") != logical:`
- line 91: `                    line_text=logical,`


## modules\tools\patchlib_guard.py
### Key mentions
- line 153: `# ---------- Safe write pipeline ----------`
- line 157: `    Pipeline: Backup -> Transform -> Gates (future/syntax) -> Commit or Rollback`


## modules\ui_buttons.py
### Key mentions
- line 12: `    tk.Button(frm, text="Open Logs",     command=lambda: _open_logs(app)).grid(row=0, column=4, padx=6)`
- line 15: `    from .logic_intake import do_scan`
- line 31: `        for mod in ("modules.ui_menus","modules.ui_buttons","modules.ui_lists","modules.ui_statusbar","modules.ui_themes","modules.logic_intake"):`
- line 40: `        import tkinter.simpledialog as sd`
- line 50: `def _open_logs(app):`
- line 57: `                messagebox.showinfo("Logs", path)`
- line 59: `            messagebox.showinfo("Logs", "debug_output.txt nicht gefunden.")`
- line 61: `        messagebox.showerror("Logs", str(ex))`


## modules\ui_filters.py
### Key mentions
- line 3: `from tkinter import filedialog`
- line 9: `    path = filedialog.askdirectory(initialdir=var.get() or os.getcwd())`
- line 28: `        # Neue Logik: direkt ui_project_tree verwenden`

### Docking module refs
- line 25: `    Wird u.a. von ui_left_panel._on_target_changed() genutzt.`
- line 70: `    Die eigentliche Steuerung fuer Name/Endung liegt jetzt im linken Intake-Panel`
- line 71: `    (ui_left_panel). Hier stellen wir nur sicher, dass app.name_var und app.ext_var`

### INI calls
- line 43: `    config_loader.save(cfg)`
- line 57: `    config_loader.save(cfg)`


## modules\ui_leds.py
### Key mentions
- line 241: `        # Echte Syntaxfehler -> ROT + Log (nur einmal pro App-Lebensdauer)`
- line 243: `            from modules.logic_actions import log_debug`
- line 244: `            if not getattr(app, "_syntax_led_syntax_error_logged", False):`
- line 245: `                log_debug(f"SyntaxLED: Parsefehler im Intake-Code: {exc}")`
- line 246: `                setattr(app, "_syntax_led_syntax_error_logged", True)`
- line 303: `        # Andere Fehler im Parser -> neutral + Log (nur einmal pro App-Lebensdauer)`
- line 305: `            from modules.logic_actions import log_debug`
- line 306: `            if not getattr(app, "_syntax_led_other_error_logged", False):`
- line 307: `                log_debug(f"SyntaxLED: unerwarteter Fehler im Syntax-Check: {exc}")`
- line 308: `                setattr(app, "_syntax_led_other_error_logged", True)`


## modules\ui_left_panel.py
### Key mentions
- line 5: `from tkinter import filedialog`
- line 21: `    damit rechte Liste und Pfad-Logik konsistent arbeiten.`
- line 55: `    # Plain-Attribute fuer Altlogik / externe Tools`
- line 63: `    """Oeffnet einen Ordnerdialog und aktualisiert Zielordner, rechte Liste und LEDs."""`
- line 64: `    from tkinter import filedialog`
- line 76: `        path = filedialog.askdirectory(initialdir=initial, title="Zielordner waehlen")`
- line 97: `    # Pfadwechsel-Logik / rechte Liste`
- line 135: `    - Intake-LED (Platzhalter, wird spaeter von Logik versorgt)`
- line 146: `    # (damit System-Logik und neue UI denselben Wert verwenden)`
- line 190: `    # Referenzen am App-Objekt bereitstellen (Kompatibilitaet fuer logic_actions)`

### Docking module refs
- line 127: `def build_left_panel(parent, app) -> tk.Frame:`

### INI calls
- line 122: `        _cfg_r1647b.save(cfg)`


## modules\ui_log_tab.py
### Key mentions
- line 3: `ui_log_tab – Log-Tab für ShrimpDev.`
- line 11: `    * Gesamtes Log kopieren und zurück zu Intake`
- line 24: `def _get_log_path() -> Path:`
- line 29: `def _load_log(text: tk.Text) -> None:`
- line 30: `    """Lädt den Inhalt der Logdatei in das Text-Widget."""`
- line 34: `        log_path = _get_log_path()`
- line 36: `            content = log_path.read_text(encoding="utf-8")`
- line 38: `            content = "Logdatei debug_output.txt wurde nicht gefunden."`
- line 40: `            content = f"Fehler beim Laden der Logdatei: {exc}"`
- line 42: `        content = f"Fehler beim Bestimmen des Log-Pfads: {exc}"`
- line 95: `    """Kopiert das gesamte Log und wechselt zurück zu Intake."""`
- line 104: `def build_log_tab(parent: tk.Widget, app: Any) -> None:`
- line 106: `    Baut den Log-Tab:`
- line 114: `        [Gesamtes Log kopieren + zurück]`
- line 122: `    # Log-Anzeige`
- line 149: `        command=lambda: (state.__setitem__('pos', 0), _load_log(text_widget)),`
- line 169: `        text="Gesamtes Log kopieren und zurück",`
- line 182: `    _load_log(text_widget)`
- line 184: `    # AUTO_TAIL_LOG_R2148`
- line 207: `        log_path = _get_log_path()`
- line 208: `        if not log_path.exists():`
- line 211: `            size = log_path.stat().st_size`
- line 218: `                data = log_path.read_text(encoding="utf-8", errors="replace")`
- line 233: `            with log_path.open("rb") as f:`

### Geometry/centering
- line 144: `    btn_frame.pack(anchor="center")`


## modules\ui_pipeline_tab.py
### Key mentions
- line 10: `    # modules/ui_pipeline_tab.py -> project root`
- line 14: `def _pipeline_path() -> Path:`
- line 15: `    return _project_root() / "docs" / "PIPELINE.md"`
- line 18: `def build_pipeline_tab(parent, app) -> None:`
- line 19: `    # PIPELINE_TREEVIEW_R2156`
- line 22: `    header = ttk.Label(parent, text="Pipeline", anchor="w")`
- line 23: `    # PIPELINE_UX_R2166`
- line 68: `        style.configure("Pipeline.Treeview", rowheight=22)`
- line 72: `    tree = ttk.Treeview(content, columns=cols, show="headings", selectmode="browse", style="Pipeline.Treeview")`
- line 147: `    def _parse_pipeline(raw: str) -> tuple[list[dict], list[str]]:`
- line 148: `        # R2158: robust task parsing for PIPELINE.md`
- line 269: `        p = _pipeline_path()`
- line 288: `        state["items"], state["raw_lines"] = _parse_pipeline(raw)`
- line 294: `        p = state.get("path") or _pipeline_path()`
- line 342: `        p = state.get("path") or _pipeline_path()`


## modules\ui_project_tree.py
### Key mentions
- line 236: `            from modules.logic_actions import refresh_right_list`
- line 291: `    # Referenzen am App-Objekt hinterlegen (Kompatibilität zu logic_actions etc.)`
- line 413: `    Einfache Filterlogik für das Suchfeld.`
- line 662: `        from modules.logic_actions import load_file_into_intake`
- line 676: `        from modules import logic_actions`
- line 736: `            delete_btn.configure(command=lambda a=app: logic_actions.action_tree_delete(a))`
- line 738: `            rename_btn.configure(command=lambda a=app: logic_actions.action_tree_rename(a))`
- line 740: `            undo_btn.configure(command=lambda a=app: logic_actions.action_tree_undo(a))`

### Restore/startup
- line 254: `            # Restart darf das UI nicht crashen`

### INI calls
- line 135: `                _cfg_tree.save(cfg_ws)`
- line 373: `                _cfg_tree.save(cfg)`
- line 568: `            _cfg_tree_save2.save(cfg)`


## modules\ui_runner_products_tab.py
### Key mentions
- line 43: `_R2304_TEXT_EXT = {".txt", ".md", ".py", ".json", ".log", ".ini", ".cfg", ".yaml", ".yml", ".csv", ".bat", ".cmd", ".ps1"}`
- line 265: `def build_runner_products_tab(parent: tk.Widget, app) -> None:`

### Docking module refs
- line 76: `        win = tk.Toplevel(app if app is not None else None)`

### Create/show window
- line 76: `        win = tk.Toplevel(app if app is not None else None)`
- line 82: `                win.transient(app)`
- line 83: `            win.lift()`

### Close hooks
- line 177: `            win.destroy()`

### Geometry/centering
- line 78: `        # --- R2306 CENTER_OVER_APP -------------------------------------------------`
- line 86: `        # --- /R2306 CENTER_OVER_APP ------------------------------------------------`
- line 88: `        win.geometry("980x650")`
- line 90: `        # --- R2306 CENTER_OVER_APP (position) --------------------------------------`
- line 100: `                ax = win.winfo_screenwidth() // 2`
- line 101: `                ay = win.winfo_screenheight() // 2`
- line 112: `                x = (win.winfo_screenwidth() - ww) // 2`
- line 113: `                y = (win.winfo_screenheight() - wh) // 2`
- line 118: `            win.geometry(f"{ww}x{wh}+{x}+{y}")`
- line 121: `        # --- /R2306 CENTER_OVER_APP (position) -------------------------------------`
- line 134: `    # Center: Text + Scroll`


## modules\ui_settings_tab.py
### Key mentions
- line 15: `from tkinter import ttk, filedialog, messagebox`
- line 51: `            selected = filedialog.askdirectory(`
- line 57: `            selected = filedialog.askdirectory(`

### INI calls
- line 17: `from modules import config_manager`
- line 30: `    mgr = config_manager.get_manager()`
- line 37: `    current_root = config_manager.get_workspace_root()`
- line 38: `    current_quiet = config_manager.get_quiet_mode()`
- line 77: `    def on_save() -> None:`
- line 80: `            config_manager.set_workspace_root(new_root, auto_save=False)`
- line 81: `            config_manager.set_quiet_mode(bool(var_quiet.get()), auto_save=False)`
- line 82: `            mgr.save()`


## modules\ui_toolbar.py
### Key mentions
- line 33: `from . import ui_theme_classic, ui_tooltips, ui_leds, logic_tools`
- line 34: `from .logic_actions import (`
- line 46: `    log_debug,`
- line 54: `def _call_logic_action(app, name: str) -> None:`
- line 56: `    Dynamischer Aufruf einer Action aus modules.logic_actions.`
- line 62: `        from . import logic_actions`
- line 72: `    func = getattr(logic_actions, name, None)`
- line 117: `                # LED-Updates duerfen die UI niemals crashen, aber Fehler werden geloggt.`
- line 119: `                    log_debug(f"LED evaluate failed in _wrap_with_led: {exc}")`
- line 131: `# R1853_WRAP_WITH_LED_AND_LOG`
- line 132: `def _wrap_with_led_and_log(app, func):`
- line 133: `    """Wie _wrap_with_led, öffnet danach zusätzlich das Logfenster."""`
- line 143: `                    log_debug(f"LED evaluate failed in _wrap_with_led_and_log: {exc}")`
- line 151: `            # Danach Logfenster öffnen (zentraler Popup)`
- line 153: `                _action_show_log(app)`
- line 156: `                    log_debug(f"Log popup failed in _wrap_with_led_and_log: {exc}")`
- line 171: `    # 1) Bevorzugt neue Refresh-Logik ueber ui_filters`
- line 232: `def _action_show_log(app):`
- line 233: `    """Zeigt die Logdatei debug_output.txt in einem Popup mit INI-Persistenz.`
- line 238: `    - Button "Ältere laden" lädt den Rest des Logs nach.`
- line 249: `        log_path = os.path.join(root_dir, "debug_output.txt")`
- line 251: `        # Loginhalt laden`
- line 253: `            with open(log_path, "r", encoding="utf-8") as f:`
- line 256: `            content = "Logdatei debug_output.txt wurde nicht gefunden."`
- line 265: `            """Teilt das Log in (older_lines, tail_lines) für den letzten Runner-Block.`
- line 295: `        win.title("ShrimpDev Log (letzter Runner)")`
- line 307: `            if cfg.has_section("LogWindow") and cfg.has_option("LogWindow", "geometry"):`
- line 308: `                geom = cfg.get("LogWindow", "geometry")`
- line 413: `                if not cfg.has_section("LogWindow"):`
- line 414: `                    cfg.add_section("LogWindow")`
- line 415: `                cfg.set("LogWindow", "geometry", geom_value)`
- line 443: `        # Log-Ansicht darf ShrimpDev niemals crashen`
- line 447: `def _load_log_geometry(app):`
- line 448: `    """Lädt Log-Popup-Geometrie aus ShrimpDev.ini."""`
- line 455: `        if "LogWindow" in cfg and "geometry" in cfg["LogWindow"]:`
- line 456: `            return cfg["LogWindow"]["geometry"]`
- line 462: `def _save_log_geometry(app, win):`
- line 463: `    """Speichert Geometrie des Logfensters in ShrimpDev.ini."""`
- line 478: `        if "LogWindow" not in cfg:`
- line 479: `            cfg.add_section("LogWindow")`
- line 480: `        cfg["LogWindow"]["geometry"] = geom`
- line 543: `        from .logic_actions import action_detect`
- line 560: `      verwendet (zentraler Dialog, kein blinkendes CMD-Fenster).`
- line 693: `        command=lambda: _call_logic_action(app, "action_tools_purge_apply"),`
- line 708: `        command=lambda: _call_logic_action(app, "action_tools_purge_scan"),`
- line 763: `        _wrap_with_led_and_log(app, action_guard_futurefix),`
- line 769: `        _wrap_with_led_and_log(app, action_guard_futurefix_safe),`
- line 775: `        _wrap_with_led_and_log(app, action_r9998),`
- line 781: `        _wrap_with_led_and_log(app, action_r9999),`
- line 787: `        _wrap_with_led_and_log(app, logic_tools.tool_masterrules_guard),`
- line 804: `        from .logic_actions import action_rename`
- line 855: `    # Fallback: ursprüngliche Logik (ohne INI-Speichern)`

### Docking module refs
- line 208: `    # R2364_RESTART_PERSIST: persist docking/tab state BEFORE quitting`
- line 210: `        dm = getattr(app, "_dock_manager", None)`
- line 294: `        win = tk.Toplevel(app)`

### Create/show window
- line 294: `        win = tk.Toplevel(app)`
- line 297: `            win.transient(app)`

### Restore/startup
- line 206: `def _action_restart(app):`
- line 208: `    # R2364_RESTART_PERSIST: persist docking/tab state BEFORE quitting`
- line 218: `    """Restart von ShrimpDev - best effort über main_gui.py im Projekt-Root."""`
- line 230: `        # Restart darf die UI nicht crashen`
- line 651: `    # Zusatz-Buttons: Always-on-Top + Restart`
- line 663: `    btn_restart = _make_button(`
- line 665: `        "Restart",`
- line 666: `        lambda: _action_restart(app),`
- line 670: `        app._btn_restart = btn_restart`
- line 825: `# R2072_AOT_RESTART_START`
- line 826: `# AOT- und Restart-Wrapper:`
- line 829: `# - _action_restart speichert vor Neustart den UI-State`
- line 872: `def _action_restart(app):  # type: ignore[override]`
- line 873: `    """R2072: Restart mit vorherigem Speichern des UI-States."""`
- line 886: `        # Restart darf die UI nicht crashen`
- line 889: `# R2072_AOT_RESTART_END`

### Close hooks
- line 421: `            win.destroy()`
- line 440: `        win.protocol("WM_DELETE_WINDOW", _close)`

### Geometry/centering
- line 314: `                win.geometry(geom)`
- line 320: `                win.geometry("700x450")`
- line 328: `                win.geometry(f"+{max(x, 0)}+{max(y, 0)}")`
- line 447: `def _load_log_geometry(app):`
- line 462: `def _save_log_geometry(app, win):`


## modules\ui_toolbar_dev.py
### Key mentions
- line 14: `from .logic_actions import (`
- line 26: `    log_debug,`
- line 31: `def _call_logic_action(app, name: str) -> None:`
- line 33: `    Dynamischer Aufruf einer Action aus modules.logic_actions.`
- line 39: `        from . import logic_actions`
- line 49: `    func = getattr(logic_actions, name, None)`
- line 92: `                # LED-Updates duerfen die UI niemals crashen, aber Fehler werden geloggt.`
- line 94: `                    log_debug(f"LED evaluate failed in _wrap_with_led: {exc}")`
- line 155: `        from .logic_actions import action_detect`
- line 287: `        from .logic_actions import action_rename`

