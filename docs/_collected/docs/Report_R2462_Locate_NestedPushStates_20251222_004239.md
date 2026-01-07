# R2462 – Locate nested _update_push_states (READ-ONLY)

- Time: 20251222_004239
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- Target: `modules/ui_toolbar.py`

## Range
- start: L833
- end:   L908
- indent(base): 4

## Hits
- purge_btns refs: 4
- purge keyword lines: 13
- reschedule lines: 1

## purge_btns lines
- L862
- L863
- L886
- L901

## Context (around first purge_btns OR function start)
```text
L00832: 
L00833:     def _update_push_states():
L00834:         busy = _runner_busy()
L00835: 
L00836:         has_r2412 = _file_exists("tools/R2691.cmd")
L00837:         has_r2411 = _file_exists("tools/R2692.cmd")
L00838:         has_r2414 = _file_exists("tools/R2414.cmd")
L00839: 
L00840:         private_ok = has_r2412 and (not busy)
L00841: 
L00842:         # Order enforcement: Public allowed only when SAFE scope is clean
L00843:         safe_clean = (not _private_safe_dirty())
L00844: 
L00845:         public_ok = has_r2411 and _public_repo_ok() and safe_clean and (not busy)
L00846: 
L00847:         if _autopush_linked():
L00848:             both_ok = has_r2414 and has_r2412 and has_r2411 and _public_repo_ok() and safe_clean and (not busy)
L00849:             _set_btn_state(btn_push_private, both_ok)
L00850:             _set_btn_state(btn_push_public, both_ok)
L00851:         else:
L00852:             _set_btn_state(btn_push_private, private_ok)
L00853:             _set_btn_state(btn_push_public, public_ok)
L00854: 
L00855:         try:
L00856: 
L00857:             # Purge buttons state (Scan/Apply)
L00858:             try:
L00859:                 plan_ok = _purge_plan_ok()
L00860:             except Exception:
L00861:                 plan_ok = False
L00862:             _set_btn_state(purge_btns.get("scan"), (not busy))
L00863:             _set_btn_state(purge_btns.get("apply"), plan_ok and (not busy))
L00864:             row_push.after(1200, _update_push_states)
L00865:         except Exception:
L00866:             pass
L00867: 
L00868:     _update_push_states()
L00869: 
L00870: 
L00871:     # Zeile 0 - Tools Purge (ROOT-only, keine Subfolder)
L00872:     row0 = ui_theme_classic.Frame(header_right)
L00873:     row0.pack(side="top", anchor="ne", pady=(0, 2))
L00874:     # rechts oben ausrichten
L00875:     btn_apply = ui_theme_classic.Button(
L00876:         row0,
L00877:         text="Tools Purge Apply",
L00878:         command=lambda: _call_logic_action(app, "action_tools_purge_apply"),
L00879:     )
L00880:     try:
L00881:         btn_apply.configure(bg="#f2b6b6", activebackground="#eaa0a0")
L00882:     except Exception:
L00883:         pass
L00884:     btn_apply.pack(side="right", padx=(6, 0), pady=0)
L00885:     try:
L00886:         purge_btns["apply"] = btn_apply
L00887:     except Exception:
L00888:         pass
L00889:     try:
L00890:         ui_tooltips.add(btn_apply, "Archiviert Dateien im tools\\-ROOT nach tools\\Archiv (nur laut Plan). Mit Sicherheitsabfrage.")
L00891:     except Exception:
L00892:         pass
```

## Note
- Dieser Report ist Grundlage für den minimalen Patch-Runner (R2463).
