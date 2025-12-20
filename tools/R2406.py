from __future__ import annotations

from pathlib import Path
from datetime import datetime
import hashlib
import py_compile
import re

RID = "R2406"
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ARCHIV = ROOT / "_Archiv"
TARGET = ROOT / "main_gui.py"

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

PATCH_BLOCK = r"""
    # {rid}: Apply main window geometry from ShrimpDev.ini [Docking] main.geometry (best-effort)
    # Reason: default geometry can drift/center if restore isn't applied early.
    try:
        import os, configparser
        ini_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "ShrimpDev.ini")
        cfg = configparser.ConfigParser()
        cfg.read(ini_path, encoding="utf-8")
        geo = ""
        try:
            geo = cfg.get("Docking", "main.geometry", fallback="").strip()
        except Exception:
            geo = ""
        if geo:
            try:
                app.update_idletasks()
            except Exception:
                pass
            try:
                app.geometry(geo)
            except Exception:
                pass
    except Exception:
        pass
""".format(rid=RID).strip("\n")

def main() -> int:
    rep = []
    rep.append(f"# Report {RID} – Apply main geometry on startup")
    rep.append("")
    rep.append(f"- Timestamp: {ts()}")
    rep.append(f"- Target: `{TARGET}`")
    rep.append("")

    if not TARGET.exists():
        out = DOCS / f"Report_{RID}_MISSING_{stamp()}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(rep) + "\n", encoding="utf-8")
        print(f"[{RID}] FEHLER: main_gui.py fehlt. Report {out}")
        return 2

    before_sha = sha256(TARGET)
    src = TARGET.read_text(encoding="utf-8", errors="replace")

    # Insert right after: app = ShrimpDevApp()
    needle = "app = ShrimpDevApp()"
    if needle not in src:
        out = DOCS / f"Report_{RID}_NO_NEEDLE_{stamp()}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        rep.append(f"- sha256 before: `{before_sha}`")
        rep.append("")
        rep.append("## FAIL")
        rep.append(f"- Needle not found: `{needle}`")
        out.write_text("\n".join(rep) + "\n", encoding="utf-8")
        print(f"[{RID}] FEHLER: Needle nicht gefunden. Report {out}")
        return 2

    # Dupe guard
    if f"{RID}: Apply main window geometry" in src:
        out = DOCS / f"Report_{RID}_NOOP_{stamp()}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        rep.append(f"- sha256 before: `{before_sha}`")
        rep.append("")
        rep.append("## No-op")
        rep.append("- Patch block already present.")
        out.write_text("\n".join(rep) + "\n", encoding="utf-8")
        print(f"[{RID}] OK: already patched (no-op). Report {out}")
        return 0

    bak = backup_file(TARGET)

    # Do insertion: find first occurrence line-wise
    lines = src.splitlines()
    out_lines = []
    inserted = False
    for ln in lines:
        out_lines.append(ln)
        if (not inserted) and ln.strip() == needle:
            out_lines.append("")
            for pl in PATCH_BLOCK.splitlines():
                out_lines.append(pl.rstrip())
            out_lines.append("")
            inserted = True

    new_src = "\n".join(out_lines) + "\n"
    TARGET.write_text(new_src, encoding="utf-8")

    after_sha = sha256(TARGET)

    # Compile gate
    ok = True
    comp_err = None
    try:
        py_compile.compile(str(TARGET), doraise=True)
    except Exception as e:
        ok = False
        comp_err = repr(e)

    rep.append(f"- backup: `{bak}`")
    rep.append(f"- sha256 before: `{before_sha}`")
    rep.append(f"- sha256 after: `{after_sha}`")
    rep.append("")
    rep.append("## Compile Gate")
    if ok:
        rep.append("- OK")
    else:
        rep.append(f"- FAIL: {comp_err}")

    out = DOCS / f"Report_{RID}_MainGeometryApply_{stamp()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(rep) + "\n", encoding="utf-8")

    print(f"[{RID}] OK: Patch applied. Report {out}")
    return 0 if ok else 2

if __name__ == "__main__":
    raise SystemExit(main())
