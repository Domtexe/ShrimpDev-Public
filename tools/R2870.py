# R2870 - PATCH (SAFE): Fix NameError 'busy' in modules/ui_toolbar.py
# - Adds optional busy parameter to _set_btn_state
# - Passes busy from _update_push_states for push buttons
# - Keeps other call sites unchanged
# - Backup + compile check + rollback on failure
from __future__ import annotations

import re
import shutil
from pathlib import Path
from datetime import datetime


def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def write_report(report_path: Path, lines: list[str]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def py_compile(path: Path) -> tuple[bool, str]:
    import py_compile
    try:
        py_compile.compile(str(path), doraise=True)
        return True, "py_compile OK"
    except Exception as e:
        return False, f"py_compile FAIL: {e!r}"


def main(root: Path) -> int:
    target = root / "modules" / "ui_toolbar.py"
    reports = root / "Reports"

    report = reports / f"Report_R2870_{ts()}.md"
    rep: list[str] = [
        "# R2870 PATCH (SAFE): Fix NameError busy in ui_toolbar",
        "",
        f"Root: `{root}`",
        f"Target: `{target}`",
        "",
    ]

    if not target.exists():
        rep += ["## ERROR", f"- Target not found: `{target}`"]
        write_report(report, rep)
        return 11

    backup = target.with_suffix(target.suffix + f".R2870_{ts()}.bak")
    shutil.copy2(target, backup)
    rep += ["## Backup", f"- `{backup.name}` created."]

    original = target.read_text(encoding="utf-8", errors="replace")
    text = original

    # 1) Expand _set_btn_state signature to accept optional busy
    # from: def _set_btn_state(btn, enabled: bool):
    # to:   def _set_btn_state(btn, enabled: bool, busy: bool | None = None):
    text, n1 = re.subn(
        r"^(\s*)def\s+_set_btn_state\s*\(\s*btn\s*,\s*enabled\s*:\s*bool\s*\)\s*:\s*$",
        r"\1def _set_btn_state(btn, enabled: bool, busy: bool | None = None):",
        text,
        flags=re.M,
    )

    # 2) Make trace line not reference busy unless provided
    # from: _r2836_trace(f"set_btn_state enabled={enabled} busy={busy}")
    # to:   _r2836_trace(f"set_btn_state enabled={enabled}" + (f" busy={busy}" if busy is not None else ""))
    text, n2 = re.subn(
        r'_r2836_trace\(\s*f"set_btn_state enabled=\{enabled\}\s+busy=\{busy\}"\s*\)',
        r'_r2836_trace(f"set_btn_state enabled={enabled}" + (f" busy={busy}" if busy is not None else ""))',
        text,
        flags=re.M,
    )

    # 3) Pass busy from _update_push_states only for push buttons
    # _set_btn_state(btn_push_private, (not busy) and private_pushable)
    # -> _set_btn_state(btn_push_private, (not busy) and private_pushable, busy=busy)
    text, n3 = re.subn(
        r"_set_btn_state\(\s*btn_push_private\s*,\s*\(not busy\)\s*and\s*private_pushable\s*\)",
        r"_set_btn_state(btn_push_private, (not busy) and private_pushable, busy=busy)",
        text,
    )
    text, n4 = re.subn(
        r"_set_btn_state\(\s*btn_push_public\s*,\s*\(not busy\)\s*and\s*public_pushable\s*\)",
        r"_set_btn_state(btn_push_public, (not busy) and public_pushable, busy=busy)",
        text,
    )

    rep += [
        "",
        "## Patch summary",
        f"- Signature updated: {n1} hit(s)",
        f"- Trace line updated: {n2} hit(s)",
        f"- Push private call updated: {n3} hit(s)",
        f"- Push public call updated: {n4} hit(s)",
    ]

    if text == original:
        rep += ["", "## NOTE", "- No changes applied (patterns not found)."]
        write_report(report, rep)
        return 11

    target.write_text(text, encoding="utf-8")

    ok, msg = py_compile(target)
    rep += ["", "## Compile check", f"- {msg}"]

    if not ok:
        # rollback
        target.write_text(original, encoding="utf-8")
        rep += ["", "## ROLLBACK", f"- Restored original from in-memory copy. Backup remains: `{backup.name}`"]
        write_report(report, rep)
        return 11

    rep += ["", "## OK", "- Patch applied successfully."]
    write_report(report, rep)
    return 0


if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parents[1]
    raise SystemExit(main(root_dir))
