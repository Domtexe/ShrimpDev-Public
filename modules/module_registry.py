from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(r"D:\ShrimpDev")
REG = ROOT / "registry" / "module_registry.json"
REG.parent.mkdir(parents=True, exist_ok=True)

SCHEMA = {
    "modules": [],  # {"name","path","version","owner","tags":[]}
    "runners": [],  # {"id","name","path","purpose","inputs":[]}
}


def load_registry() -> dict[str, Any]:
    if not REG.exists():
        save_registry(SCHEMA)
        return SCHEMA.copy()
    try:
        data = json.loads(REG.read_text(encoding="utf-8") or "{}")
        merged = SCHEMA.copy()
        merged.update({k: v for k, v in data.items() if isinstance(v, (list, dict))})
        return merged
    except Exception:
        return SCHEMA.copy()


def save_registry(d: dict[str, Any]) -> None:
    REG.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def upsert_module(name: str, path: str, **meta) -> None:
    reg = load_registry()
    mods = reg.get("modules", [])
    for m in mods:
        if m.get("name") == name:
            m.update({"path": path, **meta})
            save_registry(reg)
            return
    mods.append({"name": name, "path": path, **meta})
    reg["modules"] = mods
    save_registry(reg)


def upsert_runner(rid: int, name: str, path: str, **meta) -> None:
    reg = load_registry()
    arr = reg.get("runners", [])
    for r in arr:
        if int(r.get("id", -1)) == int(rid):
            r.update({"name": name, "path": path, **meta})
            save_registry(reg)
            return
    arr.append({"id": int(rid), "name": name, "path": path, **meta})
    reg["runners"] = arr
    save_registry(reg)
