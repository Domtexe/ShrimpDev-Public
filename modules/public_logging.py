from __future__ import annotations


def format_info(message: str) -> str:
    text = str(message).strip() or "info"
    return f"[INFO] {text}"


def format_section(title: str) -> str:
    text = str(title).strip() or "Section"
    return f"## {text}"
