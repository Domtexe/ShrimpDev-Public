# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List
import shutil
import py_compile


RUNNER_ID = "R2837"


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


def backup(repo: Path, target: Path) -> Path:
    arch = repo / "_Archiv"
    ensure_dir(arch)
    bak = arch / f"{target.name}.{RUNNER_ID}_{now()}.bak"
    shutil.copy2(target, bak)
    return bak


def restore(bak: Path, target: Path) -> None:
    if bak.exists():
        shutil.copy2(bak, target)


def main() -> int:
    repo = repo_root()
    report: List[str] = []
    report.append(f"# {RUNNER_ID} PATCH: Disable push buttons when wrapper missing")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: `{repo}`")
    report.append("")

    ui = repo / "modules" / "ui_toolbar.py"
    if not ui.exists():
        report.append("ERROR: modules/ui_toolbar.py not found")
        write_report(repo, report)
        return 11

    bak = backup(repo, ui)
    report.append(f"- Backup: `{bak}`")
    report.append("")

    src = ui.read_text(encoding="utf-8", errors="replace")

    marker = "R2837_WRAPPER_GATING"
    if marker in src:
        report.append("- Already applied (marker found)")
        write_report(repo, report)
        return 0

    # Anchor around where pushables are computed in _update_push_states
    # We patch by inserting a small block right after the public_pushable line.
    anchor = "public_pushable"
    idx = src.find(anchor)
    if idx < 0:
        report.append("ERROR: anchor 'public_pushable' not found")
        restore(bak, ui)
        write_report(repo, report)
        return 11

    # We insert a block that ANDs pushables with wrapper existence.
    insert_block = (
        "\n"
        "        # R2837_WRAPPER_GATING\n"
        "        try:\n"
        "            _tools = Path(__file__).resolve().parent.parent / 'tools'\n"
        "            _has_priv_wrap = (_tools / 'R2691.cmd').exists()\n"
        "            _has_pub_wrap  = (_tools / 'R2692.cmd').exists()\n"
        "            private_pushable = bool(private_pushable and _has_priv_wrap)\n"
        "            public_pushable  = bool(public_pushable  and _has_pub_wrap)\n"
        "        except Exception:\n"
        "            pass\n"
    )

    # Insert right after the line that defines public_pushable (first occurrence).
    lines = src.splitlines(True)
    out_lines = []
    inserted = False
    for ln in lines:
        out_lines.append(ln)
        if (not inserted) and ("public_pushable" in ln) and ("=" in ln):
            out_lines.append(insert_block)
            inserted = True

    if not inserted:
        report.append("ERROR: failed to insert block after public_pushable assignment")
        restore(bak, ui)
        write_report(repo, report)
        return 11

    ui.write_text("".join(out_lines), encoding="utf-8", errors="replace")

    try:
        py_compile.compile(str(ui), doraise=True)
        report.append("OK: py_compile passed")
    except Exception as exc:
        report.append(f"COMPILE FAIL: {exc}")
        restore(bak, ui)
        write_report(repo, report)
        return 11

    report.append("SUCCESS:")
    report.append("- Push buttons now require wrappers:")
    report.append("  - tools/R2691.cmd (private)")
    report.append("  - tools/R2692.cmd (public)")
    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
