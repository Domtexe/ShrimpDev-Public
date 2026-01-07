# R2509 – Compile Diag ui_runner_products_tab.py (READ-ONLY)

- Time: 20251222_151522
- Target: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py`

## Compile
- py_compile: FAIL
- Error: `  File "C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py", line 770
    def _preview_copy_selection_or_all():
    ^^^
SyntaxError: expected 'except' or 'finally' block
`

## R2508 markers
- L769: # --- R2508_START: Preview right-click menu ------------------------------------------
- L832: # --- R2508_END: Preview right-click menu --------------------------------------------

## Context around line 770
```text
   L00710:     def _tree_open_selected(_ev=None):
   L00711:         _on_open()
   L00712: 
   L00713:     def _tree_copy_path(_ev=None):
   L00714:         _on_copy()
   L00715: 
   L00716:     def _tree_copy_content(_ev=None):
   L00717:         _on_copy_content()
   L00718: 
   L00719:     # R2497_ACTION_START
   L00720:     def _on_copy_file_paste():
   L00721:         try:
   L00722:             p2 = _selected_path()
   L00723:         except Exception:
   L00724:             p2 = None
   L00725:         try:
   L00726:             _hwnd = tree.winfo_id()
   L00727:         except Exception:
   L00728:             _hwnd = None
   L00729:         ok, msg = _r2497_copy_file_for_paste(p2, hwnd=_hwnd)
   L00730:         try:
   L00731:             from tkinter import messagebox
   L00732:             if ok:
   L00733:                 messagebox.showinfo("Datei kopieren", "Datei im Clipboard. (Explorer: Strg+V)")
   L00734:             else:
   L00735:                 messagebox.showwarning("Datei kopieren", f"Nicht möglich: {msg}")
   L00736:         except Exception:
   L00737:             pass
   L00738:     # R2497_ACTION_END
   L00739: 
   L00740:     def _tree_context_menu(ev):
   L00741:         try:
   L00742:             iid = tree.identify_row(ev.y)
   L00743:             if iid:
   L00744:                 tree.selection_set(iid)
   L00745:         except Exception:
   L00746:             pass
   L00747: 
   L00748:         p = _selected_path()
   L00749:         if not p:
   L00750:             return
   L00751: 
   L00752:         try:
   L00753:             m = tk.Menu(tree, tearoff=0)
   L00754:             m.add_command(label="Intern anzeigen", command=_on_viewer)
   L00755:             m.add_command(label="Öffnen", command=_on_open)
   L00756:             m.add_command(label="Ordner öffnen", command=_on_folder)
   L00757:             m.add_separator()
   L00758:             m.add_command(label="Pfad kopieren", command=_on_copy)
   L00759:             m.add_command(label="Datei kopieren (Explorer-Paste)", command=_on_copy_file_paste)
   L00760:             m.add_command(label="Inhalt kopieren (Text)", command=_on_copy_content)
   L00761:             m.tk_popup(ev.x_root, ev.y_root)
   L00762:         except Exception:
   L00763:             pass
   L00764: 
   L00765:     try:
   L00766:         tree.bind("<Double-Button-1>", _tree_open_selected)
   L00767:         tree.bind("<Button-3>", _tree_context_menu)
   L00768: 
   L00769:     # --- R2508_START: Preview right-click menu ------------------------------------------
>> L00770:     def _preview_copy_selection_or_all():
   L00771:         # Copy selected text; if none selected, copy all preview text
   L00772:         try:
   L00773:             sel = txt.selection_get()
   L00774:             data = sel if sel else ""
   L00775:         except Exception:
   L00776:             data = ""
   L00777:         if not data:
   L00778:             try:
   L00779:                 data = txt.get("1.0", "end-1c")
   L00780:             except Exception:
   L00781:                 data = ""
   L00782:         try:
   L00783:             app.clipboard_clear()
   L00784:             app.clipboard_append(data or "")
   L00785:         except Exception:
   L00786:             pass
   L00787: 
   L00788:     def _preview_copy_path():
   L00789:         p = _selected_path()
   L00790:         try:
   L00791:             app.clipboard_clear()
   L00792:             app.clipboard_append(p or "")
   L00793:         except Exception:
   L00794:             pass
   L00795: 
   L00796:     def _preview_copy_file_for_paste():
   L00797:         p2 = _selected_path()
   L00798:         if not p2:
   L00799:             return
   L00800:         try:
   L00801:             _hwnd = txt.winfo_id()
   L00802:         except Exception:
   L00803:             _hwnd = None
   L00804:         ok, msg = _r2497_copy_file_for_paste(p2, hwnd=_hwnd)
   L00805:         try:
   L00806:             from tkinter import messagebox
   L00807:             if not ok:
   L00808:                 messagebox.showwarning("Datei kopieren", msg or "Nicht verfügbar.")
   L00809:         except Exception:
   L00810:             pass
   L00811: 
   L00812:     def _preview_context_menu(ev):
   L00813:         # Ensure focus (some apps require focus for selection_get)
   L00814:         try:
   L00815:             txt.focus_set()
   L00816:         except Exception:
   L00817:             pass
   L00818:         try:
   L00819:             m = tk.Menu(txt, tearoff=0)
   L00820:             m.add_command(label="Inhalt kopieren (Text)", command=_preview_copy_selection_or_all)
   L00821:             m.add_separator()
   L00822:             m.add_command(label="Pfad kopieren", command=_preview_copy_path)
   L00823:             m.add_command(label="Datei kopieren (Explorer-Paste)", command=_preview_copy_file_for_paste)
   L00824:             m.tk_popup(ev.x_root, ev.y_root)
   L00825:         except Exception:
   L00826:             pass
   L00827: 
   L00828:     try:
   L00829:         txt.bind("<Button-3>", _preview_context_menu)
   L00830:     except Exception:
```
