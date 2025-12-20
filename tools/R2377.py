# R2377 – Docking Restore Fix (INI .geometry + open/docked + main restore)
# - Patches ONLY modules/module_docking.py restore_from_ini()
# - Prefers <key>.geometry, fallback to w/h/x/y
# - Opens undocked windows only when open=1 and docked=0
# - Applies main geometry after_idle (offscreen protected)
# - Backup + compile-check + rollback + report

import os, sys, shutil, py_compile
from datetime import datetime

RID = "R2377"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")

def log(msg):
    print(f"[{RID}] {datetime.now():%Y-%m-%d %H:%M:%S} {msg}")

def root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def backup(path):
    arch = os.path.join(root_dir(), "_Archiv")
    os.makedirs(arch, exist_ok=True)
    dst = os.path.join(arch, os.path.basename(path) + f".{RID}_{TS}.bak")
    shutil.copy2(path, dst)
    log(f"Backup: {path} -> {dst}")
    return dst

def compile_ok(path):
    try:
        py_compile.compile(path, doraise=True)
        return True, ""
    except Exception as e:
        return False, repr(e)

def main():
    root = root_dir()
    path = os.path.join(root, "modules", "module_docking.py")
    if not os.path.isfile(path):
        log("FEHLER: modules/module_docking.py nicht gefunden")
        return 2

    src = open(path, "r", encoding="utf-8", errors="replace").read().splitlines()
    backup_path = backup(path)

    # Find restore_from_ini method start
    def_line = None
    for i, ln in enumerate(src):
        if ln.strip() == "def restore_from_ini(self):" and ln.startswith("    "):
            def_line = i
            break
    if def_line is None:
        log("FEHLER: Anchor 'def restore_from_ini(self):' nicht gefunden")
        return 2

    # Within restore_from_ini: locate the block that builds restore_geo from ww/hh/xx/yy and calls undock_readonly
    # We'll replace from the first "ww = " line to the undock_readonly(...) line (inclusive).
    start = end = None
    for i in range(def_line, min(def_line + 400, len(src))):
        if "ww = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.w'" in src[i].replace(" ", ""):
            start = i
            break
    if start is None:
        # fallback: locate "ww =" in that region
        for i in range(def_line, min(def_line + 500, len(src))):
            if src[i].strip().startswith("ww = _r2339_safe_int("):
                start = i
                break
    if start is None:
        log("FEHLER: Anchor für ww/hh/xx/yy Block nicht gefunden")
        return 2

    for i in range(start, min(start + 80, len(src))):
        if "self.undock_readonly(" in src[i]:
            end = i
            break
    if end is None:
        log("FEHLER: Anchor 'self.undock_readonly(' nicht gefunden")
        return 2

    # Insert main-restore block near top of restore_from_ini, after sw/sh are computed.
    # We locate "any_open = False" line as insertion point (right before it).
    insert_at = None
    for i in range(def_line, min(def_line + 350, len(src))):
        if src[i].strip() == "any_open = False":
            insert_at = i
            break
    if insert_at is None:
        log("FEHLER: Anchor 'any_open = False' nicht gefunden")
        return 2

    main_restore_block = [
        "        # R2377: Apply MAIN geometry (one-time, offscreen protected, after_idle)",
        "        try:",
        "            m_open = str(_r2339_cfg_get(cfg, sec, 'main.open', '1')).strip()",
        "            m_geo = str(_r2339_cfg_get(cfg, sec, 'main.geometry', '')).strip()",
        "            mw = _r2339_safe_int(_r2339_cfg_get(cfg, sec, 'main.w', '0'), 0)",
        "            mh = _r2339_safe_int(_r2339_cfg_get(cfg, sec, 'main.h', '0'), 0)",
        "            mx = _r2339_safe_int(_r2339_cfg_get(cfg, sec, 'main.x', '0'), 0)",
        "            my = _r2339_safe_int(_r2339_cfg_get(cfg, sec, 'main.y', '0'), 0)",
        "            restore_main = ''",
        "            if m_geo:",
        "                restore_main = m_geo",
        "            elif mw > 1 and mh > 1:",
        "                restore_main = str(mw) + 'x' + str(mh) + '+' + str(mx) + '+' + str(my)",
        "            if m_open == '1' and restore_main and sw > 0 and sh > 0:",
        "                try:",
        "                    ww2, hh2, xx2, yy2 = _r2340_parse_geo(restore_main)",
        "                    if (ww2 > 1 and hh2 > 1) and (not _r2340_is_offscreen(xx2, yy2, ww2, hh2, sw, sh)):",
        "                        self.app.after_idle(lambda g=str(restore_main): self.app.geometry(g))",
        "                except Exception:",
        "                    pass",
        "        except Exception:",
        "            pass",
        "",
        "        # R2377: Restore undocked windows uses per-key .open/.docked + .geometry (fallback w/h/x/y)",
    ]

    # Replace ww/hh/xx/yy → restore_geo build with .geometry preference + open/docked gate
    replacement_block = [
        "            # R2377: gate by flags",
        "            try:",
        "                open_v = str(_r2339_cfg_get(cfg, sec, key + '.open', '1')).strip()",
        "                docked_v = str(_r2339_cfg_get(cfg, sec, key + '.docked', '0')).strip()",
        "            except Exception:",
        "                open_v, docked_v = '1', '0'",
        "            if open_v != '1':",
        "                continue",
        "            if docked_v == '1':",
        "                # should stay docked in notebook -> do not open an undocked window",
        "                continue",
        "",
        "            # Prefer <key>.geometry, fallback to w/h/x/y",
        "            geo_str = str(_r2339_cfg_get(cfg, sec, key + '.geometry', '')).strip()",
        "            ww = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.w', '0'), 0)",
        "            hh = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.h', '0'), 0)",
        "            xx = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.x', '0'), 0)",
        "            yy = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.y', '0'), 0)",
        "",
        "            restore_geo = None",
        "            if geo_str:",
        "                try:",
        "                    ww2, hh2, xx2, yy2 = _r2340_parse_geo(geo_str)",
        "                    if ww2 > 1 and hh2 > 1 and sw > 0 and sh > 0 and (not _r2340_is_offscreen(xx2, yy2, ww2, hh2, sw, sh)):",
        "                        restore_geo = geo_str",
        "                except Exception:",
        "                    restore_geo = None",
        "",
        "            if restore_geo is None and ww > 1 and hh > 1 and sw > 0 and sh > 0:",
        "                if not _r2340_is_offscreen(xx, yy, ww, hh, sw, sh):",
        "                    restore_geo = str(ww) + 'x' + str(hh) + '+' + str(xx) + '+' + str(yy)",
        "",
        "            self.undock_readonly(key, lab, builder, restore_geometry=restore_geo)",
    ]

    # Apply patch
    patched = src[:]

    # Insert main-restore block (idempotent check)
    if not any("R2377: Apply MAIN geometry" in ln for ln in patched):
        patched[insert_at:insert_at] = main_restore_block
        log("OK: Main-Restore Block eingefügt")
    else:
        log("OK: Main-Restore Block bereits vorhanden (no-op)")

    # Replace the per-window restore block
    patched = patched[:start] + replacement_block + patched[end+1:]
    log("OK: Restore Geo Block ersetzt (.geometry + flags)")

    # Write back
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(patched) + "\n")

    ok, err = compile_ok(path)
    if not ok:
        log("FEHLER: Patch kompiliert nicht: " + err)
        shutil.copy2(backup_path, path)
        log("ROLLBACK: module_docking.py restored from backup")
        return 2

    # Report
    rep_dir = os.path.join(root, "docs")
    os.makedirs(rep_dir, exist_ok=True)
    rep = os.path.join(rep_dir, f"Report_{RID}_Docking_Restore_Fix.md")
    with open(rep, "w", encoding="utf-8") as f:
        f.write(
            f"# {RID} – Docking Restore Fix\n\n"
            f"- Zeit: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
            f"- Datei: modules/module_docking.py\n\n"
            f"## Änderungen\n"
            f"- Restore nutzt `<key>.open` / `<key>.docked` als Gate.\n"
            f"- Restore-Geometrie bevorzugt `<key>.geometry`, fallback `<key>.w/.h/.x/.y`.\n"
            f"- Main-Window: `main.geometry` wird einmalig `after_idle` gesetzt (offscreen protected).\n"
            f"- Kein Save-Verhalten geändert.\n"
        )
    log("OK: Report geschrieben: " + rep)
    return 0

if __name__ == "__main__":
    sys.exit(main())
