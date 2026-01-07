# R2471 – UI Hookpoints Audit (READ-ONLY)

- Time: 20251222_012344
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- Scanned: `modules/*.py`

## Hits by file

### `context_state.py`
- **Context menu**: 6 hit(s) (showing up to 6)
```text
   L00001: # -*- coding: utf-8 -*-
>> L00002: """Context State (Runtime)
   L00003: 
   L00004: Zweck:
   L00005: - Zentrale, kleine Zustands-Sammlung für ShrimpDev (UI / Agent / Pipeline).
   L00006: - Keine globale Wildwest-Nutzung: Zugriff ausschließlich über Funktionen.
```
```text
   L00032: def _now() -> str:
   L00033:     return time.strftime("%Y-%m-%d %H:%M:%S")
   L00034: 
   L00035: def get_context() -> Dict[str, Any]:
>> L00036:     """Gibt eine Kopie des aktuellen Context zurück."""
   L00037:     return dict(_CONTEXT)
   L00038: 
   L00039: def update_context(**kwargs: Any) -> Dict[str, Any]:
   L00040:     """Aktualisiert Context-Felder (bewusst flach gehalten)."""
```
```text
   L00036:     """Gibt eine Kopie des aktuellen Context zurück."""
   L00037:     return dict(_CONTEXT)
   L00038: 
   L00039: def update_context(**kwargs: Any) -> Dict[str, Any]:
>> L00040:     """Aktualisiert Context-Felder (bewusst flach gehalten)."""
   L00041:     for k, v in kwargs.items():
   L00042:         _CONTEXT[k] = v
   L00043:     _CONTEXT["timestamp"] = _now()
   L00044:     return dict(_CONTEXT)
```
```text
   L00043:     _CONTEXT["timestamp"] = _now()
   L00044:     return dict(_CONTEXT)
   L00045: 
   L00046: def reset_context() -> Dict[str, Any]:
>> L00047:     """Setzt Context auf Initialzustand zurück."""
   L00048:     for k in list(_CONTEXT.keys()):
   L00049:         _CONTEXT[k] = None
   L00050:     _CONTEXT["timestamp"] = _now()
   L00051:     return dict(_CONTEXT)
```
```text
   L00050:     _CONTEXT["timestamp"] = _now()
   L00051:     return dict(_CONTEXT)
   L00052: 
   L00053: def save_context(path: Path | None = None) -> Path:
>> L00054:     """Persistiert Context als JSON (optional, Debug/Pipeline)."""
   L00055:     p = path or _DEFAULT_PATH
   L00056:     p.parent.mkdir(parents=True, exist_ok=True)
   L00057:     p.write_text(json.dumps(_CONTEXT, indent=2, ensure_ascii=False), encoding="utf-8")
   L00058:     return p
```
```text
   L00057:     p.write_text(json.dumps(_CONTEXT, indent=2, ensure_ascii=False), encoding="utf-8")
   L00058:     return p
   L00059: 
   L00060: def load_context(path: Path | None = None) -> Dict[str, Any]:
>> L00061:     """Lädt Context aus JSON (falls vorhanden) und merged."""
   L00062:     p = path or _DEFAULT_PATH
   L00063:     if p.exists():
   L00064:         try:
   L00065:             data = json.loads(p.read_text(encoding="utf-8"))
```

### `exception_logger.py`
- **Context menu**: 2 hit(s) (showing up to 2)
```text
   L00032:     _ROOT = Path(project_root).resolve()
   L00033:     _DEBUG_FILE = _ROOT / 'debug_output.txt'
   L00034: 
   L00035: 
>> L00036: def log_exception(exc: BaseException, context: str = '') -> None:
   L00037:     try:
   L00038:         tb = traceback.format_exc()
   L00039:         if not tb or tb.strip() == 'NoneType: None':
   L00040:             tb = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
```
```text
   L00040:             tb = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
   L00041:     except Exception:
   L00042:         tb = 'traceback unavailable'
   L00043: 
>> L00044:     ctx = context.strip()
   L00045:     head = f"[{_now()}] EXCEPTION" + (f" ({ctx})" if ctx else '')
   L00046:     payload = head + "\n" + tb.strip() + "\n"
   L00047: 
   L00048:     if _DEBUG_FILE is not None:
```

### `learning_engine.py`
- **Context menu**: 3 hit(s) (showing up to 3)
```text
   L00331:         "total": len(entries),
   L00332:     }
   L00333: 
   L00334: 
>> L00335: def suggest_improvements(context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
   L00336:     """
   L00337:     Liefert einfache Verbesserungsvorschläge auf Basis des Journals.
   L00338: 
   L00339:     Der Algorithmus ist bewusst leichtgewichtig und defensiv:
```
```text
   L00388:             "weight": 0.5,
   L00389:         })
   L00390: 
   L00391:     # Kontextabhängige Hinweise (falls vorhanden)
>> L00392:     ctx_source = (context or {}).get("source")
   L00393:     if ctx_source == "intake":
   L00394:         suggestions.append({
   L00395:             "kind": "context",
   L00396:             "message": (
```
```text
   L00391:     # Kontextabhängige Hinweise (falls vorhanden)
   L00392:     ctx_source = (context or {}).get("source")
   L00393:     if ctx_source == "intake":
   L00394:         suggestions.append({
>> L00395:             "kind": "context",
   L00396:             "message": (
   L00397:                 "Kontext: Aufruf aus dem Intake. "
   L00398:                 "Eine Integration von LearningEngine-Hinweisen direkt im "
   L00399:                 "Intake-Tab (z. B. neben den LEDs) könnte sinnvoll sein."
```
- **Splitter/Resizable**: 4 hit(s) (showing up to 4)
```text
   L00343:       Liste zurückgegeben.
   L00344: 
   L00345:     Rückgabe:
   L00346:     - Liste von Dicts mit mindestens:
>> L00347:       { "kind": "...", "message": "...", "weight": float }
   L00348:     """
   L00349:     snapshot = get_journal_snapshot()
   L00350:     total = snapshot.get("total", 0)
   L00351:     counts_by_event = snapshot.get("counts_by_event", {})
```
```text
   L00367:             "message": (
   L00368:                 "Es wurden sehr viele Detect-Vorgänge protokolliert. "
   L00369:                 "Evtl. lohnt sich ein Auto-Detect beim Laden oder Speichern."
   L00370:             ),
>> L00371:             "weight": 0.6,
   L00372:         })
   L00373: 
   L00374:     # Beispiel-Heuristik: Viele Runs -> Hinweis auf bevorzugte Runner-Historie
   L00375:     run_like = 0
```
```text
   L00384:                 "Viele Run-Vorgänge wurden protokolliert. "
   L00385:                 "Evtl. könnte eine 'Zuletzt ausgeführt'-Liste oder ein "
   L00386:                 "Runner-Favoritensystem hilfreich sein."
   L00387:             ),
>> L00388:             "weight": 0.5,
   L00389:         })
   L00390: 
   L00391:     # Kontextabhängige Hinweise (falls vorhanden)
   L00392:     ctx_source = (context or {}).get("source")
```
```text
   L00397:                 "Kontext: Aufruf aus dem Intake. "
   L00398:                 "Eine Integration von LearningEngine-Hinweisen direkt im "
   L00399:                 "Intake-Tab (z. B. neben den LEDs) könnte sinnvoll sein."
   L00400:             ),
>> L00401:             "weight": 0.3,
   L00402:         })
   L00403: 
   L00404:     return suggestions
```

### `logic_actions.py`
- **Context menu**: 8 hit(s) (showing up to 8)
```text
   L01005:     tree = getattr(app, "tree", None)
   L01006:     if tree is None:
   L01007:         return
   L01008: 
>> L01009:     menu = _r1848_tk.Menu(tree, tearoff=False)
   L01010: 
   L01011:     def _update_selection(event):
   L01012:         try:
   L01013:             row_id = tree.identify_row(event.y)
```
```text
   L01046:             action_tree_delete(app)
   L01047:         except Exception:
   L01048:             pass
   L01049: 
>> L01050:     menu.add_command(label="In Intake laden", command=_cmd_open_intake)
   L01051:     menu.add_command(label="Explorer öffnen", command=_cmd_open_explorer)
   L01052:     menu.add_command(label="Pfad kopieren", command=_cmd_copy_path)
   L01053:     menu.add_separator()
   L01054:     menu.add_command(label="Umbenennen…", command=_cmd_rename)
```
```text
   L01047:         except Exception:
   L01048:             pass
   L01049: 
   L01050:     menu.add_command(label="In Intake laden", command=_cmd_open_intake)
>> L01051:     menu.add_command(label="Explorer öffnen", command=_cmd_open_explorer)
   L01052:     menu.add_command(label="Pfad kopieren", command=_cmd_copy_path)
   L01053:     menu.add_separator()
   L01054:     menu.add_command(label="Umbenennen…", command=_cmd_rename)
   L01055:     menu.add_command(label="In den Papierkorb", command=_cmd_trash)
```
```text
   L01048:             pass
   L01049: 
   L01050:     menu.add_command(label="In Intake laden", command=_cmd_open_intake)
   L01051:     menu.add_command(label="Explorer öffnen", command=_cmd_open_explorer)
>> L01052:     menu.add_command(label="Pfad kopieren", command=_cmd_copy_path)
   L01053:     menu.add_separator()
   L01054:     menu.add_command(label="Umbenennen…", command=_cmd_rename)
   L01055:     menu.add_command(label="In den Papierkorb", command=_cmd_trash)
   L01056: 
```
```text
   L01050:     menu.add_command(label="In Intake laden", command=_cmd_open_intake)
   L01051:     menu.add_command(label="Explorer öffnen", command=_cmd_open_explorer)
   L01052:     menu.add_command(label="Pfad kopieren", command=_cmd_copy_path)
   L01053:     menu.add_separator()
>> L01054:     menu.add_command(label="Umbenennen…", command=_cmd_rename)
   L01055:     menu.add_command(label="In den Papierkorb", command=_cmd_trash)
   L01056: 
   L01057:     def _on_button3(event, _menu=menu):
   L01058:         _update_selection(event)
```
```text
   L01051:     menu.add_command(label="Explorer öffnen", command=_cmd_open_explorer)
   L01052:     menu.add_command(label="Pfad kopieren", command=_cmd_copy_path)
   L01053:     menu.add_separator()
   L01054:     menu.add_command(label="Umbenennen…", command=_cmd_rename)
>> L01055:     menu.add_command(label="In den Papierkorb", command=_cmd_trash)
   L01056: 
   L01057:     def _on_button3(event, _menu=menu):
   L01058:         _update_selection(event)
   L01059:         try:
```
```text
   L01056: 
   L01057:     def _on_button3(event, _menu=menu):
   L01058:         _update_selection(event)
   L01059:         try:
>> L01060:             _menu.tk_popup(event.x_root, event.y_root)
   L01061:         finally:
   L01062:             try:
   L01063:                 _menu.grab_release()
   L01064:             except Exception:
```
```text
   L01064:             except Exception:
   L01065:                 pass
   L01066: 
   L01067:     try:
>> L01068:         tree.bind("<Button-3>", lambda event: _on_button3(event), add="+")
   L01069:     except Exception:
   L01070:         pass
   L01071: 
   L01072: # build_tree aus ui_project_tree wrappen, damit Kontextmenue nach dem Aufbau gesetzt wird
```
- **Refresh button**: 8 hit(s) (showing up to 8)
```text
   L00464:                     pass
   L00465: 
   L00466:     try:
   L00467:         proxy = getattr(app, 'right_list', None)
>> L00468:         if proxy is not None and hasattr(proxy, 'refresh'):
   L00469:             proxy.refresh()
   L00470:     except Exception:
   L00471:         pass
   L00472: 
```
```text
   L00465: 
   L00466:     try:
   L00467:         proxy = getattr(app, 'right_list', None)
   L00468:         if proxy is not None and hasattr(proxy, 'refresh'):
>> L00469:             proxy.refresh()
   L00470:     except Exception:
   L00471:         pass
   L00472: 
   L00473: 
```
```text
   L00918:         })
   L00919: 
   L00920:     try:
   L00921:         proxy = getattr(app, "right_list", None)
>> L00922:         if proxy and hasattr(proxy, "refresh"):
   L00923:             proxy.refresh()
   L00924:     except Exception:
   L00925:         pass
   L00926: 
```
```text
   L00919: 
   L00920:     try:
   L00921:         proxy = getattr(app, "right_list", None)
   L00922:         if proxy and hasattr(proxy, "refresh"):
>> L00923:             proxy.refresh()
   L00924:     except Exception:
   L00925:         pass
   L00926: 
   L00927: 
```
```text
   L01822: # # und arbeiten auf Basis der rechten Runner-Liste.
   L01823: # #
   L01824: # # Abhängigkeiten:
   L01825: # #   - ui_project_tree.get_selected_path(app) für Pfadermittlung
>> L01826: # #   - app.right_list.refresh() (RightListProxy) für Refresh, falls vorhanden
   L01827: # 
   L01828: # import os as _r1840_os
   L01829: # import time as _r1840_time
   L01830: # 
```
```text
   L01940: # def _r1840_refresh_right_list(app):
   L01941: #     """Aktualisiert die rechte Liste / den Tree, ohne Exceptions nach aussen."""
   L01942: #     try:
   L01943: #         proxy = getattr(app, "right_list", None)
>> L01944: #         if proxy is not None and hasattr(proxy, "refresh"):
   L01945: #             proxy.refresh()
   L01946: #             return
   L01947: #     except Exception:
   L01948: #         pass
```
```text
   L01941: #     """Aktualisiert die rechte Liste / den Tree, ohne Exceptions nach aussen."""
   L01942: #     try:
   L01943: #         proxy = getattr(app, "right_list", None)
   L01944: #         if proxy is not None and hasattr(proxy, "refresh"):
>> L01945: #             proxy.refresh()
   L01946: #             return
   L01947: #     except Exception:
   L01948: #         pass
   L01949: #     # Fallback: nichts tun
```
```text
   L02234: # 
   L02235: # def _r1841_refresh_right_list(app):
   L02236: #     try:
   L02237: #         proxy = getattr(app, "right_list", None)
>> L02238: #         if proxy is not None and hasattr(proxy, "refresh"):
   L02239: #             proxy.refresh()
   L02240: #     except Exception:
   L02241: #         pass
   L02242: # 
```
- **Scrollbars**: 8 hit(s) (showing up to 8)
```text
   L01196: 
   L01197:         frame = _r1851_tk.Frame(win)
   L01198:         frame.pack(expand=True, fill="both")
   L01199: 
>> L01200:         scrollbar = _r1851_tk.Scrollbar(frame)
   L01201:         scrollbar.pack(side="right", fill="y")
   L01202: 
   L01203:         txt = _r1851_tk.Text(frame, wrap="word")
   L01204:         txt.pack(side="left", expand=True, fill="both")
```
```text
   L01197:         frame = _r1851_tk.Frame(win)
   L01198:         frame.pack(expand=True, fill="both")
   L01199: 
   L01200:         scrollbar = _r1851_tk.Scrollbar(frame)
>> L01201:         scrollbar.pack(side="right", fill="y")
   L01202: 
   L01203:         txt = _r1851_tk.Text(frame, wrap="word")
   L01204:         txt.pack(side="left", expand=True, fill="both")
   L01205:         txt.config(yscrollcommand=scrollbar.set)
```
```text
   L01201:         scrollbar.pack(side="right", fill="y")
   L01202: 
   L01203:         txt = _r1851_tk.Text(frame, wrap="word")
   L01204:         txt.pack(side="left", expand=True, fill="both")
>> L01205:         txt.config(yscrollcommand=scrollbar.set)
   L01206:         scrollbar.config(command=txt.yview)
   L01207: 
   L01208:         if _r1851_font is not None:
   L01209:             try:
```
```text
   L01202: 
   L01203:         txt = _r1851_tk.Text(frame, wrap="word")
   L01204:         txt.pack(side="left", expand=True, fill="both")
   L01205:         txt.config(yscrollcommand=scrollbar.set)
>> L01206:         scrollbar.config(command=txt.yview)
   L01207: 
   L01208:         if _r1851_font is not None:
   L01209:             try:
   L01210:                 mono = _r1851_font.Font(family="Courier New", size=10)
```
```text
   L01449: 
   L01450:         frame = _r1852_tk.Frame(win)
   L01451:         frame.pack(expand=True, fill="both")
   L01452: 
>> L01453:         scrollbar = _r1852_tk.Scrollbar(frame)
   L01454:         scrollbar.pack(side="right", fill="y")
   L01455: 
   L01456:         txt = _r1852_tk.Text(frame, wrap="word")
   L01457:         txt.pack(side="left", expand=True, fill="both")
```
```text
   L01450:         frame = _r1852_tk.Frame(win)
   L01451:         frame.pack(expand=True, fill="both")
   L01452: 
   L01453:         scrollbar = _r1852_tk.Scrollbar(frame)
>> L01454:         scrollbar.pack(side="right", fill="y")
   L01455: 
   L01456:         txt = _r1852_tk.Text(frame, wrap="word")
   L01457:         txt.pack(side="left", expand=True, fill="both")
   L01458:         txt.config(yscrollcommand=scrollbar.set)
```
```text
   L01454:         scrollbar.pack(side="right", fill="y")
   L01455: 
   L01456:         txt = _r1852_tk.Text(frame, wrap="word")
   L01457:         txt.pack(side="left", expand=True, fill="both")
>> L01458:         txt.config(yscrollcommand=scrollbar.set)
   L01459:         scrollbar.config(command=txt.yview)
   L01460: 
   L01461:         if _r1852_font is not None:
   L01462:             try:
```
```text
   L01455: 
   L01456:         txt = _r1852_tk.Text(frame, wrap="word")
   L01457:         txt.pack(side="left", expand=True, fill="both")
   L01458:         txt.config(yscrollcommand=scrollbar.set)
>> L01459:         scrollbar.config(command=txt.yview)
   L01460: 
   L01461:         if _r1852_font is not None:
   L01462:             try:
   L01463:                 mono = _r1852_font.Font(family="Courier New", size=10)
```

### `module_agent.py`
- **Tree/Explorer widgets**: 1 hit(s) (showing up to 1)
```text
   L00528:     right = ttk.Frame(outer)
   L00529:     right.pack(side="left", fill="both", expand=True, padx=(10, 0))
   L00530: 
   L00531:     cols = ("exists", "title")
>> L00532:     tree = ttk.Treeview(left, columns=cols, show="headings", height=14, selectmode="browse")
   L00533:     tree.heading("exists", text="OK")
   L00534:     tree.heading("title", text="Empfehlung")
   L00535:     tree.column("exists", width=45, stretch=False, anchor="center")
   L00536:     tree.column("title", width=360, stretch=True, anchor="w")
```
- **Context menu**: 2 hit(s) (showing up to 2)
```text
   L00177: 
   L00178:     return out
   L00179: 
   L00180: 
>> L00181:     # R2119: Context aktualisieren (Tab = agent)
   L00182:     if context_state is not None:
   L00183:         try:
   L00184:             context_state.update_context(active_tab='agent')
   L00185:         except Exception:
```
```text
   L00187: 
   L00188: def agent_summary() -> str:
   L00189:     d = load_agent_data()
   L00190:     lines = []
>> L00191:     # R2120: Context-Hinweise (read-only)
   L00192:     if context_state is not None:
   L00193:         try:
   L00194:             ctx = context_state.get_context()
   L00195:             if ctx.get('last_action') == 'intake_save':
```
- **Scrollbars**: 4 hit(s) (showing up to 4)
```text
   L00533:     tree.heading("exists", text="OK")
   L00534:     tree.heading("title", text="Empfehlung")
   L00535:     tree.column("exists", width=45, stretch=False, anchor="center")
   L00536:     tree.column("title", width=360, stretch=True, anchor="w")
>> L00537:     vs = ttk.Scrollbar(left, orient="vertical", command=tree.yview)
   L00538:     tree.configure(yscrollcommand=vs.set)
   L00539:     tree.pack(side="left", fill="y")
   L00540:     vs.pack(side="left", fill="y")
   L00541: 
```
```text
   L00534:     tree.heading("title", text="Empfehlung")
   L00535:     tree.column("exists", width=45, stretch=False, anchor="center")
   L00536:     tree.column("title", width=360, stretch=True, anchor="w")
   L00537:     vs = ttk.Scrollbar(left, orient="vertical", command=tree.yview)
>> L00538:     tree.configure(yscrollcommand=vs.set)
   L00539:     tree.pack(side="left", fill="y")
   L00540:     vs.pack(side="left", fill="y")
   L00541: 
   L00542:     scr = ttk.Scrollbar(right, orient="vertical")
```
```text
   L00538:     tree.configure(yscrollcommand=vs.set)
   L00539:     tree.pack(side="left", fill="y")
   L00540:     vs.pack(side="left", fill="y")
   L00541: 
>> L00542:     scr = ttk.Scrollbar(right, orient="vertical")
   L00543:     scr.pack(side="right", fill="y")
   L00544:     txtw = tk.Text(right, wrap="word", yscrollcommand=scr.set)
   L00545:     txtw.pack(side="left", fill="both", expand=True)
   L00546:     scr.config(command=txtw.yview)
```
```text
   L00540:     vs.pack(side="left", fill="y")
   L00541: 
   L00542:     scr = ttk.Scrollbar(right, orient="vertical")
   L00543:     scr.pack(side="right", fill="y")
>> L00544:     txtw = tk.Text(right, wrap="word", yscrollcommand=scr.set)
   L00545:     txtw.pack(side="left", fill="both", expand=True)
   L00546:     scr.config(command=txtw.yview)
   L00547:     try:
   L00548:         txtw.config(state="disabled")
```

### `module_docking.py`
- **Context menu**: 6 hit(s) (showing up to 6)
```text
   L00598:         return any_open
   L00599: 
   L00600: 
   L00601: def install_notebook_context_menu(app, notebook):
>> L00602:     # Right-click context menu on tabs for undock (Phase-1: read-only tabs only)
   L00603:     dm = getattr(app, '_dock_manager', None)
   L00604:     if dm is None:
   L00605:         dm = DockManager(app)
   L00606:         app._dock_manager = dm
```
```text
   L00650:         if chosen is None:
   L00651:             return
   L00652: 
   L00653:         label, key, builder = chosen
>> L00654:         menu = tk.Menu(app, tearoff=0)
   L00655:         menu.add_command(label='Undock', command=lambda: dm.undock_readonly(key, label, builder))
   L00656:         if dm.is_open(key):
   L00657:             menu.add_command(label='Dock (Fenster schließen)', command=lambda: dm.close(key))
   L00658:         try:
```
```text
   L00651:             return
   L00652: 
   L00653:         label, key, builder = chosen
   L00654:         menu = tk.Menu(app, tearoff=0)
>> L00655:         menu.add_command(label='Undock', command=lambda: dm.undock_readonly(key, label, builder))
   L00656:         if dm.is_open(key):
   L00657:             menu.add_command(label='Dock (Fenster schließen)', command=lambda: dm.close(key))
   L00658:         try:
   L00659:             menu.tk_popup(ev.x_root, ev.y_root)
```
```text
   L00653:         label, key, builder = chosen
   L00654:         menu = tk.Menu(app, tearoff=0)
   L00655:         menu.add_command(label='Undock', command=lambda: dm.undock_readonly(key, label, builder))
   L00656:         if dm.is_open(key):
>> L00657:             menu.add_command(label='Dock (Fenster schließen)', command=lambda: dm.close(key))
   L00658:         try:
   L00659:             menu.tk_popup(ev.x_root, ev.y_root)
   L00660:         finally:
   L00661:             try:
```
```text
   L00655:         menu.add_command(label='Undock', command=lambda: dm.undock_readonly(key, label, builder))
   L00656:         if dm.is_open(key):
   L00657:             menu.add_command(label='Dock (Fenster schließen)', command=lambda: dm.close(key))
   L00658:         try:
>> L00659:             menu.tk_popup(ev.x_root, ev.y_root)
   L00660:         finally:
   L00661:             try:
   L00662:                 menu.grab_release()
   L00663:             except Exception:
```
```text
   L00663:             except Exception:
   L00664:                 pass
   L00665: 
   L00666:     try:
>> L00667:         notebook.bind('<Button-3>', _on_right_click)
   L00668:     except Exception:
   L00669:         pass
   L00670:     return dm
   L00671: 
```

### `module_learningjournal.py`
- **Scrollbars**: 4 hit(s) (showing up to 4)
```text
   L00365: 
   L00366:     listbox = tk.Listbox(frame_left, exportselection=False, height=20)
   L00367:     listbox.pack(side='left', fill='both', expand=True, pady=(2, 0))
   L00368: 
>> L00369:     scroll_list = ttk.Scrollbar(frame_left, orient='vertical', command=listbox.yview)
   L00370:     scroll_list.pack(side='right', fill='y')
   L00371:     listbox.configure(yscrollcommand=scroll_list.set)
   L00372: 
   L00373:     frame_right = ttk.Frame(paned)
```
```text
   L00367:     listbox.pack(side='left', fill='both', expand=True, pady=(2, 0))
   L00368: 
   L00369:     scroll_list = ttk.Scrollbar(frame_left, orient='vertical', command=listbox.yview)
   L00370:     scroll_list.pack(side='right', fill='y')
>> L00371:     listbox.configure(yscrollcommand=scroll_list.set)
   L00372: 
   L00373:     frame_right = ttk.Frame(paned)
   L00374:     paned.add(frame_right, weight=3)
   L00375: 
```
```text
   L00378: 
   L00379:     text_detail = tk.Text(frame_right, wrap='word', height=20)
   L00380:     text_detail.pack(side='left', fill='both', expand=True, pady=(2, 0))
   L00381: 
>> L00382:     scroll_detail = ttk.Scrollbar(frame_right, orient='vertical', command=text_detail.yview)
   L00383:     scroll_detail.pack(side='right', fill='y')
   L00384:     text_detail.configure(yscrollcommand=scroll_detail.set)
   L00385: 
   L00386:     state = {
```
```text
   L00380:     text_detail.pack(side='left', fill='both', expand=True, pady=(2, 0))
   L00381: 
   L00382:     scroll_detail = ttk.Scrollbar(frame_right, orient='vertical', command=text_detail.yview)
   L00383:     scroll_detail.pack(side='right', fill='y')
>> L00384:     text_detail.configure(yscrollcommand=scroll_detail.set)
   L00385: 
   L00386:     state = {
   L00387:         'entries': [],
   L00388:         'filtered': [],
```
- **Splitter/Resizable**: 8 hit(s) (showing up to 8)
```text
   L00300: 
   L00301: def build_learningjournal_tab(parent: tk.Frame, app: tk.Misc) -> None:
   L00302:     root = parent.winfo_toplevel()
   L00303: 
>> L00304:     parent.grid_rowconfigure(1, weight=1)
   L00305:     parent.grid_columnconfigure(0, weight=1)
   L00306: 
   L00307:     header = ttk.Frame(parent)
   L00308:     header.grid(row=0, column=0, sticky='ew', padx=8, pady=(8, 4))
```
```text
   L00301: def build_learningjournal_tab(parent: tk.Frame, app: tk.Misc) -> None:
   L00302:     root = parent.winfo_toplevel()
   L00303: 
   L00304:     parent.grid_rowconfigure(1, weight=1)
>> L00305:     parent.grid_columnconfigure(0, weight=1)
   L00306: 
   L00307:     header = ttk.Frame(parent)
   L00308:     header.grid(row=0, column=0, sticky='ew', padx=8, pady=(8, 4))
   L00309:     header.columnconfigure(0, weight=0)
```
```text
   L00305:     parent.grid_columnconfigure(0, weight=1)
   L00306: 
   L00307:     header = ttk.Frame(parent)
   L00308:     header.grid(row=0, column=0, sticky='ew', padx=8, pady=(8, 4))
>> L00309:     header.columnconfigure(0, weight=0)
   L00310:     header.columnconfigure(1, weight=0)
   L00311:     header.columnconfigure(2, weight=1)
   L00312:     header.columnconfigure(3, weight=0)
   L00313:     header.columnconfigure(4, weight=0)
```
```text
   L00306: 
   L00307:     header = ttk.Frame(parent)
   L00308:     header.grid(row=0, column=0, sticky='ew', padx=8, pady=(8, 4))
   L00309:     header.columnconfigure(0, weight=0)
>> L00310:     header.columnconfigure(1, weight=0)
   L00311:     header.columnconfigure(2, weight=1)
   L00312:     header.columnconfigure(3, weight=0)
   L00313:     header.columnconfigure(4, weight=0)
   L00314: 
```
```text
   L00307:     header = ttk.Frame(parent)
   L00308:     header.grid(row=0, column=0, sticky='ew', padx=8, pady=(8, 4))
   L00309:     header.columnconfigure(0, weight=0)
   L00310:     header.columnconfigure(1, weight=0)
>> L00311:     header.columnconfigure(2, weight=1)
   L00312:     header.columnconfigure(3, weight=0)
   L00313:     header.columnconfigure(4, weight=0)
   L00314: 
   L00315:     lbl_title = ttk.Label(header, text='LearningJournal')
```
```text
   L00308:     header.grid(row=0, column=0, sticky='ew', padx=8, pady=(8, 4))
   L00309:     header.columnconfigure(0, weight=0)
   L00310:     header.columnconfigure(1, weight=0)
   L00311:     header.columnconfigure(2, weight=1)
>> L00312:     header.columnconfigure(3, weight=0)
   L00313:     header.columnconfigure(4, weight=0)
   L00314: 
   L00315:     lbl_title = ttk.Label(header, text='LearningJournal')
   L00316:     lbl_title.grid(row=0, column=0, sticky='w')
```
```text
   L00309:     header.columnconfigure(0, weight=0)
   L00310:     header.columnconfigure(1, weight=0)
   L00311:     header.columnconfigure(2, weight=1)
   L00312:     header.columnconfigure(3, weight=0)
>> L00313:     header.columnconfigure(4, weight=0)
   L00314: 
   L00315:     lbl_title = ttk.Label(header, text='LearningJournal')
   L00316:     lbl_title.grid(row=0, column=0, sticky='w')
   L00317: 
```
```text
   L00353:     btn_reset.grid(row=3, column=4, sticky='e', padx=(4, 0), pady=(4, 0))
   L00354:     btn_scans = ttk.Button(header, text='Scans')
   L00355:     btn_scans.grid(row=4, column=4, sticky='e', padx=(4, 0), pady=(4, 0))
   L00356: 
>> L00357:     paned = ttk.Panedwindow(parent, orient='horizontal')
   L00358:     paned.grid(row=1, column=0, sticky='nsew', padx=8, pady=(4, 8))
   L00359: 
   L00360:     frame_left = ttk.Frame(paned)
   L00361:     paned.add(frame_left, weight=1)
```

### `module_learningjournal_ui_ext.py`
- **Tree/Explorer widgets**: 1 hit(s) (showing up to 1)
```text
   L00089:     lbl_path.pack(side="top", anchor="w", padx=8)
   L00090: 
   L00091:     # Tree
   L00092:     columns = ("id", "timestamp", "category", "score", "summary")
>> L00093:     tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
   L00094:     tree.pack(side="top", fill="both", expand=True, padx=8, pady=4)
   L00095: 
   L00096:     headers = {
   L00097:         "id": "ID",
```
- **Refresh button**: 3 hit(s) (showing up to 3)
```text
   L00118: 
   L00119:     lbl_summary = ttk.Label(footer, text="Keine Phase-B-Daten geladen.")
   L00120:     lbl_summary.pack(side="left")
   L00121: 
>> L00122:     def refresh():
   L00123:         data = load_learning_journal(root_dir)
   L00124:         entries = extract_phase_b_entries(data)
   L00125:         count, avg = summarize_phase_b(entries)
   L00126: 
```
```text
   L00149:                 os.startfile(str(path))
   L00150:             except:
   L00151:                 pass
   L00152: 
>> L00153:     btn_reload.configure(command=refresh)
   L00154:     btn_open.configure(command=open_json)
   L00155: 
   L00156:     refresh()
   L00157:     return frame
```
```text
   L00152: 
   L00153:     btn_reload.configure(command=refresh)
   L00154:     btn_open.configure(command=open_json)
   L00155: 
>> L00156:     refresh()
   L00157:     return frame
```

### `module_preflight.py`
- **Tree/Explorer widgets**: 1 hit(s) (showing up to 1)
```text
   L00023: 
   L00024: def _build_tab(parent):
   L00025:     frm = ttk.Frame(parent)
   L00026:     b = ttk.Frame(frm); b.pack(fill="x", pady=6)
>> L00027:     tree = ttk.Treeview(frm, columns=("item","value","status"), show="headings")
   L00028:     for c,w in zip(("item","value","status"),(300,280,80)): tree.heading(c, text=c); tree.column(c, width=w, anchor="w")
   L00029:     tree.pack(fill="both", expand=True)
   L00030:     def run():
   L00031:         rows = _checks()
```

### `module_runner_board.py`
- **Tree/Explorer widgets**: 1 hit(s) (showing up to 1)
```text
   L00018: def _build_tab(parent):
   L00019:     frm = ttk.Frame(parent)
   L00020:     bar = ttk.Frame(frm); bar.pack(fill="x", pady=6)
   L00021:     ttk.Button(bar, text="Refresh", command=lambda: refresh()).pack(side="left")
>> L00022:     tree = ttk.Treeview(frm, columns=("file","type"), show="headings")
   L00023:     for c,w in (("file",650),("type",160)): tree.heading(c, text=c); tree.column(c, width=w, anchor="w")
   L00024:     tree.pack(fill="both", expand=True)
   L00025: 
   L00026:     def refresh():
```
- **Refresh button**: 3 hit(s) (showing up to 3)
```text
   L00017: 
   L00018: def _build_tab(parent):
   L00019:     frm = ttk.Frame(parent)
   L00020:     bar = ttk.Frame(frm); bar.pack(fill="x", pady=6)
>> L00021:     ttk.Button(bar, text="Refresh", command=lambda: refresh()).pack(side="left")
   L00022:     tree = ttk.Treeview(frm, columns=("file","type"), show="headings")
   L00023:     for c,w in (("file",650),("type",160)): tree.heading(c, text=c); tree.column(c, width=w, anchor="w")
   L00024:     tree.pack(fill="both", expand=True)
   L00025: 
```
```text
   L00022:     tree = ttk.Treeview(frm, columns=("file","type"), show="headings")
   L00023:     for c,w in (("file",650),("type",160)): tree.heading(c, text=c); tree.column(c, width=w, anchor="w")
   L00024:     tree.pack(fill="both", expand=True)
   L00025: 
>> L00026:     def refresh():
   L00027:         for i in tree.get_children(): tree.delete(i)
   L00028:         for name, typ in _list(): tree.insert("", "end", values=(name, typ))
   L00029:     def run_sel(_evt=None):
   L00030:         sel = tree.focus()
```
```text
   L00035:         except Exception as ex:
   L00036:             try: messagebox.showerror("ShrimpDev", f"Startfehler:\n{ex}")
   L00037:             except Exception: pass
   L00038:     tree.bind("<Double-1>", run_sel)
>> L00039:     refresh()
   L00040:     return frm
   L00041: 
   L00042: def open_runner_board(app: tk.Tk) -> bool:
   L00043:     try: return ensure_tab(app, "runners", "Runner Board", _build_tab)
```

### `module_runner_popup.py`
- **Scrollbars**: 2 hit(s) (showing up to 2)
```text
   L00207:         # MID: Text + Scroll
   L00208:         mid = ttk.Frame(outer)
   L00209:         mid.pack(fill="both", expand=True, pady=(8, 0))
   L00210: 
>> L00211:         yscroll = ttk.Scrollbar(mid, orient="vertical")
   L00212:         yscroll.pack(side="right", fill="y")
   L00213: 
   L00214:         txt = tk.Text(mid, wrap="word", yscrollcommand=yscroll.set)
   L00215:         txt.pack(side="left", fill="both", expand=True)
```
```text
   L00210: 
   L00211:         yscroll = ttk.Scrollbar(mid, orient="vertical")
   L00212:         yscroll.pack(side="right", fill="y")
   L00213: 
>> L00214:         txt = tk.Text(mid, wrap="word", yscrollcommand=yscroll.set)
   L00215:         txt.pack(side="left", fill="both", expand=True)
   L00216:         yscroll.configure(command=txt.yview)
   L00217:         txt.configure(state="disabled")
   L00218: 
```
- **Splitter/Resizable**: 6 hit(s) (showing up to 6)
```text
   L00325:         bottom = ttk.Frame(outer)
   L00326:         bottom.pack(fill="x", pady=(8, 0))
   L00327: 
   L00328:         # Grid: [Auto] [spacer] [Buttons...] [spacer]
>> L00329:         bottom.columnconfigure(0, weight=0)
   L00330:         bottom.columnconfigure(1, weight=1)
   L00331:         bottom.columnconfigure(2, weight=0)
   L00332:         bottom.columnconfigure(3, weight=0)
   L00333:         bottom.columnconfigure(4, weight=0)
```
```text
   L00326:         bottom.pack(fill="x", pady=(8, 0))
   L00327: 
   L00328:         # Grid: [Auto] [spacer] [Buttons...] [spacer]
   L00329:         bottom.columnconfigure(0, weight=0)
>> L00330:         bottom.columnconfigure(1, weight=1)
   L00331:         bottom.columnconfigure(2, weight=0)
   L00332:         bottom.columnconfigure(3, weight=0)
   L00333:         bottom.columnconfigure(4, weight=0)
   L00334:         bottom.columnconfigure(5, weight=1)
```
```text
   L00327: 
   L00328:         # Grid: [Auto] [spacer] [Buttons...] [spacer]
   L00329:         bottom.columnconfigure(0, weight=0)
   L00330:         bottom.columnconfigure(1, weight=1)
>> L00331:         bottom.columnconfigure(2, weight=0)
   L00332:         bottom.columnconfigure(3, weight=0)
   L00333:         bottom.columnconfigure(4, weight=0)
   L00334:         bottom.columnconfigure(5, weight=1)
   L00335: 
```
```text
   L00328:         # Grid: [Auto] [spacer] [Buttons...] [spacer]
   L00329:         bottom.columnconfigure(0, weight=0)
   L00330:         bottom.columnconfigure(1, weight=1)
   L00331:         bottom.columnconfigure(2, weight=0)
>> L00332:         bottom.columnconfigure(3, weight=0)
   L00333:         bottom.columnconfigure(4, weight=0)
   L00334:         bottom.columnconfigure(5, weight=1)
   L00335: 
   L00336:         ttk.Checkbutton(bottom, text="Auto-Scroll", variable=var_auto).grid(
```
```text
   L00329:         bottom.columnconfigure(0, weight=0)
   L00330:         bottom.columnconfigure(1, weight=1)
   L00331:         bottom.columnconfigure(2, weight=0)
   L00332:         bottom.columnconfigure(3, weight=0)
>> L00333:         bottom.columnconfigure(4, weight=0)
   L00334:         bottom.columnconfigure(5, weight=1)
   L00335: 
   L00336:         ttk.Checkbutton(bottom, text="Auto-Scroll", variable=var_auto).grid(
   L00337:             row=0, column=0, sticky="w", padx=(0, 10)
```
```text
   L00330:         bottom.columnconfigure(1, weight=1)
   L00331:         bottom.columnconfigure(2, weight=0)
   L00332:         bottom.columnconfigure(3, weight=0)
   L00333:         bottom.columnconfigure(4, weight=0)
>> L00334:         bottom.columnconfigure(5, weight=1)
   L00335: 
   L00336:         ttk.Checkbutton(bottom, text="Auto-Scroll", variable=var_auto).grid(
   L00337:             row=0, column=0, sticky="w", padx=(0, 10)
   L00338:         )
```

### `module_runnerbar.py`
- **Splitter/Resizable**: 1 hit(s) (showing up to 1)
```text
   L00042:             "Sanity R9999": "R9999.cmd",  # erscheint nur, wenn vorhanden
   L00043:         }
   L00044: 
   L00045:     bar = ttk.Frame(parent)
>> L00046:     bar.grid_columnconfigure(999, weight=1)  # Stretch rechts
   L00047: 
   L00048:     c = 0
   L00049:     for label, fname in mapping.items():
   L00050:         cmd = TOOLS / fname
```

### `ui_filters.py`
- **Refresh button**: 2 hit(s) (showing up to 2)
```text
   L00018:             os.startfile(path)
   L00019:         except Exception:
   L00020:             pass
   L00021: 
>> L00022: def refresh(app):
   L00023:     """Aktualisiert die rechte Projektliste basierend auf dem Zielordner.
   L00024: 
   L00025:     Wird u.a. von ui_left_panel._on_target_changed() genutzt.
   L00026:     """
```
```text
   L00030:         _pt._load_dir(app)
   L00031:     except Exception:
   L00032:         # Fallback: alter Mechanismus, falls right_list noch existiert
   L00033:         try:
>> L00034:             app.right_list.refresh()
   L00035:         except Exception:
   L00036:             pass
   L00037: 
   L00038: def _save_target(path: str):
```

### `ui_learningpanel.py`
- **Splitter/Resizable**: 2 hit(s) (showing up to 2)
```text
   L00027:     tk.Frame
   L00028:         Das erzeugte Frame mit Titel- und Info-Text.
   L00029:     """
   L00030:     frame = ttk.Frame(parent)
>> L00031:     frame.grid_rowconfigure(1, weight=1)
   L00032:     frame.grid_columnconfigure(0, weight=1)
   L00033: 
   L00034:     lbl_title = ttk.Label(
   L00035:         frame,
```
```text
   L00028:         Das erzeugte Frame mit Titel- und Info-Text.
   L00029:     """
   L00030:     frame = ttk.Frame(parent)
   L00031:     frame.grid_rowconfigure(1, weight=1)
>> L00032:     frame.grid_columnconfigure(0, weight=1)
   L00033: 
   L00034:     lbl_title = ttk.Label(
   L00035:         frame,
   L00036:         text="LearningEngine - Uebersicht",
```

### `ui_left_panel.py`
- **Preview**: 4 hit(s) (showing up to 4)
```text
   L00239:         else:
   L00240:             ext_show = ext
   L00241: 
   L00242:         if not name:
>> L00243:             preview = ""
   L00244:         else:
   L00245:             filename = f"{name}{ext_show}"
   L00246:             if target:
   L00247:                 preview = f"{target}\\{filename}"
```
```text
   L00243:             preview = ""
   L00244:         else:
   L00245:             filename = f"{name}{ext_show}"
   L00246:             if target:
>> L00247:                 preview = f"{target}\\{filename}"
   L00248:             else:
   L00249:                 preview = filename
   L00250: 
   L00251:         var_path_preview.set(preview)
```
```text
   L00245:             filename = f"{name}{ext_show}"
   L00246:             if target:
   L00247:                 preview = f"{target}\\{filename}"
   L00248:             else:
>> L00249:                 preview = filename
   L00250: 
   L00251:         var_path_preview.set(preview)
   L00252: 
   L00253:     # Traces fuer automatische Aktualisierung
```
```text
   L00247:                 preview = f"{target}\\{filename}"
   L00248:             else:
   L00249:                 preview = filename
   L00250: 
>> L00251:         var_path_preview.set(preview)
   L00252: 
   L00253:     # Traces fuer automatische Aktualisierung
   L00254:     def _safe_led_eval():
   L00255:         """Sichere LED-Aktualisierung fuer den Intake-Tab."""
```
- **Refresh button**: 4 hit(s) (showing up to 4)
```text
   L00098:     try:
   L00099:         if hasattr(app, "_path_changed") and callable(getattr(app, "_path_changed")):
   L00100:             app._path_changed()
   L00101:         else:
>> L00102:             ui_filters.refresh(app)
   L00103:     except Exception:
   L00104:         try:
   L00105:             ui_filters.refresh(app)
   L00106:         except Exception:
```
```text
   L00101:         else:
   L00102:             ui_filters.refresh(app)
   L00103:     except Exception:
   L00104:         try:
>> L00105:             ui_filters.refresh(app)
   L00106:         except Exception:
   L00107:             pass
   L00108: 
   L00109:     # Intake-LEDs aktualisieren
```
```text
   L00287:             pass
   L00288:         # Rechten Bereich (Projektliste) neu laden - entspricht
   L00289:         # dem "Aktualisieren"-Button im Intake.
   L00290:         try:
>> L00291:             ui_filters.refresh(app)
   L00292:         except Exception:
   L00293:             # UI soll nicht crashen, wenn refresh Probleme macht.
   L00294:             pass
   L00295:         # LED-Zustand aktualisieren
```
```text
   L00289:         # dem "Aktualisieren"-Button im Intake.
   L00290:         try:
   L00291:             ui_filters.refresh(app)
   L00292:         except Exception:
>> L00293:             # UI soll nicht crashen, wenn refresh Probleme macht.
   L00294:             pass
   L00295:         # LED-Zustand aktualisieren
   L00296:         _safe_led_eval()
   L00297: 
```

### `ui_lists.py`
- **Tree/Explorer widgets**: 1 hit(s) (showing up to 1)
```text
   L00004: _TREE = "proj_tree"
   L00005: 
   L00006: def create_tree(parent, app):
   L00007:     cols = ("path","type","note")
>> L00008:     tree = ttk.Treeview(parent, columns=cols, show="headings", name=_TREE)
   L00009:     for c in cols:
   L00010:         tree.heading(c, text=c.capitalize())
   L00011:         tree.column(c, width=260 if c=="path" else 140, anchor="w")
   L00012:     tree.pack(fill="both", expand=True, padx=12, pady=(8,12))
```

### `ui_log_tab.py`
- **Scrollbars**: 3 hit(s) (showing up to 3)
```text
   L00123:     area = ui_theme_classic.Frame(outer, bg=BG)
   L00124:     area.pack(fill="both", expand=True, padx=4, pady=(4, 4))
   L00125: 
   L00126:     text_widget = tk.Text(area, wrap="none")
>> L00127:     vsb = ttk.Scrollbar(area, orient="vertical", command=text_widget.yview)
   L00128:     hsb = ttk.Scrollbar(area, orient="horizontal", command=text_widget.xview)
   L00129: 
   L00130:     text_widget.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
   L00131: 
```
```text
   L00124:     area.pack(fill="both", expand=True, padx=4, pady=(4, 4))
   L00125: 
   L00126:     text_widget = tk.Text(area, wrap="none")
   L00127:     vsb = ttk.Scrollbar(area, orient="vertical", command=text_widget.yview)
>> L00128:     hsb = ttk.Scrollbar(area, orient="horizontal", command=text_widget.xview)
   L00129: 
   L00130:     text_widget.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
   L00131: 
   L00132:     area.grid_rowconfigure(0, weight=1)
```
```text
   L00126:     text_widget = tk.Text(area, wrap="none")
   L00127:     vsb = ttk.Scrollbar(area, orient="vertical", command=text_widget.yview)
   L00128:     hsb = ttk.Scrollbar(area, orient="horizontal", command=text_widget.xview)
   L00129: 
>> L00130:     text_widget.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
   L00131: 
   L00132:     area.grid_rowconfigure(0, weight=1)
   L00133:     area.grid_columnconfigure(0, weight=1)
   L00134: 
```
- **Splitter/Resizable**: 2 hit(s) (showing up to 2)
```text
   L00128:     hsb = ttk.Scrollbar(area, orient="horizontal", command=text_widget.xview)
   L00129: 
   L00130:     text_widget.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
   L00131: 
>> L00132:     area.grid_rowconfigure(0, weight=1)
   L00133:     area.grid_columnconfigure(0, weight=1)
   L00134: 
   L00135:     text_widget.grid(row=0, column=0, sticky="nsew")
   L00136:     vsb.grid(row=0, column=1, sticky="ns")
```
```text
   L00129: 
   L00130:     text_widget.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
   L00131: 
   L00132:     area.grid_rowconfigure(0, weight=1)
>> L00133:     area.grid_columnconfigure(0, weight=1)
   L00134: 
   L00135:     text_widget.grid(row=0, column=0, sticky="nsew")
   L00136:     vsb.grid(row=0, column=1, sticky="ns")
   L00137:     hsb.grid(row=1, column=0, sticky="ew")
```

### `ui_menus.py`
- **Context menu**: 5 hit(s) (showing up to 5)
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
```
```text
   L00002: from tkinter import messagebox
   L00003: 
   L00004: def build_menu(app):
   L00005:     m = tk.Menu(app)
>> L00006:     file = tk.Menu(m, tearoff=False)
   L00007:     file.add_checkbutton(label="Always on Top",
   L00008:                          command=lambda: _toggle_top(app))
   L00009:     file.add_separator()
   L00010:     file.add_command(label="Beenden", command=app.destroy)
```
```text
   L00006:     file = tk.Menu(m, tearoff=False)
   L00007:     file.add_checkbutton(label="Always on Top",
   L00008:                          command=lambda: _toggle_top(app))
   L00009:     file.add_separator()
>> L00010:     file.add_command(label="Beenden", command=app.destroy)
   L00011:     m.add_cascade(label="File", menu=file)
   L00012: 
   L00013:     helpm = tk.Menu(m, tearoff=False)
   L00014:     helpm.add_command(label="Info", command=lambda: messagebox.showinfo("ShrimpDev", "ShrimpDev - Development GUI"))
```
```text
   L00009:     file.add_separator()
   L00010:     file.add_command(label="Beenden", command=app.destroy)
   L00011:     m.add_cascade(label="File", menu=file)
   L00012: 
>> L00013:     helpm = tk.Menu(m, tearoff=False)
   L00014:     helpm.add_command(label="Info", command=lambda: messagebox.showinfo("ShrimpDev", "ShrimpDev - Development GUI"))
   L00015:     m.add_cascade(label="Help", menu=helpm)
   L00016: 
   L00017:     app.config(menu=m)
```
```text
   L00010:     file.add_command(label="Beenden", command=app.destroy)
   L00011:     m.add_cascade(label="File", menu=file)
   L00012: 
   L00013:     helpm = tk.Menu(m, tearoff=False)
>> L00014:     helpm.add_command(label="Info", command=lambda: messagebox.showinfo("ShrimpDev", "ShrimpDev - Development GUI"))
   L00015:     m.add_cascade(label="Help", menu=helpm)
   L00016: 
   L00017:     app.config(menu=m)
   L00018: 
```

### `ui_pipeline_tab.py`
- **Tree/Explorer widgets**: 3 hit(s) (showing up to 3)
```text
   L00016: 
   L00017: 
   L00018: def build_pipeline_tab(parent, app) -> None:
   L00019:     # PIPELINE_TREEVIEW_R2156
>> L00020:     # UX+Debug: Task-Liste (Treeview) + Toggle + Filter + Summary + Auto-Reload + Diagnose
   L00021: 
   L00022:     header = ttk.Label(parent, text="Pipeline", anchor="w")
   L00023:     # PIPELINE_UX_R2166
   L00024: 
```
```text
   L00064:     cols = ("status", "prio", "task", "section")
   L00065: 
   L00066:     style = ttk.Style()
   L00067:     try:
>> L00068:         style.configure("Pipeline.Treeview", rowheight=22)
   L00069:     except Exception:
   L00070:         pass
   L00071: 
   L00072:     tree = ttk.Treeview(content, columns=cols, show="headings", selectmode="browse", style="Pipeline.Treeview")
```
```text
   L00068:         style.configure("Pipeline.Treeview", rowheight=22)
   L00069:     except Exception:
   L00070:         pass
   L00071: 
>> L00072:     tree = ttk.Treeview(content, columns=cols, show="headings", selectmode="browse", style="Pipeline.Treeview")
   L00073:     tree.heading("status", text="Status")
   L00074:     tree.heading("prio", text="Prio")
   L00075:     tree.heading("task", text="Task")
   L00076:     tree.heading("section", text="Section")
```
- **Scrollbars**: 2 hit(s) (showing up to 2)
```text
   L00111:     except Exception:
   L00112:         pass
   L00113: 
   L00114: 
>> L00115:     scr = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
   L00116:     tree.configure(yscrollcommand=scr.set)
   L00117:     tree.pack(side="left", fill="both", expand=True)
   L00118:     scr.pack(side="right", fill="y")
   L00119: 
```
```text
   L00112:         pass
   L00113: 
   L00114: 
   L00115:     scr = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
>> L00116:     tree.configure(yscrollcommand=scr.set)
   L00117:     tree.pack(side="left", fill="both", expand=True)
   L00118:     scr.pack(side="right", fill="y")
   L00119: 
   L00120:     empty = ttk.Label(parent, text="", anchor="w")
```

### `ui_project_tree.py`
- **Tree/Explorer widgets**: 3 hit(s) (showing up to 3)
```text
   L00262: 
   L00263: 
   L00264:     # Tree + Scrollbar
   L00265:     cols = ("name", "ext", "date", "time")
>> L00266:     tree = ttk.Treeview(wrap, columns=cols, show="headings", selectmode="extended")
   L00267:     vsb = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
   L00268:     tree.configure(yscrollcommand=vsb.set)
   L00269: 
   L00270:     tree.pack(side="left", fill="both", expand=True)
```
```text
   L00743: 
   L00744: 
   L00745: def enable_lasso(app) -> None:
   L00746:     """
>> L00747:     Aktiviert einen einfachen Lasso-/Drag-Multiselect auf der TreeView.
   L00748: 
   L00749:     Verhalten:
   L00750:     - Linke Maustaste gedrueckt halten und ueber Eintraege fahren:
   L00751:       Eintraege werden beim Ueberfahren der Maus zur Auswahl hinzugefuegt.
```
```text
   L00806: 
   L00807: 
   L00808: def enable_context_menu(app) -> None:
   L00809:     """
>> L00810:     Aktiviert ein Kontextmenue auf der TreeView (rechte Liste):
   L00811: 
   L00812:     - Rechtsklick auf einen Eintrag:
   L00813:         * Auswahl ggf. auf diesen Eintrag setzen
   L00814:         * Menue mit "Pfad(e) kopieren" anzeigen
```
- **Context menu**: 4 hit(s) (showing up to 4)
```text
   L00824: 
   L00825:     # Lokaler Import, um keine globalen Abhaengigkeiten zu erzwingen
   L00826:     import tkinter as tk
   L00827: 
>> L00828:     menu = tk.Menu(tree, tearoff=False)
   L00829: 
   L00830:     def _copy_selected():
   L00831:         try:
   L00832:             sel = tree.selection()
```
```text
   L00852:         except Exception:
   L00853:             # Clipboard darf nie crashen
   L00854:             pass
   L00855: 
>> L00856:     menu.add_command(label="Pfad(e) kopieren", command=_copy_selected)
   L00857: 
   L00858:     def _on_context(event):
   L00859:         try:
   L00860:             # Row unter Maus ermitteln
```
```text
   L00874:                         else:
   L00875:                             tree.selection_set(row)
   L00876:                     except Exception:
   L00877:                         tree.selection_set(row)
>> L00878:             menu.tk_popup(event.x_root, event.y_root)
   L00879:         finally:
   L00880:             try:
   L00881:                 menu.grab_release()
   L00882:             except Exception:
```
```text
   L00882:             except Exception:
   L00883:                 pass
   L00884: 
   L00885:     try:
>> L00886:         tree.bind("<Button-3>", _on_context, add="+")
   L00887:     except Exception:
   L00888:         pass
   L00889: 
```
- **Refresh button**: 2 hit(s) (showing up to 2)
```text
   L00611:     return result
   L00612: 
   L00613: 
   L00614: class RightListProxy:
>> L00615:     """Kleine Hülle mit refresh()-Methode für die rechte Liste."""
   L00616: 
   L00617:     def __init__(self, app):
   L00618:         self._app = app
   L00619: 
```
```text
   L00616: 
   L00617:     def __init__(self, app):
   L00618:         self._app = app
   L00619: 
>> L00620:     def refresh(self) -> None:
   L00621:         try:
   L00622:             _load_dir(self._app)
   L00623:         except Exception:
   L00624:             pass
```
- **Scrollbars**: 3 hit(s) (showing up to 3)
```text
   L00260:     btn_snaps = ui_theme_classic.Button(row_actions, text="Snapshots", command=_btn_open_snapshots, width=10)
   L00261:     btn_explorer = ui_theme_classic.Button(row_actions, text="Explorer", command=_btn_open_explorer, width=10)
   L00262: 
   L00263: 
>> L00264:     # Tree + Scrollbar
   L00265:     cols = ("name", "ext", "date", "time")
   L00266:     tree = ttk.Treeview(wrap, columns=cols, show="headings", selectmode="extended")
   L00267:     vsb = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
   L00268:     tree.configure(yscrollcommand=vsb.set)
```
```text
   L00263: 
   L00264:     # Tree + Scrollbar
   L00265:     cols = ("name", "ext", "date", "time")
   L00266:     tree = ttk.Treeview(wrap, columns=cols, show="headings", selectmode="extended")
>> L00267:     vsb = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
   L00268:     tree.configure(yscrollcommand=vsb.set)
   L00269: 
   L00270:     tree.pack(side="left", fill="both", expand=True)
   L00271:     vsb.pack(side="right", fill="y")
```
```text
   L00264:     # Tree + Scrollbar
   L00265:     cols = ("name", "ext", "date", "time")
   L00266:     tree = ttk.Treeview(wrap, columns=cols, show="headings", selectmode="extended")
   L00267:     vsb = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
>> L00268:     tree.configure(yscrollcommand=vsb.set)
   L00269: 
   L00270:     tree.pack(side="left", fill="both", expand=True)
   L00271:     vsb.pack(side="right", fill="y")
   L00272: 
```

### `ui_runner_products_tab.py`
- **Tree/Explorer widgets**: 1 hit(s) (showing up to 1)
```text
   L00310:     ent_q.pack(side="left", fill="x", expand=True, padx=(4, 0))
   L00311: 
   L00312:     # Tree
   L00313:     cols = ("mtime", "type", "runner", "name", "size")
>> L00314:     tree = ttk.Treeview(left, columns=cols, show="headings", height=18)
   L00315:     tree.heading("mtime", text="Zeit")
   L00316:     tree.heading("type", text="Typ")
   L00317:     tree.heading("runner", text="Runner")
   L00318:     tree.heading("name", text="Datei")
```
- **Context menu**: 8 hit(s) (showing up to 8)
```text
   L00487:     except Exception:
   L00488:         pass
   L00489: 
   L00490: 
>> L00491:     # --- R2303 TREE UX: Click / Context / Copy --------------------------------------
   L00492:     _R2303_MAX_COPY_BYTES = 512 * 1024  # 512 KB
   L00493: 
   L00494:     def _on_copy_content():
   L00495:         p = _selected_path()
```
```text
   L00544:         if not p:
   L00545:             return
   L00546: 
   L00547:         try:
>> L00548:             m = tk.Menu(tree, tearoff=0)
   L00549:             m.add_command(label="Intern anzeigen", command=_on_viewer)
   L00550:             m.add_command(label="Öffnen", command=_on_open)
   L00551:             m.add_command(label="Ordner öffnen", command=_on_folder)
   L00552:             m.add_separator()
```
```text
   L00545:             return
   L00546: 
   L00547:         try:
   L00548:             m = tk.Menu(tree, tearoff=0)
>> L00549:             m.add_command(label="Intern anzeigen", command=_on_viewer)
   L00550:             m.add_command(label="Öffnen", command=_on_open)
   L00551:             m.add_command(label="Ordner öffnen", command=_on_folder)
   L00552:             m.add_separator()
   L00553:             m.add_command(label="Pfad kopieren", command=_on_copy)
```
```text
   L00546: 
   L00547:         try:
   L00548:             m = tk.Menu(tree, tearoff=0)
   L00549:             m.add_command(label="Intern anzeigen", command=_on_viewer)
>> L00550:             m.add_command(label="Öffnen", command=_on_open)
   L00551:             m.add_command(label="Ordner öffnen", command=_on_folder)
   L00552:             m.add_separator()
   L00553:             m.add_command(label="Pfad kopieren", command=_on_copy)
   L00554:             m.add_command(label="Inhalt kopieren (Text)", command=_on_copy_content)
```
```text
   L00547:         try:
   L00548:             m = tk.Menu(tree, tearoff=0)
   L00549:             m.add_command(label="Intern anzeigen", command=_on_viewer)
   L00550:             m.add_command(label="Öffnen", command=_on_open)
>> L00551:             m.add_command(label="Ordner öffnen", command=_on_folder)
   L00552:             m.add_separator()
   L00553:             m.add_command(label="Pfad kopieren", command=_on_copy)
   L00554:             m.add_command(label="Inhalt kopieren (Text)", command=_on_copy_content)
   L00555:             m.tk_popup(ev.x_root, ev.y_root)
```
```text
   L00549:             m.add_command(label="Intern anzeigen", command=_on_viewer)
   L00550:             m.add_command(label="Öffnen", command=_on_open)
   L00551:             m.add_command(label="Ordner öffnen", command=_on_folder)
   L00552:             m.add_separator()
>> L00553:             m.add_command(label="Pfad kopieren", command=_on_copy)
   L00554:             m.add_command(label="Inhalt kopieren (Text)", command=_on_copy_content)
   L00555:             m.tk_popup(ev.x_root, ev.y_root)
   L00556:         except Exception:
   L00557:             pass
```
```text
   L00550:             m.add_command(label="Öffnen", command=_on_open)
   L00551:             m.add_command(label="Ordner öffnen", command=_on_folder)
   L00552:             m.add_separator()
   L00553:             m.add_command(label="Pfad kopieren", command=_on_copy)
>> L00554:             m.add_command(label="Inhalt kopieren (Text)", command=_on_copy_content)
   L00555:             m.tk_popup(ev.x_root, ev.y_root)
   L00556:         except Exception:
   L00557:             pass
   L00558: 
```
```text
   L00551:             m.add_command(label="Ordner öffnen", command=_on_folder)
   L00552:             m.add_separator()
   L00553:             m.add_command(label="Pfad kopieren", command=_on_copy)
   L00554:             m.add_command(label="Inhalt kopieren (Text)", command=_on_copy_content)
>> L00555:             m.tk_popup(ev.x_root, ev.y_root)
   L00556:         except Exception:
   L00557:             pass
   L00558: 
   L00559:     try:
```
- **Preview**: 4 hit(s) (showing up to 4)
```text
   L00283: 
   L00284:     mid = tk.Frame(container, bg=bg)
   L00285:     mid.pack(fill="both", expand=True, padx=8, pady=(0, 8))
   L00286: 
>> L00287:     # Left: list, Right: preview
   L00288:     left = tk.Frame(mid, bg=bg)
   L00289:     left.pack(side="left", fill="both", expand=True)
   L00290:     right = tk.Frame(mid, bg=bg)
   L00291:     right.pack(side="right", fill="both", expand=True)
```
```text
   L00327:     sb = ttk.Scrollbar(left, orient="vertical", command=tree.yview)
   L00328:     sb.pack(side="right", fill="y")
   L00329:     tree.configure(yscrollcommand=sb.set)
   L00330: 
>> L00331:     # Preview
   L00332:     tk.Label(right, text="Preview", bg=bg).pack(anchor="w")
   L00333:     txt = tk.Text(right, wrap="word")
   L00334:     txt.pack(fill="both", expand=True)
   L00335: 
```
```text
   L00328:     sb.pack(side="right", fill="y")
   L00329:     tree.configure(yscrollcommand=sb.set)
   L00330: 
   L00331:     # Preview
>> L00332:     tk.Label(right, text="Preview", bg=bg).pack(anchor="w")
   L00333:     txt = tk.Text(right, wrap="word")
   L00334:     txt.pack(fill="both", expand=True)
   L00335: 
   L00336:     # Actions
```
```text
   L00412:         if not path:
   L00413:             return
   L00414:         try:
   L00415:             if os.path.getsize(path) > 2 * 1024 * 1024:
>> L00416:                 txt.insert("end", "(Datei zu groß für Preview > 2MB)\n" + path)
   L00417:                 return
   L00418:         except Exception:
   L00419:             pass
   L00420:         try:
```
- **Refresh button**: 1 hit(s) (showing up to 1)
```text
   L00277:     top.pack(fill="x", padx=8, pady=6)
   L00278: 
   L00279:     tk.Label(top, text="Artefakte (Read-Only)", bg=bg).pack(side="left")
   L00280: 
>> L00281:     btn_refresh = tk.Button(top, text="Refresh")
   L00282:     btn_refresh.pack(side="right")
   L00283: 
   L00284:     mid = tk.Frame(container, bg=bg)
   L00285:     mid.pack(fill="both", expand=True, padx=8, pady=(0, 8))
```
- **Scrollbars**: 6 hit(s) (showing up to 6)
```text
   L00137: 
   L00138:     txt = tk.Text(mid, wrap="none")
   L00139:     txt.pack(side="left", fill="both", expand=True)
   L00140: 
>> L00141:     sb_y = tk.Scrollbar(mid, orient="vertical", command=txt.yview)
   L00142:     sb_y.pack(side="right", fill="y")
   L00143:     txt.configure(yscrollcommand=sb_y.set)
   L00144: 
   L00145:     sb_x = tk.Scrollbar(win, orient="horizontal", command=txt.xview)
```
```text
   L00139:     txt.pack(side="left", fill="both", expand=True)
   L00140: 
   L00141:     sb_y = tk.Scrollbar(mid, orient="vertical", command=txt.yview)
   L00142:     sb_y.pack(side="right", fill="y")
>> L00143:     txt.configure(yscrollcommand=sb_y.set)
   L00144: 
   L00145:     sb_x = tk.Scrollbar(win, orient="horizontal", command=txt.xview)
   L00146:     sb_x.pack(side="bottom", fill="x")
   L00147:     txt.configure(xscrollcommand=sb_x.set)
```
```text
   L00141:     sb_y = tk.Scrollbar(mid, orient="vertical", command=txt.yview)
   L00142:     sb_y.pack(side="right", fill="y")
   L00143:     txt.configure(yscrollcommand=sb_y.set)
   L00144: 
>> L00145:     sb_x = tk.Scrollbar(win, orient="horizontal", command=txt.xview)
   L00146:     sb_x.pack(side="bottom", fill="x")
   L00147:     txt.configure(xscrollcommand=sb_x.set)
   L00148: 
   L00149:     # Load content (best effort)
```
```text
   L00143:     txt.configure(yscrollcommand=sb_y.set)
   L00144: 
   L00145:     sb_x = tk.Scrollbar(win, orient="horizontal", command=txt.xview)
   L00146:     sb_x.pack(side="bottom", fill="x")
>> L00147:     txt.configure(xscrollcommand=sb_x.set)
   L00148: 
   L00149:     # Load content (best effort)
   L00150:     try:
   L00151:         data = path.read_text(encoding="utf-8", errors="replace")
```
```text
   L00323:     tree.column("name", width=360, anchor="w")
   L00324:     tree.column("size", width=80, anchor="e")
   L00325:     tree.pack(side="left", fill="both", expand=True)
   L00326: 
>> L00327:     sb = ttk.Scrollbar(left, orient="vertical", command=tree.yview)
   L00328:     sb.pack(side="right", fill="y")
   L00329:     tree.configure(yscrollcommand=sb.set)
   L00330: 
   L00331:     # Preview
```
```text
   L00325:     tree.pack(side="left", fill="both", expand=True)
   L00326: 
   L00327:     sb = ttk.Scrollbar(left, orient="vertical", command=tree.yview)
   L00328:     sb.pack(side="right", fill="y")
>> L00329:     tree.configure(yscrollcommand=sb.set)
   L00330: 
   L00331:     # Preview
   L00332:     tk.Label(right, text="Preview", bg=bg).pack(anchor="w")
   L00333:     txt = tk.Text(right, wrap="word")
```

### `ui_settings_tab.py`
- **Splitter/Resizable**: 1 hit(s) (showing up to 1)
```text
   L00097:     btn_save = ttk.Button(frame, text="Einstellungen speichern", command=on_save)
   L00098:     btn_save.grid(row=2, column=0, columnspan=3, sticky="e")
   L00099: 
   L00100:     # Grid-Konfiguration
>> L00101:     frame.columnconfigure(1, weight=1)
   L00102: 
   L00103:     return frame
```

### `ui_theme_classic.py`
- **Tree/Explorer widgets**: 2 hit(s) (showing up to 2)
```text
   L00030:     style.map("TNotebook.Tab",
   L00031:               background=[("selected", "white")],
   L00032:               foreground=[("selected", "black")])
   L00033: 
>> L00034:     # Treeview
   L00035:     style.configure("Treeview",
   L00036:                     background="white",
   L00037:                     fieldbackground="white",
   L00038:                     foreground="black")
```
```text
   L00031:               background=[("selected", "white")],
   L00032:               foreground=[("selected", "black")])
   L00033: 
   L00034:     # Treeview
>> L00035:     style.configure("Treeview",
   L00036:                     background="white",
   L00037:                     fieldbackground="white",
   L00038:                     foreground="black")
   L00039: 
```

### `ui_toolbar.py`
- **Refresh button**: 8 hit(s) (showing up to 8)
```text
   L00125:             # R1838: rechte Liste / Tree nach jeder Toolbar-Aktion aktualisieren
   L00126:             try:
   L00127:                 _r1838_refresh_right_list(app)
   L00128:             except Exception:
>> L00129:                 # Refresh-Fehler duerfen die UI ebenfalls nicht crashen
   L00130:                 pass
   L00131:     return _inner
   L00132: 
   L00133: 
```
```text
   L00164: 
   L00165: def _r1838_refresh_right_list(app):
   L00166: 
   L00167:     """
>> L00168:     R1838: Zentraler Refresh-Helfer fuer rechte Liste / Tree.
   L00169: 
   L00170:     Versucht nacheinander:
   L00171:     - ui_filters.refresh(app)
   L00172:     - right_list.refresh() (Proxy)
```
```text
   L00167:     """
   L00168:     R1838: Zentraler Refresh-Helfer fuer rechte Liste / Tree.
   L00169: 
   L00170:     Versucht nacheinander:
>> L00171:     - ui_filters.refresh(app)
   L00172:     - right_list.refresh() (Proxy)
   L00173:     """
   L00174:     # 1) Bevorzugt neue Refresh-Logik ueber ui_filters
   L00175:     try:
```
```text
   L00168:     R1838: Zentraler Refresh-Helfer fuer rechte Liste / Tree.
   L00169: 
   L00170:     Versucht nacheinander:
   L00171:     - ui_filters.refresh(app)
>> L00172:     - right_list.refresh() (Proxy)
   L00173:     """
   L00174:     # 1) Bevorzugt neue Refresh-Logik ueber ui_filters
   L00175:     try:
   L00176:         from modules import ui_filters
```
```text
   L00170:     Versucht nacheinander:
   L00171:     - ui_filters.refresh(app)
   L00172:     - right_list.refresh() (Proxy)
   L00173:     """
>> L00174:     # 1) Bevorzugt neue Refresh-Logik ueber ui_filters
   L00175:     try:
   L00176:         from modules import ui_filters
   L00177:         ui_filters.refresh(app)
   L00178:         return
```
```text
   L00173:     """
   L00174:     # 1) Bevorzugt neue Refresh-Logik ueber ui_filters
   L00175:     try:
   L00176:         from modules import ui_filters
>> L00177:         ui_filters.refresh(app)
   L00178:         return
   L00179:     except Exception:
   L00180:         pass
   L00181:     # 2) Fallback: RightListProxy oder aehnliche Wrapper
```
```text
   L00180:         pass
   L00181:     # 2) Fallback: RightListProxy oder aehnliche Wrapper
   L00182:     try:
   L00183:         proxy = getattr(app, "right_list", None)
>> L00184:         if proxy is not None and hasattr(proxy, "refresh"):
   L00185:             proxy.refresh()
   L00186:     except Exception:
   L00187:         pass
   L00188: 
```
```text
   L00181:     # 2) Fallback: RightListProxy oder aehnliche Wrapper
   L00182:     try:
   L00183:         proxy = getattr(app, "right_list", None)
   L00184:         if proxy is not None and hasattr(proxy, "refresh"):
>> L00185:             proxy.refresh()
   L00186:     except Exception:
   L00187:         pass
   L00188: 
   L00189: 
```
- **Scrollbars**: 3 hit(s) (showing up to 3)
```text
   L00346:         info_label.grid(row=0, column=0, sticky="w")
   L00347: 
   L00348:         state = {"older_loaded": False}
   L00349: 
>> L00350:         # Text + Scrollbar
   L00351:         txt = tk.Text(win, wrap="none")
   L00352:         scroll = tk.Scrollbar(win, orient="vertical", command=txt.yview)
   L00353:         txt.configure(yscrollcommand=scroll.set)
   L00354: 
```
```text
   L00348:         state = {"older_loaded": False}
   L00349: 
   L00350:         # Text + Scrollbar
   L00351:         txt = tk.Text(win, wrap="none")
>> L00352:         scroll = tk.Scrollbar(win, orient="vertical", command=txt.yview)
   L00353:         txt.configure(yscrollcommand=scroll.set)
   L00354: 
   L00355:         txt.grid(row=1, column=0, sticky="nsew")
   L00356:         scroll.grid(row=1, column=1, sticky="ns")
```
```text
   L00349: 
   L00350:         # Text + Scrollbar
   L00351:         txt = tk.Text(win, wrap="none")
   L00352:         scroll = tk.Scrollbar(win, orient="vertical", command=txt.yview)
>> L00353:         txt.configure(yscrollcommand=scroll.set)
   L00354: 
   L00355:         txt.grid(row=1, column=0, sticky="nsew")
   L00356:         scroll.grid(row=1, column=1, sticky="ns")
   L00357: 
```
- **Splitter/Resizable**: 5 hit(s) (showing up to 5)
```text
   L00333:                 # Fallback: Standard-Placement
   L00334:                 pass
   L00335: 
   L00336:         # Layout fuer Inhalt
>> L00337:         win.rowconfigure(1, weight=1)
   L00338:         win.columnconfigure(0, weight=1)
   L00339: 
   L00340:         # Oberer Bereich nur mit Info-Label
   L00341:         top_frame = tk.Frame(win)
```
```text
   L00334:                 pass
   L00335: 
   L00336:         # Layout fuer Inhalt
   L00337:         win.rowconfigure(1, weight=1)
>> L00338:         win.columnconfigure(0, weight=1)
   L00339: 
   L00340:         # Oberer Bereich nur mit Info-Label
   L00341:         top_frame = tk.Frame(win)
   L00342:         top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=4, pady=(4, 0))
```
```text
   L00339: 
   L00340:         # Oberer Bereich nur mit Info-Label
   L00341:         top_frame = tk.Frame(win)
   L00342:         top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=4, pady=(4, 0))
>> L00343:         top_frame.columnconfigure(0, weight=1)
   L00344: 
   L00345:         info_label = tk.Label(top_frame, text="Letzter Runner-Block aus debug_output.txt")
   L00346:         info_label.grid(row=0, column=0, sticky="w")
   L00347: 
```
```text
   L00366:         bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=4, pady=(4, 6))
   L00367: 
   L00368:         # 0 und 5 tragen die Flexbreite, 1–4 Buttons = zentrierte Gruppe
   L00369:         for col in range(6):
>> L00370:             weight = 1 if col in (0, 5) else 0
   L00371:             bottom_frame.columnconfigure(col, weight=weight)
   L00372: 
   L00373:         def _load_older():
   L00374:             if state["older_loaded"]:
```
```text
   L00367: 
   L00368:         # 0 und 5 tragen die Flexbreite, 1–4 Buttons = zentrierte Gruppe
   L00369:         for col in range(6):
   L00370:             weight = 1 if col in (0, 5) else 0
>> L00371:             bottom_frame.columnconfigure(col, weight=weight)
   L00372: 
   L00373:         def _load_older():
   L00374:             if state["older_loaded"]:
   L00375:                 return
```

### `workspace_registry.py`
- **Refresh button**: 1 hit(s) (showing up to 1)
```text
   L00132:         ws = data.get("workspaces", {})
   L00133:         if name not in ws:
   L00134:             return False
   L00135:         data["active"] = str(name)
>> L00136:         # refresh validation/last_seen
   L00137:         _ = load_registry(project_root)  # normalize once
   L00138:         data = load_registry(project_root)
   L00139:         data["active"] = str(name)
   L00140:         return save_registry(data, project_root)
```

## Next step
- Use the above file/line anchors to create minimal Patch-Runners for:
  - Tree context menu (copy file, restore backup-if-backup)
  - Preview context menu + buttons below
  - Refresh button move to bottom-right
  - Scrollbars + resizable splitter
