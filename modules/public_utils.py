from __future__ import annotations


def describe_public_surface() -> list[str]:
    return [
        "Curated public export",
        "Minimal Python entrypoint",
        "Small helper module surface",
        "Demo runner without internal workflow coupling",
    ]


def bullet_lines(items: list[str]) -> str:
    clean = [str(item).strip() for item in items if str(item).strip()]
    if not clean:
        return "- none"
    return "\n".join(f"- {item}" for item in clean)
