# R2374B – gezielte Delegation von config_manager.save() an ini_writer
# - Ersetzt NUR den Body von save()
# - Keine Regex-Spielereien am Rest der Datei
# - Backup, Compile-Check, Mini-Report

import os
import sys
import shutil
import py_compile
from datetime import datetime

RID = "R2374B"
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

    # Import sicherstellen (nur einmal)
    if "modules.ini_writer import get_writer" not in txt:
        txt = iw_import + txt
        log("Import ini_writer ergänzt")

    # save()-Body gezielt ersetzen:
    # Wir suchen den exakten Funktionskopf 'def save(' und ersetzen den eingerückten Body.
    # Vorgehen: splitten am Funktionskopf und rekonstruieren minimal-invasiv.
    marker = "def save"
    idx = txt.find(marker)
    if idx < 0:
        log("FEHLER: save()-Methode nicht gefunden")
        return 2

    # Bestimme Einrückung
    line_start = txt.rfind("\n", 0, idx) + 1
    indent = ""
    while line_start < len(txt) and txt[line_start] == " ":
        indent += " "
        line_start += 1

    # Finde Ende der save()-Methode (nächste def mit gleicher Einrückung)
    rest = txt[idx:]
    next_def = rest.find("\n" + indent + "def ", 1)
    if next_def >= 0:
        save_block = rest[:next_def]
        tail = rest[next_def:]
    else:
        save_block = rest
        tail = ""

    # Neuer Body für save()
    new_save = (
        indent + "def save(self, source=None):\n"
        + indent + "    # Delegation an zentralen INI-Writer (Single Writer Policy)\n"
        + indent + "    try:\n"
        + indent + "        writer = get_writer()\n"
        + indent + "        # aktuellen Config-Stand an den Writer uebergeben (merge-only)\n"
        + indent + "        for sec in self._config.sections():\n"
        + indent + "            items = dict(self._config.items(sec))\n"
        + indent + "            writer.update_many(sec, items, source=source or 'config_manager')\n"
        + indent + "        return writer.save_merge_atomic(source=source or 'config_manager')\n"
        + indent + "    except Exception as e:\n"
        + indent + "        try:\n"
        + indent + "            print('[config_manager] save delegation FAILED ' + repr(e))\n"
        + indent + "        except Exception:\n"
        + indent + "            pass\n"
        + indent + "        return False\n"
    )

    txt_new = txt[:idx] + new_save + tail

    write_text(cm_path, txt_new)
    ok, err = compile_ok(cm_path)
    if not ok:
        log("FEHLER: Kompilation fehlgeschlagen: " + err)
        # Rollback
        shutil.copy2(os.path.join(root, "_Archiv", os.path.basename(cm_path) + "." + RID + "_" + TS + ".bak"), cm_path)
        return 2

    # Mini-Report
    rep = os.path.join(root, "docs", "Report_" + RID + "_ConfigManager_Save_Delegation.md")
    write_text(
        rep,
        "# " + RID + " – config_manager.save Delegation\n\n"
        + "- Zeit: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
        + "- Aenderung: save() delegiert an zentralen INI-Writer\n"
        + "- Entfernt: direkte open('w') / write() Overwrites\n"
        + "- Unveraendert: set_value() (ruft save() weiter auf)\n"
    )
    log("OK: Report geschrieben: " + rep)

    log("OK: R2374B abgeschlossen")
    return 0

if __name__ == "__main__":
    sys.exit(main())
