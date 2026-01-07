# R2450 DIAG: UI Toolbar states + alignment (READ-ONLY)

- Time: 2025-12-21 21:53:19
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- File: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py`

## Runtime prerequisites (exists?)

- `tools/R2691.cmd`: **True**
- `tools/R2692.cmd`: **True**
- `tools/R2414.cmd`: **True**
- `docs/Tools_Purge_Flat_Plan.md`: **True**
- `registry/public_export_root.txt`: **False**
- `registry/public_allowlist.txt`: **True**
- `tools_keep.txt (root)`: **True**
- `registry/tools_keep.txt`: **True**
- `registry/runner_whitelist.txt`: **True**

## Code hits (line numbers, 1-based)

- `row_push_decl`: `[703]`
- `row_push_pack`: `[704]`
- `btn_push_private`: `[817, 822, 849, 852]`
- `btn_push_public`: `[800, 805, 850, 853]`
- `update_push_states_def`: `[833]`
- `row0_decl`: `[872]`
- `row0_pack`: `[873]`
- `btn_scan`: `[894, 899, 901, 905]`
- `btn_apply`: `[875, 881, 884, 886, 890]`

## Purge enable/disable logic markers (present?)

- `configure_state`: **False**
- `setitem_state`: **False**
- `set_btn_state_usage`: **False**
- `purge_plan_helper`: **True**

## Key blocks (near first hit)

### row_push_pack

```text
0696:     Zeile 1: [Run] [Löschen] [Rename] [Undo]
0697:     Zeile 2: [FutureFix] [FutureFix Safe] [Build Tools] [Diagnose]
0698:     """
0699:     outer = ui_theme_classic.Frame(parent)
0700:     # R2429: Right-top stack for Push/Purge (flush top-right, stacked)
0701:     header_right = ui_theme_classic.Frame(outer)
0702:     header_right.pack(side="top", anchor="ne", pady=(0, 0))
0703:     row_push = ui_theme_classic.Frame(header_right)
0704:     row_push.pack(side="top", anchor="ne", pady=(0, 2))
0705: 
0706:     # Toggle (gekoppelt)
0707:     try:
0708:         if not hasattr(app, "_autopush_link_var"):
0709:             app._autopush_link_var = tk.BooleanVar(value=False)
0710:         _link_var = app._autopush_link_var
0711:     except Exception:
0712:         _link_var = None
```

### btn_push_public

```text
0792:                     if path == pre or path.startswith(pre.rstrip("/") + "/"):
0793:                         return True
0794:             return False
0795:         except Exception:
0796:             # safe default: assume dirty -> blocks public
0797:             return True
0798: 
0799:     # Buttons (right aligned): Private | Link | Public (Public far right)
0800:     btn_push_public = ui_theme_classic.Button(
0801:         row_push,
0802:         text="Push Public",
0803:         command=lambda: _call_logic_action(app, "action_autopush_both") if _autopush_linked() else _call_logic_action(app, "action_autopush_public"),
0804:     )
0805:     btn_push_public.pack(side="right", padx=(6, 0))
0806: 
0807:     try:
0808:         chk = tk.Checkbutton(
```

### btn_push_private

```text
0809:             row_push,
0810:             text="<--> Link",
0811:             variable=_link_var,
0812:         )
0813:         chk.pack(side="right", padx=(6, 0))
0814:     except Exception:
0815:         pass
0816: 
0817:     btn_push_private = ui_theme_classic.Button(
0818:         row_push,
0819:         text="Push Private",
0820:         command=lambda: _call_logic_action(app, "action_autopush_both") if _autopush_linked() else _call_logic_action(app, "action_autopush_private"),
0821:     )
0822:     btn_push_private.pack(side="right", padx=(6, 0))
0823: 
0824:     def _set_btn_state(btn, enabled: bool):
0825:         try:
```

### update_push_states_def

```text
0825:         try:
0826:             btn.configure(state=("normal" if enabled else "disabled"))
0827:         except Exception:
0828:             try:
0829:                 btn["state"] = ("normal" if enabled else "disabled")
0830:             except Exception:
0831:                 pass
0832: 
0833:     def _update_push_states():
0834:         busy = _runner_busy()
0835: 
0836:         has_r2412 = _file_exists("tools/R2691.cmd")
0837:         has_r2411 = _file_exists("tools/R2692.cmd")
0838:         has_r2414 = _file_exists("tools/R2414.cmd")
0839: 
0840:         private_ok = has_r2412 and (not busy)
0841: 
```

### row0_pack

```text
0865:         except Exception:
0866:             pass
0867: 
0868:     _update_push_states()
0869: 
0870: 
0871:     # Zeile 0 - Tools Purge (ROOT-only, keine Subfolder)
0872:     row0 = ui_theme_classic.Frame(header_right)
0873:     row0.pack(side="top", anchor="ne", pady=(0, 2))
0874:     # rechts oben ausrichten
0875:     btn_apply = ui_theme_classic.Button(
0876:         row0,
0877:         text="Tools Purge Apply",
0878:         command=lambda: _call_logic_action(app, "action_tools_purge_apply"),
0879:     )
0880:     try:
0881:         btn_apply.configure(bg="#f2b6b6", activebackground="#eaa0a0")
```

### btn_scan

```text
0886:         purge_btns["apply"] = btn_apply
0887:     except Exception:
0888:         pass
0889:     try:
0890:         ui_tooltips.add(btn_apply, "Archiviert Dateien im tools\\-ROOT nach tools\\Archiv (nur laut Plan). Mit Sicherheitsabfrage.")
0891:     except Exception:
0892:         pass
0893: 
0894:     btn_scan = ui_theme_classic.Button(
0895:         row0,
0896:         text="Tools Purge Scan",
0897:         command=lambda: _call_logic_action(app, "action_tools_purge_scan"),
0898:     )
0899:     btn_scan.pack(side="right", padx=(6, 0), pady=0)
0900:     try:
0901:         purge_btns["scan"] = btn_scan
0902:     except Exception:
```

### btn_apply

```text
0867: 
0868:     _update_push_states()
0869: 
0870: 
0871:     # Zeile 0 - Tools Purge (ROOT-only, keine Subfolder)
0872:     row0 = ui_theme_classic.Frame(header_right)
0873:     row0.pack(side="top", anchor="ne", pady=(0, 2))
0874:     # rechts oben ausrichten
0875:     btn_apply = ui_theme_classic.Button(
0876:         row0,
0877:         text="Tools Purge Apply",
0878:         command=lambda: _call_logic_action(app, "action_tools_purge_apply"),
0879:     )
0880:     try:
0881:         btn_apply.configure(bg="#f2b6b6", activebackground="#eaa0a0")
0882:     except Exception:
0883:         pass
```

## Findings (interpretation)

- Push buttons: state gating is expected in `_update_push_states()` (busy + runner presence + repo conditions).
- Purge buttons: if **no** `configure(state=...)` / `_set_btn_state(btn_scan/apply)` exists, they are effectively always clickable.
- Alignment: right-edge mismatch is usually caused by inconsistent `padx` (e.g. rightmost button needs `padx=(6,0)`), or parent frame not right-anchored.

## Proposed next Runner (FIX, minimal-invasive)

- Add `_update_purge_states()` similar to push gating:
  - Disable both if runner busy.
  - Enable Scan only if `tools/R2218.cmd` exists.
  - Enable Apply only if `docs/Tools_Purge_Flat_Plan.md` exists AND `tools/R2224.cmd` exists.
- Normalize `padx` so rightmost buttons use `(6,0)`.

> NOTE: This runner made **no changes**. It only reports.
