import shutil
from datetime import datetime
from pathlib import Path
import sys

RID = "R2428"


def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def write(p: Path, s: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8", newline="\n")


def backup(p: Path, archiv: Path):
    if not p.exists():
        return None
    archiv.mkdir(parents=True, exist_ok=True)
    b = archiv / f"{p.name}.{RID}_{ts()}.bak"
    shutil.copy2(p, b)
    return b


def main() -> int:
    tools = Path(__file__).resolve().parent
    root = tools.parent
    docs = root / "docs"
    archiv = root / "_Archiv"
    ui = root / "modules" / "ui_toolbar.py"
    reg = root / "registry"
    keep = reg / "tools_keep.txt"

    report = [f"[{RID}] UI Gate: push buttons", f"Time: {now()}", f"File: {ui}", ""]

    if not ui.exists():
        rp = docs / f"Report_{RID}_UIGate_{ts()}.md"
        write(rp, "\n".join(report + ["ERROR: ui_toolbar.py missing"]) + "\n")
        print(f"[{RID}] ERROR: Report {rp}")
        return 2

    txt = read(ui)
    start = txt.find("    # Zeile - Autopush")
    end = txt.find("    # Zeile 0 - Tools Purge (ROOT-only, keine Subfolder)")
    if start < 0 or end < 0 or start >= end:
        rp = docs / f"Report_{RID}_UIGate_{ts()}.md"
        write(rp, "\n".join(report + ["ERROR: could not locate autopush block markers"]) + "\n")
        print(f"[{RID}] ERROR: Report {rp}")
        return 3

    new_block = """    # Zeile - Autopush (Intake): Private/Public + Link Toggle (gated)
    row_push = ui_theme_classic.Frame(outer)
    row_push.pack(fill="x", pady=(0, 0))

    # Toggle (gekoppelt)
    try:
        if not hasattr(app, "_autopush_link_var"):
            app._autopush_link_var = tk.BooleanVar(value=False)
        _link_var = app._autopush_link_var
    except Exception:
        _link_var = None

    def _autopush_linked() -> bool:
        try:
            return bool(_link_var.get()) if _link_var is not None else False
        except Exception:
            return False

    # --- Busy flag comes from runner executor (R2427) ---
    def _runner_busy() -> bool:
        try:
            from . import module_runner_exec
            return bool(module_runner_exec.is_runner_busy())
        except Exception:
            return False

    # Resolve private root (where this repo lives)
    _PRIVATE_ROOT = Path(__file__).resolve().parent.parent

    def _file_exists(rel: str) -> bool:
        return (_PRIVATE_ROOT / rel).exists()

    # Public export root: no hardcode.
    # Priority:
    # 1) registry/public_export_root.txt (one line path)
    # 2) app.public_export_root (if later wired from workspace/config)
    def _public_root() -> Path | None:
        try:
            reg_file = _PRIVATE_ROOT / "registry" / "public_export_root.txt"
            if reg_file.exists():
                p = reg_file.read_text(encoding="utf-8", errors="replace").strip().strip('"')
                if p:
                    return Path(p)
        except Exception:
            pass
        try:
            p = getattr(app, "public_export_root", None)
            if p:
                return Path(str(p))
        except Exception:
            pass
        return None

    def _public_repo_ok() -> bool:
        pr = _public_root()
        return bool(pr and pr.exists() and (pr / ".git").exists())

    # SAFE scope: must be clean before Public is allowed
    _SAFE_PREFIXES = ["docs/PIPELINE.md"]

    def _private_safe_dirty() -> bool:
        import subprocess
        try:
            cp = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=str(_PRIVATE_ROOT),
                text=True,
                capture_output=True,
            )
            out = (cp.stdout or "").strip()
            if not out:
                return False
            for line in out.splitlines():
                if len(line) < 4:
                    continue
                path = line[3:].strip().replace("\\\\", "/")
                for pre in _SAFE_PREFIXES:
                    if path == pre or path.startswith(pre.rstrip("/") + "/"):
                        return True
            return False
        except Exception:
            # safe default: assume dirty -> blocks public
            return True

    # Buttons (right aligned): Private | Link | Public (Public far right)
    btn_push_public = ui_theme_classic.Button(
        row_push,
        text="Push Public",
        command=lambda: _call_logic_action(app, "action_autopush_both") if _autopush_linked() else _call_logic_action(app, "action_autopush_public"),
    )
    btn_push_public.pack(side="right", padx=(6, 0))

    try:
        chk = tk.Checkbutton(
            row_push,
            text="<--> Link",
            variable=_link_var,
        )
        chk.pack(side="right", padx=(6, 0))
    except Exception:
        pass

    btn_push_private = ui_theme_classic.Button(
        row_push,
        text="Push Private",
        command=lambda: _call_logic_action(app, "action_autopush_both") if _autopush_linked() else _call_logic_action(app, "action_autopush_private"),
    )
    btn_push_private.pack(side="right", padx=(6, 0))

    def _set_btn_state(btn, enabled: bool):
        try:
            btn.configure(state=("normal" if enabled else "disabled"))
        except Exception:
            try:
                btn["state"] = ("normal" if enabled else "disabled")
            except Exception:
                pass

    def _update_push_states():
        busy = _runner_busy()

        has_r2412 = _file_exists("tools/R2691.cmd")
        has_r2411 = _file_exists("tools/R2692.cmd")
        has_r2414 = _file_exists("tools/R2414.cmd")

        private_ok = has_r2412 and (not busy)

        # Order enforcement: Public allowed only when SAFE scope is clean
        safe_clean = (not _private_safe_dirty())

        public_ok = has_r2411 and _public_repo_ok() and safe_clean and (not busy)

        if _autopush_linked():
            both_ok = has_r2414 and has_r2412 and has_r2411 and _public_repo_ok() and safe_clean and (not busy)
            _set_btn_state(btn_push_private, both_ok)
            _set_btn_state(btn_push_public, both_ok)
        else:
            _set_btn_state(btn_push_private, private_ok)
            _set_btn_state(btn_push_public, public_ok)

        try:
            row_push.after(1200, _update_push_states)
        except Exception:
            pass

    _update_push_states()
"""

    b = backup(ui, archiv)
    patched = txt[:start] + new_block + "\n\n" + txt[end:]
    write(ui, patched)

    # Ensure purge whitelist protects this runner too
    if keep.exists():
        keep_txt = read(keep).splitlines()
        items = [ln.strip() for ln in keep_txt if ln.strip() and not ln.strip().startswith("#")]
        if "R2428" not in items:
            backup(keep, archiv)
            write(keep, read(keep).rstrip() + "\nR2428\n")

    rp = docs / f"Report_{RID}_UIGate_{ts()}.md"
    write(
        rp,
        "\n".join(
            report
            + [
                "OK: autopush block replaced with gated logic (busy/order/path)",
                "Notes:",
                "- Public export root is read from registry/public_export_root.txt or app.public_export_root",
                "- Public disabled if safe docs are dirty or public repo not configured",
                f"Backup: {b}",
            ]
        )
        + "\n",
    )
    print(f"[{RID}] OK: Report {rp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
