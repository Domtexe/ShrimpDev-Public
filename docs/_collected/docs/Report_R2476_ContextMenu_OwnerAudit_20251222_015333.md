# R2476 – Context Menu Owner Audit (READ-ONLY)

- Time: 20251222_015333
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- Scan: `modules/*.py`

## Goal
- Find who binds Tree right-click (`<Button-3>`) and who calls `enable_context_menu()`.
- Detect possible double-bindings (owner conflict).

## Findings (by file)

### `logic_actions.py`
- **BIND Button-3**: 1 hit(s) (showing 1)
```text
   L01062:             try:
   L01063:                 _menu.grab_release()
   L01064:             except Exception:
   L01065:                 pass
   L01066: 
   L01067:     try:
>> L01068:         tree.bind("<Button-3>", lambda event: _on_button3(event), add="+")
   L01069:     except Exception:
   L01070:         pass
   L01071: 
   L01072: # build_tree aus ui_project_tree wrappen, damit Kontextmenue nach dem Aufbau gesetzt wird
   L01073: try:
   L01074:     from modules import ui_project_tree as _r1848_uipt  # type: ignore
```
- **tk.Menu usage**: 1 hit(s) (showing 1)
```text
   L01003:     if _r1848_tk is None:
   L01004:         return
   L01005:     tree = getattr(app, "tree", None)
   L01006:     if tree is None:
   L01007:         return
   L01008: 
>> L01009:     menu = _r1848_tk.Menu(tree, tearoff=False)
   L01010: 
   L01011:     def _update_selection(event):
   L01012:         try:
   L01013:             row_id = tree.identify_row(event.y)
   L01014:             if row_id:
   L01015:                 tree.selection_set(row_id)
```
- **tk_popup usage**: 1 hit(s) (showing 1)
```text
   L01054:     menu.add_command(label="Umbenennen…", command=_cmd_rename)
   L01055:     menu.add_command(label="In den Papierkorb", command=_cmd_trash)
   L01056: 
   L01057:     def _on_button3(event, _menu=menu):
   L01058:         _update_selection(event)
   L01059:         try:
>> L01060:             _menu.tk_popup(event.x_root, event.y_root)
   L01061:         finally:
   L01062:             try:
   L01063:                 _menu.grab_release()
   L01064:             except Exception:
   L01065:                 pass
   L01066: 
```

### `module_agent.py`
- **Treeview creation**: 1 hit(s) (showing 1)
```text
   L00526:     left.pack(side="left", fill="y")
   L00527: 
   L00528:     right = ttk.Frame(outer)
   L00529:     right.pack(side="left", fill="both", expand=True, padx=(10, 0))
   L00530: 
   L00531:     cols = ("exists", "title")
>> L00532:     tree = ttk.Treeview(left, columns=cols, show="headings", height=14, selectmode="browse")
   L00533:     tree.heading("exists", text="OK")
   L00534:     tree.heading("title", text="Empfehlung")
   L00535:     tree.column("exists", width=45, stretch=False, anchor="center")
   L00536:     tree.column("title", width=360, stretch=True, anchor="w")
   L00537:     vs = ttk.Scrollbar(left, orient="vertical", command=tree.yview)
   L00538:     tree.configure(yscrollcommand=vs.set)
```

### `module_docking.py`
- **BIND Button-3**: 1 hit(s) (showing 1)
```text
   L00661:             try:
   L00662:                 menu.grab_release()
   L00663:             except Exception:
   L00664:                 pass
   L00665: 
   L00666:     try:
>> L00667:         notebook.bind('<Button-3>', _on_right_click)
   L00668:     except Exception:
   L00669:         pass
   L00670:     return dm
   L00671: 
   L00672: # R2342_FORCE_PERSIST_ON_CLOSE
   L00673: 
```
- **tk.Menu usage**: 1 hit(s) (showing 1)
```text
   L00648:                 chosen = (label, key, builder)
   L00649:                 break
   L00650:         if chosen is None:
   L00651:             return
   L00652: 
   L00653:         label, key, builder = chosen
>> L00654:         menu = tk.Menu(app, tearoff=0)
   L00655:         menu.add_command(label='Undock', command=lambda: dm.undock_readonly(key, label, builder))
   L00656:         if dm.is_open(key):
   L00657:             menu.add_command(label='Dock (Fenster schließen)', command=lambda: dm.close(key))
   L00658:         try:
   L00659:             menu.tk_popup(ev.x_root, ev.y_root)
   L00660:         finally:
```
- **tk_popup usage**: 1 hit(s) (showing 1)
```text
   L00653:         label, key, builder = chosen
   L00654:         menu = tk.Menu(app, tearoff=0)
   L00655:         menu.add_command(label='Undock', command=lambda: dm.undock_readonly(key, label, builder))
   L00656:         if dm.is_open(key):
   L00657:             menu.add_command(label='Dock (Fenster schließen)', command=lambda: dm.close(key))
   L00658:         try:
>> L00659:             menu.tk_popup(ev.x_root, ev.y_root)
   L00660:         finally:
   L00661:             try:
   L00662:                 menu.grab_release()
   L00663:             except Exception:
   L00664:                 pass
   L00665: 
```

### `module_learningjournal_ui_ext.py`
- **Treeview creation**: 1 hit(s) (showing 1)
```text
   L00087: 
   L00088:     lbl_path = ttk.Label(frame, text="Datei: {}".format(get_learning_journal_path(root_dir)))
   L00089:     lbl_path.pack(side="top", anchor="w", padx=8)
   L00090: 
   L00091:     # Tree
   L00092:     columns = ("id", "timestamp", "category", "score", "summary")
>> L00093:     tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
   L00094:     tree.pack(side="top", fill="both", expand=True, padx=8, pady=4)
   L00095: 
   L00096:     headers = {
   L00097:         "id": "ID",
   L00098:         "timestamp": "Zeitstempel",
   L00099:         "category": "Kategorie",
```

### `module_preflight.py`
- **Treeview creation**: 1 hit(s) (showing 1)
```text
   L00021:         rows.append((f"dir:{d.name}", "exists" if d.exists() else "missing", "OK" if d.exists() else "WARN"))
   L00022:     return rows
   L00023: 
   L00024: def _build_tab(parent):
   L00025:     frm = ttk.Frame(parent)
   L00026:     b = ttk.Frame(frm); b.pack(fill="x", pady=6)
>> L00027:     tree = ttk.Treeview(frm, columns=("item","value","status"), show="headings")
   L00028:     for c,w in zip(("item","value","status"),(300,280,80)): tree.heading(c, text=c); tree.column(c, width=w, anchor="w")
   L00029:     tree.pack(fill="both", expand=True)
   L00030:     def run():
   L00031:         rows = _checks()
   L00032:         for i in tree.get_children(): tree.delete(i)
   L00033:         for r in rows: tree.insert("", "end", values=r)
```

### `module_runner_board.py`
- **Treeview creation**: 1 hit(s) (showing 1)
```text
   L00016:     return out
   L00017: 
   L00018: def _build_tab(parent):
   L00019:     frm = ttk.Frame(parent)
   L00020:     bar = ttk.Frame(frm); bar.pack(fill="x", pady=6)
   L00021:     ttk.Button(bar, text="Refresh", command=lambda: refresh()).pack(side="left")
>> L00022:     tree = ttk.Treeview(frm, columns=("file","type"), show="headings")
   L00023:     for c,w in (("file",650),("type",160)): tree.heading(c, text=c); tree.column(c, width=w, anchor="w")
   L00024:     tree.pack(fill="both", expand=True)
   L00025: 
   L00026:     def refresh():
   L00027:         for i in tree.get_children(): tree.delete(i)
   L00028:         for name, typ in _list(): tree.insert("", "end", values=(name, typ))
```

### `ui_lists.py`
- **Treeview creation**: 1 hit(s) (showing 1)
```text
   L00002: from tkinter import ttk
   L00003: 
   L00004: _TREE = "proj_tree"
   L00005: 
   L00006: def create_tree(parent, app):
   L00007:     cols = ("path","type","note")
>> L00008:     tree = ttk.Treeview(parent, columns=cols, show="headings", name=_TREE)
   L00009:     for c in cols:
   L00010:         tree.heading(c, text=c.capitalize())
   L00011:         tree.column(c, width=260 if c=="path" else 140, anchor="w")
   L00012:     tree.pack(fill="both", expand=True, padx=12, pady=(8,12))
   L00013:     # neutrale Beispielzeile
   L00014:     tree.insert("", "end", values=(".", "ProjectRoot", "ShrimpDev"))
```

### `ui_menus.py`
- **tk.Menu usage**: 3 hit(s) (showing 3)
```text
   L00001: import tkinter as tk
   L00002: from tkinter import messagebox
   L00003: 
   L00004: def build_menu(app):
>> L00005:     m = tk.Menu(app)
   L00006:     file = tk.Menu(m, tearoff=False)
   L00007:     file.add_checkbutton(label="Always on Top",
   L00008:                          command=lambda: _toggle_top(app))
   L00009:     file.add_separator()
   L00010:     file.add_command(label="Beenden", command=app.destroy)
   L00011:     m.add_cascade(label="File", menu=file)
```
```text
   L00001: import tkinter as tk
   L00002: from tkinter import messagebox
   L00003: 
   L00004: def build_menu(app):
   L00005:     m = tk.Menu(app)
>> L00006:     file = tk.Menu(m, tearoff=False)
   L00007:     file.add_checkbutton(label="Always on Top",
   L00008:                          command=lambda: _toggle_top(app))
   L00009:     file.add_separator()
   L00010:     file.add_command(label="Beenden", command=app.destroy)
   L00011:     m.add_cascade(label="File", menu=file)
   L00012: 
```
```text
   L00007:     file.add_checkbutton(label="Always on Top",
   L00008:                          command=lambda: _toggle_top(app))
   L00009:     file.add_separator()
   L00010:     file.add_command(label="Beenden", command=app.destroy)
   L00011:     m.add_cascade(label="File", menu=file)
   L00012: 
>> L00013:     helpm = tk.Menu(m, tearoff=False)
   L00014:     helpm.add_command(label="Info", command=lambda: messagebox.showinfo("ShrimpDev", "ShrimpDev - Development GUI"))
   L00015:     m.add_cascade(label="Help", menu=helpm)
   L00016: 
   L00017:     app.config(menu=m)
   L00018: 
   L00019: def _toggle_top(app):
```

### `ui_pipeline_tab.py`
- **Treeview creation**: 3 hit(s) (showing 3)
```text
   L00014: def _pipeline_path() -> Path:
   L00015:     return _project_root() / "docs" / "PIPELINE.md"
   L00016: 
   L00017: 
   L00018: def build_pipeline_tab(parent, app) -> None:
   L00019:     # PIPELINE_TREEVIEW_R2156
>> L00020:     # UX+Debug: Task-Liste (Treeview) + Toggle + Filter + Summary + Auto-Reload + Diagnose
   L00021: 
   L00022:     header = ttk.Label(parent, text="Pipeline", anchor="w")
   L00023:     # PIPELINE_UX_R2166
   L00024: 
   L00025:     header.pack(fill="x", padx=10, pady=(10, 4))
   L00026: 
```
```text
   L00062:     content.pack(fill="both", expand=True, padx=10, pady=(0, 10))
   L00063: 
   L00064:     cols = ("status", "prio", "task", "section")
   L00065: 
   L00066:     style = ttk.Style()
   L00067:     try:
>> L00068:         style.configure("Pipeline.Treeview", rowheight=22)
   L00069:     except Exception:
   L00070:         pass
   L00071: 
   L00072:     tree = ttk.Treeview(content, columns=cols, show="headings", selectmode="browse", style="Pipeline.Treeview")
   L00073:     tree.heading("status", text="Status")
   L00074:     tree.heading("prio", text="Prio")
```
```text
   L00066:     style = ttk.Style()
   L00067:     try:
   L00068:         style.configure("Pipeline.Treeview", rowheight=22)
   L00069:     except Exception:
   L00070:         pass
   L00071: 
>> L00072:     tree = ttk.Treeview(content, columns=cols, show="headings", selectmode="browse", style="Pipeline.Treeview")
   L00073:     tree.heading("status", text="Status")
   L00074:     tree.heading("prio", text="Prio")
   L00075:     tree.heading("task", text="Task")
   L00076:     tree.heading("section", text="Section")
   L00077:     tree.column("status", width=70, stretch=False, anchor="w")
   L00078:     tree.column("prio", width=80, stretch=False, anchor="w")
```

### `ui_project_tree.py`
- **CALL enable_context_menu**: 1 hit(s) (showing 1)
```text
   L00802:         tree.bind("<B1-Motion>", _on_lasso_drag, add="+")
   L00803:         tree.bind("<ButtonRelease-1>", _on_lasso_end, add="+")
   L00804:     except Exception:
   L00805:         pass
   L00806: 
   L00807: 
>> L00808: def enable_context_menu(app) -> None:
   L00809:     """
   L00810:     Aktiviert ein Kontextmenue auf der TreeView (rechte Liste):
   L00811: 
   L00812:     - Rechtsklick auf einen Eintrag:
   L00813:         * Auswahl ggf. auf diesen Eintrag setzen
   L00814:         * Menue mit "Pfad(e) kopieren" anzeigen
```
- **BIND Button-3**: 1 hit(s) (showing 1)
```text
   L00880:             try:
   L00881:                 menu.grab_release()
   L00882:             except Exception:
   L00883:                 pass
   L00884: 
   L00885:     try:
>> L00886:         tree.bind("<Button-3>", _on_context, add="+")
   L00887:     except Exception:
   L00888:         pass
   L00889: 
```
- **tk.Menu usage**: 1 hit(s) (showing 1)
```text
   L00822:     if tree is None:
   L00823:         return
   L00824: 
   L00825:     # Lokaler Import, um keine globalen Abhaengigkeiten zu erzwingen
   L00826:     import tkinter as tk
   L00827: 
>> L00828:     menu = tk.Menu(tree, tearoff=False)
   L00829: 
   L00830:     def _copy_selected():
   L00831:         try:
   L00832:             sel = tree.selection()
   L00833:         except Exception:
   L00834:             sel = ()
```
- **tk_popup usage**: 1 hit(s) (showing 1)
```text
   L00872:                         if (event.state & 0x0004):  # Control-Key
   L00873:                             tree.selection_add(row)
   L00874:                         else:
   L00875:                             tree.selection_set(row)
   L00876:                     except Exception:
   L00877:                         tree.selection_set(row)
>> L00878:             menu.tk_popup(event.x_root, event.y_root)
   L00879:         finally:
   L00880:             try:
   L00881:                 menu.grab_release()
   L00882:             except Exception:
   L00883:                 pass
   L00884: 
```
- **Treeview creation**: 3 hit(s) (showing 3)
```text
   L00260:     btn_snaps = ui_theme_classic.Button(row_actions, text="Snapshots", command=_btn_open_snapshots, width=10)
   L00261:     btn_explorer = ui_theme_classic.Button(row_actions, text="Explorer", command=_btn_open_explorer, width=10)
   L00262: 
   L00263: 
   L00264:     # Tree + Scrollbar
   L00265:     cols = ("name", "ext", "date", "time")
>> L00266:     tree = ttk.Treeview(wrap, columns=cols, show="headings", selectmode="extended")
   L00267:     vsb = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
   L00268:     tree.configure(yscrollcommand=vsb.set)
   L00269: 
   L00270:     tree.pack(side="left", fill="both", expand=True)
   L00271:     vsb.pack(side="right", fill="y")
   L00272: 
```
```text
   L00741:     except Exception:
   L00742:         pass
   L00743: 
   L00744: 
   L00745: def enable_lasso(app) -> None:
   L00746:     """
>> L00747:     Aktiviert einen einfachen Lasso-/Drag-Multiselect auf der TreeView.
   L00748: 
   L00749:     Verhalten:
   L00750:     - Linke Maustaste gedrueckt halten und ueber Eintraege fahren:
   L00751:       Eintraege werden beim Ueberfahren der Maus zur Auswahl hinzugefuegt.
   L00752:     - Bestehende Selektion bleibt erhalten (additiv).
   L00753:     """
```
```text
   L00804:     except Exception:
   L00805:         pass
   L00806: 
   L00807: 
   L00808: def enable_context_menu(app) -> None:
   L00809:     """
>> L00810:     Aktiviert ein Kontextmenue auf der TreeView (rechte Liste):
   L00811: 
   L00812:     - Rechtsklick auf einen Eintrag:
   L00813:         * Auswahl ggf. auf diesen Eintrag setzen
   L00814:         * Menue mit "Pfad(e) kopieren" anzeigen
   L00815:     - "Pfad(e) kopieren":
   L00816:         * Alle selektierten Pfade (tree_paths) werden in die Zwischenablage
```

### `ui_runner_products_tab.py`
- **BIND Button-3**: 2 hit(s) (showing 2)
```text
   L00555:             m.tk_popup(ev.x_root, ev.y_root)
   L00556:         except Exception:
   L00557:             pass
   L00558: 
   L00559:     try:
   L00560:         tree.bind("<Double-Button-1>", _tree_open_selected)
>> L00561:         tree.bind("<Button-3>", _tree_context_menu)
   L00562:         tree.bind("<Control-c>", _tree_copy_path)
   L00563:         tree.bind("<Control-Shift-C>", _tree_copy_content)
   L00564:     except Exception:
   L00565:         pass
   L00566:     # --- /R2303 TREE UX --------------------------------------------------------------
   L00567: 
```
```text
   L00646: 
   L00647:     def on_copy_content(_):
   L00648:         p = get_path_callable()
   L00649:         if p: _rp_copy_content(root, p)
   L00650: 
   L00651:     listbox.bind("<Double-Button-1>", on_dbl)
>> L00652:     listbox.bind("<Button-3>", on_menu)
   L00653:     listbox.bind("<Control-c>", on_copy)
   L00654:     listbox.bind("<Control-Shift-C>", on_copy_content)
   L00655: # --- /R2300 UX -------------------------------------------------------------------
```
- **tk.Menu usage**: 2 hit(s) (showing 2)
```text
   L00542: 
   L00543:         p = _selected_path()
   L00544:         if not p:
   L00545:             return
   L00546: 
   L00547:         try:
>> L00548:             m = tk.Menu(tree, tearoff=0)
   L00549:             m.add_command(label="Intern anzeigen", command=_on_viewer)
   L00550:             m.add_command(label="Öffnen", command=_on_open)
   L00551:             m.add_command(label="Ordner öffnen", command=_on_folder)
   L00552:             m.add_separator()
   L00553:             m.add_command(label="Pfad kopieren", command=_on_copy)
   L00554:             m.add_command(label="Inhalt kopieren (Text)", command=_on_copy_content)
```
```text
   L00629:         p = get_path_callable()
   L00630:         if p: _rp_open(p)
   L00631: 
   L00632:     def on_menu(ev):
   L00633:         p = get_path_callable()
   L00634:         if not p: return
>> L00635:         m = tk.Menu(listbox, tearoff=0)
   L00636:         m.add_command(label="Öffnen", command=lambda: _rp_open(p))
   L00637:         m.add_command(label="Ordner öffnen", command=lambda: _rp_open_folder(p))
   L00638:         m.add_separator()
   L00639:         m.add_command(label="Pfad kopieren", command=lambda: _rp_copy_path(root, p))
   L00640:         m.add_command(label="Inhalt kopieren", command=lambda: _rp_copy_content(root, p))
   L00641:         m.tk_popup(ev.x_root, ev.y_root)
```
- **tk_popup usage**: 2 hit(s) (showing 2)
```text
   L00549:             m.add_command(label="Intern anzeigen", command=_on_viewer)
   L00550:             m.add_command(label="Öffnen", command=_on_open)
   L00551:             m.add_command(label="Ordner öffnen", command=_on_folder)
   L00552:             m.add_separator()
   L00553:             m.add_command(label="Pfad kopieren", command=_on_copy)
   L00554:             m.add_command(label="Inhalt kopieren (Text)", command=_on_copy_content)
>> L00555:             m.tk_popup(ev.x_root, ev.y_root)
   L00556:         except Exception:
   L00557:             pass
   L00558: 
   L00559:     try:
   L00560:         tree.bind("<Double-Button-1>", _tree_open_selected)
   L00561:         tree.bind("<Button-3>", _tree_context_menu)
```
```text
   L00635:         m = tk.Menu(listbox, tearoff=0)
   L00636:         m.add_command(label="Öffnen", command=lambda: _rp_open(p))
   L00637:         m.add_command(label="Ordner öffnen", command=lambda: _rp_open_folder(p))
   L00638:         m.add_separator()
   L00639:         m.add_command(label="Pfad kopieren", command=lambda: _rp_copy_path(root, p))
   L00640:         m.add_command(label="Inhalt kopieren", command=lambda: _rp_copy_content(root, p))
>> L00641:         m.tk_popup(ev.x_root, ev.y_root)
   L00642: 
   L00643:     def on_copy(_):
   L00644:         p = get_path_callable()
   L00645:         if p: _rp_copy_path(root, p)
   L00646: 
   L00647:     def on_copy_content(_):
```
- **Treeview creation**: 1 hit(s) (showing 1)
```text
   L00308:     var_q = tk.StringVar(value="")
   L00309:     ent_q = tk.Entry(f, textvariable=var_q)
   L00310:     ent_q.pack(side="left", fill="x", expand=True, padx=(4, 0))
   L00311: 
   L00312:     # Tree
   L00313:     cols = ("mtime", "type", "runner", "name", "size")
>> L00314:     tree = ttk.Treeview(left, columns=cols, show="headings", height=18)
   L00315:     tree.heading("mtime", text="Zeit")
   L00316:     tree.heading("type", text="Typ")
   L00317:     tree.heading("runner", text="Runner")
   L00318:     tree.heading("name", text="Datei")
   L00319:     tree.heading("size", text="Bytes")
   L00320:     tree.column("mtime", width=150, anchor="w")
```

### `ui_theme_classic.py`
- **Treeview creation**: 2 hit(s) (showing 2)
```text
   L00028:                     foreground=FG_TEXT,
   L00029:                     padding=(8, 3))
   L00030:     style.map("TNotebook.Tab",
   L00031:               background=[("selected", "white")],
   L00032:               foreground=[("selected", "black")])
   L00033: 
>> L00034:     # Treeview
   L00035:     style.configure("Treeview",
   L00036:                     background="white",
   L00037:                     fieldbackground="white",
   L00038:                     foreground="black")
   L00039: 
   L00040: 
```
```text
   L00029:                     padding=(8, 3))
   L00030:     style.map("TNotebook.Tab",
   L00031:               background=[("selected", "white")],
   L00032:               foreground=[("selected", "black")])
   L00033: 
   L00034:     # Treeview
>> L00035:     style.configure("Treeview",
   L00036:                     background="white",
   L00037:                     fieldbackground="white",
   L00038:                     foreground="black")
   L00039: 
   L00040: 
   L00041: def Button(parent, **kw) -> tk.Button:
```

## Interpretation checklist
- If `<Button-3>` is bound in multiple places on the same widget, the last binding usually wins (unless `add='+'` is used).
- If `enable_context_menu()` binds `<Button-3>` AND `logic_actions` also binds `<Button-3>` on the Tree, we must pick ONE owner.

## Next step
- Decide owner (recommended: `ui_project_tree.enable_context_menu()`), then patch only there (R2477).
- If needed, neutralize redundant binding in the other location (R2478), minimal and reversible.
