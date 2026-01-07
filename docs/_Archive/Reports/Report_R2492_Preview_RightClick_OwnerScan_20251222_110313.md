# R2492 – Preview Right-Click Owner Scan (READ-ONLY)

- Time: 20251222_110313
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- Scan: `modules/*.py`

## Goal
- Find who binds right-click for the *preview area* in Artefakte-Tab.
- Identify menu builder and available variables for selected artifact path.

## Hits (by file)

### `logic_actions.py`
- **BIND <Button-3>**: 1 hit(s) (showing 1)
```text
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
```
- **Menu()**: 1 hit(s) (showing 1)
```text
   L01010:     """Rechtsklick-Kontextmenue an app.tree anbinden."""
   L01011:     if _r1848_tk is None:
   L01012:         return
   L01013:     tree = getattr(app, "tree", None)
   L01014:     if tree is None:
   L01015:         return
   L01016: 
>> L01017:     menu = _r1848_tk.Menu(tree, tearoff=False)
   L01018: 
   L01019:     def _update_selection(event):
   L01020:         try:
   L01021:             row_id = tree.identify_row(event.y)
   L01022:             if row_id:
   L01023:                 tree.selection_set(row_id)
   L01024:         except Exception:
```
- **tk_popup**: 1 hit(s) (showing 1)
```text
   L01061:     menu.add_separator()
   L01062:     menu.add_command(label="Umbenennen…", command=_cmd_rename)
   L01063:     menu.add_command(label="In den Papierkorb", command=_cmd_trash)
   L01064: 
   L01065:     def _on_button3(event, _menu=menu):
   L01066:         _update_selection(event)
   L01067:         try:
>> L01068:             _menu.tk_popup(event.x_root, event.y_root)
   L01069:         finally:
   L01070:             try:
   L01071:                 _menu.grab_release()
   L01072:             except Exception:
   L01073:                 pass
   L01074: 
   L01075:     try:
```
- **Text/Canvas/Label widget**: 5 hit(s) (showing 5)
```text
   L01204: 
   L01205:         frame = _r1851_tk.Frame(win)
   L01206:         frame.pack(expand=True, fill="both")
   L01207: 
   L01208:         scrollbar = _r1851_tk.Scrollbar(frame)
   L01209:         scrollbar.pack(side="right", fill="y")
   L01210: 
>> L01211:         txt = _r1851_tk.Text(frame, wrap="word")
   L01212:         txt.pack(side="left", expand=True, fill="both")
   L01213:         txt.config(yscrollcommand=scrollbar.set)
   L01214:         scrollbar.config(command=txt.yview)
   L01215: 
   L01216:         if _r1851_font is not None:
   L01217:             try:
   L01218:                 mono = _r1851_font.Font(family="Courier New", size=10)
```
```text
   L01457: 
   L01458:         frame = _r1852_tk.Frame(win)
   L01459:         frame.pack(expand=True, fill="both")
   L01460: 
   L01461:         scrollbar = _r1852_tk.Scrollbar(frame)
   L01462:         scrollbar.pack(side="right", fill="y")
   L01463: 
>> L01464:         txt = _r1852_tk.Text(frame, wrap="word")
   L01465:         txt.pack(side="left", expand=True, fill="both")
   L01466:         txt.config(yscrollcommand=scrollbar.set)
   L01467:         scrollbar.config(command=txt.yview)
   L01468: 
   L01469:         if _r1852_font is not None:
   L01470:             try:
   L01471:                 mono = _r1852_font.Font(family="Courier New", size=10)
```
```text
   L02334: #         return
   L02335: #     try:
   L02336: #         win = _r1846_tk.Toplevel()
   L02337: #         win.title(title)
   L02338: #         win.geometry("700x600")
   L02339: #         win.grab_set()
   L02340: # 
>> L02341: #         txt = _r1846_tk.Text(win, wrap="word")
   L02342: #         txt.pack(expand=True, fill="both")
   L02343: #         txt.insert("1.0", text)
   L02344: #         txt.config(state="disabled")
   L02345: # 
   L02346: #         btn = _r1846_tk.Button(win, text="Schließen", command=win.destroy)
   L02347: #         btn.pack(pady=8)
   L02348: # 
```
```text
   L02442: # 
   L02443: #         frame = _r1847_tk.Frame(win)
   L02444: #         frame.pack(expand=True, fill="both")
   L02445: # 
   L02446: #         scrollbar = _r1847_tk.Scrollbar(frame)
   L02447: #         scrollbar.pack(side="right", fill="y")
   L02448: # 
>> L02449: #         txt = _r1847_tk.Text(frame, wrap="word")
   L02450: #         txt.pack(side="left", expand=True, fill="both")
   L02451: #         txt.config(yscrollcommand=scrollbar.set)
   L02452: #         scrollbar.config(command=txt.yview)
   L02453: # 
   L02454: #         txt.insert("1.0", text or "(keine Ausgabe)")
   L02455: #         txt.config(state="disabled")
   L02456: # 
```
```text
   L02599: # 
   L02600: #         frame = _r1849_tk.Frame(win)
   L02601: #         frame.pack(expand=True, fill="both")
   L02602: # 
   L02603: #         scrollbar = _r1849_tk.Scrollbar(frame)
   L02604: #         scrollbar.pack(side="right", fill="y")
   L02605: # 
>> L02606: #         txt = _r1849_tk.Text(frame, wrap="word")
   L02607: #         txt.pack(side="left", expand=True, fill="both")
   L02608: #         txt.config(yscrollcommand=scrollbar.set)
   L02609: #         scrollbar.config(command=txt.yview)
   L02610: # 
   L02611: #         if _r1849_font is not None:
   L02612: #             try:
   L02613: #                 mono = _r1849_font.Font(family="Courier New", size=10)
```

### `logic_intake.py`
- **Text/Canvas/Label widget**: 2 hit(s) (showing 2)
```text
   L00001: from tkinter import messagebox
   L00002: import tkinter as tk
   L00003: 
   L00004: def build_intake_tab(parent, app):
   L00005:     frm = tk.Frame(parent); frm.pack(fill="both", expand=True, padx=12, pady=12)
>> L00006:     tk.Label(frm, text="ShrimpDev Intake").pack(anchor="w")
   L00007:     tk.Label(frm, text="Ziel: Code/Module/Runner verarbeiten - kein ShrimpHub-Flow.").pack(anchor="w", pady=(2,8))
   L00008: 
   L00009: def do_scan(app):
   L00010:     messagebox.showinfo("Scan Project", "Projekt wird gescannt... (Demo)")
   L00011: 
   L00012: # Platzhalter für spätere Dev-Tasks
```
```text
   L00001: from tkinter import messagebox
   L00002: import tkinter as tk
   L00003: 
   L00004: def build_intake_tab(parent, app):
   L00005:     frm = tk.Frame(parent); frm.pack(fill="both", expand=True, padx=12, pady=12)
   L00006:     tk.Label(frm, text="ShrimpDev Intake").pack(anchor="w")
>> L00007:     tk.Label(frm, text="Ziel: Code/Module/Runner verarbeiten - kein ShrimpHub-Flow.").pack(anchor="w", pady=(2,8))
   L00008: 
   L00009: def do_scan(app):
   L00010:     messagebox.showinfo("Scan Project", "Projekt wird gescannt... (Demo)")
   L00011: 
   L00012: # Platzhalter für spätere Dev-Tasks
```

### `module_agent.py`
- **Text/Canvas/Label widget**: 2 hit(s) (showing 2)
```text
   L00512: 
   L00513: def build_agent_tab(parent, app):
   L00514:     # AGENT_UI_CLICKABLE_R2173
   L00515:     import tkinter as tk
   L00516:     import tkinter.ttk as ttk
   L00517:     import tkinter.messagebox as mb
   L00518: 
>> L00519:     header = ttk.Label(parent, text="Agent", anchor="w")
   L00520:     header.pack(fill="x", padx=10, pady=(10, 6))
   L00521: 
   L00522:     outer = ttk.Frame(parent)
   L00523:     outer.pack(fill="both", expand=True, padx=10, pady=(0, 8))
   L00524: 
   L00525:     left = ttk.Frame(outer)
   L00526:     left.pack(side="left", fill="y")
```
```text
   L00537:     vs = ttk.Scrollbar(left, orient="vertical", command=tree.yview)
   L00538:     tree.configure(yscrollcommand=vs.set)
   L00539:     tree.pack(side="left", fill="y")
   L00540:     vs.pack(side="left", fill="y")
   L00541: 
   L00542:     scr = ttk.Scrollbar(right, orient="vertical")
   L00543:     scr.pack(side="right", fill="y")
>> L00544:     txtw = tk.Text(right, wrap="word", yscrollcommand=scr.set)
   L00545:     txtw.pack(side="left", fill="both", expand=True)
   L00546:     scr.config(command=txtw.yview)
   L00547:     try:
   L00548:         txtw.config(state="disabled")
   L00549:     except Exception:
   L00550:         pass
   L00551: 
```

### `module_agent_ui.py`
- **Text/Canvas/Label widget**: 1 hit(s) (showing 1)
```text
   L00006: 
   L00007: import tkinter as tk
   L00008: from tkinter import ttk
   L00009: 
   L00010: class AgentFrame(ttk.Frame):
   L00011:     def __init__(self, parent):
   L00012:         super().__init__(parent)
>> L00013:         ttk.Label(self, text="Agent").pack(anchor="w", padx=8, pady=8)
```

### `module_docking.py`
- **BIND <Button-3>**: 1 hit(s) (showing 1)
```text
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
```
- **Menu()**: 1 hit(s) (showing 1)
```text
   L00647:             if label == tab_text:
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
   L00661:             try:
```
- **tk_popup**: 1 hit(s) (showing 1)
```text
   L00652: 
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
   L00666:     try:
```
- **Artifacts keyword**: 3 hit(s) (showing 3)
```text
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
```
```text
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
```
```text
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
```
- **Text/Canvas/Label widget**: 2 hit(s) (showing 2)
```text
   L00382: 
   L00383:         outer = tk.Frame(w)
   L00384:         outer.pack(fill='both', expand=True)
   L00385: 
   L00386:         # Mini-Header
   L00387:         hdr = tk.Frame(outer)
   L00388:         hdr.pack(fill='x', padx=6, pady=6)
>> L00389:         tk.Label(hdr, text=self._safe_title(title), anchor='w').pack(side='left')
   L00390:                 # R2342_FORCE_PERSIST_ON_CLOSE
   L00391:         def _request_close():
   L00392:             try:
   L00393:                 # persist THIS window right now (geometry + keys)
   L00394:                 if hasattr(self, '_persist_one'):
   L00395:                     self._persist_one(key, w)
   L00396:             except Exception:
```
```text
   L00407:         body.pack(fill='both', expand=True, padx=6, pady=(0, 6))
   L00408: 
   L00409:         # Build content fresh (read-only viewers)
   L00410:         try:
   L00411:             builder_func(body, self.app)
   L00412:         except Exception as exc:
   L00413:             try:
>> L00414:                 tk.Label(body, text='Undock-Fehler: ' + repr(exc), anchor='w').pack(anchor='w', padx=8, pady=8)
   L00415:             except Exception:
   L00416:                 pass
   L00417: 
   L00418:         def _on_close():
   L00419:             _request_close()
   L00420: 
   L00421:         try:
```

### `module_learningjournal.py`
- **Text/Canvas/Label widget**: 8 hit(s) (showing 8)
```text
   L00308:     header.grid(row=0, column=0, sticky='ew', padx=8, pady=(8, 4))
   L00309:     header.columnconfigure(0, weight=0)
   L00310:     header.columnconfigure(1, weight=0)
   L00311:     header.columnconfigure(2, weight=1)
   L00312:     header.columnconfigure(3, weight=0)
   L00313:     header.columnconfigure(4, weight=0)
   L00314: 
>> L00315:     lbl_title = ttk.Label(header, text='LearningJournal')
   L00316:     lbl_title.grid(row=0, column=0, sticky='w')
   L00317: 
   L00318:     btn_reload = ttk.Button(header, text='Neu laden')
   L00319:     btn_reload.grid(row=0, column=3, sticky='e', padx=(4, 0))
   L00320: 
   L00321:     btn_diag = ttk.Button(header, text='Diagnose (R1802)')
   L00322:     btn_diag.grid(row=0, column=4, sticky='e', padx=(4, 0))
```
```text
   L00318:     btn_reload = ttk.Button(header, text='Neu laden')
   L00319:     btn_reload.grid(row=0, column=3, sticky='e', padx=(4, 0))
   L00320: 
   L00321:     btn_diag = ttk.Button(header, text='Diagnose (R1802)')
   L00322:     btn_diag.grid(row=0, column=4, sticky='e', padx=(4, 0))
   L00323: 
   L00324:     info_var = tk.StringVar(value='')
>> L00325:     lbl_info = ttk.Label(header, textvariable=info_var, anchor='w')
   L00326:     lbl_info.grid(row=1, column=0, columnspan=5, sticky='w', pady=(4, 0))
   L00327: 
   L00328:     stats_var = tk.StringVar(value='')
   L00329:     lbl_stats = ttk.Label(header, textvariable=stats_var, anchor='w')
   L00330:     lbl_stats.grid(row=2, column=0, columnspan=5, sticky='w', pady=(2, 0))
   L00331: 
   L00332:     filter_var = tk.StringVar(value='alle')
```
```text
   L00322:     btn_diag.grid(row=0, column=4, sticky='e', padx=(4, 0))
   L00323: 
   L00324:     info_var = tk.StringVar(value='')
   L00325:     lbl_info = ttk.Label(header, textvariable=info_var, anchor='w')
   L00326:     lbl_info.grid(row=1, column=0, columnspan=5, sticky='w', pady=(4, 0))
   L00327: 
   L00328:     stats_var = tk.StringVar(value='')
>> L00329:     lbl_stats = ttk.Label(header, textvariable=stats_var, anchor='w')
   L00330:     lbl_stats.grid(row=2, column=0, columnspan=5, sticky='w', pady=(2, 0))
   L00331: 
   L00332:     filter_var = tk.StringVar(value='alle')
   L00333:     search_var = tk.StringVar(value='')
   L00334: 
   L00335:     lbl_filter = ttk.Label(header, text='Filter:')
   L00336:     lbl_filter.grid(row=3, column=0, sticky='w', pady=(4, 0))
```
```text
   L00328:     stats_var = tk.StringVar(value='')
   L00329:     lbl_stats = ttk.Label(header, textvariable=stats_var, anchor='w')
   L00330:     lbl_stats.grid(row=2, column=0, columnspan=5, sticky='w', pady=(2, 0))
   L00331: 
   L00332:     filter_var = tk.StringVar(value='alle')
   L00333:     search_var = tk.StringVar(value='')
   L00334: 
>> L00335:     lbl_filter = ttk.Label(header, text='Filter:')
   L00336:     lbl_filter.grid(row=3, column=0, sticky='w', pady=(4, 0))
   L00337: 
   L00338:     combo_filter = ttk.Combobox(
   L00339:         header,
   L00340:         textvariable=filter_var,
   L00341:         state='readonly',
   L00342:         values=['alle', 'error', 'runner', 'intake', 'meta'],
```
```text
   L00339:         header,
   L00340:         textvariable=filter_var,
   L00341:         state='readonly',
   L00342:         values=['alle', 'error', 'runner', 'intake', 'meta'],
   L00343:     )
   L00344:     combo_filter.grid(row=3, column=1, sticky='w', pady=(4, 0))
   L00345: 
>> L00346:     lbl_search = ttk.Label(header, text='Suche:')
   L00347:     lbl_search.grid(row=3, column=2, sticky='e', pady=(4, 0))
   L00348: 
   L00349:     entry_search = ttk.Entry(header, textvariable=search_var)
   L00350:     entry_search.grid(row=3, column=3, sticky='ew', pady=(4, 0))
   L00351: 
   L00352:     btn_reset = ttk.Button(header, text='Reset')
   L00353:     btn_reset.grid(row=3, column=4, sticky='e', padx=(4, 0), pady=(4, 0))
```
```text
   L00356: 
   L00357:     paned = ttk.Panedwindow(parent, orient='horizontal')
   L00358:     paned.grid(row=1, column=0, sticky='nsew', padx=8, pady=(4, 8))
   L00359: 
   L00360:     frame_left = ttk.Frame(paned)
   L00361:     paned.add(frame_left, weight=1)
   L00362: 
>> L00363:     lbl_list = ttk.Label(frame_left, text='Eintraege')
   L00364:     lbl_list.pack(anchor='w')
   L00365: 
   L00366:     listbox = tk.Listbox(frame_left, exportselection=False, height=20)
   L00367:     listbox.pack(side='left', fill='both', expand=True, pady=(2, 0))
   L00368: 
   L00369:     scroll_list = ttk.Scrollbar(frame_left, orient='vertical', command=listbox.yview)
   L00370:     scroll_list.pack(side='right', fill='y')
```
```text
   L00369:     scroll_list = ttk.Scrollbar(frame_left, orient='vertical', command=listbox.yview)
   L00370:     scroll_list.pack(side='right', fill='y')
   L00371:     listbox.configure(yscrollcommand=scroll_list.set)
   L00372: 
   L00373:     frame_right = ttk.Frame(paned)
   L00374:     paned.add(frame_right, weight=3)
   L00375: 
>> L00376:     lbl_detail = ttk.Label(frame_right, text='Details / JSON')
   L00377:     lbl_detail.pack(anchor='w')
   L00378: 
   L00379:     text_detail = tk.Text(frame_right, wrap='word', height=20)
   L00380:     text_detail.pack(side='left', fill='both', expand=True, pady=(2, 0))
   L00381: 
   L00382:     scroll_detail = ttk.Scrollbar(frame_right, orient='vertical', command=text_detail.yview)
   L00383:     scroll_detail.pack(side='right', fill='y')
```
```text
   L00372: 
   L00373:     frame_right = ttk.Frame(paned)
   L00374:     paned.add(frame_right, weight=3)
   L00375: 
   L00376:     lbl_detail = ttk.Label(frame_right, text='Details / JSON')
   L00377:     lbl_detail.pack(anchor='w')
   L00378: 
>> L00379:     text_detail = tk.Text(frame_right, wrap='word', height=20)
   L00380:     text_detail.pack(side='left', fill='both', expand=True, pady=(2, 0))
   L00381: 
   L00382:     scroll_detail = ttk.Scrollbar(frame_right, orient='vertical', command=text_detail.yview)
   L00383:     scroll_detail.pack(side='right', fill='y')
   L00384:     text_detail.configure(yscrollcommand=scroll_detail.set)
   L00385: 
   L00386:     state = {
```

### `module_learningjournal_ui_ext.py`
- **Text/Canvas/Label widget**: 3 hit(s) (showing 3)
```text
   L00073: 
   L00074:     frame = ttk.Frame(parent)
   L00075: 
   L00076:     # Header
   L00077:     header = ttk.Frame(frame)
   L00078:     header.pack(side="top", fill="x", padx=8, pady=6)
   L00079: 
>> L00080:     ttk.Label(header, text="LearningJournal - Phase B Analyse", font=("", 11, "bold")).pack(side="left")
   L00081: 
   L00082:     btn_reload = ttk.Button(header, text="Neu laden")
   L00083:     btn_reload.pack(side="right", padx=4)
   L00084: 
   L00085:     btn_open = ttk.Button(header, text="JSON öffnen")
   L00086:     btn_open.pack(side="right", padx=4)
   L00087: 
```
```text
   L00081: 
   L00082:     btn_reload = ttk.Button(header, text="Neu laden")
   L00083:     btn_reload.pack(side="right", padx=4)
   L00084: 
   L00085:     btn_open = ttk.Button(header, text="JSON öffnen")
   L00086:     btn_open.pack(side="right", padx=4)
   L00087: 
>> L00088:     lbl_path = ttk.Label(frame, text="Datei: {}".format(get_learning_journal_path(root_dir)))
   L00089:     lbl_path.pack(side="top", anchor="w", padx=8)
   L00090: 
   L00091:     # Tree
   L00092:     columns = ("id", "timestamp", "category", "score", "summary")
   L00093:     tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
   L00094:     tree.pack(side="top", fill="both", expand=True, padx=8, pady=4)
   L00095: 
```
```text
   L00112:     for col in columns:
   L00113:         tree.heading(col, text=headers[col])
   L00114:         tree.column(col, width=widths[col], anchor="w")
   L00115: 
   L00116:     footer = ttk.Frame(frame)
   L00117:     footer.pack(side="bottom", fill="x", padx=8, pady=6)
   L00118: 
>> L00119:     lbl_summary = ttk.Label(footer, text="Keine Phase-B-Daten geladen.")
   L00120:     lbl_summary.pack(side="left")
   L00121: 
   L00122:     def refresh():
   L00123:         data = load_learning_journal(root_dir)
   L00124:         entries = extract_phase_b_entries(data)
   L00125:         count, avg = summarize_phase_b(entries)
   L00126: 
```

### `module_patch_release.py`
- **Text/Canvas/Label widget**: 1 hit(s) (showing 1)
```text
   L00013:     rel = p.relative_to(ROOT).as_posix()
   L00014:     if rel.startswith("_Reports/") or rel.startswith("_Exports/") or rel.startswith("dist/"): return False
   L00015:     if "/__pycache__/" in rel: return False
   L00016:     return True
   L00017: 
   L00018: def _build_tab(parent):
   L00019:     frm = ttk.Frame(parent)
>> L00020:     ttk.Label(frm, text="Erstellt ein ZIP der aktuellen ShrimpDev-Struktur.").pack(anchor="w", padx=10, pady=8)
   L00021:     def build():
   L00022:         name = f"ShrimpDev_patch_{time.strftime('%Y%m%d_%H%M%S')}.zip"
   L00023:         target = OUT / name
   L00024:         with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as z:
   L00025:             for p in ROOT.rglob("*"):
   L00026:                 if p.is_file() and _include(p):
   L00027:                     z.write(p, p.relative_to(ROOT))
```

### `module_project_ui.py`
- **Text/Canvas/Label widget**: 1 hit(s) (showing 1)
```text
   L00001: import tkinter as tk
   L00002: from tkinter import ttk
   L00003: 
   L00004: class ProjectFrame(ttk.Frame):
   L00005:     def __init__(self, parent):
   L00006:         super().__init__(parent)
>> L00007:         ttk.Label(self, text="Project").pack(anchor="w", padx=8, pady=8)
```

### `module_runner_popup.py`
- **Text/Canvas/Label widget**: 2 hit(s) (showing 2)
```text
   L00197: 
   L00198:         outer = ttk.Frame(win, padding=8)
   L00199:         outer.pack(fill="both", expand=True)
   L00200: 
   L00201:         # TOP: Status links (wie gewünscht)
   L00202:         top = ttk.Frame(outer)
   L00203:         top.pack(fill="x")
>> L00204:         lbl_status = ttk.Label(top, text="RUNNING")
   L00205:         lbl_status.pack(side="left")
   L00206: 
   L00207:         # MID: Text + Scroll
   L00208:         mid = ttk.Frame(outer)
   L00209:         mid.pack(fill="both", expand=True, pady=(8, 0))
   L00210: 
   L00211:         yscroll = ttk.Scrollbar(mid, orient="vertical")
```
```text
   L00207:         # MID: Text + Scroll
   L00208:         mid = ttk.Frame(outer)
   L00209:         mid.pack(fill="both", expand=True, pady=(8, 0))
   L00210: 
   L00211:         yscroll = ttk.Scrollbar(mid, orient="vertical")
   L00212:         yscroll.pack(side="right", fill="y")
   L00213: 
>> L00214:         txt = tk.Text(mid, wrap="word", yscrollcommand=yscroll.set)
   L00215:         txt.pack(side="left", fill="both", expand=True)
   L00216:         yscroll.configure(command=txt.yview)
   L00217:         txt.configure(state="disabled")
   L00218: 
   L00219:         var_auto = tk.BooleanVar(value=True)
   L00220: 
   L00221:         # Buttons / Clipboard
```

### `module_runnerbar.py`
- **Text/Canvas/Label widget**: 1 hit(s) (showing 1)
```text
   L00051:         if cmd.exists():
   L00052:             b = ttk.Button(bar, text=label, command=lambda p=cmd: _run_cmd(p))
   L00053:             b.grid(row=0, column=c, padx=(0,6), pady=4, sticky="w")
   L00054:             c += 1
   L00055: 
   L00056:     # wenn nichts existiert, trotzdem einen Hinweis anzeigen
   L00057:     if c == 0:
>> L00058:         lab = ttk.Label(bar, text="Keine Runner gefunden (tools\\*.cmd).",
   L00059:                         foreground="#888")
   L00060:         lab.grid(row=0, column=0, padx=0, pady=4, sticky="w")
   L00061:     return bar
```

### `module_settings_ui.py`
- **Text/Canvas/Label widget**: 1 hit(s) (showing 1)
```text
   L00015: def _save(conf: dict):
   L00016:     try: CFG.write_text(json.dumps(conf, ensure_ascii=False, indent=2), encoding="utf-8")
   L00017:     except Exception: pass
   L00018: 
   L00019: def _build_tab(parent):
   L00020:     frm = ttk.Frame(parent)
   L00021:     conf = _load()
>> L00022:     ttk.Label(frm, text="Workspace Root:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
   L00023:     var_ws = tk.StringVar(value=conf.get("workspace_root", r"D:\ShrimpHub"))
   L00024:     ttk.Entry(frm, textvariable=var_ws, width=46).grid(row=0, column=1, sticky="we", padx=6, pady=10)
   L00025:     def _pick():
   L00026:         d = filedialog.askdirectory(title="Workspace wählen", initialdir=str(Path(var_ws.get() or r"D:\\")))
   L00027:         if d: var_ws.set(d)
   L00028:     ttk.Button(frm, text="...", command=_pick).grid(row=0, column=2)
   L00029:     var_quiet = tk.BooleanVar(value=bool(conf.get("quiet_mode", True)))
```

### `ui_learningpanel.py`
- **Text/Canvas/Label widget**: 2 hit(s) (showing 2)
```text
   L00027:     tk.Frame
   L00028:         Das erzeugte Frame mit Titel- und Info-Text.
   L00029:     """
   L00030:     frame = ttk.Frame(parent)
   L00031:     frame.grid_rowconfigure(1, weight=1)
   L00032:     frame.grid_columnconfigure(0, weight=1)
   L00033: 
>> L00034:     lbl_title = ttk.Label(
   L00035:         frame,
   L00036:         text="LearningEngine - Uebersicht",
   L00037:         anchor="w",
   L00038:     )
   L00039:     lbl_title.grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 4))
   L00040: 
   L00041:     info_text = (
```
```text
   L00042:         "Dies ist das Learning-System von ShrimpDev.\n"
   L00043:         "Hier koennen kuenftig Journal, Engine-Status und Vorschlaege "
   L00044:         "angezeigt werden.\n"
   L00045:         "In Phase C dient dieses Panel als einfache Uebersicht und "
   L00046:         "Platzhalter fuer kuenftige Erweiterungen."
   L00047:     )
   L00048: 
>> L00049:     lbl_info = ttk.Label(
   L00050:         frame,
   L00051:         text=info_text,
   L00052:         justify="left",
   L00053:         anchor="nw",
   L00054:     )
   L00055:     lbl_info.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
   L00056: 
```

### `ui_leds.py`
- **Text/Canvas/Label widget**: 2 hit(s) (showing 2)
```text
   L00034:         self._add("target", "Zielpfad", GREY)
   L00035:         self._add("aot", "AOT", GREY)
   L00036: 
   L00037:     def _add(self, key: str, label: str, color: str) -> None:
   L00038:         holder = tk.Frame(self.frame, bg=BG)
   L00039:         holder.pack(side="left", padx=10)
   L00040: 
>> L00041:         canvas = tk.Canvas(holder, width=18, height=18, bg=BG, highlightthickness=0)
   L00042:         canvas.pack(side="top")
   L00043:         canvas.create_oval(2, 2, 16, 16, fill=color, outline="#333333", width=1)
   L00044: 
   L00045:         tk.Label(holder, text=label, bg=BG).pack(side="top")
   L00046:         self._items[key] = canvas
   L00047: 
   L00048:         # Klick-Handler, falls ein Callback fuer diese LED registriert ist
```
```text
   L00038:         holder = tk.Frame(self.frame, bg=BG)
   L00039:         holder.pack(side="left", padx=10)
   L00040: 
   L00041:         canvas = tk.Canvas(holder, width=18, height=18, bg=BG, highlightthickness=0)
   L00042:         canvas.pack(side="top")
   L00043:         canvas.create_oval(2, 2, 16, 16, fill=color, outline="#333333", width=1)
   L00044: 
>> L00045:         tk.Label(holder, text=label, bg=BG).pack(side="top")
   L00046:         self._items[key] = canvas
   L00047: 
   L00048:         # Klick-Handler, falls ein Callback fuer diese LED registriert ist
   L00049:         if hasattr(self, "_callbacks") and key in self._callbacks:
   L00050:             def _on_click(_event, k=key):
   L00051:                 cb = self._callbacks.get(k)
   L00052:                 if callable(cb):
```

### `ui_left_panel.py`
- **Preview keyword**: 6 hit(s) (showing 6)
```text
   L00127: def build_left_panel(parent, app) -> tk.Frame:
   L00128:     """
   L00129:     Linker Bereich: Intake-Editor + Metadaten.
   L00130: 
   L00131:     Elemente:
   L00132:     - Zeile fuer Dateiname + Endung (mit Punkt dazwischen)
   L00133:     - Zeile fuer Zielordner (+ "..." Browse-Button)
>> L00134:     - Zeile fuer Pfad-Vorschau
   L00135:     - Intake-LED (Platzhalter, wird spaeter von Logik versorgt)
   L00136:     - ScrolledText fuer Code
   L00137:     """
   L00138:     bg = ui_theme_classic.BG_MAIN
   L00139:     wrap = tk.Frame(parent, bg=bg)
   L00140: 
   L00141:     # StringVars anlegen / wiederverwenden
```
```text
   L00207:         command=lambda: _browse_target(app, var_target_dir),
   L00208:     )
   L00209:     btn_browse.pack(side="left", padx=(2, 0))
   L00210: 
   L00211:     app.entry_target_dir = entry_target
   L00212:     app.button_target_browse = btn_browse
   L00213: 
>> L00214:     # --- Zeile: Pfad-Vorschau + LED ---------------------------------------
   L00215:     row_info = tk.Frame(wrap, bg=bg)
   L00216:     row_info.pack(fill="x", padx=4, pady=(0, 4))
   L00217: 
   L00218:     tk.Label(row_info, text="Pfad:", bg=bg).pack(side="left", padx=2, pady=2)
   L00219: 
   L00220:     lbl_path = tk.Label(row_info, textvariable=var_path_preview, bg=bg, anchor="w")
   L00221:     lbl_path.pack(side="left", padx=(4, 8), fill="x", expand=True)
```
```text
   L00236: 
   L00237:         if ext and not ext.startswith("."):
   L00238:             ext_show = "." + ext
   L00239:         else:
   L00240:             ext_show = ext
   L00241: 
   L00242:         if not name:
>> L00243:             preview = ""
   L00244:         else:
   L00245:             filename = f"{name}{ext_show}"
   L00246:             if target:
   L00247:                 preview = f"{target}\\{filename}"
   L00248:             else:
   L00249:                 preview = filename
   L00250: 
```
```text
   L00240:             ext_show = ext
   L00241: 
   L00242:         if not name:
   L00243:             preview = ""
   L00244:         else:
   L00245:             filename = f"{name}{ext_show}"
   L00246:             if target:
>> L00247:                 preview = f"{target}\\{filename}"
   L00248:             else:
   L00249:                 preview = filename
   L00250: 
   L00251:         var_path_preview.set(preview)
   L00252: 
   L00253:     # Traces fuer automatische Aktualisierung
   L00254:     def _safe_led_eval():
```
```text
   L00242:         if not name:
   L00243:             preview = ""
   L00244:         else:
   L00245:             filename = f"{name}{ext_show}"
   L00246:             if target:
   L00247:                 preview = f"{target}\\{filename}"
   L00248:             else:
>> L00249:                 preview = filename
   L00250: 
   L00251:         var_path_preview.set(preview)
   L00252: 
   L00253:     # Traces fuer automatische Aktualisierung
   L00254:     def _safe_led_eval():
   L00255:         """Sichere LED-Aktualisierung fuer den Intake-Tab."""
   L00256:         try:
```
```text
   L00244:         else:
   L00245:             filename = f"{name}{ext_show}"
   L00246:             if target:
   L00247:                 preview = f"{target}\\{filename}"
   L00248:             else:
   L00249:                 preview = filename
   L00250: 
>> L00251:         var_path_preview.set(preview)
   L00252: 
   L00253:     # Traces fuer automatische Aktualisierung
   L00254:     def _safe_led_eval():
   L00255:         """Sichere LED-Aktualisierung fuer den Intake-Tab."""
   L00256:         try:
   L00257:             ui_leds.evaluate(app)
   L00258:         except Exception:
```
- **Text/Canvas/Label widget**: 7 hit(s) (showing 7)
```text
   L00173: 
   L00174:     var_path_preview = _ensure_stringvar(app, "var_path_preview")
   L00175: 
   L00176:     # --- Zeile: Dateiname + Endung ----------------------------------------
   L00177:     row_name = tk.Frame(wrap, bg=bg)
   L00178:     row_name.pack(fill="x", padx=4, pady=(4, 2))
   L00179: 
>> L00180:     tk.Label(row_name, text="Datei:", bg=bg).pack(side="left", padx=2, pady=2)
   L00181: 
   L00182:     entry_name = ui_theme_classic.Entry(row_name, textvariable=var_name, width=32)
   L00183:     entry_name.pack(side="left", padx=(4, 2))
   L00184: 
   L00185:     tk.Label(row_name, text=".", bg=bg).pack(side="left", padx=2, pady=2)
   L00186: 
   L00187:     entry_ext = ui_theme_classic.Entry(row_name, textvariable=var_ext, width=8)
```
```text
   L00178:     row_name.pack(fill="x", padx=4, pady=(4, 2))
   L00179: 
   L00180:     tk.Label(row_name, text="Datei:", bg=bg).pack(side="left", padx=2, pady=2)
   L00181: 
   L00182:     entry_name = ui_theme_classic.Entry(row_name, textvariable=var_name, width=32)
   L00183:     entry_name.pack(side="left", padx=(4, 2))
   L00184: 
>> L00185:     tk.Label(row_name, text=".", bg=bg).pack(side="left", padx=2, pady=2)
   L00186: 
   L00187:     entry_ext = ui_theme_classic.Entry(row_name, textvariable=var_ext, width=8)
   L00188:     entry_ext.pack(side="left", padx=(2, 4))
   L00189: 
   L00190:     # Referenzen am App-Objekt bereitstellen (Kompatibilitaet fuer logic_actions)
   L00191:     app.entry_name = entry_name
   L00192:     app.entry_ext = entry_ext
```
```text
   L00191:     app.entry_name = entry_name
   L00192:     app.entry_ext = entry_ext
   L00193: 
   L00194:     # --- Zeile: Zielordner (+ Browse-Button) ------------------------------
   L00195:     row_target = tk.Frame(wrap, bg=bg)
   L00196:     row_target.pack(fill="x", padx=4, pady=(0, 2))
   L00197: 
>> L00198:     tk.Label(row_target, text="Zielordner:", bg=bg).pack(side="left", padx=2, pady=2)
   L00199: 
   L00200:     entry_target = ui_theme_classic.Entry(row_target, textvariable=var_target_dir, width=40)
   L00201:     entry_target.pack(side="left", padx=(4, 2), fill="x", expand=True)
   L00202: 
   L00203:     btn_browse = ui_theme_classic.Button(
   L00204:         row_target,
   L00205:         text="...",
```
```text
   L00211:     app.entry_target_dir = entry_target
   L00212:     app.button_target_browse = btn_browse
   L00213: 
   L00214:     # --- Zeile: Pfad-Vorschau + LED ---------------------------------------
   L00215:     row_info = tk.Frame(wrap, bg=bg)
   L00216:     row_info.pack(fill="x", padx=4, pady=(0, 4))
   L00217: 
>> L00218:     tk.Label(row_info, text="Pfad:", bg=bg).pack(side="left", padx=2, pady=2)
   L00219: 
   L00220:     lbl_path = tk.Label(row_info, textvariable=var_path_preview, bg=bg, anchor="w")
   L00221:     lbl_path.pack(side="left", padx=(4, 8), fill="x", expand=True)
   L00222: 
   L00223:     # Intake-LED (Platzhalter: grau = unbekannt)
   L00224:     led = tk.Canvas(row_info, width=14, height=14, highlightthickness=0, bg=bg)
   L00225:     led.pack(side="right", padx=(4, 0))
```
```text
   L00213: 
   L00214:     # --- Zeile: Pfad-Vorschau + LED ---------------------------------------
   L00215:     row_info = tk.Frame(wrap, bg=bg)
   L00216:     row_info.pack(fill="x", padx=4, pady=(0, 4))
   L00217: 
   L00218:     tk.Label(row_info, text="Pfad:", bg=bg).pack(side="left", padx=2, pady=2)
   L00219: 
>> L00220:     lbl_path = tk.Label(row_info, textvariable=var_path_preview, bg=bg, anchor="w")
   L00221:     lbl_path.pack(side="left", padx=(4, 8), fill="x", expand=True)
   L00222: 
   L00223:     # Intake-LED (Platzhalter: grau = unbekannt)
   L00224:     led = tk.Canvas(row_info, width=14, height=14, highlightthickness=0, bg=bg)
   L00225:     led.pack(side="right", padx=(4, 0))
   L00226:     led_id = led.create_oval(2, 2, 12, 12, fill="#666666", outline="#444444")
   L00227: 
```
```text
   L00217: 
   L00218:     tk.Label(row_info, text="Pfad:", bg=bg).pack(side="left", padx=2, pady=2)
   L00219: 
   L00220:     lbl_path = tk.Label(row_info, textvariable=var_path_preview, bg=bg, anchor="w")
   L00221:     lbl_path.pack(side="left", padx=(4, 8), fill="x", expand=True)
   L00222: 
   L00223:     # Intake-LED (Platzhalter: grau = unbekannt)
>> L00224:     led = tk.Canvas(row_info, width=14, height=14, highlightthickness=0, bg=bg)
   L00225:     led.pack(side="right", padx=(4, 0))
   L00226:     led_id = led.create_oval(2, 2, 12, 12, fill="#666666", outline="#444444")
   L00227: 
   L00228:     app.intake_led = led
   L00229:     app.intake_led_id = led_id
   L00230: 
   L00231:     def _update_preview(*_args):
```
```text
   L00298:     var_name.trace_add("write", _on_target_changed)
   L00299:     var_ext.trace_add("write", _on_target_changed)
   L00300:     var_target_dir.trace_add("write", _on_target_changed)
   L00301: 
   L00302:     _update_preview()
   L00303:     _safe_led_eval()
   L00304:     # --- ScrolledText fuer Code -------------------------------------------
>> L00305:     app.txt_intake = ScrolledText(wrap, undo=True, font=("Consolas", 10))
   L00306:     def _on_code_change(_event=None):
   L00307:         _safe_led_eval()
   L00308: 
   L00309:     app.txt_intake.bind("<KeyRelease>", _on_code_change)
   L00310: 
   L00311:     app.txt_intake.pack(fill="both", expand=True, padx=4, pady=(0, 4))
   L00312: 
```

### `ui_log_tab.py`
- **Text/Canvas/Label widget**: 1 hit(s) (showing 1)
```text
   L00119:     outer = ui_theme_classic.Frame(parent, bg=BG)
   L00120:     outer.pack(fill="both", expand=True)
   L00121: 
   L00122:     # Log-Anzeige
   L00123:     area = ui_theme_classic.Frame(outer, bg=BG)
   L00124:     area.pack(fill="both", expand=True, padx=4, pady=(4, 4))
   L00125: 
>> L00126:     text_widget = tk.Text(area, wrap="none")
   L00127:     vsb = ttk.Scrollbar(area, orient="vertical", command=text_widget.yview)
   L00128:     hsb = ttk.Scrollbar(area, orient="horizontal", command=text_widget.xview)
   L00129: 
   L00130:     text_widget.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
   L00131: 
   L00132:     area.grid_rowconfigure(0, weight=1)
   L00133:     area.grid_columnconfigure(0, weight=1)
```

### `ui_menus.py`
- **Menu()**: 3 hit(s) (showing 3)
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
   L00012: 
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
   L00013:     helpm = tk.Menu(m, tearoff=False)
```
```text
   L00006:     file = tk.Menu(m, tearoff=False)
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
   L00020:     try:
```

### `ui_pipeline_tab.py`
- **Text/Canvas/Label widget**: 7 hit(s) (showing 7)
```text
   L00015:     return _project_root() / "docs" / "PIPELINE.md"
   L00016: 
   L00017: 
   L00018: def build_pipeline_tab(parent, app) -> None:
   L00019:     # PIPELINE_TREEVIEW_R2156
   L00020:     # UX+Debug: Task-Liste (Treeview) + Toggle + Filter + Summary + Auto-Reload + Diagnose
   L00021: 
>> L00022:     header = ttk.Label(parent, text="Pipeline", anchor="w")
   L00023:     # PIPELINE_UX_R2166
   L00024: 
   L00025:     header.pack(fill="x", padx=10, pady=(10, 4))
   L00026: 
   L00027:     diag = ttk.Label(parent, text="", anchor="w")
   L00028:     diag.pack(fill="x", padx=10, pady=(0, 4))
   L00029: 
```
```text
   L00020:     # UX+Debug: Task-Liste (Treeview) + Toggle + Filter + Summary + Auto-Reload + Diagnose
   L00021: 
   L00022:     header = ttk.Label(parent, text="Pipeline", anchor="w")
   L00023:     # PIPELINE_UX_R2166
   L00024: 
   L00025:     header.pack(fill="x", padx=10, pady=(10, 4))
   L00026: 
>> L00027:     diag = ttk.Label(parent, text="", anchor="w")
   L00028:     diag.pack(fill="x", padx=10, pady=(0, 4))
   L00029: 
   L00030:     summary = ttk.Label(parent, text="", anchor="w")
   L00031:     summary.pack(fill="x", padx=10, pady=(0, 6))
   L00032: 
   L00033:     bar = ttk.Frame(parent)
   L00034:     bar.pack(fill="x", padx=10, pady=(0, 8))
```
```text
   L00023:     # PIPELINE_UX_R2166
   L00024: 
   L00025:     header.pack(fill="x", padx=10, pady=(10, 4))
   L00026: 
   L00027:     diag = ttk.Label(parent, text="", anchor="w")
   L00028:     diag.pack(fill="x", padx=10, pady=(0, 4))
   L00029: 
>> L00030:     summary = ttk.Label(parent, text="", anchor="w")
   L00031:     summary.pack(fill="x", padx=10, pady=(0, 6))
   L00032: 
   L00033:     bar = ttk.Frame(parent)
   L00034:     bar.pack(fill="x", padx=10, pady=(0, 8))
   L00035: 
   L00036:     var_show_open = tk.BooleanVar(value=True)
   L00037:     var_show_done = tk.BooleanVar(value=True)
```
```text
   L00035: 
   L00036:     var_show_open = tk.BooleanVar(value=True)
   L00037:     var_show_done = tk.BooleanVar(value=True)
   L00038: 
   L00039:     ttk.Checkbutton(bar, text="Offen", variable=var_show_open).pack(side="left")
   L00040:     ttk.Checkbutton(bar, text="Erledigt", variable=var_show_done).pack(side="left", padx=(8, 0))
   L00041: 
>> L00042:     ttk.Label(bar, text="|").pack(side="left", padx=8)
   L00043: 
   L00044:     var_query = tk.StringVar(value="")
   L00045:     ttk.Label(bar, text="Suche:").pack(side="left", padx=(0, 6))
   L00046:     ent_query = ttk.Entry(bar, textvariable=var_query, width=26)
   L00047:     ent_query.pack(side="left")
   L00048:     btn_clear = ttk.Button(bar, text="X", width=3, command=lambda: var_query.set(""))
   L00049:     btn_clear.pack(side="left", padx=(6, 0))
```
```text
   L00038: 
   L00039:     ttk.Checkbutton(bar, text="Offen", variable=var_show_open).pack(side="left")
   L00040:     ttk.Checkbutton(bar, text="Erledigt", variable=var_show_done).pack(side="left", padx=(8, 0))
   L00041: 
   L00042:     ttk.Label(bar, text="|").pack(side="left", padx=8)
   L00043: 
   L00044:     var_query = tk.StringVar(value="")
>> L00045:     ttk.Label(bar, text="Suche:").pack(side="left", padx=(0, 6))
   L00046:     ent_query = ttk.Entry(bar, textvariable=var_query, width=26)
   L00047:     ent_query.pack(side="left")
   L00048:     btn_clear = ttk.Button(bar, text="X", width=3, command=lambda: var_query.set(""))
   L00049:     btn_clear.pack(side="left", padx=(6, 0))
   L00050: 
   L00051: 
   L00052:     btn_reload = ttk.Button(bar, text="Neu laden")
```
```text
   L00051: 
   L00052:     btn_reload = ttk.Button(bar, text="Neu laden")
   L00053:     btn_reload.pack(side="left")
   L00054: 
   L00055:     btn_open = ttk.Button(bar, text="Im Explorer")
   L00056:     btn_open.pack(side="left", padx=(8, 0))
   L00057: 
>> L00058:     hint = ttk.Label(bar, text="Tipp: Doppelklick oder SPACE toggelt ☐/☑", anchor="w")
   L00059:     hint.pack(side="right")
   L00060: 
   L00061:     content = ttk.Frame(parent)
   L00062:     content.pack(fill="both", expand=True, padx=10, pady=(0, 10))
   L00063: 
   L00064:     cols = ("status", "prio", "task", "section")
   L00065: 
```
```text
   L00113: 
   L00114: 
   L00115:     scr = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
   L00116:     tree.configure(yscrollcommand=scr.set)
   L00117:     tree.pack(side="left", fill="both", expand=True)
   L00118:     scr.pack(side="right", fill="y")
   L00119: 
>> L00120:     empty = ttk.Label(parent, text="", anchor="w")
   L00121:     empty.pack(fill="x", padx=10, pady=(0, 10))
   L00122: 
   L00123:     state = {
   L00124:         "last_mtime": None,
   L00125:         "items": [],
   L00126:         "raw_lines": [],
   L00127:         "visible": [],
```

### `ui_project_tree.py`
- **BIND <Button-3>**: 1 hit(s) (showing 1)
```text
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
- **Menu()**: 1 hit(s) (showing 1)
```text
   L01027:         try:
   L01028:             from tkinter import messagebox
   L01029:             messagebox.showinfo("Backup wiederherstellen", "OK: Wiederhergestellt.")
   L01030:         except Exception:
   L01031:             pass
   L01032:     # --- R2477_END ---
   L01033: 
>> L01034:     menu = tk.Menu(tree, tearoff=False)
   L01035: 
   L01036: 
   L01037:     def _copy_selected():
   L01038:         try:
   L01039:             sel = tree.selection()
   L01040:         except Exception:
   L01041:             sel = ()
```
- **tk_popup**: 1 hit(s) (showing 1)
```text
   L01082:                     try:
   L01083:                         if (event.state & 0x0004):  # Control-Key
   L01084:                             tree.selection_add(row)
   L01085:                         else:
   L01086:                             tree.selection_set(row)
   L01087:                     except Exception:
   L01088:                         tree.selection_set(row)
>> L01089:             menu.tk_popup(event.x_root, event.y_root)
   L01090:         finally:
   L01091:             try:
   L01092:                 menu.grab_release()
   L01093:             except Exception:
   L01094:                 pass
   L01095: 
   L01096:     try:
```
- **Text/Canvas/Label widget**: 3 hit(s) (showing 3)
```text
   L00059:     if not isinstance(count_var, tk.StringVar):
   L00060:         count_var = tk.StringVar(value="0 Einträge")
   L00061:         try:
   L00062:             app.entry_count = count_var
   L00063:         except Exception:
   L00064:             pass
   L00065: 
>> L00066:     tk.Label(row_count, textvariable=count_var, bg=bg).pack(side="left", padx=(0, 4))
   L00067: 
   L00068:     # Workspace-Auswahl (dynamisch: INI + Auto-Scan)
   L00069:     row_workspace = tk.Frame(wrap, bg=bg)
   L00070:     row_workspace.pack(fill="x", padx=0, pady=(0, 4))
   L00071: 
   L00072:     workspace_var = getattr(app, "workspace_var", None)
   L00073:     if not isinstance(workspace_var, tk.StringVar):
```
```text
   L00109:                         workspace_values.append(name)
   L00110:             except Exception:
   L00111:                 pass
   L00112:     except Exception:
   L00113:         pass
   L00114: 
   L00115:     # Label + Combobox
>> L00116:     tk.Label(row_workspace, text="Workspace:", bg=bg).pack(side="left")
   L00117:     combo_workspace = ttk.Combobox(
   L00118:         row_workspace,
   L00119:         textvariable=workspace_var,
   L00120:         values=workspace_values,
   L00121:         state="readonly",
   L00122:         width=12,
   L00123:     )
```
```text
   L00141:     except Exception:
   L00142:         pass
   L00143: 
   L00144:     # Suchzeile (rechts eigenständig)
   L00145:     row_search = tk.Frame(wrap, bg=bg)
   L00146:     row_search.pack(fill="x", padx=0, pady=(0, 4))
   L00147: 
>> L00148:     tk.Label(row_search, text="Suche:", bg=bg).pack(side="left")
   L00149:     search_var = tk.StringVar(value="")
   L00150:     ent = ui_theme_classic.Entry(row_search, textvariable=search_var, width=24)
   L00151:     ent.pack(side="left", padx=(4, 0))
   L00152: 
   L00153:     # Aktionsleiste (rechte Seite unterhalb der Suche)
   L00154:     row_actions = tk.Frame(wrap, bg=bg)
   L00155:     row_actions.pack(fill="x", padx=0, pady=(0, 4))
```

### `ui_runner_products_tab.py`
- **BIND <Button-3>**: 2 hit(s) (showing 2)
```text
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
```
```text
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
- **Menu()**: 2 hit(s) (showing 2)
```text
   L00541:             pass
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
   L00555:             m.tk_popup(ev.x_root, ev.y_root)
```
```text
   L00628:     def on_dbl(_):
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
   L00642: 
```
- **tk_popup**: 2 hit(s) (showing 2)
```text
   L00548:             m = tk.Menu(tree, tearoff=0)
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
   L00562:         tree.bind("<Control-c>", _tree_copy_path)
```
```text
   L00634:         if not p: return
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
   L00648:         p = get_path_callable()
```
- **Preview keyword**: 4 hit(s) (showing 4)
```text
   L00280: 
   L00281:     btn_refresh = tk.Button(top, text="Refresh")
   L00282:     btn_refresh.pack(side="right")
   L00283: 
   L00284:     mid = tk.Frame(container, bg=bg)
   L00285:     mid.pack(fill="both", expand=True, padx=8, pady=(0, 8))
   L00286: 
>> L00287:     # Left: list, Right: preview
   L00288:     left = tk.Frame(mid, bg=bg)
   L00289:     left.pack(side="left", fill="both", expand=True)
   L00290:     right = tk.Frame(mid, bg=bg)
   L00291:     right.pack(side="right", fill="both", expand=True)
   L00292: 
   L00293:     # Filters
   L00294:     f = tk.Frame(left, bg=bg)
```
```text
   L00324:     tree.column("size", width=80, anchor="e")
   L00325:     tree.pack(side="left", fill="both", expand=True)
   L00326: 
   L00327:     sb = ttk.Scrollbar(left, orient="vertical", command=tree.yview)
   L00328:     sb.pack(side="right", fill="y")
   L00329:     tree.configure(yscrollcommand=sb.set)
   L00330: 
>> L00331:     # Preview
   L00332:     tk.Label(right, text="Preview", bg=bg).pack(anchor="w")
   L00333:     txt = tk.Text(right, wrap="word")
   L00334:     txt.pack(fill="both", expand=True)
   L00335: 
   L00336:     # Actions
   L00337:     act = tk.Frame(container, bg=bg)
   L00338:     act.pack(fill="x", padx=8, pady=(0, 8))
```
```text
   L00325:     tree.pack(side="left", fill="both", expand=True)
   L00326: 
   L00327:     sb = ttk.Scrollbar(left, orient="vertical", command=tree.yview)
   L00328:     sb.pack(side="right", fill="y")
   L00329:     tree.configure(yscrollcommand=sb.set)
   L00330: 
   L00331:     # Preview
>> L00332:     tk.Label(right, text="Preview", bg=bg).pack(anchor="w")
   L00333:     txt = tk.Text(right, wrap="word")
   L00334:     txt.pack(fill="both", expand=True)
   L00335: 
   L00336:     # Actions
   L00337:     act = tk.Frame(container, bg=bg)
   L00338:     act.pack(fill="x", padx=8, pady=(0, 8))
   L00339:     btn_open = tk.Button(act, text="Öffnen")
```
```text
   L00409:             txt.delete("1.0", "end")
   L00410:         except Exception:
   L00411:             pass
   L00412:         if not path:
   L00413:             return
   L00414:         try:
   L00415:             if os.path.getsize(path) > 2 * 1024 * 1024:
>> L00416:                 txt.insert("end", "(Datei zu groß für Preview > 2MB)\n" + path)
   L00417:                 return
   L00418:         except Exception:
   L00419:             pass
   L00420:         try:
   L00421:             with open(path, "r", encoding="utf-8", errors="replace") as f:
   L00422:                 content = f.read()
   L00423:         except Exception as exc:
```
- **Artifacts keyword**: 1 hit(s) (showing 1)
```text
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
```
- **Text/Canvas/Label widget**: 8 hit(s) (showing 8)
```text
   L00124:         _safe_open_file(str(path))
   L00125:         return
   L00126: 
   L00127:     # Top: Info
   L00128:     top = tk.Frame(win)
   L00129:     top.pack(side="top", fill="x", padx=8, pady=6)
   L00130: 
>> L00131:     lbl = tk.Label(top, text=str(path), anchor="w", justify="left")
   L00132:     lbl.pack(side="left", fill="x", expand=True)
   L00133: 
   L00134:     # Center: Text + Scroll
   L00135:     mid = tk.Frame(win)
   L00136:     mid.pack(side="top", fill="both", expand=True, padx=8, pady=6)
   L00137: 
   L00138:     txt = tk.Text(mid, wrap="none")
```
```text
   L00131:     lbl = tk.Label(top, text=str(path), anchor="w", justify="left")
   L00132:     lbl.pack(side="left", fill="x", expand=True)
   L00133: 
   L00134:     # Center: Text + Scroll
   L00135:     mid = tk.Frame(win)
   L00136:     mid.pack(side="top", fill="both", expand=True, padx=8, pady=6)
   L00137: 
>> L00138:     txt = tk.Text(mid, wrap="none")
   L00139:     txt.pack(side="left", fill="both", expand=True)
   L00140: 
   L00141:     sb_y = tk.Scrollbar(mid, orient="vertical", command=txt.yview)
   L00142:     sb_y.pack(side="right", fill="y")
   L00143:     txt.configure(yscrollcommand=sb_y.set)
   L00144: 
   L00145:     sb_x = tk.Scrollbar(win, orient="horizontal", command=txt.xview)
```
```text
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
```
```text
   L00290:     right = tk.Frame(mid, bg=bg)
   L00291:     right.pack(side="right", fill="both", expand=True)
   L00292: 
   L00293:     # Filters
   L00294:     f = tk.Frame(left, bg=bg)
   L00295:     f.pack(fill="x", pady=(0, 6))
   L00296: 
>> L00297:     tk.Label(f, text="Runner:", bg=bg).pack(side="left")
   L00298:     var_runner = tk.StringVar(value="")
   L00299:     ent_runner = tk.Entry(f, textvariable=var_runner, width=10)
   L00300:     ent_runner.pack(side="left", padx=(4, 10))
   L00301: 
   L00302:     tk.Label(f, text="Typ:", bg=bg).pack(side="left")
   L00303:     var_type = tk.StringVar(value="All")
   L00304:     cmb_type = ttk.Combobox(f, textvariable=var_type, values=["All", "Report", "Doc", "Backup", "File"], width=10, state="readonly")
```
```text
   L00295:     f.pack(fill="x", pady=(0, 6))
   L00296: 
   L00297:     tk.Label(f, text="Runner:", bg=bg).pack(side="left")
   L00298:     var_runner = tk.StringVar(value="")
   L00299:     ent_runner = tk.Entry(f, textvariable=var_runner, width=10)
   L00300:     ent_runner.pack(side="left", padx=(4, 10))
   L00301: 
>> L00302:     tk.Label(f, text="Typ:", bg=bg).pack(side="left")
   L00303:     var_type = tk.StringVar(value="All")
   L00304:     cmb_type = ttk.Combobox(f, textvariable=var_type, values=["All", "Report", "Doc", "Backup", "File"], width=10, state="readonly")
   L00305:     cmb_type.pack(side="left", padx=(4, 10))
   L00306: 
   L00307:     tk.Label(f, text="Suche:", bg=bg).pack(side="left")
   L00308:     var_q = tk.StringVar(value="")
   L00309:     ent_q = tk.Entry(f, textvariable=var_q)
```
```text
   L00300:     ent_runner.pack(side="left", padx=(4, 10))
   L00301: 
   L00302:     tk.Label(f, text="Typ:", bg=bg).pack(side="left")
   L00303:     var_type = tk.StringVar(value="All")
   L00304:     cmb_type = ttk.Combobox(f, textvariable=var_type, values=["All", "Report", "Doc", "Backup", "File"], width=10, state="readonly")
   L00305:     cmb_type.pack(side="left", padx=(4, 10))
   L00306: 
>> L00307:     tk.Label(f, text="Suche:", bg=bg).pack(side="left")
   L00308:     var_q = tk.StringVar(value="")
   L00309:     ent_q = tk.Entry(f, textvariable=var_q)
   L00310:     ent_q.pack(side="left", fill="x", expand=True, padx=(4, 0))
   L00311: 
   L00312:     # Tree
   L00313:     cols = ("mtime", "type", "runner", "name", "size")
   L00314:     tree = ttk.Treeview(left, columns=cols, show="headings", height=18)
```
```text
   L00325:     tree.pack(side="left", fill="both", expand=True)
   L00326: 
   L00327:     sb = ttk.Scrollbar(left, orient="vertical", command=tree.yview)
   L00328:     sb.pack(side="right", fill="y")
   L00329:     tree.configure(yscrollcommand=sb.set)
   L00330: 
   L00331:     # Preview
>> L00332:     tk.Label(right, text="Preview", bg=bg).pack(anchor="w")
   L00333:     txt = tk.Text(right, wrap="word")
   L00334:     txt.pack(fill="both", expand=True)
   L00335: 
   L00336:     # Actions
   L00337:     act = tk.Frame(container, bg=bg)
   L00338:     act.pack(fill="x", padx=8, pady=(0, 8))
   L00339:     btn_open = tk.Button(act, text="Öffnen")
```
```text
   L00326: 
   L00327:     sb = ttk.Scrollbar(left, orient="vertical", command=tree.yview)
   L00328:     sb.pack(side="right", fill="y")
   L00329:     tree.configure(yscrollcommand=sb.set)
   L00330: 
   L00331:     # Preview
   L00332:     tk.Label(right, text="Preview", bg=bg).pack(anchor="w")
>> L00333:     txt = tk.Text(right, wrap="word")
   L00334:     txt.pack(fill="both", expand=True)
   L00335: 
   L00336:     # Actions
   L00337:     act = tk.Frame(container, bg=bg)
   L00338:     act.pack(fill="x", padx=8, pady=(0, 8))
   L00339:     btn_open = tk.Button(act, text="Öffnen")
   L00340:     btn_open.pack(side="left")
```

### `ui_settings_tab.py`
- **Text/Canvas/Label widget**: 1 hit(s) (showing 1)
```text
   L00034:     frame.pack(fill="both", expand=True, padx=10, pady=10)
   L00035: 
   L00036:     # Aktuelle Werte
   L00037:     current_root = config_manager.get_workspace_root()
   L00038:     current_quiet = config_manager.get_quiet_mode()
   L00039: 
   L00040:     # Row 0: workspace_root Label + Entry + Button
>> L00041:     lbl_root = ttk.Label(frame, text="Workspace-Root:")
   L00042:     lbl_root.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(0, 5))
   L00043: 
   L00044:     var_root = tk.StringVar(value=str(current_root))
   L00045:     entry_root = ttk.Entry(frame, textvariable=var_root, width=60)
   L00046:     entry_root.grid(row=0, column=1, sticky="we", padx=(0, 5), pady=(0, 5))
   L00047: 
   L00048:     def on_browse_root() -> None:
```

### `ui_statusbar.py`
- **Text/Canvas/Label widget**: 1 hit(s) (showing 1)
```text
   L00001: import tkinter as tk
   L00002: 
   L00003: def build_statusbar(app):
   L00004:     bar = tk.Frame(app); bar.pack(fill="x", side="bottom")
   L00005:     app._status = tk.StringVar(value="...")
>> L00006:     tk.Label(bar, textvariable=app._status, anchor="w").pack(fill="x", padx=8, pady=3)
   L00007: 
   L00008: def set_status(app, txt:str):
   L00009:     if hasattr(app, "_status"):
   L00010:         app._status.set(txt)
```

### `ui_toolbar.py`
- **Text/Canvas/Label widget**: 3 hit(s) (showing 3)
```text
   L00338:         win.columnconfigure(0, weight=1)
   L00339: 
   L00340:         # Oberer Bereich nur mit Info-Label
   L00341:         top_frame = tk.Frame(win)
   L00342:         top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=4, pady=(4, 0))
   L00343:         top_frame.columnconfigure(0, weight=1)
   L00344: 
>> L00345:         info_label = tk.Label(top_frame, text="Letzter Runner-Block aus debug_output.txt")
   L00346:         info_label.grid(row=0, column=0, sticky="w")
   L00347: 
   L00348:         state = {"older_loaded": False}
   L00349: 
   L00350:         # Text + Scrollbar
   L00351:         txt = tk.Text(win, wrap="none")
   L00352:         scroll = tk.Scrollbar(win, orient="vertical", command=txt.yview)
```
```text
   L00344: 
   L00345:         info_label = tk.Label(top_frame, text="Letzter Runner-Block aus debug_output.txt")
   L00346:         info_label.grid(row=0, column=0, sticky="w")
   L00347: 
   L00348:         state = {"older_loaded": False}
   L00349: 
   L00350:         # Text + Scrollbar
>> L00351:         txt = tk.Text(win, wrap="none")
   L00352:         scroll = tk.Scrollbar(win, orient="vertical", command=txt.yview)
   L00353:         txt.configure(yscrollcommand=scroll.set)
   L00354: 
   L00355:         txt.grid(row=1, column=0, sticky="nsew")
   L00356:         scroll.grid(row=1, column=1, sticky="ns")
   L00357: 
   L00358:         try:
```
```text
   L00955:         "Letzte Dateiaktion (rechts) rückgängig machen.",
   L00956:     )
   L00957: 
   L00958:     # Zeile 2 - Service / Diagnose (SR)
   L00959:     service_frame = ui_theme_classic.Frame(outer)
   L00960:     service_frame.pack(fill="x", pady=(4, 0))
   L00961: 
>> L00962:     lbl_service = tk.Label(
   L00963:         service_frame,
   L00964:         text="Service (SR) / Diagnose",
   L00965:         fg="#666666",
   L00966:         anchor="w",
   L00967:     )
   L00968:     lbl_service.pack(fill="x", padx=2, pady=(0, 2))
   L00969: 
```

### `ui_tooltips.py`
- **Text/Canvas/Label widget**: 1 hit(s) (showing 1)
```text
   L00046:         self._tip.wm_overrideredirect(True)
   L00047:         self._tip.wm_attributes("-topmost", True)
   L00048: 
   L00049:         x = self.widget.winfo_rootx() + 10
   L00050:         y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
   L00051:         self._tip.wm_geometry(f"+{x}+{y}")
   L00052: 
>> L00053:         label = tk.Label(
   L00054:             self._tip,
   L00055:             text=self.text,
   L00056:             justify="left",
   L00057:             relief="solid",
   L00058:             borderwidth=1,
   L00059:             padx=4,
   L00060:             pady=2,
```

## Next step
- Pick the single owner function/module that builds the preview context menu.
- Patch there (R2493) to add actions:
  - Inhalt kopieren (markiert/alles) [preview-level]
  - Datei(en) kopieren (Paste) [uses currently selected artifact path]
  - Im Explorer anzeigen
