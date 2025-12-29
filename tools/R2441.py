import re
import sys
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

RID = "R2441"


def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def now():
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


def py_compile(root: Path, file_path: Path) -> tuple[bool, str]:
    cp = subprocess.run(
        [sys.executable, "-m", "py_compile", str(file_path)],
        cwd=str(root),
        text=True,
        capture_output=True,
    )
    ok = cp.returncode == 0
    out = (cp.stdout or "") + (cp.stderr or "")
    return ok, out.strip()


def restore(bak: Path | None, target: Path) -> None:
    if bak and bak.exists():
        shutil.copy2(bak, target)


def ensure_import(txt: str, import_line: str) -> str:
    if re.search(rf"^\s*{re.escape(import_line)}\s*$", txt, flags=re.M):
        return txt
    # insert after initial import block
    lines = txt.splitlines(True)
    i = 0
    while i < len(lines) and (
        lines[i].lstrip().startswith("import ") or lines[i].lstrip().startswith("from ")
    ):
        i += 1
    insert_at = sum(len(lines[j]) for j in range(i))
    return txt[:insert_at] + import_line + "\n" + txt[insert_at:]


def ensure_keep(root: Path, archiv: Path, report: list[str]) -> None:
    keep = root / "registry" / "tools_keep.txt"
    if not keep.exists():
        report.append("INFO: registry/tools_keep.txt not found (skip).")
        return
    txt = read(keep)
    items = [ln.strip() for ln in txt.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    if "R2441" in items:
        report.append("NO-OP: R2441 already in tools_keep.txt")
        return
    bk = backup(keep, archiv)
    write(keep, txt.rstrip() + "\nR2441\n")
    report.append(f"OK: appended R2441 to tools_keep.txt (backup={bk})")


def indent_block(block: str, indent: str) -> str:
    out = []
    for line in block.splitlines():
        if line.strip() == "":
            out.append("")
        else:
            out.append(indent + line)
    return "\n".join(out) + "\n"


def main() -> int:
    tools = Path(__file__).resolve().parent
    root = tools.parent
    docs = root / "docs"
    archiv = root / "_Archiv"
    ui = root / "modules" / "ui_toolbar.py"

    report = [
        f"[{RID}] Workspace Dropdown (indent-safe, compile-checked)",
        f"Time: {now()}",
        f"Root: {root}",
        f"File: {ui}",
        "",
    ]

    if not ui.exists():
        rp = docs / f"Report_{RID}_WorkspaceDropdown_{ts()}.md"
        write(rp, "\n".join(report + ["ERROR: modules/ui_toolbar.py not found"]) + "\n")
        print(f"[{RID}] ERROR: Report {rp}")
        return 2

    txt = read(ui)
    if "R2441: Workspace dropdown" in txt:
        rp = docs / f"Report_{RID}_WorkspaceDropdown_{ts()}.md"
        write(rp, "\n".join(report + ["NO-OP: already patched"]) + "\n")
        print(f"[{RID}] OK (NO-OP): Report {rp}")
        return 0

    b_ui = backup(ui, archiv)

    # Ensure imports (safe)
    before = txt
    txt = ensure_import(txt, "import tkinter as tk")
    txt = ensure_import(txt, "from tkinter import ttk")
    txt = ensure_import(txt, "import json")
    txt = ensure_import(txt, "from pathlib import Path")
    if txt != before:
        report.append("OK: ensured imports (tk/ttk/json/Path)")

    # Find anchor line and its indentation
    anchor_re = re.compile(
        r"^(?P<indent>\s*)row_push\s*=\s*ui_theme_classic\.Frame\((header_right|outer)\)\s*$", re.M
    )
    m = anchor_re.search(txt)
    if not m:
        restore(b_ui, ui)
        rp = docs / f"Report_{RID}_WorkspaceDropdown_{ts()}.md"
        write(rp, "\n".join(report + ["ERROR: could not locate row_push anchor"]) + "\n")
        print(f"[{RID}] ERROR: Report {rp}")
        return 3

    indent = m.group("indent")
    insert_at = m.start()

    # The WS block WITHOUT leading indentation; we'll indent it to match anchor
    ws_block = r"""
# R2441: Workspace dropdown (active workspace)
row_ws = ui_theme_classic.Frame(header_right if 'header_right' in locals() else outer)
row_ws.pack(fill="x", pady=(0, 2), anchor="ne")

def _ws_load_registry():
    try:
        rp = Path(getattr(app, "project_root", "")) / "registry" / "workspaces.json"
        if not rp.exists():
            rp = Path(__file__).resolve().parent.parent / "registry" / "workspaces.json"
        data = json.loads(rp.read_text(encoding="utf-8"))
        return rp, data
    except Exception:
        return None, {"active": "default", "workspaces": {"default": {"path": str(Path(__file__).resolve().parent.parent)}}}

def _ws_names(data):
    ws = data.get("workspaces", {})
    if not isinstance(ws, dict) or not ws:
        return ["default"]
    return list(ws.keys())

def _ws_active(data, names):
    a = str(data.get("active", "default"))
    if a not in names and names:
        a = names[0]
    return a

_ws_path, _ws_data = _ws_load_registry()
_names = _ws_names(_ws_data)
_active = _ws_active(_ws_data, _names)

if not hasattr(app, "_workspace_name_var"):
    app._workspace_name_var = tk.StringVar(value=_active)
app._workspace_name_var.set(_active)

try:
    lbl_ws = ui_theme_classic.Label(row_ws, text="WS")
    lbl_ws.pack(side="left", padx=(0, 6))
except Exception:
    pass

cb_ws = None
try:
    cb_ws = ttk.Combobox(row_ws, values=_names, width=18, state="readonly", textvariable=app._workspace_name_var)
    cb_ws.pack(side="right")
except Exception:
    cb_ws = None

def _ws_apply(event=None):
    try:
        name = str(app._workspace_name_var.get()).strip()
        if not name:
            return
        rp, data = _ws_load_registry()
        ws = data.get("workspaces", {})
        if not isinstance(ws, dict) or name not in ws:
            return
        data["active"] = name
        if rp is not None:
            rp.parent.mkdir(parents=True, exist_ok=True)
            rp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        try:
            app.workspace_root = Path(str(ws[name].get("path",""))).resolve()
        except Exception:
            pass
        try:
            row_ws.event_generate("<<WorkspaceChanged>>")
        except Exception:
            pass
    except Exception:
        pass

try:
    if cb_ws is not None:
        cb_ws.bind("<<ComboboxSelected>>", _ws_apply, add="+")
except Exception:
    pass
""".strip("\n")

    txt2 = txt[:insert_at] + indent_block(ws_block, indent) + txt[insert_at:]
    write(ui, txt2)
    report.append(f"OK: inserted workspace dropdown with indent='{indent.replace(' ', '·')}'")

    ok, out = py_compile(root, ui)
    if not ok:
        report.append("ERROR: py_compile failed -> rollback")
        report.append(out)
        restore(b_ui, ui)
        rp = docs / f"Report_{RID}_WorkspaceDropdown_{ts()}.md"
        write(rp, "\n".join(report + [f"Backup: {b_ui}"]) + "\n")
        print(f"[{RID}] ERROR: compile failed; rolled back. Report {rp}")
        return 5

    report.append("OK: py_compile passed")
    ensure_keep(root, archiv, report)

    rp = docs / f"Report_{RID}_WorkspaceDropdown_{ts()}.md"
    write(rp, "\n".join(report + [f"Backup: {b_ui}"]) + "\n")
    print(f"[{RID}] OK: Report {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
