# -*- coding: utf-8 -*-
from pathlib import Path
from datetime import datetime
import shutil

RUNNER_ID = "R2855"

CI_YAML = """name: CI

on:
  push:
    branches: [ "main" ]
  pull_request:

jobs:
  sanity:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Python syntax gate
        run: |
          if [ -f main_gui.py ]; then
            python -m py_compile main_gui.py
          fi
          if [ -d modules ]; then
            python -m compileall -q modules
          fi
          if [ -d tools ]; then
            python -m compileall -q tools
          fi

      - name: CI sanity
        run: echo "CI OK"
"""

def now():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def patch(repo: Path):
    wf = repo / ".github" / "workflows" / "ci.yml"
    if not wf.exists():
        return
    arch = repo / "_Archiv"
    arch.mkdir(exist_ok=True)
    shutil.copy2(wf, arch / f"ci.yml.{RUNNER_ID}_{now()}.bak")
    wf.write_text(CI_YAML, encoding="utf-8")

def main():
    root = Path(__file__).resolve().parent.parent
    patch(root)
    pub = root.parent / "ShrimpDev_PUBLIC_EXPORT"
    if pub.exists():
        patch(pub)
    print(f"[{RUNNER_ID}] OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
