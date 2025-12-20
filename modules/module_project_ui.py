import tkinter as tk
from tkinter import ttk

class ProjectFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Project").pack(anchor="w", padx=8, pady=8)
