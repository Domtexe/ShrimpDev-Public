import re
import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

RID = "R2433"


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


def py_compile(root: Path, file_rel: str) -> tuple[bool, str]:
    try:
        cp = subprocess.run(
            [sys.executable, "-m", "py_compile", str(root / file_rel)],
            cwd=str(root),
            text=True,
            capture_output=True,
        )
        ok = cp.returncode == 0
        out = (cp.stdout or "") + (cp.stderr or "")
        return ok, out.strip()
    except Exception as e:
        return False, f"py_compile exception: {e}"


def ensure_keep(root: Path, archiv: Path, report: list[str]) -> None:
    keep = root / "registry" / "tools_keep.txt"
    if not keep.exists():
        return
    txt = read(keep)
    items = [ln.strip() for ln in txt.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    if "R2433" in items:
        return
    bk = backup(keep, archiv)
    write(keep, txt.rstrip() + "\nR2433\n")
    report.append(f"OK: appended R2433 to registry/tools_keep.txt (backup={bk})")


def patch_pipeline(root: Path, archiv: Path, report: list[str]) -> None:
    pipe = root / "docs" / "PIPELINE.md"
    if not pipe.exists():
        report.append("WARN: docs/PIPELINE.md not found (no pipeline update).")
        return
    txt = read(pipe)
    if "Artefakte - Tab: Treeview auto-refresh" in txt:
        report.append("NO-OP: Pipeline already contains Artefakte auto-refresh task.")
        return

    heading = "## Runner-Produkte"
    idx = txt.find(heading)
    if idx < 0:
        report.append("WARN: Could not find '## Runner-Produkte' heading (no pipeline update).")
        return

    head_end = txt.find("\n", idx)
    insert_at = head_end + 1

    block = (
        "\n"
        "- [ ] (P1) Artefakte - Tab: Treeview auto-refresh, wenn Tab aktiv wird\n"
        "  - Trigger: <<NotebookTabChanged>> -> Artefakte\n"
        "  - Prefer: refresh_runner_products_tab() falls vorhanden\n"
        "  - Fallback: safe rebuild (children destroy + build_runner_products_tab)\n"
    )

    bk = backup(pipe, archiv)
    write(pipe, txt[:insert_at] + block + txt[insert_at:])
    report.append(f"OK: Pipeline updated under '## Runner-Produkte' (backup={bk})")


def main() -> int:
    tools = Path(__file__).resolve().parent
    root = tools.parent
    docs = root / "docs"
    archiv = root / "_Archiv"
    gui = root / "main_gui.py"

    report = [
        f"[{RID}] SAFE PATCH: Artefakte tab auto-refresh (compile-checked)",
        f"Time: {now()}",
        f"Root: {root}",
        f"File: {gui}",
        "",
    ]

    if not gui.exists():
        rp = docs / f"Report_{RID}_ArtefakteAutoRefresh_{ts()}.md"
        write(rp, "\n".join(report + ["ERROR: main_gui.py not found"]) + "\n")
        print(f"[{RID}] ERROR: Report {rp}")
        return 2

    txt = read(gui)
    orig = txt

    # Already patched?
    if "def _on_notebook_tab_changed_r2433" in txt:
        rp = docs / f"Report_{RID}_ArtefakteAutoRefresh_{ts()}.md"
        write(rp, "\n".join(report + ["NO-OP: already patched"]) + "\n")
        print(f"[{RID}] OK (NO-OP): Report {rp}")
        return 0

    # --- Insert handler method inside class ShrimpDevApp ---
    # Find insertion point: before "def main(" at module level.
    m_main = re.search(r"^\s*def\s+main\s*\(", txt, flags=re.M)
    if not m_main:
        rp = docs / f"Report_{RID}_ArtefakteAutoRefresh_{ts()}.md"
        write(
            rp,
            "\n".join(report + ["ERROR: could not locate def main() for safe insertion point"])
            + "\n",
        )
        print(f"[{RID}] ERROR: Report {rp}")
        return 3

    handler = """
    # R2433: Auto-refresh Artefakte tab when activated (SAFE)
    def _on_notebook_tab_changed_r2433(self, event=None):
        try:
            nb = getattr(self, "nb", None)
            if nb is None:
                return
            sel = nb.select()
            if not sel:
                return
            tab = nb.nametowidget(sel)

            # Artefakte tab: self.tab_runner_products
            if tab is getattr(self, "tab_runner_products", None):
                # Prefer module refresh if exists
                try:
                    from modules import ui_runner_products_tab
                    if hasattr(ui_runner_products_tab, "refresh_runner_products_tab"):
                        ui_runner_products_tab.refresh_runner_products_tab(tab, self)
                        return
                    if hasattr(ui_runner_products_tab, "refresh"):
                        ui_runner_products_tab.refresh(tab, self)
                        return
                except Exception:
                    pass

                # Fallback: safe rebuild
                try:
                    for w in list(tab.winfo_children()):
                        try:
                            w.destroy()
                        except Exception:
                            pass
                    from modules import ui_runner_products_tab
                    ui_runner_products_tab.build_runner_products_tab(tab, self)
                except Exception:
                    pass
        except Exception:
            pass
"""

    insert_at = m_main.start()
    txt = txt[:insert_at] + handler + "\n" + txt[insert_at:]
    report.append("OK: inserted handler _on_notebook_tab_changed_r2433()")

    # --- Insert bind call near notebook setup ---
    # We want to bind AFTER notebook exists and tabs are created.
    # Anchor: first occurrence of "self.nb.pack" or "self.nb.grid"
    m_pack = re.search(r"^\s*self\.nb\.(pack|grid)\(", txt, flags=re.M)
    if not m_pack:
        # fallback anchor: any "ttk.Notebook(" assignment
        m_nb = re.search(r"^\s*self\.nb\s*=\s*ttk\.Notebook\(", txt, flags=re.M)
        if not m_nb:
            # If we can't find a safe anchor, revert change.
            txt = orig
            rp = docs / f"Report_{RID}_ArtefakteAutoRefresh_{ts()}.md"
            write(
                rp,
                "\n".join(
                    report
                    + [
                        "ERROR: could not locate Notebook anchor (self.nb.pack/grid or self.nb=ttk.Notebook)"
                    ]
                )
                + "\n",
            )
            print(f"[{RID}] ERROR: Report {rp}")
            return 4
        anchor_line_end = txt.find("\n", m_nb.start())
        bind_at = anchor_line_end + 1
    else:
        anchor_line_end = txt.find("\n", m_pack.start())
        bind_at = anchor_line_end + 1

    bind_block = """
        # R2433: bind tab-changed -> artefakte refresh (SAFE)
        try:
            self.nb.bind("<<NotebookTabChanged>>", self._on_notebook_tab_changed_r2433, add="+")
        except Exception:
            pass
"""
    if "self._on_notebook_tab_changed_r2433" not in txt:
        txt = txt[:bind_at] + bind_block + txt[bind_at:]
        report.append("OK: inserted NotebookTabChanged bind (safe try/except)")

    # Write + compile check
    b = backup(gui, archiv)
    write(gui, txt)

    ok, out = py_compile(root, "main_gui.py")
    if not ok:
        # rollback to backup
        if b and b.exists():
            shutil.copy2(b, gui)
        rp = docs / f"Report_{RID}_ArtefakteAutoRefresh_{ts()}.md"
        write(
            rp,
            "\n".join(
                report
                + [
                    "ERROR: py_compile failed; restored backup automatically",
                    f"Backup used: {b}",
                    "",
                    "py_compile output:",
                    out,
                ]
            )
            + "\n",
        )
        print(f"[{RID}] ERROR: compile failed; restored backup. Report {rp}")
        return 5

    report.append("OK: py_compile passed")

    # Pipeline + keep
    patch_pipeline(root, archiv, report)
    ensure_keep(root, archiv, report)

    rp = docs / f"Report_{RID}_ArtefakteAutoRefresh_{ts()}.md"
    write(rp, "\n".join(report + [f"Backup: {b}"]) + "\n")
    print(f"[{RID}] OK: Report {rp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
