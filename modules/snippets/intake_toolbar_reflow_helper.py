def intake_toolbar_reflow_helper(self):
    """
    Ordnet die Toolbar-Buttons harmonisch an.
    Vorsichtig: Nur vorhandene Widgets werden angefasst. Idempotent.
    """
    try:
        pass
    except Exception:
        return
    try:
        bar = getattr(self, "toolbar", None) or getattr(self, "frm_actions", None)
        if not bar:
            return

        # Buttons einsammeln - nur existierende werden berücksichtigt.
        btn_names = [
            "btn_guard",
            "btn_pack",
            "btn_refresh",
            "btn_repair",
            "btn_run",
            "btn_save",
            "btn_open",
            "btn_detect",
            "btn_clear",
        ]
        btns = [getattr(self, n, None) for n in btn_names]
        btns = [b for b in btns if b is not None]

        # Spalten frei machen & gleichmäßig verteilen
        for i, b in enumerate(btns):
            try:
                b.grid_configure(row=0, column=i, padx=(6 if i else 0, 0), sticky="w")
            except Exception:
                pass

        # Mindestbreite
        try:
            for i in range(len(btns)):
                bar.grid_columnconfigure(i, minsize=96, weight=0)
        except Exception:
            pass
    except Exception:
        pass
