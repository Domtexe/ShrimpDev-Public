# R2458 – Purge Gating Audit (READ-ONLY)

- Time: 20251222_003154
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- Target: `modules/ui_toolbar.py`

## Findings (quick)
- _update_purge_states() found: True
- _update_push_states() found: True
- purge_btns references: 4
- Plan file references (Tools_Purge_Flat_Plan.md): 3
- R2218 references: 1 | R2224 references: 1

## Evidence: _update_purge_states()
```text
   L00891:     except Exception:
   L00892:         pass
   L00893: 
   L00894:     btn_scan = ui_theme_classic.Button(
   L00895:         row0,
   L00896:         text="Tools Purge Scan",
   L00897:         command=lambda: _call_logic_action(app, "action_tools_purge_scan"),
   L00898:     )
   L00899:     btn_scan.pack(side="right", padx=(6, 0), pady=0)
   L00900:     try:
   L00901:         purge_btns["scan"] = btn_scan
   L00902:     except Exception:
   L00903:         pass
   L00904:     try:
   L00905:         ui_tooltips.add(btn_scan, "Erstellt Purge-Plan fuer Dateien im tools\\-ROOT (keine Subfolder).")
   L00906:     except Exception:
   L00907:         pass
   L00908:     # R2451: Purge buttons state gating (disable when not allowed)
>> L00909:     def _update_purge_states():
   L00910:         try:
   L00911:             busy = _runner_busy()
   L00912:         except Exception:
   L00913:             busy = False
   L00914: 
   L00915:         has_scan = _file_exists("tools/R2218.cmd")
   L00916:         has_apply = _file_exists("tools/R2224.cmd")
   L00917:         plan_ok = _file_exists("docs/Tools_Purge_Flat_Plan.md")
   L00918: 
   L00919:         scan_ok = bool(has_scan) and (not busy)
   L00920:         apply_ok = bool(has_apply) and bool(plan_ok) and (not busy)
   L00921: 
   L00922:         _set_btn_state(btn_scan, scan_ok)
   L00923:         _set_btn_state(btn_apply, apply_ok)
   L00924: 
   L00925:         try:
   L00926:             row0.after(1200, _update_purge_states)
   L00927:         except Exception:
```

## Evidence: purge_btns usage (possible undefined / redundant gating)
```text
   L00856: 
   L00857:             # Purge buttons state (Scan/Apply)
   L00858:             try:
   L00859:                 plan_ok = _purge_plan_ok()
   L00860:             except Exception:
   L00861:                 plan_ok = False
>> L00862:             _set_btn_state(purge_btns.get("scan"), (not busy))
   L00863:             _set_btn_state(purge_btns.get("apply"), plan_ok and (not busy))
   L00864:             row_push.after(1200, _update_push_states)
   L00865:         except Exception:
   L00866:             pass
   L00867: 
   L00868:     _update_push_states()
```

```text
   L00857:             # Purge buttons state (Scan/Apply)
   L00858:             try:
   L00859:                 plan_ok = _purge_plan_ok()
   L00860:             except Exception:
   L00861:                 plan_ok = False
   L00862:             _set_btn_state(purge_btns.get("scan"), (not busy))
>> L00863:             _set_btn_state(purge_btns.get("apply"), plan_ok and (not busy))
   L00864:             row_push.after(1200, _update_push_states)
   L00865:         except Exception:
   L00866:             pass
   L00867: 
   L00868:     _update_push_states()
   L00869: 
```

```text
   L00880:     try:
   L00881:         btn_apply.configure(bg="#f2b6b6", activebackground="#eaa0a0")
   L00882:     except Exception:
   L00883:         pass
   L00884:     btn_apply.pack(side="right", padx=(6, 0), pady=0)
   L00885:     try:
>> L00886:         purge_btns["apply"] = btn_apply
   L00887:     except Exception:
   L00888:         pass
   L00889:     try:
   L00890:         ui_tooltips.add(btn_apply, "Archiviert Dateien im tools\\-ROOT nach tools\\Archiv (nur laut Plan). Mit Sicherheitsabfrage.")
   L00891:     except Exception:
   L00892:         pass
```

```text
   L00895:         row0,
   L00896:         text="Tools Purge Scan",
   L00897:         command=lambda: _call_logic_action(app, "action_tools_purge_scan"),
   L00898:     )
   L00899:     btn_scan.pack(side="right", padx=(6, 0), pady=0)
   L00900:     try:
>> L00901:         purge_btns["scan"] = btn_scan
   L00902:     except Exception:
   L00903:         pass
   L00904:     try:
   L00905:         ui_tooltips.add(btn_scan, "Erstellt Purge-Plan fuer Dateien im tools\\-ROOT (keine Subfolder).")
   L00906:     except Exception:
   L00907:         pass
```

## Evidence: Plan file gating
```text
   L00760:     _SAFE_PREFIXES = ["docs/PIPELINE.md"]
   L00761: 
   L00762:     def _purge_plan_ok() -> bool:
   L00763:         """Tools-Purge Apply nur wenn ein aktueller Plan existiert."""
   L00764:         try:
   L00765:             # Plan wird durch action_tools_purge_scan erzeugt
>> L00766:             rp = Path(getattr(app, "project_root", "")) / "docs" / "Tools_Purge_Flat_Plan.md"
   L00767:             if not rp.exists():
   L00768:                 # fallback (wenn app.project_root nicht gesetzt)
   L00769:                 rp = Path(__file__).resolve().parent.parent / "docs" / "Tools_Purge_Flat_Plan.md"
   L00770:             return rp.exists() and rp.stat().st_size > 20
   L00771:         except Exception:
   L00772:             return False
```

```text
   L00763:         """Tools-Purge Apply nur wenn ein aktueller Plan existiert."""
   L00764:         try:
   L00765:             # Plan wird durch action_tools_purge_scan erzeugt
   L00766:             rp = Path(getattr(app, "project_root", "")) / "docs" / "Tools_Purge_Flat_Plan.md"
   L00767:             if not rp.exists():
   L00768:                 # fallback (wenn app.project_root nicht gesetzt)
>> L00769:                 rp = Path(__file__).resolve().parent.parent / "docs" / "Tools_Purge_Flat_Plan.md"
   L00770:             return rp.exists() and rp.stat().st_size > 20
   L00771:         except Exception:
   L00772:             return False
   L00773: 
   L00774: 
   L00775:     def _private_safe_dirty() -> bool:
```

```text
   L00911:             busy = _runner_busy()
   L00912:         except Exception:
   L00913:             busy = False
   L00914: 
   L00915:         has_scan = _file_exists("tools/R2218.cmd")
   L00916:         has_apply = _file_exists("tools/R2224.cmd")
>> L00917:         plan_ok = _file_exists("docs/Tools_Purge_Flat_Plan.md")
   L00918: 
   L00919:         scan_ok = bool(has_scan) and (not busy)
   L00920:         apply_ok = bool(has_apply) and bool(plan_ok) and (not busy)
   L00921: 
   L00922:         _set_btn_state(btn_scan, scan_ok)
   L00923:         _set_btn_state(btn_apply, apply_ok)
```

## Cross-check: logic_actions (presence)
- action_tools_purge_scan present: True
- action_tools_purge_apply present: True
- runner call lines: 10

## Recommendation (minimal patch target)
- Keep ONE gating loop for Purge buttons (prefer the dedicated _update_purge_states).
- If purge_btns is used anywhere, ensure it is defined or remove the dead update block.
- Align plan_ok check with the real plan semantics (existence + size threshold if desired).
