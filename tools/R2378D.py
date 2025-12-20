# R2378D - READ-ONLY INI + Docking Diagnose (no writes)
# - Reads ShrimpDev.ini and reports window states (main/log/pipeline/runner_products)
# - Checks consistency + offscreen risk for single monitor
# - Scans project for INI write entry points (open(...,'w'), config.write, etc.)
# - Writes ONLY a report file under docs/ (allowed read-only diagnosis artifact)
#   -> If you prefer ZERO file writes at all, set WRITE_REPORT = False.

import os
import re
import sys
import configparser
from datetime import datetime
from pathlib import Path

RID = "R2378D"
WRITE_REPORT = True  # set False if you want stdout only (absolutely no files)

WINDOW_KEYS = ["main", "runner_products", "log", "pipeline"]

def now_ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def project_root() -> Path:
    return Path(__file__).resolve().parent.parent

def read_ini(path: Path) -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    cfg.read(path, encoding="utf-8")
    return cfg

_geo_re = re.compile(r"^\s*(\d+)x(\d+)\+(-?\d+)\+(-?\d+)\s*$")

def parse_geo(s: str):
    m = _geo_re.match((s or "").strip())
    if not m:
        return None
    w, h, x, y = map(int, m.groups())
    return w, h, x, y

def offscreen_single_monitor(w, h, x, y, sw, sh) -> bool:
    # Conservative: window must overlap screen by at least 50px in both axes
    # to be considered "onscreen enough"
    min_overlap = 50
    x2 = x + w
    y2 = y + h
    overlap_w = min(x2, sw) - max(x, 0)
    overlap_h = min(y2, sh) - max(y, 0)
    return overlap_w < min_overlap or overlap_h < min_overlap

def find_screen_size_guess(cfg: configparser.ConfigParser):
    # We don't know runtime screen size here.
    # Use common single-monitor defaults. Report remains a "risk check".
    # You can adjust to your real resolution if desired.
    sw = 1920
    sh = 1080
    return sw, sh

def cfg_get(cfg, sec, key, default=""):
    try:
        return cfg.get(sec, key, fallback=default)
    except Exception:
        return default

def scan_write_points(root: Path):
    """
    Very practical scan: find lines that likely write config/ini files.
    We don't try to be perfect; we want a shortlist of suspects.
    """
    patterns = [
        ("open_write", re.compile(r"open\([^)]*,\s*['\"]w['\"]")),
        ("Path_open_write", re.compile(r"\.open\(\s*['\"]w['\"]")),
        ("config_write", re.compile(r"\.write\(\s*f\s*\)")),
        ("cfg_write", re.compile(r"config\.write\(")),
        ("ConfigParser_write", re.compile(r"ConfigParser\(\).*\.write\(")),
    ]
    hits = []
    exts = {".py", ".cmd", ".bat"}
    for p in root.rglob("*"):
        if p.suffix.lower() not in exts:
            continue
        # Skip archives / virtualenv / caches if present
        sp = str(p).lower()
        if any(x in sp for x in ["\\_archiv\\", "\\.venv\\", "\\venv\\", "\\__pycache__\\", "\\_snapshots\\"]):
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        lines = txt.splitlines()
        for i, line in enumerate(lines, start=1):
            for tag, rx in patterns:
                if rx.search(line):
                    hits.append((tag, str(p), i, line.strip()))
    return hits

def main():
    root = project_root()
    ini_path = root / "ShrimpDev.ini"
    docs_dir = root / "docs"
    docs_dir.mkdir(exist_ok=True)

    out = []
    out.append(f"# {RID} – READ-ONLY Docking/INI Diagnose")
    out.append("")
    out.append(f"- Zeit: {now_ts()}")
    out.append(f"- Projekt-Root: {root}")
    out.append(f"- INI: {ini_path}")
    out.append("")

    if not ini_path.exists():
        out.append("## FEHLER")
        out.append("ShrimpDev.ini nicht gefunden.")
        print("\n".join(out))
        return 2

    cfg = read_ini(ini_path)
    sec = "Docking"
    if not cfg.has_section(sec):
        out.append("## WARN")
        out.append("Section [Docking] fehlt in ShrimpDev.ini.")
        out.append("")
    keys_raw = cfg_get(cfg, sec, "keys", "")
    keys_list = [k.strip() for k in keys_raw.split(",") if k.strip()]

    out.append("## [Docking] – Keys")
    out.append(f"- keys (raw): `{keys_raw}`")
    out.append(f"- keys (list): `{', '.join(keys_list) if keys_list else '(leer)'}`")
    out.append("")

    sw, sh = find_screen_size_guess(cfg)
    out.append("## Screen-Check (Single-Monitor Risikoabschätzung)")
    out.append(f"- angenommene Screen-Size: {sw}x{sh} (nur für Offscreen-Risiko)")
    out.append("")

    out.append("## Fenster-Datensätze (pro Key)")
    for k in WINDOW_KEYS:
        open_v = cfg_get(cfg, sec, f"{k}.open", "")
        docked_v = cfg_get(cfg, sec, f"{k}.docked", "")
        geo_v = cfg_get(cfg, sec, f"{k}.geometry", "")
        ts_v = cfg_get(cfg, sec, f"{k}.ts", "")
        w_v = cfg_get(cfg, sec, f"{k}.w", "")
        h_v = cfg_get(cfg, sec, f"{k}.h", "")
        x_v = cfg_get(cfg, sec, f"{k}.x", "")
        y_v = cfg_get(cfg, sec, f"{k}.y", "")

        out.append(f"### `{k}`")
        out.append(f"- open: `{open_v}` | docked: `{docked_v}` | ts: `{ts_v}`")
        out.append(f"- geometry: `{geo_v}`")
        out.append(f"- w/h/x/y: `{w_v}/{h_v}/{x_v}/{y_v}`")

        geo = parse_geo(geo_v)
        if geo:
            ww, hh, xx, yy = geo
            off = offscreen_single_monitor(ww, hh, xx, yy, sw, sh)
            out.append(f"- parsed: w={ww}, h={hh}, x={xx}, y={yy}")
            out.append(f"- offscreen-risk: `{'YES' if off else 'NO'}`")
        else:
            out.append("- parsed: `n/a`")

        # Consistency warnings
        warns = []
        if open_v not in ("", "0", "1"):
            warns.append("open ist nicht 0/1")
        if docked_v not in ("", "0", "1"):
            warns.append("docked ist nicht 0/1")
        if open_v == "1" and not geo_v:
            warns.append("open=1 aber geometry fehlt")
        if geo_v and (w_v or h_v or x_v or y_v):
            # not an error, but signals dual-sources still present
            warns.append("geometry + w/h/x/y gleichzeitig gesetzt (Dual-Source)")
        if k not in keys_list and open_v == "1":
            warns.append("open=1 aber key ist nicht in keys-Liste")
        if warns:
            out.append(f"- WARN: {', '.join(warns)}")
        out.append("")

    # Code writepoints
    out.append("## INI/Config Write-Entry-Points (Code Scan – Shortlist)")
    hits = scan_write_points(root)
    out.append(f"- Treffer: {len(hits)}")
    out.append("")
    # show top 80 hits only to keep readable
    for idx, (tag, path, line_no, line) in enumerate(hits[:80], start=1):
        out.append(f"{idx}. `{tag}` – {path}:{line_no} – `{line}`")
    if len(hits) > 80:
        out.append("")
        out.append(f"... ({len(hits) - 80} weitere Treffer im Projekt)")
    out.append("")

    # Conclusion hints
    out.append("## Fazit (was dieses Report objektiv zeigt)")
    out.append("- Ob [Docking] überhaupt vollständig ist (pro Fenster 1 Datensatz).")
    out.append("- Ob Dual-Sources aktiv sind (geometry UND w/h/x/y).")
    out.append("- Ob open=1 ohne keys-Eintrag vorkommt.")
    out.append("- Welche Dateien potentiell INI/Config schreiben (Shortlist).")

    text = "\n".join(out)
    print(text)

    if WRITE_REPORT:
        rep = docs_dir / f"Report_{RID}_INI_Docking_ReadOnly_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        rep.write_text(text, encoding="utf-8")
        log_line = f"[{RID}] Report geschrieben: {rep}"
        print(log_line)

    return 0

if __name__ == "__main__":
    sys.exit(main())
