from __future__ import annotations

import py_compile
import shutil
from datetime import datetime
from pathlib import Path


RID = "R2448"


def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def now_human() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def write_text(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8", newline="\n")


def backup_file(src: Path, archiv_dir: Path) -> Path:
    archiv_dir.mkdir(parents=True, exist_ok=True)
    b = archiv_dir / f"{src.name}.{RID}_{ts()}.bak"
    shutil.copy2(src, b)
    return b


def try_compile(pyfile: Path) -> tuple[bool, str]:
    try:
        py_compile.compile(str(pyfile), doraise=True)
        return True, ""
    except Exception as e:
        return False, repr(e)


def patch_ui_toolbar(s: str) -> tuple[str, list[str], bool]:
    """
    Minimal-invasive Patch:
    1) Make Purge buttons disabled when:
       - app is busy (runner running)
       - APPLY: also requires docs/Tools_Purge_Flat_Plan.md exists and non-empty
    2) Align top-right padding: make rightmost padding flush (no extra right gap)
       - row0 (purge): btn_apply padx=(6,0) so it sits on the right edge.
    """
    notes: list[str] = []
    changed = False

    # --- 1) Purge button state mgmt (inject into existing _update_push_states)
    # We hook into the already-running timer function to avoid new timers / complexity.

    marker = "def _update_push_states():"
    if marker not in s:
        notes.append("ERROR: _update_push_states() not found.")
        return s, notes, False

    # Add plan existence helper + button refs used inside _update_push_states
    # We look for where btn_scan and btn_apply are created (row0) and then ensure
    # we apply state in _update_push_states with safe guards.

    # Ensure purge plan helper exists (small, local, safe).
    helper_snip = """
    def _purge_plan_ok() -> bool:
        try:
            # Plan created by Tools Purge Scan
            p = Path(getattr(app, "project_root", "")) / "docs" / "Tools_Purge_Flat_Plan.md"
            if not p.exists():
                return False
            try:
                txt = p.read_text(encoding="utf-8", errors="replace").strip()
            except Exception:
                return True  # exists -> assume ok
            return len(txt) > 0
        except Exception:
            return False
""".strip("\n")

    # Insert helper right before _update_push_states (only once)
    if helper_snip not in s:
        idx = s.find(marker)
        s = s[:idx] + helper_snip + "\n\n" + s[idx:]
        notes.append("OK: added _purge_plan_ok() helper")
        changed = True
    else:
        notes.append("OK: _purge_plan_ok() already present")

    # Inject purge enable logic into _update_push_states()
    inject_line = "        # Purge buttons state (Scan/Apply)\n"
    if inject_line not in s:
        # Find inside _update_push_states after busy computed
        needle = "        busy = _runner_busy()"
        pos = s.find(needle)
        if pos == -1:
            notes.append("ERROR: busy line not found in _update_push_states.")
            return s, notes, changed

        # Find next line break after busy line
        after = s.find("\n", pos)
        if after == -1:
            notes.append("ERROR: cannot locate newline after busy line.")
            return s, notes, changed

        block = """
        # Purge buttons state (Scan/Apply)
        try:
            purge_scan_ok = (not busy)
            purge_apply_ok = (not busy) and _purge_plan_ok()
            _set_btn_state(btn_scan, purge_scan_ok)
            _set_btn_state(btn_apply, purge_apply_ok)
        except Exception:
            pass
""".strip("\n")

        s = s[: after + 1] + block + "\n" + s[after + 1 :]
        notes.append("OK: injected purge state logic into _update_push_states()")
        changed = True
    else:
        notes.append("OK: purge state logic already present")

    # --- 2) Right-edge padding fix for purge apply button
    # We change: btn_apply.pack(side="right", padx=6, pady=0)
    # to:        btn_apply.pack(side="right", padx=(6, 0), pady=0)

    old = 'btn_apply.pack(side="right", padx=6, pady=0)'
    new = 'btn_apply.pack(side="right", padx=(6, 0), pady=0)'
    if old in s:
        s = s.replace(old, new)
        notes.append("OK: btn_apply right-edge padding set to padx=(6,0)")
        changed = True
    else:
        notes.append("NOTE: btn_apply pack line not found (maybe already adjusted).")

    # Also keep scan spacing consistent (optional, safe)
    old2 = 'btn_scan.pack(side="right", padx=6, pady=0)'
    new2 = 'btn_scan.pack(side="right", padx=(6, 0), pady=0)'
    if old2 in s:
        s = s.replace(old2, new2)
        notes.append("OK: btn_scan padding set to padx=(6,0)")
        changed = True
    else:
        notes.append("NOTE: btn_scan pack line not found (maybe already adjusted).")

    return s, notes, changed


def patch_pipeline(pipeline_path: Path, add_line: str) -> tuple[bool, str]:
    if not pipeline_path.exists():
        return False, "PIPELINE.md not found; skipped."

    txt = read_text(pipeline_path)
    stamp = now_human()
    entry = f"- [{stamp}] {add_line}\n"

    if entry.strip() in txt:
        return False, "Pipeline entry already present; skipped."

    # Append near end (minimal risk)
    write_text(pipeline_path, txt.rstrip() + "\n\n" + "## UI Tasks (Auto)\n" + entry)
    return True, "Pipeline updated (appended)."


def main() -> int:
    root = Path.cwd()
    ui = root / "modules" / "ui_toolbar.py"
    docs = root / "docs"
    report = docs / f"Report_{RID}_PurgeStateAndAlign_{ts()}.md"
    archiv = root / "_Archiv"
    pipeline = docs / "PIPELINE.md"

    if not ui.exists():
        write_text(report, f"# {RID} ERROR\n\nui_toolbar.py not found: {ui}\n")
        return 2

    before_backup = backup_file(ui, archiv)
    original = read_text(ui)

    patched, notes, changed = patch_ui_toolbar(original)

    # Write report draft
    lines = []
    lines.append(f"# {RID} UI: Purge state + top-right alignment\n")
    lines.append(f"- Time: {now_human()}")
    lines.append(f"- Root: `{root}`")
    lines.append(f"- File: `{ui}`\n")
    lines.append("## Actions\n")
    lines.extend([f"- {n}" for n in notes])
    lines.append("")
    lines.append(f"- Backup: `{before_backup}`\n")

    if not changed:
        lines.append("## Result\n- NO-OP (no changes needed or patterns not found)\n")
        write_text(report, "\n".join(lines))
        return 0

    write_text(ui, patched)

    ok, err = try_compile(ui)
    if not ok:
        # rollback
        write_text(ui, original)
        ok2, err2 = try_compile(ui)
        lines.append("## Compile\n")
        lines.append(f"- ERROR: compile failed after patch: `{err}`")
        lines.append("- Rolled back to original.")
        lines.append(f"- Compile after rollback: {'OK' if ok2 else 'ERROR'} `{err2}`\n")
        write_text(report, "\n".join(lines))
        return 5

    # pipeline update
    pip_ok, pip_msg = patch_pipeline(
        pipeline,
        "Intake: Purge Scan/Apply buttons disabled when busy; Apply requires Tools_Purge_Flat_Plan.md; top-right purge padding flush.",
    )
    lines.append("## Compile\n- OK\n")
    lines.append("## Pipeline\n")
    lines.append(f"- {pip_msg}\n")

    write_text(report, "\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
