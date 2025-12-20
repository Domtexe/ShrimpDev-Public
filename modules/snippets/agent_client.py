from __future__ import annotations
import json, os, socket, time
from pathlib import Path

ADDR = ("127.0.0.1", 9477)
ROOT = Path(r"D:\ShrimpDev")
INBOX = ROOT / "_Reports" / "Agent" / "inbox"

def send_event(ev: dict) -> None:
    ev = dict(ev or {}); ev.setdefault("ts", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    data = json.dumps(ev, ensure_ascii=False).encode("utf-8")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(data, ADDR); s.close()
    except Exception:
        try:
            INBOX.mkdir(parents=True, exist_ok=True)
            (INBOX / f"{int(time.time())}_{os.getpid()}.jsonl").open("a", encoding="utf-8").write(json.dumps(ev, ensure_ascii=False)+"\n")
        except Exception:
            pass
