from __future__ import annotations
from pathlib import Path
from datetime import datetime
import json
import shutil
from typing import Any, Dict, List, Optional, Tuple


OperationEntry = Dict[str, Any]


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def get_journal_dir(root: Path) -> Path:
    """Liefert das Journal-Verzeichnis (_Journal) fuer den angegebenen Root."""
    return root / "_Journal"


def get_trash_dir(root: Path) -> Path:
    """Liefert das Trash-Verzeichnis (_Trash) fuer sichere Deletes."""
    return root / "_Trash"


def _journal_file_for_today(root: Path) -> Path:
    """Journaldatei fuer das aktuelle Datum (moves_YYYYMMDD.jsonl)."""
    today = datetime.now().strftime("%Y%m%d")
    return get_journal_dir(root) / ("moves_" + today + ".jsonl")


def new_batch_id() -> str:
    """Erzeugt eine einfache Batch-ID auf Basis von Datum/Zeit."""
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def new_entry_id() -> str:
    """Erzeugt eine einfache Entry-ID auf Basis von Datum/Zeit."""
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def append_entries(root: Path, entries: List[OperationEntry]) -> Path:
    """Haengt die Operationseintraege als JSON-Lines an die Tages-Journaldatei an."""
    journal_dir = get_journal_dir(root)
    _ensure_dir(journal_dir)
    jf = _journal_file_for_today(root)
    with jf.open("a", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return jf


def plan_delete_batch(
    root: Path,
    user: str,
    src_paths: List[Path],
    reason: str,
    runner_id: Optional[str] = None,
) -> Tuple[str, List[OperationEntry]]:
    """
    Legt einen Delete-Batch im Journal an (Status: planned), ohne das Dateisystem zu veraendern.

    Rueckgabe:
        batch_id, liste_der_eintraege
    """
    now = datetime.now().isoformat(timespec="seconds")
    batch_id = new_batch_id()
    entries: List[OperationEntry] = []
    for src in src_paths:
        entry: OperationEntry = {
            "id": new_entry_id(),
            "timestamp": now,
            "runner_id": runner_id or "",
            "user": user,
            "op_type": "delete",
            "status": "planned",
            "paths": {
                "src": str(src),
                "dst": None,
                "backup": None,
            },
            "meta": {
                "reason": reason,
                "batch_id": batch_id,
            },
        }
        entries.append(entry)

    append_entries(root, entries)
    return batch_id, entries


def apply_delete_batch(root: Path, entries: List[OperationEntry]) -> List[OperationEntry]:
    """
    Fuehrt den Delete-Batch aus:
    - Dateien werden aus src nach _Trash verschoben.
    - status wird auf applied oder failed gesetzt.
    - Aktualisierte Eintraege werden erneut ins Journal geschrieben.
    """
    trash_root = get_trash_dir(root)
    now = datetime.now().isoformat(timespec="seconds")
    updated: List[OperationEntry] = []
    for entry in entries:
        if entry.get("op_type") != "delete":
            updated.append(entry)
            continue
        if entry.get("status") not in ("planned", "retry"):
            updated.append(entry)
            continue

        paths = entry.get("paths", {})
        src_str = paths.get("src") or ""
        src = Path(src_str)

        if not src.exists():
            entry["status"] = "failed"
            meta = entry.setdefault("meta", {})
            meta["error"] = "Quelle existiert nicht"
            entry["timestamp"] = now
            updated.append(entry)
            continue

        # Backup-Pfad berechnen
        try:
            rel = src.relative_to(root)
        except ValueError:
            rel = Path(src.name)

        trash_dir = trash_root / datetime.now().strftime("%Y%m%d") / rel.parent
        _ensure_dir(trash_dir)
        backup_path = trash_dir / rel.name

        try:
            shutil.move(str(src), str(backup_path))
            paths["backup"] = str(backup_path)
            entry["paths"] = paths
            entry["status"] = "applied"
            entry["timestamp"] = now
        except Exception as exc:
            entry["status"] = "failed"
            meta = entry.setdefault("meta", {})
            meta["error"] = "Move nach Trash fehlgeschlagen: " + str(exc)
            entry["timestamp"] = now

        updated.append(entry)

    # Aktualisierte Eintraege erneut ins Journal schreiben
    append_entries(root, updated)
    return updated


def load_all_entries(root: Path) -> List[OperationEntry]:
    """Liest alle Journaldateien unter _Journal ein und gibt alle Eintraege zurueck."""
    journal_dir = get_journal_dir(root)
    if not journal_dir.exists():
        return []
    entries: List[OperationEntry] = []
    for jf in sorted(journal_dir.glob("moves_*.jsonl")):
        try:
            with jf.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        if isinstance(obj, dict):
                            entries.append(obj)
                    except Exception:
                        continue
        except Exception:
            continue
    return entries


# Hinweis:
# Undo-Funktionen (undo_last, undo_batch) werden in einer spaeteren Phase
# auf Basis dieses Journals implementiert. Dieses Modul stellt die Grundlage
# fuer sicheres Logging und Delete-Operationen dar.


# -------------------------------------------------------------------------
# Undo-Funktionen fuer Delete-Batches (R2064)
# -------------------------------------------------------------------------

def _collect_delete_batches(entries):
    batches = {}
    for e in entries:
        if e.get("op_type") != "delete":
            continue
        status = e.get("status")
        if status != "applied":
            continue
        meta = e.get("meta", {})
        batch_id = meta.get("batch_id")
        if not batch_id:
            continue
        batches.setdefault(batch_id, []).append(e)
    return batches


def undo_delete_batch(root, batch_id):
    """
    Macht einen Delete-Batch rueckgaengig, soweit moeglich.

    Regeln:
    - Es werden nur Eintraege mit op_type=delete und status=applied betrachtet.
    - backup muss existieren, src darf nicht existieren.
    - Bei Erfolg: status=undone, bei Fehler: status=failed mit Fehlermeldung.
    - Aktualisierte Eintraege werden erneut ins Journal geschrieben.
    """
    try:
        all_entries = load_all_entries(root)
    except Exception:
        return []

    batches = _collect_delete_batches(all_entries)
    if batch_id not in batches:
        return []

    now = datetime.now().isoformat(timespec="seconds")
    updated = []
    from pathlib import Path as _Path

    for e in batches[batch_id]:
        paths = e.get("paths", {})
        src_str = paths.get("src") or ""
        backup_str = paths.get("backup") or ""
        src = _Path(src_str) if src_str else None
        backup = _Path(backup_str) if backup_str else None

        if backup is None or not backup.exists():
            e["status"] = "failed"
            meta = e.setdefault("meta", {})
            meta["error"] = "Undo nicht moeglich: Backup fehlt"
            e["timestamp"] = now
            updated.append(e)
            continue

        if src is not None and src.exists():
            e["status"] = "failed"
            meta = e.setdefault("meta", {})
            meta["error"] = "Undo nicht moeglich: Ziel existiert bereits"
            e["timestamp"] = now
            updated.append(e)
            continue

        try:
            # Zielverzeichnis sicherstellen
            if src is not None:
                target_dir = src.parent
                from pathlib import Path as _P2
                target_dir.mkdir(parents=True, exist_ok=True)
                import shutil as _sh
                _sh.move(str(backup), str(src))
            e["status"] = "undone"
            e["timestamp"] = now
        except Exception as exc:
            e["status"] = "failed"
            meta = e.setdefault("meta", {})
            meta["error"] = "Undo fehlgeschlagen: " + str(exc)
            e["timestamp"] = now

        updated.append(e)

    if updated:
        append_entries(root, updated)
    return updated


def undo_last_delete_batch(root):
    """
    Sucht den juengsten angewendeten Delete-Batch und fuehrt undo_delete_batch aus.
    Wenn kein passender Batch existiert, wird eine leere Liste zurueckgegeben.
    """
    try:
        all_entries = load_all_entries(root)
    except Exception:
        return []

    batches = _collect_delete_batches(all_entries)
    if not batches:
        return []

    # Juengsten Batch anhand des hoechsten Timestamps bestimmen
    latest_batch_id = None
    latest_ts = None

    for batch_id, entries in batches.items():
        for e in entries:
            ts_str = e.get("timestamp") or ""
            ts_val = ts_str
            if latest_ts is None or ts_val > latest_ts:
                latest_ts = ts_val
                latest_batch_id = batch_id

    if latest_batch_id is None:
        return []

    return undo_delete_batch(root, latest_batch_id)

