from __future__ import annotations

from pathlib import Path
import shutil
import datetime as dt
import sys

EXIT_OK = 0
EXIT_FAIL = 11

MR_MARKER = "MR_FSTRING_SAFETY"
PIPE_MARKER = "PIPE_GUARD_R2867"

def ts():
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(p: Path, root: Path) -> Path:
    bdir = root / "_Backups" / "R2868"
    bdir.mkdir(parents=True, exist_ok=True)
    bak = bdir / f"{p.name}.{ts()}.bak"
    shutil.copy2(p, bak)
    return bak

def write_report(root: Path, lines: list[str]):
    rdir = root / "Reports"
    rdir.mkdir(parents=True, exist_ok=True)
    rp = rdir / f"Report_R2868_{ts()}.md"
    rp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return rp

def patch_masterrules(p: Path) -> bool:
    txt = p.read_text(encoding="utf-8")
    if MR_MARKER in txt:
        return False

    block = f"""## Code Safety – f-Strings  <!-- {MR_MARKER} -->

**Regel:**
In Produktiv-Code dürfen f-Strings **keine Namen verwenden**, die nicht
- Funktionsparameter **oder**
- zuvor lokal zugewiesene Variablen
sind.

**Begründung:**
f-Strings werden zur Laufzeit ausgewertet. Nicht existente Namen führen
zu **Runtime-Crashes (NameError)**, insbesondere in GUI-Callbacks.

**Beispiele (verboten):**
```python
log(f"state={{name}}")  # name nicht definiert
```

**Erlaubt:**
```python
def foo(name):
    log(f"state={{name}}")
```

oder

```python
name = btn_name
log(f"state={{name}}")
```

**Durchsetzung:**
- READ-ONLY Guard `R2867`
- manuell vor Refactors & UI-Patches
"""
    p.write_text(txt.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
    return True

def patch_pipeline(p: Path) -> bool:
    txt = p.read_text(encoding="utf-8")
    if PIPE_MARKER in txt:
        return False

    block = f"""### R2867 – f-String Safety Guard  <!-- {PIPE_MARKER} -->

- Typ: READ-ONLY Diagnose / Safety-Guard
- Zweck: Finden von f-Strings mit nicht definierten Namen
- Exit-Code:
  - `0` → keine Treffer
  - `11` → Treffer vorhanden (kein Fehler, sondern Warnsignal)
- Einsatz:
  - vor größeren Refactors
  - nach UI- oder Callback-Patches
  - **nicht CI-blockierend**
"""
    p.write_text(txt.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")
    return True

def main(root: Path) -> int:
    mr = root / "docs" / "MasterRules.md"
    pl = root / "docs" / "PIPELINE.md"

    report = [
        "# Report R2868 – Rules & Pipeline Update",
        f"- Time: {dt.datetime.now().isoformat(timespec='seconds')}",
        f"- Root: `{root}`",
        ""
    ]

    if not mr.exists() or not pl.exists():
        report.append("ERROR: Ziel-Dateien nicht gefunden")
        write_report(root, report)
        return EXIT_FAIL

    bak_mr = backup(mr, root)
    bak_pl = backup(pl, root)

    changed_mr = patch_masterrules(mr)
    changed_pl = patch_pipeline(pl)

    report += [
        "## Ergebnisse",
        f"- MasterRules geändert: **{changed_mr}**",
        f"- Pipeline geändert: **{changed_pl}**",
        "",
        "## Backups",
        f"- {bak_mr}",
        f"- {bak_pl}",
    ]

    write_report(root, report)
    return EXIT_OK

if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve()
    sys.exit(main(root))
