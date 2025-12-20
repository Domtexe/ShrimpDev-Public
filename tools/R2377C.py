# R2377C – Restore via helper method (indent-safe)
# - Adds helper _restore_window_from_ini()
# - Replaces ONE callsite in restore_from_ini()
# - No inline block replacement
# - Backup + compile-check + rollback

import os, sys, shutil, py_compile
from datetime import datetime

RID = "R2377C"
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

HELPER = [
"    def _restore_window_from_ini(self, cfg, sec, key, lab, builder, sw, sh):",
"        try:",
"            open_v = str(_r2339_cfg_get(cfg, sec, key + '.open', '1')).strip()",
"            docked_v = str(_r2339_cfg_get(cfg, sec, key + '.docked', '0')).strip()",
"        except Exception:",
"            open_v, docked_v = '1', '0'",
"        if open_v != '1' or docked_v == '1':",
"            return False",
"",
"        geo = str(_r2339_cfg_get(cfg, sec, key + '.geometry', '')).strip()",
"        ww = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.w', '0'), 0)",
"        hh = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.h', '0'), 0)",
"        xx = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.x', '0'), 0)",
"        yy = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.y', '0'), 0)",
"",
"        restore_geo = None",
"        if geo:",
"            try:",
"                w2, h2, x2, y2 = _r2340_parse_geo(geo)",
"                if w2 > 1 and h2 > 1 and sw > 0 and sh > 0 and not _r2340_is_offscreen(x2, y2, w2, h2, sw, sh):",
"                    restore_geo = geo",
"            except Exception:",
"                restore_geo = None",
"",
"        if restore_geo is None and ww > 1 and hh > 1 and sw > 0 and sh > 0:",
"            if not _r2340_is_offscreen(xx, yy, ww, hh, sw, sh):",
"                restore_geo = str(ww) + 'x' + str(hh) + '+' + str(xx) + '+' + str(yy)",
"",
"        self.undock_readonly(key, lab, builder, restore_geometry=restore_geo)",
"        return True",
]

def main():
    root = root_dir()
    path = os.path.join(root, "modules", "module_docking.py")
    if not os.path.isfile(path):
        log("FEHLER: module_docking.py nicht gefunden")
        return 2

    src = open(path, "r", encoding="utf-8", errors="replace").read().splitlines()
    bak = backup(path)

    # Insert helper before restore_from_ini
    insert_at = None
    for i, ln in enumerate(src):
        if ln.strip() == "def restore_from_ini(self):":
            insert_at = i
            break
    if insert_at is None:
        log("FEHLER: restore_from_ini nicht gefunden")
        return 2

    if not any("_restore_window_from_ini" in ln for ln in src):
        src[insert_at:insert_at] = HELPER + [""]
        log("OK: Helper-Funktion eingefügt")
    else:
        log("OK: Helper-Funktion bereits vorhanden")

    # Replace single callsite
    replaced = False
    for i, ln in enumerate(src):
        if "self.undock_readonly(" in ln and "restore_geometry=" in ln:
            src[i] = ln.replace(
                "self.undock_readonly(key, lab, builder, restore_geometry=restore_geo)",
                "self._restore_window_from_ini(cfg, sec, key, lab, builder, sw, sh)"
            )
            replaced = True
            log(f"OK: Callsite ersetzt (Zeile {i+1})")
            break

    if not replaced:
        log("FEHLER: Callsite nicht gefunden")
        return 2

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(src) + "\n")

    ok, err = compile_ok(path)
    if not ok:
        log("FEHLER: Kompilation fehlgeschlagen: " + err)
        shutil.copy2(bak, path)
        log("ROLLBACK: Wiederhergestellt")
        return 2

    rep = os.path.join(root, "docs", f"Report_{RID}_Restore_Helper.md")
    with open(rep, "w", encoding="utf-8") as f:
        f.write(
            f"# {RID} – Restore via Helper\n\n"
            f"- Zeit: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
            f"- Strategie: Helper-Funktion + 1 Callsite\n"
            f"- Risiko: minimal\n"
        )
    log("OK: Report geschrieben: " + rep)
    return 0

if __name__ == "__main__":
    sys.exit(main())
