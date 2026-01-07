# R2447 Workspace UI Diagnose (READ-ONLY)

- Time: 2025-12-21 19:48:56

- Root: `C:\Users\rasta\OneDrive\ShrimpDev`

- File: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py`


## Ziel

Lokalisieren, **wo** das Workspace-Dropdown in `modules/ui_toolbar.py` gebaut wird und ob/wo es in der **Push-Zone** (oben rechts) landet. Keine Änderungen.


## Heuristische Row/Frame-Struktur

### Row/Frame structure (heuristic)

(No obvious row_ws/row_push frame declarations found.)


## Treffer (geordnet nach Zeile)


### L703 — row_push

```text
   0695: 
   0696:     Zeile 1: [Run] [Löschen] [Rename] [Undo]
   0697:     Zeile 2: [FutureFix] [FutureFix Safe] [Build Tools] [Diagnose]
   0698:     """
   0699:     outer = ui_theme_classic.Frame(parent)
   0700:     # R2429: Right-top stack for Push/Purge (flush top-right, stacked)
   0701:     header_right = ui_theme_classic.Frame(outer)
   0702:     header_right.pack(fill="x", pady=(0, 0), anchor="ne")
>> 0703:     row_push = ui_theme_classic.Frame(header_right)
   0704:     row_push.pack(fill="x", pady=(0, 2))
   0705: 
   0706:     # Toggle (gekoppelt)
   0707:     try:
   0708:         if not hasattr(app, "_autopush_link_var"):
   0709:             app._autopush_link_var = tk.BooleanVar(value=False)
   0710:         _link_var = app._autopush_link_var
   0711:     except Exception:
```


### L704 — row_push

```text
   0696:     Zeile 1: [Run] [Löschen] [Rename] [Undo]
   0697:     Zeile 2: [FutureFix] [FutureFix Safe] [Build Tools] [Diagnose]
   0698:     """
   0699:     outer = ui_theme_classic.Frame(parent)
   0700:     # R2429: Right-top stack for Push/Purge (flush top-right, stacked)
   0701:     header_right = ui_theme_classic.Frame(outer)
   0702:     header_right.pack(fill="x", pady=(0, 0), anchor="ne")
   0703:     row_push = ui_theme_classic.Frame(header_right)
>> 0704:     row_push.pack(fill="x", pady=(0, 2))
   0705: 
   0706:     # Toggle (gekoppelt)
   0707:     try:
   0708:         if not hasattr(app, "_autopush_link_var"):
   0709:             app._autopush_link_var = tk.BooleanVar(value=False)
   0710:         _link_var = app._autopush_link_var
   0711:     except Exception:
   0712:         _link_var = None
```


### L788 — row_push

```text
   0780:                         return True
   0781:             return False
   0782:         except Exception:
   0783:             # safe default: assume dirty -> blocks public
   0784:             return True
   0785: 
   0786:     # Buttons (right aligned): Private | Link | Public (Public far right)
   0787:     btn_push_public = ui_theme_classic.Button(
>> 0788:         row_push,
   0789:         text="Push Public",
   0790:         command=lambda: _call_logic_action(app, "action_autopush_both") if _autopush_linked() else _call_logic_action(app, "action_autopush_public"),
   0791:     )
   0792:     btn_push_public.pack(side="right", padx=(6, 0))
   0793: 
   0794:     try:
   0795:         chk = tk.Checkbutton(
   0796:             row_push,
```


### L789 — Push Public

```text
   0781:             return False
   0782:         except Exception:
   0783:             # safe default: assume dirty -> blocks public
   0784:             return True
   0785: 
   0786:     # Buttons (right aligned): Private | Link | Public (Public far right)
   0787:     btn_push_public = ui_theme_classic.Button(
   0788:         row_push,
>> 0789:         text="Push Public",
   0790:         command=lambda: _call_logic_action(app, "action_autopush_both") if _autopush_linked() else _call_logic_action(app, "action_autopush_public"),
   0791:     )
   0792:     btn_push_public.pack(side="right", padx=(6, 0))
   0793: 
   0794:     try:
   0795:         chk = tk.Checkbutton(
   0796:             row_push,
   0797:             text="<--> Link",
```


### L796 — row_push

```text
   0788:         row_push,
   0789:         text="Push Public",
   0790:         command=lambda: _call_logic_action(app, "action_autopush_both") if _autopush_linked() else _call_logic_action(app, "action_autopush_public"),
   0791:     )
   0792:     btn_push_public.pack(side="right", padx=(6, 0))
   0793: 
   0794:     try:
   0795:         chk = tk.Checkbutton(
>> 0796:             row_push,
   0797:             text="<--> Link",
   0798:             variable=_link_var,
   0799:         )
   0800:         chk.pack(side="right", padx=(6, 0))
   0801:     except Exception:
   0802:         pass
   0803: 
   0804:     btn_push_private = ui_theme_classic.Button(
```


### L805 — row_push

```text
   0797:             text="<--> Link",
   0798:             variable=_link_var,
   0799:         )
   0800:         chk.pack(side="right", padx=(6, 0))
   0801:     except Exception:
   0802:         pass
   0803: 
   0804:     btn_push_private = ui_theme_classic.Button(
>> 0805:         row_push,
   0806:         text="Push Private",
   0807:         command=lambda: _call_logic_action(app, "action_autopush_both") if _autopush_linked() else _call_logic_action(app, "action_autopush_private"),
   0808:     )
   0809:     btn_push_private.pack(side="right", padx=(6, 0))
   0810: 
   0811:     def _set_btn_state(btn, enabled: bool):
   0812:         try:
   0813:             btn.configure(state=("normal" if enabled else "disabled"))
```


### L806 — Push Private

```text
   0798:             variable=_link_var,
   0799:         )
   0800:         chk.pack(side="right", padx=(6, 0))
   0801:     except Exception:
   0802:         pass
   0803: 
   0804:     btn_push_private = ui_theme_classic.Button(
   0805:         row_push,
>> 0806:         text="Push Private",
   0807:         command=lambda: _call_logic_action(app, "action_autopush_both") if _autopush_linked() else _call_logic_action(app, "action_autopush_private"),
   0808:     )
   0809:     btn_push_private.pack(side="right", padx=(6, 0))
   0810: 
   0811:     def _set_btn_state(btn, enabled: bool):
   0812:         try:
   0813:             btn.configure(state=("normal" if enabled else "disabled"))
   0814:         except Exception:
```


### L820 — _update_push_states

```text
   0812:         try:
   0813:             btn.configure(state=("normal" if enabled else "disabled"))
   0814:         except Exception:
   0815:             try:
   0816:                 btn["state"] = ("normal" if enabled else "disabled")
   0817:             except Exception:
   0818:                 pass
   0819: 
>> 0820:     def _update_push_states():
   0821:         busy = _runner_busy()
   0822: 
   0823:         has_r2412 = _file_exists("tools/R2691.cmd")
   0824:         has_r2411 = _file_exists("tools/R2692.cmd")
   0825:         has_r2414 = _file_exists("tools/R2414.cmd")
   0826: 
   0827:         private_ok = has_r2412 and (not busy)
   0828: 
```


### L843 — _update_push_states

```text
   0835:             both_ok = has_r2414 and has_r2412 and has_r2411 and _public_repo_ok() and safe_clean and (not busy)
   0836:             _set_btn_state(btn_push_private, both_ok)
   0837:             _set_btn_state(btn_push_public, both_ok)
   0838:         else:
   0839:             _set_btn_state(btn_push_private, private_ok)
   0840:             _set_btn_state(btn_push_public, public_ok)
   0841: 
   0842:         try:
>> 0843:             row_push.after(1200, _update_push_states)
   0844:         except Exception:
   0845:             pass
   0846: 
   0847:     _update_push_states()
   0848: 
   0849: 
   0850:     # Zeile 0 - Tools Purge (ROOT-only, keine Subfolder)
   0851:     row0 = ui_theme_classic.Frame(header_right)
```


#### row_push

```text
   0835:             both_ok = has_r2414 and has_r2412 and has_r2411 and _public_repo_ok() and safe_clean and (not busy)
   0836:             _set_btn_state(btn_push_private, both_ok)
   0837:             _set_btn_state(btn_push_public, both_ok)
   0838:         else:
   0839:             _set_btn_state(btn_push_private, private_ok)
   0840:             _set_btn_state(btn_push_public, public_ok)
   0841: 
   0842:         try:
>> 0843:             row_push.after(1200, _update_push_states)
   0844:         except Exception:
   0845:             pass
   0846: 
   0847:     _update_push_states()
   0848: 
   0849: 
   0850:     # Zeile 0 - Tools Purge (ROOT-only, keine Subfolder)
   0851:     row0 = ui_theme_classic.Frame(header_right)
```


### L847 — _update_push_states

```text
   0839:             _set_btn_state(btn_push_private, private_ok)
   0840:             _set_btn_state(btn_push_public, public_ok)
   0841: 
   0842:         try:
   0843:             row_push.after(1200, _update_push_states)
   0844:         except Exception:
   0845:             pass
   0846: 
>> 0847:     _update_push_states()
   0848: 
   0849: 
   0850:     # Zeile 0 - Tools Purge (ROOT-only, keine Subfolder)
   0851:     row0 = ui_theme_classic.Frame(header_right)
   0852:     row0.pack(fill="x", pady=(0, 2))
   0853:     # rechts oben ausrichten
   0854:     btn_apply = ui_theme_classic.Button(
   0855:         row0,
```


### L850 — Tools Purge

```text
   0842:         try:
   0843:             row_push.after(1200, _update_push_states)
   0844:         except Exception:
   0845:             pass
   0846: 
   0847:     _update_push_states()
   0848: 
   0849: 
>> 0850:     # Zeile 0 - Tools Purge (ROOT-only, keine Subfolder)
   0851:     row0 = ui_theme_classic.Frame(header_right)
   0852:     row0.pack(fill="x", pady=(0, 2))
   0853:     # rechts oben ausrichten
   0854:     btn_apply = ui_theme_classic.Button(
   0855:         row0,
   0856:         text="Tools Purge Apply",
   0857:         command=lambda: _call_logic_action(app, "action_tools_purge_apply"),
   0858:     )
```


### L856 — Tools Purge

```text
   0848: 
   0849: 
   0850:     # Zeile 0 - Tools Purge (ROOT-only, keine Subfolder)
   0851:     row0 = ui_theme_classic.Frame(header_right)
   0852:     row0.pack(fill="x", pady=(0, 2))
   0853:     # rechts oben ausrichten
   0854:     btn_apply = ui_theme_classic.Button(
   0855:         row0,
>> 0856:         text="Tools Purge Apply",
   0857:         command=lambda: _call_logic_action(app, "action_tools_purge_apply"),
   0858:     )
   0859:     try:
   0860:         btn_apply.configure(bg="#f2b6b6", activebackground="#eaa0a0")
   0861:     except Exception:
   0862:         pass
   0863:     btn_apply.pack(side="right", padx=6, pady=0)
   0864:     try:
```


### L871 — Tools Purge

```text
   0863:     btn_apply.pack(side="right", padx=6, pady=0)
   0864:     try:
   0865:         ui_tooltips.add(btn_apply, "Archiviert Dateien im tools\\-ROOT nach tools\\Archiv (nur laut Plan). Mit Sicherheitsabfrage.")
   0866:     except Exception:
   0867:         pass
   0868: 
   0869:     btn_scan = ui_theme_classic.Button(
   0870:         row0,
>> 0871:         text="Tools Purge Scan",
   0872:         command=lambda: _call_logic_action(app, "action_tools_purge_scan"),
   0873:     )
   0874:     btn_scan.pack(side="right", padx=6, pady=0)
   0875:     try:
   0876:         ui_tooltips.add(btn_scan, "Erstellt Purge-Plan fuer Dateien im tools\\-ROOT (keine Subfolder).")
   0877:     except Exception:
   0878:         pass
   0879: 
```


## Nächster Schritt (Fix-Plan)

- Wenn `row_ws` **vor** `row_push` gebaut und in derselben Parent-Frame/Zone gepackt wird: Workspace-Dropdown muss aus dieser Zone entfernt und in den Treeview-Kontext (Project Tree) verlagert werden.
- Fix soll **strukturell** erfolgen (Frame/Row Entfernen), nicht via Regex-Pattern.
