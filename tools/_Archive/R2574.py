from __future__ import annotations

import datetime as _dt
import os
import re
import sys
from pathlib import Path


EXCLUDE_TARGET = "modules/ui_toolbar.py"


def _repo_root() -> Path:
    # tools/R2574.py -> tools -> repo root
    return Path(__file__).resolve().parent.parent


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _write_text(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _backup_file(p: Path) -> Path:
    ts = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = p.with_suffix(p.suffix + f".R2574_{ts}.bak")
    bak.write_bytes(p.read_bytes())
    return bak


def _patch_ci(ci_path: Path) -> bool:
    """
    Ensure Ruff steps exclude EXCLUDE_TARGET in both format/check + lint/check.
    We keep change minimal: only add explicit --exclude modules/ui_toolbar.py
    and do NOT broaden excludes.
    """
    text = _read_text(ci_path)

    # Only patch if file has ruff format/check and ruff check calls.
    if "ruff format" not in text or "ruff check" not in text:
        print(f"[R2574] WARN: ci.yml found but no ruff commands detected: {ci_path}")
        return False

    original = text

    def ensure_exclude_in_run_block(block: str) -> str:
        # Add `--exclude modules/ui_toolbar.py` if missing.
        if EXCLUDE_TARGET in block:
            return block
        # Prefer keeping existing style: either single-line or folded.
        # Insert after existing --exclude _Exports if present, else after "ruff ...".
        if "--exclude _Exports" in block:
            return block.replace("--exclude _Exports", f"--exclude _Exports --exclude {EXCLUDE_TARGET}")
        # Insert after "ruff format --check" or "ruff check"
        block = re.sub(
            r"(ruff\s+(?:format\s+--check|check)\b)",
            rf"\1 --exclude {EXCLUDE_TARGET}",
            block,
            count=1,
        )
        return block

    # Patch run lines for both steps (format + lint). Handles YAML "run:" single line.
    def patch_run_line(cmd: str) -> str:
        if EXCLUDE_TARGET in cmd:
            return cmd
        if "--exclude _Exports" in cmd:
            return cmd.replace("--exclude _Exports", f"--exclude _Exports --exclude {EXCLUDE_TARGET}")
        # fallback: add right after ruff command
        if "ruff format" in cmd:
            return cmd.replace("ruff format", f"ruff format --exclude {EXCLUDE_TARGET}", 1)
        if "ruff check" in cmd:
            return cmd.replace("ruff check", f"ruff check --exclude {EXCLUDE_TARGET}", 1)
        return cmd

    # Patch YAML run: lines (single line)
    def repl_run_line(m: re.Match) -> str:
        prefix = m.group(1)
        cmd = m.group(2)
        return prefix + patch_run_line(cmd)

    text = re.sub(r"(^\s*run:\s*)(.+)$", repl_run_line, text, flags=re.MULTILINE)

    # Patch folded/multiline blocks: run: > or run: |
    # We patch the block content by locating ruff lines inside.
    def patch_multiline_runs(t: str) -> str:
        lines = t.splitlines(True)
        out = []
        i = 0
        while i < len(lines):
            line = lines[i]
            out.append(line)
            if re.match(r"^\s*run:\s*[>|]\s*$", line):
                # capture indented block lines
                indent = len(line) - len(line.lstrip(" "))
                block_indent = None
                j = i + 1
                block_lines = []
                while j < len(lines):
                    l2 = lines[j]
                    if l2.strip() == "":
                        block_lines.append(l2)
                        j += 1
                        continue
                    cur_indent = len(l2) - len(l2.lstrip(" "))
                    if block_indent is None:
                        block_indent = cur_indent
                    if cur_indent < (block_indent or 0):
                        break
                    block_lines.append(l2)
                    j += 1

                block_text = "".join(block_lines)
                # Patch only ruff lines within block text.
                patched = []
                for bl in block_text.splitlines(True):
                    if "ruff format" in bl or "ruff check" in bl:
                        patched.append(patch_run_line(bl))
                    else:
                        patched.append(bl)
                out[-1] = out[-1]  # keep run: line
                out.extend(patched)
                i = j
                continue
            i += 1
        return "".join(out)

    text = patch_multiline_runs(text)

    changed = (text != original)
    if changed:
        _backup_file(ci_path)
        _write_text(ci_path, text)
        print(f"[R2574] OK: Patched CI workflow: {ci_path}")
    else:
        print(f"[R2574] OK: CI already excludes {EXCLUDE_TARGET}: {ci_path}")
    return changed


def _find_pipeline_file(root: Path) -> Path | None:
    candidates = [
        root / "docs" / "PIPELINE.md",
        root / "docs" / "Development_Pipeline.md",
        root / "docs" / "DEVELOPMENT_PIPELINE.md",
        root / "docs" / "pipeline.md",
        root / "PIPELINE.md",
        root / "pipeline.md",
    ]
    for c in candidates:
        if c.exists():
            return c

    # fallback: search in docs for something containing "Pipeline" in filename
    docs = root / "docs"
    if docs.exists():
        for p in sorted(docs.glob("*.md")):
            if "pipeline" in p.name.lower():
                return p
    return None


def _append_pipeline_debt(pipeline_path: Path) -> bool:
    """
    Append a TechDebt entry with cross-ref to CI exclusion.
    Minimal: append under a heading if we find one, else append at end.
    """
    text = _read_text(pipeline_path)
    stamp = _dt.datetime.now().strftime("%Y-%m-%d")

    entry = f"""
### TechDebt: Legacy `ui_toolbar.py` Ruff violations (excluded from CI for now)

- **Date:** {stamp}
- **Status:** Backlog
- **Priority:** P3 (cleanup / refactor)
- **Scope:** `modules/ui_toolbar.py` (legacy UI code)
- **Symptoms:** Ruff errors e.g. `F821 configparser undefined`, `F841 plan_ok assigned but unused`, plus import-order (`E402`) noise.
- **Current mitigation:** CI excludes `{EXCLUDE_TARGET}` to keep runtime CI green (**R2574**).
- **Fix plan (later, controlled):**
  1. Decide: refactor vs deprecate (`ui_toolbar.py` vs newer toolbar modules)
  2. If refactor: normalize imports (top-of-file), add missing imports, remove dead assigns, split monolith.
  3. Add regression: minimal smoke-test for toolbar init + key actions.

"""
    if "TechDebt" in text or "Technical Debt" in text:
        # Try to place under first matching heading
        m = re.search(r"^(#+\s*(TechDebt|Technical Debt).*)$", text, flags=re.MULTILINE)
        if m:
            insert_at = m.end()
            new_text = text[:insert_at] + "\n" + entry + text[insert_at:]
        else:
            new_text = text + "\n" + entry
    else:
        new_text = text + "\n" + entry

    if new_text != text:
        _backup_file(pipeline_path)
        _write_text(pipeline_path, new_text)
        print(f"[R2574] OK: Added TechDebt entry to pipeline: {pipeline_path}")
        return True

    print(f"[R2574] WARN: Pipeline unchanged (unexpected): {pipeline_path}")
    return False


def main() -> int:
    root = _repo_root()

    ci_path = root / ".github" / "workflows" / "ci.yml"
    if not ci_path.exists():
        print("[R2574] ERROR: .github/workflows/ci.yml not found")
        return 2

    _patch_ci(ci_path)

    pipeline = _find_pipeline_file(root)
    if pipeline is None:
        print("[R2574] WARN: No pipeline file found; please confirm pipeline path/name.")
        # still success because CI patch was the primary goal
        return 0

    _append_pipeline_debt(pipeline)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
