# Report R2404 – Post-Restore Geometry Setter Scan (READ-ONLY)

- Timestamp: 2025-12-20 00:00:33
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`

## `main_gui.py`
- size: 25195 bytes
- sha256: `9786a40e0b12dcd2b60c807707e414c9531d5419181cb9177241cb08384a543e`
- hits: **3**

### hits
- L109 [geometry_call] `self.geometry("1300x780")`
- L310 [geometry_call] `self.geometry(geo)`
- L708 [geometry_call] `app.geometry(geo)`

## `modules\module_docking.py`
- size: 36915 bytes
- sha256: `01262ec189509d0515abfc51550af3ccdd7b084256e1b03c9b2bdee07d6b377e`
- hits: **31**

### hits
- L11 [center_helper] `def _center_window(win, width, height, parent=None):`
- L47 [geometry_call] `w.geometry(str(width) + 'x' + str(height) + '+' + str(x) + '+' + str(y))`
- L226 [geometry_call] `geo = str(w.wm_geometry())`
- L245 [withdraw_deiconify] `w.withdraw()`
- L300 [withdraw_deiconify] `w.deiconify()`
- L301 [withdraw_deiconify] `w.lift()`
- L334 [center_helper] `# offscreen guard; if screen size not ready yet, skip guard and apply anyway`
- L362 [withdraw_deiconify] `w.withdraw()`
- L368 [geometry_call,after_idle_geo] `w.after_idle(lambda g=str(restore_geometry): w.geometry(g))`
- L370 [geometry_call] `w.geometry(str(restore_geometry))`
- L374 [withdraw_deiconify] `w.deiconify()`
- L379 [center_helper] `_center_window(w, 900, 700, parent=self.app)`
- L448 [geometry_call] `g = w.wm_geometry()`
- L520 [restore_from_ini] `def restore_from_ini(self):`
- L608 [restore_from_ini] `dm.restore_from_ini()`
- L678 [center_helper] `Priority: <key>.geometry, else build from w/h/x/y. Center only if nothing usable or offscreen.`
- L699 [geometry_call] `w.geometry(geo)`
- L702 [center_helper] `# offscreen guard (single monitor): clamp to visible area, else center`
- L746 [geometry_call] `# - Persist aus wm_geometry() (WxH+X+Y)`
- L814 [geometry_call] `geo = str(win.wm_geometry())`
- L871 [geometry_call] `# - Restore aus ShrimpDev.ini [Docking] <key>.geometry (WxH+X+Y)`
- L872 [center_helper] `# - Offscreen-Schutz -> fallback center`
- L945 [center_helper] `if hasattr(self, "_center_window"):`
- L946 [center_helper] `self._center_window(win)`
- L953 [geometry_call] `w.geometry(str(w) + "x" + str(h) + "+" + str(nx) + "+" + str(ny))`
- L957 [center_helper] `print("[Docking][R2368] offscreen -> center key=", key, "geo=", geo)`
- L963 [geometry_call] `w.geometry(geo)`
- L975 [restore_from_ini] `DockManager._restore_one = _r2368_restore_one`
- L1063 [geometry_call] `return str(win.wm_geometry())`
- L1168 [geometry_call] `w.geometry(geo)`
- L1183 [restore_from_ini] `DockManager._restore_one = _r2369_restore_one`

## `modules\ui_runner_products_tab.py`
- size: 20779 bytes
- sha256: `6c1e5a5b5df8e245bcca46ab5f72c33c0bd4bb47b9a85b12bcdb8f25d39754e9`
- hits: **7**

### hits
- L78 [center_helper] `# --- R2306 CENTER_OVER_APP -------------------------------------------------`
- L83 [withdraw_deiconify] `win.lift()`
- L86 [center_helper] `# --- /R2306 CENTER_OVER_APP ------------------------------------------------`
- L88 [geometry_call] `win.geometry("980x650")`
- L90 [center_helper] `# --- R2306 CENTER_OVER_APP (position) --------------------------------------`
- L118 [geometry_call] `win.geometry(f"{ww}x{wh}+{x}+{y}")`
- L121 [center_helper] `# --- /R2306 CENTER_OVER_APP (position) -------------------------------------`

## `modules\ui_pipeline_tab.py`
- size: 13225 bytes
- sha256: `4675b24cd221c17123a7a9a13eca61e3d346171e5c16ea52d86aa8b963f594bd`
- hits: **0**


## `modules\ui_log_tab.py`
- size: 7829 bytes
- sha256: `32c4622afbf57f04330d77f27cc28238256ebe574c96bff33ea446230b465d93`
- hits: **0**


## `modules\ui_toolbar.py`
- size: 29813 bytes
- sha256: `c60dc4a7bf8aa569a18badb0788ad74fa791592703ce3b67f8c2ea31a10d3352`
- hits: **3**

### hits
- L314 [geometry_call] `win.geometry(geom)`
- L320 [geometry_call] `win.geometry("700x450")`
- L328 [geometry_call] `win.geometry(f"+{max(x, 0)}+{max(y, 0)}")`

