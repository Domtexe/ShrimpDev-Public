from __future__ import annotations

import tkinter as tk
from typing import Optional


class _ToolTip:
    """Einfaches Tooltip-Widget für Tk-Widgets."""

    def __init__(self, widget: tk.Widget, text: str, delay_ms: int = 500) -> None:
        self.widget = widget
        self.text = text
        self.delay_ms = delay_ms
        self._after_id: Optional[str] = None
        self._tip: Optional[tk.Toplevel] = None

        widget.bind("<Enter>", self._on_enter, add="+")
        widget.bind("<Leave>", self._on_leave, add="+")
        widget.bind("<ButtonPress>", self._on_leave, add="+")

    def _on_enter(self, _event=None) -> None:
        self._schedule()

    def _on_leave(self, _event=None) -> None:
        self._unschedule()
        self._hide()

    def _schedule(self) -> None:
        self._unschedule()
        self._after_id = self.widget.after(self.delay_ms, self._show)

    def _unschedule(self) -> None:
        if self._after_id is not None:
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _show(self) -> None:
        if self._tip is not None or not self.text:
            return

        root = self.widget.winfo_toplevel()
        self._tip = tk.Toplevel(root)
        self._tip.wm_overrideredirect(True)
        self._tip.wm_attributes("-topmost", True)

        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self._tip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self._tip,
            text=self.text,
            justify="left",
            relief="solid",
            borderwidth=1,
            padx=4,
            pady=2,
            bg="#ffffe0",
        )
        label.pack(ipadx=1)

    def _hide(self) -> None:
        if self._tip is not None:
            try:
                self._tip.destroy()
            except Exception:
                pass
            self._tip = None


def add(widget: tk.Widget, text: str) -> None:
    """Tooltip an ein Widget hängen."""
    if not text:
        return
    _ToolTip(widget, text)
