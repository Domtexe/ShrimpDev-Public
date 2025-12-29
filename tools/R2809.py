import sys
import glob
import py_compile
from pathlib import Path
from datetime import datetime

RID = "R2809"

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

def newest_any_backup(path: Path) -> Path | None:
    # pick newest backup of any RID: ui_toolbar.py.*.bak
    pat = str(path) + ".*.bak"
    cands = sorted(glob.glob(pat))
    if not cands:
        return None
    # newest by filename sort (timestamps in name), good enough
    return Path(cands[-1])

def neutralize_popup_lines(lines: list[str]) -> tuple[list[str], int]:
    """Replace popup call lines with 'pass', keeping indentation."""
    out = []
    n = 0
    for ln in lines:
        if "_r1851_show_popup" in ln:
            indent = ln[:len(ln) - len(ln.lstrip(" \t"))]
            out.append(f"{indent}pass  # {RID}: popup suppressed here\n")
            n += 1
        else:
            out.append(ln)
    return out, n

def fix_empty_try_blocks(lines: list[str]) -> tuple[list[str], int]:
    """
    If a 'try:' line is followed (ignoring blank/comment lines) immediately by an 'except' or 'finally'
    at SAME indentation, insert an indented 'pass' to satisfy Python syntax.
    """
    def indent_of(s: str) -> str:
        return s[:len(s) - len(s.lstrip(" \t"))]

    out = []
    i = 0
    fixes = 0
    n = len(lines)

    while i < n:
        ln = lines[i]
        out.append(ln)

        if ln.strip() == "try:":
            base_ind = indent_of(ln)

            j = i + 1
            # walk over blank lines and pure comments at deeper indent or same indent
            while j < n:
                nxt = lines[j]
                st = nxt.strip()
                if st == "":
                    j += 1
                    continue
                # allow comments (at any indent) to be skipped
                if st.startswith("#"):
                    j += 1
                    continue
                break

            if j < n:
                nxt = lines[j]
                nxt_ind = indent_of(nxt)
                st = nxt.strip()
                if nxt_ind == base_ind and (st.startswith("except") or st.startswith("finally")):
                    # empty try block -> insert pass at one indent deeper
                    out.append(base_ind + "    " + f"pass  # {RID}: inserted to fix empty try\n")
                    fixes += 1

        i += 1

    return out, fixes

def main():
    if len(sys.argv) < 2:
        return 11

    root = Path(sys.argv[1]).resolve()
    ui = root / "modules" / "ui_toolbar.py"
    notes = []
    notes.append(f"# {RID} – HOTFIX ui_toolbar.py empty-try repair + popup suppression\n\n")
    notes.append(f"Root: `{root}`\n\n")
    notes.append(f"Target: `{ui}`\n\n")

    if not ui.exists():
        rp = write_report(root, "".join(notes) + "**FAIL** ui_toolbar.py missing\n")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    # 1) Optional restore from any backup (helps if current file is already mangled)
    bak = newest_any_backup(ui)
    if bak and bak.exists():
        ui.write_text(bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        notes.append(f"- Restored from backup: `{bak.name}`\n")
    else:
        notes.append("- No backup found; patching current file\n")

    # 2) Patch in-memory
    lines = ui.read_text(encoding="utf-8", errors="replace").splitlines(True)

    lines, n_pop = neutralize_popup_lines(lines)
    notes.append(f"- Popup lines neutralized: {n_pop}\n")

    lines, n_try = fix_empty_try_blocks(lines)
    notes.append(f"- Empty try blocks fixed: {n_try}\n")

    ui.write_text("".join(lines), encoding="utf-8")

    # 3) Compile gate
    try:
        compile_gate(ui)
        notes.append("- py_compile: OK\n")
    except Exception as e:
        # If we restored from a backup, roll back to it to avoid leaving broken file
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
