import sys
import re
import py_compile
from pathlib import Path
from datetime import datetime

RID = "R2813"

def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def report(root, txt):
    p = root / "Reports"
    p.mkdir(exist_ok=True)
    rp = p / f"Report_{RID}_{ts()}.md"
    rp.write_text(txt, encoding="utf-8")
    return rp

def backup(p: Path):
    b = p.with_suffix(p.suffix + f".{RID}_{ts()}.bak")
    b.write_text(p.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    return b

def compile_ok(p: Path):
    py_compile.compile(str(p), doraise=True)

def main():
    root = Path(sys.argv[1]).resolve()
    la = root / "modules" / "logic_actions.py"
    lt = root / "modules" / "logic_tools.py"
    ui = root / "modules" / "ui_toolbar.py"

    notes = [f"# {RID} FINAL FIX – Purge popup single-source (corrected)\n"]

    # --- logic_actions ---
    if not la.exists():
        raise RuntimeError("logic_actions.py missing")

    bak_la = backup(la)
    src = la.read_text(encoding="utf-8", errors="replace")

    helper = """
def _r1851_get_latest_report_text(app, runner_id: str) -> str:
    from pathlib import Path
    rid = runner_id if runner_id.startswith("R") else "R" + runner_id
    digits = "".join(c for c in rid if c.isdigit())
    reports = Path(__file__).resolve().parent.parent / "Reports"
    cands = []
    if reports.exists():
        if digits:
            cands += list(reports.glob(f"R{digits}_*.txt"))
            cands += list(reports.glob(f"R{digits}*.txt"))
        cands += list(reports.glob(f"{rid}_*.txt"))
        cands += list(reports.glob(f"{rid}*.txt"))
    if not cands:
        return ""
    newest = max(cands, key=lambda p: p.stat().st_mtime)
    return newest.read_text(encoding="utf-8", errors="replace")
""".strip()

    if "_r1851_get_latest_report_text" not in src:
        src = src + "\n\n" + helper + "\n"

    la.write_text(src, encoding="utf-8")
    compile_ok(la)
    notes.append("- logic_actions.py: helper fixed + compiled\n")

    # --- logic_tools: Purge nur Runner ---
    bak_lt = backup(lt)
    lt_src = lt.read_text(encoding="utf-8", errors="replace")

    lt_src = re.sub(
        r"def action_tools_purge_scan\(.*?\):[\s\S]*?^\S",
        'def action_tools_purge_scan(app):\n    from modules import logic_actions\n    return logic_actions._r1851_run_tools_runner(app,"R2218",title="Purge Scan")\n\n',
        lt_src,
        flags=re.M
    )

    lt_src = re.sub(
        r"def action_tools_purge_apply\(.*?\):[\s\S]*?^\S",
        'def action_tools_purge_apply(app):\n    from modules import logic_actions\n    return logic_actions._r1851_run_tools_runner(app,"R2224",title="Purge Apply")\n\n',
        lt_src,
        flags=re.M
    )

    lt.write_text(lt_src, encoding="utf-8")
    compile_ok(lt)
    notes.append("- logic_tools.py: purge functions normalized\n")

    # --- ui_toolbar: kein Popup ---
    bak_ui = backup(ui)
    ui_src = ui.read_text(encoding="utf-8", errors="replace")
    ui_src = ui_src.replace("_wrap_with_led_and_report_popup", "_wrap_with_led_only")
    ui.write_text(ui_src, encoding="utf-8")
    compile_ok(ui)
    notes.append("- ui_toolbar.py: popup wrapper removed\n")

    rp = report(root, "\n".join(notes) + "\nRESULT: OK\n")
    print(rp)
    return 0

if __name__ == "__main__":
    sys.exit(main())
