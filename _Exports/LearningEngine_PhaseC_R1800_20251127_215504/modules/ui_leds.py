from __future__ import annotations

import os
import ast
import warnings
import tkinter as tk

BG = "#e7e5d8"
GREEN = "#15c715"
RED = "#cc2020"
GREY = "#777777"


class LEDBar:
    """
    LED-Bar fuer den Intake-Tab.
    Keys:
      - "syntax"
      - "nameext"
      - "exists"
      - "target"
    """

    def __init__(self, parent: tk.Misc, callbacks: dict[str, object] | None = None) -> None:
        self.frame = tk.Frame(parent, bg=BG)
        # R1690: LED-Bar horizontal neben dem AOT-Button anordnen
        self.frame.pack(side="left", padx=6, pady=6)

        self._items: dict[str, tk.Canvas] = {}
        self._callbacks = callbacks or {}
        self._add("syntax", "Syntax", GREY)
        self._add("nameext", "Name/Ext", GREY)
        self._add("exists", "Datei", GREY)
        self._add("target", "Zielpfad", GREY)
        self._add("aot", "AOT", GREY)

    def _add(self, key: str, label: str, color: str) -> None:
        holder = tk.Frame(self.frame, bg=BG)
        holder.pack(side="left", padx=10)

        canvas = tk.Canvas(holder, width=18, height=18, bg=BG, highlightthickness=0)
        canvas.pack(side="top")
        canvas.create_oval(2, 2, 16, 16, fill=color, outline="#333333", width=1)

        tk.Label(holder, text=label, bg=BG).pack(side="top")
        self._items[key] = canvas

        # Klick-Handler, falls ein Callback fuer diese LED registriert ist
        if hasattr(self, "_callbacks") and key in self._callbacks:

            def _on_click(_event, k=key):
                cb = self._callbacks.get(k)
                if callable(cb):
                    try:
                        cb()
                    except Exception:
                        # LED-Callbacks duerfen die UI nie crashen
                        pass

            canvas.bind("<Button-1>", _on_click)
            holder.bind("<Button-1>", _on_click)

    def _set_color(self, key: str, color: str) -> None:
        canvas = self._items.get(key)
        if not canvas:
            return
        canvas.delete("all")
        canvas.create_oval(2, 2, 16, 16, fill=color, outline="#333333", width=1)

    def set_ok(self, key: str) -> None:
        self._set_color(key, GREEN)

    def set_fail(self, key: str) -> None:
        self._set_color(key, RED)

    def set_unknown(self, key: str) -> None:
        self._set_color(key, GREY)


def _get_strvar(app, attr: str) -> str:
    v = getattr(app, attr, None)
    try:
        return v.get().strip()
    except Exception:
        return ""


def _get_code(app) -> str:
    """
    Versucht, den Text-Inhalt des Intake-Editors zu ermitteln.
    Unterstuetzt mehrere moegliche Attributnamen (robust).
    """
    widget = None
    for name in ("txt_intake", "txt_code", "text_code", "code_text", "intake_text"):
        widget = getattr(app, name, None)
        if widget is not None:
            break
    if widget is None:
        return ""
    try:
        return widget.get("1.0", "end-1c")
    except Exception:
        return ""


def evaluate(app) -> None:
    """
    Aktualisiert alle Intake-LEDs anhand des aktuellen Zustands von:
      - var_name
      - var_ext
      - var_target_dir
      - Textinhalt (Syntax)
    Falls irgendetwas fehlt oder schiefgeht, werden die LEDs maximal
    defensiv aktualisiert (keine Exceptions in der UI!).
    """
    ledbar = getattr(app, "ledbar", None)
    if ledbar is None:
        return

    # --- Name/Ext ---------------------------------------------------------
    name = _get_strvar(app, "var_name")
    ext = _get_strvar(app, "var_ext").lstrip(".")
    if name and ext:
        ledbar.set_ok("nameext")
    elif name or ext:
        ledbar.set_fail("nameext")
    else:
        ledbar.set_unknown("nameext")

    # --- Zielpfad ---------------------------------------------------------
    target = _get_strvar(app, "var_target_dir")
    if target and os.path.isdir(target):
        ledbar.set_ok("target")
    elif target:
        ledbar.set_fail("target")
    else:
        ledbar.set_unknown("target")

    # --- Datei-Existenz ---------------------------------------------------
    if name and ext and target:
        path = os.path.join(target, f"{name}.{ext}")
        if os.path.isfile(path):
            ledbar.set_ok("exists")
        else:
            ledbar.set_fail("exists")
    else:
        ledbar.set_unknown("exists")

    # --- Syntax -----------------------------------------------------------
    code = _get_code(app)
    if not code.strip():
        # Kein Code => neutral
        ledbar.set_unknown("syntax")
        return

    # Endung aus Intake lesen, sofern vorhanden. Fallback: var_ext.
    raw_ext = _get_strvar(app, "var_intake_ext")
    if not raw_ext:
        raw_ext = _get_strvar(app, "var_ext")
    ext = raw_ext.lstrip(".").lower()
    # Nur fuer Python oder noch nicht gesetzte Endung wirklich pruefen
    if ext not in ("", "py"):
        ledbar.set_unknown("syntax")
        return

    import warnings

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            ast.parse(code)
        ledbar.set_ok("syntax")
    except SyntaxError as exc:
        # Echte Syntaxfehler -> ROT + Log
        try:
            from modules.logic_actions import log_debug

            log_debug(f"SyntaxLED: Parsefehler: {exc}")
        except Exception:
            pass
        ledbar.set_fail("syntax")
    except Exception as exc:
        # Andere Fehler im Parser -> neutral + Log
        try:
            from modules.logic_actions import log_debug

            log_debug(f"SyntaxLED: unerwarteter Fehler: {exc}")
        except Exception:
            pass
        ledbar.set_unknown("syntax")
