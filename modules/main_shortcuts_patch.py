from __future__ import annotations
import tkinter as tk
from modules import ui_theme_classic as th

# ⌨️ Shortcuts & Statusmeldungen
def bind_shortcuts(app):
    app.bind_all("<Alt-n>",  lambda e: _status(app, "Neu"))
    app.bind_all("<Control-s>", lambda e: _status(app, "Speichern"))
    app.bind_all("<Control-z>", lambda e: _status(app, "Undo"))
    app.bind_all("<F5>", lambda e: _status(app, "Run"))
    app.bind_all("<F2>", lambda e: _status(app, "Rename"))

def _status(app, text:str):
    try:
        app._status.set(text)
    except Exception:
        pass
