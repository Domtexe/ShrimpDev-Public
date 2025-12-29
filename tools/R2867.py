from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path
import sys

IDENT_RE = re.compile(r"\{([^{}]+)\}")
ASSIGN_RE = re.compile(r"^\s*([A-Za-z_]\w*)\s*=")
DEF_RE = re.compile(r"^\s*def\s+([A-Za-z_]\w*)\s*\((.*?)\)\s*:")

PY_SKIP_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "_Archiv", "_Archive", "_OldStuff", "_Backups", "node_modules"
}

SAFE_NAMES = {
    # builtins-ish / common
    "True", "False", "None", "len", "str", "int", "float", "bool", "min", "max",
}


def _ts() -> str:
    return _dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def _write_report(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")


def _iter_py_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for p in root.rglob("*.py"):
        parts = {pp.name for pp in p.parents}
        if parts & PY_SKIP_DIRS:
            continue
        out.append(p)
    return out


def _extract_expr_idents(expr: str) -> set[str]:
    # very light heuristic: pull bare identifiers
    # e.g. "name", "obj.attr" -> "obj"; "foo(bar)" -> "foo","bar"
    ids = set(re.findall(r"\b([A-Za-z_]\w*)\b", expr))
    # remove obvious keywords
    for kw in ("and", "or", "not", "in", "is", "if", "else", "for", "lambda"):
        ids.discard(kw)
    return ids


def main(root: Path) -> int:
    reports_dir = root / "Reports"
    report_path = reports_dir / f"Report_R2867_{_ts()}.md"

    hits: list[tuple[Path, int, str, str]] = []  # file, line, func, missing_names

    for py in _iter_py_files(root):
        try:
            lines = py.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue

        current_func = None
        func_indent = None
        params: set[str] = set()
        assigned: set[str] = set()

        for i, line in enumerate(lines, start=1):
            mdef = DEF_RE.match(line)
            if mdef:
                current_func = mdef.group(1)
                func_indent = len(line) - len(line.lstrip(" "))
                raw_params = mdef.group(2).strip()
                params = set()
                assigned = set()

                if raw_params:
                    for p in raw_params.split(","):
                        p = p.strip()
                        if not p:
                            continue
                        p = p.split("=")[0].strip()
                        p = p.lstrip("*").strip()
                        if p:
                            params.add(p)
                continue

            if current_func is not None:
                # leaving function block?
                if line.strip() and (len(line) - len(line.lstrip(" "))) <= (func_indent or 0) and not line.lstrip().startswith(("#", "@")):
                    current_func = None
                    func_indent = None
                    params = set()
                    assigned = set()
                    continue

                mass = ASSIGN_RE.match(line)
                if mass:
                    assigned.add(mass.group(1))

                # heuristic: only look at f-strings in code lines
                if "f\"" in line or "f'" in line:
                    exprs = IDENT_RE.findall(line)
                    used: set[str] = set()
                    for ex in exprs:
                        used |= _extract_expr_idents(ex)

                    # ignore safe/common + attribute-only usage base objects must exist
                    used -= SAFE_NAMES

                    missing = {u for u in used if u not in params and u not in assigned}
                    # common false positives: "self" should exist in methods
                    if "self" in params:
                        missing.discard("self")

                    if missing:
                        hits.append((py, i, current_func or "?", ", ".join(sorted(missing))))

    report = [
        "# Report R2867 — Lint-Guard f-string unknown identifiers",
        f"- Time: {_dt.datetime.now().isoformat(timespec='seconds')}",
        f"- Root: `{root.as_posix()}`",
        "",
        "## Heuristic",
        "- Scans function blocks, collects parameters + simple assignments (`x = ...`).",
        "- Flags f-strings that reference identifiers not in params/assignments.",
        "",
        "## Hits",
    ]

    if not hits:
        report.append("- None ✅")
        _write_report(report_path, report)
        return 0

    for (py, ln, fn, miss) in hits[:250]:
        report.append(f"- `{py.as_posix()}`:{ln} in `{fn}()` — missing: **{miss}**")

    if len(hits) > 250:
        report.append(f"\n… truncated ({len(hits)} total hits).")

    _write_report(report_path, report)
    return 11


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: R2867.py <repo_root>", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(Path(sys.argv[1]).resolve()))
