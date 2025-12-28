import sys
import shutil
from datetime import datetime
from pathlib import Path

RID = "R2419"


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


def force_pady_zero(line: str) -> tuple[str, bool]:
    """
    Ensures pady=(0,0) in a .pack(...) call line.
    - If pady= exists -> replace its value with (0, 0)
    - Else -> inject pady=(0, 0) before closing )
    """
    if ".pack(" not in line:
        return line, False

    # already has pady=(0,0)
    if "pady=(0, 0)" in line or "pady=(0,0)" in line:
        return line, False

    changed = False
    if "pady=" in line:
        # crude but robust: replace from "pady=" until next comma or ')'
        pre, rest = line.split("pady=", 1)
        # rest begins with something like "(0,2), ..." or "2, ..." or "(0, 2))"
        # We overwrite first token part.
        # Find separator position: comma that ends the pady arg, or closing paren.
        sep_idx = None
        for i, ch in enumerate(rest):
            if ch == ",":
                sep_idx = i
                break
            if ch == ")":
                sep_idx = i
                break
        if sep_idx is None:
            return line, False
        rest2 = rest[sep_idx:]  # includes separator
        new = pre + "pady=(0, 0)" + rest2
        return new, True

    # no pady param: inject before last ')'
    idx = line.rfind(")")
    if idx < 0:
        return line, False
    # if there are other args, add comma
    inside = line[line.find("(") + 1 : idx].strip()
    comma = ", " if inside else ""
    new = line[:idx] + f"{comma}pady=(0, 0)" + line[idx:]
    return new, True


def main() -> int:
    tools = Path(__file__).resolve().parent
    root = tools.parent
    docs = root / "docs"
    archiv = root / "_Archiv"
    ui_toolbar = root / "modules" / "ui_toolbar.py"

    report = [
        f"[{RID}] UI Fix: Force top-edge padding",
        f"Time: {now_human()}",
        f"File: {ui_toolbar}",
        "",
    ]

    if not ui_toolbar.exists():
        rp = docs / f"Report_{RID}_UIFix_{ts()}.md"
        write(rp, "\n".join(report + ["ERROR: ui_toolbar.py missing"]) + "\n")
        print(f"[{RID}] ERROR: Report {rp}")
        return 2

    txt = read(ui_toolbar)
    lines = txt.split("\n")
    out = []
    changed_any = False
    changed_row_push = 0
    changed_outer = 0

    for ln in lines:
        orig = ln
        if "row_push.pack(" in ln:
            ln, ch = force_pady_zero(ln)
            if ch:
                changed_any = True
                changed_row_push += 1
        if "outer.pack(" in ln:
            ln, ch = force_pady_zero(ln)
            if ch:
                changed_any = True
                changed_outer += 1
        out.append(ln)

    if not changed_any:
        rp = docs / f"Report_{RID}_UIFix_{ts()}.md"
        write(rp, "\n".join(report + ["NO-OP: no pack() pady changes applied"]) + "\n")
        print(f"[{RID}] OK (NO-OP): Report {rp}")
        return 0

    backup(ui_toolbar, archiv)
    write(ui_toolbar, "\n".join(out))

    rp = docs / f"Report_{RID}_UIFix_{ts()}.md"
    write(
        rp,
        "\n".join(
            report
            + [
                "OK: enforced pady=(0,0) for top alignment",
                f"- row_push.pack changed: {changed_row_push}",
                f"- outer.pack changed: {changed_outer}",
            ]
        )
        + "\n",
    )
    print(f"[{RID}] OK: Report {rp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
