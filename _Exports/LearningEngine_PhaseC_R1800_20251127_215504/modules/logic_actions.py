
# ============================================================
# logic_actions.py - FULL RESTORE VERSION (R1514)
# Kompatibel mit:
# - config_loader.py (INI)
# - ui_leds (Syntax Only for PY)
# - Intake (Name/Endung ohne Punkt)
# ============================================================

from __future__ import annotations

import os
import re
import ast
from datetime import datetime
from tkinter import messagebox


def log_debug(msg: str) -> None:
    """Schreibt eine Debugzeile in debug_output.txt (falls moeglich)."""
    try:
        import os
        from datetime import datetime
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        log_path = os.path.join(root, "debug_output.txt")
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[logic_actions] {ts} {msg}"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        # Logging darf nie die Logik zerstoeren
        pass


from . import config_loader


# ------------------------------------------------------------
# Hilfsmodule für Zugriff
# ------------------------------------------------------------

def _get_name_var(app):
    return getattr(app, "var_name", None)

def _get_ext_var(app):
    return getattr(app, "var_ext", None)

def _get_target_dir(app) -> str:
    return getattr(app, "var_target_dir", None).get().strip()

def _get_intake(app):
    return getattr(app, "txt_intake", None)

def _get_intake_text(app) -> str:
    w = _get_intake(app)
    return w.get("1.0", "end").rstrip("\n") if w else ""


# ------------------------------------------------------------
# Statusanzeige
# ------------------------------------------------------------


def _status(app, msg: str) -> None:
    """Statusmeldung setzen und gleichzeitig ins Debug-Log schreiben.

    Robust: funktioniert sowohl mit app.set_status(), app.status_var
    als auch mit einem einfachen Attribut app.var_status.
    """
    # GUI-Status, wenn vorhanden
    try:
        if hasattr(app, "set_status") and callable(getattr(app, "set_status")):
            app.set_status(msg)
        elif hasattr(app, "status_var"):
            try:
                app.status_var.set(msg)
            except Exception:
                pass
        elif hasattr(app, "var_status"):
            try:
                app.var_status.set(msg)
            except Exception:
                pass
    except Exception:
        # Status darf nie die App crashen
        pass

    # Immer ins Log schreiben
    log_debug(msg)



def _set_name_ext(app, name: str, ext: str) -> None:
    """
    Speichert Name & Endung in den Intake-Variablen.
    Endung IMMER ohne Punkt ("py", "cmd", "json"...)
    """
    v_n = _get_name_var(app)
    v_e = _get_ext_var(app)

    clean_ext = (ext or "").lstrip(".")

    if v_n:
        try:
            v_n.set(name)
        except Exception:
            pass

    if v_e:
        try:
            v_e.set(clean_ext)
        except Exception:
            pass


# ------------------------------------------------------------
# Endung erkennen (Heuristik)
# ------------------------------------------------------------


def _guess_ext(text: str) -> str:
    """
    Liefert Endung OHNE fuehrenden Punkt.
    Optimiert fuer ShrimpDev-Intake (Runner CMD/PY, JSON etc.).
    """
    import re

    t = text.lstrip()
    if not t:
        return "txt"

    lo = t.lower()

    # 1) Batch / CMD - zuerst pruefen
    if (
        t.startswith("@echo off")
        or "cmdextversion" in lo
        or "%~dp0" in lo
        or "goto :eof" in lo
        or "setlocal" in lo
    ):
        return "cmd"

    # 2) Python - typische Muster
    if (
        "def " in t
        or "class " in t
        or "import " in t
        or "from " in t
        or "if __name__" in t
    ):
        return "py"

    # 3) JSON
    if (t.startswith("{") or t.startswith("[")) and (":" in t or "}" in t or "]" in t):
        return "json"

    # 4) HTML
    if "<!doctype html" in lo or "<html" in lo:
        return "html"

    # 5) XML
    if lo.startswith("<?xml") or ("</" in t and re.search(r"<\w+[^>]*>", t)):
        return "xml"

    # 6) YAML - strenger: key: value (ohne offensichtliche Code-Keywords)
    if re.search(r"^\s*[A-Za-z0-9_]+\s*:\s+[^:]+$", t, flags=re.MULTILINE):
        if "def " not in t and "class " not in t and "import " not in t and "from " not in t:
            return "yaml"

    # 7) Log-Pattern: Zeitstempel am Zeilenanfang
    if re.search(r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}", t, flags=re.MULTILINE):
        return "txt"

    # Fallback: Text
    return "txt"


def action_detect(app) -> None:
    """Erkennt Name (Runner-ID) und Endung aus dem Intake-Code.

    Regeln:
    - Name:
        1) Wenn im Text eine Runner-ID R1234 / R1234a / R12345 vorkommt,
           wird diese als Name verwendet.
        2) Wenn KEINE Runner-ID gefunden wird UND es wie ein CMD/PY-Skript
           aussieht, wird automatisch eine neue Runner-ID aus dem tools-Ordner
           generiert (B-Regel).
        3) Andernfalls: erste sinnvolle Zeile als Name, Fallback "Intake".

    - Endung:
        1) Python, wenn typische Python-Muster gefunden werden.
        2) CMD, wenn typische Batch-Muster gefunden werden.
        3) JSON bei offensichtlichem JSON.
        4) Sonst "txt".
    """
    import re
    import os

    try:
        text = _get_intake_text(app)
    except Exception as exc:
        try:
            messagebox.showerror("Intake", f"Kein Intake-Text verfuegbar: {exc}")
        except Exception:
            pass
        try:
            log_debug(f"action_detect: Kein Intake-Text: {exc}")
        except Exception:
            pass
        return

    if not text or not text.strip():
        _status(app, "Nichts zu erkennen - Intake ist leer.")
        return

    t = text
    lo = t.lower()

    # -------------------------
    # Endung erkennen (ext)
    # -------------------------
    is_py = any(key in t for key in ("def ", "class ", "import ", "from ", "if __name__"))
    is_cmd = (
        "@echo off" in lo
        or "setlocal" in lo
        or "%~dp0" in lo
        or "goto :eof" in lo
        or "cmdextversion" in lo
        or re.search(r"^\s*rem\b", t, flags=re.IGNORECASE | re.MULTILINE) is not None
    )

    if is_py:
        ext = "py"
    elif is_cmd:
        ext = "cmd"
    else:
        stripped = t.lstrip()
        if (stripped.startswith("{") or stripped.startswith("[")) and (":" in stripped or "}" in stripped or "]" in stripped):
            ext = "json"
        else:
            ext = "txt"

    # -------------------------
    # Name erkennen (name)
    # -------------------------
    name = ""

    # 1) Versuche eine Runner-ID im kompletten Text zu finden
    m = re.search(r"\bR(\d{3,5}[A-Za-z]?)\b", t)
    if m:
        name = f"R{m.group(1)}"
    else:
        # 2) Wenn es wie ein Runner-Skript aussieht (py/cmd),
        #    aber keine ID enthalten ist: automatisch neue ID vergeben.
        if ext in ("py", "cmd"):
            try:
                name = _generate_next_runner_id()
            except Exception as exc:
                try:
                    log_debug(f"_generate_next_runner_id Fehler: {exc}")
                except Exception:
                    pass
                name = ""
        # 3) Fallback: erste sinnvolle Zeile als Name, falls noch leer
        if not name:
            for line in t.splitlines():
                s = line.strip()
                if not s:
                    continue
                if s.startswith(("#", "//", "REM", ";")):
                    continue
                # erstes Token nehmen
                token = s.split()[0]
                # Sonderzeichen entfernen
                token = re.sub(r"[^0-9A-Za-z_]", "", token)
                if token:
                    name = token
                    break

    if not name:
        name = "Intake"

    # -------------------------
    # Ergebnis in die App schreiben
    # -------------------------
    try:
        _set_name_ext(app, name, ext)
    except Exception as exc:
        try:
            log_debug(f"action_detect: _set_name_ext-Fehler: {exc}")
        except Exception:
            pass
        try:
            messagebox.showerror("Intake", f"Fehler beim Setzen von Name/Endung: {exc}")
        except Exception:
            pass
        return

    _status(app, f"Erkannt: {name}.{ext}")
    try:
        log_debug(f"Erkennen (R1610): {name}.{ext}")
    except Exception:
        pass


def action_save(app) -> None:
    txt = _get_intake_text(app)
    target = _get_target_dir(app)

    v_n = _get_name_var(app)
    v_e = _get_ext_var(app)

    name = v_n.get().strip() if v_n else ""
    ext = v_e.get().strip() if v_e else ""

    if not name:
        messagebox.showwarning("Speichern", "Kein Name gesetzt. Bitte erst 'Erkennen'.")
        _status(app, "Speichern: Kein Name.")
        return

    # Endung bereinigen
    clean_ext = "".join(c for c in ext if c.isalnum())
    if not clean_ext:
        clean_ext = "py"

    if not target:
        messagebox.showwarning("Speichern", "Ungültiger Zielordner.")
        _status(app, "Speichern: Fehler - kein Zielordner.")
        return

    try:
        os.makedirs(target, exist_ok=True)
        path = os.path.join(target, f"{name}.{clean_ext}")

        # Backup
        if os.path.exists(path):
            bak = path + "." + datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
            os.replace(path, bak)

        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(txt)

        _status(app, f"Gespeichert: {path}")
        _fs_refresh_tree(app)

    except Exception as ex:
        _status(app, f"Speichern-Fehler: {ex}")


# ------------------------------------------------------------
# Neu
# ------------------------------------------------------------

def action_new(app) -> None:
    try:
        w = _get_intake(app)
        if w:
            w.delete("1.0", "end")

        v_n = _get_name_var(app)
        v_e = _get_ext_var(app)

        if v_n:
            v_n.set("")

        if v_e:
            v_e.set("")

        _status(app, "Neu erstellt.")
    except Exception as ex:
        _status(app, f"Neu-Fehler: {ex}")


# ------------------------------------------------------------
# Undo
# ------------------------------------------------------------

def action_undo(app, side: str | None = None) -> None:
    try:
        w = _get_intake(app)
        if w:
            w.edit_undo()
        _status(app, "Undo.")
    except Exception:
        _status(app, "Undo nicht möglich.")


# ------------------------------------------------------------
# Ausführen (Run) - für .py & .cmd
# ------------------------------------------------------------

def action_run(app) -> None:
    name = _get_name_var(app).get().strip()
    ext = _get_ext_var(app).get().strip()
    target = _get_target_dir(app)

    if not name or not ext:
        _status(app, "Run abgebrochen: Name/Endung fehlt.")
        return

    path = os.path.join(target, f"{name}.{ext}")
    if not os.path.isfile(path):
        _status(app, "Run: Datei existiert nicht.")
        return

    try:
        os.startfile(path)
        _status(app, f"Ausgeführt: {path}")
    except Exception as ex:
        _status(app, f"Run-Fehler: {ex}")


# ------------------------------------------------------------
# Delete
# ------------------------------------------------------------

def action_delete(app):
    name = _get_name_var(app).get().strip()
    ext = _get_ext_var(app).get().strip()
    target = _get_target_dir(app)

    path = os.path.join(target, f"{name}.{ext}")

    if not os.path.isfile(path):
        _status(app, "Delete: Datei nicht gefunden.")
        return

    try:
        os.remove(path)
        _status(app, f"Gelöscht: {path}")

        try:
            app.right_list.refresh()
        except Exception:
            pass

    except Exception as ex:
        _status(app, f"Löschen-Fehler: {ex}")


def action_learning_journal(app) -> None:
    """Öffnet den LearningJournal-Tab."""
    try:
        nb = getattr(app, "nb", None)
        tab = getattr(app, "tab_lj", None)
        if nb is None or tab is None:
            _status(app, "LearningJournal: Tab nicht verfügbar.")
            return
        nb.select(tab)
        _status(app, "LearningJournal geöffnet.")
    except Exception as e:
        _status(app, f"LearningJournal-Fehler: {e}")


# ---- R1529: Guard-Funktionen abgesichert (R9997 / R1351) ----

def action_guard_futurefix(app) -> None:
    """Startet den Guard-FutureFix-Runner (R9997), falls vorhanden."""
    try:
        action_run_rid(app, "R9997")
    except Exception as e:
        _status(app, f"FutureFix (R9997) Fehler: {e}")


def action_guard_futurefix_safe(app) -> None:
    """Startet den sicheren Guard-FutureFix-Runner (R1351), falls vorhanden."""
    try:
        action_run_rid(app, "R1351")
    except Exception as e:
        _status(app, f"FutureFix Safe (R1351) Fehler: {e}")


# ---- R1530: SonderRunner-Wrapper für R9998 / R9999 abgesichert ----

def action_r9998(app) -> None:
    """Startet SonderRunner R9998 (z.B. Build/Repair-Pipeline)."""
    try:
        action_run_rid(app, "R9998")
    except Exception as e:
        _status(app, f"R9998-Fehler: {e}")


def action_r9999(app) -> None:
    """Startet SonderRunner R9999 (Diagnose/Analyse)."""
    try:
        action_run_rid(app, "R9999")
    except Exception as e:
        _status(app, f"R9999-Fehler: {e}")


# =====================================================================
# R1604 - Intake Detect/Ext Fix (nicht-destruktiv, appended)
# =====================================================================

def _guess_ext_r1604(text: str) -> str:
    """Bestimmt die Dateiendung (OHNE Punkt) anhand des Inhalts.

    Erkennt u.a. JSON/YAML/INI/HTML/XML/SH/PS1/CMD/PY/JS/Logs.
    Fallback ist immer "txt", wenn nichts eindeutig ist.
    """
    import re

    t = text.lstrip()
    if not t:
        return "txt"

    lo = t.lower()

    # JSON (strukturierter Inhalt mit { } oder [ ])
    if (t.startswith("{") or t.startswith("[")) and (":" in t or "}" in t or "]" in t):
        return "json"

    # YAML (key: value Zeilen)
    if re.search(r"^\s*\w+\s*:\s+.+$", t, flags=re.MULTILINE):
        return "yaml"

    # INI ([Section])
    if re.search(r"^\s*\[.+?\]\s*$", t, flags=re.MULTILINE):
        return "ini"

    # HTML
    if "<!doctype html" in lo or "<html" in lo:
        return "html"

    # XML
    if lo.startswith("<?xml") or ("</" in t and re.search(r"<\w+[^>]*>", t)):
        return "xml"

    # Shell-Script
    if t.startswith("#!/bin/sh") or t.startswith("#!/bin/bash") or re.search(r"\bfi\b", lo):
        return "sh"

    # PowerShell-Script
    if t.startswith("#!/usr/bin/pwsh") or "$PSVersionTable" in t or re.search(r"\bparam\s*\(", lo):
        return "ps1"

    # Batch / CMD
    if t.startswith("@echo off") or re.search(r"^\s*REM\b", t, flags=re.MULTILINE) or re.search(r"\bcall\s+R\d{3,5}\b", t):
        return "cmd"

    # Python
    if "def " in t or "class " in t or "import " in t or "if __name__" in t:
        return "py"

    # JavaScript
    if "function " in t or ("=>" in t and "console.log" in t):
        return "js"

    # Log-Pattern: Zeitstempel am Zeilenanfang
    if re.search(r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}", t, flags=re.MULTILINE):
        return "txt"

    # Fallback: einfacher Text
    return "txt"


def action_detect_r1604(app) -> None:
    """Erkennt Name und Endung des aktuellen Intake-Codes.

    - Name:
      - zuerst Runner-ID R1234 / R1234a im Kopf (erste ~40 Zeilen)
      - Fallback: erste kurze Zeile ohne Leerzeichen
      - letzter Fallback: "Intake"
    - Endung:
      - ueber _guess_ext_r1604 (py/cmd/json/.../txt)
    """
    import re

    text = _get_intake_text(app)
    if not text.strip():
        _status(app, "Nichts zu erkennen - Intake ist leer.")
        return

    # Runner-ID im Kopf suchen
    head = "\n".join(text.splitlines()[:40])
    name = ""
    m = re.search(r"\bR(\d{3,5}[A-Za-z]?)\b", head)
    if m:
        name = f"R{m.group(1)}"
    else:
        # Fallback: erste einfache Zeile ohne Leerzeichen
        for line in text.splitlines():
            s = line.strip()
            if not s:
                continue
            if " " not in s and len(s) < 40:
                name = re.sub(r"[^0-9A-Za-z_]", "", s)
            break

    if not name:
        name = "Intake"

    ext = _guess_ext_r1604(text)
    _set_name_ext(app, name, ext)
    _status(app, f"Erkannt: {name}.{ext}")


# Sanftes Rebinding: Nur einmal ausführen, wenn Modul geladen wird.
try:
    _R1604_APPLIED
except NameError:
    _R1604_APPLIED = True
#    try:
#        _guess_ext = guess_ext_latest
#    except Exception:
#        pass
#    try:
#        action_detect = action_detect_latest
#    except Exception:
    pass



# =====================================================================
# R1606 - Intake-Ext-Fix (CMD/PY bevorzugt)
# =====================================================================

def _guess_ext_r1606(text: str) -> str:
    """CMD- und PY-Erkennung vor das bestehende _guess_ext schalten.

    - CMD: @echo off, setlocal, %~dp0, goto :eof, cmdextversion
    - PY : def/class/import/from/if __name__ strikt erkennen
    - sonst Rueckfall auf das bestehende _guess_ext(text)
    """
    t = text.lstrip()
    if not t:
        return "txt"

    lo = t.lower()

    # CMD sehr aggressiv erkennen
    if (
        "@echo off" in lo
        or "setlocal" in lo
        or "%~dp0" in lo
        or "goto :eof" in lo
        or "cmdextversion" in lo
    ):
        return "cmd"

    # Python-Heuristik
    if (
        "def " in t
        or "class " in t
        or "import " in t
        or "from " in t
        or "if __name__" in t
    ):
        return "py"

    # Rueckfall: bisherige Heuristik
    try:
        return _guess_ext(text)
    except Exception:
        return "txt"


# =====================================================================
# R1607 - Intake-Detect & Ext-Fix (nicht-destruktiv, appended)
# =====================================================================

def _guess_ext_r1607(text: str) -> str:
    """Bestimmt Endung (ohne Punkt) mit Fokus auf CMD/PY.

    Erkennung:
    - CMD: typische Batch-Muster
    - PY : typische Python-Muster
    - JSON/HTML/XML: einfache Heuristik
    - sonst: 'txt'
    """
    t = text.lstrip()
    if not t:
        return "txt"

    lo = t.lower()

    # CMD - typische Muster
    if (
        "@echo off" in lo
        or "setlocal" in lo
        or "%~dp0" in lo
        or "goto :eof" in lo
        or "cmdextversion" in lo
    ):
        return "cmd"

    # Python - typische Muster
    if (
        "def " in t
        or "class " in t
        or "import " in t
        or "from " in t
        or "if __name__" in t
    ):
        return "py"

    # JSON
    if (t.startswith("{") or t.startswith("[")) and (":" in t or "}" in t or "]" in t):
        return "json"

    # HTML
    if "<!doctype html" in lo or "<html" in lo:
        return "html"

    # XML
    if lo.startswith("<?xml") or ("</" in t and "<" in t):
        return "xml"

    # Fallback: Text
    return "txt"


def action_detect_r1607(app) -> None:
    """Erkennt Name (Runner-ID) und Endung und schreibt sie ins UI.

    - Name:
        * Erstes Token 'Rxxxx' im Kopf (erste ~40 Zeilen)
        * Fallback: 'Intake'
    - Endung:
        * _guess_ext_r1607(text)
    """
    try:
        text = _get_intake_text(app)
    except Exception as exc:
        try:
            messagebox.showerror("Intake", f"Kein Intake-Text verfuegbar: {exc}")
        except Exception:
            pass
        log_debug(f"action_detect_r1607: Kein Intake-Text: {exc}")
        return

    if not text or not text.strip():
        _status(app, "Nichts zu erkennen - Intake ist leer.")
        return

    # Name bestimmen (Runner-ID aus Kopf)
    head = "\n".join(text.splitlines()[:40]).upper()
    name = ""

    for line in head.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.replace("=", " ").replace(":", " ").split()
        cand = None
        for p in parts:
            if len(p) >= 4 and p[0] == "R":
                digits = "".join(ch for ch in p[1:] if ch.isdigit())
                if 3 <= len(digits) <= 5:
                    cand = "R" + digits
                    break
        if cand:
            name = cand
            break

    if not name:
        name = "Intake"

    ext = _guess_ext_r1607(text)

    try:
        _set_name_ext(app, name, ext)
    except Exception as exc:
        log_debug(f"action_detect_r1607: _set_name_ext-Fehler: {exc}")
        try:
            messagebox.showerror("Intake", f"Fehler beim Setzen von Name/Endung: {exc}")
        except Exception:
            pass
        return

    _status(app, f"Erkannt: {name}.{ext}")
    log_debug(f"Erkennen: {name}.{ext}")


# R1607 einmalig anwenden: action_detect / _guess_ext umbiegen
try:
    _R1607_APPLIED
except NameError:
    _R1607_APPLIED = True
#    try:
#        _guess_ext = guess_ext_latest
#    except Exception:
#        pass
#    try:
#        action_detect = action_detect_latest
#    except Exception:
    pass




# =====================================================================
# R1608 - Intake Detect/Ext Final-Fix (append-only)
# =====================================================================

def _guess_ext_r1608(text: str) -> str:
    """Bestimmt Endung (ohne Punkt) mit klarer Prioritaet:

    1) Python (def/class/import/from/if __name__)
    2) CMD (@echo off, setlocal, %~dp0, goto :eof, cmdextversion, .bat)
    3) JSON ([{ ... }])
    4) Fallback: txt
    """
    t = text.lstrip()
    if not t:
        return "txt"

    lo = t.lower()

    # Python - zuerst
    if (
        "def " in t
        or "class " in t
        or "import " in t
        or "from " in t
        or "if __name__" in t
    ):
        return "py"

    # CMD
    if (
        "@echo off" in lo
        or "setlocal" in lo
        or "%~dp0" in lo
        or "goto :eof" in lo
        or "cmdextversion" in lo
        or ".bat" in lo
    ):
        return "cmd"

    # JSON
    if (t.startswith("{") or t.startswith("[")) and (":" in t or "}" in t or "]" in t):
        return "json"

    # Fallback: Text
    return "txt"


def action_detect_r1608(app) -> None:
    """Erkennt Name (Runner-ID) und Endung und schreibt sie ins UI.

    Name:
      - sucht im Kopf (erste ~40 Zeilen) nach Rxxxx
      - Fallback: 'Intake'
    Endung:
      - _guess_ext_r1608(text)
    """
    try:
        text = _get_intake_text(app)
    except Exception as exc:
        try:
            messagebox.showerror("Intake", f"Kein Intake-Text verfuegbar: {exc}")
        except Exception:
            pass
        try:
            log_debug(f"action_detect_r1608: Kein Intake-Text: {exc}")
        except NameError:
            pass
        return

    if not text or not text.strip():
        _status(app, "Nichts zu erkennen - Intake ist leer.")
        return

    head = "\n".join(text.splitlines()[:40]).upper()
    name = ""

    for line in head.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.replace("=", " ").replace(":", " ").split()
        cand = None
        for p in parts:
            if len(p) >= 4 and p[0] == "R":
                digits = "".join(ch for ch in p[1:] if ch.isdigit())
                if 3 <= len(digits) <= 5:
                    cand = "R" + digits
                    break
        if cand:
            name = cand
            break

    if not name:
        name = "Intake"

    ext = _guess_ext_r1608(text)

    try:
        _set_name_ext(app, name, ext)
    except Exception as exc:
        try:
            log_debug(f"action_detect_r1608: _set_name_ext-Fehler: {exc}")
        except NameError:
            pass
        try:
            messagebox.showerror("Intake", f"Fehler beim Setzen von Name/Endung: {exc}")
        except Exception:
            pass
        return

    _status(app, f"Erkannt: {name}.{ext}")
    try:
        log_debug(f"Erkennen (R1608): {name}.{ext}")
    except NameError:
        pass


# Einmalige Aktivierung: _guess_ext / action_detect auf R1608-Version legen
try:
    _R1608_APPLIED
except NameError:
    _R1608_APPLIED = True
#    try:
#        _guess_ext = guess_ext_latest
#   except Exception:
#        pass
#    try:
#        action_detect = action_detect_latest
#    except Exception:
    pass
# ======================================================================
# R1616 - Neue Intake-Erkennung (Name, Endung, Ziel)
# ======================================================================

def _guess_ext_r1616(text: str) -> str:
    """Bestimmt die Dateiendung aus dem Intake-Text."""
    t = text.lstrip()
    if not t:
        return "txt"

    lo = t.lower()

    # Python - typische Schlüsselwörter
    if (
        "def " in t
        or "class " in t
        or "import " in t
        or "from " in t
        or "if __name__" in t
    ):
        return "py"

    # CMD / Batch
    if (
        "@echo off" in lo
        or "setlocal" in lo
        or "%~dp0" in lo
        or "goto :eof" in lo
        or "cmdextversion" in lo
        or re.search(r"^\\s*rem\\b", t, flags=re.I | re.M)
    ):
        return "cmd"

    # JSON (sehr grob, aber brauchbar)
    st = t.lstrip()
    if (st.startswith("{") or st.startswith("[")) and (":" in st or "}" in st or "]" in st):
        return "json"

    return "txt"


def _generate_next_runner_id_r1616() -> str:
    """Erzeugt die nächste freie Runner-ID anhand der Dateien im tools-Ordner."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    tools = os.path.join(root, "tools")
    max_n = 999

    if os.path.isdir(tools):
        for fn in os.listdir(tools):
            m = re.match(r"^R(\\d{3,5})([A-Za-z]?)", fn)
            if not m:
                continue
            try:
                n = int(m.group(1))
            except ValueError:
                continue
            if n > max_n:
                max_n = n

    return f"R{max_n + 1}"


def action_detect_r1616(app) -> None:
    """Erkennt Name, Endung und Zielpfad aus dem Intake-Text."""
    try:
        text = _get_intake_text(app)
    except Exception as exc:
        _status(app, f"Erkennen-Fehler: Intake nicht verfügbar ({exc})")
        return

    if not text or not text.strip():
        _status(app, "Nichts zu erkennen - Intake ist leer.")
        return

    ext = _guess_ext_r1616(text)

    # 1) Versuche, eine Runner-ID im Text zu finden (R1234, R1234a ...)
    name = None
    m = re.search(r"\\bR(\\d{3,5}[A-Za-z]?)\\b", text)
    if m:
        name = "R" + m.group(1)

    # 2) Wenn keine ID und py/cmd -> neue Runner-ID erzeugen
    if not name and ext in ("py", "cmd"):
        name = _generate_next_runner_id_r1616()

    # 3) Fallback: ersten sinnvollen Token aus dem Text nehmen
    if not name:
        for line in text.splitlines():
            s = line.strip()
            if not s or s.startswith(("#", "//", "REM", ";")):
                continue
            token = re.sub(r"[^0-9A-Za-z_]", "", s.split()[0])
            if token:
                name = token
                break

    if not name:
        name = "Intake"

    # Name + Endung ins UI schreiben
    try:
        _set_name_ext(app, name, ext)
    except Exception as exc:
        _status(app, f"Fehler beim Setzen von Name/Endung: {exc}")
        return

    _status(app, f"Erkannt (R1616): {name}.{ext}")

    # Zielpfad: für py/cmd automatisch auf tools setzen,
    # sonst das bisherige Ziel unverändert lassen
    try:
        if ext in ("py", "cmd"):
            root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            tools_dir = os.path.join(root, "tools")
            if hasattr(app, "var_target_dir"):
                app.var_target_dir.set(tools_dir)
            if hasattr(app, "target"):
                app.target.set(tools_dir)
            if hasattr(app, "_target"):
                app._target.set(tools_dir)
            # ggf. Target-Variablen/Liste aktualisieren
            try:
                _sync_target_vars(app, tools_dir)
            except Exception:
                pass
    except Exception:
        # Zielpfad-Probleme sollen die Erkennung nicht crashen
        pass


# === R1616: aktiviert neue Detection ===
#_guess_ext = guess_ext_latest
#action_detect = action_detect_latest



# === DETECT MODERN START ===

def guess_ext_latest(text: str) -> str:
    """Erkennt die Endung anhand des Inhalts."""
    text_l = text.lower()
    if "python" in text_l:
        return "py"
    if text_l.strip().startswith("@echo") or ".cmd" in text_l:
        return "cmd"
    if "set \"RUNNER=" in text_l:
        if ".cmd" in text_l or "cmd" in text_l:
            return "cmd"
    if "run" in text_l and ".py" in text_l:
        return "py"
    return "py"


# def action_detect_latest(app):
    """Neue moderne Detect-Funktion."""
    try:
        text = app.txt_intake.get("1.0", "end")
    except:
        try:
            text = app.txt_code.get("1.0", "end")
        except:
            text = ""

    ext = guess_ext_latest(text)
    name = None

    m = re.search(r'RUNNER\s*=\s*"?(R\d{3,5}[A-Za-z]?)"?', text)
    if not m:
        m = re.search(r'\bR(\d{3,5}[A-Za-z]?)\b', text)
        if m:
            name = "R" + m.group(1)
    else:
        name = m.group(1)

    if not name:
        try:
            name = _generate_next_runner_id_r1616()
        except:
            name = "R9999"

    # Schreib zurück ins UI
    try:
        app.var_intake_name.set(name)
        app.var_intake_ext.set(ext)
    except:
        pass

    # Zielpfad aktualisieren
    try:
        if ext == "cmd" or ext == "py":
            tools = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools"))
            app.var_intake_target.set(tools)
    except:
        pass

    try:
        app.refresh_project_tree()
    except:
        pass

    try:
        _status(app, f"Erkannt: {name}.{ext}")
    except:
        pass

# === DETECT MODERN END ===

# =====================================================================
# R1620 - Unified Intake Detection Core (append-only, nicht-destruktiv)
# =====================================================================

import os as _r1620_os
import re as _r1620_re


def _intake_get_text_r1620(app) -> str:
    """
    Versucht, den Intake-Text aus den ueblichen Widgets zu holen.
    """
    # txt_intake
    for attr in ("txt_intake", "txt_code", "codearea"):
        try:
            widget = getattr(app, attr, None)
            if widget is None:
                continue
            try:
                return widget.get("1.0", "end")
            except Exception:
                # z. B. bei custom codearea-Implementierungen
                try:
                    return widget.get()
                except Exception:
                    continue
        except Exception:
            continue
    return ""


def guess_ext_latest(text: str) -> str:
    """
    Endungs-Heuristik (2A):
    - py: typische Python-Muster
    - cmd: typische Batch-Muster
    - json: einfache JSON-Erkennung
    - txt: sonst
    """
    if not text:
        return "txt"

    t = text.lstrip()
    lo = t.lower()

    # Python-Heuristik
    if (
        "def " in t
        or "class " in t
        or "import " in t
        or "from " in t
        or "if __name__" in t
    ):
        return "py"

    # Batch/CMD-Heuristik
    if (
        "@echo off" in lo
        or "setlocal" in lo
        or "%~dp0" in t
        or "goto :eof" in lo
        or "cmdextversion" in lo
        or _r1620_re.search(r"^\s*rem\b", lo, flags=_r1620_re.MULTILINE)
    ):
        return "cmd"

    # JSON grob
    st = t.lstrip()
    if (st.startswith("{") or st.startswith("[")) and (":" in st or "}" in st or "]" in st):
        return "json"

    return "txt"


def _generate_runner_id_r1620() -> str:
    """
    Erzeugt eine neue Runner-ID (1A-Fallback):
    - sucht im tools-Ordner nach Rxxxx(.cmd/.py/...)
    - nimmt hoechste Nummer + 1
    """
    root = _r1620_os.path.abspath(_r1620_os.path.join(_r1620_os.path.dirname(__file__), ".."))
    tools = _r1620_os.path.join(root, "tools")
    max_n = 999

    if _r1620_os.path.isdir(tools):
        for fn in _r1620_os.listdir(tools):
            m = _r1620_re.match(r"^R(\d{3,5})([A-Za-z]?)", fn)
            if not m:
                continue
            try:
                n = int(m.group(1))
            except ValueError:
                continue
            if n > max_n:
                max_n = n

    return f"R{max_n + 1}"


def _intake_set_name_ext_r1620(app, name: str, ext: str) -> None:
    """
    Setzt Name + Endung in die bekannten UI-Variablen.
    Nutzt bevorzugt _set_name_ext, faellt sonst auf Tk-Variablen zurueck.
    """
    # 1) bevorzugt die bestehende Hilfsfunktion nutzen, falls vorhanden
    try:
        from modules import logic_actions as _la_mod  # type: ignore
        if hasattr(_la_mod, "_set_name_ext"):
            try:
                _la_mod._set_name_ext(app, name, ext)  # type: ignore
                return
            except Exception:
                pass
    except Exception:
        pass

    # 2) Direkt auf typische Tk-Variablen gehen
    for attr in ("var_intake_name", "var_name", "var_filename"):
        try:
            var = getattr(app, attr, None)
            if var is not None:
                var.set(name)
                break
        except Exception:
            continue

    for attr in ("var_intake_ext", "var_ext"):
        try:
            var = getattr(app, attr, None)
            if var is not None:
                var.set(ext)
                break
        except Exception:
            continue


def _intake_set_target_r1620(app, ext: str) -> None:
    """
    Setzt je nach Endung den Zielpfad (3A):
    - py/cmd -> tools
    Andere Endungen lassen das Ziel unveraendert.
    """
    if ext not in ("py", "cmd"):
        return

    root = _r1620_os.path.abspath(_r1620_os.path.join(_r1620_os.path.dirname(__file__), ".."))
    tools_dir = _r1620_os.path.join(root, "tools")

    # Tk-Variablen setzen
    for attr in ("var_target_dir", "var_intake_target"):
        try:
            var = getattr(app, attr, None)
            if var is not None:
                var.set(tools_dir)
        except Exception:
            continue

    # interne Felder setzen
    for attr in ("target", "_target"):
        try:
            t = getattr(app, attr, None)
            if t is not None and hasattr(t, "set"):
                t.set(tools_dir)
        except Exception:
            continue

    # Sync-Funktion, falls vorhanden
    try:
        from modules import logic_actions as _la_mod  # type: ignore
        if hasattr(_la_mod, "_sync_target_vars"):
            try:
                _la_mod._sync_target_vars(app, tools_dir)  # type: ignore
            except Exception:
                pass
    except Exception:
        pass


def action_detect_latest(app) -> None:
    """
    Zentraler Detect (1A+2A+3A):

    - Text holen
    - Endung heuristisch bestimmen
    - Name bevorzugt aus Inhalt (RUNNER=Rxxxx oder Rxxxx im Text)
    - Falls keine ID gefunden: neue Runner-ID generieren
    - Name/Endung ins UI schreiben
    - Zielpfad fuer py/cmd auf tools setzen
    """
    # Text besorgen
    try:
        text = _intake_get_text_r1620(app)
    except Exception as exc:
        try:
            _status(app, f"Erkennen-Fehler (Textzugriff): {exc}")
        except Exception:
            pass
        return

    if not text or not text.strip():
        try:
            _status(app, "Nichts zu erkennen - Intake ist leer.")
        except Exception:
            pass
        return

    # Endung nach Heuristik
    ext = guess_ext_latest(text)

    # Name-Erkennung (1A)
    name = None

    # 1) RUNNER=Rxxxx im Text
    try:
        m = _r1620_re.search(r'RUNNER\s*=\s*"?((R\d{3,5}[A-Za-z]?))"?', text)
    except Exception:
        m = None
    if m:
        name = m.group(1)

    # 2) irgendeine Rxxxx im Text
    if not name:
        try:
            m = _r1620_re.search(r"\bR(\d{3,5}[A-Za-z]?)\b", text)
        except Exception:
            m = None
        if m:
            name = "R" + m.group(1)

    # 3) Fallback: neue Runner-ID
    if not name and ext in ("py", "cmd"):
        try:
            name = _generate_runner_id_r1620()
        except Exception:
            name = "R9999"

    # 4) letzter Fallback: neutrales Label
    if not name:
        name = "Intake"

    # Name + Endung ins UI schreiben
    try:
        _intake_set_name_ext_r1620(app, name, ext)
    except Exception:
        pass

    # Zielpfad ggf. setzen (3A)
    try:
        _intake_set_target_r1620(app, ext)
    except Exception:
        pass

    # Statusmeldung
    try:
        _status(app, f"Erkannt: {name}.{ext}")
    except Exception:
        pass




# ------------------------------------------------------------
# R1634 - Datei aus Projektliste in den Intake laden
# ------------------------------------------------------------

def load_file_into_intake(app, path: str) -> None:
    """Lädt eine Datei in den Intake, setzt Name/Endung,
    triggert Detect und aktualisiert die LEDs."""
    import os

    try:
        if not os.path.isfile(path):
            _status(app, f"Öffnen: Datei nicht gefunden ({path})")
            return

        # Inhalt lesen (robust gegen Encoding-Probleme)
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(path, "r", encoding="latin-1") as f:
                text = f.read()

        # In Intake schreiben
        w = _get_intake(app)
        if w is not None:
            try:
                w.delete("1.0", "end")
                w.insert("1.0", text)
            except Exception as exc:
                _status(app, f"Öffnen-Fehler (Intake): {exc}")
                return

        # Name + Endung aus Pfad ableiten
        base = os.path.basename(path)
        name, ext = os.path.splitext(base)
        ext_clean = ext.lstrip(".") or "txt"

        try:
            _set_name_ext(app, name, ext_clean)
        except Exception:
            # Name/Endung sind nice-to-have, dürfen aber nicht crashen
            pass

        # Detect laufen lassen
        try:
            action_detect(app)
        except Exception:
            pass

        # LEDs aktualisieren
        try:
            from modules import ui_leds
            ui_leds.evaluate(app)
        except Exception:
            pass

        _status(app, f"Geladen: {path}")

    except Exception as exc:
        _status(app, f"Öffnen-Fehler: {exc}")


# Bindings fuer aeltere Aufrufer
try:
    _guess_ext = guess_ext_latest
except Exception:
    pass

try:
    action_detect = action_detect_latest
except Exception:
    pass

# =====================================================================
# R1621 - Final Intake Detection Core (append-only, nicht-destruktiv)
# =====================================================================

import os as _r1621_os
import re as _r1621_re


def _intake_get_text_r1621(app) -> str:
    """
    Versucht, den Intake-Text aus den ueblichen Widgets zu holen.
    """
    for attr in ("txt_intake", "txt_code", "codearea"):
        try:
            widget = getattr(app, attr, None)
        except Exception:
            widget = None
        if widget is None:
            continue

        # Tk Text-Widget oder aehnliches
        for method, args in (("get", ("1.0", "end")), ("get", ()),):
            try:
                fn = getattr(widget, method, None)
                if fn is None:
                    continue
                text = fn(*args)
                if isinstance(text, str):
                    return text
            except Exception:
                continue

    return ""


def guess_ext_latest(text: str) -> str:
    """
    Endungs-Heuristik (2A):
    - py: typische Python-Muster
    - cmd: typische Batch-Muster
    - json: einfache JSON-Erkennung
    - txt: sonst
    """
    if not text:
        return "txt"

    t = text.lstrip()
    lo = t.lower()

    # Python-Heuristik
    if (
        "def " in t
        or "class " in t
        or "import " in t
        or "from " in t
        or "if __name__" in t
    ):
        return "py"

    # Batch/CMD-Heuristik
    if (
        "@echo off" in lo
        or "setlocal" in lo
        or "%~dp0" in t
        or "goto :eof" in lo
        or "cmdextversion" in lo
        or _r1621_re.search(r"^\s*rem\b", lo, flags=_r1621_re.MULTILINE)
    ):
        return "cmd"

    # JSON grob
    st = t.lstrip()
    if (st.startswith("{") or st.startswith("[")) and (":" in st or "}" in st or "]" in st):
        return "json"

    return "txt"


def _generate_runner_id_r1621() -> str:
    """
    Erzeugt eine neue Runner-ID (1A-Fallback):
    - sucht im tools-Ordner nach Rxxxx
    - nimmt hoechste Nummer + 1
    """
    root = _r1621_os.path.abspath(
        _r1621_os.path.join(_r1621_os.path.dirname(__file__), "..")
    )
    tools = _r1621_os.path.join(root, "tools")
    max_n = 999

    if _r1621_os.path.isdir(tools):
        for fn in _r1621_os.listdir(tools):
            m = _r1621_re.match(r"^R(\d{3,5})([A-Za-z]?)", fn)
            if not m:
                continue
            try:
                n = int(m.group(1))
            except ValueError:
                continue
            if n > max_n:
                max_n = n

    return f"R{max_n + 1}"


def _intake_set_name_ext_r1621(app, name: str, ext: str) -> None:
    """
    Setzt Name + Endung in die bekannten UI-Variablen.
    Nutzt bevorzugt _set_name_ext, faellt sonst auf Tk-Variablen zurueck.
    """
    # 1) bestehende Hilfsfunktion ausprobieren
    try:
        from modules import logic_actions as _la_mod  # type: ignore
        if hasattr(_la_mod, "_set_name_ext"):
            try:
                _la_mod._set_name_ext(app, name, ext)  # type: ignore
                return
            except Exception:
                pass
    except Exception:
        pass

    # 2) Direkt auf typische Tk-Variablen gehen
    for attr in ("var_intake_name", "var_name", "var_filename"):
        try:
            var = getattr(app, attr, None)
            if var is not None:
                var.set(name)
                break
        except Exception:
            continue

    for attr in ("var_intake_ext", "var_ext"):
        try:
            var = getattr(app, attr, None)
            if var is not None:
                var.set(ext)
                break
        except Exception:
            continue


def _intake_set_target_r1621(app, ext: str) -> None:
    """
    Setzt je nach Endung den Zielpfad (3A):
    - py/cmd -> tools
    Andere Endungen lassen das Ziel unveraendert.
    """
    if ext not in ("py", "cmd"):
        return

    root = _r1621_os.path.abspath(
        _r1621_os.path.join(_r1621_os.path.dirname(__file__), "..")
    )
    tools_dir = _r1621_os.path.join(root, "tools")

    # Tk-Variablen setzen
    for attr in ("var_target_dir", "var_intake_target"):
        try:
            var = getattr(app, attr, None)
            if var is not None:
                var.set(tools_dir)
        except Exception:
            continue

    # interne Felder setzen
    for attr in ("target", "_target"):
        try:
            t = getattr(app, attr, None)
            if t is not None and hasattr(t, "set"):
                t.set(tools_dir)
        except Exception:
            continue

    # Sync-Funktion, falls vorhanden
    try:
        from modules import logic_actions as _la_mod  # type: ignore
        if hasattr(_la_mod, "_sync_target_vars"):
            try:
                _la_mod._sync_target_vars(app, tools_dir)  # type: ignore
            except Exception:
                pass
    except Exception:
        pass


def action_detect_latest(app) -> None:
    """
    Zentraler Detect (1A+2A+3A):

    - Text holen
    - Endung heuristisch bestimmen
    - Name bevorzugt aus Inhalt (RUNNER=Rxxxx oder Rxxxx im Kopf)
    - Falls keine ID gefunden: neue Runner-ID generieren
    - Name/Endung ins UI schreiben
    - Zielpfad fuer py/cmd auf tools setzen
    - Project-Tree ggf. aktualisieren
    """
    # Text besorgen
    try:
        text = _intake_get_text_r1621(app)
    except Exception as exc:
        try:
            _status(app, f"Erkennen-Fehler (Textzugriff): {exc}")
        except Exception:
            pass
        return

    if not text or not text.strip():
        try:
            _status(app, "Nichts zu erkennen - Intake ist leer.")
        except Exception:
            pass
        return

    # Endung nach Heuristik
    ext = guess_ext_latest(text)

    # Name-Erkennung (1A)
    name = None

    # 1) RUNNER=Rxxxx im Text
    try:
        m = _r1621_re.search(r'RUNNER\s*=\s*"?((R\d{3,5}[A-Za-z]?))"?', text)
    except Exception:
        m = None
    if m:
        name = m.group(1)

    # 2) irgendeine Rxxxx im Kopfbereich
    if not name:
        head = "\n".join(text.splitlines()[:40])
        try:
            m = _r1621_re.search(r"\bR(\d{3,5}[A-Za-z]?)\b", head)
        except Exception:
            m = None
        if m:
            name = "R" + m.group(1)

    # 3) Fallback: neue Runner-ID (nur bei py/cmd)
    if not name and ext in ("py", "cmd"):
        try:
            name = _generate_runner_id_r1621()
        except Exception:
            name = "R9999"

    # 4) letzter Fallback: neutrales Label
    if not name:
        name = "Intake"

    # Name + Endung ins UI schreiben
    try:
        _intake_set_name_ext_r1621(app, name, ext)
    except Exception:
        pass

    # Zielpfad ggf. setzen (3A)
    try:
        _intake_set_target_r1621(app, ext)
    except Exception:
        pass

    # Project-Tree ggf. aktualisieren
    try:
        refresh = getattr(app, "refresh_project_tree", None)
        if callable(refresh):
            refresh()
    except Exception:
        pass

    # Statusmeldung
    try:
        _status(app, f"Erkannt: {name}.{ext}")
    except Exception:
        pass


# Bindings fuer aeltere Aufrufer
try:
    _guess_ext = guess_ext_latest
except Exception:
    pass

try:
    action_detect = action_detect_latest
except Exception:
    pass


class _FSUndoState:
    """Einfacher Container für Dateisystem-Undo-Informationen."""
    def __init__(self) -> None:
        self.kind: str | None = None  # "delete" oder "rename"
        self.old_path: str | None = None
        self.new_path: str | None = None
        self.content: str | None = None  # nur für delete


def _get_fs_undo_state(app) -> "_FSUndoState":
    state = getattr(app, "_fs_undo_state", None)
    if not isinstance(state, _FSUndoState):
        state = _FSUndoState()
        try:
            app._fs_undo_state = state
        except Exception:
            pass
    return state


def _fs_refresh_tree(app) -> None:
    """Aktualisiert die rechte Liste, falls verfügbar."""
    try:
        proxy = getattr(app, "right_list", None)
        if proxy is not None and hasattr(proxy, "refresh"):
            proxy.refresh()
    except Exception:
        pass


def _get_tree_selected_path(app) -> str | None:
    """Liefert den absoluten Pfad der markierten Datei in der rechten Liste."""
    tree = getattr(app, "tree", None)
    tree_paths = getattr(app, "tree_paths", None)
    if tree is None or not tree_paths:
        return None
    try:
        selection = tree.selection()
    except Exception:
        return None
    if not selection:
        return None
    item_id = selection[0]
    return tree_paths.get(item_id)


def action_tree_delete(app) -> None:
    """Löscht die aktuell markierte Datei rechts. Links (Intake) wird NICHT angefasst."""
    path = _get_tree_selected_path(app)
    if not path:
        _status(app, "Delete: Keine Datei in der rechten Liste markiert.")
        return

    if not os.path.isfile(path):
        _status(app, "Delete: Datei nicht gefunden.")
        return

    state = _get_fs_undo_state(app)

    content: str | None = None
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        content = None

    try:
        os.remove(path)
        state.kind = "delete"
        state.old_path = path
        state.new_path = None
        state.content = content
        _status(app, f"Gelöscht (rechts): {path}")
        _fs_refresh_tree(app)
    except Exception as ex:
        _status(app, f"Löschen-Fehler: {ex}")


def action_tree_rename(app) -> None:
    """Benennt die rechts markierte Datei um (Dialog). Intake bleibt unverändert."""
    from tkinter import simpledialog

    path_old = _get_tree_selected_path(app)
    if not path_old:
        _status(app, "Umbenennen: Keine Datei in der rechten Liste markiert.")
        return

    if not os.path.isfile(path_old):
        _status(app, "Umbenennen: Datei nicht gefunden.")
        return

    folder, filename = os.path.split(path_old)
    base, ext = os.path.splitext(filename)
    ext_clean = ext.lstrip(".")

    parent = getattr(app, "root", None)
    new_name = simpledialog.askstring(
        "Umbenennen",
        "Neuer Dateiname (ohne Endung):",
        initialvalue=base,
        parent=parent if hasattr(parent, "winfo_toplevel") else None,
    )
    if new_name is None:
        _status(app, "Umbenennen abgebrochen.")
        return

    new_name = new_name.strip()
    if not new_name:
        _status(app, "Umbenennen: Leerer Name.")
        return

    new_path = os.path.join(folder, f"{new_name}.{ext_clean}") if ext_clean else os.path.join(folder, new_name)
    if os.path.abspath(new_path) == os.path.abspath(path_old):
        _status(app, "Umbenennen: Name unverändert.")
        return
    if os.path.exists(new_path):
        _status(app, "Umbenennen: Zieldatei existiert bereits.")
        return

    state = _get_fs_undo_state(app)

    try:
        os.rename(path_old, new_path)
        state.kind = "rename"
        state.old_path = path_old
        state.new_path = new_path
        state.content = None
        _status(app, f"Umbenannt (rechts): {path_old} -> {new_path}")
        _fs_refresh_tree(app)
    except Exception as ex:
        _status(app, f"Umbenennen-Fehler: {ex}")


def action_tree_undo(app) -> None:
    """Undo nur für Delete/Umbenennen im Dateisystem. Intake bleibt unberührt."""
    state = _get_fs_undo_state(app)
    if not state.kind:
        _status(app, "Undo: Keine Dateisystem-Aktion vorhanden.")
        return

    try:
        if state.kind == "delete":
            if not state.old_path:
                _status(app, "Undo Delete: Kein Pfad gespeichert.")
            elif state.content is None:
                _status(app, "Undo Delete: Kein Inhalt gespeichert.")
            elif os.path.exists(state.old_path):
                _status(app, "Undo Delete: Datei existiert bereits.")
            else:
                os.makedirs(os.path.dirname(state.old_path), exist_ok=True)
                with open(state.old_path, "w", encoding="utf-8") as f:
                    f.write(state.content)
                _status(app, f"Undo Delete: {state.old_path} wiederhergestellt.")
        elif state.kind == "rename":
            if not state.old_path or not state.new_path:
                _status(app, "Undo Rename: Pfad unvollständig.")
            elif not os.path.exists(state.new_path):
                _status(app, "Undo Rename: Quelldatei nicht gefunden.")
            elif os.path.exists(state.old_path):
                _status(app, "Undo Rename: Zieldatei existiert bereits.")
            else:
                os.rename(state.new_path, state.old_path)
                _status(app, f"Undo Rename: {state.new_path} -> {state.old_path}")
        else:
            _status(app, "Undo: Unbekannter Typ.")
    except Exception as ex:
        _status(app, f"Undo-Fehler: {ex}")
    finally:
        state.kind = None
        state.old_path = None
        state.new_path = None
        state.content = None
        _fs_refresh_tree(app)
