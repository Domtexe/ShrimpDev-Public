# Report R2403 – ui_toolbar INI writes -> ConfigManager (SingleWriter)

- Timestamp: 2025-12-19 23:56:07
- Target: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py`

- sha256 before: `bee3900aaf705cc373513bb5c5b359404d616d2e05bce493a157e248eab42cf8`

## Patch Notes
- OK: replaced 2 direct open(...)/cfg.write(...) blocks with ConfigManager save path

## Backup
- `C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\ui_toolbar.py.R2403_20251219_235607.bak`

## sha256 after
- `c60dc4a7bf8aa569a18badb0788ad74fa791592703ce3b67f8c2ea31a10d3352`

## Compile Gate
- OK: C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py
