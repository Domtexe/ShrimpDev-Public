# -*- coding: utf-8 -*-
"""
R2858 – SAFE PATCH
Refines R2857 Smoke Test:
- Excludes tools/Archiv from compile checks
- Keeps strict checks for active code
- Backup + rollback + report
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import List

RUNNER_ID = "R2858"
EXIT_FAIL = 11


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def backup(repo: Path, target: Path) -> Path:
    arch = repo / "_Archiv"
    ensure_dir(arch)
    bak = arch / f"{target.name}.{RUNNER_ID}_{now_stamp()}.bak"
    shutil.copy2(target, bak)
    return bak


def write_report(repo: Path, lines: List[str]) -> Path:
    rp = repo / "Reports"
    ensure_dir(rp)
    out = rp / f"Report_{RUNNER_ID}_{now_stamp()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")
    return out


def patch_r2857(repo: Path) -> bool:
    """
    Modify tools/R2857.py so compileall skips tools/Archiv
    """
    target = repo / "tools" / "R2857.py"
    if not target.exists():
        return False

    txt = target.read_text(encoding="utf-8", errors="replace")
    if "exclude_dirs" in txt or "tools/Archiv" in txt:
        # already patched
        return True

    old = "ok_tools, det_tools = run_py_compileall(repo, \"tools\")"
    new = (
        "ok_tools, det_tools = run_py_compileall(\n"
        "        repo,\n"
        "        \"tools\",\n"
        "        exclude_dirs=[\"Archiv\"],\n"
        "    )"
    )

    if old not in txt:
        return False

    txt = txt.replace(old, new)

    # inject helper if missing
    if "exclude_dirs" not in txt:
        inject = """
def run_py_compileall(repo: Path, rel_dir: str, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = []
    target = repo / rel_dir
    if not target.exists():
        return True, [f"SKIP: `{rel_dir}` missing (allowed)"]

    paths = []
    for p in target.iterdir():
        if p.is_dir() and p.name in exclude_dirs:
            continue
        paths.append(str(p))

    if not paths:
        return True, ["OK: nothing to compile"]

    cmd = ["python", "-m", "compileall", "-q"] + paths
    p = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True)
    out = []
    if p.stdout.strip():
        out.append("STDOUT:")
        out.extend(p.stdout.rstrip().splitlines())
    if p.stderr.strip():
        out.append("STDERR:")
        out.extend(p.stderr.rstrip().splitlines())
    return (p.returncode == 0), (out or ["OK: compileall passed"])
"""
        txt = txt.replace(
            "def run_py_compileall(repo: Path, rel_dir: str) -> Tuple[bool, List[str]]:",
            inject.strip() + "\n\n# replaced original helper\n"
            "def run_py_compileall(repo: Path, rel_dir: str) -> Tuple[bool, List[str]]:",
        )

    target.write_text(txt, encoding="utf-8", errors="replace")
    return True


def main(root_arg: str) -> int:
    repo = Path(root_arg).resolve()
    report: List[str] = []
    report.append(f"# {RUNNER_ID} SAFE PATCH: Smoke-Test refinement")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: `{repo}`")
    report.append("")

    target = repo / "tools" / "R2857.py"
    if not target.exists():
        report.append("ERROR: tools/R2857.py not found")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return EXIT_FAIL

    bak = backup(repo, target)
    report.append(f"- Patched: `{target}`")
    report.append(f"- Backup: `{bak}`")
    report.append("")

    try:
        ok = patch_r2857(repo)
        if not ok:
            raise RuntimeError("Expected pattern not found in R2857.py")

        report.append("## Changes")
        report.append("- Excluded `tools/Archiv/` from compile checks")
        report.append("- Active code paths remain fully checked")
        report.append("")
        report.append("## Rationale")
        report.append("- Archiv contains historical runners")
        report.append("- Archiv is documentation, not executable code")
        report.append("- Smoke-Test must be strict but fair")

        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] OK -> {rp}")
        return 0

    except Exception as e:
        try:
            shutil.copy2(bak, target)
        except Exception:
            pass
        report.append(f"ERROR: {type(e).__name__}: {e}")
        report.append("Rollback: restored from backup")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return EXIT_FAIL


if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parents[1])
    raise SystemExit(main(root))
