import configparser
import os

INI_PATH = os.path.join(os.path.dirname(__file__), '..', 'ShrimpDev.ini')

def load():
    cfg = configparser.ConfigParser()
    if os.path.exists(INI_PATH):
        cfg.read(INI_PATH, encoding='utf-8')
    return cfg

def save(cfg):
    with open(INI_PATH, 'w', encoding='utf-8') as f:
        cfg.write(f)

# === R1651_TREE_LEARNINGJOURNAL_HELPERS_START ===
# Dieser Block wurde automatisch von R1651 erzeugt.
# Generische Helper-Funktionen für INI-Persistenz von Tree & LearningJournal.

from typing import Mapping  # type: ignore[override]

def load_tree_state(config, section: str = "Tree") -> dict:
    """Lädt Tree-Status aus der INI.

    Erwartete Keys (optional):
    - sort_column: Name der aktuell sortierten Spalte
    - sort_direction: 'asc' oder 'desc'
    - column_widths: kommaseparierte Liste von Breiten (ints)
    - search_term: aktueller Suchstring
    """
    if config is None:
        return {}
    if not config.has_section(section):
        return {}
    sec = config[section]
    data = {
        "sort_column": sec.get("sort_column", ""),
        "sort_direction": sec.get("sort_direction", ""),
        "search_term": sec.get("search_term", ""),
        "column_widths": [],
    }
    widths = sec.get("column_widths", "").strip()
    if widths:
        try:
            data["column_widths"] = [int(x) for x in widths.split(",") if x.strip()]
        except ValueError:
            data["column_widths"] = []
    return data


def save_tree_state(config, state: Mapping[str, object], section: str = "Tree") -> None:
    """Speichert Tree-Status in die INI."""
    if config is None or state is None:
        return
    if not config.has_section(section):
        config.add_section(section)

    sort_column = str(state.get("sort_column", "") or "")
    sort_direction = str(state.get("sort_direction", "") or "")
    widths = state.get("column_widths", [])
    if isinstance(widths, (list, tuple)):
        width_str = ",".join(str(int(w)) for w in widths)
    else:
        width_str = ""
    search_term = str(state.get("search_term", "") or "")

    config.set(section, "sort_column", sort_column)
    config.set(section, "sort_direction", sort_direction)
    config.set(section, "column_widths", width_str)
    config.set(section, "search_term", search_term)


def load_learningjournal_state(config, section: str = "LearningJournal") -> dict:
    """Lädt LearningJournal-Status aus der INI."""
    if config is None:
        return {}
    if not config.has_section(section):
        return {}
    sec = config[section]
    data = {
        "last_file": sec.get("last_file", ""),
        "last_cursor_line": 0,
        "last_cursor_column": 0,
        "last_scroll_y": 0.0,
    }
    try:
        data["last_cursor_line"] = int(sec.get("last_cursor_line", "0"))
    except ValueError:
        data["last_cursor_line"] = 0
    try:
        data["last_cursor_column"] = int(sec.get("last_cursor_column", "0"))
    except ValueError:
        data["last_cursor_column"] = 0
    try:
        data["last_scroll_y"] = float(sec.get("last_scroll_y", "0.0"))
    except ValueError:
        data["last_scroll_y"] = 0.0
    return data


def save_learningjournal_state(config, state: Mapping[str, object], section: str = "LearningJournal") -> None:
    """Speichert LearningJournal-Status in der INI."""
    if config is None or state is None:
        return
    if not config.has_section(section):
        config.add_section(section)

    def _to_int_str(value, default: int = 0) -> str:
        try:
            return str(int(value))
        except Exception:
            return str(default)

    def _to_float_str(value, default: float = 0.0) -> str:
        try:
            return str(float(value))
        except Exception:
            return str(default)

    last_file = str(state.get("last_file", "") or "")
    last_cursor_line = _to_int_str(state.get("last_cursor_line", 0), 0)
    last_cursor_column = _to_int_str(state.get("last_cursor_column", 0), 0)
    last_scroll_y = _to_float_str(state.get("last_scroll_y", 0.0), 0.0)

    config.set(section, "last_file", last_file)
    config.set(section, "last_cursor_line", last_cursor_line)
    config.set(section, "last_cursor_column", last_cursor_column)
    config.set(section, "last_scroll_y", last_scroll_y)

# === R1651_TREE_LEARNINGJOURNAL_HELPERS_END ===
