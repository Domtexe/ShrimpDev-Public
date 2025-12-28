import sys, os, subprocess
from pathlib import Path
from datetime import datetime

RID="R2820"

def ts(): return datetime.now().strftime("%Y%m%d_%H%M%S")

def report(root: Path, txt: str) -> Path:
    d = root/"Reports"
    d.mkdir(exist_ok=True)
    rp = d/f"Report_{RID}_{ts()}.md"
    rp.write_text(txt, encoding="utf-8")
    return rp

def run(cmd, cwd=None):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        return r.returncode, (r.stdout or ""), (r.stderr or "")
    except Exception as e:
        return 999, "", repr(e)

def git_probe(repo: Path):
    g = repo/".git"
    info = {
        "path": str(repo),
        ".git_exists": g.exists(),
        ".git_is_dir": g.is_dir(),
        ".git_is_file": g.is_file(),
    }
    if not repo.exists():
        info["exists"]=False
        return info
    info["exists"]=True

    rc, out, err = run(["git","-C",str(repo),"rev-parse","--is-inside-work-tree"])
    info["rev_parse_rc"]=rc
    info["rev_parse_out"]=out.strip()
    info["rev_parse_err"]=err.strip()

    rc, out, err = run(["git","-C",str(repo),"status","--porcelain"])
    info["status_rc"]=rc
    info["dirty_lines"]=len([l for l in out.splitlines() if l.strip()])
    info["status_err"]=err.strip()

    # ahead/behind
    rc, out, err = run(["git","-C",str(repo),"rev-list","--left-right","--count","HEAD...@{upstream}"])
    info["ahead_rc"]=rc
    info["ahead_raw"]=out.strip()
    info["ahead_err"]=err.strip()

    return info

def candidate_public_roots(private_root: Path):
    c = []
    parent = private_root.parent
    c += [
        parent/"ShrimpDev-Public",
        parent/"ShrimpDev_PUBLIC_EXPORT",
        parent/"ShrimpDev_PUBLIC_REPO",
        parent/"ShrimpDevPublic",
    ]
    # env
    for k in ("SHRIMPDEV_PUBLIC_ROOT","SHRIMPDEV_PUBLIC_REPO"):
        v = os.environ.get(k,"").strip()
        if v:
            c.append(Path(v))
    return c

def main():
    root = Path(sys.argv[1]).resolve()
    private_root = root  # tools\.. = repo root assumption
    out=[]
    out.append(f"# {RID} READ-ONLY – Push Buttons Disabled Diagnose\n\n")
    out.append(f"cwd: `{os.getcwd()}`\n\n")
    out.append(f"private_root(arg): `{private_root}`\n\n")

    priv = git_probe(private_root)
    out.append("## Private repo probe\n\n")
    for k,v in priv.items():
        out.append(f"- **{k}**: `{v}`\n")
    out.append("\n")

    out.append("## Public repo candidates probe\n\n")
    pubs = candidate_public_roots(private_root)
    if not pubs:
        out.append("_No candidates._\n\n")
    for p in pubs:
        info = git_probe(p)
        out.append(f"### Candidate: `{p}`\n\n")
        for k,v in info.items():
            out.append(f"- **{k}**: `{v}`\n")
        out.append("\n")

    rp = report(root, "".join(out))
    print(f"[{RID}] OK: Report: {rp}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
