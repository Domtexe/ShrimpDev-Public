from __future__ import annotations
import os, time
from pathlib import Path

def write_atomic(target: Path, data: str) -> bool:
    tmp = target.with_suffix(target.suffix + f".tmp.{int(time.time()*1000)}")
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(data, encoding="utf-8")
    try:
        os.replace(tmp, target)
        return True
    except PermissionError:
        try: tmp.unlink(missing_ok=True)
        except Exception: pass
        return False

def try_rename(p: Path) -> bool:
    probe = p.with_suffix(p.suffix + ".lockprobe")
    try:
        p.rename(probe); probe.rename(p); return True
    except Exception:
        return False
