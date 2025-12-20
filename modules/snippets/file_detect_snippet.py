"""Robuste Dateiname/Endung-Erkennung."""
from __future__ import annotations
import os
from typing import Tuple

ALLOWED_EXTS = {".py", ".bat", ".cmd", ".json", ".txt", ".yml", ".yaml", ".ini", ".md", ".shcut"}

def split_name_ext(path: str) -> Tuple[str, str]:
    base = os.path.basename(path).strip()
    name, ext = os.path.splitext(base)
    return name, ext.lower()

def classify(path: str) -> str:
    _, ext = split_name_ext(path)
    if not ext:
        return "unknown"
    if ext in {".py"}: return "python"
    if ext in {".bat", ".cmd"}: return "batch"
    if ext in {".json", ".shcut"}: return "plan"
    if ext in {".ini"}: return "config"
    if ext in {".md", ".txt"}: return "doc"
    return "other"

def is_supported(path: str) -> bool:
    return split_name_ext(path)[1] in ALLOWED_EXTS
