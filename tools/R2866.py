from __future__ import annotations

import datetime as _dt
from pathlib import Path
import shutil
import sys

RULE_MARKER = "MR-DEBUG-LOGGING-NO-NEW-VARS"


def _ts() -> str:
    return _dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def _write_report(report_path: Path, lines: list[str]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")


def _backup_file(p: Path, backups_dir: Path) -> Path:
    backups_dir.mkdir(parents=True, exist_ok=True)
    bak = backups_dir / f"{p.name}.bak_{_ts()}"
    shutil.copy2(p, bak)
    return bak


def _patch_append_once(md_path: Path, block: str) -> tuple[bool, str]:
    txt = md_path.read_text(encoding="utf-8", errors="replace")
    if RULE_MARKER in txt:
        return False, f"Skip: Marker already present in {md_path.as_posix()}"
    # Append at end with clear separator
    new_txt = txt.rstrip() + "\n\n---\n\n" + block.rstrip() + "\n"
    md_path.write_text(new_txt, encoding="utf-8", errors="replace")
    return True, f"Patched: appended block to {md_path.as_posix()}"


def main(root: Path) -> int:
    tools_dir = root / "tools"
    reports_dir = root / "Reports"
    backups_dir = root / "_Backups" / "R2866"

    tech = root / "docs" / "Master" / "MasterRules_Tech.md"
    syn = root / "docs" / "Master" / "MasterRules_Syntax.md"

    report = [
        f"# Report R2866 — MasterRules PATCH",
        f"- Time: {_dt.datetime.now().isoformat(timespec='seconds')}",
        f"- Root: `{root.as_posix()}`",
        "",
        "## Target files",
        f"- `{tech.as_posix()}`",
        f"- `{syn.as_posix()}`",
        "",
    ]

    if not tech.exists():
        report.append(f"ERROR: MasterRules_Tech.md not found at: {tech.as_posix()}")
        _write_report(reports_dir / f"Report_R2866_{_ts()}.md", report)
        return 11
    if not syn.exists():
        report.append(f"ERROR: MasterRules_Syntax.md not found at: {syn.as_posix()}")
        _write_report(reports_dir / f"Report_R2866_{_ts()}.md", report)
        return 11

    # Backup
    backups: list[Path] = []
    try:
        backups.append(_backup_file(tech, backups_dir))
        backups.append(_backup_file(syn, backups_dir))

        block = (
            f"## Logging & Debugging\n\n"
            f"### Debug-Logging darf keine neuen Variablen einführen  <!-- {RULE_MARKER} -->\n\n"
            f"- **Regel:** Debug-/Trace-Logging darf **keine** Variablen referenzieren, die in der aktuellen "
            f"Funktion **nicht existieren** (kein \"mal schnell\" `name`, `busy`, etc.).\n"
            f"- **Erlaubt:** Nur **Parameter**, **lokal definierte Variablen** (im selben Scope) oder **sichere Literale**.\n"
            f"- **No-Go:** Logging, das neue Namen erfindet → kann in Tk-Callbacks Runtime-crashen (z. B. `NameError`).\n"
            f"- **Enforcement:** CI Syntax Gate / Smoke Test + Lint-Guard (heuristisch) für f-Strings in Funktionen.\n"
        )

        changed_tech, note_tech = _patch_append_once(tech, block)

        # Minimaler Querverweis im Syntax-Dokument (nur wenn nicht schon vorhanden)
        syn_txt = syn.read_text(encoding="utf-8", errors="replace")
        if RULE_MARKER in syn_txt:
            changed_syn = False
            note_syn = "Skip: Marker already present in MasterRules_Syntax.md"
        else:
            add = (
                "\n\n- **Logging/Debug:** siehe Regel in `MasterRules_Tech.md` "
                f"(Marker: `{RULE_MARKER}`).\n"
            )
            syn.write_text(syn_txt.rstrip() + add, encoding="utf-8", errors="replace")
            changed_syn = True
            note_syn = "Patched: added cross-reference to MasterRules_Tech.md"

        report += [
            "## Result",
            f"- Tech changed: **{changed_tech}** — {note_tech}",
            f"- Syntax changed: **{changed_syn}** — {note_syn}",
            "",
            "## Backups",
        ]
        for b in backups:
            report.append(f"- `{b.as_posix()}`")

        _write_report(reports_dir / f"Report_R2866_{_ts()}.md", report)
        return 0

    except Exception as e:
        # Rollback
        report += ["", "## ERROR", f"- {type(e).__name__}: {e}", "", "## ROLLBACK"]
        try:
            # Restore from backups in same order
            if backups:
                shutil.copy2(backups[0], tech)
                shutil.copy2(backups[1], syn)
                report.append("- Restored Tech + Syntax from backups.")
        except Exception as re:
            report.append(f"- Rollback failed: {type(re).__name__}: {re}")

        _write_report(reports_dir / f"Report_R2866_{_ts()}.md", report)
        return 11


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: R2866.py <repo_root>", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(Path(sys.argv[1]).resolve()))
