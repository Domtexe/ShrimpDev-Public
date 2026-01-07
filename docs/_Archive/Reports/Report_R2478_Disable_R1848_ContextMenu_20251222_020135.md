# R2478 – Disable R1848 Tree Context Menu when UI owner is active

- Time: 20251222_020135
- Target: `modules/logic_actions.py`

## Change
- Added owner-guard in `_r1848_attach_context_menu(app)` (returns if app._tree_ctx_owner == 'ui_project_tree')

## Backup
- `C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\logic_actions.py.R2478_20251222_020135.bak`

## Compile
- py_compile: OK

