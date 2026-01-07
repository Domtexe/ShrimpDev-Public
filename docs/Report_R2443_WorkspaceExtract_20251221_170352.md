[R2443] READ-ONLY: Workspace logic extract
Time: 2025-12-21 17:03:52
Root: C:\Users\rasta\OneDrive\ShrimpDev

## Files
- ui_project_tree.py: C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_project_tree.py (OK)
- ui_settings_tab.py: C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_settings_tab.py (OK)
- module_settings_ui.py: C:\Users\rasta\OneDrive\ShrimpDev\modules\module_settings_ui.py (OK)
- config_manager.py: C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py (OK)
- workspace_registry.py: C:\Users\rasta\OneDrive\ShrimpDev\modules\workspace_registry.py (OK)

## ui_project_tree.py – workspace anchors
- combo_workspace: 117
- Workspace:: 116
- workspace_var: 72
- Combobox: 117

### Excerpt around workspace UI (ui_project_tree.py)
(lines 47-187 of 889)
   47:     - Eigenes Suchfeld *nur* für die rechte Liste
   48:     - Unabhängig von Name/Endung links
   49:     - Spaltenköpfe klickbar zum Sortieren
   50:     """
   51:     bg = ui_theme_classic.BG_MAIN
   52:     wrap = tk.Frame(parent, bg=bg)
   53: 
   54:     # Zählerzeile (Einträge)
   55:     row_count = tk.Frame(wrap, bg=bg)
   56:     row_count.pack(fill="x", padx=0, pady=(0, 2))
   57: 
   58:     count_var = getattr(app, "entry_count", None)
   59:     if not isinstance(count_var, tk.StringVar):
   60:         count_var = tk.StringVar(value="0 Einträge")
   61:         try:
   62:             app.entry_count = count_var
   63:         except Exception:
   64:             pass
   65: 
   66:     tk.Label(row_count, textvariable=count_var, bg=bg).pack(side="left", padx=(0, 4))
   67: 
   68:     # Workspace-Auswahl (dynamisch: INI + Auto-Scan)
   69:     row_workspace = tk.Frame(wrap, bg=bg)
   70:     row_workspace.pack(fill="x", padx=0, pady=(0, 4))
   71: 
   72:     workspace_var = getattr(app, "workspace_var", None)
   73:     if not isinstance(workspace_var, tk.StringVar):
   74:         workspace_var = tk.StringVar(value="ShrimpDev")
   75:         try:
   76:             app.workspace_var = workspace_var
   77:         except Exception:
   78:             pass
   79: 
   80:     # Basisliste
   81:     workspace_values = ["ShrimpDev", "ShrimpHub"]
   82: 
   83:     # Aus Tree-State lesen (workspace_list, workspace_current)
   84:     try:
   85:         if _cfg_tree is not None and load_tree_state is not None:
   86:             cfg_ws = _cfg_tree.load()
   87:             state_ws = load_tree_state(cfg_ws) or {}
   88:             raw_list = state_ws.get("workspace_list")
   89:             if isinstance(raw_list, str) and raw_list.strip():
   90:                 for name in raw_list.split(","):
   91:                     name = name.strip()
   92:                     if name and name not in workspace_values:
   93:                         workspace_values.append(name)
   94:             stored_current = state_ws.get("workspace_current")
   95:             if isinstance(stored_current, str) and stored_current:
   96:                 workspace_var.set(stored_current)
   97:     except Exception:
   98:         pass
   99: 
  100:     # Auto-Scan: Parent-Verzeichnis nach 'Shrimp*'-Ordnern
  101:     try:
  102:         from pathlib import Path as _Path
  103:         base = _Path.cwd().resolve().parent
  104:         for d in base.iterdir():
  105:             try:
  106:                 if d.is_dir():
  107:                     name = d.name
  108:                     if name.lower().startswith("shrimp") and name not in workspace_values:
  109:                         workspace_values.append(name)
  110:             except Exception:
  111:                 pass
  112:     except Exception:
  113:         pass
  114: 
  115:     # Label + Combobox
  116:     tk.Label(row_workspace, text="Workspace:", bg=bg).pack(side="left")
  117:     combo_workspace = ttk.Combobox(
  118:         row_workspace,
  119:         textvariable=workspace_var,
  120:         values=workspace_values,
  121:         state="readonly",
  122:         width=12,
  123:     )
  124:     combo_workspace.pack(side="left", padx=(4, 0))
  125: 
  126:     # Aenderungen in Tree-State zurueckschreiben
  127:     def _on_workspace_change(*_args) -> None:
  128:         try:
  129:             if _cfg_tree is not None and load_tree_state is not None and save_tree_state is not None:
  130:                 cfg_ws = _cfg_tree.load()
  131:                 state_ws = load_tree_state(cfg_ws) or {}
  132:                 state_ws["workspace_current"] = workspace_var.get()
  133:                 state_ws["workspace_list"] = ",".join(workspace_values)
  134:                 save_tree_state(cfg_ws, state_ws)
  135:                 _cfg_tree.save(cfg_ws)
  136:         except Exception:
  137:             pass
  138: 
  139:     try:
  140:         workspace_var.trace_add("write", _on_workspace_change)
  141:     except Exception:
  142:         pass
  143: 
  144:     # Suchzeile (rechts eigenständig)
  145:     row_search = tk.Frame(wrap, bg=bg)
  146:     row_search.pack(fill="x", padx=0, pady=(0, 4))
  147: 
  148:     tk.Label(row_search, text="Suche:", bg=bg).pack(side="left")
  149:     search_var = tk.StringVar(value="")
  150:     ent = ui_theme_classic.Entry(row_search, textvariable=search_var, width=24)
  151:     ent.pack(side="left", padx=(4, 0))
  152: 
  153:     # Aktionsleiste (rechte Seite unterhalb der Suche)
  154:     row_actions = tk.Frame(wrap, bg=bg)
  155:     row_actions.pack(fill="x", padx=0, pady=(0, 4))
  156: 
  157:     def _open_path(path: str) -> None:
  158:         if not path:
  159:             return
  160:         try:
  161:             if os.path.isdir(path) or os.path.isfile(path):
  162:                 os.startfile(path)
  163:         except Exception:
  164:             pass
  165: 
  166:     def _get_workspace_root() -> str:
  167:         # Basis: aktueller Workspace aus workspace_var, sonst ShrimpDev
  168:         try:
  169:             ws_var = getattr(app, "workspace_var", None)
  170:             if isinstance(ws_var, tk.StringVar):
  171:                 name = ws_var.get().strip()
  172:             else:
  173:                 name = "ShrimpDev"
  174:         except Exception:
  175:             name = "ShrimpDev"
  176:         try:
  177:             cwd = os.path.abspath(os.getcwd())
  178:             base = os.path.abspath(os.path.join(cwd, ".."))
  179:             if name.lower() == "shrimpdev":
  180:                 root_dir = cwd
  181:             else:
  182:                 cand = os.path.join(base, name)
  183:                 if os.path.isdir(cand):
  184:                     root_dir = cand
  185:                 else:
  186:                     root_dir = cwd
  187:         except Exception:

## ui_settings_tab.py – workspace_root related excerpt
- first 'workspace_root': 5

(lines 1-40 of 103)
    1: """
    2: modules/ui_settings_tab.py – Settings-Tab für ShrimpDev
    3: 
    4: Inhalte:
    5: - workspace_root anzeigen/ändern
    6: - quiet_mode (Checkbox) anzeigen/ändern
    7: """
    8: 
    9: from __future__ import annotations
   10: 
   11: from pathlib import Path
   12: from typing import Optional
   13: 
   14: import tkinter as tk
   15: from tkinter import ttk, filedialog, messagebox
   16: 
   17: from modules import config_manager
   18: 
   19: 
   20: def build_settings_tab(parent: tk.Widget) -> ttk.Frame:
   21:     """
   22:     Erzeugt den Settings-Tab-Inhalt und hängt ihn an parent an.
   23: 
   24:     Args:
   25:         parent: Container (z. B. eine ttk.Frame-Instanz im Notebook)
   26: 
   27:     Returns:
   28:         Der Haupt-Frame des Settings-Tabs.
   29:     """
   30:     mgr = config_manager.get_manager()
   31:     mgr.ensure_loaded()
   32: 
   33:     frame = ttk.Frame(parent)
   34:     frame.pack(fill="both", expand=True, padx=10, pady=10)
   35: 
   36:     # Aktuelle Werte
   37:     current_root = config_manager.get_workspace_root()
   38:     current_quiet = config_manager.get_quiet_mode()
   39: 
   40:     # Row 0: workspace_root Label + Entry + Button

- first 'D:\ShrimpHub': None
- first 'C:\Users\rasta\OneDrive\ShrimpDev': None
- first 'Workspace-Root': 41

(lines 6-76 of 103)
    6: - quiet_mode (Checkbox) anzeigen/ändern
    7: """
    8: 
    9: from __future__ import annotations
   10: 
   11: from pathlib import Path
   12: from typing import Optional
   13: 
   14: import tkinter as tk
   15: from tkinter import ttk, filedialog, messagebox
   16: 
   17: from modules import config_manager
   18: 
   19: 
   20: def build_settings_tab(parent: tk.Widget) -> ttk.Frame:
   21:     """
   22:     Erzeugt den Settings-Tab-Inhalt und hängt ihn an parent an.
   23: 
   24:     Args:
   25:         parent: Container (z. B. eine ttk.Frame-Instanz im Notebook)
   26: 
   27:     Returns:
   28:         Der Haupt-Frame des Settings-Tabs.
   29:     """
   30:     mgr = config_manager.get_manager()
   31:     mgr.ensure_loaded()
   32: 
   33:     frame = ttk.Frame(parent)
   34:     frame.pack(fill="both", expand=True, padx=10, pady=10)
   35: 
   36:     # Aktuelle Werte
   37:     current_root = config_manager.get_workspace_root()
   38:     current_quiet = config_manager.get_quiet_mode()
   39: 
   40:     # Row 0: workspace_root Label + Entry + Button
   41:     lbl_root = ttk.Label(frame, text="Workspace-Root:")
   42:     lbl_root.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(0, 5))
   43: 
   44:     var_root = tk.StringVar(value=str(current_root))
   45:     entry_root = ttk.Entry(frame, textvariable=var_root, width=60)
   46:     entry_root.grid(row=0, column=1, sticky="we", padx=(0, 5), pady=(0, 5))
   47: 
   48:     def on_browse_root() -> None:
   49:         start_dir = var_root.get().strip() or str(current_root)
   50:         try:
   51:             selected = filedialog.askdirectory(
   52:                 parent=frame,
   53:                 title="Workspace-Root wählen",
   54:                 initialdir=start_dir,
   55:             )
   56:         except Exception:
   57:             selected = filedialog.askdirectory(
   58:                 parent=frame,
   59:                 title="Workspace-Root wählen",
   60:             )
   61:         if selected:
   62:             var_root.set(selected)
   63: 
   64:     btn_browse = ttk.Button(frame, text="...", width=3, command=on_browse_root)
   65:     btn_browse.grid(row=0, column=2, sticky="w", pady=(0, 5))
   66: 
   67:     # Row 1: quiet_mode Checkbox
   68:     var_quiet = tk.BooleanVar(value=bool(current_quiet))
   69:     chk_quiet = ttk.Checkbutton(
   70:         frame,
   71:         text="Quiet-Mode (Popups der SonderRunner reduzieren)",
   72:         variable=var_quiet,
   73:     )
   74:     chk_quiet.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 10))
   75: 
   76:     # Row 2: Speichern-Button

- first 'Workspace Root': None

## module_settings_ui.py – workspace_root related excerpt
- first 'workspace_root': 11

(lines 1-45 of 45)
    1: from __future__ import annotations
    2: import json, tkinter as tk
    3: from tkinter import ttk, messagebox, filedialog
    4: from pathlib import Path
    5: from .common_tabs import ensure_tab
    6: 
    7: ROOT = Path(r"C:\Users\rasta\OneDrive\ShrimpDev")
    8: CFG  = ROOT / "config.json"
    9: 
   10: def _load() -> dict:
   11:     if not CFG.exists(): return {"workspace_root": r"D:\ShrimpHub", "quiet_mode": True}
   12:     try: return json.loads(CFG.read_text(encoding="utf-8", errors="ignore") or "{}") or {}
   13:     except Exception: return {"workspace_root": r"D:\ShrimpHub", "quiet_mode": True}
   14: 
   15: def _save(conf: dict):
   16:     try: CFG.write_text(json.dumps(conf, ensure_ascii=False, indent=2), encoding="utf-8")
   17:     except Exception: pass
   18: 
   19: def _build_tab(parent):
   20:     frm = ttk.Frame(parent)
   21:     conf = _load()
   22:     ttk.Label(frm, text="Workspace Root:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
   23:     var_ws = tk.StringVar(value=conf.get("workspace_root", r"D:\ShrimpHub"))
   24:     ttk.Entry(frm, textvariable=var_ws, width=46).grid(row=0, column=1, sticky="we", padx=6, pady=10)
   25:     def _pick():
   26:         d = filedialog.askdirectory(title="Workspace wählen", initialdir=str(Path(var_ws.get() or r"D:\\")))
   27:         if d: var_ws.set(d)
   28:     ttk.Button(frm, text="...", command=_pick).grid(row=0, column=2)
   29:     var_quiet = tk.BooleanVar(value=bool(conf.get("quiet_mode", True)))
   30:     ttk.Checkbutton(frm, text="Quiet Mode (Popup-Reduktion)", variable=var_quiet).grid(row=1, column=1, sticky="w", padx=6)
   31:     def _save_btn():
   32:         conf["workspace_root"] = var_ws.get().strip() or r"D:\ShrimpHub"
   33:         conf["quiet_mode"] = bool(var_quiet.get())
   34:         _save(conf)
   35:         try: messagebox.showinfo("ShrimpDev", "Gespeichert.")
   36:         except Exception: pass
   37:     ttk.Button(frm, text="Speichern", command=_save_btn).grid(row=2, column=1, sticky="e", padx=6, pady=12)
   38:     return frm
   39: 
   40: def open_settings(app: tk.Tk) -> bool:
   41:     try: return ensure_tab(app, "settings", "Settings", _build_tab)
   42:     except Exception as ex:
   43:         try: messagebox.showerror("ShrimpDev", f"Settings Fehler:\n{ex}")
   44:         except Exception: pass
   45:         return False

- first 'D:\ShrimpHub': 11

(lines 1-45 of 45)
    1: from __future__ import annotations
    2: import json, tkinter as tk
    3: from tkinter import ttk, messagebox, filedialog
    4: from pathlib import Path
    5: from .common_tabs import ensure_tab
    6: 
    7: ROOT = Path(r"C:\Users\rasta\OneDrive\ShrimpDev")
    8: CFG  = ROOT / "config.json"
    9: 
   10: def _load() -> dict:
   11:     if not CFG.exists(): return {"workspace_root": r"D:\ShrimpHub", "quiet_mode": True}
   12:     try: return json.loads(CFG.read_text(encoding="utf-8", errors="ignore") or "{}") or {}
   13:     except Exception: return {"workspace_root": r"D:\ShrimpHub", "quiet_mode": True}
   14: 
   15: def _save(conf: dict):
   16:     try: CFG.write_text(json.dumps(conf, ensure_ascii=False, indent=2), encoding="utf-8")
   17:     except Exception: pass
   18: 
   19: def _build_tab(parent):
   20:     frm = ttk.Frame(parent)
   21:     conf = _load()
   22:     ttk.Label(frm, text="Workspace Root:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
   23:     var_ws = tk.StringVar(value=conf.get("workspace_root", r"D:\ShrimpHub"))
   24:     ttk.Entry(frm, textvariable=var_ws, width=46).grid(row=0, column=1, sticky="we", padx=6, pady=10)
   25:     def _pick():
   26:         d = filedialog.askdirectory(title="Workspace wählen", initialdir=str(Path(var_ws.get() or r"D:\\")))
   27:         if d: var_ws.set(d)
   28:     ttk.Button(frm, text="...", command=_pick).grid(row=0, column=2)
   29:     var_quiet = tk.BooleanVar(value=bool(conf.get("quiet_mode", True)))
   30:     ttk.Checkbutton(frm, text="Quiet Mode (Popup-Reduktion)", variable=var_quiet).grid(row=1, column=1, sticky="w", padx=6)
   31:     def _save_btn():
   32:         conf["workspace_root"] = var_ws.get().strip() or r"D:\ShrimpHub"
   33:         conf["quiet_mode"] = bool(var_quiet.get())
   34:         _save(conf)
   35:         try: messagebox.showinfo("ShrimpDev", "Gespeichert.")
   36:         except Exception: pass
   37:     ttk.Button(frm, text="Speichern", command=_save_btn).grid(row=2, column=1, sticky="e", padx=6, pady=12)
   38:     return frm
   39: 
   40: def open_settings(app: tk.Tk) -> bool:
   41:     try: return ensure_tab(app, "settings", "Settings", _build_tab)
   42:     except Exception as ex:
   43:         try: messagebox.showerror("ShrimpDev", f"Settings Fehler:\n{ex}")
   44:         except Exception: pass
   45:         return False

- first 'C:\Users\rasta\OneDrive\ShrimpDev': 7

(lines 1-42 of 45)
    1: from __future__ import annotations
    2: import json, tkinter as tk
    3: from tkinter import ttk, messagebox, filedialog
    4: from pathlib import Path
    5: from .common_tabs import ensure_tab
    6: 
    7: ROOT = Path(r"C:\Users\rasta\OneDrive\ShrimpDev")
    8: CFG  = ROOT / "config.json"
    9: 
   10: def _load() -> dict:
   11:     if not CFG.exists(): return {"workspace_root": r"D:\ShrimpHub", "quiet_mode": True}
   12:     try: return json.loads(CFG.read_text(encoding="utf-8", errors="ignore") or "{}") or {}
   13:     except Exception: return {"workspace_root": r"D:\ShrimpHub", "quiet_mode": True}
   14: 
   15: def _save(conf: dict):
   16:     try: CFG.write_text(json.dumps(conf, ensure_ascii=False, indent=2), encoding="utf-8")
   17:     except Exception: pass
   18: 
   19: def _build_tab(parent):
   20:     frm = ttk.Frame(parent)
   21:     conf = _load()
   22:     ttk.Label(frm, text="Workspace Root:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
   23:     var_ws = tk.StringVar(value=conf.get("workspace_root", r"D:\ShrimpHub"))
   24:     ttk.Entry(frm, textvariable=var_ws, width=46).grid(row=0, column=1, sticky="we", padx=6, pady=10)
   25:     def _pick():
   26:         d = filedialog.askdirectory(title="Workspace wählen", initialdir=str(Path(var_ws.get() or r"D:\\")))
   27:         if d: var_ws.set(d)
   28:     ttk.Button(frm, text="...", command=_pick).grid(row=0, column=2)
   29:     var_quiet = tk.BooleanVar(value=bool(conf.get("quiet_mode", True)))
   30:     ttk.Checkbutton(frm, text="Quiet Mode (Popup-Reduktion)", variable=var_quiet).grid(row=1, column=1, sticky="w", padx=6)
   31:     def _save_btn():
   32:         conf["workspace_root"] = var_ws.get().strip() or r"D:\ShrimpHub"
   33:         conf["quiet_mode"] = bool(var_quiet.get())
   34:         _save(conf)
   35:         try: messagebox.showinfo("ShrimpDev", "Gespeichert.")
   36:         except Exception: pass
   37:     ttk.Button(frm, text="Speichern", command=_save_btn).grid(row=2, column=1, sticky="e", padx=6, pady=12)
   38:     return frm
   39: 
   40: def open_settings(app: tk.Tk) -> bool:
   41:     try: return ensure_tab(app, "settings", "Settings", _build_tab)
   42:     except Exception as ex:

- first 'Workspace-Root': None
- first 'Workspace Root': 22

(lines 1-45 of 45)
    1: from __future__ import annotations
    2: import json, tkinter as tk
    3: from tkinter import ttk, messagebox, filedialog
    4: from pathlib import Path
    5: from .common_tabs import ensure_tab
    6: 
    7: ROOT = Path(r"C:\Users\rasta\OneDrive\ShrimpDev")
    8: CFG  = ROOT / "config.json"
    9: 
   10: def _load() -> dict:
   11:     if not CFG.exists(): return {"workspace_root": r"D:\ShrimpHub", "quiet_mode": True}
   12:     try: return json.loads(CFG.read_text(encoding="utf-8", errors="ignore") or "{}") or {}
   13:     except Exception: return {"workspace_root": r"D:\ShrimpHub", "quiet_mode": True}
   14: 
   15: def _save(conf: dict):
   16:     try: CFG.write_text(json.dumps(conf, ensure_ascii=False, indent=2), encoding="utf-8")
   17:     except Exception: pass
   18: 
   19: def _build_tab(parent):
   20:     frm = ttk.Frame(parent)
   21:     conf = _load()
   22:     ttk.Label(frm, text="Workspace Root:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
   23:     var_ws = tk.StringVar(value=conf.get("workspace_root", r"D:\ShrimpHub"))
   24:     ttk.Entry(frm, textvariable=var_ws, width=46).grid(row=0, column=1, sticky="we", padx=6, pady=10)
   25:     def _pick():
   26:         d = filedialog.askdirectory(title="Workspace wählen", initialdir=str(Path(var_ws.get() or r"D:\\")))
   27:         if d: var_ws.set(d)
   28:     ttk.Button(frm, text="...", command=_pick).grid(row=0, column=2)
   29:     var_quiet = tk.BooleanVar(value=bool(conf.get("quiet_mode", True)))
   30:     ttk.Checkbutton(frm, text="Quiet Mode (Popup-Reduktion)", variable=var_quiet).grid(row=1, column=1, sticky="w", padx=6)
   31:     def _save_btn():
   32:         conf["workspace_root"] = var_ws.get().strip() or r"D:\ShrimpHub"
   33:         conf["quiet_mode"] = bool(var_quiet.get())
   34:         _save(conf)
   35:         try: messagebox.showinfo("ShrimpDev", "Gespeichert.")
   36:         except Exception: pass
   37:     ttk.Button(frm, text="Speichern", command=_save_btn).grid(row=2, column=1, sticky="e", padx=6, pady=12)
   38:     return frm
   39: 
   40: def open_settings(app: tk.Tk) -> bool:
   41:     try: return ensure_tab(app, "settings", "Settings", _build_tab)
   42:     except Exception as ex:
   43:         try: messagebox.showerror("ShrimpDev", f"Settings Fehler:\n{ex}")
   44:         except Exception: pass
   45:         return False


## config_manager.py – workspace_root related excerpt
- first 'workspace_root': 7

(lines 1-42 of 222)
    1: """
    2: modules/config_manager.py – Zentrale Konfiguration für ShrimpDev
    3: 
    4: Verantwortung:
    5: - Laden/Speichern von ShrimpDev.ini
    6: - Einheitlicher Zugriff auf:
    7:   - workspace_root
    8:   - quiet_mode
    9: 
   10: Konvention:
   11: - INI-Datei liegt im Projekt-Root (akt. Arbeitsverzeichnis von ShrimpDev).
   12: - Section: [settings]
   13: """
   14: 
   15: from __future__ import annotations
   16: 
   17: import configparser
   18: from pathlib import Path
   19: from typing import Optional
   20: 
   21: 
   22: CONFIG_FILENAME = "ShrimpDev.ini"
   23: SETTINGS_SECTION = "settings"
   24: 
   25: 
   26: class ShrimpDevConfigManager:
   27:     """
   28:     Verwaltet die zentralen Config-Werte von ShrimpDev.ini.
   29:     """
   30: 
   31:     def __init__(self) -> None:
   32:         self._config: Optional[configparser.ConfigParser] = None
   33:         self._project_root: Optional[Path] = None
   34: 
   35:     def _get_default_project_root(self) -> Path:
   36:         """
   37:         Ermittelt den Standard-Projekt-Root (aktuelles Arbeitsverzeichnis).
   38:         """
   39:         return Path.cwd()
   40: 
   41:     def ensure_loaded(self, project_root: Optional[Path] = None) -> None:
   42:         """

- first 'D:\ShrimpHub': None
- first 'C:\Users\rasta\OneDrive\ShrimpDev': None
- first 'Workspace-Root': None
- first 'Workspace Root': None

