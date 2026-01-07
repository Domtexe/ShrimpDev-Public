# Report R2392 – Toplevel/Center Scan (READ-ONLY)

- Timestamp: 2025-12-19 22:12:18
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`

## ui_runner_products_tab.py
- Path: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py`
- Size: 20779 bytes
- SHA256: `6c1e5a5b5df8e245bcca46ab5f72c33c0bd4bb47b9a85b12bcdb8f25d39754e9`

### Hits: toplevel
- line 76: `        win = tk.Toplevel(app if app is not None else None)`

### Hits: center
- line 100: `                ax = win.winfo_screenwidth() // 2`
- line 101: `                ay = win.winfo_screenheight() // 2`
- line 112: `                x = (win.winfo_screenwidth() - ww) // 2`
- line 113: `                y = (win.winfo_screenheight() - wh) // 2`

### Hits: geometry
- line 88: `        win.geometry("980x650")`
- line 118: `            win.geometry(f"{ww}x{wh}+{x}+{y}")`

### Hits: restored_flag
_none_

## ui_pipeline_tab.py
- Path: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_pipeline_tab.py`
- Size: 13225 bytes
- SHA256: `4675b24cd221c17123a7a9a13eca61e3d346171e5c16ea52d86aa8b963f594bd`

### Hits: toplevel
_none_

### Hits: center
_none_

### Hits: geometry
_none_

### Hits: restored_flag
_none_

## ui_log_tab.py
- Path: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_log_tab.py`
- Size: 7829 bytes
- SHA256: `32c4622afbf57f04330d77f27cc28238256ebe574c96bff33ea446230b465d93`

### Hits: toplevel
_none_

### Hits: center
- line 144: `    btn_frame.pack(anchor="center")`

### Hits: geometry
_none_

### Hits: restored_flag
_none_

## module_docking.py
- Path: `C:\Users\rasta\OneDrive\ShrimpDev\modules\module_docking.py`
- Size: 35794 bytes
- SHA256: `cb475649b3f92db71b77ce766c12dfa94fae52d7d663396aa04e84a4976528c5`

### Hits: toplevel
- line 307: `        w = tk.Toplevel(self.app)`

### Hits: center
- line 11: `def _center_window(win, width, height, parent=None):`
- line 30: `                sw = int(win.winfo_screenwidth())`
- line 31: `                sh = int(win.winfo_screenheight())`
- line 35: `            sw = int(win.winfo_screenwidth())`
- line 36: `            sh = int(win.winfo_screenheight())`
- line 336: `                        sw = _r2339_safe_int(self.app.winfo_screenwidth(), 0)`
- line 337: `                        sh = _r2339_safe_int(self.app.winfo_screenheight(), 0)`
- line 353: `        # R2339: center only on first open; restore geometry if provided`
- line 379: `                _center_window(w, 900, 700, parent=self.app)`
- line 553: `            sw = _r2339_safe_int(self.app.winfo_screenwidth(), 0)`
- line 554: `            sh = _r2339_safe_int(self.app.winfo_screenheight(), 0)`
- line 679: `            # offscreen guard (single monitor): clamp to visible area, else center`
- line 682: `                sx = w.winfo_screenwidth(); sy = w.winfo_screenheight()`
- line 849: `# - Offscreen-Schutz -> fallback center`
- line 886: `        sw = int(win.winfo_screenwidth())`
- line 887: `        sh = int(win.winfo_screenheight())`
- line 920: `        # fallback center (nur dann!)`
- line 922: `            if hasattr(self, "_center_window"):`
- line 923: `                self._center_window(win)`
- line 925: `                # fallback center minimal`
- line 926: `                sw = int(win.winfo_screenwidth())`
- line 927: `                sh = int(win.winfo_screenheight())`
- line 934: `            print("[Docking][R2368] offscreen -> center key=", key, "geo=", geo)`

### Hits: geometry
- line 47: `        w.geometry(str(width) + 'x' + str(height) + '+' + str(x) + '+' + str(y))`
- line 368: `                    w.after_idle(lambda g=str(restore_geometry): w.geometry(g))`
- line 370: `                    w.geometry(str(restore_geometry))`
- line 676: `                w.geometry(geo)`
- line 848: `# - Restore aus ShrimpDev.ini [Docking] <key>.geometry (WxH+X+Y)`
- line 930: `                w.geometry(str(w) + "x" + str(h) + "+" + str(nx) + "+" + str(ny))`
- line 940: `        w.geometry(geo)`
- line 1145: `            w.geometry(geo)`

### Hits: restored_flag
- line 293: `    def undock_readonly(self, key, title, builder_func, restore_geometry=None):`
- line 320: `            _r2355_diag(self.app, f"undock key={key} ini={ini} keys={keys} open={op} geo={geo} w={ww} h={hh} x={xx} y={yy} restore_in={restore_geometry}")`
- line 323: `        # R2352_RESTORE_FIX: ensure restore_geometry from INI x/y/w/h when caller passes None`
- line 325: `            if not restore_geometry:`
- line 342: `                            restore_geometry = str(ww)+'x'+str(hh)+'+'+str(xx)+'+'+str(yy)`
- line 344: `                        restore_geometry = str(ww)+'x'+str(hh)+'+'+str(xx)+'+'+str(yy)`
- line 354: `        _r2355_diag(self.app, f"restore_branch key={key} restore_geometry={restore_geometry!r}")`
- line 355: `        if restore_geometry:`
- line 359: `                # Wichtig: restore_geometry muss STRING bleiben, sonst fällt Restore auf Center/WM-Default zurück`
- line 360: `                restore_geometry = geo`
- line 368: `                    w.after_idle(lambda g=str(restore_geometry): w.geometry(g))`
- line 370: `                    w.geometry(str(restore_geometry))`
- line 573: `            self.undock_readonly(key, lab, builder, restore_geometry=restore_geo)`
