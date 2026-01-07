# Report R2394 – ui_runner_products_tab Builder/Toplevel Scan (READ-ONLY)

- Timestamp: 2025-12-19 22:31:58
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- Target: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py`

- Size: 20779 bytes
- SHA256: `6c1e5a5b5df8e245bcca46ab5f72c33c0bd4bb47b9a85b12bcdb8f25d39754e9`

## Builder candidates
- line 263: `build_runner_products_tab`

## Focus: build_runner_products_tab
- Found at line ~263

## Hits (Toplevel/Center/Geometry)
### tk.Toplevel(
- line 76: `        win = tk.Toplevel(app if app is not None else None)`

### geometry(
- line 88: `        win.geometry("980x650")`
- line 118: `            win.geometry(f"{ww}x{wh}+{x}+{y}")`

### screenwidth/height
- line 100: `                ax = win.winfo_screenwidth() // 2`
- line 101: `                ay = win.winfo_screenheight() // 2`
- line 112: `                x = (win.winfo_screenwidth() - ww) // 2`
- line 113: `                y = (win.winfo_screenheight() - wh) // 2`

### center helper
- line 78: `        # --- R2306 CENTER_OVER_APP -------------------------------------------------`
- line 86: `        # --- /R2306 CENTER_OVER_APP ------------------------------------------------`
- line 90: `        # --- R2306 CENTER_OVER_APP (position) --------------------------------------`
- line 93: `            # Ziel: über app (Shrimpi) zentrieren, sonst Screen-Mitte`
- line 121: `        # --- /R2306 CENTER_OVER_APP (position) -------------------------------------`
- line 162: `    # Bottom buttons (zentriert)`

### restored flag
_none_
