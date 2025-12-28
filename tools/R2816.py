import sys
import re
import py_compile
from pathlib import Path
from datetime import datetime

RID="R2816"

def ts(): return datetime.now().strftime("%Y%m%d_%H%M%S")

def report(root: Path, txt: str) -> Path:
    d = root / "Reports"
    d.mkdir(exist_ok=True)
    rp = d / f"Report_{RID}_{ts()}.md"
    rp.write_text(txt, encoding="utf-8")
    return rp

def backup(p: Path) -> Path:
    bak = p.with_suffix(p.suffix + f".{RID}_{ts()}.bak")
    bak.write_text(p.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    return bak

def compile_gate(p: Path):
    py_compile.compile(str(p), doraise=True)

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
    notes.append(f"# {RID} – HOTFIX: _r1851_run_tools_runner requires positional label\n\n")
    notes.append(f"Root: `{root}`\n\n")
    notes.append(f"Target: `{lt}`\n\n")

    if not lt.exists():
        rp = report(root, "".join(notes) + "**FAIL** logic_tools.py missing\n")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    bak = backup(lt)
    notes.append(f"- Backup: `{bak.name}`\n")

    src = lt.read_text(encoding="utf-8", errors="replace")

    purge_scan = """
def action_tools_purge_scan(app):
    \"\"\"Run Purge Scan via tools runner. Popup is shown ONLY by logic_actions.\"\"\"
    from modules import logic_actions
    return logic_actions._r1851_run_tools_runner(app, "R2218", "Purge Scan")
""".strip("\n")

    purge_apply = """
def action_tools_purge_apply(app):
    \"\"\"Run Purge Apply via tools runner. Popup is shown ONLY by logic_actions.\"\"\"
    from modules import logic_actions
    return logic_actions._r1851_run_tools_runner(app, "R2224", "Purge Apply")
""".strip("\n")

    src, ok1 = replace_top_level_def(src, "action_tools_purge_scan", purge_scan)
    src, ok2 = replace_top_level_def(src, "action_tools_purge_apply", purge_apply)

    if not ok1 or not ok2:
        lt.write_text(bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        rp = report(root, "".join(notes) + f"**FAIL** replace missing: scan={ok1} apply={ok2}\n")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    lt.write_text(src, encoding="utf-8")

    try:
        compile_gate(lt)
        notes.append("- py_compile: OK\n")
    except Exception as e:
        lt.write_text(bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        rp = report(root, "".join(notes) + f"\n**FAIL** compile: {e}\nRollback: `{bak.name}`\n")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    rp = report(root, "".join(notes) + "\n**RESULT: OK**\n")
    print(f"[{RID}] OK: Report: {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
