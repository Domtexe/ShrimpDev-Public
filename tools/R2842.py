# -*- coding: utf-8 -*-
from pathlib import Path
from datetime import datetime

RUNNER_ID = "R2842"

def now():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def repo_root():
    return Path(__file__).resolve().parent.parent

def main():
    repo = repo_root()
    doc = repo / "docs" / "Push_Purge_System.md"
    doc.parent.mkdir(exist_ok=True)

    content = f"""
# Push- & Purge-System – Technische Übersicht

## Push-Workflow
- UI aktiviert Push-Buttons nur bei:
  - gültigem Repo-Root
  - existierendem Wrapper (`R2691.cmd` / `R2692.cmd`)
- Ausführung erfolgt ausschließlich über Wrapper.

## Purge-System
- Grundlage: R2218 / R2224
- Schutzdateien:
  - registry/runner_whitelist.txt
  - registry/tools_keep.txt
- Whitelist wirkt stem-basiert (`R####`)
- Erweiterung durch R2839 stellt robusten Schutz sicher.

## Fehlerszenarien
- Wrapper fehlt → Button disabled
- Whitelist greift nicht → Diagnose R2838

Stand: {now()}
"""
    doc.write_text(content.strip() + "\n", encoding="utf-8")

    rep = repo / "Reports" / f"Report_{RUNNER_ID}_{now()}.md"
    rep.write_text(f"# {RUNNER_ID}\n\nTechnische Doku erstellt.\n")

    print(f"[{RUNNER_ID}] OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
