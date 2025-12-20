from __future__ import annotations
import os, sys, tkinter as tk
from tkinter import ttk

ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from modules import ui_menus, ui_toolbar, ui_filters, ui_project_tree, ui_left_panel, ui_leds, ui_theme_classic, config_manager, ui_settings_tab, ui_pipeline_tab, ui_runner_products_tab, exception_logger, module_docking

# --- R2296: Import-Pfade beim Start in debug_output.txt loggen (Guard gegen "anderes Root / falscher Import") ---
def _r2296_log_import_paths_once() -> None:
    try:
        import os
        from datetime import datetime
        dbg = os.path.join(os.path.dirname(__file__), "debug_output.txt")
        parts = []
        try:
            from modules import logic_actions as _la
            parts.append(f"logic_actions={getattr(_la, '__file__', '?')}")
        except Exception as e:
            parts.append(f"logic_actions=ERR:{e}")
        try:
            from modules import module_runner_exec as _mre
            parts.append(f"module_runner_exec={getattr(_mre, '__file__', '?')}")
        except Exception as e:
            parts.append(f"module_runner_exec=ERR:{e}")
        try:
            from modules import module_runner_popup as _mrp
            parts.append(f"module_runner_popup={getattr(_mrp, '__file__', '?')}")
        except Exception as e:
            parts.append(f"module_runner_popup=ERR:{e}")
        try:
            from modules import exception_logger as _elog
            parts.append(f"exception_logger={getattr(_elog, '__file__', '?')}")
        except Exception as e:
            parts.append(f"exception_logger=ERR:{e}")

        line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [BOOT] import_paths " + " | ".join(parts)
        with open(dbg, "a", encoding="utf-8", errors="replace", newline="\n") as f:
            f.write(line + "\n")
    except Exception:
        pass

_r2296_log_import_paths_once()
# --- /R2296 ---


from modules.module_learningjournal import build_learningjournal_tab

APP_TITLE = "ShrimpDev - v9.9.13"


from modules import config_loader, ui_log_tab

def _hide_legacy_target_bar(app):
    """
    Versteckt den alten Zielordner-Balken im Intake-Tab, falls vorhanden.
    Sucht nach einem Frame mit einem Label "Zielordner:" und ruft pack_forget().
    Defensive Implementierung: Fehler werden still geschluckt.
    """
    try:
        import tkinter as tk  # nur fuer isinstance-Checks
        tab = getattr(app, "tab_intake", None)
        if tab is None:
            return
        for child in tab.winfo_children():
            try:
                widgets = child.winfo_children()
            except Exception:
                continue
            for w in widgets:
                try:
                    if isinstance(w, tk.Label) and "Zielordner" in str(w.cget("text")):
                        try:
                            child.pack_forget()
                        except Exception:
                            pass
                        return
                except Exception:
                    continue
    except Exception:
        # UI darf durch den Helper niemals crashen
        return


class ShrimpDevApp(tk.Tk):
    def __init__(self) -> None:
        try:
            from modules.logic_actions import _learning_log_event
            _learning_log_event(self, 'app_start', {})
        except Exception:
            pass

        try:
            def _lj_tab_event(event):
                try:
                    from modules.logic_actions import _learning_log_event
                    tab = self.nb.tab(self.nb.select(), 'text')
                    _learning_log_event(self, 'tab_change', {'tab': tab})
                except Exception:
                    pass
            self.nb.bind('<<NotebookTabChanged>>', _lj_tab_event)
        except Exception:
            pass

        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1300x780")
        self.minsize(1100, 680)
        # Always-on-Top (R2070): Toggle via config_loader, Initialzustand aus _init_ui_from_ini
        try:
            from modules import config_loader as _cfg_top
        except Exception:
            _cfg_top = None

        def _aot_write_flag(flag: bool) -> None:
            if _cfg_top is None:
                return
            try:
                cfg = _cfg_top.load()
            except Exception:
                return
            try:
                if not cfg.has_section('UI'):
                    cfg.add_section('UI')
                cfg.set('UI', 'always_on_top', 'true' if flag else 'false')
                _cfg_top.save(cfg)
            except Exception:
                return

        def toggle_topmost() -> None:
            try:
                cur = bool(self.attributes('-topmost'))
            except Exception:
                cur = False
            new = not cur
            try:
                self.attributes('-topmost', new)
            except Exception:
                return
            _aot_write_flag(new)
            try:
                self.set_status('Always-on-Top: ' + ('An' if new else 'Aus'))
            except Exception:
                pass
            try:
                if hasattr(self, '_update_aot_button'):
                    self._update_aot_button()
            except Exception:
                pass

        self.toggle_topmost = toggle_topmost

        ui_theme_classic.apply(self)
        ui_menus.build_menu(self)

        # Notebook
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)

        self.tab_intake = tk.Frame(self.nb, bg=ui_theme_classic.BG_MAIN)
        self.nb.add(self.tab_intake, text="Intake")

        # R2053: Log-Tab als 2. Tab
        self.tab_log = tk.Frame(self.nb, bg=ui_theme_classic.BG_MAIN)
        self.nb.add(self.tab_log, text="Log")
        try:
            ui_log_tab.build_log_tab(self.tab_log, self)
        except Exception:
            pass

        self.tab_lj = tk.Frame(self.nb, bg=ui_theme_classic.BG_MAIN)
        self.nb.add(self.tab_lj, text="LearningJournal")

        self.tab_settings = tk.Frame(self.nb, bg=ui_theme_classic.BG_MAIN)
        ui_settings_tab.build_settings_tab(self.tab_settings)

        # R2099: Pipeline-Tab (Read-Only Viewer fuer docs/PIPELINE.md)
        self.tab_pipeline = tk.Frame(self.nb, bg=ui_theme_classic.BG_MAIN)
        self.nb.add(self.tab_pipeline, text="Pipeline")
        try:
            ui_pipeline_tab.build_pipeline_tab(self.tab_pipeline, self)
        except Exception:
            pass


        # R2256: Runner-Produkte-Tab (Read-Only Viewer fuer _Reports/docs/_Archiv)
        self.tab_runner_products = tk.Frame(self.nb, bg=ui_theme_classic.BG_MAIN)
        self.nb.add(self.tab_runner_products, text="Artefakte")
        try:
            ui_runner_products_tab.build_runner_products_tab(self.tab_runner_products, self)
        except Exception:
            pass

        # R2322: Dock/Undock Context-Menu (Read-Only Tabs) BEGIN
        try:
            # Phase-1: nur Read-Only Tabs (Pipeline/Runner-Produkte/Log) als Extra-Viewer
            module_docking.install_notebook_context_menu(self, self.nb)
        except Exception:
            pass
        # R2322: Dock/Undock Context-Menu (Read-Only Tabs) END


        self.tab_agent = tk.Frame(self.nb, bg=ui_theme_classic.BG_MAIN)
        self.nb.add(self.tab_agent, text="Agent")
        # SAFE_AGENT_TAB_LOAD_BEGIN
        try:
            from modules import module_agent
            if hasattr(module_agent, 'build_agent_tab'):
                module_agent.build_agent_tab(self.tab_agent, self)
            else:
                import tkinter as _tk
                _tk.Label(self.tab_agent, text='Agent: build_agent_tab fehlt.').pack(anchor='w', padx=8, pady=8)
        except Exception as _exc:
            try:
                import tkinter as _tk
                _tk.Label(self.tab_agent, text='Agent-Tab Fehler: ' + repr(_exc)).pack(anchor='w', padx=8, pady=8)
            except Exception:
                pass
        # SAFE_AGENT_TAB_LOAD_END

        self.tab_proj = tk.Frame(self.nb, bg=ui_theme_classic.BG_MAIN)
        self.nb.add(self.tab_proj, text="Project")
        self.nb.add(self.tab_settings, text="Settings")

        # Intake-Tab aufbauen
        self._build_intake(self.tab_intake)
        _hide_legacy_target_bar(self)
        # LearningJournal-Tab aufbauen
        build_learningjournal_tab(self.tab_lj, self)

        # Statuszeile
        self._status = tk.StringVar(value="Bereit.")
        tk.Label(
            self,
            textvariable=self._status,
            anchor="w",
            bg=ui_theme_classic.BG_STATUS,
            bd=1,
            relief="sunken",
        ).pack(side="bottom", fill="x")

        # R1650: UI-Zustand aus INI laden und Close-Handler setzen
        try:
            self._init_ui_from_ini()
        except Exception:
            pass

        # R2034b: AOT-LED/Button nach INI-Laden synchronisieren
        try:
            if hasattr(self, "_update_aot_button"):
                self._update_aot_button()
        except Exception:
            pass

        try:
            self._init_close_protocol()
        except Exception:
            pass

    @property
    def status(self) -> tk.StringVar:
        """Status-Bridge für logic_actions."""
        return self._status

    def set_status(self, msg: str) -> None:
        """Sicheres Setzen des Status-Texts inkl. UI-Refresh."""
        try:
            self._status.set(msg)
            self.update_idletasks()
        except Exception:
            # Status darf niemals das UI crashen
            pass


    def _init_ui_from_ini(self) -> None:
        """
        R1650: Liest Fensterzustand, Topmost und zuletzt aktiven Tab aus der INI.
        """
        try:
            from modules import config_loader, ui_log_tab
        except Exception:
            return
        try:
            cfg = config_loader.load()
        except Exception:
            return
        try:
            has_section = cfg.has_section("UI")
        except Exception:
            return
        if not has_section:
            return

        try:
            sec = cfg["UI"]
        except Exception:
            sec = None
        if sec is None:
            return

        # Geometrie
        try:
            geo = sec.get("geometry", "").strip()
        except Exception:
            geo = ""
        if geo:
            try:
                self.geometry(geo)
            except Exception:
                pass

        # Maximiert
        try:
            max_flag = sec.get("maximized", "false").lower() in ("1", "true", "yes", "on")
        except Exception:
            max_flag = False
        if max_flag:
            try:
                self.state("zoomed")
            except Exception:
                pass

        # Always-on-Top
        try:
            atop = sec.get("always_on_top", "false").lower() in ("1", "true", "yes", "on")
        except Exception:
            atop = False
        try:
            self.attributes("-topmost", atop)
        except Exception:
            pass

        # Zuletzt aktiver Tab
        try:
            last_tab = sec.get("last_tab", "").strip()
        except Exception:
            last_tab = ""
        if last_tab.isdigit():
            try:
                idx = int(last_tab)
                self.nb.select(idx)
            except Exception:
                pass

    def _save_ui_state_to_ini(self) -> None:
        """R1650: Speichert Fensterzustand, Topmost und zuletzt aktiven Tab in die INI."""
        try:
            from modules import config_loader, ui_log_tab
        except Exception:
            return
        try:
            cfg = config_loader.load()
        except Exception:
            return
        try:
            if not cfg.has_section("UI"):
                cfg.add_section("UI")
        except Exception:
            return

        # Maximiert / Geometrie
        try:
            state = self.state()
        except Exception:
            state = ""
        try:
            if state == "zoomed":
                cfg.set("UI", "maximized", "true")
            else:
                cfg.set("UI", "maximized", "false")
                try:
                    geo = self.winfo_geometry()
                    cfg.set("UI", "geometry", geo)
                except Exception:
                    pass
        except Exception:
            pass

        # Always-on-Top
        try:
            top = bool(self.attributes("-topmost"))
            cfg.set("UI", "always_on_top", "true" if top else "false")
        except Exception:
            pass

        # Zuletzt aktiver Tab
        try:
            idx = self.nb.index(self.nb.select())
            cfg.set("UI", "last_tab", str(idx))
        except Exception:
            pass

        try:
            config_loader.save(cfg)
        except Exception:
            pass

    def _init_close_protocol(self) -> None:
        """R1650: Registriert einen Close-Handler, der zuerst den UI-State speichert."""
        def _on_close() -> None:
            try:
                self._save_ui_state_to_ini()
            except Exception:
                pass
            try:
                # R2385: persist docking state before closing (best-effort)
                try:
                    dm = getattr(self, "_dock_manager", None)
                    if dm is not None:
                        dm.persist_all()
                except Exception:
                    pass

                self.destroy()
            except Exception:
                try:
                    self.quit()
                except Exception:
                    pass
        try:
            self.protocol("WM_DELETE_WINDOW", _on_close)
        except Exception:
            pass

    def _build_intake(self, parent: tk.Widget) -> None:
        BG = ui_theme_classic.BG_MAIN

        from modules.ui_theme_classic import Entry, Button, Frame

        # Row 0: LED + Zähler
        row_led = Frame(parent, bg=BG)
        row_led.pack(fill="x", padx=6, pady=(3, 0))
        self.ledbar = None  # LEDBar wird spaeter mit Klick-Callbacks erzeugt
        self._entry_count = tk.StringVar(value="0 Einträge")
        self.entry_count = self._entry_count  # Alias für ui_project_tree
        # Hinweis: Das Zähler-Label wird im Projektbaum (ui_project_tree) angezeigt.

        # Row 1: Zielordner
        top = Frame(parent, bg=BG)
        top.pack(fill="x", padx=6, pady=(3, 2))
        for i in range(3):
            top.grid_columnconfigure(i, weight=0)
        top.grid_columnconfigure(1, weight=1)

        tk.Label(top, text="Zielordner:", bg=BG).grid(row=0, column=0, sticky="w")
        # Zielordner als StringVar - wird von logic_actions defensiv gelesen (geladen aus INI)
        try:
            cfg = config_loader.load()
            if cfg is not None and cfg.has_section("Intake"):
                last = cfg.get("Intake", "last_target_dir", fallback="")
            else:
                last = ""
        except Exception:
            last = ""
        if not last:
            # R2030: Fallback zuerst auf workspace_root/snippets, dann auf cwd/snippets
            try:
                from modules import config_manager as _cfg_mgr
                ws_root = _cfg_mgr.get_workspace_root()
                last = os.path.join(str(ws_root), "snippets")
            except Exception:
                last = os.path.join(os.getcwd(), "snippets")
        self._target = tk.StringVar(value=last)
        self.target = self._target
        self.target_dir_var = self._target
        self.var_target_dir = self._target

        # Klick-Aktionen fuer die Intake-LEDs
        def _on_led_syntax():
            """Fokussiert den Intake-Editor."""
            try:
                widget = getattr(self, "txt_intake", None) or getattr(self, "txt_code", None) or getattr(self, "intake_text", None)
                if widget is not None:
                    widget.focus_set()
            except Exception:
                pass

        def _on_led_nameext():
            """Fuehrt die Name/Endung-Erkennung aus (action_detect)."""
            try:
                from modules import logic_actions
                logic_actions.action_detect(self)
            except Exception:
                pass

        def _on_led_exists():
            """Oeffnet die zugehoerige Datei, falls sie existiert."""
            try:
                import os
                name_var = getattr(self, "var_name", None)
                ext_var = getattr(self, "var_ext", None)
                target_var = getattr(self, "var_target_dir", None)
                if not (name_var and ext_var and target_var):
                    return
                try:
                    n = name_var.get().strip()
                    e = ext_var.get().strip().lstrip(".")
                    t = target_var.get().strip()
                except Exception:
                    return
                if not (n and e and t):
                    return
                path = os.path.join(t, f"{n}.{e}")
                if os.path.isfile(path):
                    os.startfile(path)
            except Exception:
                pass

        def _on_led_target():
            """Oeffnet den Zielordner im Explorer."""
            try:
                import os, subprocess
                t = self.var_target_dir.get().strip()
                if t and os.path.isdir(t):
                    subprocess.Popen(["explorer", t])
            except Exception:
                pass

        # Always-on-Top Button + LEDBar im Intake (R1693b)
        # LEDs links, AOT-Button direkt rechts daneben.

        try:
            self.ledbar = ui_leds.LEDBar(
                row_led,
                callbacks={
                    "syntax": _on_led_syntax,
                    "nameext": _on_led_nameext,
                    "exists": _on_led_exists,
                    "target": _on_led_target,
                },
            )
            try:
                ui_leds.evaluate(self)
            except Exception:
                # LED-Updates duerfen die Intake-Anzeige nicht crashen
                pass
        except Exception:
            # LED-Callbacks sind optional - Fehler hier duerfen Intake nicht blockieren
            pass

        try:
            from modules.ui_theme_classic import Button as _AOTButton
        except Exception:
            import tkinter as _tk
            _AOTButton = _tk.Button

        def _update_aot_button() -> None:
            """Synchronisiert AOT-Button und AOT-LED in der LEDBar.

            - Button bleibt neutral mit Text "AOT".
            - AOT-LED in der LEDBar wird gruen, wenn AOT aktiv ist,
              sonst grau (unknown).
            """
            try:
                cur = bool(self.attributes("-topmost"))
            except Exception:
                cur = False

            # Button immer neutral halten
            try:
                btn = getattr(self, "_btn_aot", None)
                if btn is not None:
                    btn.config(text="AOT")
            except Exception:
                pass

            # AOT-LED in der LEDBar aktualisieren (wenn vorhanden)
            try:
                ledbar = getattr(self, "ledbar", None)
                if ledbar is not None:
                    if cur:
                        ledbar.set_ok("aot")
                    else:
                        ledbar.set_unknown("aot")
            except Exception:
                pass

        # Helper auch als Attribut registrieren, damit Toolbar darauf zugreifen kann
        self._update_aot_button = _update_aot_button

        def _on_aot_click() -> None:
            try:
                toggle = getattr(self, "toggle_topmost", None)
                if callable(toggle):
                    toggle()
                else:
                    cur = bool(self.attributes("-topmost"))
                    self.attributes("-topmost", not cur)
            except Exception:
                # AOT-Toggle darf nie das UI killen
                pass
            _update_aot_button()

        try:
            # Intake erzeugt hier keine eigenen AOT/Restart-Buttons mehr.
            # Die Buttons werden in der linken Toolbar aufgebaut.
            self._btn_aot = None
            self._btn_restart = None
            _update_aot_button()
        except Exception:
            # AOT-Initialisierung darf Intake niemals crashen
            pass


        ent = Entry(top, textvariable=self._target, width=52)
        ent.grid(row=0, column=1, sticky="we", padx=(4, 4))
        Button(
            top,
            text="...",
            width=3,
            command=lambda: ui_filters.browse_dir(self, self._target),
        ).grid(row=0, column=2, padx=(0, 8))

        # Auto-Refresh beim Pfad ändern (Enter/FocusOut)
        def _path_changed(_e=None):
            ui_filters.refresh(self)

        ent.bind("<Return>", _path_changed)
        ent.bind("<FocusOut>", _path_changed)

        # Row 3: Filter
        ui_filters.build_filters(parent, self)

        # Split: zwei Spalten (links Intake, rechts Runner-Liste) – R2052 PanedWindow unterhalb Toolbars
        import tkinter.ttk as ttk

        # Oberes Grid fuer die Toolbars + darunter PanedWindow fuer Panels
        grid = Frame(parent, bg=BG)
        grid.pack(fill="both", expand=True, padx=6, pady=(2, 6))
        grid.grid_rowconfigure(1, weight=1)
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        # Toolbar-Container links/rechts (fix, nicht verschiebbar)
        frame_toolbar_left = Frame(grid, bg=BG)
        frame_toolbar_right = Frame(grid, bg=BG)

        frame_toolbar_left.grid(row=0, column=0, sticky="we", padx=(0, 6), pady=(0, 4))
        frame_toolbar_right.grid(row=0, column=1, sticky="we", padx=(6, 0), pady=(0, 4))

        # Toolbars auf gleicher Hoehe
        tl = ui_toolbar.build_toolbar_left(frame_toolbar_left, self)
        tl.pack(fill="x")

        tr = ui_toolbar.build_toolbar_right(frame_toolbar_right, self)
        tr.pack(fill="x")

        # PanedWindow nur fuer die Panels (unterhalb der Toolbars)
        paned = ttk.PanedWindow(grid, orient="horizontal")
        paned.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Linker/ rechter Panelbereich im Splitter
        left_frame = Frame(paned, bg=BG)
        right_frame = Frame(paned, bg=BG)

        paned.add(left_frame, weight=1)
        paned.add(right_frame, weight=2)

        # Panels
        left = ui_left_panel.build_left_panel(left_frame, self)
        right = ui_project_tree.build_tree(right_frame, self)
        try:
            ui_project_tree.enable_lasso(self)
        except Exception:
            pass
        try:
            ui_project_tree.enable_context_menu(self)
        except Exception:
            pass

        left.pack(fill="both", expand=True, padx=(0, 6))
        right.pack(fill="both", expand=True, padx=(6, 0))


def main() -> None:
    exception_logger.install(ROOT)
    app = ShrimpDevApp()

    # R2406: Apply main window geometry from ShrimpDev.ini [Docking] main.geometry (best-effort)
    # Reason: default geometry can drift/center if restore isn't applied early.
    try:
        import os, configparser
        ini_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "ShrimpDev.ini")
        cfg = configparser.ConfigParser()
        cfg.read(ini_path, encoding="utf-8")
        geo = ""
        try:
            geo = cfg.get("Docking", "main.geometry", fallback="").strip()
        except Exception:
            geo = ""
        if geo:
            try:
                app.update_idletasks()
            except Exception:
                pass
            try:
                app.geometry(geo)
            except Exception:
                pass
    except Exception:
        pass

    app.mainloop()


if __name__ == "__main__":
    main()


# R2368_MAIN_GEOMETRY_LATE_APPLY
def _r2368_apply_main_geometry(app):
    try:
        import configparser, os
        root_dir = os.path.abspath(os.path.dirname(__file__))
        ini_path = os.path.join(root_dir, "ShrimpDev.ini")
        cfg = configparser.ConfigParser()
        if os.path.isfile(ini_path):
            cfg.read(ini_path, encoding="utf-8")
        geo = ""
        if cfg.has_section("UI"):
            geo = cfg.get("UI", "geometry", fallback="").strip()
        # R2388: Fallback – wenn UI.geometry fehlt, nimm Docking main.geometry
        if not geo and cfg.has_section("Docking"):
            geo = cfg.get("Docking", "main.geometry", fallback="").strip()
        if geo:
            try:
                app.update_idletasks()
            except Exception:
                pass
            try:
                app.geometry(geo)
            except Exception:
                pass
    except Exception:
        pass


# R2369_CALL_PERSIST_ON_RESTART
def _r2369_try_persist(app):
    try:
        dm = getattr(app, "_dock_manager", None)
        if dm is not None:
            try:
                dm.persist_all()
            except Exception:
                pass
    except Exception:
        pass
