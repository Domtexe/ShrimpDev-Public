# Report R2401 – INI Writer Deep Scan (READ-ONLY)

- Timestamp: 2025-12-19 23:43:16
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`

## `modules\config_loader.py`
- size: 2936 bytes
- sha256: `bc20ac95815cd9b1826982a5f3b2f0d6a49fb26ac2d36122781a7246229db758`
- save() blocks found: **1**
- suspicious hits: **7**

### save() block excerpts
- Lines 70-107:
  - L70: `def save(cfg) -> None:`
  - L71: `    """R2350_MERGE_SAVE`
  - L72: `    Merge-save: verhindert, dass unbekannte Sections (z.B. [Docking]) beim Speichern verloren gehen.`
  - L73: `    """`
  - L74: `    if cfg is None:`
  - L75: `        return`
  - L76: `    path = _get_ini_path()`
  - L77: `    # load existing file first`
  - L78: `    existing = load()`
  - L79: `    try:`
  - L80: `        for sec in cfg.sections():`
  - L81: `            if not existing.has_section(sec):`
  - L82: `                try:`
  - L83: `                    existing.add_section(sec)`
  - L84: `                except Exception:`
  - L85: `                    pass`
  - L86: `            try:`
  - L87: `                for k, v in cfg.items(sec):`
  - L88: `                    try:`
  - L89: `                        existing.set(sec, k, v)`
  - L90: `                    except Exception:`
  - L91: `                        pass`
  - L92: `            except Exception:`
  - L93: `                pass`
  - L94: `    except Exception:`
  - L95: `        pass`
  - L96: `    try:`
  - L97: `        with path.open('w', encoding='utf-8') as f:`
  - L98: `            existing.write(f)`
  - L99: `    except Exception:`
  - L100: `        try:`
  - L101: `            with path.open('w') as f:`
  - L102: `                existing.write(f)`
  - L103: `        except Exception:`
  - L104: `            pass`
  - L105: ``
  - L106: ``
  - L107: `# R2350_MERGE_SAVE`

### grep hits
- L14 [ini_path] `Storage: project-root ShrimpDev.ini (same folder as main_gui.py).`
- L23 [ini_path] `INI_NAME = "ShrimpDev.ini"`
- L72 [docking] `Merge-save: verhindert, dass unbekannte Sections (z.B. [Docking]) beim Speichern verloren gehen.`
- L97 [open('w')] `with path.open('w', encoding='utf-8') as f:`
- L98 [cfg.write/configparser] `existing.write(f)`
- L101 [open('w')] `with path.open('w') as f:`
- L102 [cfg.write/configparser] `existing.write(f)`

## `modules\config_mgr.py`
- size: 2936 bytes
- sha256: `bc20ac95815cd9b1826982a5f3b2f0d6a49fb26ac2d36122781a7246229db758`
- save() blocks found: **1**
- suspicious hits: **7**

### save() block excerpts
- Lines 70-107:
  - L70: `def save(cfg) -> None:`
  - L71: `    """R2350_MERGE_SAVE`
  - L72: `    Merge-save: verhindert, dass unbekannte Sections (z.B. [Docking]) beim Speichern verloren gehen.`
  - L73: `    """`
  - L74: `    if cfg is None:`
  - L75: `        return`
  - L76: `    path = _get_ini_path()`
  - L77: `    # load existing file first`
  - L78: `    existing = load()`
  - L79: `    try:`
  - L80: `        for sec in cfg.sections():`
  - L81: `            if not existing.has_section(sec):`
  - L82: `                try:`
  - L83: `                    existing.add_section(sec)`
  - L84: `                except Exception:`
  - L85: `                    pass`
  - L86: `            try:`
  - L87: `                for k, v in cfg.items(sec):`
  - L88: `                    try:`
  - L89: `                        existing.set(sec, k, v)`
  - L90: `                    except Exception:`
  - L91: `                        pass`
  - L92: `            except Exception:`
  - L93: `                pass`
  - L94: `    except Exception:`
  - L95: `        pass`
  - L96: `    try:`
  - L97: `        with path.open('w', encoding='utf-8') as f:`
  - L98: `            existing.write(f)`
  - L99: `    except Exception:`
  - L100: `        try:`
  - L101: `            with path.open('w') as f:`
  - L102: `                existing.write(f)`
  - L103: `        except Exception:`
  - L104: `            pass`
  - L105: ``
  - L106: ``
  - L107: `# R2350_MERGE_SAVE`

### grep hits
- L14 [ini_path] `Storage: project-root ShrimpDev.ini (same folder as main_gui.py).`
- L23 [ini_path] `INI_NAME = "ShrimpDev.ini"`
- L72 [docking] `Merge-save: verhindert, dass unbekannte Sections (z.B. [Docking]) beim Speichern verloren gehen.`
- L97 [open('w')] `with path.open('w', encoding='utf-8') as f:`
- L98 [cfg.write/configparser] `existing.write(f)`
- L101 [open('w')] `with path.open('w') as f:`
- L102 [cfg.write/configparser] `existing.write(f)`

## `modules\ui_toolbar.py`
- size: 29171 bytes
- sha256: `bee3900aaf705cc373513bb5c5b359404d616d2e05bce493a157e248eab42cf8`
- save() blocks found: **0**
- suspicious hits: **19**

### grep hits
- L248 [ini_path] `ini_path = os.path.join(root_dir, "ShrimpDev.ini")`
- L307 [logwindow] `if cfg.has_section("LogWindow") and cfg.has_option("LogWindow", "geometry"):`
- L308 [logwindow] `geom = cfg.get("LogWindow", "geometry")`
- L413 [logwindow] `if not cfg.has_section("LogWindow"):`
- L414 [logwindow] `cfg.add_section("LogWindow")`
- L415 [logwindow] `cfg.set("LogWindow", "geometry", geom_value)`
- L417 [open('w')] `with open(ini_path, "w", encoding="utf-8") as f:`
- L418 [cfg.write/configparser] `cfg.write(f)`
- L448 [ini_path] `"""Lädt Log-Popup-Geometrie aus ShrimpDev.ini."""`
- L451 [ini_path] `ini_path = os.path.join(root, "ShrimpDev.ini")`
- L455 [logwindow] `if "LogWindow" in cfg and "geometry" in cfg["LogWindow"]:`
- L456 [logwindow] `return cfg["LogWindow"]["geometry"]`
- L463 [ini_path] `"""Speichert Geometrie des Logfensters in ShrimpDev.ini."""`
- L466 [ini_path] `ini_path = os.path.join(root, "ShrimpDev.ini")`
- L478 [logwindow] `if "LogWindow" not in cfg:`
- L479 [logwindow] `cfg.add_section("LogWindow")`
- L480 [logwindow] `cfg["LogWindow"]["geometry"] = geom`
- L482 [open('w')] `with open(ini_path, "w", encoding="utf-8") as f:`
- L483 [cfg.write/configparser] `cfg.write(f)`

## `modules\config_manager.py`
- size: 6742 bytes
- sha256: `71f77e2b428f27dc645e46b00cddd430959268bef4a6709f6ae3969209b37052`
- save() blocks found: **1**
- suspicious hits: **11**

### save() block excerpts
- Lines 78-107:
  - L78: `    def save(self) -> None:`
  - L79: `        # SingleWriter delegation: write ONLY via modules/ini_writer.py`
  - L80: `        self.ensure_loaded(project_root=self._project_root if hasattr(self, "_project_root") else None)`
  - L81: `        cfg_path = self.get_config_path()`
  - L82: `        cfg = getattr(self, "_config", None)`
  - L83: ``
  - L84: `        # Nothing loaded -> nothing to save`
  - L85: `        if cfg is None:`
  - L86: `            return`
  - L87: ``
  - L88: `        # Convert ConfigParser to nested dict, but never overwrite [Docking] here`
  - L89: `        updates = {}`
  - L90: `        for section in cfg.sections():`
  - L91: `            if section.strip().lower() == "docking":`
  - L92: `                continue`
  - L93: `            updates[section] = dict(cfg.items(section))`
  - L94: ``
  - L95: `        # Write through single writer (supports both get_writer() and direct merge_write_ini)`
  - L96: `        try:`
  - L97: `            from modules.ini_writer import get_writer`
  - L98: `            w = get_writer()`
  - L99: `            if hasattr(w, "merge_write_ini"):`
  - L100: `                w.merge_write_ini(str(cfg_path), updates)`
  - L101: `                return`
  - L102: `        except Exception:`
  - L103: `            pass`
  - L104: ``
  - L105: `        from modules.ini_writer import merge_write_ini`
  - L106: `        merge_write_ini(str(cfg_path), updates)`
  - L107: `        return`

### grep hits
- L5 [ini_path] `- Laden/Speichern von ShrimpDev.ini`
- L22 [ini_path] `CONFIG_FILENAME = "ShrimpDev.ini"`
- L28 [ini_path] `Verwaltet die zentralen Config-Werte von ShrimpDev.ini.`
- L54 [ini_path] `cfg_path = self.get_config_path()`
- L71 [ini_path] `def get_config_path(self) -> Path:`
- L73 [ini_path] `Pfad zur ShrimpDev.ini.`
- L76 [ini_path] `return root / CONFIG_FILENAME`
- L81 [ini_path] `cfg_path = self.get_config_path()`
- L88 [docking] `# Convert ConfigParser to nested dict, but never overwrite [Docking] here`
- L100 [merge_write_ini] `w.merge_write_ini(str(cfg_path), updates)`
- L106 [merge_write_ini] `merge_write_ini(str(cfg_path), updates)`

## `modules\ini_writer.py`
- size: 6212 bytes
- sha256: `cb3e4bf442a6ef4db75e6fe52e73dd4df6852d6935efb873d08e9712a266d7ac`
- save() blocks found: **0**
- suspicious hits: **7**

### grep hits
- L24 [ini_path] `return os.path.join(base, 'ShrimpDev.ini')`
- L115 [open('w')] `with open(tmp, 'w', encoding='utf-8') as f:`
- L116 [cfg.write/configparser] `base.write(f)`
- L150 [ini_path] `return (project_root / "ShrimpDev.ini").resolve()`
- L157 [merge_write_ini] `def merge_write_ini(project_root: Path,`
- L189 [open('w')] `with path.open("w", encoding="utf-8") as f:`
- L190 [cfg.write/configparser] `base.write(f)`

