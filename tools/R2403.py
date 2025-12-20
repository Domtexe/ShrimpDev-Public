from __future__ import annotations

from pathlib import Path
from datetime import datetime
import hashlib
import py_compile
import re

RID = "R2403"
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ARCHIV = ROOT / "_Archiv"
TARGET = ROOT / "modules" / "ui_toolbar.py"

def ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def backup_file(p: Path) -> Path:
    ARCHIV.mkdir(parents=True, exist_ok=True)
    bak = ARCHIV / f"{p.name}.{RID}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    bak.write_bytes(p.read_bytes())
    return bak

def patch(text: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    out = text

    # 1) _save_log_geometry: ersetze direkten INI write durch config_manager.set_value + mgr.save()
    # Wir patchen nur den INNEREN TRY-Block (wo geom gesetzt und Datei geschrieben wurde).
    # Typische Struktur in ui_toolbar.py:
    # def _save_log_geometry(app, win):
    #   ...
    #   try:
    #       cfg = ...
    #       ...
    #       with open(ini_path, "w", ...) as f:
    #           cfg.write(f)
    #   except Exception:
    #       ...
    #
    # Wir ersetzen alles von "with open(ini_path" bis inkl "cfg.write(f)" + Block-Ende.
    pattern_open_write = re.compile(
        r"""(?P<indent>^[ \t]*)with[ \t]+open\([^\n]*\n(?:(?P=indent)[ \t]+.*\n)*?(?P=indent)[ \t]*cfg\.write\([^\n]*\)\n""",
        re.MULTILINE
    )

    repl = (
        r"\g<indent># {rid}: SingleWriter – do not write ShrimpDev.ini directly here\n"
        r"\g<indent>try:\n"
        r"\g<indent>    from modules import config_manager as _cfgm  # type: ignore\n"
        r"\g<indent>    _cfgm.set_value('geometry', str(geom), section='LogWindow', auto_save=False)\n"
        r"\g<indent>    _cfgm.get_manager().save()\n"
        r"\g<indent>except Exception:\n"
        r"\g<indent>    # best-effort, never crash UI\n"
        r"\g<indent>    pass\n"
    ).format(rid=RID)

    new_out, n = pattern_open_write.subn(repl, out, count=4)  # max wenige Stellen
    if n > 0:
        out = new_out
        notes.append(f"OK: replaced {n} direct open(...)/cfg.write(...) blocks with ConfigManager save path")
    else:
        notes.append("WARN: no direct open(...)/cfg.write(...) block found (no-op)")

    # 2) Zusätzlich: falls es noch cfg['LogWindow']['geometry']=... gibt, lassen wir es stehen.
    # Wichtig ist nur: kein kompletter INI Rewrite.
    return out, notes

def main() -> int:
    report = []
    report.append(f"# Report {RID} – ui_toolbar INI writes -> ConfigManager (SingleWriter)")
    report.append("")
    report.append(f"- Timestamp: {ts()}")
    report.append(f"- Target: `{TARGET}`")
    report.append("")

    if not TARGET.exists():
        out = DOCS / f"Report_{RID}_MISSING_{stamp()}.md"
        out.write_text("\n".join(report) + "\n", encoding="utf-8")
        print(f"[{RID}] FEHLER: Target missing. Report {out}")
        return 2

    before_sha = sha256(TARGET)
    before = TARGET.read_text(encoding="utf-8", errors="replace")

    patched, notes = patch(before)
    changed = (patched != before)

    report.append(f"- sha256 before: `{before_sha}`")
    report.append("")
    report.append("## Patch Notes")
    for n in notes:
        report.append(f"- {n}")
    report.append("")

    backups = []
    if changed:
        bak = backup_file(TARGET)
        backups.append(str(bak))
        TARGET.write_text(patched, encoding="utf-8")
        after_sha = sha256(TARGET)
        report.append("## Backup")
        report.append(f"- `{bak}`")
        report.append("")
        report.append("## sha256 after")
        report.append(f"- `{after_sha}`")
        report.append("")
    else:
        report.append("## No changes")
        report.append("- File already compliant or pattern not matched.")
        report.append("")

    # Compile gate
    report.append("## Compile Gate")
    ok = True
    try:
        py_compile.compile(str(TARGET), doraise=True)
        report.append(f"- OK: {TARGET}")
    except Exception as e:
        ok = False
        report.append(f"- FAIL: {TARGET} :: {e!r}")

    out = DOCS / f"Report_{RID}_UIToolbar_SingleWriter_{stamp()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(report) + "\n", encoding="utf-8")

    print(f"[{RID}] OK: Report {out}")
    return 0 if ok else 2

if __name__ == "__main__":
    raise SystemExit(main())
