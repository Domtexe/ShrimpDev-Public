import sys
import glob
import py_compile
from pathlib import Path
from datetime import datetime

RID = "R2808"

def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def write_report(root: Path, content: str) -> Path:
    d = root / "Reports"
    d.mkdir(parents=True, exist_ok=True)
    rp = d / f"Report_{RID}_{ts()}.md"
    rp.write_text(content, encoding="utf-8")
    return rp

def compile_gate(p: Path):
    py_compile.compile(str(p), doraise=True)

def newest_backup(path: Path, rid: str) -> Path | None:
    pat = str(path) + f".{rid}_*.bak"
    cands = sorted(glob.glob(pat))
    if not cands:
        return None
    # newest by filename timestamp; good enough here
    return Path(cands[-1])

def safe_neutralize_popup_calls(text: str) -> tuple[str, int]:
    """
    Replace any line containing _r1851_show_popup( with a 'pass' line of same indentation.
    This prevents empty try blocks -> IndentationError.
    """
    out = []
    n = 0
    for ln in text.splitlines(True):
        if "_r1851_show_popup" in ln:
            indent = ln[:len(ln) - len(ln.lstrip(" \t"))]
            out.append(f"{indent}pass  # {RID}: popup removed from UI\n")
            n += 1
        else:
            out.append(ln)
    return "".join(out), n

def main():
    if len(sys.argv) < 2:
        return 11

    root = Path(sys.argv[1]).resolve()
    ui = root / "modules" / "ui_toolbar.py"

    notes = []
    notes.append(f"# {RID} – Hotfix ui_toolbar.py after R2807 IndentationError\n\n")
    notes.append(f"Root: `{root}`\n\n")
    notes.append(f"Target: `{ui}`\n\n")

    if not ui.exists():
        rp = write_report(root, "".join(notes) + "**FAIL** ui_toolbar.py missing\n")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    # 1) restore from latest R2807 backup if present
    bak = newest_backup(ui, "R2807")
    if bak and bak.exists():
        ui.write_text(bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        notes.append(f"- Restored from backup: `{bak.name}`\n")
    else:
        notes.append("- WARNING: No R2807 backup found; patching current file as-is\n")

    # 2) safe neutralize popup calls (replace line, don't delete)
    txt = ui.read_text(encoding="utf-8", errors="replace")
    txt2, n = safe_neutralize_popup_calls(txt)
    ui.write_text(txt2, encoding="utf-8")
    notes.append(f"- Neutralized popup lines in UI: {n}\n")

    # 3) compile gate
    try:
        compile_gate(ui)
        notes.append("- py_compile: OK\n")
    except Exception as e:
        # rollback to backup if we had one
        if bak and bak.exists():
            ui.write_text(bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
            notes.append(f"- ROLLBACK to `{bak.name}` due to compile fail\n")
        rp = write_report(root, "".join(notes) + f"\n**FAIL** {e}\n")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    rp = write_report(root, "".join(notes) + "\n**RESULT: OK**\n")
    print(f"[{RID}] OK: Report: {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
