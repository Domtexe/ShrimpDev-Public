# R2872.py - PATCH (SAFE): Fix ui_toolbar runtime NameErrors (frame_toolbar_right / busy / name in trace)
# Root: ShrimpDev_REPO
# Strategy:
#  - Backup target file
#  - Apply conservative regex-based edits (works across minor variations)
#  - Compile-check patched module + main_gui.py
#  - Roll back on failure
#
# Notes:
#  - This runner intentionally avoids "full rewrites" and only patches narrowly-scoped lines.
#  - It removes/neutralizes debug f-strings that reference undefined identifiers (busy/name).
#  - It also replaces accidental 'frame_toolbar_right' references with the actual function arg (commonly 'parent').

from __future__ import annotations

import sys
import re
import shutil
from pathlib import Path
from datetime import datetime

RUNNER_ID = "R2872"


def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def write_text(p: Path, s: str) -> None:
    p.write_text(s, encoding="utf-8", newline="\n")


def backup_file(root: Path, target: Path) -> Path:
    bdir = root / "_Backups" / RUNNER_ID
    bdir.mkdir(parents=True, exist_ok=True)
    bpath = bdir / f"{target.name}.{RUNNER_ID}_{ts()}.bak"
    shutil.copy2(target, bpath)
    return bpath


def compile_check(paths: list[Path]) -> tuple[bool, str]:
    import py_compile

    out = []
    try:
        for p in paths:
            py_compile.compile(str(p), doraise=True)
            out.append(f"OK compile: {p}")
        return True, "\n".join(out)
    except Exception as e:
        return False, f"FAIL compile: {e!r}"


def patch_ui_toolbar(src: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    s = src

    # 1) Replace accidental Frame(frame_toolbar_right) with Frame(parent)
    #    (common slip inside build_toolbar_right(parent, app))
    before = s
    s = re.sub(r"\bFrame\(\s*frame_toolbar_right\s*\)", "Frame(parent)", s)
    if s != before:
        notes.append("Replaced Frame(frame_toolbar_right) -> Frame(parent)")

    # 2) Neutralize debug trace f-strings that reference undefined identifiers (busy/name).
    #    We conservatively rewrite ONLY lines containing _r2836_trace( ...set_btn_state... )
    #    to a constant string (keeps logging without NameError).
    def _fix_trace_line(m: re.Match) -> str:
        notes.append("Neutralized _r2836_trace set_btn_state line to avoid undefined identifiers")
        indent = m.group("indent") or ""
        return indent + "_r2836_trace('set_btn_state')"

    before = s
    s = re.sub(
        r"(?m)^(?P<indent>\s*)_r2836_trace\(\s*f?['\"]\s*set_btn_state[^'\"]*['\"]\s*\)\s*$",
        _fix_trace_line,
        s,
    )
    if s != before:
        # note already appended in callback
        pass

    # 3) If there are any other _r2836_trace f-strings that include {busy} or {name} literals,
    #    strip those interpolations to safe repr via concatenation.
    #    Example: _r2836_trace(f"... busy={busy}") -> _r2836_trace("... busy=" + str(busy))
    #    We do this only when the f-string contains "{busy}" or "{name}".
    def _rewrite_fstring(expr: str, var: str) -> str:
        # Replace "...{var}..." with '"+ str(var) +"' style inside the f-string content.
        # We'll just remove the interpolation entirely if it's messy.
        return expr.replace("{" + var + "}", f'"+str({var})+"')

    # This is intentionally conservative: if we detect f"...{busy}..." we replace with a safe plain string.
    before = s
    s = re.sub(
        r"(?m)^(?P<indent>\s*)_r2836_trace\(\s*f(['\"])(?P<body>.*?\{(?:busy|name)\}.*)\2\s*\)\s*$",
        lambda m: (m.group("indent") or "") + "_r2836_trace('trace')",
        s,
    )
    if s != before:
        notes.append("Neutralized _r2836_trace f-strings containing {busy}/{name} to avoid NameError")

    return s, notes


def main(root: Path) -> int:
    root = root.resolve()
    target = root / "modules" / "ui_toolbar.py"
    if not target.exists():
        print(f"[{RUNNER_ID}] ERROR: target not found: {target}")
        return 11

    original = read_text(target)
    patched, notes = patch_ui_toolbar(original)

    if patched == original:
        print(f"[{RUNNER_ID}] NOTE: No changes needed in {target}")
        return 0

    bpath = backup_file(root, target)
    write_text(target, patched)

    ok, det = compile_check([target, root / "main_gui.py"])
    if not ok:
        # rollback
        write_text(target, original)
        print(f"[{RUNNER_ID}] FAIL compile -> rolled back. Backup: {bpath}")
        print(det)
        return 11

    print(f"[{RUNNER_ID}] OK patched: {target}")
    print(f"[{RUNNER_ID}] Backup: {bpath}")
    for n in notes:
        print(f"[{RUNNER_ID}] - {n}")
    return 0


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    raise SystemExit(main(root))
