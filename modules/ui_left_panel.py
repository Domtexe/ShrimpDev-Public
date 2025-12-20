from __future__ import annotations

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog

from modules import ui_theme_classic, ui_filters, ui_leds


def _ensure_stringvar(app, attr: str) -> tk.StringVar:
    """Stellt sicher, dass app.attr ein StringVar ist und gibt es zurueck."""
    var = getattr(app, attr, None)
    if not isinstance(var, tk.StringVar):
        var = tk.StringVar()
        setattr(app, attr, var)
    return var


def _sync_target_vars(app, value: str) -> None:
    """Synchronisiert den Zielpfad in moegliche Ziel-Variablen des App-Objekts,
    damit rechte Liste und Pfad-Logik konsistent arbeiten.
    var_target_dir wird als Single Source of Truth verwendet und auf
    Legacy-Variablen gespiegelt.
    """
    import tkinter as tk  # lokale Absicherung, falls das Modul anders importiert wurde

    # Canonical StringVar fuer den Zielordner sicherstellen
    var_target = getattr(app, "var_target_dir", None)
    if not isinstance(var_target, tk.StringVar):
        try:
            from tkinter import StringVar  # type: ignore
            var_target = StringVar()
        except Exception:
            var_target = tk.StringVar()
        setattr(app, "var_target_dir", var_target)

    try:
        var_target.set(value)
    except Exception:
        # Darf die restliche Synchronisation nicht verhindern
        pass

    # Legacy-StringVars aktualisieren bzw. mit var_target_dir verknuepfen
    for cand in ("target", "_target", "target_dir_var"):
        try:
            v = getattr(app, cand, None)
            if isinstance(v, tk.StringVar):
                v.set(value)
            elif v is None and var_target is not None:
                # Falls bisher kein StringVar existiert, an var_target_dir koppeln
                setattr(app, cand, var_target)
        except Exception:
            continue

    # Plain-Attribute fuer Altlogik / externe Tools
    for cand in ("target_dir", "dest_dir"):
        try:
            setattr(app, cand, value)
        except Exception:
            continue

def _browse_target(app, var_target) -> None:
    """Oeffnet einen Ordnerdialog und aktualisiert Zielordner, rechte Liste und LEDs."""
    from tkinter import filedialog
    from modules import ui_filters, ui_leds

    current = ""
    if hasattr(var_target, "get"):
        try:
            current = (var_target.get() or "").strip()
        except Exception:
            current = ""
    initial = current if current else "."

    try:
        path = filedialog.askdirectory(initialdir=initial, title="Zielordner waehlen")
    except Exception:
        path = ""

    if not path:
        return

    # Ziel-StringVar aktualisieren
    if hasattr(var_target, "set"):
        try:
            var_target.set(path)
        except Exception:
            pass

    # App-Variablen synchronisieren
    try:
        _sync_target_vars(app, path)
    except Exception:
        # Darf UI nicht crashen
        pass

    # Pfadwechsel-Logik / rechte Liste
    try:
        if hasattr(app, "_path_changed") and callable(getattr(app, "_path_changed")):
            app._path_changed()
        else:
            ui_filters.refresh(app)
    except Exception:
        try:
            ui_filters.refresh(app)
        except Exception:
            pass

    # Intake-LEDs aktualisieren
    try:
        ui_leds.evaluate(app)
    except Exception:
        pass

    # R1647: Gewaehltens Zielverzeichnis in der INI persistieren
    try:
        from modules import config_loader as _cfg_r1647b
        cfg = _cfg_r1647b.load()
        if not cfg.has_section("Intake"):
            cfg.add_section("Intake")
        cfg.set("Intake", "last_target_dir", path)
        _cfg_r1647b.save(cfg)
    except Exception:
        # Persistenz ist nice-to-have, darf aber nie die UI crashen
        pass

def build_left_panel(parent, app) -> tk.Frame:
    """
    Linker Bereich: Intake-Editor + Metadaten.

    Elemente:
    - Zeile fuer Dateiname + Endung (mit Punkt dazwischen)
    - Zeile fuer Zielordner (+ "..." Browse-Button)
    - Zeile fuer Pfad-Vorschau
    - Intake-LED (Platzhalter, wird spaeter von Logik versorgt)
    - ScrolledText fuer Code
    """
    bg = ui_theme_classic.BG_MAIN
    wrap = tk.Frame(parent, bg=bg)

    # StringVars anlegen / wiederverwenden
    var_name = _ensure_stringvar(app, "var_name")
    var_ext = _ensure_stringvar(app, "var_ext")

    # Zielordner-Var: nach Moeglichkeit an bestehende Ziel-Var anbinden
    # (damit System-Logik und neue UI denselben Wert verwenden)
    linked_target: tk.StringVar | None = None
    for cand in ("target", "_target", "target_dir_var"):
        v = getattr(app, cand, None)
        if isinstance(v, tk.StringVar):
            linked_target = v
            break
    if linked_target is None:
        linked_target = _ensure_stringvar(app, "var_target_dir")
    else:
        setattr(app, "var_target_dir", linked_target)
    var_target_dir = linked_target

    # R1647: Standard-Zielordner aus INI laden (falls vorhanden)
    try:
        from modules import config_loader as _cfg_r1647
        cfg = _cfg_r1647.load()
        if cfg.has_section("Intake"):
            last_dir = cfg.get("Intake", "last_target_dir", fallback="").strip()
            if last_dir:
                try:
                    var_target_dir.set(last_dir)
                except Exception:
                    pass
    except Exception:
        # Config-Fehler duerfen den Intake-Aufbau nicht verhindern
        pass

    var_path_preview = _ensure_stringvar(app, "var_path_preview")

    # --- Zeile: Dateiname + Endung ----------------------------------------
    row_name = tk.Frame(wrap, bg=bg)
    row_name.pack(fill="x", padx=4, pady=(4, 2))

    tk.Label(row_name, text="Datei:", bg=bg).pack(side="left", padx=2, pady=2)

    entry_name = ui_theme_classic.Entry(row_name, textvariable=var_name, width=32)
    entry_name.pack(side="left", padx=(4, 2))

    tk.Label(row_name, text=".", bg=bg).pack(side="left", padx=2, pady=2)

    entry_ext = ui_theme_classic.Entry(row_name, textvariable=var_ext, width=8)
    entry_ext.pack(side="left", padx=(2, 4))

    # Referenzen am App-Objekt bereitstellen (Kompatibilitaet fuer logic_actions)
    app.entry_name = entry_name
    app.entry_ext = entry_ext

    # --- Zeile: Zielordner (+ Browse-Button) ------------------------------
    row_target = tk.Frame(wrap, bg=bg)
    row_target.pack(fill="x", padx=4, pady=(0, 2))

    tk.Label(row_target, text="Zielordner:", bg=bg).pack(side="left", padx=2, pady=2)

    entry_target = ui_theme_classic.Entry(row_target, textvariable=var_target_dir, width=40)
    entry_target.pack(side="left", padx=(4, 2), fill="x", expand=True)

    btn_browse = ui_theme_classic.Button(
        row_target,
        text="...",
        width=3,
        command=lambda: _browse_target(app, var_target_dir),
    )
    btn_browse.pack(side="left", padx=(2, 0))

    app.entry_target_dir = entry_target
    app.button_target_browse = btn_browse

    # --- Zeile: Pfad-Vorschau + LED ---------------------------------------
    row_info = tk.Frame(wrap, bg=bg)
    row_info.pack(fill="x", padx=4, pady=(0, 4))

    tk.Label(row_info, text="Pfad:", bg=bg).pack(side="left", padx=2, pady=2)

    lbl_path = tk.Label(row_info, textvariable=var_path_preview, bg=bg, anchor="w")
    lbl_path.pack(side="left", padx=(4, 8), fill="x", expand=True)

    # Intake-LED (Platzhalter: grau = unbekannt)
    led = tk.Canvas(row_info, width=14, height=14, highlightthickness=0, bg=bg)
    led.pack(side="right", padx=(4, 0))
    led_id = led.create_oval(2, 2, 12, 12, fill="#666666", outline="#444444")

    app.intake_led = led
    app.intake_led_id = led_id

    def _update_preview(*_args):
        """Aktualisiert die Pfadvorschau basierend auf Name, Ext und Zielordner."""
        name = (var_name.get() or "").strip()
        ext = (var_ext.get() or "").strip()
        target = (var_target_dir.get() or "").strip()

        if ext and not ext.startswith("."):
            ext_show = "." + ext
        else:
            ext_show = ext

        if not name:
            preview = ""
        else:
            filename = f"{name}{ext_show}"
            if target:
                preview = f"{target}\\{filename}"
            else:
                preview = filename

        var_path_preview.set(preview)

    # Traces fuer automatische Aktualisierung
    def _safe_led_eval():
        """Sichere LED-Aktualisierung fuer den Intake-Tab."""
        try:
            ui_leds.evaluate(app)
        except Exception:
            # LED-Updates duerfen die UI niemals crashen.
            pass

    def _on_target_changed(*_args):
        """Wird aufgerufen, wenn sich Name, Endung oder Zielordner aendert.
        Aktualisiert die Pfadvorschau, synchronisiert die Ziel-
        Variablen der App, laedt die rechte Liste neu und
        aktualisiert die Intake-LEDs.
        R1612: Wenn Endung py/cmd => Zielordner automatisch auf tools setzen.
        """
        # Zielordner bei py/cmd automatisch auf tools-Kontext setzen
        try:
            ext_val = (var_ext.get() or "").strip().lower()
            if ext_val in ("py", "cmd"):
                import os
                root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                tools_dir = os.path.join(root, "tools")
                current = (var_target_dir.get() or "").strip()
                if os.path.isdir(tools_dir) and current != tools_dir:
                    var_target_dir.set(tools_dir)
        except Exception:
            # darf die UI nicht crashen, falls etwas schief geht
            pass
        _update_preview()
        # Zielvariablen der App mit neuem Zielordner synchronisieren
        try:
            _sync_target_vars(app, var_target_dir.get())
        except Exception:
            pass
        # Rechten Bereich (Projektliste) neu laden - entspricht
        # dem "Aktualisieren"-Button im Intake.
        try:
            ui_filters.refresh(app)
        except Exception:
            # UI soll nicht crashen, wenn refresh Probleme macht.
            pass
        # LED-Zustand aktualisieren
        _safe_led_eval()

    var_name.trace_add("write", _on_target_changed)
    var_ext.trace_add("write", _on_target_changed)
    var_target_dir.trace_add("write", _on_target_changed)

    _update_preview()
    _safe_led_eval()
    # --- ScrolledText fuer Code -------------------------------------------
    app.txt_intake = ScrolledText(wrap, undo=True, font=("Consolas", 10))
    def _on_code_change(_event=None):
        _safe_led_eval()

    app.txt_intake.bind("<KeyRelease>", _on_code_change)

    app.txt_intake.pack(fill="both", expand=True, padx=4, pady=(0, 4))

    if not hasattr(app, "intake_text"):
        app.intake_text = app.txt_intake
    if not hasattr(app, "txt_code"):
        app.txt_code = app.txt_intake

    return wrap
