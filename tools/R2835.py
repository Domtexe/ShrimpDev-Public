# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List
import shutil
import py_compile


RUNNER_ID = "R2835"


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
    report.append(f"# {RUNNER_ID} PATCH: Registry-first resolver")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    ui = repo / "modules" / "ui_toolbar.py"
    if not ui.exists():
        report.append("ERROR: modules/ui_toolbar.py not found")
        write_report(repo, report)
        return 11

    bak = backup(repo, ui)
    report.append(f"- Backup: `{bak}`")
    report.append("")

    lines = ui.read_text(encoding="utf-8", errors="replace").splitlines()

    start = 1057  # 1-based -> index 1057 = line 1058
    end   = 1131  # inclusive

    if len(lines) < end:
        report.append("ERROR: File shorter than expected block range")
        restore(bak, ui)
        write_report(repo, report)
        return 11

    new_block = [
        "    def _resolve_repo_path(kind: str) -> str:",
        "        # R2835_REGISTRY_FIRST",
        "        # Registry is source of truth. Workspace/cwd removed.",
        "        try:",
        "            import os",
        "            here_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))",
        "            reg_dir = os.path.join(here_root, 'registry')",
        "            if kind == 'private':",
        "                reg_fp = os.path.join(reg_dir, 'private_repo_root.txt')",
        "            else:",
        "                reg_fp = os.path.join(reg_dir, 'public_export_root.txt')",
        "",
        "            def _clean(p: str) -> str:",
        "                try:",
        "                    return (p or '').strip().strip('\"')",
        "                except Exception:",
        "                    return ''",
        "",
        "            def _ok(p: str) -> str:",
        "                try:",
        "                    if not p:",
        "                        return ''",
        "                    p = _clean(p)",
        "                    if os.path.isdir(p) and os.path.isdir(os.path.join(p, '.git')):",
        "                        return p",
        "                except Exception:",
        "                    pass",
        "                return ''",
        "",
        "            # 1) Registry",
        "            if os.path.isfile(reg_fp):",
        "                try:",
        "                    with open(reg_fp, 'r', encoding='utf-8', errors='replace') as f:",
        "                        p = f.read()",
        "                    ok = _ok(p)",
        "                    if ok:",
        "                        return ok",
        "                except Exception:",
        "                    pass",
        "",
        "            # 2) Deterministic fallback (no workspace)",
        "            if kind == 'private':",
        "                return _ok(here_root)",
        "            else:",
        "                parent = os.path.dirname(here_root)",
        "                return _ok(os.path.join(parent, 'ShrimpDev_PUBLIC_EXPORT'))",
        "        except Exception:",
        "            return ''",
    ]

    # Replace exact slice
    new_lines = lines[:start] + new_block + lines[end:]

    ui.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    try:
        py_compile.compile(str(ui), doraise=True)
        report.append("OK: py_compile passed")
    except Exception as exc:
        report.append(f"COMPILE FAIL: {exc}")
        restore(bak, ui)
        write_report(repo, report)
        return 11

    report.append("SUCCESS: Resolver replaced (registry-first, workspace removed)")
    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
