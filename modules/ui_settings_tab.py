"""
modules/ui_settings_tab.py – Settings-Tab für ShrimpDev

Inhalte:
- workspace_root anzeigen/ändern
- quiet_mode (Checkbox) anzeigen/ändern
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from modules import config_manager


def build_settings_tab(parent: tk.Widget) -> ttk.Frame:
    """
    Erzeugt den Settings-Tab-Inhalt und hängt ihn an parent an.

    Args:
        parent: Container (z. B. eine ttk.Frame-Instanz im Notebook)

    Returns:
        Der Haupt-Frame des Settings-Tabs.
    """
    mgr = config_manager.get_manager()
    mgr.ensure_loaded()

    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Aktuelle Werte
    current_root = config_manager.get_workspace_root()
    current_quiet = config_manager.get_quiet_mode()

    # Row 0: workspace_root Label + Entry + Button
    lbl_root = ttk.Label(frame, text="Workspace-Root:")
    lbl_root.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(0, 5))

    var_root = tk.StringVar(value=str(current_root))
    entry_root = ttk.Entry(frame, textvariable=var_root, width=60)
    entry_root.grid(row=0, column=1, sticky="we", padx=(0, 5), pady=(0, 5))

    def on_browse_root() -> None:
        start_dir = var_root.get().strip() or str(current_root)
        try:
            selected = filedialog.askdirectory(
                parent=frame,
                title="Workspace-Root wählen",
                initialdir=start_dir,
            )
        except Exception:
            selected = filedialog.askdirectory(
                parent=frame,
                title="Workspace-Root wählen",
            )
        if selected:
            var_root.set(selected)

    btn_browse = ttk.Button(frame, text="...", width=3, command=on_browse_root)
    btn_browse.grid(row=0, column=2, sticky="w", pady=(0, 5))

    # Row 1: quiet_mode Checkbox
    var_quiet = tk.BooleanVar(value=bool(current_quiet))
    chk_quiet = ttk.Checkbutton(
        frame,
        text="Quiet-Mode (Popups der SonderRunner reduzieren)",
        variable=var_quiet,
    )
    chk_quiet.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 10))

    # Row 2: Speichern-Button
    def on_save() -> None:
        try:
            new_root = Path(var_root.get().strip() or ".").resolve()
            config_manager.set_workspace_root(new_root, auto_save=False)
            config_manager.set_quiet_mode(bool(var_quiet.get()), auto_save=False)
            mgr.save()
            messagebox.showinfo(
                "Settings gespeichert",
                f"Die Einstellungen wurden gespeichert.\n\n"
                f"workspace_root:\n{new_root}\n"
                f"quiet_mode: {'aktiv' if var_quiet.get() else 'inaktiv'}",
                parent=frame,
            )
        except Exception as exc:
            messagebox.showerror(
                "Fehler",
                f"Fehler beim Speichern der Einstellungen:\n{exc}",
                parent=frame,
            )

    btn_save = ttk.Button(frame, text="Einstellungen speichern", command=on_save)
    btn_save.grid(row=2, column=0, columnspan=3, sticky="e")

    # Grid-Konfiguration
    frame.columnconfigure(1, weight=1)

    return frame
