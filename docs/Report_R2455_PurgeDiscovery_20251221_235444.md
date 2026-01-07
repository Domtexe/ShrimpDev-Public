# R2455 – Purge Discovery (READ-ONLY)

- Time: 20251221_235444
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- Source: `modules/logic_actions.py`

## Summary
- purge keyword hits: **9**
- runner call hits: **9** (parsed labels)
- purge runner calls: **2**

## Purge runner calls (parsed)
- L2902: **Tools Purge Scan** → **R2218**
- L2916: **Tools Purge Apply** → **R2224**

## Context: first purge keyword hits

```text
   L02891: 
   L02892: # R2066_TREE_RENAME_UNDO_END
   L02893: # ============================================================
   L02894: 
   L02895: 
   L02896: # ------------------------------------------------------------------
>> L02897: # Tools Purge Actions (ROOT-only; no subfolders)
   L02898: # Added by R2212 (EOF-only)
   L02899: # ------------------------------------------------------------------
   L02900: def action_tools_purge_scan(app, *args, **kwargs):  # type: ignore
   L02901:     # Erstellt Plan: docs\Tools_Purge_Flat_Plan.md (nur tools\ Root-Dateien)
   L02902:     _r1851_run_tools_runner(app, "R2218", "Tools Purge Scan")
   L02903: 
```

```text
   L02894: 
   L02895: 
   L02896: # ------------------------------------------------------------------
   L02897: # Tools Purge Actions (ROOT-only; no subfolders)
   L02898: # Added by R2212 (EOF-only)
   L02899: # ------------------------------------------------------------------
>> L02900: def action_tools_purge_scan(app, *args, **kwargs):  # type: ignore
   L02901:     # Erstellt Plan: docs\Tools_Purge_Flat_Plan.md (nur tools\ Root-Dateien)
   L02902:     _r1851_run_tools_runner(app, "R2218", "Tools Purge Scan")
   L02903: 
   L02904: def action_tools_purge_apply(app, *args, **kwargs):  # type: ignore
   L02905:     # Verschiebt NUR Dateien direkt in tools\ nach tools\Archiv (laut Plan). Subfolder werden NICHT angefasst.
   L02906:     if _r1851_mb is not None:
```

```text
   L02895: 
   L02896: # ------------------------------------------------------------------
   L02897: # Tools Purge Actions (ROOT-only; no subfolders)
   L02898: # Added by R2212 (EOF-only)
   L02899: # ------------------------------------------------------------------
   L02900: def action_tools_purge_scan(app, *args, **kwargs):  # type: ignore
>> L02901:     # Erstellt Plan: docs\Tools_Purge_Flat_Plan.md (nur tools\ Root-Dateien)
   L02902:     _r1851_run_tools_runner(app, "R2218", "Tools Purge Scan")
   L02903: 
   L02904: def action_tools_purge_apply(app, *args, **kwargs):  # type: ignore
   L02905:     # Verschiebt NUR Dateien direkt in tools\ nach tools\Archiv (laut Plan). Subfolder werden NICHT angefasst.
   L02906:     if _r1851_mb is not None:
   L02907:         ok = _r1851_mb.askyesno(
```

```text
   L02896: # ------------------------------------------------------------------
   L02897: # Tools Purge Actions (ROOT-only; no subfolders)
   L02898: # Added by R2212 (EOF-only)
   L02899: # ------------------------------------------------------------------
   L02900: def action_tools_purge_scan(app, *args, **kwargs):  # type: ignore
   L02901:     # Erstellt Plan: docs\Tools_Purge_Flat_Plan.md (nur tools\ Root-Dateien)
>> L02902:     _r1851_run_tools_runner(app, "R2218", "Tools Purge Scan")
   L02903: 
   L02904: def action_tools_purge_apply(app, *args, **kwargs):  # type: ignore
   L02905:     # Verschiebt NUR Dateien direkt in tools\ nach tools\Archiv (laut Plan). Subfolder werden NICHT angefasst.
   L02906:     if _r1851_mb is not None:
   L02907:         ok = _r1851_mb.askyesno(
   L02908:             "Tools Purge Apply",
```

```text
   L02898: # Added by R2212 (EOF-only)
   L02899: # ------------------------------------------------------------------
   L02900: def action_tools_purge_scan(app, *args, **kwargs):  # type: ignore
   L02901:     # Erstellt Plan: docs\Tools_Purge_Flat_Plan.md (nur tools\ Root-Dateien)
   L02902:     _r1851_run_tools_runner(app, "R2218", "Tools Purge Scan")
   L02903: 
>> L02904: def action_tools_purge_apply(app, *args, **kwargs):  # type: ignore
   L02905:     # Verschiebt NUR Dateien direkt in tools\ nach tools\Archiv (laut Plan). Subfolder werden NICHT angefasst.
   L02906:     if _r1851_mb is not None:
   L02907:         ok = _r1851_mb.askyesno(
   L02908:             "Tools Purge Apply",
   L02909:             "Wirklich Purge APPLY ausfuehren?\n\n"
   L02910:             "- betrifft nur tools\\ (ROOT-Dateien)\n"
```

```text
   L02902:     _r1851_run_tools_runner(app, "R2218", "Tools Purge Scan")
   L02903: 
   L02904: def action_tools_purge_apply(app, *args, **kwargs):  # type: ignore
   L02905:     # Verschiebt NUR Dateien direkt in tools\ nach tools\Archiv (laut Plan). Subfolder werden NICHT angefasst.
   L02906:     if _r1851_mb is not None:
   L02907:         ok = _r1851_mb.askyesno(
>> L02908:             "Tools Purge Apply",
   L02909:             "Wirklich Purge APPLY ausfuehren?\n\n"
   L02910:             "- betrifft nur tools\\ (ROOT-Dateien)\n"
   L02911:             "- Subfolder werden NICHT angefasst\n"
   L02912:             "- Basis: docs\\Tools_Purge_Flat_Plan.md\n",
   L02913:         )
   L02914:         if not ok:
```

```text
   L02903: 
   L02904: def action_tools_purge_apply(app, *args, **kwargs):  # type: ignore
   L02905:     # Verschiebt NUR Dateien direkt in tools\ nach tools\Archiv (laut Plan). Subfolder werden NICHT angefasst.
   L02906:     if _r1851_mb is not None:
   L02907:         ok = _r1851_mb.askyesno(
   L02908:             "Tools Purge Apply",
>> L02909:             "Wirklich Purge APPLY ausfuehren?\n\n"
   L02910:             "- betrifft nur tools\\ (ROOT-Dateien)\n"
   L02911:             "- Subfolder werden NICHT angefasst\n"
   L02912:             "- Basis: docs\\Tools_Purge_Flat_Plan.md\n",
   L02913:         )
   L02914:         if not ok:
   L02915:             return
```

```text
   L02906:     if _r1851_mb is not None:
   L02907:         ok = _r1851_mb.askyesno(
   L02908:             "Tools Purge Apply",
   L02909:             "Wirklich Purge APPLY ausfuehren?\n\n"
   L02910:             "- betrifft nur tools\\ (ROOT-Dateien)\n"
   L02911:             "- Subfolder werden NICHT angefasst\n"
>> L02912:             "- Basis: docs\\Tools_Purge_Flat_Plan.md\n",
   L02913:         )
   L02914:         if not ok:
   L02915:             return
   L02916:     _r1851_run_tools_runner(app, "R2224", "Tools Purge Apply")
   L02917: 
   L02918: def action_autopush_private(app, *args, **kwargs):  # type: ignore
```

## Context: purge runner calls

### Tools Purge Scan → R2218 (around L2902)
```text
   L02892: # R2066_TREE_RENAME_UNDO_END
   L02893: # ============================================================
   L02894: 
   L02895: 
   L02896: # ------------------------------------------------------------------
   L02897: # Tools Purge Actions (ROOT-only; no subfolders)
   L02898: # Added by R2212 (EOF-only)
   L02899: # ------------------------------------------------------------------
   L02900: def action_tools_purge_scan(app, *args, **kwargs):  # type: ignore
   L02901:     # Erstellt Plan: docs\Tools_Purge_Flat_Plan.md (nur tools\ Root-Dateien)
>> L02902:     _r1851_run_tools_runner(app, "R2218", "Tools Purge Scan")
   L02903: 
   L02904: def action_tools_purge_apply(app, *args, **kwargs):  # type: ignore
   L02905:     # Verschiebt NUR Dateien direkt in tools\ nach tools\Archiv (laut Plan). Subfolder werden NICHT angefasst.
   L02906:     if _r1851_mb is not None:
   L02907:         ok = _r1851_mb.askyesno(
   L02908:             "Tools Purge Apply",
   L02909:             "Wirklich Purge APPLY ausfuehren?\n\n"
   L02910:             "- betrifft nur tools\\ (ROOT-Dateien)\n"
   L02911:             "- Subfolder werden NICHT angefasst\n"
   L02912:             "- Basis: docs\\Tools_Purge_Flat_Plan.md\n",
```

### Tools Purge Apply → R2224 (around L2916)
```text
   L02906:     if _r1851_mb is not None:
   L02907:         ok = _r1851_mb.askyesno(
   L02908:             "Tools Purge Apply",
   L02909:             "Wirklich Purge APPLY ausfuehren?\n\n"
   L02910:             "- betrifft nur tools\\ (ROOT-Dateien)\n"
   L02911:             "- Subfolder werden NICHT angefasst\n"
   L02912:             "- Basis: docs\\Tools_Purge_Flat_Plan.md\n",
   L02913:         )
   L02914:         if not ok:
   L02915:             return
>> L02916:     _r1851_run_tools_runner(app, "R2224", "Tools Purge Apply")
   L02917: 
   L02918: def action_autopush_private(app, *args, **kwargs):  # type: ignore
   L02919:     # SAFE: docs-only push in private repo
   L02920:     _r1851_run_tools_runner(app, "R2691", "Autopush Private (SAFE)")
   L02921: 
   L02922: def action_autopush_public(app, *args, **kwargs):  # type: ignore
   L02923:     # Public export via allowlist
   L02924:     _r1851_run_tools_runner(app, "R2692", "Autopush Public (Allowlist)")
   L02925: 
   L02926: def action_autopush_both(app, *args, **kwargs):  # type: ignore
```
