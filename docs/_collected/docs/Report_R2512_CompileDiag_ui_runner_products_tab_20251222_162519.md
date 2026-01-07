# R2512 – Compile Diag ui_runner_products_tab.py (READ-ONLY)

- Time: 20251222_162519
- Target: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py`

## Compile
- py_compile: FAIL
- Error: `  File "C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py", line 869
    m.add_separator()
SyntaxError: expected 'except' or 'finally' block
`

## R2511 markers
- L739: # --- R2511_START: Backup restore (SAFE) ----------------------------------------------
- L842: # --- R2511_END: Backup restore (SAFE) -----------------------------------------------

## Context around line 869
```text
   L00799:                     msg += f"\n... (+{len(cands)-20} weitere)"
   L00800:             try:
   L00801:                 from tkinter import messagebox
   L00802:                 messagebox.showwarning("Backup wiederherstellen", msg)
   L00803:             except Exception:
   L00804:                 pass
   L00805:             try:
   L00806:                 app.clipboard_clear()
   L00807:                 app.clipboard_append("\n".join(cands) if cands else base)
   L00808:             except Exception:
   L00809:                 pass
   L00810:             return
   L00811: 
   L00812:         target_path = cands[0]
   L00813: 
   L00814:         # Safety: back up current target before overwrite
   L00815:         try:
   L00816:             arch = os.path.join(_root_dir, "_Archiv")
   L00817:             os.makedirs(arch, exist_ok=True)
   L00818:             stamp2 = datetime.now().strftime("%Y%m%d_%H%M%S")
   L00819:             safety_bak = os.path.join(arch, f"{os.path.basename(target_path)}.RESTORE_BEFORE_{RID}_{stamp2}.bak")
   L00820:             shutil.copy2(target_path, safety_bak)
   L00821:         except Exception:
   L00822:             safety_bak = None
   L00823: 
   L00824:         try:
   L00825:             shutil.copy2(p, target_path)
   L00826:             ok = True
   L00827:         except Exception as e:
   L00828:             ok = False
   L00829:             err = str(e)
   L00830: 
   L00831:         try:
   L00832:             from tkinter import messagebox
   L00833:             if ok:
   L00834:                 msg = f"OK: Wiederhergestellt.\n\nBackup:\n{p}\n\nZiel:\n{target_path}"
   L00835:                 if safety_bak:
   L00836:                     msg += f"\n\nSicherungs-Backup vorher:\n{safety_bak}"
   L00837:                 messagebox.showinfo("Backup wiederherstellen", msg)
   L00838:             else:
   L00839:                 messagebox.showerror("Backup wiederherstellen", f"FEHLER:\n{err}\n\nBackup:\n{p}\n\nZiel:\n{target_path}")
   L00840:         except Exception:
   L00841:             pass
   L00842:     # --- R2511_END: Backup restore (SAFE) -----------------------------------------------
   L00843: 
   L00844: 
   L00845:     def _tree_context_menu(ev):
   L00846:         try:
   L00847:             iid = tree.identify_row(ev.y)
   L00848:             if iid:
   L00849:                 tree.selection_set(iid)
   L00850:         except Exception:
   L00851:             pass
   L00852: 
   L00853:         p = _selected_path()
   L00854:         if not p:
   L00855:             return
   L00856: 
   L00857:         try:
   L00858:             m = tk.Menu(tree, tearoff=0)
   L00859:             m.add_command(label="Intern anzeigen", command=_on_viewer)
   L00860:             m.add_command(label="Öffnen", command=_on_open)
   L00861:             m.add_command(label="Ordner öffnen", command=_on_folder)
   L00862:                         # R2511: gated restore only for _Archiv backups
   L00863:             try:
   L00864:                 if _is_backup_path(p):
   L00865:                     m.add_command(label="Backup wiederherstellen", command=_on_restore_backup)
   L00866:                     m.add_separator()
   L00867:             except Exception:
   L00868:                 pass
>> L00869: m.add_separator()
   L00870:             m.add_command(label="Pfad kopieren", command=_on_copy)
   L00871:             m.add_command(label="Datei kopieren (Explorer-Paste)", command=_on_copy_file_paste)
   L00872:             m.add_command(label="Inhalt kopieren (Text)", command=_on_copy_content)
   L00873:             m.tk_popup(ev.x_root, ev.y_root)
   L00874:         except Exception:
   L00875:             pass
   L00876: 
   L00877:     try:
   L00878:         tree.bind("<Double-Button-1>", _tree_open_selected)
   L00879:         tree.bind("<Button-3>", _tree_context_menu)
   L00880: 
   L00881:     except Exception:
   L00882:         pass
   L00883: 
   L00884:     # --- R2508_START: Preview right-click menu ------------------------------------------
   L00885:     def _preview_copy_selection_or_all():
   L00886:         # Copy selected text; if none selected, copy all preview text
   L00887:         try:
   L00888:             sel = txt.selection_get()
   L00889:             data = sel if sel else ""
   L00890:         except Exception:
   L00891:             data = ""
   L00892:         if not data:
   L00893:             try:
   L00894:                 data = txt.get("1.0", "end-1c")
   L00895:             except Exception:
   L00896:                 data = ""
   L00897:         try:
   L00898:             app.clipboard_clear()
   L00899:             app.clipboard_append(data or "")
   L00900:         except Exception:
   L00901:             pass
   L00902: 
   L00903:     def _preview_copy_path():
   L00904:         p = _selected_path()
   L00905:         try:
   L00906:             app.clipboard_clear()
   L00907:             app.clipboard_append(p or "")
   L00908:         except Exception:
   L00909:             pass
   L00910: 
   L00911:     def _preview_copy_file_for_paste():
   L00912:         p2 = _selected_path()
   L00913:         if not p2:
   L00914:             return
   L00915:         try:
   L00916:             _hwnd = txt.winfo_id()
   L00917:         except Exception:
   L00918:             _hwnd = None
   L00919:         ok, msg = _r2497_copy_file_for_paste(p2, hwnd=_hwnd)
   L00920:         try:
   L00921:             from tkinter import messagebox
   L00922:             if not ok:
   L00923:                 messagebox.showwarning("Datei kopieren", msg or "Nicht verfügbar.")
   L00924:         except Exception:
   L00925:             pass
   L00926: 
   L00927:     def _preview_context_menu(ev):
   L00928:         # Ensure focus (some apps require focus for selection_get)
   L00929:         try:
   L00930:             txt.focus_set()
   L00931:         except Exception:
   L00932:             pass
   L00933:         try:
   L00934:             m = tk.Menu(txt, tearoff=0)
   L00935:             m.add_command(label="Inhalt kopieren (Text)", command=_preview_copy_selection_or_all)
   L00936:             m.add_separator()
   L00937:             m.add_command(label="Pfad kopieren", command=_preview_copy_path)
   L00938:             m.add_command(label="Datei kopieren (Explorer-Paste)", command=_preview_copy_file_for_paste)
   L00939:             m.tk_popup(ev.x_root, ev.y_root)
```
