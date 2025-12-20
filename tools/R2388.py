import re
import sys
import hashlib
from pathlib import Path
from datetime import datetime

RUNNER_ID = "R2388"

def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def backup_file(src: Path, archiv_dir: Path) -> Path:
    archiv_dir.mkdir(parents=True, exist_ok=True)
    bak = archiv_dir / f"{src.name}.{RUNNER_ID}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    bak.write_bytes(src.read_bytes())
    return bak

def write_report(root: Path, lines: list[str]) -> Path:
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    rp = docs / f"Report_{RUNNER_ID}_Docking_RestoreFix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    rp.write_text("\n".join(lines), encoding="utf-8")
    return rp

def patch_module_docking(text: str) -> tuple[str, list[str], bool]:
    notes = []
    changed = False

    # 1) Fix wrong variable "win.geometry(" -> "w.geometry("
    if "win.geometry(" in text:
        text2 = text.replace("win.geometry(", "w.geometry(")
        if text2 != text:
            notes.append("- FIX: ersetze `win.geometry(` -> `w.geometry(`")
            text = text2
            changed = True

    # 2) Fix restore_geometry logic: if Docking.<key>.geometry exists, DO NOT set restore_geometry=False.
    #    Instead: restore_geometry = geo (string), so later geometry apply uses correct value.
    #    We patch the specific block as seen in your scan.
    pat = re.compile(
        r"(# R2361_GEOMETRY_PERSIST\s*\n\s*geo\s*=\s*cfg\.get\(\"Docking\",\s*f\"\{key\}\.geometry\",\s*fallback=\"\"\)\s*\n\s*if\s+geo:\s*\n\s*w\.geometry\(geo\)\s*\n\s*restore_geometry\s*=\s*False\s*\n)",
        re.MULTILINE
    )
    m = pat.search(text)
    if m:
        repl = (
            "# R2361_GEOMETRY_PERSIST\n"
            "            geo = cfg.get(\"Docking\", f\"{key}.geometry\", fallback=\"\").strip()\n"
            "            if geo:\n"
            "                # Wichtig: restore_geometry muss STRING bleiben, sonst fällt Restore auf Center/WM-Default zurück\n"
            "                restore_geometry = geo\n"
        )
        text = pat.sub(repl, text, count=1)
        notes.append("- FIX: `restore_geometry` bleibt Geometry-String (kein False), wenn `Docking.<key>.geometry` existiert")
        changed = True
    else:
        notes.append("- WARN: Block `R2361_GEOMETRY_PERSIST` nicht exakt gefunden (kein Patch an dieser Stelle)")

    return text, notes, changed

def patch_main_gui(text: str) -> tuple[str, list[str], bool]:
    notes = []
    changed = False

    # Add fallback: if [UI].geometry is empty, try [Docking] main.geometry
    # Find the spot after UI geometry read and before `if geo: ... app.geometry(geo)`
    anchor = 'if cfg.has_section("UI"):\n            geo = cfg.get("UI", "geometry", fallback="").strip()\n'
    if anchor in text:
        insert = (
            anchor +
            "        # R2388: Fallback – wenn UI.geometry fehlt, nimm Docking main.geometry\n"
            "        if not geo and cfg.has_section(\"Docking\"):\n"
            "            geo = cfg.get(\"Docking\", \"main.geometry\", fallback=\"\").strip()\n"
        )
        text2 = text.replace(anchor, insert, 1)
        if text2 != text:
            text = text2
            notes.append("- FIX: main restore liest jetzt fallback aus `[Docking] main.geometry`")
            changed = True
    else:
        notes.append("- WARN: Anchor in _r2368_apply_main_geometry nicht gefunden (kein Patch)")

    return text, notes, changed

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    archiv = root / "_Archiv"

    f_docking = root / "modules" / "module_docking.py"
    f_main = root / "main_gui.py"

    report = []
    report.append(f"# Report {RUNNER_ID} – Docking Restore Fix")
    report.append("")
    report.append(f"- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: `{root}`")
    report.append("")

    ok = True

    for fp in (f_docking, f_main):
        if not fp.exists():
            report.append(f"## ERROR: Datei fehlt: `{fp}`")
            ok = False

    if not ok:
        rp = write_report(root, report)
        print(f"[{RUNNER_ID}] FEHLER: Dateien fehlen. Report: {rp}")
        return 2

    # Backups
    bak_d = backup_file(f_docking, archiv)
    bak_m = backup_file(f_main, archiv)

    report.append("## Backups")
    report.append(f"- `{f_docking}` -> `{bak_d.name}`")
    report.append(f"- `{f_main}` -> `{bak_m.name}`")
    report.append("")

    # Patch module_docking.py
    d0 = f_docking.read_text(encoding="utf-8", errors="ignore")
    d1, notes_d, changed_d = patch_module_docking(d0)

    # Patch main_gui.py
    m0 = f_main.read_text(encoding="utf-8", errors="ignore")
    m1, notes_m, changed_m = patch_main_gui(m0)

    report.append("## module_docking.py")
    report.append(f"- Before SHA256: `{hashlib.sha256(d0.encode('utf-8', errors='ignore')).hexdigest()}`")
    report.extend(notes_d)
    report.append(f"- Changed: **{changed_d}**")
    report.append("")

    report.append("## main_gui.py")
    report.append(f"- Before SHA256: `{hashlib.sha256(m0.encode('utf-8', errors='ignore')).hexdigest()}`")
    report.extend(notes_m)
    report.append(f"- Changed: **{changed_m}**")
    report.append("")

    if changed_d:
        f_docking.write_text(d1, encoding="utf-8")
    if changed_m:
        f_main.write_text(m1, encoding="utf-8")

    # quick import/syntax check (py_compile)
    report.append("## Syntax-Check")
    try:
        import py_compile
        py_compile.compile(str(f_docking), doraise=True)
        py_compile.compile(str(f_main), doraise=True)
        report.append("- OK: py_compile für beide Dateien")
        rc = 0
    except Exception as e:
        report.append(f"- FAIL: py_compile: `{e!r}`")
        rc = 2

    # After hashes (file-based)
    report.append("")
    report.append("## After (file hashes)")
    report.append(f"- module_docking.py SHA256: `{sha256(f_docking)}`")
    report.append(f"- main_gui.py SHA256: `{sha256(f_main)}`")

    rp = write_report(root, report)
    print(f"[{RUNNER_ID}] OK: Report {rp}")
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
