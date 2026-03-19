from __future__ import annotations

from modules.public_logging import format_info
from modules.public_utils import describe_public_surface


def main() -> int:
    print(format_info("ShrimpDev public showcase entrypoint"))
    print("")
    for line in describe_public_surface():
        print(f"- {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
