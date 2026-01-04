# ini_writer.py
# Zentraler INI-Writer (Single Writer Policy)
# - merge-save (fremde sections bleiben)
# - atomic write (tmp + replace)
# - source logging

import os
import threading
import configparser
from datetime import datetime


class IniWriter:
    def __init__(self, ini_path=None, logger=None):
        self._lock = threading.Lock()
        self._logger = logger
        self._mem = self._new_cfg()
        if ini_path:
            self._ini_path = ini_path
        else:
            self._ini_path = self._default_ini_path()

    def _default_ini_path(self):
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        return os.path.join(base, "ShrimpDev.ini")

    def _new_cfg(self):
        cfg = configparser.ConfigParser(interpolation=None)
        cfg.optionxform = str
        return cfg

    def _log(self, msg):
        try:
            if self._logger:
                self._logger(msg)
                return
        except Exception:
            pass
        try:
            print("[INI] " + msg)
        except Exception:
            pass

    def get(self, section, key, fallback=None):
        with self._lock:
            if not self._mem.has_section(section):
                return fallback
            try:
                return self._mem.get(section, key, fallback=fallback)
            except Exception:
                return fallback

    def set(self, section, key, value, source=None):
        with self._lock:
            if not self._mem.has_section(section):
                self._mem.add_section(section)
            self._mem.set(section, str(key), str(value))
            self._log("set " + section + "." + str(key) + " source=" + str(source))
            return True

    def update_many(self, section, dict_values, source=None):
        if dict_values is None:
            return False
        with self._lock:
            if not self._mem.has_section(section):
                self._mem.add_section(section)
            for k in dict_values:
                self._mem.set(section, str(k), str(dict_values[k]))
            self._log(
                "update_many "
                + section
                + " keys="
                + str(len(dict_values))
                + " source="
                + str(source)
            )
            return True

    def snapshot(self):
        with self._lock:
            out = {}
            for sec in self._mem.sections():
                out[sec] = {}
                for k, v in self._mem.items(sec):
                    out[sec][k] = v
            return out

    def load_existing(self):
        path = self._ini_path
        cfg = self._new_cfg()
        if path and os.path.isfile(path):
            try:
                cfg.read(path, encoding="utf-8")
            except Exception:
                try:
                    cfg.read(path)
                except Exception:
                    pass
        return cfg

    def save_merge_atomic(self, source=None):
        with self._lock:
            base = self.load_existing()
            # merge mem into base
            for sec in self._mem.sections():
                if not base.has_section(sec):
                    base.add_section(sec)
                for k, v in self._mem.items(sec):
                    base.set(sec, str(k), str(v))

            path = self._ini_path
            if not path:
                return False
            d = os.path.dirname(path)
            if d:
                try:
                    os.makedirs(d, exist_ok=True)
                except Exception:
                    pass

            tmp = path + ".tmp"
            try:
                with open(tmp, "w", encoding="utf-8") as f:
                    base.write(f)
                os.replace(tmp, path)
                self._log("save_merge_atomic ok path=" + path + " source=" + str(source))
                return True
            except Exception as e:
                try:
                    if os.path.isfile(tmp):
                        os.remove(tmp)
                except Exception:
                    pass
                self._log("save_merge_atomic FAILED " + repr(e) + " source=" + str(source))
                return False


# Singleton helper (optional use)
_SINGLETON = None


def get_writer():
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = IniWriter()
    return _SINGLETON


# --- R2379: SingleWriter merge API ---
from pathlib import Path
import configparser
from datetime import datetime

# R3001_PUBLIC_EXPORT_GUARDS
# Defaults for public-export safety guards (used by tools and wrappers)
PUBLIC_EXPORT_MAX_FALLBACK_FILES = 200  # if allowlist missing/empty and fallback list is huge -> abort
PUBLIC_EXPORT_MAX_EXTRA_FILES = 5       # tolerated extra files vs keep-list (e.g., public_allowlist.txt)

PRESERVE_SECTIONS_DEFAULT = {"Docking"}


def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ini_path(project_root: Path) -> Path:
    return (project_root / "ShrimpDev.ini").resolve()


def read_ini(path: Path) -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    cfg.read(path, encoding="utf-8")
    return cfg


def merge_write_ini(
    project_root,
    updates,
    preserve_sections=None,
    add_timestamp=True,
):
    """
    DEPRECATED – Single Writer Policy enforced.

    This function is kept ONLY for backward compatibility.
    All calls are delegated to IniWriter.save_merge_atomic().
    """
    from modules.ini_writer import get_writer

    writer = get_writer()
    if updates:
        for sec, kv in updates.items():
            if kv:
                for k, v in kv.items():
                    writer.set(sec, k, v, source="legacy_merge_write_ini")

    writer.save_merge_atomic(source="legacy_merge_write_ini")
    return writer._ini_path
