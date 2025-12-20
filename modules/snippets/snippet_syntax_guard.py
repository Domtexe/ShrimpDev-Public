# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Literal


IssueKind = Literal["syntax", "style"]


@dataclass
class IntakeIssue:
    """
    Repräsentiert einen gefundenen Fehler/Hinweis im Intake-Code.
    kind="syntax"  -> harter Syntaxfehler (blockiert Save)
    kind="style"   -> PEP8-ähnlicher Hinweis (blockiert nicht)
    """
    kind: IssueKind
    message: str
    line: int
    column: Optional[int]
    line_text: Optional[str]


def analyze_source(source: str, filename: str = "<intake>") -> List[IntakeIssue]:
    """
    Analysiert den übergebenen Python-Quelltext:
    - Syntaxcheck via compile()  -> maximal 1 echter Syntaxfehler
    - einfache PEP8-Checks:
      - Zeile > 120 Zeichen
      - Tabs
      - trailing spaces
    """
    issues: List[IntakeIssue] = []

    try:
        compile(source, filename, "exec")
    except SyntaxError as err:
        issues.append(
            IntakeIssue(
                kind="syntax",
                message=err.msg,
                line=err.lineno or 0,
                column=err.offset,
                line_text=(err.text.rstrip("\n") if err.text else None),
            )
        )
    except Exception as exc:
        issues.append(
            IntakeIssue(
                kind="syntax",
                message=f"Unerwarteter Fehler beim Syntax-Check: {exc}",
                line=0,
                column=None,
                line_text=None,
            )
        )

    lines = source.splitlines()
    for i, line in enumerate(lines, start=1):
        logical = line.rstrip("\n")

        if len(line.expandtabs(4)) > 120:
            issues.append(
                IntakeIssue(
                    kind="style",
                    message="Zeile > 120 Zeichen (PEP8-Empfehlung)",
                    line=i,
                    column=None,
                    line_text=logical,
                )
            )

        if "\t" in line:
            issues.append(
                IntakeIssue(
                    kind="style",
                    message="Tabulator im Code (PEP8: Spaces bevorzugt)",
                    line=i,
                    column=None,
                    line_text=logical,
                )
            )

        if logical.rstrip(" ") != logical:
            issues.append(
                IntakeIssue(
                    kind="style",
                    message="Überflüssige Leerzeichen am Zeilenende",
                    line=i,
                    column=None,
                    line_text=logical,
                )
            )

    return issues
