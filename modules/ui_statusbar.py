import tkinter as tk


def build_statusbar(app):
    bar = tk.Frame(app)
    bar.pack(fill="x", side="bottom")
    app._status = tk.StringVar(value="...")
    tk.Label(bar, textvariable=app._status, anchor="w").pack(fill="x", padx=8, pady=3)


def set_status(app, txt: str):
    if hasattr(app, "_status"):
        app._status.set(txt)
