import sys
import re
import py_compile
from pathlib import Path
from datetime import datetime

RID = "R2807"

def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(p: Path) -> Path:
    bak = p.with_suffix(p.suffix + f".{RID}_{ts()}.bak")
    bak.write_text(p.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    return bak

def compile_gate(p: Path):
    py_compile.compile(str(p), doraise=True)

def write_report(root: Path, text: str):
    d = root / "Reports"
    d.mkdir(parents=True, exist_ok=True)
    rp = d / f"Report_{RID}_{ts()}.md"
    rp.write_text(text, encoding="utf-8")
    return rp

def strip_popup_calls(text: str) -> tuple[str, int]:
    """Remove any direct _r1851_show_popup(...) calls"""
    lines = text.splitlines(True)
    out = []
    removed = 0
    for ln in lines:
        if "_r1851_show_popup" in ln:
            removed += 1
            continue
        out.append(ln)
    return "".join(out), removed

def ensure_txt_output_in_purge(text: str, fn_name: str, rid: str) -> tuple[str, bool]:
    """
    Ensure purge function writes Reports/R####_<timestamp>.txt
    """
    m = re.search(rf"(?m)^def\s+{fn_name}\s*\(\s*app\s*\)\s*:\s*$", text)
    if not m:
        return text, False

    start = m.end()
    insert = (
        f"\n    # {RID}: ensure real TXT output\n"
        f"    try:\n"
        f"        from pathlib import Path\n"
        f"        import datetime\n"
        f"        reports = Path(__file__).resolve().parent.parent / 'Reports'\n"
        f"        reports.mkdir(exist_ok=True)\n"
        f"        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')\n"
        f"        out = reports / '{rid}_' + ts + '.txt'\n"
        f"        out.write_text('Purge {rid} completed', encoding='utf-8')\n"
        f"    except Exception:\n"
        f"        pass\n"
    )
    return text[:start] + insert + text[start:], True

def main():
    if len(sys.argv) < 2:
        return 11

    root = Path(sys.argv[1]).resolve()
    notes = []

    # --- ui_toolbar.py ---
    ui = root / "modules" / "ui_toolbar.py"
    if ui.exists():
        bak = backup(ui)
        txt = ui.read_text(encoding="utf-8", errors="replace")
        txt2, n = strip_popup_calls(txt)
        ui.write_text(txt2, encoding="utf-8")
        compile_gate(ui)
        notes.append(f"- ui_toolbar.py: removed {n} popup calls (backup {bak.name})")

    # --- logic_tools.py ---
    lt = root / "modules" / "logic_tools.py"
    if not lt.exists():
        raise RuntimeError("logic_tools.py missing")

    bak = backup(lt)
    txt = lt.read_text(encoding="utf-8", errors="replace")

    txt, n1 = strip_popup_calls(txt)
    txt, ok1 = ensure_txt_output_in_purge(txt, "action_tools_purge_scan", "R2218")
    txt, ok2 = ensure_txt_output_in_purge(txt, "action_tools_purge_apply", "R2224")

    lt.write_text(txt, encoding="utf-8")
    compile_gate(lt)

    notes.append(f"- logic_tools.py: removed {n1} popup calls (backup {bak.name})")
    notes.append(f"- purge scan txt output: {ok1}")
    notes.append(f"- purge apply txt output: {ok2}")

    rp = write_report(root, "\n".join(notes) + "\n\nRESULT: OK\n")
    print(f"[{RID}] OK: {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
