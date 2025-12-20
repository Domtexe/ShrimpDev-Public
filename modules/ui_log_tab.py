from __future__ import annotations
"""
ui_log_tab – Log-Tab für ShrimpDev.

Funktionen:
- debug_output.txt anzeigen
- Buttons unten, zentriert:
    * Neu laden
    * Markiertes kopieren und zurück zu Intake
    * Sichtbares kopieren und zurück zu Intake
    * Gesamtes Log kopieren und zurück zu Intake
    * Zurück zu Intake
"""

from typing import Any
from pathlib import Path

import tkinter as tk
from tkinter import ttk

from . import ui_theme_classic


def _get_log_path() -> Path:
    root = Path(__file__).resolve().parent.parent
    return root / "debug_output.txt"


def _load_log(text: tk.Text) -> None:
    """Lädt den Inhalt der Logdatei in das Text-Widget."""
    text.configure(state="normal")
    text.delete("1.0", "end")
    try:
        log_path = _get_log_path()
        try:
            content = log_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            content = "Logdatei debug_output.txt wurde nicht gefunden."
        except Exception as exc:
            content = f"Fehler beim Laden der Logdatei: {exc}"
    except Exception as exc:
        content = f"Fehler beim Bestimmen des Log-Pfads: {exc}"

    text.insert("1.0", content)
    text.see("end")
    # Text bleibt 'normal', damit der Nutzer markieren kann.


def _copy_to_clipboard(app: Any, data: str) -> None:
    """Kopiert textuelle Daten in die Zwischenablage."""
    try:
        app.clipboard_clear()
        if data:
            app.clipboard_append(data)
    except Exception:
        # Clipboard darf niemals crashen
        pass


def _back_to_intake(app: Any) -> None:
    """Wechselt zurück zum Intake-Tab."""
    try:
        nb = getattr(app, "nb", None)
        tab_intake = getattr(app, "tab_intake", None)
        if nb is not None and tab_intake is not None:
            nb.select(tab_intake)
    except Exception:
        # Tab-Wechsel darf nicht crashen
        pass


def _copy_selected_and_back(app: Any, text: tk.Text) -> None:
    """Kopiert markierten Text und wechselt zurück zu Intake."""
    try:
        data = text.get("sel.first", "sel.last")
    except Exception:
        data = ""
    _copy_to_clipboard(app, data)
    _back_to_intake(app)


def _copy_visible_and_back(app: Any, text: tk.Text) -> None:
    """Kopiert den sichtbaren Bereich und wechselt zurück zu Intake."""
    try:
        top_index = text.index("@0,0")
        bottom_index = text.index("@0,%d" % text.winfo_height())
        data = text.get(top_index, bottom_index)
    except Exception:
        data = ""
    _copy_to_clipboard(app, data)
    _back_to_intake(app)


def _copy_all_and_back(app: Any, text: tk.Text) -> None:
    """Kopiert das gesamte Log und wechselt zurück zu Intake."""
    try:
        data = text.get("1.0", "end-1c")
    except Exception:
        data = ""
    _copy_to_clipboard(app, data)
    _back_to_intake(app)


def build_log_tab(parent: tk.Widget, app: Any) -> None:
    """
    Baut den Log-Tab:

    Mitte:
        Textbereich mit Scrollbars

    Unten, zentriert:
        [Neu laden] [Markiertes kopieren + zurück]
        [Sichtbares kopieren + zurück]
        [Gesamtes Log kopieren + zurück]
        [Zurück zu Intake]
    """
    BG = ui_theme_classic.BG_MAIN

    outer = ui_theme_classic.Frame(parent, bg=BG)
    outer.pack(fill="both", expand=True)

    # Log-Anzeige
    area = ui_theme_classic.Frame(outer, bg=BG)
    area.pack(fill="both", expand=True, padx=4, pady=(4, 4))

    text_widget = tk.Text(area, wrap="none")
    vsb = ttk.Scrollbar(area, orient="vertical", command=text_widget.yview)
    hsb = ttk.Scrollbar(area, orient="horizontal", command=text_widget.xview)

    text_widget.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    area.grid_rowconfigure(0, weight=1)
    area.grid_columnconfigure(0, weight=1)

    text_widget.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    # Button-Leiste unten, zentriert
    bottom = ui_theme_classic.Frame(outer, bg=BG)
    bottom.pack(fill="x", pady=(0, 6))

    btn_frame = ui_theme_classic.Frame(bottom, bg=BG)
    btn_frame.pack(anchor="center")

    btn_reload = ui_theme_classic.Button(
        btn_frame,
        text="Neu laden",
        command=lambda: (state.__setitem__('pos', 0), _load_log(text_widget)),
    )
    btn_reload.pack(side="left", padx=4, pady=2)

    btn_sel = ui_theme_classic.Button(
        btn_frame,
        text="Markiertes kopieren und zurück",
        command=lambda: _copy_selected_and_back(app, text_widget),
    )
    btn_sel.pack(side="left", padx=4, pady=2)

    btn_vis = ui_theme_classic.Button(
        btn_frame,
        text="Sichtbares kopieren und zurück",
        command=lambda: _copy_visible_and_back(app, text_widget),
    )
    btn_vis.pack(side="left", padx=4, pady=2)

    btn_all = ui_theme_classic.Button(
        btn_frame,
        text="Gesamtes Log kopieren und zurück",
        command=lambda: _copy_all_and_back(app, text_widget),
    )
    btn_all.pack(side="left", padx=4, pady=2)

    btn_back = ui_theme_classic.Button(
        btn_frame,
        text="Zurück zu Intake",
        command=lambda: _back_to_intake(app),
    )
    btn_back.pack(side="left", padx=4, pady=2)

    # Initialer Load
    _load_log(text_widget)

    # AUTO_TAIL_LOG_R2148
    state = {"pos": 0, "after_id": None}

    def _is_visible() -> bool:
        try:
            nb = getattr(app, "nb", None)
            if nb is None:
                return True
            cur = nb.select()
            return cur == str(parent)
        except Exception:
            return True

    def _at_bottom() -> bool:
        try:
            first, last = text_widget.yview()
            return last >= 0.995
        except Exception:
            return True

    def _tail_once() -> None:
        if not _is_visible():
            return
        log_path = _get_log_path()
        if not log_path.exists():
            return
        try:
            size = log_path.stat().st_size
        except Exception:
            return
        if state["pos"] > size:
            state["pos"] = 0
        if state["pos"] == 0:
            try:
                data = log_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                return
            text_widget.configure(state="normal")
            text_widget.delete("1.0", "end")
            text_widget.insert("1.0", data)
            state["pos"] = size
            try:
                text_widget.see("end")
            except Exception:
                pass
            return
        if size == state["pos"]:
            return
        try:
            with log_path.open("rb") as f:
                f.seek(state["pos"])
                chunk = f.read()
        except Exception:
            return
        try:
            txt = chunk.decode("utf-8", errors="replace")
        except Exception:
            return
        if not txt:
            return
        was_bottom = _at_bottom()
        text_widget.configure(state="normal")
        text_widget.insert("end", txt)
        state["pos"] = size
        if was_bottom:
            try:
                text_widget.see("end")
            except Exception:
                pass

    def _tick() -> None:
        try:
            _tail_once()
        except Exception:
            pass
        try:
            state["after_id"] = parent.after(1000, _tick)
        except Exception:
            state["after_id"] = None

    try:
        _tick()
    except Exception:
        pass
