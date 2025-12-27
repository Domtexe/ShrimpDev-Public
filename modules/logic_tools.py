r"""
SonderRunner-Logik - als modulare Funktionen, auf Buttons verdrahtet.
Startet vorhandene tools\Rxxxx.cmd; bei Fehlen: Statusmeldung, kein Crash.
"""

from __future__ import annotations
import os, subprocess


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
    """Run Purge Scan runner."""
    _run_cmd(app, "R2218.cmd", "Purge Scan")

def action_tools_purge_apply(app):
    """Run Purge Apply runner."""
    _run_cmd(app, "R2224.cmd", "Purge Apply")
