import tkinter as tk
from tkinter import ttk

_TREE = "proj_tree"

def create_tree(parent, app):
    cols = ("path","type","note")
    tree = ttk.Treeview(parent, columns=cols, show="headings", name=_TREE)
    for c in cols:
        tree.heading(c, text=c.capitalize())
        tree.column(c, width=260 if c=="path" else 140, anchor="w")
    tree.pack(fill="both", expand=True, padx=12, pady=(8,12))
    # neutrale Beispielzeile
    tree.insert("", "end", values=(".", "ProjectRoot", "ShrimpDev"))

def bind_handlers(app):  # optional zukünftige Doppelklick-Aktionen
    pass
