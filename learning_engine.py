# -*- coding: utf-8 -*-
"""
LearningEngine – Phase C

Diese Implementierung ist defensiv und kapselt die Arbeit mit dem LearningJournal.
Sie ist so gebaut, dass sie ShrimpDev nicht zerstoert, selbst wenn es Fehler im
Journal gibt. Sie kann spaeter erweitert werden, ohne Intake zu beeinflussen.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


LEARNING_JOURNAL_FILENAME = "learning_journal.json"


@dataclass
class JournalEntry:
    id: str
    timestamp: str
    event: str
    payload: Dict[str, Any]
    type: str


@dataclass
class LearningEngineConfig:
    project_root: Path
    journal_path: Path

    @classmethod
    def from_project_root(cls, project_root: Path) -> "LearningEngineConfig":
        journal_path = project_root / LEARNING_JOURNAL_FILENAME
        return cls(project_root=project_root, journal_path=journal_path)


# ---------------------------------------------------------------------------#
# Interne Utils
# ---------------------------------------------------------------------------#


def _get_project_root() -> Path:
    """Bestimme das Projekt-Root anhand dieser Datei."""
    return Path(__file__).resolve().parent


def _load_journal(cfg: LearningEngineConfig) -> Dict[str, Any]:
    """Journal-Datei defensiv laden."""
    if not cfg.journal_path.is_file():
        return {"entries": []}
    try:
        with cfg.journal_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {"entries": []}
        if "entries" not in data or not isinstance(data["entries"], list):
            data["entries"] = []
        return data
    except Exception:
        # Im Fehlerfall nicht abstuerzen, sondern mit leerem Journal weiterarbeiten
        return {"entries": []}


def _save_journal(cfg: LearningEngineConfig, data: Dict[str, Any]) -> None:
    """Journal-Datei sicher speichern."""
    cfg.journal_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = cfg.journal_path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(cfg.journal_path)


def _normalize_entry_dict(raw: Dict[str, Any]) -> JournalEntry:
    """Dict aus der App in ein JournalEntry-Objekt umwandeln."""
    event_id = str(raw.get("id") or "").zfill(3) if raw.get("id") else "000"
    return JournalEntry(
        id=event_id,
        timestamp=str(raw.get("timestamp") or datetime.now().isoformat()),
        event=str(raw.get("event") or "unknown"),
        payload=dict(raw.get("payload") or {}),
        type=str(raw.get("type") or "analysis"),
    )


def _next_entry_id(entries: List[Dict[str, Any]]) -> str:
    """Naechste ID als 3-stellige Zeichenkette bestimmen."""
    max_id = 0
    for e in entries:
        try:
            v = int(str(e.get("id", "0")))
        except Exception:
            v = 0
        max_id = max(max_id, v)
    return f"{max_id + 1:03d}"


def _classify_type(event_type: str) -> str:
    """Einfache Event-Typ-Klassifikation (kann spaeter erweitert werden)."""
    if event_type.startswith("app_"):
        return "analysis"
    if event_type.startswith("intake_"):
        return "intake"
    if event_type.startswith("runner_"):
        return "runner"
    return "analysis"


# ---------------------------------------------------------------------------#
# Oeffentliche API-Funktionen
# ---------------------------------------------------------------------------#


def learn_from_event(event_type: str, payload: Optional[Dict[str, Any]] = None) -> JournalEntry:
    """
    Protokolliert ein Ereignis im LearningJournal.

    - event_type: z. B. "intake_detect", "intake_save", "runner_executed", "syntax_error".
    - payload: zusaetzliche Informationen (Name, Ext, Pfad, Runner-ID, etc.)

    Rueckgabe:
    - Der gespeicherte JournalEntry (inkl. finaler ID).
    """
    cfg = LearningEngineConfig.from_project_root(_get_project_root())
    data = _load_journal(cfg)

    entries: List[Dict[str, Any]] = list(data.get("entries") or [])
    payload = payload or {}

    raw_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "payload": payload,
        "type": _classify_type(event_type),
    }

    # Normalisieren & ID vergeben
    entry_obj = _normalize_entry_dict(raw_entry)
    entry_obj.id = _next_entry_id(entries)
    entries.append(asdict(entry_obj))

    data["entries"] = entries
    _save_journal(cfg, data)

    return entry_obj


def get_journal_snapshot() -> Dict[str, Any]:
    """
    Liefert eine kompakte Zusammenfassung des LearningJournals fuer Runner/Diagnose.
    """
    cfg = LearningEngineConfig.from_project_root(_get_project_root())
    data = _load_journal(cfg)
    entries: List[Dict[str, Any]] = list(data.get("entries") or [])

    counts = {}
    for e in entries:
        et = str(e.get("event") or "unknown")
        counts[et] = counts.get(et, 0) + 1

    return {
        "entries_total": len(entries),
        "events_by_type": counts,
        "examples": entries[-5:],  # letzte 5 Eintraege
    }


def update_journal(transform_fn, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Erlaubt spaetere Transformations-Runner (z. B. Aufraeumen, Migrationen).
    transform_fn bekommt (data, context) und gibt neues data zurueck.
    """
    cfg = LearningEngineConfig.from_project_root(_get_project_root())
    data = _load_journal(cfg)
    try:
        new_data = transform_fn(data, context or {})
        if not isinstance(new_data, dict):
            raise ValueError("Transform-Funktion hat kein Dict geliefert.")
        _save_journal(cfg, new_data)
        return new_data
    except Exception:
        # Im Fehlerfall das alte Journal unveraendert lassen.
        return data


def suggest_improvements() -> Dict[str, Any]:
    """
    Platzhalter fuer spaetere Heuristiken / Verbesserungsvorschlaege.
    Aktuell nur simple Auswertung der Events.
    """
    snapshot = get_journal_snapshot()
    hints: List[str] = []

    if snapshot["entries_total"] == 0:
        hints.append("Keine Eintraege im LearningJournal – es gibt noch nichts auszuwerten.")
    if snapshot["events_by_type"].get("syntax_error", 0) > 0:
        hints.append(
            "Es wurden Syntaxfehler protokolliert – Intake-Patches sollten vorsichtig sein."
        )
    if snapshot["events_by_type"].get("intake_detect", 0) == 0:
        hints.append("Noch keine Intake-Erkennungsereignisse – ggf. Testszenarien anlegen.")

    return {
        "snapshot": snapshot,
        "hints": hints,
    }
