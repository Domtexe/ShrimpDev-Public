"""Konfigurationsmanager für ShrimpDev (config/intake.ini)."""

from __future__ import annotations
import os, threading, configparser
from typing import List

# Logger optional einbinden - Fallback = No-Op
try:
    from modules.snippets.logger_snippet import write_log as _log
except Exception:

    def _log(_p: str, _m: str) -> None:
        pass


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CFG_DIR = os.path.join(ROOT, "config")
INI_PATH = os.path.join(CFG_DIR, "intake.ini")
_LOCK = threading.RLock()

DEFAULTS = {
    "general": {
        "popup_errors": "false",
        "default_path": ".",
        "target_folder": ".",
        "suppress_save_ok": "false",
        "history_limit": "50",
        "always_on_top": "false",
    },
    "history": {"items": ""},
}


def _ensure_ini() -> None:
    os.makedirs(CFG_DIR, exist_ok=True)
    if not os.path.exists(INI_PATH):
        cfg = configparser.ConfigParser()
        for sec, kv in DEFAULTS.items():
            cfg[sec] = kv
        with open(INI_PATH, "w", encoding="utf-8") as f:
            cfg.write(f)
        _log("CFG", "INI neu erstellt")


class ConfigMgr:
    """Threadsichere INI-Verwaltung für ShrimpDev."""

    def __init__(self) -> None:
        _ensure_ini()
        self.cfg = configparser.ConfigParser()
        self.reload()

    # --- I/O ---
    def reload(self) -> None:
        with _LOCK:
            self.cfg.read(INI_PATH, encoding="utf-8")

    def save(self) -> None:
        with _LOCK:
            with open(INI_PATH, "w", encoding="utf-8") as f:
                self.cfg.write(f)
        _log("CFG", "INI gespeichert")

    # --- Getter/Setter ---
    def get_bool(self, section: str, key: str, default: bool = False) -> bool:
        try:
            return self.cfg.getboolean(section, key, fallback=default)
        except Exception:
            return default

    def get_str(self, section: str, key: str, default: str = "") -> str:
        try:
            return self.cfg.get(section, key, fallback=default)
        except Exception:
            return default

    def set_str(self, section: str, key: str, value: str) -> None:
        with _LOCK:
            if not self.cfg.has_section(section):
                self.cfg.add_section(section)
            self.cfg.set(section, key, value)
            self.save()

    # --- History ---
    def get_history(self) -> List[str]:
        raw = self.get_str("history", "items", "")
        if not raw.strip():
            return []
        return [x for x in raw.split("|") if x.strip()]

    def append_history(self, item: str) -> None:
        with _LOCK:
            hist = self.get_history()
            if item in hist:
                hist.remove(item)
            hist.insert(0, item)
            try:
                limit = int(self.get_str("general", "history_limit", "50") or "50")
            except Exception:
                limit = 50
            hist = hist[: max(1, limit)]
            if not self.cfg.has_section("history"):
                self.cfg.add_section("history")
            self.cfg.set("history", "items", "|".join(hist))
            self.save()

    def remove_history(self, item: str) -> None:
        with _LOCK:
            hist = self.get_history()
            if item in hist:
                hist.remove(item)
            if not self.cfg.has_section("history"):
                self.cfg.add_section("history")
            self.cfg.set("history", "items", "|".join(hist))
            self.save()

    def clear_history(self) -> None:
        with _LOCK:
            if not self.cfg.has_section("history"):
                self.cfg.add_section("history")
            self.cfg.set("history", "items", "")
            self.save()
