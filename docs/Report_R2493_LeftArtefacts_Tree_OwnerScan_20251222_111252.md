# R2493 – Left Artefakte Tree Owner Scan (READ-ONLY)

- Time: 20251222_111252
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`


## logic_actions.py
- **Button-3 bind**: 1 hit(s)
```text
   L01068:             _menu.tk_popup(event.x_root, event.y_root)
   L01069:         finally:
   L01070:             try:
   L01071:                 _menu.grab_release()
   L01072:             except Exception:
   L01073:                 pass
   L01074: 
   L01075:     try:
>> L01076:         tree.bind("<Button-3>", lambda event: _on_button3(event), add="+")
   L01077:     except Exception:
   L01078:         pass
   L01079: 
   L01080: # build_tree aus ui_project_tree wrappen, damit Kontextmenue nach dem Aufbau gesetzt wird
   L01081: try:
   L01082:     from modules import ui_project_tree as _r1848_uipt  # type: ignore
   L01083:     _r1848_orig_build_tree = getattr(_r1848_uipt, "build_tree", None)
   L01084: except Exception:
```

## module_agent.py
- **Treeview**: 1 hit(s)
```text
   L00524: 
   L00525:     left = ttk.Frame(outer)
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
   L00539:     tree.pack(side="left", fill="y")
   L00540:     vs.pack(side="left", fill="y")
```

## module_docking.py
- **Artefakt keyword**: 3 hit(s)
```text
   L00533:         mapping = {}
   L00534:         try:
   L00535:             from modules import ui_pipeline_tab
   L00536:             mapping['pipeline'] = ('Pipeline', ui_pipeline_tab.build_pipeline_tab)
   L00537:         except Exception:
   L00538:             pass
   L00539:         try:
   L00540:             from modules import ui_runner_products_tab
>> L00541:             mapping['runner_products'] = ('Artefakte', ui_runner_products_tab.build_runner_products_tab)
   L00542:         except Exception:
   L00543:             pass
   L00544:         try:
   L00545:             from modules import ui_log_tab
   L00546:             mapping['log'] = ('Log', ui_log_tab.build_log_tab)
   L00547:         except Exception:
   L00548:             pass
   L00549: 
```
```text
   L00614:         targets = []
   L00615:         try:
   L00616:             from modules import ui_pipeline_tab
   L00617:             targets.append(('Pipeline', 'pipeline', ui_pipeline_tab.build_pipeline_tab))
   L00618:         except Exception:
   L00619:             pass
   L00620:         try:
   L00621:             from modules import ui_runner_products_tab
>> L00622:             targets.append(('Artefakte', 'runner_products', ui_runner_products_tab.build_runner_products_tab))
   L00623:         except Exception:
   L00624:             pass
   L00625:         try:
   L00626:             from modules import ui_log_tab
   L00627:             targets.append(('Log', 'log', ui_log_tab.build_log_tab))
   L00628:         except Exception:
   L00629:             pass
   L00630:         return targets
```
```text
   L00976: except Exception:
   L00977:     pass
   L00978: 
   L00979: 
   L00980: # ---------------------------------------------------------------------------
   L00981: # R2369_DOCKING_STATE_V2
   L00982: # Docking State v2:
   L00983: # - pro Fenster 1 Datensatz: open/docked/geometry/ts
>> L00984: # - keys: main, log, pipeline, runner_products (Artefakte)
   L00985: # - MERGE-write, Projektroot/ShrimpDev.ini
   L00986: # - Diagnose-Prints (werden im Log-Tab sichtbar)
   L00987: # ---------------------------------------------------------------------------
   L00988: def _r2369_now_iso():
   L00989:     import datetime
   L00990:     return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   L00991: 
   L00992: def _r2369_ini_path():
```
- **Button-3 bind**: 1 hit(s)
```text
   L00659:             menu.tk_popup(ev.x_root, ev.y_root)
   L00660:         finally:
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
   L00674: # R2343_HARD_INI_GEOMETRY
   L00675: 
```

## module_learningjournal_ui_ext.py
- **Treeview**: 1 hit(s)
```text
   L00085:     btn_open = ttk.Button(header, text="JSON öffnen")
   L00086:     btn_open.pack(side="right", padx=4)
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
   L00100:         "score": "Score",
   L00101:         "summary": "Zusammenfassung"
```

## module_preflight.py
- **Treeview**: 1 hit(s)
```text
   L00019:         rows.append(("tkinter", f"error: {ex}", "FAIL"))
   L00020:     for d in (ROOT/"modules", ROOT/"tools", ROOT/"Reports"):
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
   L00034:         rep = OUT / f"Preflight_{time.strftime('%Y%m%d_%H%M%S')}.txt"
   L00035:         rep.write_text("\n".join([f"{a}\t{b}\t{c}" for a, b, c in rows]), encoding="utf-8")
```

## module_runner_board.py
- **Treeview**: 1 hit(s)
```text
   L00014:             if p.suffix.lower() in {".py",".bat",".cmd"}:
   L00015:                 out.append((p.name, p.suffix.lower().lstrip(".")))
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
   L00029:     def run_sel(_evt=None):
   L00030:         sel = tree.focus()
```

## ui_lists.py
- **Treeview**: 1 hit(s)
```text
   L00001: import tkinter as tk
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
   L00015: 
   L00016: def bind_handlers(app):  # optional zukünftige Doppelklick-Aktionen
```

## ui_pipeline_tab.py
- **Treeview**: 1 hit(s)
```text
   L00064:     cols = ("status", "prio", "task", "section")
   L00065: 
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
   L00079:     tree.column("task", width=700, stretch=True, anchor="w")
   L00080:     tree.column("section", width=220, stretch=False, anchor="w")
```

## ui_project_tree.py
- **Treeview**: 2 hit(s)
```text
   L00258:     btn_tools = ui_theme_classic.Button(row_actions, text="Tools", command=_btn_open_tools, width=8)
   L00259:     btn_reports = ui_theme_classic.Button(row_actions, text="Reports", command=_btn_open_reports, width=8)
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
   L00273:     # Spalten-Setup
   L00274:     headings = {
```
```text
   L00802:         tree.bind("<B1-Motion>", _on_lasso_drag, add="+")
   L00803:         tree.bind("<ButtonRelease-1>", _on_lasso_end, add="+")
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
   L00817:           kopiert (als Zeilenliste).
   L00818:     """
```
- **Button-3 bind**: 1 hit(s)
```text
   L01089:             menu.tk_popup(event.x_root, event.y_root)
   L01090:         finally:
   L01091:             try:
   L01092:                 menu.grab_release()
   L01093:             except Exception:
   L01094:                 pass
   L01095: 
   L01096:     try:
>> L01097:         tree.bind("<Button-3>", _on_context, add="+")
   L01098:     except Exception:
   L01099:         pass
   L01100: 
```

## ui_runner_products_tab.py
- **Treeview**: 1 hit(s)
```text
   L00306: 
   L00307:     tk.Label(f, text="Suche:", bg=bg).pack(side="left")
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
   L00321:     tree.column("type", width=70, anchor="w")
   L00322:     tree.column("runner", width=70, anchor="w")
```
- **Artefakt keyword**: 1 hit(s)
```text
   L00271:         bg = None
   L00272: 
   L00273:     container = tk.Frame(parent, bg=bg)
   L00274:     container.pack(fill="both", expand=True)
   L00275: 
   L00276:     top = tk.Frame(container, bg=bg)
   L00277:     top.pack(fill="x", padx=8, pady=6)
   L00278: 
>> L00279:     tk.Label(top, text="Artefakte (Read-Only)", bg=bg).pack(side="left")
   L00280: 
   L00281:     btn_refresh = tk.Button(top, text="Refresh")
   L00282:     btn_refresh.pack(side="right")
   L00283: 
   L00284:     mid = tk.Frame(container, bg=bg)
   L00285:     mid.pack(fill="both", expand=True, padx=8, pady=(0, 8))
   L00286: 
   L00287:     # Left: list, Right: preview
```
- **Button-3 bind**: 2 hit(s)
```text
   L00553:             m.add_command(label="Pfad kopieren", command=_on_copy)
   L00554:             m.add_command(label="Inhalt kopieren (Text)", command=_on_copy_content)
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
   L00568:     def _refilter(*_a):
   L00569:         try:
```
```text
   L00644:         p = get_path_callable()
   L00645:         if p: _rp_copy_path(root, p)
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
