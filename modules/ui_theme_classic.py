import tkinter as tk
from tkinter import ttk

# Klassische Standardfarben (hell)
BG_MAIN = "#e0e0d6"
BG_BTN = "#f2f2ef"
BG_ENTRY = "white"
BG_STATUS = "#d4d4cc"  # << NEU: Status-Bar Farbe
FG_TEXT = "black"

FONT_BASE = ("Segoe UI", 10)


def apply(app: tk.Tk) -> None:
    app.configure(bg=BG_MAIN)
    app.option_add("*Font", FONT_BASE)

    style = ttk.Style(app)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # Notebook
    style.configure("TNotebook", background=BG_MAIN)
    style.configure("TNotebook.Tab", background=BG_BTN, foreground=FG_TEXT, padding=(8, 3))
    style.map(
        "TNotebook.Tab", background=[("selected", "white")], foreground=[("selected", "black")]
    )

    # Treeview
    style.configure("Treeview", background="white", fieldbackground="white", foreground="black")


def Button(parent, **kw) -> tk.Button:
    kw.setdefault("bg", BG_BTN)
    kw.setdefault("fg", FG_TEXT)
    kw.setdefault("relief", "raised")
    kw.setdefault("bd", 1)
    kw.setdefault("highlightthickness", 0)
    return tk.Button(parent, **kw)


def Entry(parent, **kw) -> tk.Entry:
    kw.setdefault("bg", BG_ENTRY)
    kw.setdefault("fg", FG_TEXT)
    kw.setdefault("insertbackground", FG_TEXT)
    return tk.Entry(parent, **kw)


def Frame(parent, **kw) -> tk.Frame:
    kw.setdefault("bg", BG_MAIN)
    return tk.Frame(parent, **kw)
