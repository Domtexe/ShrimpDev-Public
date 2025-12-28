from __future__ import annotations

import datetime as _dt
import os
from pathlib import Path


def _now_stamp() -> str:
    return _dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def _backup(path: Path, tag: str) -> Path:
    ts = _now_stamp()
    bak = path.with_suffix(path.suffix + f".{tag}_{ts}.bak")
    bak.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return bak


def _ensure_section(
    text: str,
    header: str,
    body: str,
) -> str:
    """
    Insert section if missing.
    Strategy: if header exists -> no-op, else append at end with spacing.
    """
    if header in text:
        return text
    sep = "\n" if text.endswith("\n") else "\n\n"
    return text + sep + header + "\n\n" + body.strip() + "\n"


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    docs = root / "docs"
    reports = root / "Reports"
    reports.mkdir(exist_ok=True)

    dev_rules = docs / "DEVELOPMENT_RULES.md"
    arch = docs / "ARCHITECTURE.md"

    if not dev_rules.exists():
        print(f"[R2570] ERROR: missing {dev_rules}")
        return 2
    if not arch.exists():
        print(f"[R2570] ERROR: missing {arch}")
        return 2

    _backup(dev_rules, "R2570")
    _backup(arch, "R2570")

    # --- Canonical rules (DEVELOPMENT_RULES.md)
    rules_header = "## CI & Ruff – Scope (Runtime-only)"
    rules_body = """
**Ziel:** CI soll Stabilität erzwingen, ohne Legacy-/Learning-Artefakte (Runner/Tools) zu blockieren.

### Hard Rules
1. **CI Scope = Runtime-Code**
   - **IN:** `modules/`, `main_gui.py` (ggf. weitere Runtime-Entrypoints nach expliziter Entscheidung)
   - **OUT:** `tools/` (Runner/Legacy/Learning) und `_Exports/` (Artefakte)

2. **Kein Format-Zwang für alte Runner**
   - Historische/experimentelle Runner in `tools/` dürfen unformatiert sein.
   - Format/Style in `tools/` ist optional und darf nicht CI-breaken.

3. **Wenn CI rot wird**
   - **Erst Scope prüfen** (checkt CI aus Versehen `tools/`?),
   - dann erst Code anfassen.

### Implementation (GitHub Actions)
Empfohlene Targets (statt fragile `--exclude`-Listen):
- `uvx ruff format --check modules main_gui.py`
- `uvx ruff check modules main_gui.py`
"""
    dev_text = dev_rules.read_text(encoding="utf-8")
    dev_text2 = _ensure_section(dev_text, rules_header, rules_body)
    if dev_text2 != dev_text:
        dev_rules.write_text(dev_text2, encoding="utf-8")

    # --- Architecture cross-reference (ARCHITECTURE.md)
    arch_header = "## CI & Style"
    arch_body = """
CI ist bewusst **runtime-fokussiert** (Stabilität der App), während `tools/` als **Learning-/Runner-Sandbox** gilt.

**Kanonische Regeln:** siehe `docs/DEVELOPMENT_RULES.md` → Abschnitt **“CI & Ruff – Scope (Runtime-only)”**.
"""
    arch_text = arch.read_text(encoding="utf-8")
    arch_text2 = _ensure_section(arch_text, arch_header, arch_body)
    if arch_text2 != arch_text:
        arch.write_text(arch_text2, encoding="utf-8")

    # Report (local, ignored by git)
    report_path = reports / f"Report_R2570_{_now_stamp()}.md"
    report_path.write_text(
        "\n".join(
            [
                "# R2570 Report",
                "",
                f"- Root: `{root}`",
                f"- Updated: `{dev_rules}`",
                f"- Updated: `{arch}`",
                "",
                "## Notes",
                "- DEVELOPMENT_RULES.md is canonical for CI/ruff scope.",
                "- ARCHITECTURE.md contains a short cross-reference only.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"[R2570] OK: Updated docs + wrote report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
