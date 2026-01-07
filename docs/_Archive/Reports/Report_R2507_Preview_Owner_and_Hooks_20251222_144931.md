# R2507 – Preview Owner & Hooks (READ-ONLY)

- Time: 20251222_144931
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`

## ui_runner_products_tab.py
```text
L00148:         # Also provide plaintext paths for apps that paste text (e.g. chat/editor).
L00150:         CF_UNICODETEXT = 13
L00152:             text_payload = "\r\n".join([str(p) for p in file_paths]) + "\r\n"
L00153:             text_data = text_payload.encode("utf-16le") + b"\x00\x00"
L00154:             htxt = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(text_data))
L00159:                         ctypes.memmove(ptxt, text_data, len(text_data))
L00163:                     user32.SetClipboardData(CF_UNICODETEXT, htxt)
L00225: # --- R2304 INTERNAL VIEWER -----------------------------------------------------------
L00227: _R2304_TEXT_EXT = {".txt", ".md", ".py", ".json", ".log", ".ini", ".cfg", ".yaml", ".yml", ".csv", ".bat", ".cmd", ".ps1"}
L00229: def _r2304_is_text_file(p: Path) -> bool:
L00231:         return p.suffix.lower() in _R2304_TEXT_EXT
L00235: def _r2304_open_internal_viewer(app, title: str, path: Path) -> None:
L00236:     """Read-only Text-Viewer wie Runner-Popup, für Runner-Produkte."""
L00315:     lbl = tk.Label(top, text=str(path), anchor="w", justify="left")
L00318:     # Center: Text + Scroll
L00322:     txt = tk.Text(mid, wrap="none")
L00335:         data = path.read_text(encoding="utf-8", errors="replace")
L00365:     btn_ext = tk.Button(row, text="Extern öffnen", command=_open_external)
L00366:     btn_folder = tk.Button(row, text="Ordner", command=_open_folder)
L00367:     btn_close = tk.Button(row, text="Schließen", command=_close)
L00373: # --- /R2304 INTERNAL VIEWER ----------------------------------------------------------
L00463:     tk.Label(top, text="Artefakte (Read-Only)", bg=bg).pack(side="left")
L00465:     btn_refresh = tk.Button(top, text="Refresh")
L00471:     # Left: list, Right: preview
L00481:     tk.Label(f, text="Runner:", bg=bg).pack(side="left")
L00483:     ent_runner = tk.Entry(f, textvariable=var_runner, width=10)
L00486:     tk.Label(f, text="Typ:", bg=bg).pack(side="left")
L00488:     cmb_type = ttk.Combobox(f, textvariable=var_type, values=["All", "Report", "Doc", "Backup", "File"], width=10, state="readonly")
L00491:     tk.Label(f, text="Suche:", bg=bg).pack(side="left")
L00493:     ent_q = tk.Entry(f, textvariable=var_q)
L00499:     tree.heading("mtime", text="Zeit")
L00500:     tree.heading("type", text="Typ")
L00501:     tree.heading("runner", text="Runner")
L00502:     tree.heading("name", text="Datei")
L00503:     tree.heading("size", text="Bytes")
L00515:     # Preview
L00516:     tk.Label(right, text="Preview", bg=bg).pack(anchor="w")
L00517:     txt = tk.Text(right, wrap="word")
L00523:     btn_open = tk.Button(act, text="Öffnen")
L00525:     btn_view = tk.Button(act, text="Intern anzeigen")
L00527:     btn_folder = tk.Button(act, text="Ordner")
L00529:     btn_copy = tk.Button(act, text="Pfad kopieren")
L00578:     def _selected_path() -> str:
L00587:     def _load_preview(path: str) -> None:
L00600:                 txt.insert("end", "(Datei zu groß für Preview > 2MB)\n" + path)
L00615:         _load_preview(_selected_path())
L00617:     def _on_viewer():
L00618:         p = _selected_path()
L00623:             if _r2304_is_text_file(pp):
L00624:                 _r2304_open_internal_viewer(app, f"Runner-Produkt: {pp.name}", pp)
L00631:         p = _selected_path()
L00636:             if _r2304_is_text_file(pp):
L00637:                 _r2304_open_internal_viewer(app, f"Runner-Produkt: {pp.name}", pp)
L00644:         _safe_open_folder(_selected_path())
L00647:         p = _selected_path()
L00663:         btn_view.configure(command=_on_viewer)
L00675:     # --- R2303 TREE UX: Click / Context / Copy --------------------------------------
L00679:         p = _selected_path()
L00697:             data = pp.read_text(encoding="utf-8", errors="replace")
L00722:             p2 = _selected_path()
L00740:     def _tree_context_menu(ev):
L00748:         p = _selected_path()
L00753:             m = tk.Menu(tree, tearoff=0)
L00754:             m.add_command(label="Intern anzeigen", command=_on_viewer)
L00760:             m.add_command(label="Inhalt kopieren (Text)", command=_on_copy_content)
L00767:         tree.bind("<Button-3>", _tree_context_menu)
L00792: # --- R2300 UX: Click / Copy / Context -------------------------------------------
L00826:         text = path.read_text(encoding="utf-8", errors="replace")
L00828:         root.clipboard_append(text)
L00838:     def on_menu(ev):
L00841:         m = tk.Menu(listbox, tearoff=0)
L00858:     listbox.bind("<Button-3>", on_menu)
```

## ui_project_tree.py
```text
L00066:     tk.Label(row_count, textvariable=count_var, bg=bg).pack(side="left", padx=(0, 4))
L00116:     tk.Label(row_workspace, text="Workspace:", bg=bg).pack(side="left")
L00119:         textvariable=workspace_var,
L00148:     tk.Label(row_search, text="Suche:", bg=bg).pack(side="left")
L00150:     ent = ui_theme_classic.Entry(row_search, textvariable=search_var, width=24)
L00257:     btn_root = ui_theme_classic.Button(row_actions, text="Ordner", command=_btn_open_root, width=8)
L00258:     btn_tools = ui_theme_classic.Button(row_actions, text="Tools", command=_btn_open_tools, width=8)
L00259:     btn_reports = ui_theme_classic.Button(row_actions, text="Reports", command=_btn_open_reports, width=8)
L00260:     btn_snaps = ui_theme_classic.Button(row_actions, text="Snapshots", command=_btn_open_snapshots, width=10)
L00261:     btn_explorer = ui_theme_classic.Button(row_actions, text="Explorer", command=_btn_open_explorer, width=10)
L00288:         tree.heading(cid, text=headings[cid])
L00301:         tree.bind("<Double-1>", lambda event, a=app: open_selected_in_intake(a))
L00402:             root, ext = os.path.splitext(name)
L00573: def get_selected_path(app) -> str | None:
L00589: def get_selected_paths(app) -> list[str]:
L00647: def open_selected_in_intake(app) -> None:
L00652:     path = get_selected_path(app)
L00656:     _, ext = os.path.splitext(path)
L00704:             label = str(btn.cget('text')).strip().lower()
L00721:                 label = str(btn.cget('text')).strip().lower()
L00808: def enable_context_menu(app) -> None:
L00810:     Aktiviert ein Kontextmenue auf der TreeView (rechte Liste):
L00829:     # Owner marker to avoid double context menus (logic_actions also binds Button-3 with add="+")
L00954:     def _r2477_copy_files_for_paste(selected_paths: list[str]) -> None:
L00955:         files = [p for p in selected_paths if p and os.path.isfile(p)]
L01034:     menu = tk.Menu(tree, tearoff=False)
L01066:     menu.add_command(label="Datei(en) kopieren (Paste)", command=lambda: _r2477_copy_files_for_paste(get_selected_paths(app)))
L01067:     menu.add_command(label="Backup wiederherstellen…", command=lambda: _r2477_restore_backup(get_selected_path(app) or ""))
L01069:     def _on_context(event):
L01097:         tree.bind("<Button-3>", _on_context, add="+")
```

## ui_left_panel.py
```text
L00004: from tkinter.scrolledtext import ScrolledText
L00136:     - ScrolledText fuer Code
L00174:     var_path_preview = _ensure_stringvar(app, "var_path_preview")
L00180:     tk.Label(row_name, text="Datei:", bg=bg).pack(side="left", padx=2, pady=2)
L00182:     entry_name = ui_theme_classic.Entry(row_name, textvariable=var_name, width=32)
L00185:     tk.Label(row_name, text=".", bg=bg).pack(side="left", padx=2, pady=2)
L00187:     entry_ext = ui_theme_classic.Entry(row_name, textvariable=var_ext, width=8)
L00198:     tk.Label(row_target, text="Zielordner:", bg=bg).pack(side="left", padx=2, pady=2)
L00200:     entry_target = ui_theme_classic.Entry(row_target, textvariable=var_target_dir, width=40)
L00205:         text="...",
L00218:     tk.Label(row_info, text="Pfad:", bg=bg).pack(side="left", padx=2, pady=2)
L00220:     lbl_path = tk.Label(row_info, textvariable=var_path_preview, bg=bg, anchor="w")
L00224:     led = tk.Canvas(row_info, width=14, height=14, highlightthickness=0, bg=bg)
L00231:     def _update_preview(*_args):
L00243:             preview = ""
L00247:                 preview = f"{target}\\{filename}"
L00249:                 preview = filename
L00251:         var_path_preview.set(preview)
L00269:         # Zielordner bei py/cmd automatisch auf tools-Kontext setzen
L00282:         _update_preview()
L00302:     _update_preview()
L00304:     # --- ScrolledText fuer Code -------------------------------------------
L00305:     app.txt_intake = ScrolledText(wrap, undo=True, font=("Consolas", 10))
L00313:     if not hasattr(app, "intake_text"):
L00314:         app.intake_text = app.txt_intake
```

## ui_toolbar.py
```text
L00008: SR_HELP_TEXT_R2134 = 'Service Runner (SR) – Kurzüberblick\n\nSR9997 – FutureFix:\n  Sammel-Button für zukünftige Fixes / Reparaturketten (schnell, experimenteller).\n\nSR1352 – FutureFix Safe:\n  Wie FutureFix, aber konservativer: weniger Risiko, mehr Checks.\n\nSR9998 – Build Tools:\n  Werkzeuge/Build-Helfer (Build/Patch/Tools vorbereiten).\n\nSR9999 – Diagnose:\n  Diagnose-Läufe/Checks (Fehleranalyse, Status, Problemstellen finden).\n\nSR1922 – Systemcheck:\n  System-/Projekt-Check (Struktur, Konsistenz, Basischecks).'
L00012:         messagebox.showinfo('SR Hilfe', SR_HELP_TEXT_R2134)
L00016: # R2133: SR Hilfe Text
L00017: SR_TEXT_R2133 = 'Service Runner (SR) – Kurzüberblick\n\nSR9997 – FutureFix:\n  Sammel-Button für zukünftige Fixes / Reparaturketten (schnell, experimenteller).\n\nSR1352 – FutureFix Safe:\n  Wie FutureFix, aber konservativer: weniger Risiko, mehr Checks.\n\nSR9998 – Build Tools:\n  Werkzeuge/Build-Helfer (z. B. Tools sammeln, patch/build vorbereiten).\n\nSR9999 – Diagnose:\n  Diagnose-Läufe/Checks (typisch: Fehleranalyse, Status, Problemstellen finden).\n\nSR1922 – Systemcheck:\n  System-/Projekt-Check (Grundgesundheit: Struktur, Dateien, Konsistenz, Basischecks).'
L00021:         messagebox.showinfo('Service Runner (SR) Hilfe', SR_TEXT_R2133)
L00070:                 status.configure(text=f"{name}: Importfehler ({exc})")
L00083:                     status.configure(text=f"{name}: Fehler ({exc})")
L00090:                 status.configure(text=f"{name}: Aktion nicht verfügbar.")
L00098:     text: str,
L00102:     btn = ui_theme_classic.Button(parent, text=text, command=command)
L00293:         tail_text = "\n".join(tail_lines)
L00294:         older_text = "\n".join(older_lines)
L00345:         info_label = tk.Label(top_frame, text="Letzter Runner-Block aus debug_output.txt")
L00350:         # Text + Scrollbar
L00351:         txt = tk.Text(win, wrap="none")
L00359:             txt.insert("1.0", tail_text)
L00376:             if not older_text:
L00383:                     txt.insert("1.0", older_text + "\n" + current)
L00385:                     txt.insert("1.0", older_text)
L00437:         btn_older = tk.Button(bottom_frame, text="Ältere laden", command=_load_older)
L00440:         btn_copy = tk.Button(bottom_frame, text="Inhalt kopieren", command=_copy_content)
L00443:         btn_copy_close = tk.Button(bottom_frame, text="Kopieren & schließen", command=_copy_and_close)
L00446:         btn_close = tk.Button(bottom_frame, text="Schließen", command=_close)
L00505:     # Liefert das Intake-Textwidget (intake_text / txt_intake), falls vorhanden.
L00506:     for cand in ("intake_text", "txt_intake"):
L00516:         text = app.clipboard_get()
L00518:         text = ""
L00519:     if not text:
L00523:                 status.configure(text="Zwischenablage leer.")
L00533:                 status.configure(text="Einfügen: Kein Intake-Widget gefunden.")
L00540:         w.insert("1.0", text)
L00545:                 status.configure(text="Einfügen fehlgeschlagen.")
L00553:             status.configure(text="Code eingefügt (Zwischenablage).")
L00564:                 status.configure(text="Erkennung nach Einfügen fehlgeschlagen.")
L00573:     - Holt den Pfad der markierten Datei aus der rechten Liste (ui_project_tree.get_selected_path).
L00583:             path = ui_project_tree.get_selected_path(app)
L00598:     _, ext = _os.path.splitext(path)
L00742:                 p = reg_file.read_text(encoding="utf-8", errors="replace").strip().strip('"')
L00781:                 text=True,
L00802:         text="Push Public",
L00810:             text="<--> Link",
L00819:         text="Push Private",
L00874:         text="Tools Purge Apply",
L00893:         text="Tools Purge Scan",
L00964:         text="Service (SR) / Diagnose",
L01022:                 status.configure(text=f"Rename: Importfehler ({exc})")
L01033:                 status.configure(text=f"Rename-Fehler: {exc}")
```

