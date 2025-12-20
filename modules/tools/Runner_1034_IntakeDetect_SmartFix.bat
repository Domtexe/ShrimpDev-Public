"""
Runner_1033_FixBrokenPanedwindow
- Repariert zerbrochene Zeile 'body = ttk.Panedwindow(self, orient="horizontal")'
  (durch vorherigen Regex-Patch getrennt worden)
- Verifiziert Body-Aufbau (add(left), add(right))
- Lässt Toolbar/Wrapper unverändert
- Version -> v9.9.23
"""
from __future__ import annotations
import os, re, time, shutil, traceback

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ARCH = os.path.join(ROOT, "_Archiv")
MOD  = os.path.join(ROOT, "modules", "module_code_intake.py")
LOG  = os.path.join(ROOT, "debug_output.txt")

def log(msg: str) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"[R1033] {ts} {msg}\n")
    except Exception:
        pass
    print(msg, flush=True)

def backup_write(path: str, data: str) -> None:
    os.makedirs(ARCH, exist_ok=True)
    bck = os.path.join(ARCH, f"{os.path.basename(path)}.{int(time.time())}.bak")
    shutil.copy2(path, bck)
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(data)
    log(f"Backup: {path} -> {bck}")

def patch() -> int:
    with open(MOD, "r", encoding="utf-8") as f:
        src = f.read()

    changed = False

    # 1) Repariere harte Zeilentrennung bei Panedwindow
    fix1 = re.sub(
        r"body\s*=\s*ttk\.Panedwindow\s*\r?\n\s*\(self,\s*orient\s*=\s*\"horizontal\"\s*\)",
        'body = ttk.Panedwindow(self, orient="horizontal")',
        src,
        flags=re.MULTILINE,
    )
    if fix1 != src:
        src = fix1
        changed = True

    # 2) Falls aus Versehen nur 'body = ttk.Panedwindow' ohne Argumente existiert → ersetze
    fix2 = re.sub(
        r"body\s*=\s*ttk\.Panedwindow\s*(?=\r?\n)",
        'body = ttk.Panedwindow(self, orient="horizontal")',
        src,
        count=1
    )
    if fix2 != src:
        src = fix2
        changed = True

    # 3) Minimal-Check: beide Adds vorhanden, sonst ergänzen wir deklarativ
    if "body.add(left" not in src or "body.add(right" not in src:
        src = re.sub(
            r"(#\s*Editor links[\s\S]+?body\.add\(left[^\n]*\)\s*)"
            r"(?:\r?\n)+\s*#\s*Tabelle rechts",
            r"\1\n\n        # Tabelle rechts",
            src,
            flags=re.MULTILINE
        )
        # Falls right-Add fehlt, fügen wir es direkt vor dem Zielordner-Kontext ein
        if "body.add(right" not in src:
            src = src.replace(
                "right = ttk.Frame(body); right.rowconfigure(0, weight=1); right.columnconfigure(0, weight=1)",
                "right = ttk.Frame(body); right.rowconfigure(0, weight=1); right.columnconfigure(0, weight=1)\n        body.add(right, weight=2)"
            )
        changed = True

    if changed:
        backup_write(MOD, src)
        log("Panedwindow-Zeile repariert und Body geprüft.")
    else:
        log("Keine Reparatur nötig (Panedwindow-Zeile ok).")

    # Meta
    with open(os.path.join(ROOT, "CURRENT_VERSION.txt"), "w", encoding="utf-8") as f:
        f.write("ShrimpDev v9.9.23\n")
    with open(os.path.join(ROOT, "CHANGELOG.md"), "a", encoding="utf-8") as f:
        f.write("""
## v9.9.23 (2025-10-18)
- Fix: 'body = ttk.Panedwindow(self, orient="horizontal")' wieder korrekt in einer Zeile
- Body-Adds geprüft (left/right)
""")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(patch())
    except Exception:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write("[R1033] FEHLER:\n" + traceback.format_exc() + "\n")
        print("FEHLER:\n" + traceback.format_exc())
        raise
