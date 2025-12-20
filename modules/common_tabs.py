from __future__ import annotations
import tkinter as tk
from tkinter import ttk

def ensure_tab(app: tk.Tk, key: str, title: str, builder):
    """
    Stellt sicher, dass es EINEN Tab (Notebook) mit Schlüssel `key` gibt.
    Falls kein Notebook existiert, wird ein Toplevel als Fallback genutzt.
    """
    if not hasattr(app, "nb") or app.nb is None:
        # Fallback - sollte bei dir nicht passieren, Notebook ist vorhanden
        win = tk.Toplevel(app); win.title(title)
        frame = builder(win)
        frame.pack(fill="both", expand=True)
        return True

    if not hasattr(app, "_tab_registry"): app._tab_registry = {}
    if key in app._tab_registry:
        app.nb.select(app._tab_registry[key]["index"])
        return True

    container = ttk.Frame(app.nb)
    frame = builder(container)
    frame.pack(fill="both", expand=True)
    app.nb.add(container, text=title)
    app._tab_registry[key] = {"frame": container, "index": app.nb.index("end") - 1}
    app.nb.select(app._tab_registry[key]["index"])
    return True
