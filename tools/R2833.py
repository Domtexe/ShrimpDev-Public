# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List, Tuple
import shutil
import re
import py_compile


RUNNER_ID = "R2833"


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


def replace_def_block(src: str, func_name: str, new_block: str) -> Tuple[str, bool, str]:
    # Replace top-level "def func_name(...):" block until next top-level "def "
    pat = re.compile(r"^def\s+" + re.escape(func_name) + r"\s*\(.*?\):\s*\n", re.M)
    m = pat.search(src)
    if not m:
        return src, False, f"ERROR: def {func_name} not found"

    start = m.start()
    nxt = re.search(r"^def\s+\w+\s*\(.*?\):\s*\n", src[m.end():], re.M)
    end = (m.end() + nxt.start()) if nxt else len(src)

    out = src[:start] + new_block.rstrip() + "\n\n" + src[end:].lstrip("\n")
    return out, True, f"Replaced def-block: {func_name} (chars {start}-{end})"


def main() -> int:
    repo = repo_root()
    report: List[str] = []
    report.append(f"# {RUNNER_ID} PATCH: Registry-first _resolve_repo_path (no workspace)")
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

    marker = "# R2833_REGISTRY_FIRST"
    if marker in src:
        report.append("- Already applied (marker found)")
        write_report(repo, report)
        return 0

    new_block = (
        "def _resolve_repo_path(kind: str) -> str:\n"
        "    " + marker + "\n"
        "    # Registry is the source of truth. No workspace/cwd heuristics.\n"
        "    try:\n"
        "        import os\n"
        "        here_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))\n"
        "        reg_dir = os.path.join(here_root, 'registry')\n"
        "        if kind == 'private':\n"
        "            reg_fp = os.path.join(reg_dir, 'private_repo_root.txt')\n"
        "        else:\n"
        "            reg_fp = os.path.join(reg_dir, 'public_export_root.txt')\n"
        "\n"
        "        def _clean(p: str) -> str:\n"
        "            try:\n"
        "                return (p or '').strip().strip('\"')\n"
        "            except Exception:\n"
        "                return ''\n"
        "\n"
        "        def _ok(repo_path: str) -> str:\n"
        "            try:\n"
        "                if not repo_path:\n"
        "                    return ''\n"
        "                repo_path = _clean(repo_path)\n"
        "                if not repo_path:\n"
        "                    return ''\n"
        "                if os.path.isdir(repo_path) and os.path.isdir(os.path.join(repo_path, '.git')):\n"
        "                    return repo_path\n"
        "            except Exception:\n"
        "                pass\n"
        "            return ''\n"
        "\n"
        "        # 1) Registry-first\n"
        "        if os.path.isfile(reg_fp):\n"
        "            try:\n"
        "                with open(reg_fp, 'r', encoding='utf-8', errors='replace') as f:\n"
        "                    p = _clean(f.read())\n"
        "                ok = _ok(p)\n"
        "                if ok:\n"
        "                    return ok\n"
        "            except Exception:\n"
        "                pass\n"
        "\n"
        "        # 2) Fallback: deterministic paths (no workspace)\n"
        "        if kind == 'private':\n"
        "            return _ok(here_root)\n"
        "        else:\n"
        "            # sibling export folder\n"
        "            parent = os.path.dirname(here_root)\n"
        "            pub = os.path.join(parent, 'ShrimpDev_PUBLIC_EXPORT')\n"
        "            return _ok(pub)\n"
        "    except Exception:\n"
        "        return ''\n"
    )

    src2, changed, note = replace_def_block(src, "_resolve_repo_path", new_block)
    report.append(note)
    report.append(f"- Changed: **{changed}**")
    report.append("")

    if not changed:
        restore(bak, ui)
        write_report(repo, report)
        return 11

    ui.write_text(src2, encoding="utf-8", errors="replace")

    # compile check
    try:
        py_compile.compile(str(ui), doraise=True)
        report.append("OK: py_compile passed")
    except Exception as exc:
        report.append(f"COMPILE FAIL: {exc}")
        restore(bak, ui)
        write_report(repo, report)
        return 11

    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
