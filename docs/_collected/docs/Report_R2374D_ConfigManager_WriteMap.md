# R2374D – ConfigManager Write-Entry Diagnose

- Zeit: 2025-12-18 21:36:37
- Datei: modules/config_manager.py

## Gefundene Schreibpfade

### Treffer 1
- Typ: write() call
- Zeile: 110
- Klasse: ShrimpDevConfigManager
- Funktion: save

### Treffer 2
- Typ: write() call
- Zeile: 115
- Klasse: ShrimpDevConfigManager
- Funktion: save

## Hinweis

- READ-ONLY Analyse
- Treffer sind **reale** Write-Entry-Points (keine Heuristik)
- Naechster Schritt: gezielte Delegation **exakt dieser Stellen** an ini_writer
