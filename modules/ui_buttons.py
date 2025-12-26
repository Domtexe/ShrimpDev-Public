import tkinter as tk
from tkinter import messagebox
import importlib, os, subprocess, sys


def create_buttons(parent, app):
    frm = tk.Frame(parent)
    frm.pack(anchor="w", padx=12, pady=10)

    tk.Button(frm, text="Scan Project", command=lambda: _scan(app)).grid(row=0, column=0, padx=6)
    tk.Button(frm, text="Syntax Check", command=lambda: _syntax(app)).grid(row=0, column=1, padx=6)
    tk.Button(frm, text="Reload Modules", command=lambda: _reload(app)).grid(
        row=0, column=2, padx=6
    )
    tk.Button(frm, text="Run Runner...", command=lambda: _run_runner(app)).grid(
        row=0, column=3, padx=6
    )
    tk.Button(frm, text="Open Logs", command=lambda: _open_logs(app)).grid(row=0, column=4, padx=6)


def _scan(app):
    from .logic_intake import do_scan

    do_scan(app)


def _syntax(app):
    try:
        # einfacher Syntax-Check der wichtigsten Dateien
        import py_compile

        py_compile.compile("main_gui.py", doraise=True)
        messagebox.showinfo("Syntax", "OK: main_gui.py")
    except Exception as ex:
        messagebox.showerror("Syntax", str(ex))


def _reload(app):
    try:
        importlib.invalidate_caches()
        # Zielmodule neu laden
        for mod in (
            "modules.ui_menus",
            "modules.ui_buttons",
            "modules.ui_lists",
            "modules.ui_statusbar",
            "modules.ui_themes",
            "modules.logic_intake",
        ):
            if mod in sys.modules:
                importlib.reload(sys.modules[mod])
        messagebox.showinfo("Reload", "Module reloaded.")
    except Exception as ex:
        messagebox.showerror("Reload", str(ex))


def _run_runner(app):
    try:
        import tkinter.simpledialog as sd

        name = sd.askstring("Runner", "Runner-Datei (z.B. tools\\R1434.py/.cmd):")
        if not name:
            return
        if name.lower().endswith(".cmd"):
            subprocess.Popen(name, shell=True)
        else:
            subprocess.Popen(["py", "-3", "-u", name], shell=False)
    except Exception as ex:
        messagebox.showerror("Runner", str(ex))


def _open_logs(app):
    try:
        path = os.path.join(os.getcwd(), "debug_output.txt")
        if os.path.exists(path):
            if sys.platform.startswith("win"):
                os.startfile(path)  # type: ignore
            else:
                messagebox.showinfo("Logs", path)
        else:
            messagebox.showinfo("Logs", "debug_output.txt nicht gefunden.")
    except Exception as ex:
        messagebox.showerror("Logs", str(ex))
