from __future__ import annotations

import os
import ast
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
    # R1984: Nur .py-Dateien werden syntaktisch geprueft
    try:
        # Wenn keine LEDBar vorhanden ist, brechen wir frueh ab.
        if ledbar is None:
            return
        # Dateiendung aus var_ext lesen, falls vorhanden.
        ext_val = ""
        try:
            ext_var = getattr(app, "var_ext", None)
            if ext_var is not None:
                if hasattr(ext_var, "get"):
                    ext_val = (ext_var.get() or "").strip().lower()
                else:
                    ext_val = str(ext_var).strip().lower()
        except Exception:
            ext_val = ""
        ext_val = ext_val.lstrip(".")
        # Nur 'py' wird syntaktisch geprueft; alles andere -> UNKNOWN.
        if ext_val != "py":
            try:
                ledbar.set_unknown("syntax")
            except Exception:
                pass
            return
    except Exception:
        # Guard darf niemals das UI crashen.
        pass
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
        ledbar.set_unknown("nameext")  # R2028
        # Kein Code => neutral
        ledbar.set_unknown("syntax")
        return

    # R2022: Intake leer? -> Alle LEDs neutral
    if not code.strip():
        ledbar.set_unknown("syntax")
        ledbar.set_unknown("nameext")
        ledbar.set_unknown("exists")
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

    # R1986: Heuristik fuer Inhalt, der nicht nach Python aussieht
    try:
        # Nur bei expliziter Python-Endung pruefen wir den Inhalt grob.
        if ext == "py" and code:
            first_nonempty = ""
            for _line in code.splitlines():
                s = _line.strip()
                if s:
                    first_nonempty = s.lower()
                    break
            suspicious = False
            if first_nonempty.startswith("@echo"):
                suspicious = True
            elif first_nonempty.startswith("rem ") or first_nonempty == "rem":
                suspicious = True
            elif first_nonempty.startswith("::"):
                suspicious = True
            elif "%~dp0" in first_nonempty:
                suspicious = True
            if suspicious:
                try:
                    ledbar.set_unknown("syntax")
                except Exception:
                    pass
                try:
                    if hasattr(app, "set_status") and callable(getattr(app, "set_status")):
                        app.set_status(
                            "Hinweis: Inhalt wirkt nicht wie Python (Endung .py pruefen)"
                        )
                except Exception:
                    pass
                return
    except Exception:
        # Heuristik darf niemals das UI crashen.
        pass

    import warnings

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            ast.parse(_sanitize_code_for_syntax_check(code))
        ledbar.set_ok("syntax")
    except SyntaxError as exc:
        # Echte Syntaxfehler -> ROT + Log (nur einmal pro App-Lebensdauer)
        try:
            from modules.logic_actions import log_debug

            if not getattr(app, "_syntax_led_syntax_error_logged", False):
                log_debug(f"SyntaxLED: Parsefehler im Intake-Code: {exc}")
                setattr(app, "_syntax_led_syntax_error_logged", True)
        except Exception:
            pass
        # R1983: Syntaxfehler zusätzlich im ShrimpDev-Status anzeigen
        try:
            # Bevorzugt eine kurze Meldung mit Zeilennummer, falls verfuegbar
            msg = None
            try:
                line = getattr(exc, "lineno", None)
                base = getattr(exc, "msg", None) or str(exc)
                if line:
                    msg = f"Syntaxfehler in Zeile {line}: {base}"
                else:
                    msg = f"Syntaxfehler im Intake-Code: {base}"
            except Exception:
                msg = f"Syntaxfehler im Intake-Code: {exc}"
            if hasattr(app, "set_status") and callable(getattr(app, "set_status")):
                app.set_status(msg)
        except Exception:
            # Status-Update darf niemals das UI crashen
            pass
        ledbar.set_fail("syntax")
        # R1985: SyntaxError-Highlight im Editor
        try:
            # Editor ermitteln
            txt = None
            for name in ("txt_intake", "txt_code", "intake_text"):
                if hasattr(app, name):
                    txt = getattr(app, name)
                    break
            if txt:
                # vorhandene Tags löschen
                try:
                    txt.tag_delete("syntax_error")
                except Exception:
                    pass

                # Tag neu anlegen
                try:
                    txt.tag_config("syntax_error", background="#ffcccc")
                except Exception:
                    pass

                # Fehlerzeile hervorheben
                try:
                    line = getattr(exc, "lineno", None)
                    if line:
                        start = f"{line}.0"
                        end = f"{line}.end"
                        txt.tag_add("syntax_error", start, end)
                        txt.see(start)
                except Exception:
                    pass
        except Exception:
            pass

    except Exception as exc:
        # Andere Fehler im Parser -> neutral + Log (nur einmal pro App-Lebensdauer)
        try:
            from modules.logic_actions import log_debug

            if not getattr(app, "_syntax_led_other_error_logged", False):
                log_debug(f"SyntaxLED: unerwarteter Fehler im Syntax-Check: {exc}")
                setattr(app, "_syntax_led_other_error_logged", True)
        except Exception:
            pass
        ledbar.set_unknown("syntax")


# ---------------------------------------------------------------------------
# Helper fuer SyntaxLED (R1813): Code vor ast.parse() bereinigen
# ---------------------------------------------------------------------------


def _sanitize_code_for_syntax_check(code: str) -> str:
    """
    Ersetzt problematische Unicode-Zeichen durch ASCII-Varianten und entfernt
    Steuerzeichen, damit ast.parse nicht an z.B. '–' (U+2013) scheitert.
    Zusaetzlich werden typische Steuer-/Richtungszeichen wie BOM entfernt.
    """
    replacements = {
        "–": "-",
        "—": "-",
        "…": "...",
        "“": '"',
        "”": '"',
        "„": '"',
        "‚": "'",
        "‘": "'",
        "’": "'",
        "→": "->",
        "⇒": "=>",
        "\ufeff": "",
        "\u202a": "",
        "\u202b": "",
        "\u202d": "",
        "\u202e": "",
    }
    for bad, good in replacements.items():
        if bad in code:
            code = code.replace(bad, good)

    cleaned = []
    for ch in code:
        # \n und \t bleiben erhalten, andere Steuerzeichen fliegen raus
        if ord(ch) < 32 and ch not in ("\n", "\t"):
            continue
        cleaned.append(ch)
    return "".join(cleaned)
