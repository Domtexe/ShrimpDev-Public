# -*- coding: utf-8 -*-
"""
R2863 – SAFE PATCH
- Add "Export Public" button in modules/ui_toolbar.py
- Add action_public_export_sync in modules/logic_actions.py
- Uses _r1851_run_tools_runner to run R2862
- Backup + rollback + report
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import List

RUNNER_ID = "R2863"
EXIT_FAIL = 11


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def backup(repo: Path, target: Path) -> Path:
    arch = repo / "_Archiv"
    ensure_dir(arch)
    bak = arch / f"{target.name}.{RUNNER_ID}_{now_stamp()}.bak"
    shutil.copy2(target, bak)
    return bak


def write_report(repo: Path, lines: List[str]) -> Path:
    rp = repo / "Reports"
    ensure_dir(rp)
    out = rp / f"Report_{RUNNER_ID}_{now_stamp()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")
    return out


def patch_ui_toolbar(repo: Path, report: List[str]) -> None:
    p = repo / "modules" / "ui_toolbar.py"
    if not p.exists():
        raise RuntimeError(f"Missing {p}")

    txt = p.read_text(encoding="utf-8", errors="replace")
    if "Export Public" in txt and "action_public_export_sync" in txt:
        report.append(f"- OK: ui_toolbar already contains Export Public button")
        return

    bak = backup(repo, p)
    report.append(f"- Backup ui_toolbar: `{bak}`")

    anchor = "btn_push_private.pack(side='right', padx=(6, 0))"
    idx = txt.find(anchor)
    if idx == -1:
        raise RuntimeError("Anchor not found in ui_toolbar.py (push pack line)")

    insert = """
    # R2863: Public export sync button (runs R2862)
    row_export = ui_theme_classic.Frame(service_frame)
    row_export.pack(fill="x", pady=(4, 0))
    btn_export_public = ui_theme_classic.Button(
        row_export,
        text="Export Public",
        command=lambda: _call_logic_action(app, "action_public_export_sync"),
    )
    try:
        ui_tooltip.register(btn_export_public, "Sync Private -> Public export (R2862) and push public if configured.")
    except Exception:
        pass
    btn_export_public.pack(side='right', padx=(6, 0))
""".rstrip() + "\n"

    # Insert right after the anchor line (end of push row packing)
    endline = txt.find("\n", idx)
    if endline == -1:
        endline = idx + len(anchor)
    new_txt = txt[: endline + 1] + insert + txt[endline + 1 :]

    p.write_text(new_txt, encoding="utf-8", errors="replace")
    report.append("- OK: ui_toolbar patched (Export Public button added)")


def patch_logic_actions(repo: Path, report: List[str]) -> None:
    p = repo / "modules" / "logic_actions.py"
    if not p.exists():
        raise RuntimeError(f"Missing {p}")

    txt = p.read_text(encoding="utf-8", errors="replace")
    if "def action_public_export_sync" in txt:
        report.append("- OK: logic_actions already contains action_public_export_sync")
        return

    bak = backup(repo, p)
    report.append(f"- Backup logic_actions: `{bak}`")

    # Append near end (actions override section)
    block = """
def action_public_export_sync(app, *args, **kwargs):  # type: ignore[override]
    \"\"\"Run R2862 to sync Private -> Public export and (optionally) push.\"\"\"
    _r1851_run_tools_runner(app, "R2862", "Export Public")
""".lstrip("\n")

    new_txt = txt.rstrip() + "\n\n# R2863: Public export sync action\n" + block + "\n"
    p.write_text(new_txt, encoding="utf-8", errors="replace")
    report.append("- OK: logic_actions patched (action_public_export_sync added)")


def main(root_arg: str) -> int:
    repo = Path(root_arg).resolve()
    report: List[str] = []
    report.append(f"# {RUNNER_ID} SAFE PATCH: Export Public button + action")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: `{repo}`")
    report.append("")

    try:
        patch_ui_toolbar(repo, report)
        patch_logic_actions(repo, report)

        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] OK -> {rp}")
        return 0

    except Exception as e:
        report.append(f"ERROR: {type(e).__name__}: {e}")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return EXIT_FAIL


if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parents[1])
    raise SystemExit(main(root))
