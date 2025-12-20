from __future__ import annotations
"""
Toolbar-Modul für ShrimpDev.

- Linke Toolbar: Intake (Neu / Einfügen / Erkennen / Speichern / Undo)
- Rechte Toolbar: Runner-Liste (Run / Löschen / Rename / Undo + SonderRunner)
"""

from typing import Any

import tkinter as tk

from . import ui_theme_classic, ui_tooltips, ui_leds
from .logic_actions import (
    action_new,
    action_detect,
    action_save,
    action_undo,
    action_run,
    action_delete,
    action_learning_journal,
    action_guard_futurefix,
    action_guard_futurefix_safe,
    action_r9998,
    action_r9999,
    log_debug,
)



def _call_logic_action(app, name: str) -> None:
    """
    Dynamischer Aufruf einer Action aus modules.logic_actions.

    Wenn die Funktion existiert, wird sie mit (app) ausgeführt.
    Wenn nicht, wird eine Statusmeldung gesetzt, aber kein Fehler geworfen.
    """
    try:
        from . import logic_actions
    except Exception as exc:
        status = getattr(app, "status", None)
        if status is not None:
            try:
                status.configure(text=f"{name}: Importfehler ({exc})")
            except Exception:
                pass
        return

    func = getattr(logic_actions, name, None)
    if callable(func):
        try:
            func(app)
        except Exception as exc:
            status = getattr(app, "status", None)
            if status is not None:
                try:
                    status.configure(text=f"{name}: Fehler ({exc})")
                except Exception:
                    pass
    else:
        status = getattr(app, "status", None)
        if status is not None:
            try:
                status.configure(text=f"{name}: Aktion nicht verfügbar.")
            except Exception:
                pass



def _make_button(
    parent: tk.Widget,
    text: str,
    command,
    tooltip: str | None = None,
) -> tk.Button:
    btn = ui_theme_classic.Button(parent, text=text, command=command)
    btn.pack(side="left", padx=2, pady=0)
    if tooltip:
        ui_tooltips.add(btn, tooltip)
    return btn


def _wrap_with_led(app, func):
    """Wrappt eine Toolbar-Aktion und aktualisiert danach sicher die Intake-LEDs."""
    def _inner():
        try:
            func(app)
        finally:
            try:
                ui_leds.evaluate(app)
            except Exception as exc:
                # LED-Updates duerfen die UI niemals crashen, aber Fehler werden geloggt.
                try:
                    log_debug(f"LED evaluate failed in _wrap_with_led: {exc}")
                except Exception:
                    pass
    return _inner



def _get_intake_widget(app):
    # Liefert das Intake-Textwidget (intake_text / txt_intake), falls vorhanden.
    for cand in ("intake_text", "txt_intake"):
        w = getattr(app, cand, None)
        if w is not None:
            return w
    return None


def _action_insert_and_detect(app):
    # Fügt Code aus der Zwischenablage in den Intake ein und ruft danach action_detect(app) auf.
    try:
        text = app.clipboard_get()
    except Exception:
        text = ""
    if not text:
        status = getattr(app, "status", None)
        if status is not None:
            try:
                status.configure(text="Zwischenablage leer.")
            except Exception:
                pass
        return

    w = _get_intake_widget(app)
    if w is None:
        status = getattr(app, "status", None)
        if status is not None:
            try:
                status.configure(text="Einfügen: Kein Intake-Widget gefunden.")
            except Exception:
                pass
        return

    try:
        w.delete("1.0", "end")
        w.insert("1.0", text)
    except Exception:
        status = getattr(app, "status", None)
        if status is not None:
            try:
                status.configure(text="Einfügen fehlgeschlagen.")
            except Exception:
                pass
        return

    status = getattr(app, "status", None)
    if status is not None:
        try:
            status.configure(text="Code eingefügt (Zwischenablage).")
        except Exception:
            pass

    try:
        from .logic_actions import action_detect
        action_detect(app)
    except Exception:
        status = getattr(app, "status", None)
        if status is not None:
            try:
                status.configure(text="Erkennung nach Einfügen fehlgeschlagen.")
            except Exception:
                pass

def build_toolbar_left(parent: tk.Widget, app: Any) -> tk.Frame:
    """
    Linke Toolbar (Intake):

    [Neu] [Einfügen] [Erkennen] [Speichern] [Undo]
    """
    bar = ui_theme_classic.Frame(parent)

    _make_button(
        bar,
        "Neu",
        _wrap_with_led(app, action_new),
        "Intake leeren.",
    )
    _make_button(
        bar,
        "Einfügen",
        _wrap_with_led(app, _action_insert_and_detect),
        "Code aus der Zwischenablage in den Intake einfügen und erkennen.",
    )
    _make_button(
        bar,
        "Erkennen",
        _wrap_with_led(app, action_detect),
        "Name und Endung aus dem Intake-Code ermitteln.",
    )
    _make_button(
        bar,
        "Speichern",
        _wrap_with_led(app, action_save),
        "Datei im Zielordner speichern.",
    )
    _make_button(
        bar,
        "Undo",
        _wrap_with_led(app, action_undo),
        "Letzte Änderung im Editor (falls unterstützt) rückgängig machen.",
    )

    return bar


def build_toolbar_right(parent: tk.Widget, app: Any) -> tk.Frame:
    """
    Rechte Toolbar (Runner-Liste):

    Zeile 1: [Run] [Löschen] [Rename] [Undo]
    Zeile 2: [FutureFix] [FutureFix Safe] [Build Tools] [Diagnose]
    """
    outer = ui_theme_classic.Frame(parent)

    # Zeile 1 - Basisaktionen
    row1 = ui_theme_classic.Frame(outer)
    row1.pack(fill="x", pady=(0, 2))

    _make_button(
        row1,
        "Run",
        _wrap_with_led(app, action_run),
        "Markierten Runner bzw. Datei ausführen.",
    )
    _make_button(
        row1,
        "Löschen",
        _wrap_with_led(app, action_delete),
        "Markierte Datei löschen.",
    )
    _make_button(
        row1,
        "Rename",
        _wrap_with_led(app, _action_rename_stub),
        "Markierte Datei anhand der Felder Name/Endung umbenennen.",
    )
    _make_button(
        row1,
        "Undo",
        _wrap_with_led(app, action_undo),
        "Einfaches Undo (Editor).",
    )

    # Zeile 2 - SonderRunner
    row2 = ui_theme_classic.Frame(outer)
    row2.pack(fill="x", pady=(0, 0))

    _make_button(
        row2,
        "FutureFix (R9997)",
        _wrap_with_led(app, action_guard_futurefix),
        "SonderRunner R9997: Future-Fix Guard ausführen.",
    )
    _make_button(
        row2,
        "FutureFix Safe (R1351)",
        _wrap_with_led(app, action_guard_futurefix_safe),
        "SonderRunner R1351: Future-Fix Safe ausführen.",
    )
    _make_button(
        row2,
        "Build Tools (R9998)",
        _wrap_with_led(app, action_r9998),
        "SonderRunner R9998: Build-/Tools-Runner.",
    )
    _make_button(
        row2,
        "Diagnose (R9999)",
        _wrap_with_led(app, action_r9999),
        "SonderRunner R9999: Diagnose-/Analyse-Runner.",
    )

    return outer


def build_toolbar(parent: tk.Widget, app: Any, side: str = "left") -> tk.Frame:
    """Kompatibilitäts-Hook."""
    if side == "right":
        return build_toolbar_right(parent, app)
    return build_toolbar_left(parent, app)


def _action_rename_stub(app):
    """Adapter für den Rename-Button - ruft die echte action_rename(app) auf."""
    try:
        from .logic_actions import action_rename
    except Exception as exc:  # Import sollte normalerweise funktionieren
        status = getattr(app, "status", None)
        if status is not None:
            try:
                status.configure(text=f"Rename: Importfehler ({exc})")
            except Exception:
                pass
        return

    try:
        action_rename(app)
    except Exception as exc:
        status = getattr(app, "status", None)
        if status is not None:
            try:
                status.configure(text=f"Rename-Fehler: {exc}")
            except Exception:
                pass
