# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List


RUNNER_ID = "R2849"


def now() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def write_report(repo: Path, lines: List[str]) -> Path:
    rp = repo / "Reports"
    ensure_dir(rp)
    out = rp / f"Report_{RUNNER_ID}_{now()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")
    return out


def read_txt(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace").strip()
    except Exception:
        return ""


def main() -> int:
    repo = repo_root()
    lines: List[str] = []
    lines.append(f"# {RUNNER_ID} READ-ONLY: Push Button Enable/Disable Audit")
    lines.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- Repo: `{repo}`")
    lines.append("")

    tools = repo / "tools"
    priv_wrap = tools / "R2691.cmd"
    pub_wrap = tools / "R2692.cmd"
    lines.append("## Wrapper existence")
    lines.append(f"- `{priv_wrap}` exists={priv_wrap.exists()}")
    lines.append(f"- `{pub_wrap}` exists={pub_wrap.exists()}")
    lines.append("")

    reg = repo / "registry"
    priv_root = read_txt(reg / "private_repo_root.txt")
    pub_root  = read_txt(reg / "public_export_root.txt")
    lines.append("## Registry roots")
    lines.append(f"- private_repo_root.txt: `{priv_root}`")
    lines.append(f"- public_export_root.txt: `{pub_root}`")
    lines.append("")

    ui = repo / "modules" / "ui_toolbar.py"
    if not ui.exists():
        lines.append("ERROR: modules/ui_toolbar.py not found")
        rp = write_report(repo, lines)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return 11

    src = ui.read_text(encoding="utf-8", errors="replace")
    lines.append("## Markers present in ui_toolbar.py")
    for mk in ["R2836_TRACE_PUSH", "R2837_WRAPPER_GATING", "R2835_REGISTRY_FIRST"]:
        lines.append(f"- {mk}: {'YES' if mk in src else 'NO'}")
    lines.append("")

    # Show a small excerpt around the gating marker (if present)
    if "R2837_WRAPPER_GATING" in src:
        lines.append("## Excerpt around R2837_WRAPPER_GATING")
        all_lines = src.splitlines()
        idx = next((i for i, ln in enumerate(all_lines) if "R2837_WRAPPER_GATING" in ln), -1)
        start = max(0, idx - 8)
        end = min(len(all_lines), idx + 25)
        for i in range(start, end):
            lines.append(f"{i+1:>5}: {all_lines[i]}")
        lines.append("")
    else:
        lines.append("NOTE: No excerpt (gating marker missing).")
        lines.append("")

    rp = write_report(repo, lines)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
