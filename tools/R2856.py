# -*- coding: utf-8 -*-
"""
R2856 – PATCH: Learnings / Regeln / Nutzen sichern

- Ergänzt docs/Master/MasterRules.md um verbindliche CI-Regeln
- Erstellt/aktualisiert docs/Guides/CI_Workflow.md
- Backup + Report + Rollback bei Fehlern (MR-konform)
"""

from __future__ import annotations

import shutil
from pathlib import Path
from datetime import datetime
from typing import List

RUNNER_ID = "R2856"
EXIT_FAIL = 11


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def backup(repo: Path, target: Path) -> Path:
    arch = repo / "_Archiv"
    ensure_dir(arch)
    bak = arch / f"{target.name}.{RUNNER_ID}_{now_stamp()}.bak"
    shutil.copy2(target, bak)
    return bak


def write_report(repo: Path, lines: List[str]) -> Path:
    rp = repo / "Reports"
    ensure_dir(rp)
    out = rp / f"Report_{RUNNER_ID}_{now_stamp()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")
    return out


def append_if_missing(path: Path, marker: str, block: str) -> bool:
    txt = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    if marker in txt:
        return False
    new_txt = (txt.rstrip() + "\n\n" + block.strip() + "\n") if txt.strip() else (block.strip() + "\n")
    path.write_text(new_txt, encoding="utf-8", errors="replace")
    return True


def main(root_arg: str) -> int:
    repo = Path(root_arg).resolve()
    report: List[str] = []
    report.append(f"# {RUNNER_ID} PATCH: Learnings / Regeln / Nutzen")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: `{repo}`")
    report.append("")

    mr = repo / "docs" / "Master" / "MasterRules.md"
    if not mr.exists():
        report.append(f"ERROR: Missing `{mr}`")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return EXIT_FAIL

    guide = repo / "docs" / "Guides" / "CI_Workflow.md"
    ensure_dir(guide.parent)

    bak_mr = backup(repo, mr)
    report.append(f"- MasterRules backup: `{bak_mr}`")

    if guide.exists():
        bak_g = backup(repo, guide)
        report.append(f"- CI guide backup: `{bak_g}`")
    report.append("")

    try:
        mr_marker = "## ✅ CI-Regeln (Workflow, Public-Mirror, Syntax-Gate)"
        mr_block = f"""
{mr_marker}

- **Workflow-YAML:** Jeder `steps:`-Eintrag ist **ein** Mapping. `name`, `uses`, `with`, `run` gehören in **denselben** Block.
- **Public-Mirror-sicher:** CI darf keine Dateien hart voraussetzen, die im Public-Export fehlen können (z. B. `main_gui.py`).
- **Syntax-Gate verpflichtend:** CI muss `py_compile` / `compileall` ausführen, um echte Syntaxfehler früh zu erkennen.
- **Nutzen:** Ehrliche CI – findet echte Fehler ohne False Positives.
- **Rollback:** Bei CI-/Workflow-Fails sofort auf Backup zurückrollen.
"""
        changed_mr = append_if_missing(mr, mr_marker, mr_block)

        guide_marker = "# CI Workflow (ShrimpDev)"
        guide_block = f"""
{guide_marker}

Stand: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Ziele
- Valides YAML
- Frühe Fehlererkennung (Syntax)
- Public-Mirror-kompatibel

## Richtiger Step-Aufbau
```yaml
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.11"
```

## Guards für Public-Repos
```bash
if [ -f main_gui.py ]; then python -m py_compile main_gui.py; fi
```

## Minimaler Syntax-Gate
```bash
python -m compileall -q modules
python -m compileall -q tools
```
"""
        changed_guide = append_if_missing(guide, guide_marker, guide_block)

        report.append("## Changes")
        report.append(f"- MasterRules updated: {changed_mr}")
        report.append(f"- CI guide updated/created: {changed_guide}")

        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] OK -> {rp}")
        return 0

    except Exception as e:
        try:
            shutil.copy2(bak_mr, mr)
        except Exception:
            pass
        report.append(f"ERROR: Exception during patch: {type(e).__name__}: {e}")
        report.append("Rollback: MasterRules restored from backup.")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return EXIT_FAIL


if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parents[1])
    raise SystemExit(main(root))
