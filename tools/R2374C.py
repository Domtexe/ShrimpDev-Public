# R2374C – Robust save delegation via delegate method
# - save() bleibt bestehen und ruft _save_delegate()
# - _save_delegate() delegiert an ini_writer
# - Entfernt keine Methoden ausserhalb von save()-Body
# - Backup, Compile-Check, Rollback bei Fehler

import os
import sys
import shutil
import py_compile
from datetime import datetime

RID = "R2374C"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")

def log(msg):
    print("[" + RID + "] " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + msg)

def root_dir():
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(here, ".."))

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def read_text(p):
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def write_text(p, t):
    ensure_dir(os.path.dirname(p))
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)

def backup(p):
    arch = os.path.join(root_dir(), "_Archiv")
    ensure_dir(arch)
    dst = os.path.join(arch, os.path.basename(p) + "." + RID + "_" + TS + ".bak")
    shutil.copy2(p, dst)
    log("Backup: " + p + " -> " + dst)
    return dst

def compile_ok(p):
    try:
        py_compile.compile(p, doraise=True)
        return True, ""
    except Exception as e:
        return False, repr(e)

def main():
    root = root_dir()
    cm_path = os.path.join(root, "modules", "config_manager.py")
    iw_import = "from modules.ini_writer import get_writer\n"

    if not os.path.isfile(cm_path):
        log("FEHLER: config_manager.py nicht gefunden")
        return 2

    txt = read_text(cm_path)
    backup(cm_path)

    # Import sicherstellen (einmalig)
    if "modules.ini_writer import get_writer" not in txt:
        txt = iw_import + txt
        log("Import ini_writer ergänzt")

    # 1) save()-Body minimal ersetzen: save() ruft _save_delegate()
    # Wir ersetzen nur den Funktionsrumpf von save(), nicht die Signatur-Struktur drumherum.
    import re

    save_pattern = re.compile(
        r"(^\s*def\s+save\s*\(.*?\)\s*:\s*\n)([\s\S]*?)(?=^\s*def\s+|\Z)",
        re.MULTILINE
    )

    def repl_save(m):
        header = m.group(1)
        indent = header.split("def")[0]
        body = (
            indent + "    # Delegation an robuste Delegate-Methode\n"
            + indent + "    return self._save_delegate(source=source)\n"
        )
        return header + body

    txt_new, n = save_pattern.subn(repl_save, txt, count=1)
    if n == 0:
        log("FEHLER: save()-Methode nicht gefunden/ersetzbar")
        return 2

    # 2) _save_delegate() ergänzen, falls noch nicht vorhanden
    if "_save_delegate(" not in txt_new:
        insert_point = txt_new.rfind("\n")
        delegate = (
            "\n\n"
            "    def _save_delegate(self, source=None):\n"
            "        # Zentrale Delegation an INI-Writer (Single Writer Policy)\n"
            "        try:\n"
            "            writer = get_writer()\n"
            "            # aktuellen Config-Stand uebergeben (merge-only)\n"
            "            for sec in self._config.sections():\n"
            "                items = dict(self._config.items(sec))\n"
            "                writer.update_many(sec, items, source=source or 'config_manager')\n"
            "            return writer.save_merge_atomic(source=source or 'config_manager')\n"
            "        except Exception as e:\n"
            "            try:\n"
            "                print('[config_manager] save delegation FAILED ' + repr(e))\n"
            "            except Exception:\n"
            "                pass\n"
            "            return False\n"
        )
        txt_new = txt_new[:insert_point] + delegate + txt_new[insert_point:]
        log("Delegate-Methode _save_delegate() ergänzt")

    write_text(cm_path, txt_new)

    ok, err = compile_ok(cm_path)
    if not ok:
        log("FEHLER: Kompilation fehlgeschlagen: " + err)
        # Rollback
        shutil.copy2(
            os.path.join(root, "_Archiv", os.path.basename(cm_path) + "." + RID + "_" + TS + ".bak"),
            cm_path
        )
        return 2

    # Mini-Report
    rep = os.path.join(root, "docs", "Report_" + RID + "_ConfigManager_Save_Delegate.md")
    write_text(
        rep,
        "# " + RID + " – Robuste save-Delegation\n\n"
        + "- Zeit: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
        + "- Aenderung: save() -> _save_delegate() -> ini_writer\n"
        + "- Risiko: minimal (API bleibt stabil)\n"
    )
    log("OK: Report geschrieben: " + rep)

    log("OK: R2374C abgeschlossen")
    return 0

if __name__ == "__main__":
    sys.exit(main())
