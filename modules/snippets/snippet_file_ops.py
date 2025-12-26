"""
snippet_file_ops - R1177b
Sichere Datei-Transaktionen:
- safe_move_with_verify: Copy -> Verify (SHA256) -> Delete
- Journal: JSON Move-Historie für Undo
"""

from __future__ import annotations
import os, shutil, json, hashlib, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOG = os.path.join(ROOT, "debug_output.txt")


def _log(msg: str):
    try:
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] [FileOps] {msg}\n")
    except Exception:
        pass


def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)


def sha256(p: str) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class Journal:
    def __init__(self, path: str):
        self.path = path
        ensure_dir(os.path.dirname(self.path))
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                f.write("[]")

    def _load(self):
        try:
            return json.load(open(self.path, encoding="utf-8"))
        except Exception:
            return []

    def _save(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def append(self, src: str, dst: str):
        data = self._load()
        data.append(
            {"src": src, "dst": dst, "ts": datetime.datetime.now().isoformat(timespec="seconds")}
        )
        self._save(data)

    def pop_last(self):
        data = self._load()
        if not data:
            return None
        item = data.pop()
        self._save(data)
        return item


def safe_move_with_verify(
    src: str, dst: str, *, journal: Journal | None = None, record: bool = True
):
    if not os.path.isfile(src):
        raise FileNotFoundError(src)
    ensure_dir(os.path.dirname(dst))
    tmp = dst + ".tmpcopy"
    shutil.copy2(src, tmp)
    if sha256(src) != sha256(tmp):
        os.remove(tmp)
        raise OSError("Hash mismatch after copy")
    os.replace(tmp, dst)
    os.remove(src)
    if journal and record:
        journal.append(src, dst)
    _log(f"Move OK: {src} -> {dst}")
