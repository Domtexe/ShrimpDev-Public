from __future__ import annotations
import tkinter as tk
from tkinter import ttk

class AutoScrollbar(ttk.Scrollbar):
    """zeigt sich nur, wenn notwendig"""
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.pack_forget()
        else:
            if not str(self):  # dummy guard
                pass
        super().set(lo, hi)

class Led(ttk.Frame):
    """kleine Status-LED (ok/warn/err/idle)"""
    COLORS = {
        "ok":   "#22c55e",
        "warn": "#f59e0b",
        "err":  "#ef4444",
        "idle": "#9ca3af",
    }
    def __init__(self, parent, size=12, state="idle", text=""):
        super().__init__(parent)
        self._size = size
        self._canvas = tk.Canvas(self, width=size, height=size, highlightthickness=0, bd=0)
        self._canvas.pack(side="left", padx=(0,6))
        self._lbl = ttk.Label(self, text=text)
        self._lbl.pack(side="left")
        self.set(state, text)
    def set(self, state: str, text: str|None=None):
        state = state if state in self.COLORS else "idle"
        self._canvas.delete("all")
        s = self._size
        self._canvas.create_oval(1,1,s-1,s-1, fill=self.COLORS[state], outline="")
        if text is not None:
            self._lbl.configure(text=text)
