# R2486 – Compile Diagnose ui_project_tree.py (READ-ONLY)

- Time: 20251222_103052
- Target: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_project_tree.py`

## Compile
- py_compile: FAIL
- Error: `PyCompileError('Sorry: IndentationError: unexpected indent (ui_project_tree.py, line 1037)', 'IndentationError', IndentationError('unexpected indent', ('C:\\Users\\rasta\\OneDrive\\ShrimpDev\\modules\\ui_project_tree.py', 1037, 8, '        import re as _r2485_re\n', 1037, -1)), 'C:\\Users\\rasta\\OneDrive\\ShrimpDev\\modules\\ui_project_tree.py')`
- Line: `1037`

## Context
```text
   L01025:             pass
   L01026: 
   L01027:         try:
   L01028:             from tkinter import messagebox
   L01029:             messagebox.showinfo("Backup wiederherstellen", "OK: Wiederhergestellt.")
   L01030:         except Exception:
   L01031:             pass
   L01032:     # --- R2477_END ---
   L01033: 
   L01034:     menu = tk.Menu(tree, tearoff=False)
   L01035: 
   L01036:         # R2485_START: Right-list menu actions (files + restore)
>> L01037:         import re as _r2485_re
   L01038:         import shutil as _r2485_shutil
   L01039:     
   L01040:         _r2485_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
   L01041:     
   L01042:         def _r2485_selected_paths():
   L01043:             # uses existing mapping paths (iid -> path)
   L01044:             try:
   L01045:                 sel = tree.selection()
   L01046:             except Exception:
   L01047:                 sel = ()
   L01048:             out = []
   L01049:             for iid in sel:
```
