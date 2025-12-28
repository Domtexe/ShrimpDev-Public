# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List, Dict
import os


RUNNER_ID = "R2838"


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


def read_list(fp: Path) -> List[str]:
    if not fp.exists():
        return []
    return [
        ln.strip()
        for ln in fp.read_text(encoding="utf-8", errors="replace").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]


def norm_variants(p: Path) -> Dict[str, str]:
    """Return common normalization variants used by purge logic."""
    return {
        "name": p.name,
        "stem": p.stem,
        "rel_tools": str(Path("tools") / p.name),
        "abs": str(p.resolve()),
        "abs_norm": os.path.normcase(str(p.resolve())),
    }


def main() -> int:
    repo = repo_root()
    report: List[str] = []

    report.append(f"# {RUNNER_ID} READ-ONLY: Purge Whitelist Resolution")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Repo: `{repo}`")
    report.append("")

    reg = repo / "registry"
    wl_runner = reg / "runner_whitelist.txt"
    wl_tools = reg / "tools_keep.txt"

    report.append("## Whitelists (raw)")
    report.append("")
    report.append(f"- runner_whitelist.txt: `{wl_runner}`")
    for ln in read_list(wl_runner):
        report.append(f"  - {ln}")
    report.append("")
    report.append(f"- tools_keep.txt: `{wl_tools}`")
    for ln in read_list(wl_tools):
        report.append(f"  - {ln}")
    report.append("")

    tools_dir = repo / "tools"
    candidates = [
        tools_dir / "R2691.cmd",
        tools_dir / "R2692.cmd",
        tools_dir / "R2691.py",
        tools_dir / "R2692.py",
    ]

    report.append("## Candidates")
    report.append("")
    for p in candidates:
        report.append(f"- `{p}` exists={p.exists()}")
    report.append("")

    # Build normalized whitelist sets
    wl_raw = set(read_list(wl_runner) + read_list(wl_tools))
    wl_norm = set()
    for w in wl_raw:
        wl_norm.add(w)
        wl_norm.add(os.path.normcase(w))
        wl_norm.add(w.replace("\\", "/"))
        wl_norm.add(Path(w).name)

    report.append("## Normalized whitelist variants")
    report.append("")
    for w in sorted(wl_norm):
        report.append(f"- {w}")
    report.append("")

    report.append("## Decision matrix (simulation)")
    report.append("")
    for p in candidates:
        report.append(f"### {p.name}")
        if not p.exists():
            report.append("- SKIP: file missing")
            report.append("")
            continue

        variants = norm_variants(p)
        for k, v in variants.items():
            hit = (v in wl_norm)
            report.append(f"- {k}: `{v}` -> {'HIT' if hit else 'no'}")
        keep = any(v in wl_norm for v in variants.values())
        report.append(f"- RESULT: **{'KEEP' if keep else 'ARCHIVE'}** (simulated)")
        report.append("")

    report.append("## Interpretation")
    report.append("")
    report.append("- If RESULT=ARCHIVE while you expect KEEP:")
    report.append("  - Purge compares against a different normalization (path vs name).")
    report.append("  - Or only one whitelist file is consulted.")
    report.append("  - Or extension (.cmd) is excluded by logic.")
    report.append("")
    report.append("## Next Step")
    report.append("- Patch purge logic to normalize paths consistently and protect both .cmd and .py.")
    report.append("- Single PATCH runner after confirmation.")

    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
