# R2398 - Build snapshot zip:
# - includes modules/, docs/, ShrimpDev.ini and SNAPSHOT_README.md
# - writes report
# Safe: no deletes, create _Snapshots/, deterministic naming.

from __future__ import annotations
from pathlib import Path
from datetime import datetime
import zipfile
import hashlib

RID = "R2398"
ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / "_Snapshots"
DOCS = ROOT / "docs"

def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def write(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")

def add_tree(z: zipfile.ZipFile, base: Path, arc_prefix: str) -> int:
    n = 0
    if not base.exists():
        return 0
    for p in base.rglob("*"):
        if p.is_dir():
            continue
        rel = p.relative_to(ROOT)
        # store under same tree structure
        z.write(p, str(rel))
        n += 1
    return n

def main() -> int:
    rep = []
    rep.append(f"# Report {RID} – Snapshot Build")
    rep.append("")
    rep.append(f"- Timestamp: {ts()}")
    rep.append(f"- Root: `{ROOT}`")
    rep.append("")

    SNAP.mkdir(parents=True, exist_ok=True)

    zip_name = f"ShrimpDev_DockingStable_R2395_{stamp()}.zip"
    zip_path = SNAP / zip_name

    readme = []
    readme.append("# SNAPSHOT README")
    readme.append("")
    readme.append(f"- Created: {ts()}")
    readme.append(f"- Snapshot: {zip_name}")
    readme.append("- Purpose: Fixpoint after Docking restore bug resolved and documentation synced.")
    readme.append("- Includes: modules/, docs/, ShrimpDev.ini")
    readme.append("")
    readme_text = "\n".join(readme) + "\n"

    tmp_readme = ROOT / "_Snapshots" / "SNAPSHOT_README.md"
    write(tmp_readme, readme_text)

    count = 0
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        count += add_tree(z, ROOT / "modules", "modules")
        count += add_tree(z, ROOT / "docs", "docs")
        ini = ROOT / "ShrimpDev.ini"
        if ini.exists():
            z.write(ini, str(ini.relative_to(ROOT)))
            count += 1
        z.write(tmp_readme, str(tmp_readme.relative_to(ROOT)))
        count += 1

    rep.append(f"- Zip: `{zip_path}`")
    rep.append(f"- Files: {count}")
    rep.append(f"- SHA256: `{sha256(zip_path)}`")
    rep.append("")

    rp = DOCS / f"Report_{RID}_Snapshot_{stamp()}.md"
    write(rp, "\n".join(rep) + "\n")
    print(f"[{RID}] OK: Snapshot {zip_path} | Report {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
