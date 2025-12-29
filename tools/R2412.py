import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

RID = "R2691"

ROOT = Path(r"C:\Users\rasta\OneDrive\ShrimpDev").resolve()
DOCS = ROOT / "docs"
ARCHIV = ROOT / "_Archiv"

# SAFE SCOPE (minimal)
SAFE_PATHS = [
    "docs/PIPELINE.md",
    # Optional later:
    # "docs/ARCHITECTURE.md",
    # "docs/Architecture_ShrimpDev.md",
    # "docs/DEVELOPMENT_RULES.md",
]


def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def now_human() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_text(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def backup_file(p: Path) -> Path | None:
    if not p.exists():
        return None
    ARCHIV.mkdir(parents=True, exist_ok=True)
    b = ARCHIV / f"{p.name}.{RID}_{ts()}.bak"
    shutil.copy2(p, b)
    return b


def run(cmd: list[str], cwd: Path, report: list[str]) -> tuple[int, str]:
    try:
        cp = subprocess.run(
            cmd,
            cwd=str(cwd),
            text=True,
            capture_output=True,
            shell=False,
        )
        out = (cp.stdout or "") + (cp.stderr or "")
        report.append(f"$ ({cwd}) " + " ".join(cmd))
        if out.strip():
            report.append(out.strip())
        return cp.returncode, out
    except Exception as e:
        report.append(f"ERROR running: {' '.join(cmd)} -> {e!r}")
        return 99, repr(e)


def ensure_expected_root(report: list[str]) -> bool:
    here = Path(__file__).resolve().parent.parent
    if here != ROOT:
        report.append("ERROR: Wrong root detected.")
        report.append(f"Expected: {ROOT}")
        report.append(f"Actual:   {here}")
        return False
    return True


def main() -> int:
    report: list[str] = []
    report.append(f"[{RID}] Private Push SAFE (docs-only)")
    report.append(f"Time: {now_human()}")
    report.append(f"Root: {ROOT}")
    report.append("Safe paths:")
    for p in SAFE_PATHS:
        report.append(f"- {p}")
    report.append("")

    if not ensure_expected_root(report):
        rp = DOCS / f"Report_{RID}_PrivatePushSAFE_{ts()}.md"
        write_text(rp, "\n".join(report) + "\n")
        print(f"[{RID}] ERROR: wrong root. Report: {rp}")
        return 2

    # Sanity: ensure git repo
    if not (ROOT / ".git").exists():
        report.append("ERROR: .git missing in private root.")
        rp = DOCS / f"Report_{RID}_PrivatePushSAFE_{ts()}.md"
        write_text(rp, "\n".join(report) + "\n")
        print(f"[{RID}] ERROR: not a git repo. Report: {rp}")
        return 3

    # Stage only safe paths (if present)
    staged_any = False
    for rel in SAFE_PATHS:
        src = ROOT / rel
        if not src.exists():
            report.append(f"WARN: missing (skipped) {rel}")
            continue
        rc, _ = run(["git", "add", rel], ROOT, report)
        if rc != 0:
            report.append(f"ERROR: git add failed for {rel}")
            rp = DOCS / f"Report_{RID}_PrivatePushSAFE_{ts()}.md"
            write_text(rp, "\n".join(report) + "\n")
            print(f"[{RID}] ERROR: add failed. Report: {rp}")
            return 4
        staged_any = True

    if not staged_any:
        report.append("NO-OP: nothing to stage (no safe files found).")
        rp = DOCS / f"Report_{RID}_PrivatePushSAFE_{ts()}.md"
        write_text(rp, "\n".join(report) + "\n")
        print(f"[{RID}] OK (NO-OP): Report {rp}")
        return 0

    # Check if anything actually staged
    rc, staged = run(["git", "diff", "--cached", "--name-only"], ROOT, report)
    if rc != 0:
        report.append("ERROR: git diff --cached failed.")
        rp = DOCS / f"Report_{RID}_PrivatePushSAFE_{ts()}.md"
        write_text(rp, "\n".join(report) + "\n")
        print(f"[{RID}] ERROR: diff failed. Report: {rp}")
        return 5

    staged = staged.strip()
    if not staged:
        report.append("NO-OP: nothing changed in safe paths; no commit/push.")
        rp = DOCS / f"Report_{RID}_PrivatePushSAFE_{ts()}.md"
        write_text(rp, "\n".join(report) + "\n")
        print(f"[{RID}] OK (NO-OP): Report {rp}")
        return 0

    report.append("Staged:")
    for line in staged.splitlines():
        report.append(f"- {line}")
    report.append("")

    # Commit (safe message)
    msg = f"docs: safe push ({RID})"
    rc, out = run(["git", "commit", "-m", msg], ROOT, report)
    if rc != 0:
        # If commit fails because nothing to commit, treat as OK
        if "nothing to commit" in out.lower():
            report.append("NO-OP: nothing to commit.")
            rp = DOCS / f"Report_{RID}_PrivatePushSAFE_{ts()}.md"
            write_text(rp, "\n".join(report) + "\n")
            print(f"[{RID}] OK (NO-OP): Report {rp}")
            return 0
        report.append("ERROR: git commit failed.")
        rp = DOCS / f"Report_{RID}_PrivatePushSAFE_{ts()}.md"
        write_text(rp, "\n".join(report) + "\n")
        print(f"[{RID}] ERROR: commit failed. Report: {rp}")
        return 6

    # Push
    rc, _ = run(["git", "push"], ROOT, report)
    rp = DOCS / f"Report_{RID}_PrivatePushSAFE_{ts()}.md"
    write_text(rp, "\n".join(report) + "\n")

    if rc != 0:
        print(f"[{RID}] ERROR: push failed. Report {rp}")
        return 7

    print(f"[{RID}] OK: pushed safe docs. Report {rp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
