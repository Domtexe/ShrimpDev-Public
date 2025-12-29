import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RID = "R2436"


def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def now_human() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def write_text(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8", newline="\n")


def backup(p: Path, archiv: Path) -> Path | None:
    if not p.exists():
        return None
    archiv.mkdir(parents=True, exist_ok=True)
    b = archiv / f"{p.name}.{RID}_{ts()}.bak"
    shutil.copy2(p, b)
    return b


def py_compile(root: Path, file_path: Path) -> tuple[bool, str]:
    try:
        cp = subprocess.run(
            [sys.executable, "-m", "py_compile", str(file_path)],
            cwd=str(root),
            text=True,
            capture_output=True,
        )
        ok = cp.returncode == 0
        out = (cp.stdout or "") + (cp.stderr or "")
        return ok, out.strip()
    except Exception as e:
        return False, f"py_compile exception: {e}"


def ensure_keep(root: Path, archiv: Path, report: list[str]) -> None:
    keep = root / "registry" / "tools_keep.txt"
    if not keep.exists():
        report.append("INFO: registry/tools_keep.txt not found (skip).")
        return
    txt = read_text(keep)
    items = [ln.strip() for ln in txt.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    if "R2436" in items:
        report.append("NO-OP: R2436 already in tools_keep.txt")
        return
    bk = backup(keep, archiv)
    write_text(keep, txt.rstrip() + "\nR2436\n")
    report.append(f"OK: appended R2436 to tools_keep.txt (backup={bk})")


def ensure_registry_file(root: Path, report: list[str]) -> None:
    ws = root / "registry" / "workspaces.json"
    if ws.exists():
        return
    data = {
        "active": "default",
        "workspaces": {
            "default": {
                "path": str(root),
                "type": "project",
                "valid": True,
                "last_seen": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            }
        },
    }
    ws.parent.mkdir(parents=True, exist_ok=True)
    ws.write_text(json.dumps(data, indent=2), encoding="utf-8")
    report.append("OK: created registry/workspaces.json (default)")


def main() -> int:
    tools_dir = Path(__file__).resolve().parent
    root = tools_dir.parent
    docs = root / "docs"
    archiv = root / "_Archiv"
    mod = root / "modules" / "workspace_registry.py"

    report = [
        f"[{RID}] Workspace API (READ-ONLY): modules/workspace_registry.py",
        f"Time: {now_human()}",
        f"Root: {root}",
        "",
    ]

    ensure_registry_file(root, report)

    module_code = f'''"""
Workspace Registry API (READ-ONLY)

Registry file: registry/workspaces.json

Schema (minimum):
{{
  "active": "default",
  "workspaces": {{
    "default": {{
      "path": "C:/.../ShrimpDev",
      "type": "project",
      "valid": true,
      "last_seen": "2025-12-21T14:50:00"
    }}
  }}
}}

R2436: Canonical loader to remove hardcoded roots from UI/tools.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


REGISTRY_REL = Path("registry") / "workspaces.json"


def _now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _project_root(project_root: Optional[str | Path] = None) -> Path:
    if project_root:
        return Path(project_root).resolve()
    # modules/ -> project root
    return Path(__file__).resolve().parent.parent


def registry_path(project_root: Optional[str | Path] = None) -> Path:
    return _project_root(project_root) / REGISTRY_REL


def load_registry(project_root: Optional[str | Path] = None) -> Dict[str, Any]:
    rp = registry_path(project_root)
    if not rp.exists():
        # caller may have created it via runner; but stay safe
        return {{"active": "default", "workspaces": {{"default": {{"path": str(_project_root(project_root)), "type": "project", "valid": True, "last_seen": _now_iso()}}}}}}
    try:
        data = json.loads(rp.read_text(encoding="utf-8"))
    except Exception:
        # corrupt file -> keep app alive, fall back
        data = {{"active": "default", "workspaces": {{"default": {{"path": str(_project_root(project_root)), "type": "project", "valid": True, "last_seen": _now_iso()}}}}}}

    # normalize + validate
    ws = data.get("workspaces", {{}})
    if not isinstance(ws, dict):
        ws = {{}}
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
        data["workspaces"] = {{"default": {{"path": str(_project_root(project_root)), "type": "project", "valid": True, "last_seen": _now_iso()}}}}

    return data


def list_workspaces(project_root: Optional[str | Path] = None) -> List[Tuple[str, Path, bool]]:
    data = load_registry(project_root)
    out: List[Tuple[str, Path, bool]] = []
    for name, cfg in data.get("workspaces", {{}}).items():
        p = Path(str(cfg.get("path", "")))
        out.append((str(name), p, bool(cfg.get("valid", False))))
    return out


def get_active_workspace_root(project_root: Optional[str | Path] = None) -> Path:
    data = load_registry(project_root)
    active = data.get("active", "default")
    cfg = data.get("workspaces", {{}}).get(active) or {{}}
    p = Path(str(cfg.get("path", "")))
    # last resort: project root
    if not str(p).strip():
        return _project_root(project_root)
    return p


def get_active_name(project_root: Optional[str | Path] = None) -> str:
    data = load_registry(project_root)
    return str(data.get("active", "default"))


def explain_active(project_root: Optional[str | Path] = None) -> str:
    data = load_registry(project_root)
    name = str(data.get("active", "default"))
    cfg = data.get("workspaces", {{}}).get(name, {{}})
    return f"active={{name}} path={{cfg.get('path','')}} valid={{cfg.get('valid', False)}}"
'''

    # Write module (backup if exists)
    if mod.exists():
        bk = backup(mod, archiv)
        report.append(f"Backup: {bk}")
    write_text(mod, module_code)
    report.append("OK: wrote modules/workspace_registry.py")

    ok, out = py_compile(root, mod)
    if not ok:
        report.append("ERROR: py_compile failed for workspace_registry.py")
        report.append(out)
        # rollback if we had backup
        # (if file existed before, restore backup; if new, delete file)
        if mod.exists():
            try:
                # if backup exists for this run
                candidates = sorted(
                    archiv.glob("workspace_registry.py.R2436_*.bak"),
                    key=lambda p: p.stat().st_mtime,
                    reverse=True,
                )
                if candidates:
                    shutil.copy2(candidates[0], mod)
                    report.append(f"ROLLBACK: restored from {candidates[0]}")
                else:
                    mod.unlink(missing_ok=True)
                    report.append("ROLLBACK: deleted newly created module")
            except Exception as e:
                report.append(f"ROLLBACK ERROR: {e}")

        rp = docs / f"Report_{RID}_WorkspaceAPI_{ts()}.md"
        write_text(rp, "\n".join(report) + "\n")
        print(f"[{RID}] ERROR: Report {rp}")
        return 5

    report.append("OK: py_compile passed")

    # Architecture note
    arch = docs / "Architecture_Workspaces.md"
    if not arch.exists():
        write_text(
            arch,
            "\n".join(
                [
                    "# Workspaces (Registry)",
                    "",
                    "Kanonische Quelle: `registry/workspaces.json`",
                    "",
                    "API: `modules/workspace_registry.py`",
                    "",
                    "- `get_active_workspace_root()` liefert den Root-Pfad für alle Workspace-abhängigen Aktionen.",
                    "- UI/Tools dürfen keine alten Hardcodes auf OneDrive/D:/ etc. behalten; stattdessen immer den Workspace-Root verwenden.",
                    "",
                    f"Erst-Setup via Runner: {RID}",
                    "",
                ]
            )
            + "\n",
        )
        report.append("OK: created docs/Architecture_Workspaces.md (initial)")

    ensure_keep(root, archiv, report)

    rp = docs / f"Report_{RID}_WorkspaceAPI_{ts()}.md"
    write_text(rp, "\n".join(report) + "\n")
    print(f"[{RID}] OK: Report {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
