import os
import time
import tkinter as tk
from tkinter import ttk

from modules import ui_theme_classic
from modules import config_loader as _cfg_tree
try:
    from modules.config_loader import load_tree_state, save_tree_state
except Exception:
    load_tree_state = None
    save_tree_state = None



def _fmt(ts: float) -> tuple[str, str]:
    """Format timestamp to (YYYY-MM-DD, HH:MM:SS)."""
    try:
        t = time.localtime(ts)
        return time.strftime("%Y-%m-%d", t), time.strftime("%H:%M:%S", t)
    except Exception:
        return "", ""


def _get_target_dir(app) -> str:
    """
    Robust Zugriff auf den Zielordner.

    Bevorzugt app.target (StringVar), fällt zurück auf app._target.
    """
    var = getattr(app, "target", None)
    if var is None:
        var = getattr(app, "_target", None)
    if var is None:
        return ""
    try:
        val = var.get() if hasattr(var, "get") else str(var)
    except Exception:
        val = ""
    return (val or "").strip()


def build_tree(parent: tk.Widget, app) -> tk.Frame:
    """
    Rechter Bereich: Datei-/Runner-Liste mit eigenem Suchfeld.

    - Eigenes Suchfeld *nur* für die rechte Liste
    - Unabhängig von Name/Endung links
    - Spaltenköpfe klickbar zum Sortieren
    """
    bg = ui_theme_classic.BG_MAIN
    wrap = tk.Frame(parent, bg=bg)

    # Zählerzeile (Einträge)
    row_count = tk.Frame(wrap, bg=bg)
    row_count.pack(fill="x", padx=0, pady=(0, 2))

    count_var = getattr(app, "entry_count", None)
    if not isinstance(count_var, tk.StringVar):
        count_var = tk.StringVar(value="0 Einträge")
        try:
            app.entry_count = count_var
        except Exception:
            pass

    tk.Label(row_count, textvariable=count_var, bg=bg).pack(side="left", padx=(0, 4))

    # Workspace-Auswahl (dynamisch: INI + Auto-Scan)
    row_workspace = tk.Frame(wrap, bg=bg)
    row_workspace.pack(fill="x", padx=0, pady=(0, 4))

    workspace_var = getattr(app, "workspace_var", None)
    if not isinstance(workspace_var, tk.StringVar):
        workspace_var = tk.StringVar(value="ShrimpDev")
        try:
            app.workspace_var = workspace_var
        except Exception:
            pass

    # Basisliste
    workspace_values = ["ShrimpDev", "ShrimpHub"]

    # Aus Tree-State lesen (workspace_list, workspace_current)
    try:
        if _cfg_tree is not None and load_tree_state is not None:
            cfg_ws = _cfg_tree.load()
            state_ws = load_tree_state(cfg_ws) or {}
            raw_list = state_ws.get("workspace_list")
            if isinstance(raw_list, str) and raw_list.strip():
                for name in raw_list.split(","):
                    name = name.strip()
                    if name and name not in workspace_values:
                        workspace_values.append(name)
            stored_current = state_ws.get("workspace_current")
            if isinstance(stored_current, str) and stored_current:
                workspace_var.set(stored_current)
    except Exception:
        pass

    # Auto-Scan: Parent-Verzeichnis nach 'Shrimp*'-Ordnern
    try:
        from pathlib import Path as _Path
        base = _Path.cwd().resolve().parent
        for d in base.iterdir():
            try:
                if d.is_dir():
                    name = d.name
                    if name.lower().startswith("shrimp") and name not in workspace_values:
                        workspace_values.append(name)
            except Exception:
                pass
    except Exception:
        pass

    # Label + Combobox
    tk.Label(row_workspace, text="Workspace:", bg=bg).pack(side="left")
    combo_workspace = ttk.Combobox(
        row_workspace,
        textvariable=workspace_var,
        values=workspace_values,
        state="readonly",
        width=12,
    )
    combo_workspace.pack(side="left", padx=(4, 0))

    # Aenderungen in Tree-State zurueckschreiben
    def _on_workspace_change(*_args) -> None:
        try:
            if _cfg_tree is not None and load_tree_state is not None and save_tree_state is not None:
                cfg_ws = _cfg_tree.load()
                state_ws = load_tree_state(cfg_ws) or {}
                state_ws["workspace_current"] = workspace_var.get()
                state_ws["workspace_list"] = ",".join(workspace_values)
                save_tree_state(cfg_ws, state_ws)
                _cfg_tree.save(cfg_ws)
        except Exception:
            pass

    try:
        workspace_var.trace_add("write", _on_workspace_change)
    except Exception:
        pass

    # Suchzeile (rechts eigenständig)
    row_search = tk.Frame(wrap, bg=bg)
    row_search.pack(fill="x", padx=0, pady=(0, 4))

    tk.Label(row_search, text="Suche:", bg=bg).pack(side="left")
    search_var = tk.StringVar(value="")
    ent = ui_theme_classic.Entry(row_search, textvariable=search_var, width=24)
    ent.pack(side="left", padx=(4, 0))

    # Aktionsleiste (rechte Seite unterhalb der Suche)
    row_actions = tk.Frame(wrap, bg=bg)
    row_actions.pack(fill="x", padx=0, pady=(0, 4))

    def _open_path(path: str) -> None:
        if not path:
            return
        try:
            if os.path.isdir(path) or os.path.isfile(path):
                os.startfile(path)
        except Exception:
            pass

    def _get_workspace_root() -> str:
        # Basis: aktueller Workspace aus workspace_var, sonst ShrimpDev
        try:
            ws_var = getattr(app, "workspace_var", None)
            if isinstance(ws_var, tk.StringVar):
                name = ws_var.get().strip()
            else:
                name = "ShrimpDev"
        except Exception:
            name = "ShrimpDev"
        try:
            cwd = os.path.abspath(os.getcwd())
            base = os.path.abspath(os.path.join(cwd, ".."))
            if name.lower() == "shrimpdev":
                root_dir = cwd
            else:
                cand = os.path.join(base, name)
                if os.path.isdir(cand):
                    root_dir = cand
                else:
                    root_dir = cwd
        except Exception:
            root_dir = os.path.abspath(os.getcwd())
        return root_dir

    def _btn_open_root() -> None:
        _open_path(_get_workspace_root())

    def _btn_open_tools() -> None:
        root_dir = _get_workspace_root()
        _open_path(os.path.join(root_dir, "tools"))

    def _btn_open_reports() -> None:
        root_dir = _get_workspace_root()
        _open_path(os.path.join(root_dir, "_Reports"))

    def _btn_open_snapshots() -> None:
        root_dir = _get_workspace_root()
        _open_path(os.path.join(root_dir, "_Snapshots"))

    def _btn_open_explorer() -> None:
        # Markierte Datei im Explorer, sonst Workspace-Root
        try:
            tree = getattr(app, "tree", None)
            paths = getattr(app, "tree_paths", {})
            if tree is None or not paths:
                _open_path(_get_workspace_root())
                return
            sel = tree.selection()
            if not sel:
                _open_path(_get_workspace_root())
                return
            item_id = sel[0]
            path = paths.get(item_id)
        except Exception:
            path = None
        if not path:
            _open_path(_get_workspace_root())
            return
        try:
            if os.path.isfile(path):
                os.startfile(path)
            else:
                _open_path(path)
        except Exception:
            pass

    def _btn_refresh() -> None:
        # Versuche, die rechte Liste zu aktualisieren
        try:
            from modules.logic_actions import refresh_right_list
            refresh_right_list(app)
        except Exception:
            # Wenn nicht verfuegbar, einfach nichts tun
            pass

        # Versuche, ShrimpDev/Workspace neu zu starten
        try:
            root_dir = _get_workspace_root()
            main_py = os.path.join(root_dir, "main_gui.py")
            if os.path.isfile(main_py):
                os.startfile(main_py)
            # aktuelles Fenster schliessen
            try:
                app.quit()
            except Exception:
                pass
        except Exception:
            # Restart darf das UI nicht crashen
            pass

    btn_root = ui_theme_classic.Button(row_actions, text="Ordner", command=_btn_open_root, width=8)
    btn_tools = ui_theme_classic.Button(row_actions, text="Tools", command=_btn_open_tools, width=8)
    btn_reports = ui_theme_classic.Button(row_actions, text="Reports", command=_btn_open_reports, width=8)
    btn_snaps = ui_theme_classic.Button(row_actions, text="Snapshots", command=_btn_open_snapshots, width=10)
    btn_explorer = ui_theme_classic.Button(row_actions, text="Explorer", command=_btn_open_explorer, width=10)


    # Tree + Scrollbar
    cols = ("name", "ext", "date", "time")
    tree = ttk.Treeview(wrap, columns=cols, show="headings", selectmode="extended")
    vsb = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    # Spalten-Setup
    headings = {
        "name": "Name",
        "ext": "Endung",
        "date": "Datum",
        "time": "Zeit",
    }
    widths = {
        "name": 220,
        "ext": 80,
        "date": 100,
        "time": 80,
    }

    for cid in cols:
        tree.heading(cid, text=headings[cid])
        tree.column(cid, width=widths[cid], anchor="w", stretch=(cid == "name"))

    # Referenzen am App-Objekt hinterlegen (Kompatibilität zu logic_actions etc.)
    app.tree = tree
    app.tree_paths = {}
    app.tree_filter_var = search_var
    app.tree_sort_col = "date"
    app.tree_sort_reverse = True
    app.right_list = RightListProxy(app)

    # Doppelklick auf Eintrag -> Datei in Intake
    try:
        tree.bind("<Double-1>", lambda event, a=app: open_selected_in_intake(a))
    except Exception:
        pass

    # Sortierungs-Callbacks nach dem Setzen der Referenzen definieren
    def _sort_cmd(col: str):
        def _cb():
            _sort_by(app, col, toggle=True)
        return _cb

    for cid in cols:
        tree.heading(cid, command=_sort_cmd(cid))

    # Directory initial laden (inkl. Tree-INI-Zustand)
    try:
        if _cfg_tree is not None and load_tree_state is not None:
            cfg = _cfg_tree.load()
            state = load_tree_state(cfg)
            if state:
                term = state.get("search_term", "")
                if isinstance(term, str) and term:
                    try:
                        search_var.set(term)
                    except Exception:
                        pass
                col = state.get("sort_column", "")
                if isinstance(col, str) and col:
                    app.tree_sort_col = col
                direction = str(state.get("sort_direction", "")).lower()
                app.tree_sort_reverse = direction in ("1", "true", "yes", "on", "desc", "down")
                widths_state = state.get("column_widths", [])
                if isinstance(widths_state, (list, tuple)):
                    for cid, w in zip(cols, widths_state):
                        try:
                            tree.column(cid, width=int(w))
                        except Exception:
                            pass
    except Exception:
        pass

    _load_dir(app)

    # Filter-Callback: bei Eingabe Liste neu laden
    def _on_search_change(*_args):
        _load_dir(app)
        # Tree-Zustand in INI speichern
        try:
            if _cfg_tree is not None and save_tree_state is not None:
                cfg = _cfg_tree.load()
                state = {}
                try:
                    state["search_term"] = (app.tree_filter_var.get() or "").strip()
                except Exception:
                    state["search_term"] = ""
                try:
                    col = getattr(app, "tree_sort_col", "name")
                    rev = getattr(app, "tree_sort_reverse", False)
                    state["sort_column"] = col
                    state["sort_direction"] = "desc" if rev else "asc"
                except Exception:
                    pass
                try:
                    widths_state = []
                    for cid in ("name", "ext", "date", "time"):
                        try:
                            widths_state.append(int(app.tree.column(cid, "width")))
                        except Exception:
                            widths_state.append(0)
                    state["column_widths"] = widths_state
                except Exception:
                    pass
                save_tree_state(cfg, state)
                _cfg_tree.save(cfg)
        except Exception:
            pass

    search_var.trace_add("write", _on_search_change)

    # Fokus auf Suchfeld setzen (komfortabel für direkte Eingabe)
    try:
        ent.focus_set()
    except Exception:
        pass

    # Buttons rechts (Delete/Rename/Undo) nachträglich verdrahten
    try:
        wire_tree_buttons(app, wrap)
    except Exception:
        pass

    return wrap


def _iter_files(base: str):
    """Erzeuge (name, ext, path, mtime) für alle Dateien im Zielordner (nicht rekursiv)."""
    try:
        for entry in os.scandir(base):
            if not entry.is_file():
                continue
            path = entry.path
            name = os.path.basename(path)
            root, ext = os.path.splitext(name)
            ext = ext or ""
            yield root, ext, path, entry.stat().st_mtime
    except FileNotFoundError:
        return
    except PermissionError:
        return


def _matches_filter(name: str, ext: str, query: str) -> bool:
    """
    Einfache Filterlogik für das Suchfeld.

    - query wird in Kleinbuchstaben mit name/ext verglichen
    - mehrere Begriffe werden als UND verknüpft
    """
    if not query:
        return True
    name_l = name.lower()
    ext_l = ext.lower()
    for token in query.split():
        if token not in name_l and token not in ext_l:
            return False
    return True


def _load_dir(app) -> None:
    """
    Liste rechts komplett neu aufbauen.

    - Basis: Zielordner (app.target / app._target)
    - Filter: ausschließlich Suchfeld rechts (app.tree_filter_var)
    - Keine Abhängigkeit von Name/Endung links
    """
    tree = getattr(app, "tree", None)
    if tree is None:
        return

    base = _get_target_dir(app)
    query = ""
    try:
        query = getattr(app, "tree_filter_var", None).get().strip().lower()
    except Exception:
        query = ""

    # Tree leeren
    for iid in tree.get_children(""):
        tree.delete(iid)
    paths: dict[str, str] = {}
    count = 0

    if not base or not os.path.isdir(base):
        try:
            app.entry_count.set("0 Einträge")
        except Exception:
            pass
        app.tree_paths = paths
        return

    # Dateien einsammeln
    rows: list[tuple[str, str, str, float]] = []
    for name, ext, path, mtime in _iter_files(base):
        if not _matches_filter(name, ext, query):
            continue
        rows.append((name, ext, path, mtime))

    # Standard-Sortierung nach Name (ohne Endungsabhängigkeit)
        # Sortierung: neueste Datei oben
    rows.sort(key=lambda r: r[3], reverse=True)

    for name, ext, path, mtime in rows:
        d, t = _fmt(mtime)
        iid = tree.insert("", "end", values=(name, ext[1:] if ext.startswith(".") else ext, d, t))
        paths[iid] = path
        count += 1

    app.tree_paths = paths

    try:
        app.entry_count.set(f"{count} Einträge")
    except Exception:
        pass

    # Aktuelle Sortierung anwenden (falls Nutzer bereits geklickt hat)
    try:
        col = getattr(app, "tree_sort_col", "name")
        rev = getattr(app, "tree_sort_reverse", False)
        _sort_by(app, col, reverse=rev, toggle=False)
    except Exception:
        pass


def _sort_by(app, col: str, reverse: bool | None = None, toggle: bool = True) -> None:
    """
    Spaltensortierung für den Tree.

    - toggle=True: Richtung wird umgeschaltet, wenn gleiche Spalte erneut geklickt wird
    - reverse steuert explizit die Richtung, falls angegeben
    """
    tree = getattr(app, "tree", None)
    if tree is None:
        return

    curr_col = getattr(app, "tree_sort_col", "name")
    curr_rev = getattr(app, "tree_sort_reverse", False)

    if reverse is None:
        reverse = curr_rev

    if toggle:
        if col == curr_col:
            reverse = not curr_rev
        else:
            reverse = False  # neue Spalte -> erst mal aufsteigend

    # Daten auslesen
    items = []
    for iid in tree.get_children(""):
        val = tree.set(iid, col)
        items.append((val, iid))

    # Sortierfunktion je nach Spalte
    if col in ("date", "time"):
        items.sort(key=lambda x: x[0], reverse=reverse)
    else:
        items.sort(key=lambda x: x[0].lower(), reverse=reverse)

    # Reihenfolge anwenden
    for idx, (_, iid) in enumerate(items):
        tree.move(iid, "", idx)

    # Zustand merken
    app.tree_sort_col = col
    app.tree_sort_reverse = reverse

    # Tree-Sortierzustand in INI speichern
    try:
        from modules import config_loader as _cfg_tree_save2
        try:
            from modules.config_loader import save_tree_state as _save_tree_state2
        except Exception:
            _save_tree_state2 = None
        if _save_tree_state2 is not None:
            cfg = _cfg_tree_save2.load()
            state = {}
            try:
                tfv = getattr(app, "tree_filter_var", None)
                if tfv is not None:
                    state["search_term"] = (tfv.get() or "").strip()
                else:
                    state["search_term"] = ""
            except Exception:
                state["search_term"] = ""
            state["sort_column"] = col
            state["sort_direction"] = "desc" if reverse else "asc"
            try:
                widths_state = []
                for cid2 in ("name", "ext", "date", "time"):
                    try:
                        widths_state.append(int(tree.column(cid2, "width")))
                    except Exception:
                        widths_state.append(0)
                state["column_widths"] = widths_state
            except Exception:
                pass
            _save_tree_state2(cfg, state)
            _cfg_tree_save2.save(cfg)
    except Exception:
        pass


def get_selected_path(app) -> str | None:
    """
    Liefert den vollständigen Pfad des aktuell in der rechten Liste
    markierten Eintrags zurück.
    """
    tree = getattr(app, "tree", None)
    paths = getattr(app, "tree_paths", {})

    if tree is None:
        return None
    sel = tree.selection()
    if not sel:
        return None
    return paths.get(sel[0])


def get_selected_paths(app) -> list[str]:
    """
    Liefert eine Liste aller Pfade der in der rechten Liste
    markierten Eintraege (Mehrfachauswahl).
    """
    tree = getattr(app, "tree", None)
    paths = getattr(app, "tree_paths", {})

    if tree is None:
        return []
    try:
        sel = tree.selection()
    except Exception:
        return []
    result: list[str] = []
    for item in sel:
        try:
            p = paths.get(item)
        except Exception:
            p = None
        if p:
            result.append(p)
    return result


class RightListProxy:
    """Kleine Hülle mit refresh()-Methode für die rechte Liste."""

    def __init__(self, app):
        self._app = app

    def refresh(self) -> None:
        try:
            _load_dir(self._app)
        except Exception:
            pass


# ------------------------------------------------------------
# R1634 - Doppelklick-Öffnen von Code-Dateien in den Intake
# ------------------------------------------------------------

CODE_EXTS = (
    ".py",
    ".cmd",
    ".bat",
    ".ps1",
    ".sh",
    ".json",
    ".ini",
    ".cfg",
    ".yaml",
    ".yml",
    ".toml",
    ".txt",
)


def open_selected_in_intake(app) -> None:
    """Öffnet die aktuell markierte Datei aus der rechten Liste im Intake,
    sofern es sich um eine Code-Datei handelt."""
    import os

    path = get_selected_path(app)
    if not path:
        return

    _, ext = os.path.splitext(path)
    if ext.lower() not in CODE_EXTS:
        # keine Code-Datei -> ignorieren
        return

    try:
        from modules.logic_actions import load_file_into_intake
    except Exception:
        return

    try:
        load_file_into_intake(app, path)
    except Exception:
        # Öffnen darf niemals die GUI töten
        pass


def wire_tree_buttons(app, wrap) -> None:
    import tkinter as tk
    try:
        from modules import logic_actions
    except Exception:
        return

    def _collect_buttons(widget, collected):
        try:
            children = widget.winfo_children()
        except Exception:
            return
        for child in children:
            try:
                if isinstance(child, tk.Button):
                    collected.append(child)
            except Exception:
                pass
            _collect_buttons(child, collected)

    buttons = []
    _collect_buttons(wrap, buttons)
    if not buttons:
        return

    delete_btn = None
    rename_btn = None
    undo_btn = None

    for btn in buttons:
        try:
            label = str(btn.cget('text')).strip().lower()
        except Exception:
            continue
        if 'löschen' in label or 'delete' in label:
            if delete_btn is None:
                delete_btn = btn
        elif 'rename' in label or 'umbenennen' in label or 'name ändern' in label or 'namensänderung' in label:
            if rename_btn is None:
                rename_btn = btn
        elif 'undo' in label or 'rückgängig' in label:
            if undo_btn is None:
                undo_btn = btn

    if not delete_btn or not rename_btn or not undo_btn:
        sequence = []
        for btn in buttons:
            try:
                label = str(btn.cget('text')).strip().lower()
            except Exception:
                label = ''
            if 'run' in label or 'start' in label or 'ausführen' in label:
                continue
            sequence.append(btn)
        if not delete_btn and len(sequence) > 1:
            delete_btn = sequence[1]
        if not rename_btn and len(sequence) > 2:
            rename_btn = sequence[2]
        if not undo_btn and len(sequence) > 3:
            undo_btn = sequence[3]

    try:
        if delete_btn is not None:
            delete_btn.configure(command=lambda a=app: logic_actions.action_tree_delete(a))
        if rename_btn is not None:
            rename_btn.configure(command=lambda a=app: logic_actions.action_tree_rename(a))
        if undo_btn is not None:
            undo_btn.configure(command=lambda a=app: logic_actions.action_tree_undo(a))
    except Exception:
        pass


def enable_lasso(app) -> None:
    """
    Aktiviert einen einfachen Lasso-/Drag-Multiselect auf der TreeView.

    Verhalten:
    - Linke Maustaste gedrueckt halten und ueber Eintraege fahren:
      Eintraege werden beim Ueberfahren der Maus zur Auswahl hinzugefuegt.
    - Bestehende Selektion bleibt erhalten (additiv).
    """
    tree = getattr(app, "tree", None)
    if tree is None:
        return

    state = {
        "active": False,
        "last_item": None,
    }

    def _on_lasso_start(event):
        try:
            state["active"] = True
            item = tree.identify_row(event.y)
            state["last_item"] = item
            if item:
                # additiv selektieren, nicht löschen
                try:
                    sel = tree.selection()
                    if item not in sel:
                        tree.selection_add(item)
                except Exception:
                    pass
        except Exception:
            state["active"] = False

    def _on_lasso_drag(event):
        if not state.get("active"):
            return
        try:
            item = tree.identify_row(event.y)
            if not item or item == state.get("last_item"):
                return
            state["last_item"] = item
            try:
                sel = tree.selection()
                if item not in sel:
                    tree.selection_add(item)
            except Exception:
                pass
        except Exception:
            state["active"] = False

    def _on_lasso_end(event):
        state["active"] = False

    # Events additiv binden, damit bestehende Bindings erhalten bleiben
    try:
        tree.bind("<Button-1>", _on_lasso_start, add="+")
        tree.bind("<B1-Motion>", _on_lasso_drag, add="+")
        tree.bind("<ButtonRelease-1>", _on_lasso_end, add="+")
    except Exception:
        pass


def enable_context_menu(app) -> None:
    """
    Aktiviert ein Kontextmenue auf der TreeView (rechte Liste):

    - Rechtsklick auf einen Eintrag:
        * Auswahl ggf. auf diesen Eintrag setzen
        * Menue mit "Pfad(e) kopieren" anzeigen
    - "Pfad(e) kopieren":
        * Alle selektierten Pfade (tree_paths) werden in die Zwischenablage
          kopiert (als Zeilenliste).
    """
    tree = getattr(app, "tree", None)
    paths = getattr(app, "tree_paths", {})

    if tree is None:
        return

    # Lokaler Import, um keine globalen Abhaengigkeiten zu erzwingen
    import tkinter as tk

    menu = tk.Menu(tree, tearoff=False)

    def _copy_selected():
        try:
            sel = tree.selection()
        except Exception:
            sel = ()
        collected: list[str] = []
        try:
            for item in sel:
                try:
                    p = paths.get(item)
                except Exception:
                    p = None
                if p:
                    collected.append(str(p))
        except Exception:
            collected = []

        data = "\n".join(collected)
        try:
            app.clipboard_clear()
            if data:
                app.clipboard_append(data)
        except Exception:
            # Clipboard darf nie crashen
            pass

    menu.add_command(label="Pfad(e) kopieren", command=_copy_selected)

    def _on_context(event):
        try:
            # Row unter Maus ermitteln
            row = tree.identify_row(event.y)
            if row:
                try:
                    current_sel = tree.selection()
                except Exception:
                    current_sel = ()
                # Wenn der angeklickte Eintrag noch nicht selektiert ist,
                # ihn selektieren (alleine oder additiv, je nach Modifier)
                if row not in current_sel:
                    # Strg gedrueckt? -> additiv, sonst Selektion ersetzen
                    try:
                        if (event.state & 0x0004):  # Control-Key
                            tree.selection_add(row)
                        else:
                            tree.selection_set(row)
                    except Exception:
                        tree.selection_set(row)
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            try:
                menu.grab_release()
            except Exception:
                pass

    try:
        tree.bind("<Button-3>", _on_context, add="+")
    except Exception:
        pass

