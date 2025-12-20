# -*- coding: utf-8 -*-
"""Context State (Runtime)

Zweck:
- Zentrale, kleine Zustands-Sammlung für ShrimpDev (UI / Agent / Pipeline).
- Keine globale Wildwest-Nutzung: Zugriff ausschließlich über Funktionen.
- Default: Runtime (In-Memory), optional persistierbar.

R2118 – Initiale Einführung (Phase 4.1a, pure).
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict

_CONTEXT: Dict[str, Any] = {
    "active_tab": None,
    "last_action": None,
    "last_runner": None,
    "syntax_ok": None,
    "unsaved_changes": None,
    "intake_has_code": None,
    "errors_detected": None,
    "timestamp": None,
}

_DEFAULT_PATH = Path(__file__).resolve().parent.parent / "_State" / "context_state.json"

def _now() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")

def get_context() -> Dict[str, Any]:
    """Gibt eine Kopie des aktuellen Context zurück."""
    return dict(_CONTEXT)

def update_context(**kwargs: Any) -> Dict[str, Any]:
    """Aktualisiert Context-Felder (bewusst flach gehalten)."""
    for k, v in kwargs.items():
        _CONTEXT[k] = v
    _CONTEXT["timestamp"] = _now()
    return dict(_CONTEXT)

def reset_context() -> Dict[str, Any]:
    """Setzt Context auf Initialzustand zurück."""
    for k in list(_CONTEXT.keys()):
        _CONTEXT[k] = None
    _CONTEXT["timestamp"] = _now()
    return dict(_CONTEXT)

def save_context(path: Path | None = None) -> Path:
    """Persistiert Context als JSON (optional, Debug/Pipeline)."""
    p = path or _DEFAULT_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(_CONTEXT, indent=2, ensure_ascii=False), encoding="utf-8")
    return p

def load_context(path: Path | None = None) -> Dict[str, Any]:
    """Lädt Context aus JSON (falls vorhanden) und merged."""
    p = path or _DEFAULT_PATH
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                _CONTEXT.update(data)
        except Exception:
            pass
    return dict(_CONTEXT)
