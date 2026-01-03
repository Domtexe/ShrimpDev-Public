"""
Pure repository/registry helpers (NO Tk imports).

Design goals:
- Side-effect free (best-effort reads)
- Windows-safe paths
- Git checks via subprocess (no shell=True)
- Import-safe (usable in smoke tests)
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Optional

def project_root() -> Path:
    """Resolve project root assuming this file lives in <root>/modules/."""
    return Path(__file__).resolve().parent.parent

def registry_dir() -> Path:
    return project_root() / "registry"

def read_registry_path(filename: str) -> str:
    """Read a registry path file (best-effort). Returns '' if missing/invalid."""
    try:
        p = registry_dir() / filename
        if not p.exists():
            return ""
        txt = (p.read_text(encoding="utf-8", errors="replace") or "").strip()
        return txt.strip('"')
    except Exception:
        return ""

def is_git_repo(path: str | Path) -> bool:
    try:
        p = Path(path)
        return bool(path) and p.is_dir() and (p / ".git").is_dir()
    except Exception:
        return False

def repo_dirty(path: str | Path) -> bool:
    """Return True if repo has uncommitted changes (best-effort)."""
    try:
        if not is_git_repo(path):
            return False
        r = subprocess.run(
            ["git", "-C", str(path), "status", "--porcelain"],
            capture_output=True,
            text=True,
        )
        return bool((r.stdout or "").strip())
    except Exception:
        return False

def repo_ahead(path: str | Path) -> bool:
    """Return True if repo is ahead of upstream (best-effort)."""
    try:
        if not is_git_repo(path):
            return False
        r = subprocess.run(
            ["git", "-C", str(path), "status", "-sb"],
            capture_output=True,
            text=True,
        )
        return "ahead" in ((r.stdout or "").lower())
    except Exception:
        return False

def repo_pushable(path: str | Path) -> bool:
    """Pushable iff dirty OR ahead (best-effort)."""
    return repo_dirty(path) or repo_ahead(path)

def file_exists_rel(rel: str | Path) -> bool:
    """Best-effort existence check relative to project root."""
    try:
        p = project_root() / Path(rel)
        return p.exists()
    except Exception:
        return False

def normalize_path(p: str | Path) -> str:
    try:
        return str(Path(p).resolve())
    except Exception:
        return str(p)
