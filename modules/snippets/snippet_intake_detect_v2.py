"""
snippet_intake_detect_v2
Robuste Intake-Erkennung:
- Endung .py/.bat via Heuristik + Compile-Fallback für Python
- Name aus Runner_####_* oder Fallback snippet_YYYYMMDD_HHMMSS
- LEDs/Status werden über vorhandene Variablen der Host-Instanz gesetzt:
    self.var_name (StringVar), self.var_ext (StringVar)
    self.led_name, self.led_ext, self.led_syntax, self.led_all  (BooleanVars)
    self.var_stat (StringVar)
    self.editor (Text)
    self._hilite_err(line_no|None)
    self._update_leds()
"""

from __future__ import annotations
import re, time


def detect_ext(text: str) -> str:
    t = text or ""
    tl = t.lstrip().lower()

    # .bat sehr eindeutig
    if tl.startswith("@echo off") or any(
        kw in tl
        for kw in (
            "\nrem ",
            "\r\nrem ",
            "\n::",
            "\r\n::",
            "\ngoto ",
            "\r\ngoto ",
            "\n set ",
            "\r\n set ",
        )
    ):
        return ".bat"

    # .py heuristisch
    if tl.startswith("#!") and "python" in tl[:80]:
        return ".py"
    if any(k in t for k in ("import ", "from ", "def ", "class ", "print(", "__name__")):
        return ".py"

    # Compile-Fallback: kompilierbar => .py
    try:
        compile(t, "<detect>", "exec")
        return ".py"
    except Exception:
        pass

    return ".txt"


def _detect_name(text: str, current: str | None) -> str:
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.lower().startswith(("rem", "::")):
            continue
        m = re.search(r"(Runner_[0-9]{3,5}_[A-Za-z0-9_]+)", s)
        if m:
            return m.group(1)
    if current and current.strip():
        return current.strip()
    return "snippet_" + time.strftime("%Y%m%d_%H%M%S")


def run_detect(self) -> None:
    txt = self.editor.get("1.0", "end-1c")
    if not txt.strip():
        self.var_stat.set("Nichts zu erkennen.")
        return

    ext = detect_ext(txt)
    name = _detect_name(txt, self.var_name.get())

    # Syntax-Check nur bei .py
    syntax_ok = True
    err_line = None
    if ext == ".py":
        try:
            compile(txt, "<intake>", "exec")
        except SyntaxError as e:
            syntax_ok = False
            err_line = getattr(e, "lineno", None)
        except Exception:
            syntax_ok = False

    # UI aktualisieren
    try:
        self._hilite_err(err_line)
    except Exception:
        pass

    self.var_ext.set(ext)
    self.var_name.set(name)

    try:
        # LEDs setzen
        self.led_name.set(bool(name))
        self.led_ext.set(bool(ext))
    except Exception:
        pass

    try:
        self.led_syntax.set(bool(syntax_ok))
        self.led_all.set(bool(name and ext and syntax_ok))
    except Exception:
        pass

    try:
        self._update_leds()
    except Exception:
        pass

    self.var_stat.set(
        "Alles OK"
        if (name and ext and syntax_ok)
        else ("Syntaxfehler" if not syntax_ok else "Name/Endung prüfen")
    )
