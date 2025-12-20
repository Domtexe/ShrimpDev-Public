"""
modules/config_manager.py – Zentrale Konfiguration für ShrimpDev

Verantwortung:
- Laden/Speichern von ShrimpDev.ini
- Einheitlicher Zugriff auf:
  - workspace_root
  - quiet_mode

Konvention:
- INI-Datei liegt im Projekt-Root (akt. Arbeitsverzeichnis von ShrimpDev).
- Section: [settings]
"""

from __future__ import annotations

import configparser
from pathlib import Path
from typing import Optional


CONFIG_FILENAME = "ShrimpDev.ini"
SETTINGS_SECTION = "settings"


class ShrimpDevConfigManager:
    """
    Verwaltet die zentralen Config-Werte von ShrimpDev.ini.
    """

    def __init__(self) -> None:
        self._config: Optional[configparser.ConfigParser] = None
        self._project_root: Optional[Path] = None

    def _get_default_project_root(self) -> Path:
        """
        Ermittelt den Standard-Projekt-Root (aktuelles Arbeitsverzeichnis).
        """
        return Path.cwd()

    def ensure_loaded(self, project_root: Optional[Path] = None) -> None:
        """
        Stellt sicher, dass die Konfiguration geladen ist.
        """
        if self._config is not None:
            # bereits geladen
            return

        if project_root is None:
            project_root = self._get_default_project_root()
        self._project_root = project_root

        cfg = configparser.ConfigParser()
        cfg_path = self.get_config_path()

        if cfg_path.exists():
            cfg.read(cfg_path, encoding="utf-8")

        if SETTINGS_SECTION not in cfg:
            cfg[SETTINGS_SECTION] = {}

        # Default-Werte setzen, falls nicht vorhanden
        settings = cfg[SETTINGS_SECTION]
        if "workspace_root" not in settings:
            settings["workspace_root"] = str(project_root)
        if "quiet_mode" not in settings:
            settings["quiet_mode"] = "false"

        self._config = cfg

    def get_config_path(self) -> Path:
        """
        Pfad zur ShrimpDev.ini.
        """
        root = self._project_root or self._get_default_project_root()
        return root / CONFIG_FILENAME

    def save(self) -> None:
        # SingleWriter delegation: write ONLY via modules/ini_writer.py
        self.ensure_loaded(project_root=self._project_root if hasattr(self, "_project_root") else None)
        cfg_path = self.get_config_path()
        cfg = getattr(self, "_config", None)

        # Nothing loaded -> nothing to save
        if cfg is None:
            return

        # Convert ConfigParser to nested dict, but never overwrite [Docking] here
        updates = {}
        for section in cfg.sections():
            if section.strip().lower() == "docking":
                continue
            updates[section] = dict(cfg.items(section))

        # Write through single writer (supports both get_writer() and direct merge_write_ini)
        try:
            from modules.ini_writer import get_writer
            w = get_writer()
            if hasattr(w, "merge_write_ini"):
                w.merge_write_ini(str(cfg_path), updates)
                return
        except Exception:
            pass

        from modules.ini_writer import merge_write_ini
        merge_write_ini(str(cfg_path), updates)
        return
    def get_section(self, section: str = SETTINGS_SECTION):
        """
        Liefert eine mutable Section-View.
        """
        self.ensure_loaded()
        assert self._config is not None
        if section not in self._config:
            self._config[section] = {}
        return self._config[section]

    def get_value(
        self,
        key: str,
        default: Optional[str] = None,
        section: str = SETTINGS_SECTION,
    ) -> Optional[str]:
        """
        Liest einen String-Wert aus der Konfiguration.
        """
        self.ensure_loaded()
        section_obj = self.get_section(section)
        return section_obj.get(key, default)

    def set_value(
        self,
        key: str,
        value: str,
        section: str = SETTINGS_SECTION,
        auto_save: bool = True,
    ) -> None:
        """
        Schreibt einen String-Wert in die Konfiguration.
        """
        self.ensure_loaded()
        section_obj = self.get_section(section)
        section_obj[key] = value
        if auto_save:
            self.save()

    # ------------------------------------------------------------------
    # Spezialisierte Convenience-Methoden
    # ------------------------------------------------------------------

    def get_workspace_root(self) -> Path:
        """
        Liefert den aktuellen workspace_root als Path.
        """
        self.ensure_loaded()
        raw = self.get_value("workspace_root", None)
        if not raw:
            # Fallback: Projekt-Root
            root = self._project_root or self._get_default_project_root()
            raw = str(root)
            self.set_value("workspace_root", raw, auto_save=True)
        return Path(raw)

    def set_workspace_root(self, path: Path, auto_save: bool = True) -> None:
        """
        Setzt den workspace_root.
        """
        self.set_value("workspace_root", str(path), auto_save=auto_save)

    def get_quiet_mode(self) -> bool:
        """
        Liefert den quiet_mode als bool.
        """
        self.ensure_loaded()
        raw = self.get_value("quiet_mode", "false") or "false"
        return raw.strip().lower() in ("1", "true", "yes", "on")

    def set_quiet_mode(self, value: bool, auto_save: bool = True) -> None:
        """
        Setzt den quiet_mode.
        """
        self.set_value("quiet_mode", "true" if value else "false", auto_save=auto_save)


# Modulweiter Singleton-Manager
_manager = ShrimpDevConfigManager()


def get_manager() -> ShrimpDevConfigManager:
    """
    Liefert den globalen Config-Manager (Singleton).
    """
    return _manager


# Convenience-Funktionen
def get_workspace_root() -> Path:
    """
    Shortcut auf ShrimpDevConfigManager.get_workspace_root().
    """
    return _manager.get_workspace_root()


def set_workspace_root(path: Path, auto_save: bool = True) -> None:
    """
    Shortcut auf ShrimpDevConfigManager.set_workspace_root().
    """
    _manager.set_workspace_root(path, auto_save=auto_save)


def get_quiet_mode() -> bool:
    """
    Shortcut auf ShrimpDevConfigManager.get_quiet_mode().
    """
    return _manager.get_quiet_mode()


def set_quiet_mode(value: bool, auto_save: bool = True) -> None:
    """
    Shortcut auf ShrimpDevConfigManager.set_quiet_mode().
    """
    _manager.set_quiet_mode(value, auto_save=auto_save)
