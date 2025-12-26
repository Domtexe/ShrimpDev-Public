"""Compat shim for legacy config_loader/config_mgr (R2346)

Some modules still import:
- from modules import config_loader
- from modules import config_mgr

and expect:
- cfg = config_loader.load()
- config_loader.save(cfg)

Canonical is still modules/config_manager.py, but to avoid breaking older code
we provide this minimal, conservative API.

Storage: project-root ShrimpDev.ini (same folder as main_gui.py).
"""

from __future__ import annotations

import configparser
from pathlib import Path


INI_NAME = "ShrimpDev.ini"


class ShrimpDevConfig(configparser.ConfigParser):
    """ConfigParser with legacy get(section, {}) behavior."""

    def __init__(self) -> None:
        super().__init__()

    def get(self, section, option=None, **kwargs):  # type: ignore[override]
        # Legacy-Mode: cfg.get('UI', {}) -> dict with options
        if option is None or isinstance(option, (dict, list, tuple)):
            default = option if isinstance(option, dict) else {}
            if not self.has_section(section):
                return dict(default)
            out = dict(default)
            try:
                for k, v in self.items(section):
                    out[k] = v
            except Exception:
                pass
            return out
        # Normal ConfigParser.get
        return super().get(section, option, **kwargs)


def _get_ini_path() -> Path:
    # modules/.. = project root
    pr = Path(__file__).resolve().parent.parent
    return pr / INI_NAME


def load() -> ShrimpDevConfig:
    path = _get_ini_path()
    cfg = ShrimpDevConfig()
    if not path.exists():
        return cfg
    try:
        cfg.read(path, encoding="utf-8")
    except Exception:
        try:
            cfg.read(path)
        except Exception:
            pass
    return cfg


def save(cfg) -> None:
    # R2402: SingleWriter delegation – DO NOT write INI directly here
    try:
        from modules import config_manager as _cfgm  # type: ignore

        mgr = _cfgm.get_manager()
        # Bestehende cfg Instanz übernehmen (Kompatibilität zu bisherigen Call-Sites)
        try:
            mgr._config = cfg  # type: ignore[attr-defined]
        except Exception:
            pass
        mgr.save()
    except Exception as _e:
        # Fallback: niemals GUI crashen (log best-effort)
        try:
            from modules.logic_actions import log_debug as _log_debug  # type: ignore

            _log_debug("[R2402] save delegation failed: " + repr(_e))
        except Exception:
            pass


# R2350_MERGE_SAVE
