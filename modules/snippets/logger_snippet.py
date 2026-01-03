from __future__ import annotations

import os, time

_MAX_BYTES = 1_000_000  # einfache Rotation bei ~1MB


def _target_path() -> str:
    # Root = Ordner von main_gui.py / Projekt-Root
    root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    root = os.path.abspath(os.path.join(root, ".."))  # zurück zum Projekt-Root
    return os.path.join(root, "debug_output.txt")


def _rotate_if_needed(p: str) -> None:
    try:
        if os.path.exists(p) and os.path.getsize(p) > _MAX_BYTES:
            bak = p + ".1"
            if os.path.exists(bak):
                try:
                    os.remove(bak)
                except Exception:
                    pass
            try:
                os.replace(p, bak)
            except Exception:
                pass
    except Exception:
        pass


def write_log(prefix: str, message: str) -> None:
    """Zentraler Logger mit Fallback & einfacher Rotation."""
    try:
        p = _target_path()
        os.makedirs(os.path.dirname(p), exist_ok=True)
        _rotate_if_needed(p)
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{prefix}] {ts} {message}\n"
        with open(p, "a", encoding="utf-8", newline="\n") as f:
            f.write(line)
    except Exception:
        # Harter Fallback: still - wir wollen niemals das UI crashen
        pass
