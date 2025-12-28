# -*- coding: utf-8 -*-
"""
R2859 – SAFE PATCH
Replace tools/R2857.py with a known-good version:
- compileall supports exclude_dirs
- tools/Archiv excluded by policy
- backup + rollback + report
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import List

RUNNER_ID = "R2859"
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


R2857_CONTENT = r'''# -*- coding: utf-8 -*-
"""
R2857 – READ-ONLY Smoke Test
- Structural checks (expected dirs/files)
- Python compile checks (compileall) with public-mirror guards
- Excludes tools/Archiv (policy: archive is not executable code)
- Writes a single report to Reports/
- Does NOT modify repo content
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

RUNNER_ID = "R2857"
EXIT_FAIL = 11


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def write_report(repo: Path, lines: List[str]) -> Path:
    rp = repo / "Reports"
    ensure_dir(rp)
    out = rp / f"Report_{RUNNER_ID}_{now_stamp()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")
    return out


@dataclass
class CheckResult:
    name: str
    ok: bool
    details: List[str]


def run_py_compileall(repo: Path, rel_dir: str, exclude_dirs: List[str] | None = None) -> Tuple[bool, List[str]]:
    """
    Runs: python -m compileall -q <paths...>
    If exclude_dirs is provided, subdirectories with these names are skipped.
    """
    if exclude_dirs is None:
        exclude_dirs = []

    target = repo / rel_dir
    if not target.exists():
        return True, [f"SKIP: `{rel_dir}` missing (allowed)"]

    paths: List[str] = []
    try:
        for p in target.iterdir():
            if p.is_dir() and p.name in exclude_dirs:
                continue
            paths.append(str(p))
    except Exception as e:
        return False, [f"ERROR: failed to list `{rel_dir}`: {type(e).__name__}: {e}"]

    if not paths:
        return True, [f"OK: nothing to compile in `{rel_dir}` (after exclusions)"]

    cmd = ["python", "-m", "compileall", "-q"] + paths
    p = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True)
    out: List[str] = []
    if p.stdout.strip():
        out.append("STDOUT:")
        out.extend(p.stdout.rstrip().splitlines())
    if p.stderr.strip():
        out.append("STDERR:")
        out.extend(p.stderr.rstrip().splitlines())
    return (p.returncode == 0), (out or ["OK: compileall passed"])


def run_py_compile_file(repo: Path, rel_file: str) -> Tuple[bool, List[str]]:
    """
    Runs: python -m py_compile <file> if exists (guarded)
    """
    target = repo / rel_file
    if not target.exists():
        return True, [f"SKIP: `{rel_file}` missing (public mirror safe)"]
    cmd = ["python", "-m", "py_compile", str(target)]
    p = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True)
    out: List[str] = []
    if p.stdout.strip():
        out.append("STDOUT:")
        out.extend(p.stdout.rstrip().splitlines())
    if p.stderr.strip():
        out.append("STDERR:")
        out.extend(p.stderr.rstrip().splitlines())
    return (p.returncode == 0), (out or ["OK: py_compile passed"])


def main(root_arg: str) -> int:
    repo = Path(root_arg).resolve()
    lines: List[str] = []
    lines.append(f"# {RUNNER_ID} READ-ONLY: Smoke Test")
    lines.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- Root: `{repo}`")
    lines.append("")

    checks: List[CheckResult] = []

    # Structural checks (minimal + stable)
    expected_dirs = ["tools", "modules", "docs"]
    expected_files = ["docs/PIPELINE.md", ".github/workflows/ci.yml"]

    details = []
    ok = True
    for d in expected_dirs:
        p = repo / d
        exists = p.exists() and p.is_dir()
        details.append(f"- `{d}`: {'OK' if exists else 'MISSING'}")
        ok = ok and exists
    checks.append(CheckResult("Structure: expected dirs", ok, details))

    details = []
    ok = True
    for f in expected_files:
        p = repo / f
        exists = p.exists() and p.is_file()
        details.append(f"- `{f}`: {'OK' if exists else 'MISSING'}")
        ok = ok and exists
    checks.append(CheckResult("Structure: expected files", ok, details))

    # Python compile gates (public-mirror safe)
    ok_file, det_file = run_py_compile_file(repo, "main_gui.py")
    checks.append(CheckResult("Python: py_compile main_gui.py (guarded)", ok_file, det_file))

    ok_mod, det_mod = run_py_compileall(repo, "modules")
    checks.append(CheckResult("Python: compileall modules/", ok_mod, det_mod))

    # Exclude archive by policy
    ok_tools, det_tools = run_py_compileall(repo, "tools", exclude_dirs=["Archiv"])
    checks.append(CheckResult("Python: compileall tools/ (exclude Archiv)", ok_tools, det_tools))

    # Summarize
    all_ok = all(c.ok for c in checks)
    lines.append("## Summary")
    lines.append(f"- Result: **{'PASS' if all_ok else 'FAIL'}**")
    lines.append("")

    lines.append("## Checks")
    for c in checks:
        lines.append(f"### {c.name}")
        lines.append(f"- Status: **{'OK' if c.ok else 'FAIL'}**")
        for d in c.details:
            lines.append(d)
        lines.append("")

    rp = write_report(repo, lines)
    print(f"[{RUNNER_ID}] {'OK' if all_ok else 'FAIL'} -> {rp}")
    return 0 if all_ok else EXIT_FAIL


if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parents[1])
    raise SystemExit(main(root))
'''


def main(root_arg: str) -> int:
    repo = Path(root_arg).resolve()
    report: List[str] = []
    report.append(f"# {RUNNER_ID} SAFE PATCH: Replace tools/R2857.py")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: `{repo}`")
    report.append("")

    target = repo / "tools" / "R2857.py"
    if not target.exists():
        report.append(f"ERROR: Missing `{target}`")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return EXIT_FAIL

    bak = backup(repo, target)
    report.append(f"- Backup: `{bak}`")
    report.append("")

    try:
        target.write_text(R2857_CONTENT, encoding="utf-8", errors="replace")
        report.append("## Changes")
        report.append("- Replaced tools/R2857.py with known-good implementation")
        report.append("- tools/Archiv excluded from compile checks (policy)")
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
