# R2496 – Extract _tree_context_menu (READ-ONLY)

- Time: 20251222_114014
- Target: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py`

## Function block
```python
00535:     def _tree_context_menu(ev):
00536:         try:
00537:             iid = tree.identify_row(ev.y)
00538:             if iid:
00539:                 tree.selection_set(iid)
00540:         except Exception:
00541:             pass
00542: 
00543:         p = _selected_path()
00544:         if not p:
00545:             return
00546: 
00547:         try:
00548:             m = tk.Menu(tree, tearoff=0)
00549:             m.add_command(label="Intern anzeigen", command=_on_viewer)
00550:             m.add_command(label="Öffnen", command=_on_open)
00551:             m.add_command(label="Ordner öffnen", command=_on_folder)
00552:             m.add_separator()
00553:             m.add_command(label="Pfad kopieren", command=_on_copy)
00554:             m.add_command(label="Inhalt kopieren (Text)", command=_on_copy_content)
00555:             m.tk_popup(ev.x_root, ev.y_root)
00556:         except Exception:
00557:             pass
00558: 
00559:     try:
00560:         tree.bind("<Double-Button-1>", _tree_open_selected)
00561:         tree.bind("<Button-3>", _tree_context_menu)
00562:         tree.bind("<Control-c>", _tree_copy_path)
00563:         tree.bind("<Control-Shift-C>", _tree_copy_content)
00564:     except Exception:
00565:         pass
00566:     # --- /R2303 TREE UX --------------------------------------------------------------
00567: 
```

## Menu-related lines (within function)
```text
L00535:     def _tree_context_menu(ev):
L00548:             m = tk.Menu(tree, tearoff=0)
L00549:             m.add_command(label="Intern anzeigen", command=_on_viewer)
L00550:             m.add_command(label="Öffnen", command=_on_open)
L00551:             m.add_command(label="Ordner öffnen", command=_on_folder)
L00552:             m.add_separator()
L00553:             m.add_command(label="Pfad kopieren", command=_on_copy)
L00554:             m.add_command(label="Inhalt kopieren (Text)", command=_on_copy_content)
L00555:             m.tk_popup(ev.x_root, ev.y_root)
```
