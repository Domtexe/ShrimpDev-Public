import sys
from pathlib import Path
from datetime import datetime

RID="R2823"

def ts(): return datetime.now().strftime("%Y%m%d_%H%M%S")

def report(root: Path, txt: str) -> Path:
    d = root/"Reports"; d.mkdir(exist_ok=True)
    rp = d/f"Report_{RID}_{ts()}.md"
    rp.write_text(txt, encoding="utf-8")
    return rp

def backup(p: Path) -> Path:
    b = p.with_suffix(p.suffix + f".{RID}_{ts()}.bak")
    b.write_text(p.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    return b

def ensure_section(lines, name):
    hdr = f"[{name}]"
    if any(l.strip().lower() == hdr.lower() for l in lines):
        return lines
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    if lines and lines[-1].strip() != "":
        lines.append("\n")
    lines.append(hdr + "\n")
    return lines

def upsert_key(lines, section, key, value):
    # minimal INI editor, preserves most formatting
    sec = f"[{section}]".lower()
    in_sec = False
    wrote = False
    out = []
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s.startswith("[") and s.endswith("]"):
            if in_sec and not wrote:
                out.append(f"{key} = {value}\n")
                wrote = True
            in_sec = (s.lower() == sec)
            out.append(ln)
            continue
        if in_sec and s.lower().startswith(key.lower() + " "):
            out.append(f"{key} = {value}\n")
            wrote = True
        else:
            out.append(ln)
    if in_sec and not wrote:
        out.append(f"{key} = {value}\n")
    return out, wrote

def main():
    root = Path(sys.argv[1]).resolve()
    ini = root/"ShrimpDev.ini"
    notes = [f"# {RID} – Disable Workspace + Repo roots in INI\n\n", f"INI: `{ini}`\n\n"]

    if not ini.exists():
        rp = report(root, "".join(notes)+"**FAIL** ShrimpDev.ini missing\n")
        print(f"[{RID}] FAIL: {rp}")
        return 11

    bak = backup(ini)
    notes.append(f"- Backup: `{bak.name}`\n")

    lines = ini.read_text(encoding="utf-8", errors="replace").splitlines(True)

    # Ensure sections
    lines = ensure_section(lines, "settings")
    lines = ensure_section(lines, "Repo")

    # Disable workspace
    lines, _ = upsert_key(lines, "settings", "workspace_enabled", "false")

    # Repo keys
    lines, _ = upsert_key(lines, "Repo", "private_root", "")
    lines, _ = upsert_key(lines, "Repo", "public_root", "")
    lines, _ = upsert_key(lines, "Repo", "public_autocreate", "true")

    ini.write_text("".join(lines), encoding="utf-8")
    rp = report(root, "".join(notes) + "\n**RESULT: OK**\n")
    print(f"[{RID}] OK: Report: {rp}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
