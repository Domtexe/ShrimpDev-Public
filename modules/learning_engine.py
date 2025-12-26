from __future__ import annotations

"""
learning_engine.py - LearningEngine Core (Phase C)

Dieses Modul stellt eine stabile, rückwärtskompatible API bereit,
um Ereignisse aus ShrimpDev (Intake, Runner, Gates) im
learning_journal.json zu protokollieren und einfache Auswertungen
zu ermöglichen.

Es arbeitet rein dateibasiert:
- Journal: <project_root>/learning_journal.json
- Keine Netzwerkzugriffe, keine Fremdabhängigkeiten.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Datenstrukturen
# ---------------------------------------------------------------------------


@dataclass
class JournalEntry:
    """
    Repräsentiert einen Eintrag im LearningJournal.
    """

    id: str
    timestamp: str
    event: str
    payload: dict[str, Any]
    type: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "event": self.event,
            "payload": self.payload,
            "type": self.type,
        }


# ---------------------------------------------------------------------------
# Pfad-Utilities
# ---------------------------------------------------------------------------


def _get_project_root() -> Path:
    """
    Bestimmt das Projekt-Root relativ zu diesem Modul.

    Erwartete Struktur:
    modules/
        learning_engine.py
    learning_journal.json  (im Projekt-Root)
    """
    # modules/learning_engine.py -> modules -> project_root
    return Path(__file__).resolve().parent.parent


def _get_journal_path() -> Path:
    """
    Liefert den Pfad zur learning_journal.json im Projekt-Root.
    """
    return _get_project_root() / "learning_journal.json"


def _get_debug_log_path() -> Path:
    """
    Liefert den Pfad zur zentralen Debug-Logdatei.
    """
    return _get_project_root() / "debug_output.txt"


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


def _log_debug(message: str) -> None:
    """
    Schreibt eine Debugzeile in debug_output.txt.
    Fehler beim Loggen dürfen niemals das Programm abbrechen.
    """
    try:
        log_path = _get_debug_log_path()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[learning_engine] {ts} {message}"
        with log_path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        # Niemals Exceptions durch Logging nach außen lecken
        pass


# ---------------------------------------------------------------------------
# Journal-Lade-/Speicherlogik
# ---------------------------------------------------------------------------


def _load_journal() -> dict[str, Any]:
    """
    Lädt das LearningJournal aus der JSON-Datei.

    Rückgabeformat:
    {
        "entries": [ ... ]
    }

    Falls die Datei nicht existiert oder defekt ist, wird eine
    minimale Struktur zurückgegeben.
    """
    path = _get_journal_path()
    if not path.is_file():
        _log_debug("Journal nicht gefunden - neue Struktur wird angelegt.")
        return {"entries": []}

    try:
        import json

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError("Journal-Root ist kein Dict")
        if "entries" not in data or not isinstance(data["entries"], list):
            raise ValueError("Journal hat keine gültige 'entries'-Liste")

        return data
    except Exception as exc:
        _log_debug(f"Journal-Laden fehlgeschlagen: {exc!r} - verwende leere Struktur.")
        return {"entries": []}


def _save_journal(data: dict[str, Any]) -> None:
    """
    Speichert die Journal-Daten sicher in die learning_journal.json.
    """
    path = _get_journal_path()
    try:
        import json

        # Ordner sicherstellen
        path.parent.mkdir(parents=True, exist_ok=True)

        # Optional: kleines Backup anlegen, falls bereits Datei existiert
        if path.is_file():
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup = path.with_suffix(f".{ts}.bak")
            try:
                path.replace(backup)
            except Exception:
                # Wenn Backup fehlschlägt, trotzdem schreiben
                pass

        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    except Exception as exc:
        _log_debug(f"Journal-Speichern fehlgeschlagen: {exc!r}")


def _next_entry_id(entries: list[dict[str, Any]]) -> str:
    """
    Ermittelt die nächste numerische ID im Format 'NNN' (z. B. '029').

    Betrachtet alle vorhandenen Einträge und erhöht die höchste
    numerische ID um 1. Falls keine gültige ID gefunden wird, startet
    die Zählung bei '001'.
    """
    max_id = 0
    for entry in entries:
        raw_id = str(entry.get("id", "") or "").strip()
        try:
            value = int(raw_id)
            if value > max_id:
                max_id = value
        except Exception:
            continue
    return f"{max_id + 1:03d}"


def _classify_type(event_type: str) -> str:
    """
    Leichte Heuristik, um den Typ eines Eintrags zu klassifizieren.
    """
    et = event_type.lower().strip()
    if et.startswith("intake_"):
        return "intake"
    if et.startswith("runner_"):
        return "runner"
    if et.startswith("gate_"):
        return "gate"
    if et.startswith("app_"):
        return "analysis"
    return "event"


def _normalize_entry_dict(raw: dict[str, Any]) -> JournalEntry:
    """
    Normalisiert ein rohes Entry-Dict in einen JournalEntry.
    Fehlende Felder werden ergänzt.
    """
    timestamp = str(raw.get("timestamp") or datetime.now().isoformat())
    event = str(raw.get("event") or "unknown")
    payload = raw.get("payload") or {}
    if not isinstance(payload, dict):
        payload = {"value": payload}

    entry_type = str(raw.get("type") or _classify_type(event))

    # ID erst einmal leer; wird in append_entry gesetzt
    entry_id = str(raw.get("id") or "").strip() or "000"

    return JournalEntry(
        id=entry_id,
        timestamp=timestamp,
        event=event,
        payload=payload,
        type=entry_type,
    )


# ---------------------------------------------------------------------------
# Öffentliche API
# ---------------------------------------------------------------------------


def learn_from_event(event_type: str, payload: dict[str, Any] | None = None) -> JournalEntry:
    """
    Protokolliert ein Ereignis im LearningJournal.

    - event_type: z. B. "intake_detect", "intake_save", "runner_executed", "syntax_error".
    - payload: zusätzliche Informationen (Name, Ext, Pfad, Runner-ID, etc.)

    Rückgabe:
    - Der tatsächlich gespeicherte JournalEntry (inkl. finaler ID).
    """
    payload = payload or {}
    raw_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "payload": payload,
        "type": _classify_type(event_type),
    }

    data = _load_journal()
    entries = data.get("entries") or []
    if not isinstance(entries, list):
        entries = []

    # Normalisieren
    entry = _normalize_entry_dict(raw_entry)
    # ID setzen
    entry.id = _next_entry_id(entries)

    entries.append(entry.to_dict())
    data["entries"] = entries

    _save_journal(data)
    _log_debug(
        f"learn_from_event: {entry.event} id={entry.id} payload_keys={list(entry.payload.keys())}"
    )

    return entry


def update_journal(entry_data: dict[str, Any]) -> JournalEntry:
    """
    Fügt einen spezifischen Eintrag in das Journal ein.

    Anders als learn_from_event kann hier ein fast fertiger Eintrag mit
    eigenen Feldern übergeben werden. ID und Typ werden ggf. angepasst.

    Rückgabe:
    - Der tatsächlich gespeicherte JournalEntry (inkl. finaler ID).
    """
    data = _load_journal()
    entries = data.get("entries") or []
    if not isinstance(entries, list):
        entries = []

    raw = dict(entry_data)
    # Fallbacks
    raw.setdefault("timestamp", datetime.now().isoformat())
    raw.setdefault("event", "custom")
    raw.setdefault("payload", {})
    raw.setdefault("type", _classify_type(str(raw.get("event") or "custom")))

    entry = _normalize_entry_dict(raw)
    # ID neu vergeben
    entry.id = _next_entry_id(entries)

    entries.append(entry.to_dict())
    data["entries"] = entries
    _save_journal(data)

    _log_debug(f"update_journal: {entry.event} id={entry.id}")
    return entry


def get_journal_snapshot() -> dict[str, Any]:
    """
    Liefert einen Schnappschuss der Journal-Daten.

    Rückgabe:
    {
        "entries": [...],
        "counts_by_event": { "intake_detect": 10, ... },
        "total": 28
    }
    """
    data = _load_journal()
    entries = data.get("entries") or []
    if not isinstance(entries, list):
        entries = []

    counts_by_event: dict[str, int] = {}
    for entry in entries:
        ev = str(entry.get("event") or "unknown")
        counts_by_event[ev] = counts_by_event.get(ev, 0) + 1

    return {
        "entries": entries,
        "counts_by_event": counts_by_event,
        "total": len(entries),
    }


def suggest_improvements(context: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """
    Liefert einfache Verbesserungsvorschläge auf Basis des Journals.

    Der Algorithmus ist bewusst leichtgewichtig und defensiv:
    - Es werden nur grobe Muster betrachtet (z. B. viele Wiederholungen
      eines bestimmten Ereignistyps).
    - Falls keine sinnvollen Hinweise ableitbar sind, wird eine leere
      Liste zurückgegeben.

    Rückgabe:
    - Liste von Dicts mit mindestens:
      { "kind": "...", "message": "...", "weight": float }
    """
    snapshot = get_journal_snapshot()
    total = snapshot.get("total", 0)
    counts_by_event = snapshot.get("counts_by_event", {})

    suggestions: list[dict[str, Any]] = []

    if not total:
        return suggestions

    # Beispiel-Heuristik: Sehr häufige Detect-Events -> vielleicht Auto-Detect?
    detect_count = 0
    for key, value in counts_by_event.items():
        if "detect" in key:
            detect_count += value

    if detect_count >= 10:
        suggestions.append(
            {
                "kind": "intake_detect",
                "message": (
                    "Es wurden sehr viele Detect-Vorgänge protokolliert. "
                    "Evtl. lohnt sich ein Auto-Detect beim Laden oder Speichern."
                ),
                "weight": 0.6,
            }
        )

    # Beispiel-Heuristik: Viele Runs -> Hinweis auf bevorzugte Runner-Historie
    run_like = 0
    for key, value in counts_by_event.items():
        if "run" in key:
            run_like += value

    if run_like >= 5:
        suggestions.append(
            {
                "kind": "runner_usage",
                "message": (
                    "Viele Run-Vorgänge wurden protokolliert. "
                    "Evtl. könnte eine 'Zuletzt ausgeführt'-Liste oder ein "
                    "Runner-Favoritensystem hilfreich sein."
                ),
                "weight": 0.5,
            }
        )

    # Kontextabhängige Hinweise (falls vorhanden)
    ctx_source = (context or {}).get("source")
    if ctx_source == "intake":
        suggestions.append(
            {
                "kind": "context",
                "message": (
                    "Kontext: Aufruf aus dem Intake. "
                    "Eine Integration von LearningEngine-Hinweisen direkt im "
                    "Intake-Tab (z. B. neben den LEDs) könnte sinnvoll sein."
                ),
                "weight": 0.3,
            }
        )

    return suggestions
