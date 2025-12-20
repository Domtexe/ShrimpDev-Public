
from __future__ import annotations
import ast, json, re, time
from pathlib import Path
from typing import Any, Dict, List, Set

HUB = Path(r"D:\ShrimpHub")
OUT = Path(r"D:\ShrimpDev\_Reports\ProjectMap"); OUT.mkdir(parents=True, exist_ok=True)
MAP_JSON = OUT/"project_map.json"
MAP_HTML = OUT/"project_map.html"

IGNORE_DIRS = {"_Archiv","_Reports",".git","dist","build","__pycache__"}

def _want(p: Path) -> bool:
    if not p.is_file(): return False
    for seg in p.parts:
        if seg in IGNORE_DIRS: return False
    return p.suffix.lower() in {".py",".bat",".cmd"}

def _py_info(p: Path) -> Dict[str, Any]:
    info: Dict[str, Any] = {"path": str(p.relative_to(HUB)), "lang":"py"}
    src = p.read_text(encoding="utf-8", errors="ignore")
    try: tree = ast.parse(src)
    except Exception as ex:
        info["error"]=f"{type(ex).__name__}: {ex}"; return info
    imps:Set[str]=set(); defs=[]; classes=[]; handlers=[]
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names: imps.add(a.name)
        elif isinstance(n, ast.ImportFrom):
            if n.module: imps.add(n.module)
        elif isinstance(n, ast.FunctionDef):
            defs.append({"name":n.name,"args":[a.arg for a in n.args.args]})
        elif isinstance(n, ast.ClassDef):
            methods=[m.name for m in n.body if isinstance(m, ast.FunctionDef)]
            classes.append({"name":n.name,"methods":methods})
    # Tkinter-Wiring heuristisch
    for m in re.finditer(r'command\s*=\s*([A-Za-z_]\w*)', src):
        handlers.append({"kind":"button","target":m.group(1)})
    for m in re.finditer(r'\.bind[_a-z]*\(\s*[^,]+,\s*[\'"]([^\'"]+)[\'"]\s*,\s*([A-Za-z_]\w*)', src):
        handlers.append({"kind":"bind","sequence":m.group(1),"target":m.group(2)})

    info["imports"]=sorted(imps); info["defs"]=defs; info["classes"]=classes; info["handlers"]=handlers
    return info

def _bat_info(p: Path) -> Dict[str, Any]:
    t = p.read_text(encoding="utf-8", errors="ignore")
    calls = re.findall(r'(?im)\b(?:call|py\s+-3\s+-u|python\s+-u)\s+([^\s&|>]+)', t)
    sets  = re.findall(r'(?im)^\s*set\s+(\w+)=', t)
    return {"path": str(p.relative_to(HUB)), "lang":"bat", "calls":calls, "sets":sets}

def scan() -> Dict[str, Any]:
    files=[]
    for p in HUB.rglob("*"):
        if not _want(p): continue
        if p.suffix.lower()==".py": files.append(_py_info(p))
        else: files.append(_bat_info(p))
    # Orphans/Missing: einfache Heuristik
    all_py = {f["path"] for f in files if f.get("lang")=="py"}
    imports=set()
    for f in files:
        if f.get("lang")=="py":
            for mod in f.get("imports",[]):
                if mod.startswith("modules."):
                    mp = "modules/" + mod.split(".",1)[1].replace(".","/") + ".py"
                    imports.add(mp)
    missing = sorted([m for m in imports if m not in all_py])
    data = {
        "scanned_root": str(HUB),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": files,
        "stats": {
            "files_scanned": len(files),
            "py": sum(f["lang"]=="py" for f in files),
            "bat": sum(f["lang"]=="bat" for f in files),
            "missing_internal_modules": len(missing)
        },
        "missing_modules": missing
    }
    # JSON
    MAP_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    # HTML (kompakt)
    rows=[]
    for f in files:
        rows.append(f"<tr><td>{f.get('path','')}</td><td>{f.get('lang','')}</td>"
                    f"<td>{len(f.get('defs',[]))}</td><td>{len(f.get('classes',[]))}</td>"
                    f"<td>{len(f.get('handlers',[]))}</td></tr>")
    MAP_HTML.write_text(
        "<meta charset='utf-8'><style>table{border-collapse:collapse}td,th{border:1px solid #ccc;padding:4px 6px;font:12px Segoe UI}</style>"
        "<h3>ShrimpDev Project Map v2</h3><table><tr><th>Datei</th><th>Typ</th><th>Funktionen</th><th>Klassen</th><th>Handler</th></tr>"
        + "".join(rows) + "</table>", encoding="utf-8")
    return data

# Public API für UI:
def scan_project(root: Path, **_kwargs):
    global HUB
    try: HUB = Path(root)
    except Exception: pass
    return scan()

def write_reports(result, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir/"project_map.json"
    p.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return [p]
