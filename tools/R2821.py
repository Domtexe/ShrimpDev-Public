import sys, re, py_compile
from pathlib import Path
from datetime import datetime

RID="R2821"

def ts(): return datetime.now().strftime("%Y%m%d_%H%M%S")

def report(root: Path, txt: str) -> Path:
    d = root/"Reports"; d.mkdir(exist_ok=True)
    rp = d/f"Report_{RID}_{ts()}.md"
    rp.write_text(txt, encoding="utf-8")
    return rp

def backup(p: Path) -> Path:
    b = p.with_suffix(p.suffix + f".{RID}_{ts()}.bak")
    b.write_text(p.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    return b

def compile_gate(p: Path):
    py_compile.compile(str(p), doraise=True)

def main():
    root = Path(sys.argv[1]).resolve()
    ui = root/"modules"/"ui_toolbar.py"
    notes=[f"# {RID} – Fix .git dir/file detection for push gating\n\n", f"Target: `{ui}`\n\n"]

    if not ui.exists():
        rp = report(root, "".join(notes)+"**FAIL** missing ui_toolbar.py\n")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    bak = backup(ui)
    notes.append(f"- Backup: `{bak.name}`\n")

    src = ui.read_text(encoding="utf-8", errors="replace")

    # Replace only the strict .git dir checks
    n1 = src.count('os.path.isdir(os.path.join(repo_path, ".git"))')
    src = src.replace(
        'os.path.isdir(os.path.join(repo_path, ".git"))',
        'os.path.exists(os.path.join(repo_path, ".git"))'
    )
    n2 = src.count('os.path.isdir(os.path.join(p, ".git"))')
    src = src.replace(
        'os.path.isdir(os.path.join(p, ".git"))',
        'os.path.exists(os.path.join(p, ".git"))'
    )

    notes.append(f"- Replaced repo_path .git isdir checks: {n1}\n")
    notes.append(f"- Replaced candidate p .git isdir checks: {n2}\n")

    ui.write_text(src, encoding="utf-8")

    try:
        compile_gate(ui)
        notes.append("- py_compile: OK\n")
    except Exception as e:
        ui.write_text(bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        rp = report(root, "".join(notes)+f"\n**FAIL** compile: {e}\nRollback: `{bak.name}`\n")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    rp = report(root, "".join(notes)+"\n**RESULT: OK**\n")
    print(f"[{RID}] OK: Report: {rp}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
