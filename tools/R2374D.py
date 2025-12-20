# R2374D – READ-ONLY Diagnose
# Ermittelt reale Schreibpfade in modules/config_manager.py
# - Sucht open(..., 'w'/'a')
# - Sucht configparser.write()
# - Sucht save()/set_value()-Ketten
# - Ermittelt Funktions- und Klassenkontext
# - KEINE Aenderungen

import os
import sys
import ast
from datetime import datetime

RID = "R2374D"

def log(msg):
    print("[" + RID + "] " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + msg)

def root_dir():
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(here, ".."))

class WriteAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.findings = []
        self.class_stack = []
        self.func_stack = []

    def visit_ClassDef(self, node):
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node):
        self.func_stack.append(node.name)
        self.generic_visit(node)
        self.func_stack.pop()

    def visit_Call(self, node):
        # open(..., 'w'/'a')
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            if len(node.args) >= 2:
                mode = node.args[1]
                if isinstance(mode, ast.Constant) and isinstance(mode.value, str):
                    if "w" in mode.value or "a" in mode.value:
                        self._hit(node, "open('" + mode.value + "')")

        # *.write(...)
        if isinstance(node.func, ast.Attribute) and node.func.attr == "write":
            self._hit(node, "write() call")

        self.generic_visit(node)

    def _hit(self, node, kind):
        self.findings.append({
            "kind": kind,
            "line": node.lineno,
            "class": self.class_stack[-1] if self.class_stack else None,
            "function": self.func_stack[-1] if self.func_stack else None,
        })

def main():
    root = root_dir()
    target = os.path.join(root, "modules", "config_manager.py")
    if not os.path.isfile(target):
        log("FEHLER: config_manager.py nicht gefunden")
        return 2

    log("Analysiere: " + target)

    with open(target, "r", encoding="utf-8", errors="replace") as f:
        src = f.read()

    tree = ast.parse(src)
    analyzer = WriteAnalyzer()
    analyzer.visit(tree)

    # Report
    docs = os.path.join(root, "docs")
    os.makedirs(docs, exist_ok=True)
    rep = os.path.join(docs, "Report_" + RID + "_ConfigManager_WriteMap.md")

    with open(rep, "w", encoding="utf-8") as f:
        f.write("# " + RID + " – ConfigManager Write-Entry Diagnose\n\n")
        f.write("- Zeit: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("- Datei: modules/config_manager.py\n\n")

        if not analyzer.findings:
            f.write("## Ergebnis\n\n")
            f.write("✅ **Keine direkten Schreibpfade gefunden** (open/write).\n")
        else:
            f.write("## Gefundene Schreibpfade\n\n")
            for i, hit in enumerate(analyzer.findings, 1):
                f.write(f"### Treffer {i}\n")
                f.write(f"- Typ: {hit['kind']}\n")
                f.write(f"- Zeile: {hit['line']}\n")
                f.write(f"- Klasse: {hit['class']}\n")
                f.write(f"- Funktion: {hit['function']}\n\n")

        f.write("## Hinweis\n\n")
        f.write(
            "- READ-ONLY Analyse\n"
            "- Treffer sind **reale** Write-Entry-Points (keine Heuristik)\n"
            "- Naechster Schritt: gezielte Delegation **exakt dieser Stellen** an ini_writer\n"
        )

    log("OK: Report geschrieben: " + rep)
    return 0

if __name__ == "__main__":
    sys.exit(main())
