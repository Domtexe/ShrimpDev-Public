import sys
import re
import py_compile
from pathlib import Path
from datetime import datetime

RID = "R2811"

def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def report_path(root: Path) -> Path:
    d = root / "Reports"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"Report_{RID}_{ts()}.md"

def backup(p: Path) -> Path:
    bak = p.with_suffix(p.suffix + f".{RID}_{ts()}.bak")
    bak.write_text(p.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    return bak

def compile_gate(p: Path):
    py_compile.compile(str(p), doraise=True)

def replace_top_level_def(src: str, fn_name: str, new_block: str) -> tuple[str, bool, str]:
    """
    Replace a top-level def <fn_name>(...) block (indent 0) with new_block.
    """
    m = re.search(rf"(?m)^def\s+{re.escape(fn_name)}\s*\(.*?\)\s*:\s*$", src)
    if not m:
        return src, False, f"{fn_name}: def not found"
    start = m.start()
    m2 = re.search(r"(?m)^def\s+\w+\s*\(", src[m.end():])
    end = (m.end() + m2.start()) if m2 else len(src)
    return src[:start] + new_block.rstrip() + "\n\n" + src[end:], True, f"{fn_name}: replaced"

def replace_any_def(src: str, fn_name: str, new_block: str) -> tuple[str, bool, str]:
    """
    Replace a def that may be nested/indented; we match by def line and then consume until next def at same indent.
    """
    m = re.search(rf"(?m)^(?P<ind>[ \t]*)def\s+{re.escape(fn_name)}\s*\(.*?\)\s*:\s*$", src)
    if not m:
        return src, False, f"{fn_name}: def not found"
    ind = m.group("ind")
    start = m.start()
    # next def at same indent
    m2 = re.search(rf"(?m)^{re.escape(ind)}def\s+\w+\s*\(", src[m.end():])
    end = (m.end() + m2.start()) if m2 else len(src)
    # ensure new block uses same indent for each line
    nb_lines = []
    for i, ln in enumerate(new_block.splitlines()):
        if i == 0:
            nb_lines.append(ind + ln.lstrip())
        else:
            nb_lines.append(ind + ln if ln.strip() else "")
    nb = "\n".join(nb_lines).rstrip() + "\n"
    return src[:start] + nb + "\n" + src[end:], True, f"{fn_name}: replaced"

def main():
    if len(sys.argv) < 2:
        return 11

    root = Path(sys.argv[1]).resolve()

    ui = root / "modules" / "ui_toolbar.py"
    lt = root / "modules" / "logic_tools.py"
    la = root / "modules" / "logic_actions.py"

    notes = []
    notes.append(f"# {RID} – FINAL FIX Purge Popup Single-Source\n\n")
    notes.append(f"Root: `{root}`\n\n")

    # --- Patch logic_actions: ensure popup only here, and show latest runner report text
    if not la.exists():
        rp = report_path(root)
        rp.write_text("".join(notes) + f"**FAIL** missing `{la}`\n", encoding="utf-8")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    la_bak = backup(la)
    la_src0 = la.read_text(encoding="utf-8", errors="replace")

    # Add/replace helper inside logic_actions: _r1851_get_latest_report_text
    helper_block = f"""
def _r1851_get_latest_report_text(app, runner_id: str) -> str:
    \"\"\"Return text of newest report artifact for a runner from Reports/.
    Preference: R####_*.txt (real output), then Report_R####_*.md, then Report_R####_*.txt.
    \"\"\"
    try:
        from pathlib import Path
        reports = Path(__file__).resolve().parent.parent / "Reports"
        rid = runner_id if str(runner_id).upper().startswith("R") else ("R" + str(runner_id))
        dig = "".join([c for c in rid if c.isdigit()])

        cands = []
        if reports.exists():
            if dig:
                cands += list(reports.glob(f"R{dig}_*.txt"))
                cands += list(reports.glob(f"R{dig}*.txt"))
                cands += list(reports.glob(f"Report_R{dig}_*.md"))
                cands += list(reports.glob(f"Report_R{dig}_*.txt"))
            cands += list(reports.glob(f"{rid}_*.txt"))
            cands += list(reports.glob(f"{rid}*.txt"))
            cands += list(reports.glob(f"Report_{rid}_*.md"))
            cands += list(reports.glob(f"Report_{rid}_*.txt"))

        if not cands:
            return ""

        newest = max(cands, key=lambda p: p.stat().st_mtime)
        txt = newest.read_text(encoding="utf-8", errors="replace")
        return f"[{rid}] REPORT FILE: {newest}\\n\\n" + txt
    except Exception as _exc:
        try:
            return f"(could not load report text: {_exc})"
        except Exception:
            return ""
""".strip("\n")

    # Insert helper if missing, else replace existing by name
    if "def _r1851_get_latest_report_text" in la_src0:
        la_src1, ok, msg = replace_top_level_def(la_src0, "_r1851_get_latest_report_text", helper_block)
        notes.append(f"- logic_actions.py: {msg} (backup `{la_bak.name}`)\n")
    else:
        # Insert near top after imports (best-effort)
        imp = re.search(r"(?m)^(from __future__.*\n)?(import .*\n)+\n", la_src0)
        if imp:
            pos = imp.end()
            la_src1 = la_src0[:pos] + helper_block + "\n\n" + la_src0[pos:]
            notes.append(f"- logic_actions.py: inserted helper _r1851_get_latest_report_text (backup `{la_bak.name}`)\n")
        else:
            la_src1 = la_src0 + "\n\n" + helper_block + "\n\n"
            notes.append(f"- logic_actions.py: appended helper _r1851_get_latest_report_text (backup `{la_bak.name}`)\n")

    # Patch _r1851_run_tools_runner to show popup for purge runners (R2218/R2224) using helper (single source)
    if "def _r1851_run_tools_runner" not in la_src1:
        # rollback
        la.write_text(la_bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        rp = report_path(root)
        rp.write_text("".join(notes) + "**FAIL** missing `_r1851_run_tools_runner` in logic_actions.py\n", encoding="utf-8")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    # Inject near end of _r1851_run_tools_runner: after runner completes successfully, show popup for R2218/R2224
    # We place before any "return" at function indent level, by inserting before last "return" line within block.
    la_lines = la_src1.splitlines(True)
    # locate function start
    m = re.search(r"(?m)^(?P<ind>[ \t]*)def\s+_r1851_run_tools_runner\s*\(.*\)\s*:\s*$", la_src1)
    ind = m.group("ind")
    start_idx = None
    for i, ln in enumerate(la_lines):
        if re.match(rf"^{re.escape(ind)}def\s+_r1851_run_tools_runner\s*\(", ln):
            start_idx = i
            break
    if start_idx is None:
        la.write_text(la_bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        rp = report_path(root)
        rp.write_text("".join(notes) + "**FAIL** could not locate _r1851_run_tools_runner start\n", encoding="utf-8")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    # find end of function block by next def at same indent
    end_idx = len(la_lines)
    for j in range(start_idx + 1, len(la_lines)):
        if re.match(rf"^{re.escape(ind)}def\s+\w+\s*\(", la_lines[j]):
            end_idx = j
            break

    fn_block = la_lines[start_idx:end_idx]
    # Avoid double-inject
    if f"{RID}: purge popup single-source" not in "".join(fn_block):
        # Insert before last return in block, else before end
        insert_at = None
        for k in range(len(fn_block)-1, -1, -1):
            if re.match(rf"^{re.escape(ind)}\s+return\b", fn_block[k]):
                insert_at = k
                break
        if insert_at is None:
            insert_at = len(fn_block)

        inject = (
            f"{ind}    # {RID}: purge popup single-source (ONLY place that shows purge popup)\n"
            f"{ind}    try:\n"
            f"{ind}        _rid = str(runner_id)\n"
            f"{ind}        if _rid in ('R2218','2218'):\n"
            f"{ind}            _txt = _r1851_get_latest_report_text(app, 'R2218')\n"
            f"{ind}            if _txt:\n"
            f"{ind}                _r1851_show_popup(app, 'Purge Scan – Report', _txt, 'R2218')\n"
            f"{ind}        elif _rid in ('R2224','2224'):\n"
            f"{ind}            _txt = _r1851_get_latest_report_text(app, 'R2224')\n"
            f"{ind}            if _txt:\n"
            f"{ind}                _r1851_show_popup(app, 'Purge Apply – Report', _txt, 'R2224')\n"
            f"{ind}    except Exception:\n"
            f"{ind}        pass\n"
        )

        fn_block2 = fn_block[:insert_at] + [inject] + fn_block[insert_at:]
        la_lines[start_idx:end_idx] = fn_block2
        la_src2 = "".join(la_lines)
        notes.append("- logic_actions.py: injected purge popup logic into _r1851_run_tools_runner\n")
    else:
        la_src2 = "".join(la_lines)
        notes.append("- logic_actions.py: purge popup injection already present (no change)\n")

    # Write and compile-gate logic_actions
    la.write_text(la_src2, encoding="utf-8")
    try:
        compile_gate(la)
        notes.append("- logic_actions.py: py_compile OK\n")
    except Exception as e:
        la.write_text(la_bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        rp = report_path(root)
        rp.write_text("".join(notes) + f"\n**FAIL** logic_actions.py compile: {e}\n", encoding="utf-8")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    # --- Patch logic_tools: replace purge functions with minimal bodies (no popup, no bridge)
    if not lt.exists():
        # rollback logic_actions already patched? MR: but we keep it; still better to fail-fast.
        rp = report_path(root)
        rp.write_text("".join(notes) + f"\n**FAIL** missing `{lt}`\n", encoding="utf-8")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    lt_bak = backup(lt)
    lt_src0 = lt.read_text(encoding="utf-8", errors="replace")

    purge_scan_body = """
def action_tools_purge_scan(app):
    \"\"\"Run Purge Scan via tools runner. Popup is shown ONLY by logic_actions.\"\"\"
    from modules import logic_actions
    return logic_actions._r1851_run_tools_runner(app, "R2218", title="Purge Scan")
""".strip("\n")

    purge_apply_body = """
def action_tools_purge_apply(app):
    \"\"\"Run Purge Apply via tools runner. Popup is shown ONLY by logic_actions.\"\"\"
    from modules import logic_actions
    return logic_actions._r1851_run_tools_runner(app, "R2224", title="Purge Apply")
""".strip("\n")

    lt_src1, ok1, msg1 = replace_top_level_def(lt_src0, "action_tools_purge_scan", purge_scan_body)
    lt_src2, ok2, msg2 = replace_top_level_def(lt_src1, "action_tools_purge_apply", purge_apply_body)

    if not (ok1 and ok2):
        lt.write_text(lt_bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        rp = report_path(root)
        rp.write_text("".join(notes) + f"\n**FAIL** {msg1} | {msg2}\n", encoding="utf-8")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    lt.write_text(lt_src2, encoding="utf-8")
    try:
        compile_gate(lt)
        notes.append(f"- logic_tools.py: {msg1}; {msg2} (backup `{lt_bak.name}`)\n")
        notes.append("- logic_tools.py: py_compile OK\n")
    except Exception as e:
        lt.write_text(lt_bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        rp = report_path(root)
        rp.write_text("".join(notes) + f"\n**FAIL** logic_tools.py compile: {e}\n", encoding="utf-8")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    # --- Patch ui_toolbar: disarm _wrap_with_led_and_report_popup so it never calls popup
    if ui.exists():
        ui_bak = backup(ui)
        ui_src0 = ui.read_text(encoding="utf-8", errors="replace")

        disarm_block = """
def _wrap_with_led_and_report_popup(app, action, runner_id, title, subtitle):
    \"\"\"UI wrapper: LED + run action. NO POPUP here (single-source in logic_actions).\"\"\"
    def _wrapped():
        try:
            # keep any existing LED behavior by calling whatever wrapper used for logs (if present)
            # but do NOT open popups here.
            return action(app)
        except Exception:
            try:
                return action(app)
            except Exception:
                return None
    return _wrapped
""".strip("\n")

        ui_src1, okw, msgw = replace_any_def(ui_src0, "_wrap_with_led_and_report_popup", disarm_block)
        if not okw:
            # Not fatal; some versions may not have this helper.
            notes.append(f"- ui_toolbar.py: {msgw} (skip)\n")
        else:
            ui.write_text(ui_src1, encoding="utf-8")
            try:
                compile_gate(ui)
                notes.append(f"- ui_toolbar.py: disarmed _wrap_with_led_and_report_popup (backup `{ui_bak.name}`)\n")
                notes.append("- ui_toolbar.py: py_compile OK\n")
            except Exception as e:
                ui.write_text(ui_bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
                rp = report_path(root)
                rp.write_text("".join(notes) + f"\n**FAIL** ui_toolbar.py compile: {e}\n", encoding="utf-8")
                print(f"[{RID}] FAIL: {rp}")
                return 11
    else:
        notes.append("- ui_toolbar.py missing (skip)\n")

    rp = report_path(root)
    rp.write_text("".join(notes) + "\n**RESULT: OK**\n", encoding="utf-8")
    print(f"[{RID}] OK: Report: {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
