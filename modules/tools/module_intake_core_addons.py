# coding: utf-8
"""
module_intake_core_addons.py
Nicht-invasiver Addon-Layer für den Legacy-Intake:
- verschiebt "Speichern unter" ins Menü (Toolbar bleibt clean)
- sorgt dafür, dass create_intake_tab(...) notfalls vorhanden ist
- triggert Erkennen nach Einfügen
Alle Eingriffe sind idempotent & try/except-geschützt.
"""


def apply_intake_core_addons(ns: dict):
    import tkinter as tk
    import tkinter.ttk as ttk

    # 1) Wrapper für create_intake_tab
    if "create_intake_tab" not in ns:

        def create_intake_tab(nb):
            Dev = ns.get("DevIntake") or ns.get("_DevIntake")
            frm = Dev(nb) if Dev else ttk.Frame(nb)
            try:
                nb.add(frm, text="Intake")
            except Exception:
                pass
            return frm

        ns["create_intake_tab"] = create_intake_tab

    Dev = ns.get("DevIntake") or ns.get("_DevIntake")
    if Dev and not getattr(Dev, "_addons_patched", False):
        orig_init = Dev.__init__

        def _wrap(self, *a, **k):
            orig_init(self, *a, **k)
            # Toolbar säubern (Speichern unter raus)
            try:
                for key, val in list(self.__dict__.items()):
                    if hasattr(val, "cget"):
                        try:
                            t = val.cget("text")
                            if isinstance(t, str) and ("Speichern" in t and "als" in t.lower()):
                                # Button verstecken
                                try:
                                    val.pack_forget()
                                except Exception:
                                    pass
                        except Exception:
                            pass
            except Exception:
                pass
            # Einfügen -> danach automatisch Erkennen
            try:
                if hasattr(self, "_insert"):
                    old_insert = self._insert

                    def _after():
                        try:
                            old_insert()
                        finally:
                            try:
                                if hasattr(self, "_detect_all"):
                                    self._detect_all()
                                elif hasattr(self, "detect_all"):
                                    self.detect_all()
                            except Exception:
                                pass

                    self._insert = _after
            except Exception:
                pass

        Dev.__init__ = _wrap
        Dev._addons_patched = True
