# -*- coding: utf-8 -*-
from __future__ import annotations

import ast
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Tuple


RUNNER_ID = "R2834"


def now() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def write_report(repo: Path, lines: List[str]) -> Path:
    rp = repo / "Reports"
    ensure_dir(rp)
    out = rp / f"Report_{RUNNER_ID}_{now()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")
    return out


class Locator(ast.NodeVisitor):
    def __init__(self) -> None:
        self.stack: List[str] = []
        self.found: List[Tuple[str, int, int]] = []  # (qname, lineno, end_lineno)

    def _qname(self, name: str) -> str:
        if not self.stack:
            return name
        return ".".join(self.stack + [name])

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        qn = self._qname(node.name)
        if node.name == "_resolve_repo_path":
            lineno = getattr(node, "lineno", -1)
            end_lineno = getattr(node, "end_lineno", -1)
            self.found.append((qn, lineno, end_lineno))
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        # just in case
        qn = self._qname(node.name)
        if node.name == "_resolve_repo_path":
            lineno = getattr(node, "lineno", -1)
            end_lineno = getattr(node, "end_lineno", -1)
            self.found.append((qn, lineno, end_lineno))
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()


def main() -> int:
    repo = repo_root()
    ui = repo / "modules" / "ui_toolbar.py"

    report: List[str] = []
    report.append(f"# {RUNNER_ID} READ-ONLY: AST Locate _resolve_repo_path")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: `{repo}`")
    report.append("")

    if not ui.exists():
        report.append("ERROR: modules/ui_toolbar.py not found")
        write_report(repo, report)
        return 11

    text = ui.read_text(encoding="utf-8", errors="replace")

    try:
        tree = ast.parse(text)
    except Exception as exc:
        report.append("ERROR: ast.parse failed (ui_toolbar.py is not syntactically valid right now)")
        report.append(f"- Exception: {repr(exc)}")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return 11

    loc = Locator()
    loc.visit(tree)

    report.append("## Results")
    report.append("")
    if not loc.found:
        report.append("- NOT FOUND: _resolve_repo_path")
        report.append("")
        report.append("## Note")
        report.append("- If the name differs, we need to locate the real resolver function name via grep.")
    else:
        for qn, ln, eln in loc.found:
            report.append(f"- `{qn}`  Lines: **{ln}–{eln}**")

    report.append("")
    report.append("## Next Step")
    report.append("")
    report.append("- Build a single-block PATCH runner using the exact lines above (no assumptions).")
    report.append("")

    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
