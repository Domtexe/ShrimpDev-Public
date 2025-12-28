import sys
import subprocess
from datetime import datetime
from pathlib import Path

RID = "R2414"


def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def now_human() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_text(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def run_py(py_path: Path, cwd: Path, report: list[str]) -> int:
    report.append(f"$ python {py_path.name}")
    cp = subprocess.run(
        [sys.executable, str(py_path)], cwd=str(cwd), text=True, capture_output=True
    )
    if cp.stdout.strip():
        report.append(cp.stdout.strip())
    if cp.stderr.strip():
        report.append(cp.stderr.strip())
    report.append(f"Exit: {cp.returncode}")
    report.append("")
    return cp.returncode


def main() -> int:
    tools_dir = Path(__file__).resolve().parent
    root = tools_dir.parent
    docs = root / "docs"

    r2412_py = tools_dir / "R2691.py"
    r2411_py = tools_dir / "R2692.py"

    report: list[str] = []
    report.append(f"[{RID}] Autopush BOTH (Private -> Public)")
    report.append(f"Time: {now_human()}")
    report.append(f"Root: {root}")
    report.append("")

    if not r2412_py.exists():
        report.append("ERROR: tools/R2691.py missing")
        rp = docs / f"Report_{RID}_AutopushBoth_{ts()}.md"
        write_text(rp, "\n".join(report) + "\n")
        print(f"[{RID}] ERROR: Report {rp}")
        return 2
    if not r2411_py.exists():
        report.append("ERROR: tools/R2692.py missing")
        rp = docs / f"Report_{RID}_AutopushBoth_{ts()}.md"
        write_text(rp, "\n".join(report) + "\n")
        print(f"[{RID}] ERROR: Report {rp}")
        return 3

    rc = run_py(r2412_py, root, report)
    if rc != 0:
        report.append("STOP: Private push failed; skipping public.")
        rp = docs / f"Report_{RID}_AutopushBoth_{ts()}.md"
        write_text(rp, "\n".join(report) + "\n")
        print(f"[{RID}] ERROR: Report {rp}")
        return 10

    rc = run_py(r2411_py, root, report)
    rp = docs / f"Report_{RID}_AutopushBoth_{ts()}.md"
    write_text(rp, "\n".join(report) + "\n")

    if rc != 0:
        print(f"[{RID}] ERROR: public failed. Report {rp}")
        return 11

    print(f"[{RID}] OK: Report {rp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
