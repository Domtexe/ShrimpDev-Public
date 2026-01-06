# D:\ShrimpDev\tools\shrimpdev_event.py
from __future__ import annotations
import os, json, socket, argparse, time
from pathlib import Path

PORT = int(os.environ.get("SHRIMPDEV_PORT", "9488"))
ADDR = ("127.0.0.1", PORT)
ROOT = Path(r"D:\ShrimpDev")
INBOX = ROOT / "Reports" / "Agent" / "inbox"


def send_event(ev: dict):
    ev = dict(ev or {})
    ev.setdefault("ts", time.strftime("%m-%d %H:%M:%S", time.localtime()))
    data = json.dumps(ev, ensure_ascii=False).encode("utf-8")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(data, ADDR)
        s.close()
        return True
    except Exception:
        try:
            INBOX.mkdir(parents=True, exist_ok=True)
            (INBOX / f"{int(time.time())}_{os.getpid()}.jsonl").open("a", encoding="utf-8").write(
                json.dumps(ev, ensure_ascii=False) + "\n"
            )
            return True
        except Exception:
            return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runner", required=True)
    ap.add_argument("--level", default="INFO")
    ap.add_argument("--msg", required=True)
    ap.add_argument("--data", help="JSON-String oder Pfad zu .json")
    args = ap.parse_args()

    payload = {"runner": args.runner, "level": args.level, "msg": args.msg}
    if args.data:
        try:
            if os.path.isfile(args.data):
                payload["data"] = json.loads(Path(args.data).read_text(encoding="utf-8"))
            else:
                payload["data"] = json.loads(args.data)
        except Exception:
            payload["data"] = {"raw": args.data}

    ok = send_event(payload)
    if not ok:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
