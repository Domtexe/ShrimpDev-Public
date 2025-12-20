from __future__ import annotations

from pathlib import Path
from datetime import datetime
import configparser

RID = "R2407"
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INI = ROOT / "ShrimpDev.ini"

KEYS = ["main", "pipeline", "runner_products", "log"]

def ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def _read_ini() -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    cfg.read(INI, encoding="utf-8")
    return cfg

def main() -> int:
    lines = []
    lines.append(f"# Report {RID} – Docking Start State Audit (READ-ONLY)")
    lines.append("")
    lines.append(f"- Timestamp: {ts()}")
    lines.append(f"- Root: `{ROOT}`")
    lines.append(f"- INI: `{INI}`")
    lines.append("")

    cfg = _read_ini()
    has = cfg.has_section("Docking")
    lines.append(f"## INI [Docking]")
    lines.append(f"- present: **{has}**")
    lines.append("")
    if has:
        for k in KEYS:
            open_v = cfg.get("Docking", f"{k}.open", fallback="").strip()
            docked_v = cfg.get("Docking", f"{k}.docked", fallback="").strip()
            geo_v = cfg.get("Docking", f"{k}.geometry", fallback="").strip()
            ts_v = cfg.get("Docking", f"{k}.ts", fallback="").strip()
            lines.append(f"- {k}: open=`{open_v}` docked=`{docked_v}` geo=`{geo_v}` ts=`{ts_v}`")
    lines.append("")

    lines.append("## Runtime Audit Notes")
    lines.append("- Dieser Runner ist READ-ONLY und liest nur die INI.")
    lines.append("- Für den Runtime-Teil (existierende Fenster im _dock_manager) brauchen wir einen App-Hook beim Start.")
    lines.append("")
    lines.append("## Next")
    lines.append("- Wenn Fenster trotz korrekt gesetzter INI zentrieren: dann kommt ein Start-Hook in main_gui.py, der direkt nach DockManager.restore_from_ini() einen Log-Dump schreibt (R2408).")
    lines.append("")

    out = DOCS / f"Report_{RID}_DockingStartState_{stamp()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"[{RID}] OK: Report {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
