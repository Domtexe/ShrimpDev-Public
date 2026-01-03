# LEGACY_AGENT_UI_R2167A
# HINWEIS:
# Diese Datei ist LEGACY/UNUSED. Der produktive Agent-Tab wird in modules/module_agent.py gebaut:
#   build_agent_tab(parent, app)
# Bitte diese Datei nicht mehr erweitern. Neue Agent-Features gehören in module_agent.py.

from tkinter import ttk


class AgentFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Agent").pack(anchor="w", padx=8, pady=8)
