import sys
import glob
import re
import py_compile
from pathlib import Path
from datetime import datetime

RID = "R2814"

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

def backup(p: Path) -> Path:
    bak = p.with_suffix(p.suffix + f".{RID}_{ts()}.bak")
    bak.write_text(p.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    return bak

def newest_backup_anyrid(p: Path) -> Path | None:
    # pick newest file matching logic_tools.py.<RID>_YYYYMMDD_HHMMSS.bak
    pat = str(p) + ".*.bak"
    cands = sorted(glob.glob(pat))
    if not cands:
        return None
    return Path(cands[-1])

def replace_top_level_def(src: str, fn_name: str, new_block: str) -> tuple[str, bool]:
    m = re.search(rf"(?m)^def\s+{re.escape(fn_name)}\s*\(.*?\)\s*:\s*$", src)
    if not m:
        return src, False
    start = m.start()
    m2 = re.search(r"(?m)^def\s+\w+\s*\(", src[m.end():])
    end = (m.end() + m2.start()) if m2 else len(src)
    return src[:start] + new_block.rstrip() + "\n\n" + src[end:], True

def main():
    root = Path(sys.argv[1]).resolve()
    lt = root / "modules" / "logic_tools.py"

    notes = []
    notes.append(f"# {RID} – Restore+Fix logic_tools.py purge functions\n\n")
    notes.append(f"Root: `{root}`\n\n")
    notes.append(f"Target: `{lt}`\n\n")

    if not lt.exists():
        rp = write_report(root, "".join(notes) + "**FAIL** logic_tools.py missing\n")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    # Always make a safety backup of current broken state (for forensics)
    cur_bak = backup(lt)
    notes.append(f"- Safety backup (current state): `{cur_bak.name}`\n")

    # Try restore from newest prior backup (any RID)
    restored_from = None
    prev = newest_backup_anyrid(lt)
    if prev and prev.exists():
        # Don't restore from our just-created backup
        if prev.name != cur_bak.name:
            lt.write_text(prev.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
            restored_from = prev.name
            notes.append(f"- Restored from newest backup: `{restored_from}`\n")
    if restored_from is None:
        notes.append("- No prior backup found (or only current); attempting minimal syntax repair\n")
        txt = lt.read_text(encoding="utf-8", errors="replace")
        # minimal fix: 'ef action_tools_purge_apply' -> 'def action_tools_purge_apply'
        txt2, nfix = re.subn(r"(?m)^ef(\s+action_tools_purge_apply\s*\()", r"def\1", txt)
        if nfix:
            lt.write_text(txt2, encoding="utf-8")
            notes.append(f"- Minimal repair applied: fixed {nfix} occurrence(s) of 'ef ...' -> 'def ...'\n")
        else:
            notes.append("- Minimal repair: no 'ef action_tools_purge_apply' pattern found\n")

    # Now patch purge functions deterministically (no popup, no bridge)
    txt = lt.read_text(encoding="utf-8", errors="replace")

    purge_scan = """
def action_tools_purge_scan(app):
    \"\"\"Run Purge Scan via tools runner. Popup is shown ONLY by logic_actions.\"\"\"
    from modules import logic_actions
    return logic_actions._r1851_run_tools_runner(app, "R2218", title="Purge Scan")
""".strip("\n")

    purge_apply = """
def action_tools_purge_apply(app):
    \"\"\"Run Purge Apply via tools runner. Popup is shown ONLY by logic_actions.\"\"\"
    from modules import logic_actions
    return logic_actions._r1851_run_tools_runner(app, "R2224", title="Purge Apply")
""".strip("\n")

    txt, ok1 = replace_top_level_def(txt, "action_tools_purge_scan", purge_scan)
    txt, ok2 = replace_top_level_def(txt, "action_tools_purge_apply", purge_apply)

    if not ok1:
        notes.append("- WARNING: def action_tools_purge_scan not found (no replace)\n")
    else:
        notes.append("- Patched: action_tools_purge_scan\n")
    if not ok2:
        notes.append("- WARNING: def action_tools_purge_apply not found (no replace)\n")
    else:
        notes.append("- Patched: action_tools_purge_apply\n")

    lt.write_text(txt, encoding="utf-8")

    # Compile gate + rollback to safety backup if needed
    try:
        compile_gate(lt)
        notes.append("- py_compile: OK\n")
    except Exception as e:
        lt.write_text(cur_bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        notes.append(f"- ROLLBACK to `{cur_bak.name}` (compile failed)\n")
        rp = write_report(root, "".join(notes) + f"\n**FAIL** {e}\n")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    rp = write_report(root, "".join(notes) + "\n**RESULT: OK**\n")
    print(f"[{RID}] OK: Report: {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
