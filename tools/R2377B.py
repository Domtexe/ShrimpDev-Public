# R2377B – Minimal Restore Fix
# - Replaces ONLY the per-key restore block inside restore_from_ini()
# - Uses <key>.open/.docked gating
# - Prefers <key>.geometry, fallback to w/h/x/y
# - Applies main.geometry once via after_idle
# - Backup + compile-check + rollback + report

import os, sys, shutil, py_compile
from datetime import datetime

RID = "R2377B"
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
    bak = backup(path)

    # Locate restore_from_ini
    def_idx = None
    for i, ln in enumerate(src):
        if ln.strip() == "def restore_from_ini(self):":
            def_idx = i
            break
    if def_idx is None:
        log("FEHLER: restore_from_ini nicht gefunden")
        return 2

    # Find screen size lines (after which we can inject main restore)
    swsh_end = None
    for i in range(def_idx, min(def_idx+200, len(src))):
        if src[i].strip().startswith("sh ="):
            swsh_end = i
            break
    if swsh_end is None:
        log("FEHLER: Screen-size Block nicht gefunden")
        return 2

    # Inject main restore once (idempotent)
    main_block = [
        "                # R2377B: apply MAIN geometry once (after_idle, offscreen-safe)",
        "                try:",
        "                        m_geo = str(_r2339_cfg_get(cfg, sec, 'main.geometry', '')).strip()",
        "                        if m_geo:",
        "                                self.app.after_idle(lambda g=m_geo: self.app.geometry(g))",
        "                except Exception:",
        "                        pass",
        ""
    ]
    if not any("R2377B: apply MAIN geometry" in ln for ln in src):
        src[swsh_end+1:swsh_end+1] = main_block
        log("OK: Main restore block eingefügt")
    else:
        log("OK: Main restore block bereits vorhanden")

    # Find the per-key restore block to replace (diagnosed lines 459-473)
    start = end = None
    for i in range(def_idx, min(def_idx+400, len(src))):
        if src[i].strip().startswith("for key in keys:"):
            # inside loop, find ww assignment
            for j in range(i, min(i+80, len(src))):
                if src[j].strip().startswith("ww ="):
                    start = j
                    break
            # find undock call
            for j in range(i, min(i+120, len(src))):
                if "self.undock_readonly(" in src[j]:
                    end = j
                    break
            break

    if start is None or end is None:
        log("FEHLER: Restore-Block nicht gefunden")
        return 2

    # Replacement block (INDENT = 24 spaces based on diagnosis)
    repl = [
        "                        # R2377B: gate by flags",
        "                        try:",
        "                                open_v = str(_r2339_cfg_get(cfg, sec, key + '.open', '1')).strip()",
        "                                docked_v = str(_r2339_cfg_get(cfg, sec, key + '.docked', '0')).strip()",
        "                        except Exception:",
        "                                open_v, docked_v = '1', '0'",
        "                        if open_v != '1' or docked_v == '1':",
        "                                continue",
        "",
        "                        # R2377B: prefer <key>.geometry, fallback w/h/x/y",
        "                        geo = str(_r2339_cfg_get(cfg, sec, key + '.geometry', '')).strip()",
        "                        ww = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.w', '0'), 0)",
        "                        hh = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.h', '0'), 0)",
        "                        xx = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.x', '0'), 0)",
        "                        yy = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.y', '0'), 0)",
        "",
        "                        restore_geo = None",
        "                        if geo:",
        "                                try:",
        "                                        w2, h2, x2, y2 = _r2340_parse_geo(geo)",
        "                                        if w2 > 1 and h2 > 1 and sw > 0 and sh > 0 and not _r2340_is_offscreen(x2, y2, w2, h2, sw, sh):",
        "                                                restore_geo = geo",
        "                                except Exception:",
        "                                        restore_geo = None",
        "",
        "                        if restore_geo is None and ww > 1 and hh > 1 and sw > 0 and sh > 0:",
        "                                if not _r2340_is_offscreen(xx, yy, ww, hh, sw, sh):",
        "                                        restore_geo = str(ww) + 'x' + str(hh) + '+' + str(xx) + '+' + str(yy)",
        "",
        "                        self.undock_readonly(key, lab, builder, restore_geometry=restore_geo)",
    ]

    # Replace lines start..end inclusive
    src = src[:start] + repl + src[end+1:]
    log("OK: Per-key restore block ersetzt")

    # Write back
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(src) + "\n")

    ok, err = compile_ok(path)
    if not ok:
        log("FEHLER: Kompilation fehlgeschlagen: " + err)
        shutil.copy2(bak, path)
        log("ROLLBACK: Wiederhergestellt")
        return 2

    # Report
    rep_dir = os.path.join(root, "docs")
    os.makedirs(rep_dir, exist_ok=True)
    rep = os.path.join(rep_dir, f"Report_{RID}_Restore_Fix.md")
    with open(rep, "w", encoding="utf-8") as f:
        f.write(
            f"# {RID} – Minimal Restore Fix\n\n"
            f"- Zeit: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
            f"- Datei: modules/module_docking.py\n"
            f"- Änderungen:\n"
            f"  - Gate via <key>.open/.docked\n"
            f"  - Prefer <key>.geometry, fallback w/h/x/y\n"
            f"  - Main geometry once via after_idle\n"
        )
    log("OK: Report geschrieben: " + rep)
    return 0

if __name__ == "__main__":
    sys.exit(main())
