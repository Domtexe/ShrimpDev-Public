# -*- coding: utf-8 -*-
from pathlib import Path
from datetime import datetime

RUNNER_ID = "R2841"

def now():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def repo_root():
    return Path(__file__).resolve().parent.parent

def main():
    repo = repo_root()
    pipe = repo / "docs" / "PIPELINE.md"
    pipe.parent.mkdir(exist_ok=True)

    entry = f"""
## ✅ Repo-Roots, Push-Buttons & Purge-Stabilisierung – DONE

**Diagnose:**
- R2834 (AST Locator)
- R2836 (Runtime Trace)
- R2838 (Whitelist Analyse)

**Fixes:**
- R2837 – Push-Buttons nur bei vorhandenen Wrappern aktiv
- R2839 – Whitelist-Hardening (stem + cmd/py + Pfade)

**Ergebnis:**
- Push-Buttons konsistent
- Wrapper werden nicht mehr purged
- Registry ist Source of Truth

**Status:** abgeschlossen
"""

    txt = pipe.read_text(encoding="utf-8", errors="replace") if pipe.exists() else ""
    if "Push-Buttons & Purge-Stabilisierung" not in txt:
        txt += "\n" + entry.strip() + "\n"
        pipe.write_text(txt, encoding="utf-8")

    rep = repo / "Reports" / f"Report_{RUNNER_ID}_{now()}.md"
    rep.write_text(f"# {RUNNER_ID}\n\nPipeline aktualisiert.\n")

    print(f"[{RUNNER_ID}] OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
