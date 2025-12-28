import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

RID = "R2692"

PRIVATE_ROOT = Path(r"C:\Users\rasta\OneDrive\ShrimpDev").resolve()
PUBLIC_ROOT = Path(r"C:\Users\rasta\OneDrive\ShrimpDev_PUBLIC_EXPORT").resolve()

REGISTRY_DIR = PRIVATE_ROOT / "registry"
ALLOWLIST = REGISTRY_DIR / "public_allowlist.txt"

TOOLS_KEEP = PRIVATE_ROOT / "tools_keep.txt"

ARCHIV = PRIVATE_ROOT / "_Archiv"
DOCS = PRIVATE_ROOT / "docs"


def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def now_human() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def norm(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def write_text(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def read_text(p: Path) -> str:
    return norm(p.read_text(encoding="utf-8", errors="replace"))


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
    if here != PRIVATE_ROOT:
        report.append("ERROR: Wrong private root detected.")
        report.append(f"Expected: {PRIVATE_ROOT}")
        report.append(f"Actual:   {here}")
        return False
    return True


def ensure_allowlist(report: list[str]) -> None:
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    if not ALLOWLIST.exists():
        default = "\n".join(
            [
                "# Public export allowlist (relative paths from repo root)",
                "# One entry per line. Comments start with '#'.",
                "",
                "docs/PIPELINE.md",
                "",
            ]
        )
        write_text(ALLOWLIST, default)
        report.append(
            f"OK: created {ALLOWLIST.relative_to(PRIVATE_ROOT)} with default docs/PIPELINE.md"
        )
    else:
        report.append(f"OK: found {ALLOWLIST.relative_to(PRIVATE_ROOT)}")


def parse_allowlist(report: list[str]) -> list[str]:
    lines = read_text(ALLOWLIST).split("\n")
    items: list[str] = []
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        s = s.replace("\\", "/")
        items.append(s)
    # de-dup keep order
    seen = set()
    out = []
    for x in items:
        if x not in seen:
            out.append(x)
            seen.add(x)
    report.append(f"Allowlist entries: {len(out)}")
    return out


def ensure_tools_keep_contains(runner_id: str, report: list[str]) -> None:
    # Ensure tools_keep exists
    if not TOOLS_KEEP.exists():
        header = "\n".join(
            [
                "# filenames in tools\\ root that must stay (one per line)",
                "# runner ids without extension, e.g. R2692",
                "",
            ]
        )
        write_text(TOOLS_KEEP, header)
        report.append(f"OK: created {TOOLS_KEEP.relative_to(PRIVATE_ROOT)}")

    old = read_text(TOOLS_KEEP).split("\n")
    existing = set()
    for ln in old:
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        existing.add(s)

    if runner_id in existing:
        report.append(f"NO-OP: tools_keep already contains {runner_id}")
        return

    backup_file(TOOLS_KEEP)
    new = norm(read_text(TOOLS_KEEP)).rstrip() + "\n" + runner_id + "\n"
    write_text(TOOLS_KEEP, new)
    report.append(f"OK: appended {runner_id} to tools_keep.txt (Purge-Whitelist)")


def file_equal(a: Path, b: Path) -> bool:
    if not a.exists() or not b.exists():
        return False
    return read_text(a) == read_text(b)


def copy_allowlisted(items: list[str], report: list[str]) -> list[str]:
    changed_paths: list[str] = []
    for rel in items:
        src = PRIVATE_ROOT / rel
        dst = PUBLIC_ROOT / rel
        if not src.exists():
            report.append(f"WARN: missing source -> {rel} (skipped)")
            continue

        if dst.exists() and file_equal(src, dst):
            report.append(f"NO-OP: {rel} already identical")
            continue

        # backup destination into private archive (we keep history in master)
        if dst.exists():
            backup_file(dst)

        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(read_text(src), encoding="utf-8", newline="\n")
        report.append(f"OK: copied {rel}")
        changed_paths.append(rel)

    return changed_paths


def public_git_commit_push(changed_paths: list[str], report: list[str]) -> int:
    if not changed_paths:
        report.append("NO-OP: nothing changed; no git commit/push")
        return 0

    if not (PUBLIC_ROOT / ".git").exists():
        report.append("ERROR: Public export is not a git repo (.git missing).")
        return 5

    # Stage only changed allowlisted paths
    for rel in changed_paths:
        rc, _ = run(["git", "add", rel], PUBLIC_ROOT, report)
        if rc != 0:
            report.append(f"ERROR: git add failed for {rel}")
            return 7

    # Ensure something staged
    rc, staged = run(["git", "diff", "--cached", "--name-only"], PUBLIC_ROOT, report)
    if rc != 0:
        report.append("ERROR: git diff --cached failed")
        return 8
    if not staged.strip():
        report.append("NO-OP: nothing staged (unexpected but safe)")
        return 0

    msg = f"public: sync allowlist from private ({RID})"
    rc, _ = run(["git", "commit", "-m", msg], PUBLIC_ROOT, report)
    if rc != 0:
        report.append("WARN: git commit non-zero (maybe nothing to commit).")
        # treat as soft fail, still attempt push
    rc, _ = run(["git", "push"], PUBLIC_ROOT, report)
    if rc != 0:
        report.append("ERROR: git push failed")
        return 10

    report.append("OK: public commit + push done")
    return 0


def main() -> int:
    report: list[str] = []
    report.append(f"[{RID}] Public Whitelist Sync (Private -> Public)")
    report.append(f"Time: {now_human()}")
    report.append(f"Private: {PRIVATE_ROOT}")
    report.append(f"Public:  {PUBLIC_ROOT}")
    report.append("")

    if not ensure_expected_root(report):
        rp = DOCS / f"Report_{RID}_PublicWhitelistSync_{ts()}.md"
        write_text(rp, "\n".join(report) + "\n")
        print(f"[{RID}] ERROR: wrong root. Report: {rp}")
        return 2

    if not PUBLIC_ROOT.exists():
        report.append("ERROR: Public export folder missing.")
        rp = DOCS / f"Report_{RID}_PublicWhitelistSync_{ts()}.md"
        write_text(rp, "\n".join(report) + "\n")
        print(f"[{RID}] ERROR: public missing. Report: {rp}")
        return 4

    # Ensure allowlist exists
    ensure_allowlist(report)

    # Ensure Purge-Whitelist contains R2692
    ensure_tools_keep_contains(RID, report)

    items = parse_allowlist(report)
    changed_paths = copy_allowlisted(items, report)

    rc = public_git_commit_push(changed_paths, report)

    rp = DOCS / f"Report_{RID}_PublicWhitelistSync_{ts()}.md"
    write_text(rp, "\n".join(report) + "\n")
    if rc == 0:
        print(f"[{RID}] OK: Report {rp}")
    else:
        print(f"[{RID}] ERROR({rc}): Report {rp}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
