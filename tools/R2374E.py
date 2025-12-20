# R2374E – Finaler gezielter Delegations-Patch
# Ersetzt exakt die write()-Calls in ShrimpDevConfigManager.save
# (Zeilen ~110, ~115 laut R2374D)
# Backup + Compile-Check + Rollback

import os
import sys
import shutil
import py_compile
from datetime import datetime

RID = "R2374E"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")

def log(msg):
    print(f"[{RID}] {datetime.now():%Y-%m-%d %H:%M:%S} {msg}")

def root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def backup(path):
    arch = os.path.join(root_dir(), "_Archiv")
    os.makedirs(arch, exist_ok=True)
    dst = os.path.join(
        arch, os.path.basename(path) + f".{RID}_{TS}.bak"
    )
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
    path = os.path.join(root, "modules", "config_manager.py")
    if not os.path.isfile(path):
        log("FEHLER: config_manager.py nicht gefunden")
        return 2

    src = open(path, "r", encoding="utf-8", errors="replace").read()
    backup(path)

    if "modules.ini_writer import get_writer" not in src:
        src = "from modules.ini_writer import get_writer\n" + src
        log("Import ini_writer ergänzt")

    # Ersetze ALLE configparser.write()-Calls in save()
    lines = src.splitlines()
    out = []
    replaced = 0

    for line in lines:
        if ".write(" in line and "save(" not in line:
            # write()-Call eliminieren
            out.append("        # write() entfernt – Delegation an INI-Writer")
            replaced += 1
        else:
            out.append(line)

    if replaced != 2:
        log(f"FEHLER: Erwartet 2 write()-Calls, gefunden: {replaced}")
        return 2

    # Sicherstellen, dass Delegation existiert (einmal)
    delegate_snippet = (
        "        writer = get_writer()\n"
        "        for sec in self._config.sections():\n"
        "            writer.update_many(\n"
        "                sec,\n"
        "                dict(self._config.items(sec)),\n"
        "                source='config_manager'\n"
        "            )\n"
        "        return writer.save_merge_atomic(source='config_manager')\n"
    )

    joined = "\n".join(out)
    if "save_merge_atomic" not in joined:
        joined = joined.replace(
            "def save",
            "def save"
        ).replace(
            "pass",
            delegate_snippet
        )
        log("Delegations-Logik ergänzt")

    with open(path, "w", encoding="utf-8") as f:
        f.write(joined)

    ok, err = compile_ok(path)
    if not ok:
        log("FEHLER: Kompilation fehlgeschlagen: " + err)
        shutil.copy2(
            os.path.join(root, "_Archiv", os.path.basename(path) + f".{RID}_{TS}.bak"),
            path
        )
        return 2

    report = os.path.join(root, "docs", f"Report_{RID}_ConfigManager_Final_Delegation.md")
    with open(report, "w", encoding="utf-8") as f:
        f.write(
            f"# {RID} – Final Delegation\n\n"
            f"- Zeit: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
            f"- Datei: modules/config_manager.py\n"
            f"- Entfernt: 2× write()\n"
            f"- Neu: ini_writer.save_merge_atomic()\n"
        )

    log("OK: Finaler Delegations-Patch abgeschlossen")
    log("OK: Report geschrieben: " + report)
    return 0

if __name__ == "__main__":
    sys.exit(main())
