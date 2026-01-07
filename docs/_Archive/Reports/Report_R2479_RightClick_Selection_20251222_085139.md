# R2479 – Right-Click Selection Audit (READ-ONLY)

- Time: 20251222_085139
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- Target: `modules/ui_project_tree.py`

## Findings

### Context menu binding excerpts
```text
   L01088:             try:
   L01089:                 menu.grab_release()
   L01090:             except Exception:
   L01091:                 pass
   L01092: 
   L01093:     try:
>> L01094:         tree.bind("<Button-3>", _on_context, add="+")
   L01095:     except Exception:
   L01096:         pass
   L01097: 
```

## Interpretation
- In Tk, right-click does NOT automatically change selection.
- If no explicit `selection_set(row_under_mouse)` exists in the `<Button-3>` handler,
  the selection is often empty at click time.

## Next step
- If selection is not explicitly set on right-click, implement R2480:
  - determine row under mouse
  - call `tree.selection_set(row)` before showing menu
