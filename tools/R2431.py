import sys
import shutil
from datetime import datetime
from pathlib import Path

RID = "R2431"


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


def ensure_keep(root: Path, archiv: Path, report_lines: list[str]) -> None:
    keep = root / "registry" / "tools_keep.txt"
    if not keep.exists():
        return
    txt = read(keep)
    items = [ln.strip() for ln in txt.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    if "R2431" in items:
        return
    bk = backup(keep, archiv)
    write(keep, txt.rstrip() + "\nR2431\n")
    report_lines.append(f"OK: appended R2431 to registry/tools_keep.txt (backup={bk})")


def patch_pipeline(root: Path, archiv: Path, report_lines: list[str]) -> None:
    pipe = root / "docs" / "PIPELINE.md"
    if not pipe.exists():
        report_lines.append("WARN: docs/PIPELINE.md not found (no pipeline update).")
        return
    txt = read(pipe)
    if "Artefakte - Tab" in txt or "auto-refresh" in txt or "Auto-Refresh" in txt:
        report_lines.append("NO-OP: Pipeline already contains Artefakte auto-refresh task.")
        return

    heading = "## Runner-Produkte"
    idx = txt.find(heading)
    if idx < 0:
        report_lines.append(
            "WARN: Could not find '## Runner-Produkte' heading (no pipeline update)."
        )
        return

    head_end = txt.find("\n", idx)
    insert_at = head_end + 1

    block = (
        "\n"
        "- [ ] (P1) Artefakte - Tab: Treeview auto-refresh, wenn Tab aktiv wird\n"
        "  - Trigger: NotebookTabChanged -> Artefakte\n"
        "  - Prefer: refresh_runner_products_tab() falls vorhanden\n"
        "  - Fallback: Tab-Inhalt neu aufbauen (safe rebuild)\n"
    )

    bk = backup(pipe, archiv)
    write(pipe, txt[:insert_at] + block + txt[insert_at:])
    report_lines.append(f"OK: Pipeline updated under '## Runner-Produkte' (backup={bk})")


def main() -> int:
    tools_dir = Path(__file__).resolve().parent
    root = tools_dir.parent
    docs = root / "docs"
    archiv = root / "_Archiv"
    gui = root / "main_gui.py"

    report = [
        f"[{RID}] Artefakte Tab Auto-Refresh + Pipeline",
        f"Time: {now_human()}",
        f"Root: {root}",
        "",
    ]

    if not gui.exists():
        rp = docs / f"Report_{RID}_ArtefakteAutoRefresh_{ts()}.md"
        write(rp, "\n".join(report + ["ERROR: main_gui.py not found"]) + "\n")
        print(f"[{RID}] ERROR: Report {rp}")
        return 2

    txt = read(gui)
    orig = txt

    # 1) Add binding after tabs are built (after runner-products tab is added)
    bind_snippet = """
        # R2431: Auto-refresh Artefakte tab when activated
        try:
            self.nb.bind("<<NotebookTabChanged>>", self._on_notebook_tab_changed, add="+")
        except Exception:
            pass
"""
    if "R2431: Auto-refresh Artefakte tab when activated" not in txt:
        anchor = "ui_runner_products_tab.build_runner_products_tab(self.tab_runner_products, self)"
        pos = txt.find(anchor)
        if pos < 0:
            report.append("ERROR: Could not locate runner-products tab build call in main_gui.py")
        else:
            # insert a bit after the try/except block ends; simplest: insert after that anchor line
            insert_at = txt.find("\n", pos)
            if insert_at > 0:
                txt = txt[: insert_at + 1] + bind_snippet + txt[insert_at + 1 :]
                report.append("OK: inserted NotebookTabChanged bind for Artefakte auto-refresh")

    # 2) Add method in class ShrimpDevApp (before def main())
    method_snippet = """
    # R2431: Auto-refresh Artefakte tab when activated
    def _on_notebook_tab_changed(self, event=None):
        try:
            nb = getattr(self, "nb", None)
            if nb is None:
                return
            sel = nb.select()
            if not sel:
                return
            tab = nb.nametowidget(sel)

            if tab is getattr(self, "tab_runner_products", None):
                # 1) Notify via event (optional listeners)
                try:
                    tab.event_generate("<<ArtefakteRefresh>>")
                except Exception:
                    pass

                # 2) Prefer explicit refresh function if the module provides one
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

                # 3) Fallback: safe rebuild (guaranteed refresh)
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
    if "def _on_notebook_tab_changed" not in txt:
        marker = "\ndef main("
        p = txt.find(marker)
        if p > 0:
            txt = txt[:p] + method_snippet + "\n" + txt[p:]
            report.append("OK: inserted _on_notebook_tab_changed() into ShrimpDevApp")
        else:
            report.append("ERROR: Could not locate def main() to insert method")

    if txt == orig or "ERROR:" in "\n".join(report):
        rp = docs / f"Report_{RID}_ArtefakteAutoRefresh_{ts()}.md"
        write(rp, "\n".join(report + (["NO-OP: nothing changed"] if txt == orig else [])) + "\n")
        print(f"[{RID}] {'OK (NO-OP)' if txt == orig else 'ERROR'}: Report {rp}")
        return 0 if txt == orig else 3

    bk = backup(gui, archiv)
    write(gui, txt)
    report.append(f"Backup: {bk}")

    # Pipeline + keep
    patch_pipeline(root, archiv, report)
    ensure_keep(root, archiv, report)

    rp = docs / f"Report_{RID}_ArtefakteAutoRefresh_{ts()}.md"
    write(rp, "\n".join(report) + "\n")
    print(f"[{RID}] OK: Report {rp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
