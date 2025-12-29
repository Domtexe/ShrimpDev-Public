# -*- coding: utf-8 -*-
"""
R2860 – SAFE PATCH
Add Smoke-Test step to .github/workflows/ci.yml:
- runs: python tools/R2857.py .
- backup + rollback + report
- applies to private repo and local public mirror if present
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import List

RUNNER_ID = "R2860"
EXIT_FAIL = 11

SMOKE_STEP_YAML = """
      - name: Smoke test (R2857)
        run: |
          python tools/R2857.py .
""".lstrip("\n")

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

def patch_ci(repo: Path, report: List[str]) -> None:
    wf = repo / ".github" / "workflows" / "ci.yml"
    if not wf.exists():
        report.append(f"- SKIP: `{wf}` not found")
        return

    txt = wf.read_text(encoding="utf-8", errors="replace")
    if "Smoke test (R2857)" in txt or "tools/R2857.py" in txt:
        report.append(f"- OK: `{wf}` already contains smoke step")
        return

    bak = backup(repo, wf)
    report.append(f"- Backup: `{bak}`")

    # Insert after setup-python step block (best effort) or after checkout
    insert_after = "uses: actions/setup-python@v5"
    idx = txt.find(insert_after)
    if idx != -1:
        # find end of that step block by next "\n      - " at same indentation
        start = txt.rfind("\n      - ", 0, idx)
        if start == -1:
            start = 0
        # find next step after the setup-python block
        next_step = txt.find("\n      - ", idx + len(insert_after))
        if next_step == -1:
            next_step = len(txt)
        new_txt = txt[:next_step] + "\n" + SMOKE_STEP_YAML + txt[next_step:]
    else:
        # fallback: after checkout
        insert_after2 = "uses: actions/checkout@v4"
        idx2 = txt.find(insert_after2)
        if idx2 == -1:
            raise RuntimeError("Could not find insertion anchor in ci.yml (checkout/setup-python).")
        next_step = txt.find("\n      - ", idx2 + len(insert_after2))
        if next_step == -1:
            next_step = len(txt)
        new_txt = txt[:next_step] + "\n" + SMOKE_STEP_YAML + txt[next_step:]

    wf.write_text(new_txt, encoding="utf-8", errors="replace")
    report.append(f"- OK: patched `{wf}` (added smoke step)")

def main(root_arg: str) -> int:
    repo = Path(root_arg).resolve()
    report: List[str] = []
    report.append(f"# {RUNNER_ID} SAFE PATCH: CI add Smoke-Test step")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: `{repo}`")
    report.append("")

    try:
        report.append("## Private repo")
        patch_ci(repo, report)
        report.append("")

        pub = repo.parent / "ShrimpDev_PUBLIC_EXPORT"
        report.append("## Public mirror (local)")
        if pub.exists():
            patch_ci(pub, report)
        else:
            report.append(f"- SKIP: `{pub}` not present locally")
        report.append("")

        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] OK -> {rp}")
        return 0

    except Exception as e:
        report.append(f"ERROR: {type(e).__name__}: {e}")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return EXIT_FAIL

if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parents[1])
    raise SystemExit(main(root))
