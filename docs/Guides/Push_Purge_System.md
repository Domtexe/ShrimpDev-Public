# Push- & Purge-System (ShrimpDev)

Stand: 2025-12-28 11:52:24

## Registry (Source of Truth)
- `registry/private_repo_root.txt`
- `registry/public_export_root.txt`
- `registry/runner_whitelist.txt`
- `registry/tools_keep.txt`

## Push-Buttons (UI)
Push-Buttons sind nur aktiv, wenn:
1) Repo-Root gültig ist (private/public), **und**
2) Wrapper-Datei existiert:
   - Private Push → `tools/R2691.cmd`
   - Public Push → `tools/R2692.cmd`

Ziel: keine aktivierten Buttons, die beim Klick in „Runner-Datei nicht gefunden“ laufen.

## Purge (Tools)
- Purge Scan: `R2218`
- Purge Apply: `R2224`
- Schutz muss stem-basiert wirken (`R####`), unabhängig von `.cmd` / `.py`.

## Fix-Historie (relevant)
- R2837: Wrapper-Gating für Push-Buttons
- R2839: Whitelist-Hardening (stem + cmd/py + tools\… Varianten)
  → verhindert, dass Wrapper/Runner trotz Whitelist archiviert werden.

## Checks / Troubleshooting
- Buttons aus:
  - existieren `tools/R2691.cmd` und `tools/R2692.cmd`?
  - sind `registry/*_repo_root.txt` korrekt?
- Runner verschwinden nach Purge:
  - Purge Scan Report prüfen: betroffene Runner müssen als **KEEP** erscheinen
