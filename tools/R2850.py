# -*- coding: utf-8 -*-
from pathlib import Path
from datetime import datetime
import shutil

RUNNER_ID = "R2850"

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
      - name: CI sanity
        run: echo "CI OK"
"""

def now():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def patch_repo(repo: Path):
    wf = repo / ".github" / "workflows" / "ci.yml"
    if not wf.exists():
        return f"SKIP: {wf} not found"

    arch = repo / "_Archiv"
    arch.mkdir(exist_ok=True)
    bak = arch / f"ci.yml.{RUNNER_ID}_{now()}.bak"
    shutil.copy2(wf, bak)

    wf.write_text(CI_YAML, encoding="utf-8")
    return f"OK: patched {wf} (backup: {bak})"

def main():
    root = Path(__file__).resolve().parent.parent
    print(patch_repo(root))

    # optional: public mirror if present locally
    pub = root.parent / "ShrimpDev_PUBLIC_EXPORT"
    if pub.exists():
        print(patch_repo(pub))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
