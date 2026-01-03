from __future__ import annotations

"""
Toolbar-Modul für ShrimpDev.

# R2134: SR Hilfe
SR_HELP_TEXT_R2134 = 'Service Runner (SR) – Kurzüberblick\n\nSR9997 – FutureFix:\n  Sammel-Button für zukünftige Fixes / Reparaturketten (schnell, experimenteller).\n\nSR1352 – FutureFix Safe:\n  Wie FutureFix, aber konservativer: weniger Risiko, mehr Checks.\n\nSR9998 – Build Tools:\n  Werkzeuge/Build-Helfer (Build/Patch/Tools vorbereiten).\n\nSR9999 – Diagnose:\n  Diagnose-Läufe/Checks (Fehleranalyse, Status, Problemstellen finden).\n\nSR1922 – Systemcheck:\n  System-/Projekt-Check (Struktur, Konsistenz, Basischecks).'

def _sr_help_popup_r2134():
    try:
        messagebox.showinfo('SR Hilfe', SR_HELP_TEXT_R2134)
    except Exception:
        pass

# R2133: SR Hilfe Text
SR_TEXT_R2133 = 'Service Runner (SR) – Kurzüberblick\n\nSR9997 – FutureFix:\n  Sammel-Button für zukünftige Fixes / Reparaturketten (schnell, experimenteller).\n\nSR1352 – FutureFix Safe:\n  Wie FutureFix, aber konservativer: weniger Risiko, mehr Checks.\n\nSR9998 – Build Tools:\n  Werkzeuge/Build-Helfer (z. B. Tools sammeln, patch/build vorbereiten).\n\nSR9999 – Diagnose:\n  Diagnose-Läufe/Checks (typisch: Fehleranalyse, Status, Problemstellen finden).\n\nSR1922 – Systemcheck:\n  System-/Projekt-Check (Grundgesundheit: Struktur, Dateien, Konsistenz, Basischecks).'

def _sr_help_popup_r2133():
    try:
        messagebox.showinfo('Service Runner (SR) Hilfe', SR_TEXT_R2133)
    except Exception:
        pass

- Linke Toolbar: Intake (Neu / Einfügen / Erkennen / Speichern / Undo)
- Rechte Toolbar: Runner-Liste (Run / Löschen / Rename / Undo + SonderRunner)
"""

from typing import Any

import tkinter as tk
from modules.ui_link_led_button import LinkLedButton
import os
from pathlib import Path

from . import ui_theme_classic, ui_tooltips, ui_leds, logic_tools
from .logic_actions import (
    action_new,
    action_detect,
    action_save,
    action_undo,
    action_run,
    action_guard_futurefix,
    action_guard_futurefix_safe,
    action_r9998,
    action_r9999,
    log_debug,
    action_tree_delete,
    action_tree_rename,
    action_tree_undo,
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
    """Wrappt eine Toolbar-Aktion und aktualisiert danach sicher die Intake-LEDs
    sowie die rechte Liste/Tree."""

    def _inner():
        try:
            func(app)
        finally:
            # LEDs immer versuchen zu aktualisieren
            try:
                ui_leds.evaluate(app)
            except Exception as exc:
                # LED-Updates duerfen die UI niemals crashen, aber Fehler werden geloggt.
                try:
                    log_debug(f"LED evaluate failed in _wrap_with_led: {exc}")
                except Exception:
                    pass
            # R1838: rechte Liste / Tree nach jeder Toolbar-Aktion aktualisieren
            try:
                _r1838_refresh_right_list(app)
            except Exception:
                # Refresh-Fehler duerfen die UI ebenfalls nicht crashen
                pass

    return _inner


# R1853_WRAP_WITH_LED_AND_LOG
# R2798_CLICK_TRACE

def _wrap_with_led_and_log(app, func):
    """Wie _wrap_with_led, öffnet danach zusätzlich das Logfenster."""

    def _inner():
        try:
            logic_actions._r2798_trace_event('CLICK_WRAPPER', getattr(func, '__name__', str(func)))
        except Exception:
            pass
        try:
            func(app)
        finally:
            # LEDs immer versuchen zu aktualisieren
            try:
                ui_leds.evaluate(app)
            except Exception as exc:
                try:
                    log_debug(f"LED evaluate failed in _wrap_with_led_and_log: {exc}")
                except Exception:
                    pass
            # R1838: rechte Liste / Tree nach jeder Toolbar-Aktion aktualisieren
            try:
                _r1838_refresh_right_list(app)
            except Exception:
                pass
            # Danach Logfenster öffnen (zentraler Popup)
            try:
                _action_show_log(app)
            except Exception as exc:
                try:
                    log_debug(f"Log popup failed in _wrap_with_led_and_log: {exc}")
                except Exception:
                    pass

    return _inner




# R2785_WRAP_WITH_LED_AND_REPORT_POPUP
def _wrap_with_led_and_report_popup(app, func, runner_id: str, title: str, text: str = ""):
    try:
        logic_actions._r2798_trace_event('ABOUT_TO_POPUP', str(runner_id) if 'runner_id' in locals() else '')
    except Exception:
        pass

    def _inner():
        try:
            logic_actions._r2798_trace_event('CLICK_WRAPPER', getattr(func, '__name__', str(func)))
        except Exception:
            pass
        try:
            func(app)
        finally:
            # LEDs immer versuchen zu aktualisieren
            try:
                ui_leds.evaluate(app)
            except Exception:
                pass

            # rechte Liste / Tree nach jeder Toolbar-Aktion aktualisieren
            try:
                _r1838_refresh_right_list(app)
            except Exception:
                pass

            # Altes Report-Popup (bewährter Standard)
            try:
                pass  # R2809: inserted to fix empty try
            except Exception as exc:
                try:
                    log_debug(f"Report popup failed in _wrap_with_led_and_report_popup: {exc}")
                except Exception:
                    pass

    return _inner
def _r1838_refresh_right_list(app):
    """
    R1838: Zentraler Refresh-Helfer fuer rechte Liste / Tree.

    Versucht nacheinander:
    - ui_filters.refresh(app)
    - right_list.refresh() (Proxy)
    """
    # 1) Bevorzugt neue Refresh-Logik ueber ui_filters
    try:
        from modules import ui_filters

        ui_filters.refresh(app)
        return
    except Exception:
        pass
    # 2) Fallback: RightListProxy oder aehnliche Wrapper
    try:
        proxy = getattr(app, "right_list", None)
        if proxy is not None and hasattr(proxy, "refresh"):
            proxy.refresh()
    except Exception:
        pass


def _action_toggle_aot(app):
    """Schaltet das Hauptfenster auf Always-on-Top um und aktualisiert AOT-LED/Button."""
    try:
        cur = bool(app.attributes("-topmost"))
    except Exception:
        cur = False
    try:
        app.attributes("-topmost", not cur)
    except Exception:
        return
    # AOT-Status in Button + LEDBar spiegeln
    try:
        updater = getattr(app, "_update_aot_button", None)
        if callable(updater):
            updater()
    except Exception:
        pass


def _action_restart(app):
    # R2364_RESTART_PERSIST: persist docking/tab state BEFORE quitting
    try:
        dm = getattr(app, "_dock_manager", None)
        if dm is not None:
            try:
                dm.persist_all()
            except Exception:
                pass
    except Exception:
        pass
    """Restart von ShrimpDev - best effort über main_gui.py im Projekt-Root."""
    try:
        # modules/ui_toolbar.py -> Projekt-Root = eine Ebene nach oben
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        main_py = os.path.join(root_dir, "main_gui.py")
        if os.path.isfile(main_py):
            os.startfile(main_py)
        try:
            app.quit()
        except Exception:
            pass
    except Exception:
        # Restart darf die UI nicht crashen
        pass


def _action_show_log(app):
    """Zeigt die Logdatei debug_output.txt in einem Popup mit INI-Persistenz.

    Phase 1.1:
    - Fokus auf den letzten Runner-Block (Heuristik über [Rxxxx]-Block).
    - Fallback: letzte 200 Zeilen.
    - Button "Ältere laden" lädt den Rest des Logs nach.
    - Untere Leiste zentriert:
      "Ältere laden", "Inhalt kopieren", "Kopieren & schließen", "Schließen".
    """

    import configparser

    try:
        # Projekt-Root bestimmen (eine Ebene ueber modules)
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        ini_path = os.path.join(root_dir, "ShrimpDev.ini")
        log_path = os.path.join(root_dir, "debug_output.txt")

        # Loginhalt laden
        try:
            with open(log_path, encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            content = "Logdatei debug_output.txt wurde nicht gefunden."
        except Exception as exc:
            content = f"Fehler beim Lesen von debug_output.txt: {exc}"

        lines = content.splitlines()
        tail_lines = lines
        older_lines = []

        def _split_last_block(all_lines):
            """Teilt das Log in (older_lines, tail_lines) für den letzten Runner-Block.

            Heuristik:
            - Von unten nach oben nach einer Zeile suchen, die wie ein Runner-Header aussieht,
              z. B. "[R1234] 2025-12-03 12:34:56 ..." oder einfach "[R1234] ...".
            - Falls nichts gefunden wird, wird auf die letzten 200 Zeilen zurückgegriffen.
            """
            if not all_lines:
                return [], []
            start_idx = None
            for idx in range(len(all_lines) - 1, -1, -1):
                line = all_lines[idx].lstrip()
                if line.startswith("[R") and "]" in line.split(" ", 1)[0]:
                    start_idx = idx
                    break
            if start_idx is None:
                limit = 200
                if len(all_lines) <= limit:
                    return [], all_lines
                return all_lines[:-limit], all_lines[-limit:]
            return all_lines[:start_idx], all_lines[start_idx:]

        if lines:
            older_lines, tail_lines = _split_last_block(lines)

        tail_text = "\n".join(tail_lines)
        older_text = "\n".join(older_lines)

        # Popup-Fenster bauen
        win = tk.Toplevel(app)
        win.title("ShrimpDev Log (letzter Runner)")
        try:
            win.transient(app)
        except Exception:
            pass

        # Geometrie aus INI laden (falls vorhanden)
        geom = None
        try:
            cfg = configparser.ConfigParser()
            if os.path.isfile(ini_path):
                cfg.read(ini_path, encoding="utf-8")
            if cfg.has_section("LogWindow") and cfg.has_option("LogWindow", "geometry"):
                geom = cfg.get("LogWindow", "geometry")
        except Exception:
            geom = None

        if geom:
            try:
                win.geometry(geom)
            except Exception:
                pass
        else:
            # Standardgröße (mittlere Größe) + Zentrierung
            try:
                win.geometry("700x450")
            except Exception:
                pass
            try:
                app.update_idletasks()
                win.update_idletasks()
                x = app.winfo_rootx() + (app.winfo_width() // 2) - (win.winfo_reqwidth() // 2)
                y = app.winfo_rooty() + (app.winfo_height() // 2) - (win.winfo_reqheight() // 2)
                win.geometry(f"+{max(x, 0)}+{max(y, 0)}")
            except Exception:
                # Fallback: Standard-Placement
                pass

        # Layout fuer Inhalt
        win.rowconfigure(1, weight=1)
        win.columnconfigure(0, weight=1)

        # Oberer Bereich nur mit Info-Label
        top_frame = tk.Frame(win)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=4, pady=(4, 0))
        top_frame.columnconfigure(0, weight=1)

        info_label = tk.Label(top_frame, text="Letzter Runner-Block aus debug_output.txt")
        info_label.grid(row=0, column=0, sticky="w")

        state = {"older_loaded": False}

        # Text + Scrollbar
        txt = tk.Text(win, wrap="none")
        scroll = tk.Scrollbar(win, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=scroll.set)

        txt.grid(row=1, column=0, sticky="nsew")
        scroll.grid(row=1, column=1, sticky="ns")

        try:
            txt.insert("1.0", tail_text)
            txt.see("end")
        except Exception:
            pass

        # Untere Button-Leiste (zentriert)
        bottom_frame = tk.Frame(win)
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=4, pady=(4, 6))

        # 0 und 5 tragen die Flexbreite, 1–4 Buttons = zentrierte Gruppe
        for col in range(6):
            weight = 1 if col in (0, 5) else 0
            bottom_frame.columnconfigure(col, weight=weight)

        def _load_older():
            if state["older_loaded"]:
                return
            if not older_text:
                return
            try:
                txt.configure(state="normal")
                current = txt.get("1.0", "end-1c")
                txt.delete("1.0", "end")
                if current:
                    txt.insert("1.0", older_text + "\n" + current)
                else:
                    txt.insert("1.0", older_text)
                txt.see("end")
                state["older_loaded"] = True
                try:
                    btn_older.configure(state="disabled")
                except Exception:
                    pass
            except Exception:
                pass

        def _copy_content():
            try:
                data = txt.get("1.0", "end-1c")
                win.clipboard_clear()
                if data:
                    win.clipboard_append(data)
            except Exception:
                pass

        def _close():
            """Fenster schließen und aktuelle Geometrie in INI speichern."""
            try:
                x = win.winfo_x()
                y = win.winfo_y()
                w = win.winfo_width()
                h = win.winfo_height()
                geom_value = f"{w}x{h}+{x}+{y}"

                cfg = configparser.ConfigParser()
                if os.path.isfile(ini_path):
                    cfg.read(ini_path, encoding="utf-8")
                if not cfg.has_section("LogWindow"):
                    cfg.add_section("LogWindow")
                cfg.set("LogWindow", "geometry", geom_value)

                # R2403: SingleWriter – do not write ShrimpDev.ini directly here
                try:
                    from modules import config_manager as _cfgm  # type: ignore

                    _cfgm.set_value("geometry", str(geom), section="LogWindow", auto_save=False)
                    _cfgm.get_manager().save()
                except Exception:
                    # best-effort, never crash UI
                    pass
            except Exception:
                pass
            win.destroy()

        def _copy_and_close():
            _copy_content()
            _close()

        # Buttons zentriert in Spalten 1–4
        btn_older = tk.Button(bottom_frame, text="Ältere laden", command=_load_older)
        btn_older.grid(row=0, column=1, padx=(0, 4), pady=0)

        btn_copy = tk.Button(bottom_frame, text="Inhalt kopieren", command=_copy_content)
        btn_copy.grid(row=0, column=2, padx=4, pady=0)

        btn_copy_close = tk.Button(
            bottom_frame, text="Kopieren & schließen", command=_copy_and_close
        )
        btn_copy_close.grid(row=0, column=3, padx=4, pady=0)

        btn_close = tk.Button(bottom_frame, text="Schließen", command=_close)
        btn_close.grid(row=0, column=4, padx=(4, 0), pady=0)

        win.protocol("WM_DELETE_WINDOW", _close)
        win.focus_set()
    except Exception:
        # Log-Ansicht darf ShrimpDev niemals crashen
        pass


def _load_log_geometry(app):
    """Lädt Log-Popup-Geometrie aus ShrimpDev.ini."""
    try:
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        ini_path = os.path.join(root, "ShrimpDev.ini")
        cfg = configparser.ConfigParser()
        cfg.read(ini_path, encoding="utf-8")

        if "LogWindow" in cfg and "geometry" in cfg["LogWindow"]:
            return cfg["LogWindow"]["geometry"]
    except Exception:
        pass
    return None


def _save_log_geometry(app, win):
    """Speichert Geometrie des Logfensters in ShrimpDev.ini."""
    try:
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        ini_path = os.path.join(root, "ShrimpDev.ini")

        x = win.winfo_x()
        y = win.winfo_y()
        w = win.winfo_width()
        h = win.winfo_height()

        geom = f"{w}x{h}+{x}+{y}"

        cfg = configparser.ConfigParser()
        cfg.read(ini_path, encoding="utf-8")

        if "LogWindow" not in cfg:
            cfg.add_section("LogWindow")
        cfg["LogWindow"]["geometry"] = geom

        # R2403: SingleWriter – do not write ShrimpDev.ini directly here
        try:
            from modules import config_manager as _cfgm  # type: ignore

            _cfgm.set_value("geometry", str(geom), section="LogWindow", auto_save=False)
            _cfgm.get_manager().save()
        except Exception:
            # best-effort, never crash UI
            pass
    except Exception:
        pass


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


def _action_run_with_popup(app):
    """
    Führt den markierten Runner über ein Popup aus.

    Verhalten:
    - Holt den Pfad der markierten Datei aus der rechten Liste (ui_project_tree.get_selected_path).
    - Wenn es sich um eine .cmd/.bat-Datei handelt, wird module_runner_popup.run_runner_with_popup
      verwendet (zentraler Dialog, kein blinkendes CMD-Fenster).
    - In allen anderen Fällen oder bei Fehlern fällt die Funktion auf action_run(app) zurück.
    """
    # Pfad der markierten Datei aus der rechten Liste ermitteln
    path = None
    try:
        from . import ui_project_tree

        try:
            path = ui_project_tree.get_selected_path(app)
        except Exception:
            path = None
    except Exception:
        path = None

    # Kein Eintrag markiert -> Fallback auf bisheriges Verhalten
    if not path:
        try:
            action_run(app)
        except Exception:
            pass
        return

    import os as _os

    _, ext = _os.path.splitext(path)

    # Nur für klassische Runner-Skripte .cmd/.bat das Popup verwenden
    if ext.lower() not in (".cmd", ".bat"):
        try:
            action_run(app)
        except Exception:
            pass
        return

    # Popup-Runner versuchen; bei Problemen auf action_run zurückfallen
    try:
        try:
            from . import module_runner_popup
        except Exception:
            module_runner_popup = None

        if module_runner_popup is not None:
            module_runner_popup.run_runner_with_popup(app, path)
        else:
            action_run(app)
    except Exception:
        try:
            action_run(app)
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

    # Zusatz-Buttons: Always-on-Top + Restart
    btn_aot = _make_button(
        bar,
        "AOT",
        _wrap_with_led(app, _action_toggle_aot),
        "Fenster Always-on-Top umschalten.",
    )
    try:
        app._btn_aot = btn_aot
    except Exception:
        pass

    btn_restart = _make_button(
        bar,
        "Restart",
        lambda: _action_restart(app),
        "ShrimpDev neu starten.",
    )
    try:
        app._btn_restart = btn_restart
    except Exception:
        pass

    return bar


def build_toolbar_right(parent: tk.Widget, app: Any) -> tk.Frame:
    """
    Rechte Toolbar (Runner-Liste):

    Oben rechts (P&P):
      - Push (wired auf action_autopush_both)
      - Purge (Option B: R2218 Scan -> parse Report -> R2224 Apply nur bei Treffern)

    Darunter: klassische Runner-Controls + SR Buttons (bestehender Block).
    """
    outer = ui_theme_classic.Frame(parent)

    # --- P&P Header (top-right) ---
    header_right = ui_theme_classic.Frame(outer)
    header_right.pack(side="top", anchor="ne", padx=(0, 2), pady=(0, 0))

    row_block = ui_theme_classic.Frame(header_right)
    row_block.pack(side="top", anchor="ne", padx=(0, 2), pady=(0, 2))

    def _root_dir() -> Path:
        return Path(__file__).resolve().parent.parent

    def _abs(rel: str) -> Path:
        return _root_dir() / rel.replace("/", os.sep)

    def _file_exists(rel: str) -> bool:
        try:
            return _abs(rel).exists()
        except Exception:
            return False

    def _runner_busy() -> bool:
        """Best-effort Busy-Check: block P&P clicks while a runner is running."""
        for attr in ("_runner_busy", "runner_busy", "_is_runner_running", "_runner_running"):
            try:
                v = getattr(app, attr, None)
                if isinstance(v, bool):
                    return v
                if callable(v):
                    return bool(v())
            except Exception:
                pass
        return False

    def _resolve_repo_path(kind: str) -> str:
        """Resolve repo roots without hardcoding absolute paths.

        Rules (best-effort):
        - private: project root (…/ShrimpDev_REPO)
        - public: sibling folder "ShrimpDev_PUBLIC_EXPORT" if exists
        - optional override via registry/<kind>_repo_root.txt (one-line path)
        """
        try:
            reg = _root_dir() / "registry" / f"{kind}_repo_root.txt"
            if reg.exists():
                p = reg.read_text(encoding="utf-8", errors="replace").strip().strip('"')
                if p and os.path.isdir(p) and os.path.isdir(os.path.join(p, ".git")):
                    return p
        except Exception:
            pass
        try:
            priv = str(_root_dir())
            if kind == "private":
                return priv if os.path.isdir(os.path.join(priv, ".git")) else ""
            sib = str(_root_dir().parent / "ShrimpDev_PUBLIC_EXPORT")
            return sib if os.path.isdir(os.path.join(sib, ".git")) else ""
        except Exception:
            return ""

    def _is_repo_pushable(repo_path: str) -> bool:
        """True if repo has local changes or is ahead of upstream (best-effort)."""
        import subprocess
        if not repo_path or not os.path.isdir(repo_path):
            return False
        try:
            cp = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_path, text=True, capture_output=True,
            )
            if (cp.stdout or "").strip():
                return True
        except Exception:
            return False
        try:
            cp2 = subprocess.run(
                ["git", "status", "-sb"],
                cwd=repo_path, text=True, capture_output=True,
            )
            sb = (cp2.stdout or "")
            return "ahead " in sb
        except Exception:
            return False

    def _safe_call(name: str) -> None:
        try:
            _call_logic_action(app, name)
        except Exception:
            pass

    def _show_report_best_effort(runner_id: str) -> None:
        """Central report popup (preferred)."""
        try:
            from . import logic_actions as _la
            fn = getattr(_la, "_r1851_show_popup", None)
            if callable(fn):
                fn(app, runner_id=runner_id)
        except Exception:
            pass

    def _action_push_one() -> None:
        _safe_call("action_autopush_both")

    def _action_purge_one() -> None:
        """Option B: run scan, parse hits, run apply only if hits>0; show ONE report popup at end."""
        try:
            log_debug("[Purge] Clicked (Option B)")
        except Exception:
            pass

        def _run_popup(rel_cmd: str) -> bool:
            p = _abs(rel_cmd)
            try:
                if not p.is_file():
                    return False
            except Exception:
                return False
            try:
                from . import module_runner_popup
                module_runner_popup.run_runner_with_popup(app, str(p))
                return True
            except Exception as exc:
                try:
                    log_debug(f"[Purge] popup run failed for {rel_cmd}: {exc}")
                except Exception:
                    pass
                return False

        def _latest_report(prefix: str) -> str | None:
            try:
                rdir = _abs("Reports")
                if not rdir.is_dir():
                    return None
                cands = [p for p in rdir.iterdir() if p.is_file() and p.name.startswith(prefix) and p.suffix.lower()==".md"]
                if not cands:
                    return None
                cands.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                return str(cands[0])
            except Exception:
                return None

        def _parse_hits(report_path: str) -> int | None:
            try:
                txt = Path(report_path).read_text(encoding="utf-8", errors="replace").lower()
            except Exception:
                return None
            zero_phrases = [
                "candidates: 0", "candidate: 0", "found: 0", "files: 0", "0 files",
                "nothing to purge", "no files to purge", "keine", "nichts zu",
            ]
            for z in zero_phrases:
                if z in txt:
                    return 0
            keys = ["candidates", "candidate", "found", "files", "items", "matches"]
            for line in txt.splitlines():
                for k in keys:
                    if k in line:
                        digits = "".join(ch if ch.isdigit() else " " for ch in line).split()
                        for d in digits:
                            try:
                                return int(d)
                            except Exception:
                                pass
            if "purge" in txt:
                digits = "".join(ch if ch.isdigit() else " " for ch in txt).split()
                for d in digits:
                    try:
                        n = int(d)
                        if n > 0:
                            return n
                    except Exception:
                        pass
            return None

        ran_apply = False
        try:
            ran_scan = _run_popup("tools/R2218.cmd")
            if not ran_scan:
                try:
                    log_debug("[Purge] R2218.cmd not found / could not start")
                except Exception:
                    pass
                return

            rp = _latest_report("Report_R2218_")
            hits = _parse_hits(rp) if rp else None
            if hits is None:
                try:
                    log_debug("[Purge] Scan report ambiguous -> SKIP apply (Option B)")
                except Exception:
                    pass
                return
            if hits <= 0:
                try:
                    log_debug("[Purge] Scan hits=0 -> SKIP apply (Option B)")
                except Exception:
                    pass
                return

            ran_apply = _run_popup("tools/R2224.cmd")
            if not ran_apply:
                try:
                    log_debug("[Purge] R2224.cmd not found / could not start (optional)")
                except Exception:
                    pass
        finally:
            try:
                ui_leds.evaluate(app)
            except Exception:
                pass
            try:
                _r1838_refresh_right_list(app)
            except Exception:
                pass
            try:
                _show_report_best_effort("R2224" if ran_apply else "R2218")
            except Exception:
                pass

    # Buttons (top-right)
    btn_push = ui_theme_classic.Button(row_block, text="Push", command=_action_push_one)
    btn_push.pack(side="top", anchor="e", pady=(0, 4))

    btn_purge = ui_theme_classic.Button(row_block, text="Purge", command=_action_purge_one)
    btn_purge.pack(side="top", anchor="e", pady=(0, 0))

    def _set_btn_state_local(btn, enabled: bool) -> None:
        try:
            btn.configure(state=("normal" if enabled else "disabled"))
        except Exception:
            try:
                btn["state"] = "normal" if enabled else "disabled"
            except Exception:
                pass

    def _update_states_min() -> None:
        """Enable/disable P&P deterministically; never crashes UI."""
        try:
            busy = _runner_busy()
        except Exception:
            busy = False

        can_push = False
        try:
            priv = _resolve_repo_path("private")
            pub = _resolve_repo_path("public")
            has_both_wrap = _file_exists("tools/R2693.cmd") or _file_exists("tools/R2693.py")
            has_priv_wrap = _file_exists("tools/R2691.cmd") or _file_exists("tools/R2691.py")
            has_pub_wrap  = _file_exists("tools/R2692.cmd") or _file_exists("tools/R2692.py")
            if has_both_wrap:
                if priv:
                    can_push = can_push or _is_repo_pushable(priv)
                if pub:
                    can_push = can_push or _is_repo_pushable(pub)
            else:
                if has_priv_wrap and priv:
                    can_push = can_push or _is_repo_pushable(priv)
                if has_pub_wrap and pub:
                    can_push = can_push or _is_repo_pushable(pub)
        except Exception:
            can_push = False

        can_purge = bool(_file_exists("tools/R2218.cmd") or _file_exists("tools/R2218.py"))

        _set_btn_state_local(btn_push, (not busy) and can_push)
        _set_btn_state_local(btn_purge, (not busy) and can_purge)

        try:
            row_block.after(1200, _update_states_min)
        except Exception:
            pass

    try:
        _update_states_min()
    except Exception:
        pass

    # Zeile 1 - Basisaktionen
    row1 = ui_theme_classic.Frame(outer)
    row1.pack(fill="x", pady=(0, 2), anchor="w")

    _make_button(
        row1,
        "Run",
        _wrap_with_led(app, _action_run_with_popup),
        "Markierten Runner bzw. Datei ausführen.",
    )
    _make_button(
        row1,
        "Löschen",
        _wrap_with_led(app, action_tree_delete),
        "Markierte Datei in der rechten Liste löschen.",
    )
    _make_button(
        row1,
        "Rename",
        _wrap_with_led(app, action_tree_rename),
        "Markierte Datei in der rechten Liste umbenennen.",
    )
    _make_button(
        row1,
        "Undo",
        _wrap_with_led(app, action_tree_undo),
        "Letzte Dateiaktion (rechts) rückgängig machen.",
    )

    # Zeile 2 - Service / Diagnose (SR)
    service_frame = ui_theme_classic.Frame(outer)
    service_frame.pack(fill="x", pady=(4, 0))

    lbl_service = tk.Label(
        service_frame,
        text="Service (SR) / Diagnose",
        fg="#666666",
        anchor="w",
    )
    lbl_service.pack(fill="x", padx=2, pady=(0, 2))

    row2 = ui_theme_classic.Frame(service_frame)
    row2.pack(fill="x", pady=(0, 0))

    _make_button(
        row2,
        "FutureFix (SR9997)",
        _wrap_with_led_and_log(app, action_guard_futurefix),
        "SonderRunner R9997: Future-Fix Guard ausführen.",
    )
    _make_button(
        row2,
        "FutureFix Safe (SR1352)",
        _wrap_with_led_and_log(app, action_guard_futurefix_safe),
        "SonderRunner SR1352: Future-Fix Safe ausführen.",
    )
    _make_button(
        row2,
        "Build Tools (SR9998)",
        _wrap_with_led_and_log(app, action_r9998),
        "SonderRunner R9998: Build-/Tools-Runner.",
    )
    _make_button(
        row2,
        "Diagnose (SR9999)",
        _wrap_with_led_and_log(app, action_r9999),
        "SonderRunner R9999: Diagnose-/Analyse-Runner.",
    )
    _make_button(
        row2,
        "Systemcheck (SR1922)",
        _wrap_with_led_and_log(app, logic_tools.tool_masterrules_guard),
        "MasterRulesGuard (R1922): Architektur- und Regel-Check.",
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


# ============================================================
# R2072_AOT_RESTART_START
# AOT- und Restart-Wrapper:
# - _action_toggle_aot nutzt bevorzugt app.toggle_topmost()
#   (inkl. INI-Persistenz via config_loader).
# - _action_restart speichert vor Neustart den UI-State
#   über app._save_ui_state_to_ini(), falls vorhanden.
# ============================================================


def _r2072_safe_call_save_state(app) -> None:
    try:
        if hasattr(app, "_save_ui_state_to_ini"):
            app._save_ui_state_to_ini()
    except Exception:
        pass


def _action_toggle_aot(app):  # type: ignore[override]
    """R2072: bevorzugt app.toggle_topmost(), sonst Fallback auf altes Verhalten."""
    fn = None
    try:
        fn = getattr(app, "toggle_topmost", None)
    except Exception:
        fn = None
    if callable(fn):
        try:
            fn()
            return
        except Exception:
            pass

    # Fallback: ursprüngliche Logik (ohne INI-Speichern)
    try:
        cur = bool(app.attributes("-topmost"))
    except Exception:
        cur = False
    try:
        app.attributes("-topmost", not cur)
    except Exception:
        return
    try:
        updater = getattr(app, "_update_aot_button", None)
        if callable(updater):
            updater()
    except Exception:
        pass


def _action_restart(app):  # type: ignore[override]
    """R2072: Restart mit vorherigem Speichern des UI-States."""
    _r2072_safe_call_save_state(app)
    # R2385: persist docking before restart (best-effort)
    try:
        dm = getattr(app, "_dock_manager", None)
        if dm is not None:
            dm.persist_all()
    except Exception:
        pass

    try:
        import os as _r2072_os

        root_dir = _r2072_os.path.abspath(
            _r2072_os.path.join(_r2072_os.path.dirname(__file__), "..")
        )
        main_py = _r2072_os.path.join(root_dir, "main_gui.py")
        if _r2072_os.path.isfile(main_py):
            _r2072_os.startfile(main_py)
        try:
            app.quit()
        except Exception:
            pass
    except Exception:
        # Restart darf die UI nicht crashen
        pass


# R2072_AOT_RESTART_END
# ============================================================
