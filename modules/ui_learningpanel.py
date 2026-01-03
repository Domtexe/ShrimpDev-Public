from __future__ import annotations

"""Learning-Panel - Grundgeruest fuer ShrimpDev LearningEngine Phase C.

Dieses Modul stellt ein einfaches UI-Panel bereit, das zukuenftig fuer
LearningEngine-Status, Hinweise und Ueberblick genutzt werden kann.
Aktuell zeigt es nur statische Informationen an und ist Darkmode-kompatibel.
"""

import tkinter as tk
from tkinter import ttk


def build_learning_panel(parent: tk.Frame, app: tk.Misc) -> tk.Frame:
    """Erzeugt das Learning-Panel-Frame.

    Parameters
    ----------
    parent:
        Container-Frame (z. B. ein Tab-Frame).
    app:
        Hauptanwendung; wird aktuell nicht benutzt, ist aber fuer
        spaetere Erweiterungen vorgesehen.

    Returns
    -------
    tk.Frame
        Das erzeugte Frame mit Titel- und Info-Text.
    """
    frame = ttk.Frame(parent)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    lbl_title = ttk.Label(
        frame,
        text="LearningEngine - Uebersicht",
        anchor="w",
    )
    lbl_title.grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 4))

    info_text = (
        "Dies ist das Learning-System von ShrimpDev.\n"
        "Hier koennen kuenftig Journal, Engine-Status und Vorschlaege "
        "angezeigt werden.\n"
        "In Phase C dient dieses Panel als einfache Uebersicht und "
        "Platzhalter fuer kuenftige Erweiterungen."
    )

    lbl_info = ttk.Label(
        frame,
        text=info_text,
        justify="left",
        anchor="nw",
    )
    lbl_info.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    return frame
