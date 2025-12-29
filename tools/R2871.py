#!/usr/bin/env python3
# R2871: Public Repo Sanitize & Contract-Enforcer
#
# Safe-by-default:
# - Reads canonical config from private repo: registry/public_export_root.txt + registry/public_allowlist.txt
# - Creates a ZIP backup of the PUBLIC repo (outside of public repo) before destructive changes
# - Removes everything in the public repo root that is NOT allowlisted (with some always-keep safety)
# - Writes/updates Public_Contract.md into public repo docs/
# - Updates private repo docs/PIPELINE.md and docs/Master/MasterRules_Tech.md with the derived rule
#
# Exit codes:
# 0 OK
# 11 policy/operational error (missing files, bad paths, backup failure)
# 12 partial (non-fatal warnings occurred but sanitize completed)

from __future__ import annotations

import os
import sys
import shutil
import zipfile
import fnmatch
import datetime as _dt
from pathlib import Path
import subprocess
import textwrap

def now_stamp() -> str:
    return _dt.datetime.now().strftime("%Y%m%d_%H%M%S")

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")

def write_text(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8", newline="\n")

def normalize_rel(rel: str) -> str:
    rel = rel.strip().replace("\\", "/")
    while rel.startswith("./"):
        rel = rel[2:]
    rel = rel.strip("/")
    return rel

def load_allowlist(allowlist_path: Path) -> list[str]:
    lines = read_text(allowlist_path).splitlines()
    pats: list[str] = []
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        pats.append(normalize_rel(s))
    return pats

def is_allowed(rel: str, patterns: list[str], always_keep: set[str]) -> bool:
    rel = normalize_rel(rel)
    if rel in always_keep:
        return True
    # allow keeping any parent directories of always_keep entries
    for a in always_keep:
        if a.startswith(rel + "/"):
            return True
    for pat in patterns:
        # directory pattern like "docs/**" or "modules/**"
        if fnmatch.fnmatch(rel, pat):
            return True
        # allow "foo" to mean "foo/**"
        if rel == pat.rstrip("/"):
            return True
        if pat.endswith("/**") and rel.startswith(pat[:-3] + "/"):
            return True
    return False

def zip_dir(src: Path, dst_zip: Path, exclude_dirs: set[str] | None = None) -> None:
    exclude_dirs = exclude_dirs or set()
    with zipfile.ZipFile(dst_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in src.rglob("*"):
            rel = p.relative_to(src).as_posix()
            top = rel.split("/", 1)[0] if rel else ""
            if top in exclude_dirs:
                continue
            if p.is_dir():
                continue
            zf.write(p, arcname=rel)

def try_git_rm(path: Path) -> bool:
    # If repo is a git repo and git is available, prefer git rm for tracked files.
    try:
        subprocess.run(["git", "--version"], cwd=str(path), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception:
        return False
    try:
        # only if .git exists
        if not (path / ".git").exists():
            return False
        return True
    except Exception:
        return False

def git_remove(targets: list[Path], repo_root: Path, report_lines: list[str]) -> None:
    # Group removals: git rm -r --ignore-unmatch <targets...>
    rels = [t.relative_to(repo_root).as_posix() for t in targets]
    if not rels:
        return
    cmd = ["git", "rm", "-r", "--ignore-unmatch", "--quiet", "--"] + rels
    r = subprocess.run(cmd, cwd=str(repo_root), capture_output=True, text=True)
    report_lines.append(f"- git rm exit={r.returncode} on {len(rels)} targets")
    if r.stdout.strip():
        report_lines.append("  - stdout: " + r.stdout.strip().replace("\n", " | "))
    if r.stderr.strip():
        report_lines.append("  - stderr: " + r.stderr.strip().replace("\n", " | "))

def fs_remove(target: Path, report_lines: list[str]) -> None:
    try:
        if target.is_symlink() or target.is_file():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)
        else:
            # doesn't exist
            return
        report_lines.append(f"- removed: {target}")
    except Exception as e:
        report_lines.append(f"- ERROR removing {target}: {e}")
        raise

def ensure_contract(public_root: Path, report_lines: list[str]) -> None:
    contract_path = public_root / "docs" / "Public_Contract.md"
    content = textwrap.dedent(f"""\
        # Public Contract (ShrimpDev-Public)

        This repository is a **curated public export**, not a full mirror.

        ## What belongs here
        - Public-ready code modules and examples
        - Clean documentation (architecture, usage, contribution)
        - CI workflow for sanity checks
        - A small, explicit set of tools/runners that are intended for public use

        ## What must not be exported
        - Private repo registry/state/config that controls exports
        - Backups, reports, debug captures, internal journals
        - Internal pipelines, internal master rules, internal diagnostics
        - Any data that can reveal private structure, local paths, or operational details

        ## Enforcement
        The public export is **allowlist-based**. Anything not allowlisted is removed during export.

        Generated/updated: { _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") }
        """)
    write_text(contract_path, content)
    report_lines.append(f"- wrote: {contract_path}")

def patch_private_docs(private_root: Path, report_lines: list[str]) -> None:
    # Pipeline
    pipeline_path = private_root / "docs" / "PIPELINE.md"
    if not pipeline_path.exists():
        raise FileNotFoundError(f"PIPELINE.md not found at {pipeline_path}")

    mr_tech_path = private_root / "docs" / "Master" / "MasterRules_Tech.md"
    if not mr_tech_path.exists():
        raise FileNotFoundError(f"MasterRules_Tech.md not found at {mr_tech_path}")

    rule_block = textwrap.dedent("""\
        ### Public Repo Contract (export policy)

        - The public repo is **not a mirror**. It is a curated export.
        - Export must be **allowlist-based** (explicit include patterns).
        - Forbidden in public: backups, reports, debug captures, registry/state, internal pipeline, internal master rules, internal journals.
        - Export must write/update `docs/Public_Contract.md` in the public repo.
        - Any policy breach triggers a repair runner that sanitizes the public repo.
        """)

    def upsert_section(path: Path, header: str, block: str) -> None:
        txt = read_text(path)
        if header in txt and block.strip() in txt:
            report_lines.append(f"- docs already contain rule block: {path.name}")
            return
        # append at end with separator
        if not txt.endswith("\n"):
            txt += "\n"
        txt += "\n" + header + "\n\n" + block + "\n"
        write_text(path, txt)
        report_lines.append(f"- updated docs: {path}")

    upsert_section(pipeline_path, "## Policy Updates", rule_block)
    upsert_section(mr_tech_path, "## Public Export Policy", rule_block)

def main(root: Path) -> int:
    # root is PRIVATE repo root
    ts = now_stamp()
    report_lines: list[str] = []
    warnings: list[str] = []

    registry_dir = root / "registry"
    public_root_file = registry_dir / "public_export_root.txt"
    allowlist_file = registry_dir / "public_allowlist.txt"

    if not public_root_file.exists():
        raise FileNotFoundError(f"Missing {public_root_file}")
    if not allowlist_file.exists():
        raise FileNotFoundError(f"Missing {allowlist_file}")

    public_root = Path(read_text(public_root_file).strip().strip('"')).expanduser()
    if not public_root.exists():
        raise FileNotFoundError(f"public_export_root does not exist: {public_root}")

    # Safety: do not allow public_root == private root
    if public_root.resolve() == root.resolve():
        raise RuntimeError("public_export_root points to the private repo root. Aborting.")

    patterns = load_allowlist(allowlist_file)

    always_keep = {
        ".git",
        ".github",
        ".gitignore",
        "README.md",
        "LICENSE",
        "LICENSE.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "CURRENT_VERSION.txt",
        "docs/Public_Contract.md",
    }

    report_lines.append(f"# R2871 Report ({ts})")
    report_lines.append("")
    report_lines.append(f"- Private root: `{root}`")
    report_lines.append(f"- Public root: `{public_root}`")
    report_lines.append(f"- Allowlist: `{allowlist_file}` ({len(patterns)} patterns)")
    report_lines.append("")

    # Backup public repo (outside public repo)
    backups_dir = root / "_Backups" / "R2871"
    backups_dir.mkdir(parents=True, exist_ok=True)
    backup_zip = backups_dir / f"public_repo_backup_{ts}.zip"
    try:
        # do not include .git to keep zip smaller / less sensitive
        zip_dir(public_root, backup_zip, exclude_dirs={".git"})
        report_lines.append(f"- backup zip: `{backup_zip}`")
    except Exception as e:
        raise RuntimeError(f"Backup failed: {e}")

    # Determine removal targets in public root
    top_entries = [p for p in public_root.iterdir() if p.name not in (".git",)]
    to_remove: list[Path] = []

    for p in top_entries:
        rel = p.relative_to(public_root).as_posix()
        if is_allowed(rel, patterns, always_keep):
            continue
        to_remove.append(p)

    report_lines.append(f"- top-level entries: {len(top_entries)}")
    report_lines.append(f"- to remove (top-level): {len(to_remove)}")

    use_git = try_git_rm(public_root)
    if use_git:
        report_lines.append("- removal mode: git rm (tracked) + filesystem cleanup (untracked)")
    else:
        report_lines.append("- removal mode: filesystem delete (git not available or not a repo)")

    # Remove disallowed top-level entries
    if use_git and to_remove:
        try:
            git_remove(to_remove, public_root, report_lines)
        except Exception as e:
            warnings.append(f"git rm failed: {e} (falling back to filesystem)")
            use_git = False

    if not use_git:
        for t in to_remove:
            fs_remove(t, report_lines)

    # Ensure contract doc in public repo
    ensure_contract(public_root, report_lines)

    # Extra safety: prevent recursive export folder-in-public
    recursive = public_root / "ShrimpDev_PUBLIC_EXPORT"
    if recursive.exists():
        warnings.append("Found recursive folder ShrimpDev_PUBLIC_EXPORT inside public repo; removing.")
        if use_git:
            git_remove([recursive], public_root, report_lines)
        else:
            fs_remove(recursive, report_lines)

    # Patch private docs (pipeline + master rules)
    patch_private_docs(root, report_lines)

    # Write report into private Reports
    reports_dir = root / "Reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / f"Report_R2871_{ts}.md"
    if warnings:
        report_lines.append("")
        report_lines.append("## Warnings")
        for w in warnings:
            report_lines.append(f"- {w}")

    write_text(report_path, "\n".join(report_lines) + "\n")

    print(f"[R2871] OK: Report: {report_path}")
    if warnings:
        print(f"[R2871] WARN: {len(warnings)} warnings (see report).")
        return 12
    return 0

if __name__ == "__main__":
    try:
        root = Path(os.getcwd()).resolve()
        code = main(root)
        raise SystemExit(code)
    except Exception as e:
        # write minimal error report if possible
        try:
            root = Path(os.getcwd()).resolve()
            reports_dir = root / "Reports"
            reports_dir.mkdir(parents=True, exist_ok=True)
            ts = now_stamp()
            rp = reports_dir / f"Report_R2871_{ts}.md"
            write_text(rp, f"# R2871 FAIL ({ts})\n\nError: {e}\n")
            print(f"[R2871] FAIL -> {rp}")
        except Exception:
            print(f"[R2871] FAIL: {e}")
        raise SystemExit(11)
