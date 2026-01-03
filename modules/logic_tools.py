r"""
SonderRunner-Logik - als modulare Funktionen, auf Buttons verdrahtet.
Startet vorhandene tools\Rxxxx.cmd; bei Fehlen: Statusmeldung, kein Crash.
"""

from __future__ import annotations
import os, subprocess


# R2802_AFTER_RUN_HOOK
# R2805_AFTER_RUN_HOOK
def _after_runner_show_report(app, runner_id: str, md_path: str, title: str):
    """Standard UI hook: show the newest runner report in popup (deterministic).

    Preferred source:
      - Reports/Report_<runner_id>_*.md (then .txt)
      - Reports/<runner_id>*.txt (legacy)
    Fallback:
      - md_path content
    """
    txt = None
    try:
        from pathlib import Path as _P
        import os as _os

        root = _P(__file__).resolve().parent.parent
        reports = root / "Reports"

        rid = str(runner_id).strip()
        if not rid.upper().startswith("R"):
            rid = "R" + rid

        digits = "".join([c for c in rid if c.isdigit()])

        candidates = []
        if reports.exists():
            # canonical reports (preferred)
            candidates += list(reports.glob(f"Report_{rid}_*.md"))
            candidates += list(reports.glob(f"Report_{rid}_*.txt"))
            if digits:
                candidates += list(reports.glob(f"Report_R{digits}_*.md"))
                candidates += list(reports.glob(f"Report_R{digits}_*.txt"))

            # legacy txt outputs (fallback)
            candidates += list(reports.glob(f"{rid}_*.txt"))
            candidates += list(reports.glob(f"{rid}*.txt"))
            if digits:
                candidates += list(reports.glob(f"R{digits}_*.txt"))
                candidates += list(reports.glob(f"R{digits}*.txt"))

        if candidates:
            newest = max(candidates, key=lambda p: p.stat().st_mtime)
            txt = newest.read_text(encoding="utf-8", errors="replace")
            txt = f"[{rid}] REPORT FILE: {newest}\n\n" + txt
        else:
            if md_path and isinstance(md_path, str) and _os.path.isfile(md_path):
                txt = open(md_path, "r", encoding="utf-8", errors="replace").read()
            else:
                txt = str(md_path)

    except Exception as _exc:
        try:
            txt = str(md_path)
        except Exception:
            txt = f"(no report text; error={_exc})"

    try:
        from modules import logic_actions
        logic_actions._r1851_show_popup(app, title, txt, runner_id)
    except Exception as _exc:
        try:
            print(f"[R2805] WARN: popup failed: {_exc}")
        except Exception:
            pass
# R2805_AFTER_RUN_HOOK_END
# R2802_AFTER_RUN_HOOK_END


def _tools_dir(app) -> str:
    # robust relativ zum Projekt
    here = os.path.dirname(os.path.dirname(__file__))
    return os.path.normpath(os.path.join(here, "tools"))


def _run_cmd(app, filename: str, title: str):
    path = os.path.join(_tools_dir(app), filename)
    if not os.path.exists(path):
        try:
            app.set_status(f"{title}: {filename} nicht gefunden.")
        except Exception:
            pass
        return
    try:
        subprocess.Popen([path], cwd=os.path.dirname(path), shell=True)
        try:
            app.set_status(f"{title} gestartet.")
        except Exception:
            pass
    except Exception as e:
        try:
            app.set_status(f"{title}: Fehler: {e}")
        except Exception:
            pass


def tool_futurefix(app):
    _run_cmd(app, "R9997.cmd", "FutureFix")


def tool_futurefix_safe(app):
    _run_cmd(app, "R1351.cmd", "FutureFix Safe")


def tool_learningjournal(app):
    _run_cmd(app, "R1252.cmd", "LearningJournal")


def tool_activate(app):
    _run_cmd(app, "Activate.cmd", "Activate")


def tool_r9998(app):
    _run_cmd(app, "R9998.cmd", "R9998")


def tool_r9999(app):
    _run_cmd(app, "R9999.cmd", "R9999")


def tool_masterrules_guard(app):
    """Startet den MasterRulesGuard (R1922)."""
    _run_cmd(app, "R1922.cmd", "MasterRulesGuard")
# --- Toolbar actions (Purge) ---
def action_tools_purge_scan(app):
    """Run Purge Scan via tools runner. Popup is shown ONLY by logic_actions."""
    from modules import logic_actions
    return logic_actions._r1851_run_tools_runner(app, "R2218", "Purge Scan")

def action_tools_purge_apply(app):
    """Run Purge Apply via tools runner. Popup is shown ONLY by logic_actions."""
    from modules import logic_actions
    return logic_actions._r1851_run_tools_runner(app, "R2224", "Purge Apply")

def _r2787_latest_matching_file(dir_path, prefix: str, suffix: str):
    try:
        import os
        if not os.path.isdir(dir_path):
            return None
        best = None
        best_m = -1.0
        for name in os.listdir(dir_path):
            if not (name.startswith(prefix) and name.endswith(suffix)):
                continue
            p = os.path.join(dir_path, name)
            try:
                m = os.path.getmtime(p)
            except Exception:
                continue
            if m > best_m:
                best_m = m
                best = p
        return best
    except Exception:
        return None

def _r2787_write_runner_md_report(app, runner_id: str, title: str, txt_report_path: str, plan_path: str = ""):
    # Create Reports/Report_R####_*.md so logic_actions._r1851_show_popup can display it.
    try:
        from pathlib import Path
        root = Path(__file__).resolve().parent.parent
        reports_dir = root / "Reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        stamp = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
        md = reports_dir / f"Report_{runner_id}_{stamp}.md"

        lines = []
        lines.append(f"# {title}")
        lines.append("")
        lines.append(f"- Runner: **{runner_id}**")
        if plan_path:
            lines.append(f"- Plan: `{plan_path}`")
        if txt_report_path:
            lines.append(f"- Report TXT: `{txt_report_path}`")
        lines.append("")
        lines.append("## Hinweis")
        lines.append("Dieser Report ist ein Bridge-Wrapper, damit das Standard-Report-Popup (r1851) den Purge-Output anzeigen kann.")
        lines.append("")
        lines.append("## Inhalt (TXT)")
        lines.append("")
        if txt_report_path:
            try:
                p = Path(txt_report_path)
                if p.exists():
                    txt = p.read_text(encoding="utf-8", errors="replace")
                    lines.append("```text")
                    lines.append(txt.strip())
                    lines.append("```")
                else:
                    lines.append("_TXT-Datei nicht gefunden._")
            except Exception as e:
                lines.append(f"_Fehler beim Lesen der TXT: {e}_")

        md.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return str(md)
    except Exception:
        return ""

# -------------------------------------------------------------------------
