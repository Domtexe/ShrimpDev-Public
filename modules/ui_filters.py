import os
import tkinter as tk
from tkinter import filedialog
from modules import ui_theme_classic

from modules import config_loader


def browse_dir(app, var):
    path = filedialog.askdirectory(initialdir=var.get() or os.getcwd())
    if path:
        var.set(path)
        _save_target(path)
        actions_refresh(app)


def open_dir(path):
    if path:
        try:
            os.startfile(path)
        except Exception:
            pass


def refresh(app):
    """Aktualisiert die rechte Projektliste basierend auf dem Zielordner.

    Wird u.a. von ui_left_panel._on_target_changed() genutzt.
    """
    try:
        # Neue Logik: direkt ui_project_tree verwenden
        from modules import ui_project_tree as _pt

        _pt._load_dir(app)
    except Exception:
        # Fallback: alter Mechanismus, falls right_list noch existiert
        try:
            app.right_list.refresh()
        except Exception:
            pass


def _save_target(path: str):
    cfg = config_loader.load()
    if "Intake" not in cfg:
        cfg["Intake"] = {}
    cfg["Intake"]["last_target_dir"] = path
    config_loader.save(cfg)


def _load_target() -> str:
    cfg = config_loader.load()
    try:
        return cfg["Intake"].get("last_target_dir", "")
    except Exception:
        return ""


def _save_ext(ext: str) -> None:
    cfg = config_loader.load()
    if "Intake" not in cfg:
        cfg["Intake"] = {}
    cfg["Intake"]["last_ext"] = ext
    config_loader.save(cfg)


def _load_ext() -> str:
    cfg = config_loader.load()
    try:
        return cfg["Intake"].get("last_ext", "")
    except Exception:
        return ""


def build_filters(parent: tk.Widget, app):
    """
    Platzhalterzeile unterhalb des Zielordners.

    Die eigentliche Steuerung fuer Name/Endung liegt jetzt im linken Intake-Panel
    (ui_left_panel). Hier stellen wir nur sicher, dass app.name_var und app.ext_var
    als StringVar existieren, ohne weitere sichtbare Eingabefelder zu erzeugen.
    """
    frm = tk.Frame(parent, bg=ui_theme_classic.BG_MAIN)
    frm.pack(fill="x", padx=6, pady=(0, 4))

    # Sicherstellen, dass Name/Endung-Variablen vorhanden sind
    name_var = getattr(app, "name_var", None)
    if not isinstance(name_var, tk.StringVar):
        name_var = tk.StringVar(value="")
        app.name_var = name_var

    ext_var = getattr(app, "ext_var", None)
    if not isinstance(ext_var, tk.StringVar):
        ext_var = tk.StringVar(value=_load_ext())
        app.ext_var = ext_var

    # Intake-Standard: var_name / var_ext als Alias anbieten
    if not hasattr(app, "var_name") or not isinstance(app.var_name, tk.StringVar):
        app.var_name = name_var
    if not hasattr(app, "var_ext") or not isinstance(app.var_ext, tk.StringVar):
        app.var_ext = ext_var

    # Keine sichtbaren Widgets mehr - die alte Name/Endung-Zeile ist damit entfernt.
    return frm
