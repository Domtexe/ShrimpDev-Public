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

    Zeile 1: [Run] [Löschen] [Rename] [Undo]
    Zeile 2: [FutureFix] [FutureFix Safe] [Build Tools] [Diagnose]
    """
    # R2866: alias frame_toolbar_right
    _ftr = None
    for _nm in ('frame_toolbar_right','frame','parent','container','master','root'):
        if _nm in locals():
            _ftr = locals().get(_nm)
            if _ftr is not None:
                break
    if _ftr is not None:
        frame_toolbar_right = _ftr
    del _ftr, _nm
    
    # R2836_TRACE_PUSH
    def _r2836_trace(msg: str) -> None:
        try:
            import os
            from datetime import datetime
            _root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
            _fp = os.path.join(_root, 'Reports', 'trace_push_buttons.log')
            os.makedirs(os.path.dirname(_fp), exist_ok=True)
            with open(_fp, 'a', encoding='utf-8', errors='replace') as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
        except Exception:
            pass

    outer = ui_theme_classic.Frame(parent)
    # R2429: Right-top stack for Push/Purge (flush top-right, stacked)
    header_right = ui_theme_classic.Frame(outer)
    header_right.pack(side="top", anchor="ne", padx=(0, 2), pady=(0, 0))
    # R2738_CONSOLIDATED_PUSH_PURGE
    # Top-right block: 2 rows (Push above, Purge below) - consolidated
    row_block = ui_theme_classic.Frame(header_right)
    row_block.pack(side="top", anchor="ne", padx=(0, 2), pady=(0, 2))

    row_push = ui_theme_classic.Frame(row_block)
    row_push.pack(side="top", anchor="ne", pady=(0, 2))

    row_purge = ui_theme_classic.Frame(row_block)
    row_purge.pack(side="top", anchor="ne", pady=(0, 0))

    # Zeile 0 – Purge-Tools (Scan / Apply)
    btn_apply = ui_theme_classic.Button(
        row_purge,
        text="Purge Apply",
        command=_wrap_with_led_and_report_popup(app, getattr(logic_tools, 'action_tools_purge_apply', lambda *a, **k: None), "R2224", "Purge Apply", "Latest runner report"),
    )
    btn_apply.pack(side="right", padx=(6, 0))
    try:
        btn_apply.configure(bg="#f4b6b6", activebackground="#f1a9a9")
    except Exception:
        pass

    btn_scan = ui_theme_classic.Button(
        row_purge,
        text="Purge Scan",
        command=_wrap_with_led_and_report_popup(app, getattr(logic_tools, 'action_tools_purge_scan', lambda *a, **k: None), "R2218", "Purge Scan", "Latest runner report"),
    )
    btn_scan.pack(side="right", padx=(6, 0))
# Toggle (gekoppelt)
    try:
        if not hasattr(app, "_autopush_link_var"):
            app._autopush_link_var = tk.BooleanVar(value=False)
        _link_var = app._autopush_link_var
    except Exception:
        _link_var = None

    
    def _diag_link(msg: str) -> None:
        try:
            from pathlib import Path
            _root = Path(__file__).resolve().parent.parent
            logp = _root / 'Reports' / 'link_diag.log'
            logp.parent.mkdir(parents=True, exist_ok=True)
            line = msg.rstrip('\\n') + '\\n'
            with open(logp, 'a', encoding='utf-8', errors='replace') as f:
                f.write(line)
        except Exception:
            pass
        try:
            print(msg)
        except Exception:
            pass
    def _autopush_linked() -> bool:
        try:
            return bool(_link_var.get()) if _link_var is not None else False
        except Exception:
            return False


    def _autopush_set_linked(val: bool) -> None:
        try:
            if _link_var is not None:
                _link_var.set(bool(val))
        except Exception:
            pass
    # --- Busy flag comes from runner executor (R2427) ---
    def _runner_busy() -> bool:
        try:
            from . import module_runner_exec

            return bool(module_runner_exec.is_runner_busy())
        except Exception:
            return False

    # Resolve private root (where this repo lives)
    _PRIVATE_ROOT = Path(__file__).resolve().parent.parent

    # R2825_REPO_ROOTS
    # Deterministic repo roots (private selectable, public auto-derived)
    # Workspace/cwd heuristics intentionally ignored for repo roots.

    def _r2825_reg_dir() -> Path:
        return _PRIVATE_ROOT / 'registry'

    def _r2825_read_reg_text(name: str) -> str:
        try:
            fp = _r2825_reg_dir() / name
            if fp.exists():
                return fp.read_text(encoding='utf-8', errors='replace').strip().strip('"')
        except Exception:
            pass
        return ''

    def _r2825_write_reg_text(name: str, value: str) -> None:
        try:
            _r2825_reg_dir().mkdir(parents=True, exist_ok=True)
            fp = _r2825_reg_dir() / name
            fp.write_text((value or '').strip() + '\n', encoding='utf-8', errors='replace')
        except Exception:
            pass

    def _r2825_derive_public_from_private(private_root: Path) -> Path:
        try:
            pr = private_root
            if pr.name == 'ShrimpDev_REPO':
                return pr.with_name('ShrimpDev_PUBLIC_EXPORT')
            return pr.parent / 'ShrimpDev_PUBLIC_EXPORT'
        except Exception:
            return _PRIVATE_ROOT.parent / 'ShrimpDev_PUBLIC_EXPORT'

    def _r2825_private_root_cfg() -> Path:
        p = _r2825_read_reg_text('private_repo_root.txt')
        if p:
            try:
                return Path(p)
            except Exception:
                pass
        return _PRIVATE_ROOT

    def _r2825_public_root_cfg(auto_create: bool = True) -> Path | None:
        p = _r2825_read_reg_text('public_export_root.txt')
        if p:
            try:
                return Path(p)
            except Exception:
                pass
        pub = _r2825_derive_public_from_private(_r2825_private_root_cfg())
        if auto_create:
            try:
                pub.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass
        _r2825_write_reg_text('public_export_root.txt', str(pub))
        return pub

    def _r2825_choose_private_root(app) -> None:
        try:
            import tkinter.filedialog as _fd
            start = str(_r2825_private_root_cfg())
            sel = _fd.askdirectory(title='Select Private Repo Root', initialdir=start)
            if sel:
                _r2825_write_reg_text('private_repo_root.txt', sel)
                _r2825_public_root_cfg(auto_create=True)
                try:
                    upd = getattr(app, '_update_push_states', None)
                    if callable(upd):
                        upd()
                except Exception:
                    pass
        except Exception:
            pass

    def _file_exists(rel: str) -> bool:
        return (_PRIVATE_ROOT / rel).exists()

    # Public export root: no hardcode.
    # Priority:
    # 1) registry/public_export_root.txt (one line path)
    # 2) app.public_export_root (if later wired from workspace/config)
    def _public_root() -> Path | None:
        try:
            reg_file = _PRIVATE_ROOT / "registry" / "public_export_root.txt"
            if reg_file.exists():
                p = reg_file.read_text(encoding="utf-8", errors="replace").strip().strip('"')
                if p:
                    return Path(p)
        except Exception:
            pass
        try:
            p = getattr(app, "public_export_root", None)
            if p:
                return Path(str(p))
        except Exception:
            pass
        return None

    def _public_repo_ok() -> bool:
        pr = _public_root()
        return bool(pr and pr.exists() and (pr / ".git").exists())

    # SAFE scope: must be clean before Public is allowed
    _SAFE_PREFIXES = ["docs/PIPELINE.md"]

    def _purge_plan_ok() -> bool:
        """Tools-Purge Apply nur wenn ein aktueller Plan existiert."""
        try:
            # Plan wird durch action_tools_purge_scan erzeugt
            rp = Path(getattr(app, "project_root", "")) / "docs" / "Tools_Purge_Flat_Plan.md"
            if not rp.exists():
                # fallback (wenn app.project_root nicht gesetzt)
                rp = Path(__file__).resolve().parent.parent / "docs" / "Tools_Purge_Flat_Plan.md"
            return rp.exists() and rp.stat().st_size > 20
        except Exception:
            return False

    def _private_safe_dirty() -> bool:
        import subprocess

        try:
            cp = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=str(_PRIVATE_ROOT),
                text=True,
                capture_output=True,
            )
            out = (cp.stdout or "").strip()
            if not out:
                return False
            for line in out.splitlines():
                if len(line) < 4:
                    continue
                path = line[3:].strip().replace("\\", "/")
                for pre in _SAFE_PREFIXES:
                    if path == pre or path.startswith(pre.rstrip("/") + "/"):
                        return True
            return False
        except Exception:
            # safe default: assume dirty -> blocks public
            return True

    # Buttons (right aligned): Private | Link | Public (Public far right)
    btn_push_public = ui_theme_classic.Button(
        row_push,
        text="Push Public",
        command=lambda: _call_logic_action(app, "action_autopush_both")
        if _autopush_linked()
        else _call_logic_action(app, "action_autopush_public"),
    )
    btn_push_private = ui_theme_classic.Button(
        row_push,
        text="Push Private",
        command=lambda: _call_logic_action(app, "action_autopush_both")
        if _autopush_linked()
        else _call_logic_action(app, "action_autopush_private"),
    )
    # : Link is a real themed Button with LED-box icon inside
    # R2747: Link as LinkLedButton (icon+text+LED in one control)
    app._btn_link = LinkLedButton(
        row_push,
        text="Link",
        command=lambda: _toggle_link_clicked(),
        width=58,
        height=22,
    led_size=8,
    padding_x=6,
    )
    app._btn_link.set_enabled(True)
    # Top row order required: Push Private | Link | Push Public
    # pack(side='right') -> insert in reverse to render left-to-right
    btn_push_public.pack(side='right', padx=(6, 0))
    app._btn_link.pack(side='right', padx=(6, 0))
    btn_push_private.pack(side='right', padx=(6, 0))

    # R2863: Public export sync button (runs R2862)
    row_export = ui_theme_classic.Frame(frame_toolbar_right)
    row_export.pack(fill="x", pady=(4, 0))
    btn_export_public = ui_theme_classic.Button(
        row_export,
        text="Export Public",
        command=lambda: _call_logic_action(app, "action_public_export_sync"),
    )
    try:
        ui_tooltip.register(btn_export_public, "Sync Private -> Public export (R2862) and push public if configured.")
    except Exception:
        pass
    btn_export_public.pack(side='right', padx=(6, 0))

    # R2825: Private repo picker ('…')
    try:
        btn_repo_pick = ui_theme_classic.Button(row_push, text='…', command=lambda: _r2825_choose_private_root(app))
        btn_repo_pick.pack(side='right', padx=(6, 0))
    except Exception:
        pass
    # Pack order (side=right): Public (right) | Link (middle) | Private (left)
    # Link visuals handled by LinkLedButton.set_state() (no images)
    try:
        app._btn_link.set_state('on' if _autopush_linked() else 'off')
    except Exception:
        pass

    def _set_btn_state(btn, enabled: bool, busy: bool | None = None):
        _r2836_trace(f"set_btn_state enabled={enabled}" + (f" busy={busy}" if busy is not None else ""))
        try:
            btn.configure(state=("normal" if enabled else "disabled"))
        except Exception:
            try:
                btn["state"] = "normal" if enabled else "disabled"
            except Exception:
                pass
    def _is_repo_pushable(repo_path: str) -> bool:
        """Return True iff repo_path is a git repo that is dirty OR ahead."""
        try:
            import os
            import subprocess
            if not repo_path or not os.path.isdir(repo_path):
                return False
            if not os.path.isdir(os.path.join(repo_path, ".git")):
                return False
    
            # Dirty check
            r = subprocess.run(
                ["git", "-C", repo_path, "status", "--porcelain"],
                capture_output=True,
                text=True,
            )
            if (r.stdout or "").strip():
                return True
    
            # Ahead check (best-effort)
            r = subprocess.run(
                ["git", "-C", repo_path, "status", "-sb"],
                capture_output=True,
                text=True,
            )
            return "ahead" in ((r.stdout or "").lower())
        except Exception:
            return False
    
    def _resolve_repo_path(kind: str) -> str:
        # R2835_REGISTRY_FIRST
        # Registry is source of truth. Workspace/cwd removed.
        try:
            import os
            here_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
            reg_dir = os.path.join(here_root, 'registry')
            if kind == 'private':
                reg_fp = os.path.join(reg_dir, 'private_repo_root.txt')
            else:
                reg_fp = os.path.join(reg_dir, 'public_export_root.txt')

            def _clean(p: str) -> str:
                try:
                    return (p or '').strip().strip('"')
                except Exception:
                    return ''

            def _ok(p: str) -> str:
                try:
                    if not p:
                        return ''
                    p = _clean(p)
                    if os.path.isdir(p) and os.path.isdir(os.path.join(p, '.git')):
                        return p
                except Exception:
                    pass
                return ''

            # 1) Registry
            if os.path.isfile(reg_fp):
                try:
                    with open(reg_fp, 'r', encoding='utf-8', errors='replace') as f:
                        p = f.read()
                    ok = _ok(p)
                    if ok:
                        return ok
                except Exception:
                    pass

            # 2) Deterministic fallback (no workspace)
            if kind == 'private':
                return _ok(here_root)
            else:
                parent = os.path.dirname(here_root)
                return _ok(os.path.join(parent, 'ShrimpDev_PUBLIC_EXPORT'))
        except Exception:
            return ''

    
    # Link button with LED (no checkbox)
    def _link_led_update():
        """Update Link LED from single source of truth."""
        try:
            app._app._btn_link.set_state('on' if _autopush_linked() else 'off')
        except Exception:
            pass


    def _toggle_link_clicked():


        """Toggle link state; LED reflects _link_var via _autopush_linked()."""


        try:


            on = bool(_autopush_linked())


        except Exception:


            on = False


        try:


            _autopush_set_linked(not on)


        except Exception:


            pass


        _link_led_update()


        try:


            _update_push_states()


        except Exception:


            pass



    def _update_push_states():
        _r2836_trace('update_push_states enter')
        busy = _runner_busy()

        # Repo-only autopush runners (OneDrive)
        has_private = _file_exists("tools/R2691.cmd") or _file_exists("tools/R2691.py")
        has_public  = _file_exists("tools/R2692.cmd") or _file_exists("tools/R2692.py")
        has_both    = _file_exists("tools/R2693.cmd") or _file_exists("tools/R2693.py")

        # Resolve repo roots (best-effort)
        private_root = _resolve_repo_path("private")
        _r2836_trace(f"private_root={private_root}")
        public_root  = _resolve_repo_path("public")
        _r2836_trace(f"public_root={public_root}")

        # Pushable means: repo exists AND (dirty OR branch ahead)
        private_pushable = bool(has_private and private_root and (Path(private_root) / '.git').exists())
        public_pushable = bool(has_public  and public_root  and (Path(public_root)  / '.git').exists())

        # R2837_WRAPPER_GATING
        try:
            _tools = Path(__file__).resolve().parent.parent / 'tools'
            _has_priv_wrap = (_tools / 'R2691.cmd').exists()
            _has_pub_wrap  = (_tools / 'R2692.cmd').exists()
            private_pushable = bool(private_pushable and _has_priv_wrap)
            public_pushable  = bool(public_pushable  and _has_pub_wrap)
        except Exception:
            pass
        # Deterministic UI gating
        _set_btn_state(btn_push_private, (not busy) and private_pushable, busy=busy)
        _set_btn_state(btn_push_public, (not busy) and public_pushable, busy=busy)

        # Auto-Link: only auto-enable when it makes sense; never auto-disable
        if private_pushable and _public_repo_ok():
            try:
                if not _autopush_linked():
                    _autopush_link_var.set(True)
            except Exception:
                pass

    def _update_purge_states():
        try:
            busy = _runner_busy()
        except Exception:
            busy = False

        has_scan = _file_exists("tools/R2218.cmd")
        has_apply = _file_exists("tools/R2224.cmd")

        scan_ok = bool(has_scan) and (not busy)
        plan_ok = _file_exists("docs/Tools_Purge_Flat_Plan.md")  # R2475: ensure defined
        apply_ok = bool(has_apply) and bool(plan_ok) and (not busy)

        try:
            try:
                _set_btn_state(btn_scan, scan_ok)
            except NameError:
                # optional button handle not present in this toolbar variant
                pass
        except NameError:
            # btn_scan not present in this toolbar variant; do not crash startup
            pass
        try:
            _set_btn_state(btn_apply, apply_ok)
        except NameError:
            # optional button handle not present in this toolbar variant
            pass
        try:
            row_purge.after(1200, _update_purge_states)
        except Exception:
            pass

    _update_purge_states()

    # --- Push/Link state must be live (start + periodic tick) ---
    try:
        _update_push_states()
    except Exception:
        pass
    try:
        # keep buttons & link LED deterministic
        row_push.after(1200, _update_push_states)
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
