# ConfigManager – Write Path Analyse

- Zeit: 2025-12-18 21:17:05
- Datei: modules/config_manager.py

## Gefundene potentielle Schreibstellen

### Funktion: `<module-level>`
- Zeile: 17
- Typ: configparser usage
```python
import configparser
```

### Funktion: `__init__`
- Zeile: 32
- Typ: configparser usage
```python
        self._config: Optional[configparser.ConfigParser] = None
```

### Funktion: `ensure_loaded`
- Zeile: 53
- Typ: configparser usage
```python
        cfg = configparser.ConfigParser()
```

### Funktion: `save`
- Zeile: 83
- Typ: save() call
```python
        - Dadurch überschreibt config_manager.save() nicht mehr Docking-Persistenz.
```

### Funktion: `save`
- Zeile: 88
- Typ: configparser usage
```python
        import configparser
```

### Funktion: `save`
- Zeile: 93
- Typ: configparser usage
```python
        base = configparser.ConfigParser()
```

### Funktion: `save`
- Zeile: 109
- Typ: open(...,'w')
```python
            with cfg_path.open("w", encoding="utf-8") as f:
```

### Funktion: `save`
- Zeile: 110
- Typ: write() call
```python
                self._config.write(f)
```

### Funktion: `save`
- Zeile: 114
- Typ: open(...,'w')
```python
        with cfg_path.open("w", encoding="utf-8") as f:
```

### Funktion: `save`
- Zeile: 115
- Typ: write() call
```python
            base.write(f)
```

### Funktion: `set_value`
- Zeile: 155
- Typ: save() call
```python
            self.save()
```

