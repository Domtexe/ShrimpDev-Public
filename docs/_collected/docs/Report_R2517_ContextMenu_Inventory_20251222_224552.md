# R2517 – ContextMenu Inventory (READ-ONLY)

- Time: 20251222_224552
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`

## module_docking.py

### Button-3 bindings
```text
L00667: <Button-3> -> _on_right_click
```

### _on_right_click() block
- Range: L638-L674
- tk.Menu used: True

**Labels:**
- Undock
- Dock (Fenster schließen)

## ui_runner_products_tab.py

### Button-3 bindings
```text
L00876: <Button-3> -> _tree_context_menu
L00941: <Button-3> -> _preview_context_menu
L01035: <Button-3> -> on_menu
```

### _tree_context_menu() block
- Range: L845-L880
- tk.Menu used: True

**Labels:**
- Intern anzeigen
- Öffnen
- Ordner öffnen
- Backup wiederherstellen
- Pfad kopieren
- Datei kopieren (Explorer-Paste)
- Inhalt kopieren (Text)

### _preview_context_menu() block
- Range: L924-L949
- tk.Menu used: True

**Labels:**
- Inhalt kopieren (Text)
- Pfad kopieren
- Datei kopieren (Explorer-Paste)

### on_menu() block
- Range: L1015-L1024
- tk.Menu used: True

**Labels:**
- Öffnen
- Ordner öffnen
- Pfad kopieren
- Inhalt kopieren

