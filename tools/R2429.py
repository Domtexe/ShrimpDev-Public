import sys
import shutil
from datetime import datetime
from pathlib import Path

RID = "R2429"


def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def now_human() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def write(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8", newline="\n")


def backup(p: Path, archiv: Path) -> Path | None:
    if not p.exists():
        return None
    archiv.mkdir(parents=True, exist_ok=True)
    b = archiv / f"{p.name}.{RID}_{ts()}.bak"
    shutil.copy2(p, b)
    return b


def main() -> int:
    tools_dir = Path(__file__).resolve().parent
    root = tools_dir.parent
    docs = root / "docs"
    archiv = root / "_Archiv"
    ui = root / "modules" / "ui_toolbar.py"
    keep = root / "registry" / "tools_keep.txt"

    report = [
        f"[{RID}] UI Layout Fix: top-right alignment for push/purge + row1 left",
        f"Time: {now_human()}",
        f"Root: {root}",
        f"File: {ui}",
        "",
    ]

    if not ui.exists():
        rp = docs / f"Report_{RID}_UILayout_{ts()}.md"
        write(rp, "\n".join(report + ["ERROR: modules/ui_toolbar.py missing"]) + "\n")
        print(f"[{RID}] ERROR: {rp}")
        return 2

    txt = read(ui)
    orig = txt

    # --- 1) Ensure we have a dedicated header_right frame inside build_toolbar_right ---
    # Replace the "outer = ..." line (may have trailing comment) with clean outer + header_right.
    # We match the line that starts with "outer = ui_theme_classic.Frame(parent)"
    import re

    outer_pat = re.compile(r"^(\s*)outer\s*=\s*ui_theme_classic\.Frame\(parent\).*?$", re.M)

    m = outer_pat.search(txt)
    if not m:
        rp = docs / f"Report_{RID}_UILayout_{ts()}.md"
        write(
            rp,
            "\n".join(report + ["ERROR: could not locate 'outer = ui_theme_classic.Frame(parent)'"])
            + "\n",
        )
        print(f"[{RID}] ERROR: {rp}")
        return 3

    indent = m.group(1)
    replacement_outer = (
        f"{indent}outer = ui_theme_classic.Frame(parent)\n"
        f"{indent}# R2429: Right-top stack for Push/Purge (flush top-right, stacked)\n"
        f"{indent}header_right = ui_theme_classic.Frame(outer)\n"
        f'{indent}header_right.pack(fill="x", pady=(0, 0), anchor="ne")'
    )
    txt = outer_pat.sub(replacement_outer, txt, count=1)

    # --- 2) Move row_push + row0 to header_right (instead of outer) and anchor them top-right ---
    txt = txt.replace(
        "row_push = ui_theme_classic.Frame(outer)",
        "row_push = ui_theme_classic.Frame(header_right)",
    )
    txt = txt.replace(
        'row_push.pack(fill="x", pady=(0, 0))', 'row_push.pack(fill="x", pady=(0, 0), anchor="ne")'
    )

    txt = txt.replace(
        "row0 = ui_theme_classic.Frame(outer)", "row0 = ui_theme_classic.Frame(header_right)"
    )
    # row0.pack(...) variants:
    txt = re.sub(
        r'row0\.pack\(\s*fill="x",\s*pady=\(0,\s*2\)\s*\)',
        'row0.pack(fill="x", pady=(0, 2), anchor="ne")',
        txt,
    )

    # --- 3) Force Row1 (Run/Löschen/Rename/Undo) to be left-aligned above the treeview area ---
    # Keep in outer; just make pack anchor explicit (doesn't change logic).
    txt = re.sub(
        r'row1\.pack\(\s*fill="x",\s*pady=\(0,\s*2\)\s*\)',
        'row1.pack(fill="x", pady=(0, 2), anchor="w")',
        txt,
    )

    if txt == orig:
        rp = docs / f"Report_{RID}_UILayout_{ts()}.md"
        write(rp, "\n".join(report + ["NO-OP: nothing changed"]) + "\n")
        print(f"[{RID}] OK (NO-OP): {rp}")
        return 0

    b = backup(ui, archiv)
    write(ui, txt)

    # Keep-list: ensure runner isn't purged
    if keep.exists():
        keep_txt = read(keep).splitlines()
        items = [ln.strip() for ln in keep_txt if ln.strip() and not ln.strip().startswith("#")]
        if "R2429" not in items:
            bk = backup(keep, archiv)
            write(keep, read(keep).rstrip() + "\nR2429\n")
            report.append(f"OK: appended R2429 to registry/tools_keep.txt (backup={bk})")

    rp = docs / f"Report_{RID}_UILayout_{ts()}.md"
    write(
        rp,
        "\n".join(
            report
            + [
                "OK: Push/Purge moved into header_right (top-right flush, stacked).",
                "OK: Row1 pack anchor set to 'w' (left over treeview).",
                f"Backup: {b}",
            ]
        )
        + "\n",
    )

    print(f"[{RID}] OK: Report {rp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
