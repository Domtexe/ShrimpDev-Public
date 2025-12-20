# R2374G – AST-safe replacement of save()
# - Finds ANY save() definition via AST
# - Moves legacy body to _save_legacy (disabled)
# - Replaces save() with delegation to ini_writer
# - Backup + Compile-Check + Rollback

import os, sys, shutil, py_compile, ast
from datetime import datetime

RID = "R2374G"
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

class SaveFinder(ast.NodeVisitor):
    def __init__(self):
        self.targets = []  # (node, parent_class_name)

    def visit_ClassDef(self, node):
        for n in node.body:
            if isinstance(n, ast.FunctionDef) and n.name == "save":
                self.targets.append((n, node.name))
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # also catch top-level save()
        if node.name == "save":
            self.targets.append((node, None))
        self.generic_visit(node)

def main():
    root = root_dir()
    path = os.path.join(root, "modules", "config_manager.py")
    if not os.path.isfile(path):
        log("FEHLER: config_manager.py nicht gefunden")
        return 2

    src = open(path, "r", encoding="utf-8", errors="replace").read()
    backup(path)

    # ensure import
    if "modules.ini_writer import get_writer" not in src:
        src = "from modules.ini_writer import get_writer\n" + src
        log("Import ini_writer ergänzt")

    tree = ast.parse(src)
    finder = SaveFinder()
    finder.visit(tree)

    if not finder.targets:
        log("FEHLER: Keine save()-Methode per AST gefunden")
        return 2

    # Use the FIRST found save() (deterministic)
    save_node, class_name = finder.targets[0]
    log(f"Gefunden: save() in Klasse={class_name}")

    # Extract source segment safely
    lines = src.splitlines()
    start = save_node.lineno - 1
    end = save_node.end_lineno

    indent = lines[start][:len(lines[start]) - len(lines[start].lstrip())]

    legacy = lines[start:end]
    legacy_name = "_save_legacy"

    # Build legacy method
    legacy_header = indent + f"def {legacy_name}(self, *args, **kwargs):"
    legacy_body = []
    for i, ln in enumerate(legacy):
        if i == 0:
            legacy_body.append(legacy_header)
        else:
            legacy_body.append(indent + "    " + ln.lstrip())
    legacy_block = legacy_body

    # Build new save()
    new_save = [
        indent + "def save(self, source=None):",
        indent + "    # FINAL: Delegation an zentralen INI-Writer (Single Writer Policy)",
        indent + "    writer = get_writer()",
        indent + "    for sec in self._config.sections():",
        indent + "        writer.update_many(",
        indent + "            sec,",
        indent + "            dict(self._config.items(sec)),",
        indent + "            source=source or 'config_manager'",
        indent + "        )",
        indent + "    return writer.save_merge_atomic(source=source or 'config_manager')",
    ]

    # Replace in source
    new_lines = lines[:start] + new_save + [""] + legacy_block + lines[end:]
    new_src = "\n".join(new_lines)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_src)

    ok, err = compile_ok(path)
    if not ok:
        log("FEHLER: Kompilation fehlgeschlagen: " + err)
        shutil.copy2(
            os.path.join(root, "_Archiv", os.path.basename(path) + f".{RID}_{TS}.bak"),
            path
        )
        return 2

    rep = os.path.join(root, "docs", f"Report_{RID}_Final_Save_AST.md")
    with open(rep, "w", encoding="utf-8") as f:
        f.write(
            f"# {RID} – Finaler AST-Ersatz von save()\n\n"
            f"- Zeit: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
            f"- Klasse: {class_name}\n"
            f"- Aktion: save() ersetzt, Legacy nach {legacy_name} verschoben\n"
            f"- Schreibpfad: ini_writer.save_merge_atomic()\n"
        )
    log("OK: save() final ersetzt (AST-safe)")
    log("OK: Report geschrieben: " + rep)
    return 0

if __name__ == "__main__":
    sys.exit(main())
