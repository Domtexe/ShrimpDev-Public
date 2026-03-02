# UI_MAP

<!-- R9267_UI_MAP BEGIN -->
# UI_MAP

## Intake Toolbar (SSOT)

- Builder (SSOT): `modules/ui_toolbar.py::build_toolbar_left(parent, app)`
  - Buttons: Neu, Einfügen, Erkennen, Speichern, Undo, AOT, Restart

- Callsite: `main_gui.py::ShrimpDevApp._build_intake`
  - Container: `frame_toolbar_left` (grid row=0, colspan=2)
  - Build: `tl = ui_toolbar.build_toolbar_left(frame_toolbar_left, self)`
  - Pack: `tl.pack(fill="x")`

## Runtime Proof (R9267)
- Buttons are mapped (ismapped=1) and have non-zero geometry.
<!-- R9267_UI_MAP END -->
