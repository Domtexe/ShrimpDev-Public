# R2395 - Patch module_docking.restore_from_ini:
# - respect Docking.<key>.open (open=1 only)
# - prefer Docking.<key>.geometry (WxH+X+Y)
# - fallback to legacy w/h/x/y only if geometry missing
# - offscreen-guard before applying geometry
#
# Mastermodus: Backup, minimal patch, compile gate, report.

from __future__ import annotations

import re
import sys
import hashlib
import datetime as _dt
from pathlib import Path
import py_compile

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "modules" / "module_docking.py"
DOCS = ROOT / "docs"

RID = "R2395"


def _ts() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def _backup(p: Path) -> Path:
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = ROOT / "_Archiv" / f"{p.name}.{RID}_{stamp}.bak"
    bak.parent.mkdir(parents=True, exist_ok=True)
    bak.write_bytes(p.read_bytes())
    return bak


def _write_report(lines: list[str]) -> Path:
    DOCS.mkdir(parents=True, exist_ok=True)
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    rp = DOCS / f"Report_{RID}_Docking_RestoreOpenGeo_{stamp}.md"
    rp.write_text("\n".join(lines), encoding="utf-8")
    return rp


def _patch_restore_from_ini(src: str) -> tuple[str, bool, str]:
    """
    Replace the loop inside DockManager.restore_from_ini that undocks windows
    without respecting open/docked and without using <key>.geometry.
    """

    # We target the specific block:
    #   for key in keys:
    #       if key not in mapping: ...
    #       ...
    #       ww/hh/xx/yy ...
    #       restore_geo = None
    #       if ww > 1 ...
    #       self.undock_readonly(...)
    #
    # We replace that whole loop body with a corrected version.

    pattern = re.compile(
        r"""
(?P<indent>^[ \t]+)for[ \t]+key[ \t]+in[ \t]+keys:[ \t]*\n
(?P<body>
(?:^(?P=indent)[ \t]+.*\n)+?
)
(?=^(?P=indent)\S)  # next statement at same indent
        """,
        re.VERBOSE | re.MULTILINE,
    )

    m = pattern.search(src)
    if not m:
        return src, False, "restore_from_ini loop not found (pattern miss)"

    indent = m.group("indent")

    replacement = (
        f"{indent}for key in keys:\n"
        f"{indent}    if key not in mapping:\n"
        f"{indent}        continue\n"
        f"{indent}    if self.is_open(key):\n"
        f"{indent}        continue\n"
        f"{indent}    lab, builder = mapping[key]\n"
        f"{indent}    # Respect persisted open/docked flags\n"
        f"{indent}    try:\n"
        f"{indent}        open_v = str(_r2339_cfg_get(cfg, sec, key + '.open', '0')).strip()\n"
        f"{indent}        docked_v = str(_r2339_cfg_get(cfg, sec, key + '.docked', '0')).strip()\n"
        f"{indent}    except Exception:\n"
        f"{indent}        open_v, docked_v = '0', '0'\n"
        f"{indent}    if open_v != '1' or docked_v == '1':\n"
        f"{indent}        continue\n"
        f"{indent}    # Prefer geometry string (WxH+X+Y)\n"
        f"{indent}    restore_geo = ''\n"
        f"{indent}    try:\n"
        f"{indent}        restore_geo = str(_r2339_cfg_get(cfg, sec, key + '.geometry', '')).strip()\n"
        f"{indent}    except Exception:\n"
        f"{indent}        restore_geo = ''\n"
        f"{indent}    if restore_geo:\n"
        f"{indent}        try:\n"
        f"{indent}            ww, hh, xx, yy = _r2340_parse_geo(restore_geo)\n"
        f"{indent}            if ww > 1 and hh > 1 and sw > 0 and sh > 0:\n"
        f"{indent}                if _r2340_is_offscreen(xx, yy, ww, hh, sw, sh):\n"
        f"{indent}                    restore_geo = ''\n"
        f"{indent}        except Exception:\n"
        f"{indent}            restore_geo = ''\n"
        f"{indent}    # Fallback: legacy w/h/x/y if geometry missing\n"
        f"{indent}    if not restore_geo:\n"
        f"{indent}        ww = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.w', '0'), 0)\n"
        f"{indent}        hh = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.h', '0'), 0)\n"
        f"{indent}        xx = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.x', '0'), 0)\n"
        f"{indent}        yy = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.y', '0'), 0)\n"
        f"{indent}        if ww > 1 and hh > 1 and sw > 0 and sh > 0:\n"
        f"{indent}            if not _r2340_is_offscreen(xx, yy, ww, hh, sw, sh):\n"
        f"{indent}                restore_geo = str(ww) + 'x' + str(hh) + '+' + str(xx) + '+' + str(yy)\n"
        f"{indent}    self.undock_readonly(key, lab, builder, restore_geometry=(restore_geo or None))\n"
        f"{indent}    any_open = True\n"
    )

    new_src = src[: m.start("indent")] + replacement + src[m.end("body") :]
    return new_src, True, "patched restore_from_ini loop (open flag + geometry preferred)"


def main() -> int:
    rep: list[str] = []
    rep.append(f"# Report {RID} – Docking Restore (open flag + geometry preference)")
    rep.append("")
    rep.append(f"- Timestamp: {_ts()}")
    rep.append(f"- Root: `{ROOT}`")
    rep.append(f"- Target: `{TARGET}`")
    rep.append("")

    if not TARGET.exists():
        rep.append("## ERROR\nTarget file missing.")
        _write_report(rep)
        return 2

    before_sha = _sha256(TARGET)
    before_size = TARGET.stat().st_size
    rep.append("## Before")
    rep.append(f"- Size: {before_size} bytes")
    rep.append(f"- SHA256: `{before_sha}`")
    rep.append("")

    src = TARGET.read_text(encoding="utf-8", errors="replace")

    # compile gate BEFORE (so we never patch a broken base silently)
    try:
        py_compile.compile(str(TARGET), doraise=True)
        rep.append("- AST/compile before: OK")
    except Exception as exc:
        rep.append(f"- AST/compile before: FAIL: `{exc!r}`")
        rep.append("")
        rep.append("Aborting patch (base is not compiling).")
        _write_report(rep)
        return 1

    new_src, changed, note = _patch_restore_from_ini(src)

    rep.append("## Patch")
    rep.append(f"- Result: **{ 'CHANGED' if changed else 'NO-OP' }**")
    rep.append(f"- Note: {note}")
    rep.append("")

    if not changed:
        rp = _write_report(rep)
        print(f"[{RID}] OK: no-op. Report {rp}")
        return 0

    bak = _backup(TARGET)
    TARGET.write_text(new_src, encoding="utf-8")

    # compile gate AFTER
    try:
        py_compile.compile(str(TARGET), doraise=True)
        rep.append("## After")
        rep.append("- AST/compile after: OK")
    except Exception as exc:
        rep.append("## After")
        rep.append(f"- AST/compile after: FAIL: `{exc!r}`")
        # rollback
        try:
            TARGET.write_bytes(bak.read_bytes())
            rep.append(f"- ROLLBACK: restored from `{bak.name}`")
        except Exception as rex:
            rep.append(f"- ROLLBACK FAILED: `{rex!r}`")
        rp = _write_report(rep)
        print(f"[{RID}] FEHLER: compile after failed, rollback attempted. Report {rp}")
        return 1

    after_sha = _sha256(TARGET)
    rep.append(f"- SHA256 after: `{after_sha}`")
    rep.append(f"- Backup: `{bak}`")

    rp = _write_report(rep)
    print(f"[{RID}] OK: patched. Report {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
