# Report R2381 – config_manager.py Struktur-Scan (READ-ONLY)

- Timestamp: 2025-12-19 10:02:50

- Target: `C:\Users\rasta\OneDrive\ShrimpDev\modules\config_manager.py`

- Size: 6125 bytes

- SHA256: `af7516f4eb244a9aa4d623179d232d7354203fbd44a30da07b90409dbbd0e12b`

- AST parse: OK


## Klassen & Methoden

### ShrimpDevConfigManager (line 26)

- `__init__` (line 31), args=['self']

- `_get_default_project_root` (line 35), args=['self']

- `ensure_loaded` (line 41), args=['self', 'project_root']

- `get_config_path` (line 71), args=['self']

- `save` (line 78), args=['self']

- `get_section` (line 97), args=['self', 'section']

- `get_value` (line 107), args=['self', 'key', 'default', 'section']

- `set_value` (line 120), args=['self', 'key', 'value', 'section', 'auto_save']

- `get_workspace_root` (line 140), args=['self']

- `set_workspace_root` (line 153), args=['self', 'path', 'auto_save']

- `get_quiet_mode` (line 159), args=['self']

- `set_quiet_mode` (line 167), args=['self', 'value', 'auto_save']



## Verdächtige Entry-Points (save/persist/write/...)

- `ShrimpDevConfigManager.save()` (line 78), args=['self']


### Module-level

- `save()` (line 78), args=['self']


## Call-Sites (Write/IO/ini_writer)

### direct_open

_nichts gefunden._

### configparser_write

_nichts gefunden._

### pathlib_write

_nichts gefunden._

### ini_writer_usage

_nichts gefunden._

### other_suspicious

- line 57: `cfg.read` → `cfg.read(cfg_path, encoding='utf-8')`



## Grep-Hits (funktioniert auch ohne AST)

### INI path mentions

- line 5: `- Laden/Speichern von ShrimpDev.ini`

- line 22: `CONFIG_FILENAME = "ShrimpDev.ini"`

- line 28: `    Verwaltet die zentralen Config-Werte von ShrimpDev.ini.`

- line 73: `        Pfad zur ShrimpDev.ini.`

- line 85: `        from modules.ini_writer import get_writer`


### configparser usage

- line 17: `import configparser`

- line 32: `        self._config: Optional[configparser.ConfigParser] = None`

- line 53: `        cfg = configparser.ConfigParser()`


### file write patterns

_keine Treffer._

### ini_writer mentions

- line 85: `        from modules.ini_writer import get_writer`

