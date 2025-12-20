
# R2044 – Logging Snippet fuer neue Runner
from pathlib import Path
from datetime import datetime
from modules.config_loader import ConfigLoader

def log_runner(msg: str):
    try:
        root = Path(__file__).resolve().parent.parent
        cfg = ConfigLoader(root / "ShrimpDev.ini")
        do_log = cfg.get_logging_bool("runner_debug", True)
        use_ts = cfg.get_logging_bool("timestamps", True)

        if not do_log:
            return

        if use_ts:
            msg = f"{datetime.now().isoformat()} " + msg

        log_path = root / "debug_output.txt"
        # R2045: Logrotation
        try:
            max_size_mb = int(cfg._config.get("logging", "max_size_mb", fallback="5"))
        except Exception:
            max_size_mb = 5
        try:
            rotations = int(cfg._config.get("logging", "rotations", fallback="5"))
        except Exception:
            rotations = 5
        if max_size_mb < 1:
            max_size_mb = 1
        if rotations < 1:
            rotations = 1

        def _rotate_log(path, max_mb, max_rot):
            try:
                max_bytes = max_mb * 1024 * 1024
                if not path.exists() or path.stat().st_size <= max_bytes:
                    return
                oldest = Path(str(path) + f".{max_rot}")
                if oldest.exists():
                    oldest.unlink()
                for idx in range(max_rot - 1, 0, -1):
                    src = Path(str(path) + f".{idx}")
                    if src.exists():
                        dst = Path(str(path) + f".{idx+1}")
                        src.rename(dst)
                backup_path = Path(str(path) + ".1")
                if path.exists():
                    path.rename(backup_path)
            except Exception:
                pass

        _rotate_log(log_path, max_size_mb, rotations)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        pass
