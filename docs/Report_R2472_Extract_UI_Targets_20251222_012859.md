# R2472 – Extract UI Targets (READ-ONLY)

- Time: 20251222_012859
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`

## Extracts

### `modules/ui_project_tree.py`
- Range: L808–L889

```text
L00808: def enable_context_menu(app) -> None:
L00809:     """
L00810:     Aktiviert ein Kontextmenue auf der TreeView (rechte Liste):
L00811: 
L00812:     - Rechtsklick auf einen Eintrag:
L00813:         * Auswahl ggf. auf diesen Eintrag setzen
L00814:         * Menue mit "Pfad(e) kopieren" anzeigen
L00815:     - "Pfad(e) kopieren":
L00816:         * Alle selektierten Pfade (tree_paths) werden in die Zwischenablage
L00817:           kopiert (als Zeilenliste).
L00818:     """
L00819:     tree = getattr(app, "tree", None)
L00820:     paths = getattr(app, "tree_paths", {})
L00821: 
L00822:     if tree is None:
L00823:         return
L00824: 
L00825:     # Lokaler Import, um keine globalen Abhaengigkeiten zu erzwingen
L00826:     import tkinter as tk
L00827: 
L00828:     menu = tk.Menu(tree, tearoff=False)
L00829: 
L00830:     def _copy_selected():
L00831:         try:
L00832:             sel = tree.selection()
L00833:         except Exception:
L00834:             sel = ()
L00835:         collected: list[str] = []
L00836:         try:
L00837:             for item in sel:
L00838:                 try:
L00839:                     p = paths.get(item)
L00840:                 except Exception:
L00841:                     p = None
L00842:                 if p:
L00843:                     collected.append(str(p))
L00844:         except Exception:
L00845:             collected = []
L00846: 
L00847:         data = "\n".join(collected)
L00848:         try:
L00849:             app.clipboard_clear()
L00850:             if data:
L00851:                 app.clipboard_append(data)
L00852:         except Exception:
L00853:             # Clipboard darf nie crashen
L00854:             pass
L00855: 
L00856:     menu.add_command(label="Pfad(e) kopieren", command=_copy_selected)
L00857: 
L00858:     def _on_context(event):
L00859:         try:
L00860:             # Row unter Maus ermitteln
L00861:             row = tree.identify_row(event.y)
L00862:             if row:
L00863:                 try:
L00864:                     current_sel = tree.selection()
L00865:                 except Exception:
L00866:                     current_sel = ()
L00867:                 # Wenn der angeklickte Eintrag noch nicht selektiert ist,
L00868:                 # ihn selektieren (alleine oder additiv, je nach Modifier)
L00869:                 if row not in current_sel:
L00870:                     # Strg gedrueckt? -> additiv, sonst Selektion ersetzen
L00871:                     try:
L00872:                         if (event.state & 0x0004):  # Control-Key
L00873:                             tree.selection_add(row)
L00874:                         else:
L00875:                             tree.selection_set(row)
L00876:                     except Exception:
L00877:                         tree.selection_set(row)
L00878:             menu.tk_popup(event.x_root, event.y_root)
L00879:         finally:
L00880:             try:
L00881:                 menu.grab_release()
L00882:             except Exception:
L00883:                 pass
L00884: 
L00885:     try:
L00886:         tree.bind("<Button-3>", _on_context, add="+")
L00887:     except Exception:
L00888:         pass
L00889: 
```

### `modules/logic_actions.py`
- Range: L1009–L1229

```text
L01009:     menu = _r1848_tk.Menu(tree, tearoff=False)
L01010: 
L01011:     def _update_selection(event):
L01012:         try:
L01013:             row_id = tree.identify_row(event.y)
L01014:             if row_id:
L01015:                 tree.selection_set(row_id)
L01016:         except Exception:
L01017:             pass
L01018: 
L01019:     def _cmd_open_intake():
L01020:         try:
L01021:             from modules.ui_project_tree import open_selected_in_intake  # type: ignore
L01022:             open_selected_in_intake(app)
L01023:         except Exception:
L01024:             pass
L01025: 
L01026:     def _cmd_open_explorer():
L01027:         try:
L01028:             action_tree_open_in_explorer(app)
L01029:         except Exception:
L01030:             pass
L01031: 
L01032:     def _cmd_copy_path():
L01033:         try:
L01034:             action_tree_copy_path(app)
L01035:         except Exception:
L01036:             pass
L01037: 
L01038:     def _cmd_rename():
L01039:         try:
L01040:             action_tree_rename(app)
L01041:         except Exception:
L01042:             pass
L01043: 
L01044:     def _cmd_trash():
L01045:         try:
L01046:             action_tree_delete(app)
L01047:         except Exception:
L01048:             pass
L01049: 
L01050:     menu.add_command(label="In Intake laden", command=_cmd_open_intake)
L01051:     menu.add_command(label="Explorer öffnen", command=_cmd_open_explorer)
L01052:     menu.add_command(label="Pfad kopieren", command=_cmd_copy_path)
L01053:     menu.add_separator()
L01054:     menu.add_command(label="Umbenennen…", command=_cmd_rename)
L01055:     menu.add_command(label="In den Papierkorb", command=_cmd_trash)
L01056: 
L01057:     def _on_button3(event, _menu=menu):
L01058:         _update_selection(event)
L01059:         try:
L01060:             _menu.tk_popup(event.x_root, event.y_root)
L01061:         finally:
L01062:             try:
L01063:                 _menu.grab_release()
L01064:             except Exception:
L01065:                 pass
L01066: 
L01067:     try:
L01068:         tree.bind("<Button-3>", lambda event: _on_button3(event), add="+")
L01069:     except Exception:
L01070:         pass
L01071: 
L01072: # build_tree aus ui_project_tree wrappen, damit Kontextmenue nach dem Aufbau gesetzt wird
L01073: try:
L01074:     from modules import ui_project_tree as _r1848_uipt  # type: ignore
L01075:     _r1848_orig_build_tree = getattr(_r1848_uipt, "build_tree", None)
L01076: except Exception:
L01077:     _r1848_orig_build_tree = None
L01078: 
L01079: def _r1848_install_build_tree_wrapper():
L01080:     if _r1848_orig_build_tree is None:
L01081:         return
L01082: 
L01083:     def _wrapped_build_tree(parent, app):
L01084:         result = _r1848_orig_build_tree(parent, app)
L01085:         try:
L01086:             _r1848_attach_context_menu(app)
L01087:         except Exception:
L01088:             pass
L01089:         return result
L01090: 
L01091:     try:
L01092:         _r1848_uipt.build_tree = _wrapped_build_tree  # type: ignore
L01093:     except Exception:
L01094:         pass
L01095: 
L01096: _r1848_install_build_tree_wrapper()
L01097: 
L01098: # R1848_END_TREE_CONTEXT_MENU
L01099: # R1851_START_RUNNERPOPUPS_INI
L01100: # SonderRunner-Popups mit Persistenz in ShrimpDev.ini ([RunnerPopups]).
L01101: 
L01102: import os as _r1851_os
L01103: import subprocess as _r1851_sub
L01104: import threading as _r1851_thread
L01105: 
L01106: try:
L01107:     import tkinter as _r1851_tk
L01108:     from tkinter import messagebox as _r1851_mb
L01109:     import tkinter.font as _r1851_font
L01110: except Exception:
L01111:     _r1851_tk = None
L01112:     _r1851_mb = None
L01113:     _r1851_font = None
L01114: 
L01115: def _r1851_load_ini():
L01116:     '''ShrimpDev.ini ueber modules.config_loader.load() einlesen.'''
L01117:     try:
L01118:         from modules import config_loader as _r1851_cfg  # type: ignore
L01119:     except Exception:
L01120:         return None
L01121:     try:
L01122:         return _r1851_cfg.load()
L01123:     except Exception:
L01124:         return None
L01125: 
L01126: def _r1851_save_ini(cfg):
L01127:     '''ShrimpDev.ini ueber modules.config_loader.save() speichern.'''
L01128:     try:
L01129:         from modules import config_loader as _r1851_cfg  # type: ignore
L01130:     except Exception:
L01131:         return
L01132:     try:
L01133:         _r1851_cfg.save(cfg)
L01134:     except Exception:
L01135:         return
L01136: 
L01137: def _r1851_get_runnerpopup_flag(runner_id: str) -> bool:
L01138:     '''True = Popup anzeigen, False = unterdruecken (Default: True).'''
L01139:     cfg = _r1851_load_ini()
L01140:     if cfg is None:
L01141:         return True
L01142:     section = "RunnerPopups"
L01143:     if not cfg.has_section(section):
L01144:         return True
L01145:     try:
L01146:         return cfg.getboolean(section, runner_id, fallback=True)
L01147:     except Exception:
L01148:         return True
L01149: 
L01150: def _r1851_set_runnerpopup_flag(runner_id: str, show: bool) -> None:
L01151:     cfg = _r1851_load_ini()
L01152:     if cfg is None:
L01153:         return
L01154:     section = "RunnerPopups"
L01155:     if not cfg.has_section(section):
L01156:         cfg.add_section(section)
L01157:     cfg.set(section, runner_id, "true" if show else "false")
L01158:     _r1851_save_ini(cfg)
L01159: 
L01160: def _r1851_show_popup(app, title: str, text: str, runner_id: str):
L01161:     '''Popup fuer Runner-Ausgaben mit Checkbox "nicht mehr anzeigen".'''
L01162:     if _r1851_tk is None:
L01163:         return
L01164: 
L01165:     content = text or "(keine Ausgabe)"
L01166: 
L01167:     def _build():
L01168:         try:
L01169:             win = _r1851_tk.Toplevel(app)
L01170:         except Exception:
L01171:             win = _r1851_tk.Toplevel()
L01172:         win.title(str(title))
L01173:         win.geometry("900x600")
L01174:         # R2213: center+topmost runner popup (existing popup, no new UI)
L01175:         try:
L01176:             win.update_idletasks()
L01177:             sw = win.winfo_screenwidth()
L01178:             sh = win.winfo_screenheight()
L01179:             w = win.winfo_width() or 900
L01180:             h = win.winfo_height() or 600
L01181:             x = max(0, int((sw - w) / 2))
L01182:             y = max(0, int((sh - h) / 4))  # leicht nach oben (TOP)
L01183:             win.geometry(f"{w}x{h}+{x}+{y}")
L01184:         except Exception:
L01185:             pass
L01186:         try:
L01187:             win.attributes("-topmost", True)
L01188:             win.lift()
L01189:             win.focus_force()
L01190:         except Exception:
L01191:             pass
L01192:         try:
L01193:             win.grab_set()
L01194:         except Exception:
L01195:             pass
L01196: 
L01197:         frame = _r1851_tk.Frame(win)
L01198:         frame.pack(expand=True, fill="both")
L01199: 
L01200:         scrollbar = _r1851_tk.Scrollbar(frame)
L01201:         scrollbar.pack(side="right", fill="y")
L01202: 
L01203:         txt = _r1851_tk.Text(frame, wrap="word")
L01204:         txt.pack(side="left", expand=True, fill="both")
L01205:         txt.config(yscrollcommand=scrollbar.set)
L01206:         scrollbar.config(command=txt.yview)
L01207: 
L01208:         if _r1851_font is not None:
L01209:             try:
L01210:                 mono = _r1851_font.Font(family="Courier New", size=10)
L01211:                 txt.configure(font=mono)
L01212:             except Exception:
L01213:                 pass
L01214: 
L01215:         txt.insert("1.0", content)
L01216:         txt.config(state="normal")
L01217: 
L01218:         ctrl = _r1851_tk.Frame(win)
L01219:         ctrl.pack(fill="x", pady=4)
L01220: 
L01221:         var_suppress = _r1851_tk.BooleanVar(
L01222:             value=not _r1851_get_runnerpopup_flag(runner_id)
L01223:         )
L01224:         chk = _r1851_tk.Checkbutton(
L01225:             ctrl,
L01226:             text="nicht mehr anzeigen",
L01227:             variable=var_suppress
L01228:         )
L01229:         chk.pack(side="left", padx=4)
```

### `modules/ui_left_panel.py`
- Range: L174–L318

```text
L00174:     var_path_preview = _ensure_stringvar(app, "var_path_preview")
L00175: 
L00176:     # --- Zeile: Dateiname + Endung ----------------------------------------
L00177:     row_name = tk.Frame(wrap, bg=bg)
L00178:     row_name.pack(fill="x", padx=4, pady=(4, 2))
L00179: 
L00180:     tk.Label(row_name, text="Datei:", bg=bg).pack(side="left", padx=2, pady=2)
L00181: 
L00182:     entry_name = ui_theme_classic.Entry(row_name, textvariable=var_name, width=32)
L00183:     entry_name.pack(side="left", padx=(4, 2))
L00184: 
L00185:     tk.Label(row_name, text=".", bg=bg).pack(side="left", padx=2, pady=2)
L00186: 
L00187:     entry_ext = ui_theme_classic.Entry(row_name, textvariable=var_ext, width=8)
L00188:     entry_ext.pack(side="left", padx=(2, 4))
L00189: 
L00190:     # Referenzen am App-Objekt bereitstellen (Kompatibilitaet fuer logic_actions)
L00191:     app.entry_name = entry_name
L00192:     app.entry_ext = entry_ext
L00193: 
L00194:     # --- Zeile: Zielordner (+ Browse-Button) ------------------------------
L00195:     row_target = tk.Frame(wrap, bg=bg)
L00196:     row_target.pack(fill="x", padx=4, pady=(0, 2))
L00197: 
L00198:     tk.Label(row_target, text="Zielordner:", bg=bg).pack(side="left", padx=2, pady=2)
L00199: 
L00200:     entry_target = ui_theme_classic.Entry(row_target, textvariable=var_target_dir, width=40)
L00201:     entry_target.pack(side="left", padx=(4, 2), fill="x", expand=True)
L00202: 
L00203:     btn_browse = ui_theme_classic.Button(
L00204:         row_target,
L00205:         text="...",
L00206:         width=3,
L00207:         command=lambda: _browse_target(app, var_target_dir),
L00208:     )
L00209:     btn_browse.pack(side="left", padx=(2, 0))
L00210: 
L00211:     app.entry_target_dir = entry_target
L00212:     app.button_target_browse = btn_browse
L00213: 
L00214:     # --- Zeile: Pfad-Vorschau + LED ---------------------------------------
L00215:     row_info = tk.Frame(wrap, bg=bg)
L00216:     row_info.pack(fill="x", padx=4, pady=(0, 4))
L00217: 
L00218:     tk.Label(row_info, text="Pfad:", bg=bg).pack(side="left", padx=2, pady=2)
L00219: 
L00220:     lbl_path = tk.Label(row_info, textvariable=var_path_preview, bg=bg, anchor="w")
L00221:     lbl_path.pack(side="left", padx=(4, 8), fill="x", expand=True)
L00222: 
L00223:     # Intake-LED (Platzhalter: grau = unbekannt)
L00224:     led = tk.Canvas(row_info, width=14, height=14, highlightthickness=0, bg=bg)
L00225:     led.pack(side="right", padx=(4, 0))
L00226:     led_id = led.create_oval(2, 2, 12, 12, fill="#666666", outline="#444444")
L00227: 
L00228:     app.intake_led = led
L00229:     app.intake_led_id = led_id
L00230: 
L00231:     def _update_preview(*_args):
L00232:         """Aktualisiert die Pfadvorschau basierend auf Name, Ext und Zielordner."""
L00233:         name = (var_name.get() or "").strip()
L00234:         ext = (var_ext.get() or "").strip()
L00235:         target = (var_target_dir.get() or "").strip()
L00236: 
L00237:         if ext and not ext.startswith("."):
L00238:             ext_show = "." + ext
L00239:         else:
L00240:             ext_show = ext
L00241: 
L00242:         if not name:
L00243:             preview = ""
L00244:         else:
L00245:             filename = f"{name}{ext_show}"
L00246:             if target:
L00247:                 preview = f"{target}\\{filename}"
L00248:             else:
L00249:                 preview = filename
L00250: 
L00251:         var_path_preview.set(preview)
L00252: 
L00253:     # Traces fuer automatische Aktualisierung
L00254:     def _safe_led_eval():
L00255:         """Sichere LED-Aktualisierung fuer den Intake-Tab."""
L00256:         try:
L00257:             ui_leds.evaluate(app)
L00258:         except Exception:
L00259:             # LED-Updates duerfen die UI niemals crashen.
L00260:             pass
L00261: 
L00262:     def _on_target_changed(*_args):
L00263:         """Wird aufgerufen, wenn sich Name, Endung oder Zielordner aendert.
L00264:         Aktualisiert die Pfadvorschau, synchronisiert die Ziel-
L00265:         Variablen der App, laedt die rechte Liste neu und
L00266:         aktualisiert die Intake-LEDs.
L00267:         R1612: Wenn Endung py/cmd => Zielordner automatisch auf tools setzen.
L00268:         """
L00269:         # Zielordner bei py/cmd automatisch auf tools-Kontext setzen
L00270:         try:
L00271:             ext_val = (var_ext.get() or "").strip().lower()
L00272:             if ext_val in ("py", "cmd"):
L00273:                 import os
L00274:                 root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
L00275:                 tools_dir = os.path.join(root, "tools")
L00276:                 current = (var_target_dir.get() or "").strip()
L00277:                 if os.path.isdir(tools_dir) and current != tools_dir:
L00278:                     var_target_dir.set(tools_dir)
L00279:         except Exception:
L00280:             # darf die UI nicht crashen, falls etwas schief geht
L00281:             pass
L00282:         _update_preview()
L00283:         # Zielvariablen der App mit neuem Zielordner synchronisieren
L00284:         try:
L00285:             _sync_target_vars(app, var_target_dir.get())
L00286:         except Exception:
L00287:             pass
L00288:         # Rechten Bereich (Projektliste) neu laden - entspricht
L00289:         # dem "Aktualisieren"-Button im Intake.
L00290:         try:
L00291:             ui_filters.refresh(app)
L00292:         except Exception:
L00293:             # UI soll nicht crashen, wenn refresh Probleme macht.
L00294:             pass
L00295:         # LED-Zustand aktualisieren
L00296:         _safe_led_eval()
L00297: 
L00298:     var_name.trace_add("write", _on_target_changed)
L00299:     var_ext.trace_add("write", _on_target_changed)
L00300:     var_target_dir.trace_add("write", _on_target_changed)
L00301: 
L00302:     _update_preview()
L00303:     _safe_led_eval()
L00304:     # --- ScrolledText fuer Code -------------------------------------------
L00305:     app.txt_intake = ScrolledText(wrap, undo=True, font=("Consolas", 10))
L00306:     def _on_code_change(_event=None):
L00307:         _safe_led_eval()
L00308: 
L00309:     app.txt_intake.bind("<KeyRelease>", _on_code_change)
L00310: 
L00311:     app.txt_intake.pack(fill="both", expand=True, padx=4, pady=(0, 4))
L00312: 
L00313:     if not hasattr(app, "intake_text"):
L00314:         app.intake_text = app.txt_intake
L00315:     if not hasattr(app, "txt_code"):
L00316:         app.txt_code = app.txt_intake
L00317: 
L00318:     return wrap
```

### `modules/ui_filters.py`
- Range: L22–L38

```text
L00022: def refresh(app):
L00023:     """Aktualisiert die rechte Projektliste basierend auf dem Zielordner.
L00024: 
L00025:     Wird u.a. von ui_left_panel._on_target_changed() genutzt.
L00026:     """
L00027:     try:
L00028:         # Neue Logik: direkt ui_project_tree verwenden
L00029:         from modules import ui_project_tree as _pt
L00030:         _pt._load_dir(app)
L00031:     except Exception:
L00032:         # Fallback: alter Mechanismus, falls right_list noch existiert
L00033:         try:
L00034:             app.right_list.refresh()
L00035:         except Exception:
L00036:             pass
L00037: 
L00038: def _save_target(path: str):
```

### `modules/ui_log_tab.py`
- Range: L128–L267

```text
L00128:     hsb = ttk.Scrollbar(area, orient="horizontal", command=text_widget.xview)
L00129: 
L00130:     text_widget.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
L00131: 
L00132:     area.grid_rowconfigure(0, weight=1)
L00133:     area.grid_columnconfigure(0, weight=1)
L00134: 
L00135:     text_widget.grid(row=0, column=0, sticky="nsew")
L00136:     vsb.grid(row=0, column=1, sticky="ns")
L00137:     hsb.grid(row=1, column=0, sticky="ew")
L00138: 
L00139:     # Button-Leiste unten, zentriert
L00140:     bottom = ui_theme_classic.Frame(outer, bg=BG)
L00141:     bottom.pack(fill="x", pady=(0, 6))
L00142: 
L00143:     btn_frame = ui_theme_classic.Frame(bottom, bg=BG)
L00144:     btn_frame.pack(anchor="center")
L00145: 
L00146:     btn_reload = ui_theme_classic.Button(
L00147:         btn_frame,
L00148:         text="Neu laden",
L00149:         command=lambda: (state.__setitem__('pos', 0), _load_log(text_widget)),
L00150:     )
L00151:     btn_reload.pack(side="left", padx=4, pady=2)
L00152: 
L00153:     btn_sel = ui_theme_classic.Button(
L00154:         btn_frame,
L00155:         text="Markiertes kopieren und zurück",
L00156:         command=lambda: _copy_selected_and_back(app, text_widget),
L00157:     )
L00158:     btn_sel.pack(side="left", padx=4, pady=2)
L00159: 
L00160:     btn_vis = ui_theme_classic.Button(
L00161:         btn_frame,
L00162:         text="Sichtbares kopieren und zurück",
L00163:         command=lambda: _copy_visible_and_back(app, text_widget),
L00164:     )
L00165:     btn_vis.pack(side="left", padx=4, pady=2)
L00166: 
L00167:     btn_all = ui_theme_classic.Button(
L00168:         btn_frame,
L00169:         text="Gesamtes Log kopieren und zurück",
L00170:         command=lambda: _copy_all_and_back(app, text_widget),
L00171:     )
L00172:     btn_all.pack(side="left", padx=4, pady=2)
L00173: 
L00174:     btn_back = ui_theme_classic.Button(
L00175:         btn_frame,
L00176:         text="Zurück zu Intake",
L00177:         command=lambda: _back_to_intake(app),
L00178:     )
L00179:     btn_back.pack(side="left", padx=4, pady=2)
L00180: 
L00181:     # Initialer Load
L00182:     _load_log(text_widget)
L00183: 
L00184:     # AUTO_TAIL_LOG_R2148
L00185:     state = {"pos": 0, "after_id": None}
L00186: 
L00187:     def _is_visible() -> bool:
L00188:         try:
L00189:             nb = getattr(app, "nb", None)
L00190:             if nb is None:
L00191:                 return True
L00192:             cur = nb.select()
L00193:             return cur == str(parent)
L00194:         except Exception:
L00195:             return True
L00196: 
L00197:     def _at_bottom() -> bool:
L00198:         try:
L00199:             first, last = text_widget.yview()
L00200:             return last >= 0.995
L00201:         except Exception:
L00202:             return True
L00203: 
L00204:     def _tail_once() -> None:
L00205:         if not _is_visible():
L00206:             return
L00207:         log_path = _get_log_path()
L00208:         if not log_path.exists():
L00209:             return
L00210:         try:
L00211:             size = log_path.stat().st_size
L00212:         except Exception:
L00213:             return
L00214:         if state["pos"] > size:
L00215:             state["pos"] = 0
L00216:         if state["pos"] == 0:
L00217:             try:
L00218:                 data = log_path.read_text(encoding="utf-8", errors="replace")
L00219:             except Exception:
L00220:                 return
L00221:             text_widget.configure(state="normal")
L00222:             text_widget.delete("1.0", "end")
L00223:             text_widget.insert("1.0", data)
L00224:             state["pos"] = size
L00225:             try:
L00226:                 text_widget.see("end")
L00227:             except Exception:
L00228:                 pass
L00229:             return
L00230:         if size == state["pos"]:
L00231:             return
L00232:         try:
L00233:             with log_path.open("rb") as f:
L00234:                 f.seek(state["pos"])
L00235:                 chunk = f.read()
L00236:         except Exception:
L00237:             return
L00238:         try:
L00239:             txt = chunk.decode("utf-8", errors="replace")
L00240:         except Exception:
L00241:             return
L00242:         if not txt:
L00243:             return
L00244:         was_bottom = _at_bottom()
L00245:         text_widget.configure(state="normal")
L00246:         text_widget.insert("end", txt)
L00247:         state["pos"] = size
L00248:         if was_bottom:
L00249:             try:
L00250:                 text_widget.see("end")
L00251:             except Exception:
L00252:                 pass
L00253: 
L00254:     def _tick() -> None:
L00255:         try:
L00256:             _tail_once()
L00257:         except Exception:
L00258:             pass
L00259:         try:
L00260:             state["after_id"] = parent.after(1000, _tick)
L00261:         except Exception:
L00262:             state["after_id"] = None
L00263: 
L00264:     try:
L00265:         _tick()
L00266:     except Exception:
L00267:         pass
```
