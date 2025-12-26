"""
snippet_auto_category - R1177b
Einfaches Mapping von Datei-Endungen auf Kategorien.
"""

from __future__ import annotations
import os

MAP = {
    # Bilder
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".webp": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".tif": "Images",
    ".tiff": "Images",
    # Videos
    ".mp4": "Videos",
    ".mov": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",
    ".wmv": "Videos",
    # Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".flac": "Audio",
    ".ogg": "Audio",
    # Docs
    ".pdf": "Docs",
    ".txt": "Docs",
    ".md": "Docs",
    ".json": "Docs",
    ".csv": "Docs",
}


def guess_category(name: str, path: str) -> str:
    ext = os.path.splitext(name or path)[1].lower()
    return MAP.get(ext, "Misc")
