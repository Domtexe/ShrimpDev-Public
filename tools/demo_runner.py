from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.public_logging import format_info, format_section
from modules.public_utils import bullet_lines, describe_public_surface


def build_demo_output(name: str) -> str:
    lines: list[str] = []
    lines.append("# Demo Runner")
    lines.append("")
    lines.append(format_info(f"Hello {name}"))
    lines.append("")
    lines.append(format_section("Summary"))
    lines.append(f"- timestamp_utc: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    lines.append("- runner_type: public_demo")
    lines.append("- internal_coupling: none")
    lines.append("")
    lines.append(format_section("Public Surface"))
    lines.append(bullet_lines(describe_public_surface()))
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Public-safe ShrimpDev demo runner")
    parser.add_argument("--name", default="public-user")
    args = parser.parse_args()
    print(build_demo_output(str(args.name).strip() or "public-user"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
