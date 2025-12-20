# R2375 – Update PIPELINE + MasterRules (INI SingleWriter Phase 2 + Diagnose-first + Defactoring)
# - READ/WRITE docs only, no app code changes
# - robust paths: prefers docs/PIPELINE.md, fallback PIPELINE.md
# - backups into _Archiv

import os
import shutil
from datetime import datetime

RID = "R2375"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")

def log(msg):
    print(f"[{RID}] {datetime.now():%Y-%m-%d %H:%M:%S} {msg}")

def root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def pick_path(preferred, fallback):
    return preferred if os.path.isfile(preferred) else fallback

def backup(path):
    arch = os.path.join(root_dir(), "_Archiv")
    os.makedirs(arch, exist_ok=True)
    dst = os.path.join(arch, os.path.basename(path) + f".{RID}_{TS}.bak")
    shutil.copy2(path, dst)
    log(f"Backup: {path} -> {dst}")
    return dst

def insert_block_after_anchor(text, anchor, block):
    if block.strip() in text:
        return text, False
    idx = text.find(anchor)
    if idx == -1:
        return text, None
    insert_at = idx
    new_text = text[:insert_at] + block + "\n\n" + text[insert_at:]
    return new_text, True

def append_if_missing(text, block):
    if block.strip() in text:
        return text, False
    return text.rstrip() + "\n\n" + block.strip() + "\n", True

def main():
    root = root_dir()

    pipeline_docs = os.path.join(root, "docs", "PIPELINE.md")
    pipeline_root = os.path.join(root, "PIPELINE.md")
    pipeline_path = pick_path(pipeline_docs, pipeline_root)

    mr_docs = os.path.join(root, "docs", "MasterRules.md")
    mr_root = os.path.join(root, "MasterRules.md")
    mr_path = pick_path(mr_docs, mr_root)

    if not os.path.isfile(pipeline_path):
        log("WARN: PIPELINE.md nicht gefunden (skip)")
    else:
        backup(pipeline_path)
        txt = open(pipeline_path, "r", encoding="utf-8", errors="replace").read()

        block = """## INI SingleWriter – Konsolidierung (TOP-PRIO)

**Status:** SAVE-Seite stabil (keine Overwrites). Offenes Thema: **Restore-Orchestrierung** (Fensterpositionen/Geometry pro Key korrekt wiederherstellen).

- [ ] (TOP/HIGH) Phase 2: Restore-Orchestrierung (pro Fenster-Key)
  - Ziel: Main, Log, Pipeline, Artefakte (runner_products) öffnen **exakt** dort, wo sie geschlossen wurden.
  - Regeln:
    - Restore nur **einmalig** beim Start (kein Auto-Refresh).
    - Apply-Timing: `after_idle` / WM-ready, damit WM nicht “drüberbügelt”.
    - Offscreen-Schutz: wenn Geometry außerhalb Screen -> Default/Center.
    - Pro Fenster **eigener Datensatz**: `<key>.open/.docked/.geometry/.ts`
  - Subtasks (zerlegt, damit es nicht eskaliert):
    - R2376 (DIAG, READ-ONLY): Logge Restore-Input (INI) + Apply + Effective Geometry (Main + Undocked)
    - R2377 (FIX): Per-Key Restore anwenden (Timing + Offscreen Clamp) **ohne** Save-Anpassungen
    - R2378 (HOOKS): Restore in App-Start + Restart-Button Pfad sicherstellen (immer gleicher Writer/INI)
    - R2379 (VERIFY): Testplan + Report + Doku-Update (Architektur/Changelog)

- [ ] (HIGH) Migration: Remaining Writers -> SingleWriter
  - Ziel: **Alle** INI-Schreibpfade (config_loader/config_mgr/docking/sonstige) konsolidieren, sodass nur `modules/ini_writer` schreibt.
  - Vorgehen: Diagnose-Report -> gezielte Delegation -> Verify.

- [ ] (MED) Defactoring / Archivierung (nach erfolgreicher Umstellung)
  - Alte/obsolete Dateien und Altpfade **erst nach** erfolgreicher Migration archivieren (kein Früh-Aufräumen).
  - Ergebnis: weniger Verwechslungen, weniger Import-Crashes, klare Struktur.
"""

        anchor = "## GUI"
        txt2, changed = insert_block_after_anchor(txt, anchor, block)
        if changed is None:
            # if GUI anchor missing, append at end
            txt2, changed2 = append_if_missing(txt, block)
            changed = changed2
            if changed:
                log("PIPELINE: Anchor nicht gefunden, Block ans Ende angehängt")
        if changed:
            with open(pipeline_path, "w", encoding="utf-8") as f:
                f.write(txt2)
            log(f"OK: PIPELINE aktualisiert: {pipeline_path}")
        else:
            log("OK: PIPELINE bereits aktuell (no-op)")

    if not os.path.isfile(mr_path):
        log("WARN: MasterRules.md nicht gefunden (skip)")
    else:
        backup(mr_path)
        txt = open(mr_path, "r", encoding="utf-8", errors="replace").read()

        mr_block = """## Ergänzung – Diagnose-first & SingleWriter-INI (Stand 2025-12-18)

- **Diagnose-first (verbindlich):** Wenn ein Fix nicht beim **ersten** Versuch verifiziert funktioniert, sofort Diagnose-Modus einschalten (Instrumentierung/Logs/kleiner Diagnose-Runner), **bevor** weitere Trial-&-Error-Patches gemacht werden.
- **INI SingleWriter Policy:** `ShrimpDev.ini` darf nur durch `modules/ini_writer` geschrieben werden. Alle anderen Module dürfen nur lesen oder über den Writer (API) aktualisieren. Keine direkten `open(...,"w")` / `configparser.write()` außerhalb des Writers.
- **__future__-Regel:** Wenn eine Datei `from __future__ import ...` enthält, darf **kein** Import/Code davor eingefügt werden. Falls nötig: Imports **innerhalb** der Funktion oder nach dem `__future__`.
- **Pipeline-first bei Features:** Feature-Requests werden zuerst als klar zerlegte Pipeline-Tasks einsortiert (mit Prio/Risiko), erst dann implementiert – außer bei akuten Crash-Bugs.
"""

        # append at end as a new section, idempotent
        txt2, changed = append_if_missing(txt, mr_block)
        if changed:
            with open(mr_path, "w", encoding="utf-8") as f:
                f.write(txt2)
            log(f"OK: MasterRules aktualisiert: {mr_path}")
        else:
            log("OK: MasterRules bereits aktuell (no-op)")

    # tiny report
    rep_dir = os.path.join(root, "docs")
    os.makedirs(rep_dir, exist_ok=True)
    rep = os.path.join(rep_dir, f"Report_{RID}_Pipeline_MasterRules_Update.md")
    with open(rep, "w", encoding="utf-8") as f:
        f.write(
            f"# {RID} – Pipeline + MasterRules Update\n\n"
            f"- Zeit: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
            f"- Inhalt:\n"
            f"  - Pipeline: INI SingleWriter Phase 2 Restore-Orchestrierung (zerlegt)\n"
            f"  - Pipeline: Defactoring/Archivierung nach erfolgreicher Migration\n"
            f"  - MasterRules: Diagnose-first + SingleWriter Policy + __future__ Regel + Pipeline-first\n"
        )
    log(f"OK: Report geschrieben: {rep}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
