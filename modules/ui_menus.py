import tkinter as tk
from tkinter import messagebox


def build_menu(app):
    m = tk.Menu(app)
    file = tk.Menu(m, tearoff=False)
    file.add_checkbutton(label="Always on Top", command=lambda: _toggle_top(app))
    file.add_separator()
    file.add_command(label="Beenden", command=app.destroy)
    m.add_cascade(label="File", menu=file)

    helpm = tk.Menu(m, tearoff=False)
    helpm.add_command(
        label="Info",
        command=lambda: messagebox.showinfo("ShrimpDev", "ShrimpDev - Development GUI"),
    )
    m.add_cascade(label="Help", menu=helpm)

    app.config(menu=m)


def _toggle_top(app):
    try:
        app.attributes("-topmost", not bool(app.attributes("-topmost")))
    except Exception:
        pass
