from __future__ import annotations


# --- R2299: HARD PROTECT --------------------------------------------------------------
def _r2299_read_keep_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    try:
        keepfile = root / "registry" / "tools_keep.txt"
        if keepfile.exists():
            for line in keepfile.read_text(encoding="utf-8", errors="replace").splitlines():
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                ids.add(s.upper())
    except Exception:
        pass
    # Purge-Runners themselves
    ids.add("R2218")
    ids.add("R2224")
    return ids


def _r2299_anchor_pairs_by_mtime(tools_dir: Path) -> set[Path]:
    newest = None
    newest_m = -1.0
    try:
        for p in tools_dir.iterdir():
            if not p.is_file():
                continue
            if p.suffix.lower() not in (".cmd", ".bat", ".py"):
                continue
            try:
                m = p.stat().st_mtime
            except Exception:
                continue
            if m > newest_m:
                newest_m = m
                newest = p
    except Exception:
        newest = None

    out: set[Path] = set()
    if newest is None:
        return out

    out.add(newest.resolve())
    base = newest.stem
    for ext in (".cmd", ".bat", ".py"):
        sib = tools_dir / f"{base}{ext}"
        if sib.exists():
            out.add(sib.resolve())
    return out


def _r2299_is_protected(root: Path, tools_dir: Path, path: Path) -> tuple[bool, str]:
    p = path.resolve()

    # Keep folders
    if any(part.lower() in ("_keep", "tools_keep") for part in p.parts):
        return True, "KEEP_FOLDER"

    # Keep list file itself
    keepfile = (root / "registry" / "tools_keep.txt").resolve()
    if p == keepfile:
        return True, "KEEPFILE"

    # Anchor (newest by mtime) pair protect
    anchors = _r2299_anchor_pairs_by_mtime(tools_dir)
    if p in anchors:
        return True, "ANCHOR_MTIME"

    # Keep IDs (by stem/name)
    keep_ids = _r2299_read_keep_ids(root)
    name_u = p.name.upper()
    stem_u = p.stem.upper()
    for kid in keep_ids:
        if stem_u == kid or name_u == kid:
            return True, f"KEEP_ID:{kid}"
        if stem_u == kid:
            return True, f"KEEP_ID:{kid}"
    return False, ""


# --- /R2299 --------------------------------------------------------------------------

import re
from pathlib import Path
from datetime import datetime


# --- R2297: HARD PROTECT (Self-Purge / KEEP / Anchor) ---------------------------------
def _r2297_read_keep_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    try:
        keepfile = root / "registry" / "tools_keep.txt"
        if keepfile.exists():
            for line in keepfile.read_text(encoding="utf-8", errors="replace").splitlines():
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                # Accept: R####, SR####, file names, etc. Normalize to upper tokens.
                ids.add(s.upper())
    except Exception:
        pass
    # Always protect the purge runners themselves
    ids.add("R2218")
    ids.add("R2224")
    return ids


def _r2297_anchor_paths_by_mtime(tools_dir: Path) -> set[Path]:
    # Protect newest .cmd/.py in tools root (pair-aware-ish: protect both if present)
    newest = None
    newest_m = -1.0
    try:
        for p in tools_dir.iterdir():
            if not p.is_file():
                continue
            if p.suffix.lower() not in (".cmd", ".bat", ".py"):
                continue
            try:
                m = p.stat().st_mtime
            except Exception:
                continue
            if m > newest_m:
                newest_m = m
                newest = p
    except Exception:
        newest = None

    out: set[Path] = set()
    if newest is None:
        return out

    out.add(newest.resolve())
    base = newest.stem  # e.g. R2249
    # Protect sibling pair(s)
    for ext in (".cmd", ".bat", ".py"):
        sib = tools_dir / f"{base}{ext}"
        if sib.exists():
            out.add(sib.resolve())
    return out


def _r2297_is_protected(root: Path, tools_dir: Path, path: Path) -> tuple[bool, str]:
    p = path.resolve()
    # Protect keep folders
    if any(part.lower() in ("_keep", "tools_keep") for part in p.parts):
        return True, "KEEP_FOLDER"

    # Protect keep list file itself
    keepfile = (root / "registry" / "tools_keep.txt").resolve()
    if p == keepfile:
        return True, "KEEPFILE"

    # Protect newest anchor by mtime (tools root)
    anchors = _r2297_anchor_paths_by_mtime(tools_dir)
    if p in anchors:
        return True, "ANCHOR_MTIME"

    # Protect named keep IDs (R#### / SR#### etc.) by filename token match
    keep_ids = _r2297_read_keep_ids(root)
    name_u = p.name.upper()
    stem_u = p.stem.upper()

    # If any keep token appears as whole-word-ish in name or stem, protect
    for kid in keep_ids:
        # R2297: HARD PROTECT filter (self/keep/anchor)
        _prot, _why = _r2297_is_protected(ROOT, TOOLS_DIR, Path(kid))
        if _prot:
            try:
                print(f"[R2224] SKIP PROTECTED: {kid} ({_why})")
            except Exception:
                pass
            continue

        if kid in (stem_u, name_u):
            return True, f"KEEP_ID:{kid}"
        # common: "R2249.cmd"
        if stem_u == kid or stem_u.startswith(kid + "_") or stem_u.startswith(kid + "."):
            return True, f"KEEP_ID:{kid}"

    return False, ""


# --- /R2297 ---------------------------------------------------------------------------

RID = "R2224"
ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
ARCHIVE_DIR = TOOLS / "Archiv"  # existiert bei euch bereits
DOCS = ROOT / "docs"
REPORTS = ROOT / "_Reports"

PLAN = DOCS / "Tools_Purge_Flat_Plan.md"
RX_ID = re.compile(r"^- R(\d{4})\b", re.M)


def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def main() -> int:
    REPORTS.mkdir(exist_ok=True)
    ARCHIVE_DIR.mkdir(exist_ok=True)

    print("=" * 72)
    print(f"[{RID}] Tools Purge Flat APPLY v3 (plan-driven, ROOT ONLY, pair-aware)")
    print(f"Plan: {PLAN}")
    print("=" * 72)

    if not PLAN.exists():
        print(f"[{RID}] ABORT: Plan nicht gefunden.")
        return 2

    txt = PLAN.read_text(encoding="utf-8", errors="replace")

    # Nur ARCHIVE-Section auslesen (alles darunter)
    mark = "\n## ARCHIVE"
    idx = txt.find(mark)
    if idx < 0:
        print(f"[{RID}] ABORT: ARCHIVE-Section nicht gefunden.")
        return 2

    tail = txt[idx:]
    ids = [int(m.group(1)) for m in RX_ID.finditer(tail)]
    ids = sorted(set(ids))

    report_path = REPORTS / f"{RID}_Tools_Purge_Flat_APPLY_{ts()}.txt"
    rep = []
    rep.append(f"{RID} APPLY Report")
    rep.append(f"Plan: {PLAN}")
    rep.append(f"IDs in ARCHIVE: {len(ids)}")

    moved = 0
    missing = 0

    for rid in ids:
        py = TOOLS / f"R{rid:04d}.py"
        cmd = TOOLS / f"R{rid:04d}.cmd"

        # R2299: HARD PROTECT BEFORE MOVE
        prot_py, why_py = _r2299_is_protected(ROOT, TOOLS, py)
        prot_cmd, why_cmd = _r2299_is_protected(ROOT, TOOLS, cmd)
        if prot_py or prot_cmd:
            print(f"[R2224] SKIP PROTECTED R{rid:04d} py={why_py or '-'} cmd={why_cmd or '-'}")
            rep.append(f"[SKIP_PROTECTED] R{rid:04d} py={why_py or '-'} cmd={why_cmd or '-'}")
            continue

        # pair-aware move; missing parts are OK but logged
        did_any = False

        if py.exists():
            py.rename(ARCHIVE_DIR / py.name)
            rep.append(f"[MOVE] {py.name} -> Archiv")
            moved += 1
            did_any = True
        else:
            rep.append(f"[MISS] {py.name}")
            missing += 1

        if cmd.exists():
            cmd.rename(ARCHIVE_DIR / cmd.name)
            rep.append(f"[MOVE] {cmd.name} -> Archiv")
            moved += 1
            did_any = True
        else:
            rep.append(f"[MISS] {cmd.name}")
            missing += 1

        if not did_any:
            rep.append(f"[SKIP] R{rid:04d} nothing to move (already archived?)")

    rep.append("")
    rep.append(f"moved_files: {moved}")
    rep.append(f"missing_parts: {missing}")

    report_path.write_text("\n".join(rep) + "\n", encoding="utf-8")
    print(f"[{RID}] moved_files={moved} missing_parts={missing}")
    print(f"[{RID}] REPORT: {report_path}")
    print(f"[{RID}] DONE (Code 0)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
