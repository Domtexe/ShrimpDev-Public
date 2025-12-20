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
from tkinter import messagebox
import os

from . import ui_theme_classic, ui_tooltips, ui_leds, logic_tools
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
def _wrap_with_led_and_log(app, func):
    """Wie _wrap_with_led, öffnet danach zusätzlich das Logfenster."""
    def _inner():
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
            with open(log_path, "r", encoding="utf-8") as f:
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
                    _cfgm.set_value('geometry', str(geom), section='LogWindow', auto_save=False)
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

        btn_copy_close = tk.Button(bottom_frame, text="Kopieren & schließen", command=_copy_and_close)
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
            _cfgm.set_value('geometry', str(geom), section='LogWindow', auto_save=False)
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
    outer = ui_theme_classic.Frame(parent)

    # Zeile 0 - Tools Purge (ROOT-only, keine Subfolder)
    row0 = ui_theme_classic.Frame(outer)
    row0.pack(fill="x", pady=(0, 2))
    # rechts oben ausrichten
    btn_apply = ui_theme_classic.Button(
        row0,
        text="Tools Purge Apply",
        command=lambda: _call_logic_action(app, "action_tools_purge_apply"),
    )
    try:
        btn_apply.configure(bg="#f2b6b6", activebackground="#eaa0a0")
    except Exception:
        pass
    btn_apply.pack(side="right", padx=6, pady=0)
    try:
        ui_tooltips.add(btn_apply, "Archiviert Dateien im tools\\-ROOT nach tools\\Archiv (nur laut Plan). Mit Sicherheitsabfrage.")
    except Exception:
        pass

    btn_scan = ui_theme_classic.Button(
        row0,
        text="Tools Purge Scan",
        command=lambda: _call_logic_action(app, "action_tools_purge_scan"),
    )
    btn_scan.pack(side="right", padx=6, pady=0)
    try:
        ui_tooltips.add(btn_scan, "Erstellt Purge-Plan fuer Dateien im tools\\-ROOT (keine Subfolder).")
    except Exception:
        pass

    # Zeile 1 - Basisaktionen
    row1 = ui_theme_classic.Frame(outer)
    row1.pack(fill="x", pady=(0, 2))

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
        if hasattr(app, '_save_ui_state_to_ini'):
            app._save_ui_state_to_ini()
    except Exception:
        pass


def _action_toggle_aot(app):  # type: ignore[override]
    """R2072: bevorzugt app.toggle_topmost(), sonst Fallback auf altes Verhalten."""
    fn = None
    try:
        fn = getattr(app, 'toggle_topmost', None)
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
        cur = bool(app.attributes('-topmost'))
    except Exception:
        cur = False
    try:
        app.attributes('-topmost', not cur)
    except Exception:
        return
    try:
        updater = getattr(app, '_update_aot_button', None)
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
        root_dir = _r2072_os.path.abspath(_r2072_os.path.join(_r2072_os.path.dirname(__file__), '..'))
        main_py = _r2072_os.path.join(root_dir, 'main_gui.py')
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
