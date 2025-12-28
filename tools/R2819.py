import sys
import py_compile
from pathlib import Path
from datetime import datetime

RID="R2819"

def ts(): return datetime.now().strftime("%Y%m%d_%H%M%S")

def report(root: Path, txt: str) -> Path:
    d = root/"Reports"
    d.mkdir(exist_ok=True)
    rp = d/f"Report_{RID}_{ts()}.md"
    rp.write_text(txt, encoding="utf-8")
    return rp

def backup(p: Path) -> Path:
    bak = p.with_suffix(p.suffix + f".{RID}_{ts()}.bak")
    bak.write_text(p.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    return bak

def compile_gate(p: Path):
    py_compile.compile(str(p), doraise=True)

def main():
    root = Path(sys.argv[1]).resolve()
    ui = root/"modules"/"ui_toolbar.py"
    notes = [f"# {RID} – Fix push gating repo-root resolution\n\n", f"Target: `{ui}`\n\n"]

    if not ui.exists():
        rp = report(root, "".join(notes) + "**FAIL** ui_toolbar.py missing\n")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    bak = backup(ui)
    notes.append(f"- Backup: `{bak.name}`\n")

    src = ui.read_text(encoding="utf-8", errors="replace")

    needle = "base = os.getcwd()"
    if needle not in src:
        ui.write_text(bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        rp = report(root, "".join(notes) + f"**FAIL** pattern not found: `{needle}`\n")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    repl = (
        "base = os.getcwd()\n"
        "            # R2819: deterministic repo root (don't trust cwd)\n"
        "            try:\n"
        "                _this_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))\n"
        "            except Exception:\n"
        "                _this_root = \"\"\n"
    )
    src = src.replace(needle, repl, 1)
    notes.append("- Injected deterministic _this_root fallback\n")

    # Ensure _this_root is actually used as candidate (private + public)
    # Insert right after candidates list creation (first occurrence).
    needle2 = "candidates: list[str] = []"
    if needle2 in src:
        src = src.replace(
            needle2,
            needle2 + "\n            if _this_root:\n                candidates.append(_this_root)\n",
            1
        )
        notes.append("- Added _this_root to candidates\n")
    else:
        notes.append("- WARNING: candidates list marker not found (no candidate injection)\n")

    ui.write_text(src, encoding="utf-8")

    try:
        compile_gate(ui)
        notes.append("- py_compile: OK\n")
    except Exception as e:
        ui.write_text(bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        rp = report(root, "".join(notes) + f"\n**FAIL** compile: {e}\nRollback: `{bak.name}`\n")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    rp = report(root, "".join(notes) + "\n**RESULT: OK**\n")
    print(f"[{RID}] OK: Report: {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
