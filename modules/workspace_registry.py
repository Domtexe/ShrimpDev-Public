"""
Workspace Registry API (READ-ONLY)

Registry file: registry/workspaces.json

Schema (minimum):
{
  "active": "default",
  "workspaces": {
    "default": {
      "path": "C:/.../ShrimpDev",
      "type": "project",
      "valid": true,
      "last_seen": "2025-12-21T14:50:00"
    }
  }
}

R2436: Canonical loader to remove hardcoded roots from UI/tools.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

REGISTRY_REL = Path("registry") / "workspaces.json"


def _now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _project_root(project_root: str | Path | None = None) -> Path:
    if project_root:
        return Path(project_root).resolve()
    # modules/ -> project root
    return Path(__file__).resolve().parent.parent


def registry_path(project_root: str | Path | None = None) -> Path:
    return _project_root(project_root) / REGISTRY_REL


def load_registry(project_root: str | Path | None = None) -> dict[str, Any]:
    rp = registry_path(project_root)
    if not rp.exists():
        # caller may have created it via runner; but stay safe
        return {
            "active": "default",
            "workspaces": {
                "default": {
                    "path": str(_project_root(project_root)),
                    "type": "project",
                    "valid": True,
                    "last_seen": _now_iso(),
                }
            },
        }
    try:
        data = json.loads(rp.read_text(encoding="utf-8"))
    except Exception:
        # corrupt file -> keep app alive, fall back
        data = {
            "active": "default",
            "workspaces": {
                "default": {
                    "path": str(_project_root(project_root)),
                    "type": "project",
                    "valid": True,
                    "last_seen": _now_iso(),
                }
            },
        }

    # normalize + validate
    ws = data.get("workspaces", {})
    if not isinstance(ws, dict):
        ws = {}
    for name, cfg in list(ws.items()):
        if not isinstance(cfg, dict):
            ws.pop(name, None)
            continue
        p = Path(str(cfg.get("path", ""))).expanduser()
        cfg["path"] = str(p)
        cfg["valid"] = bool(p.exists())
        cfg["last_seen"] = _now_iso()
    data["workspaces"] = ws

    active = data.get("active", "default")
    if active not in ws and ws:
        data["active"] = next(iter(ws.keys()))
    elif not ws:
        data["active"] = "default"
        data["workspaces"] = {
            "default": {
                "path": str(_project_root(project_root)),
                "type": "project",
                "valid": True,
                "last_seen": _now_iso(),
            }
        }

    return data


def list_workspaces(project_root: str | Path | None = None) -> list[tuple[str, Path, bool]]:
    data = load_registry(project_root)
    out: list[tuple[str, Path, bool]] = []
    for name, cfg in data.get("workspaces", {}).items():
        p = Path(str(cfg.get("path", "")))
        out.append((str(name), p, bool(cfg.get("valid", False))))
    return out


def get_active_workspace_root(project_root: str | Path | None = None) -> Path:
    data = load_registry(project_root)
    active = data.get("active", "default")
    cfg = data.get("workspaces", {}).get(active) or {}
    p = Path(str(cfg.get("path", "")))
    # last resort: project root
    if not str(p).strip():
        return _project_root(project_root)
    return p


def get_active_name(project_root: str | Path | None = None) -> str:
    data = load_registry(project_root)
    return str(data.get("active", "default"))


def explain_active(project_root: str | Path | None = None) -> str:
    data = load_registry(project_root)
    name = str(data.get("active", "default"))
    cfg = data.get("workspaces", {}).get(name, {})
    return f"active={name} path={cfg.get('path', '')} valid={cfg.get('valid', False)}"


# R2437: write support (controlled) for UI dropdown
def save_registry(data: dict[str, Any], project_root: str | Path | None = None) -> bool:
    """Write registry/workspaces.json. Returns True on success."""
    try:
        rp = registry_path(project_root)
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return True
    except Exception:
        return False


def set_active_workspace(name: str, project_root: str | Path | None = None) -> bool:
    """Set active workspace by name and persist."""
    try:
        data = load_registry(project_root)
        ws = data.get("workspaces", {})
        if name not in ws:
            return False
        data["active"] = str(name)
        # refresh validation/last_seen
        _ = load_registry(project_root)  # normalize once
        data = load_registry(project_root)
        data["active"] = str(name)
        return save_registry(data, project_root)
    except Exception:
        return False
