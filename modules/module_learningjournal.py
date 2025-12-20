"""
module_learningjournal - LearningJournal Tab fuer ShrimpDev

Dieses Modul stellt eine robuste, eigenstaendige Implementierung bereit,
um den LearningJournal-Tab aufzubauen und learning_journal.json anzuzeigen.

Haupt-Einstieg:
    build_learningjournal_tab(parent, app)

Verhalten:
- Sucht learning_journal.json im Projekt-Root oder unter data/.
- Laedt JSON defensiv:
    * Liste von Eintraegen
    * oder Dict -> wird in eine Liste konvertiert
- Zeigt Eintraege links als Liste (Listbox).
- Zeigt den ausgewaehlten Eintrag rechts als formatierten JSON-Text.
- Fehler (keine Datei, JSON-Fehler, etc.) werden im UI angezeigt und geloggt.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

import tkinter as tk
from tkinter import ttk
from collections import Counter
import subprocess



ROOT = Path(__file__).resolve().parent.parent
LOG_FILE_NAME = "debug_output.txt"


def _log(message: str) -> None:
    """Schreibt eine Debugzeile nach stdout und in debug_output.txt."""
    from datetime import datetime
    line = "[module_learningjournal] {} {}".format(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        message,
    )
    print(line)
    try:
        with (ROOT / LOG_FILE_NAME).open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        # Logging darf die GUI nicht zerstoeren
        pass


def _find_journal_file() -> Tuple[Optional[Path], str]:
    """
    Versucht, die learning_journal.json zu finden.

    Rueckgabe:
        (pfad_oder_none, info_text)
    """
    candidates = [
        ROOT / "learning_journal.json",
        ROOT / "data" / "learning_journal.json",
    ]
    for p in candidates:
        if p.is_file():
            return p, "Verwende Datei: {}".format(p)
    # Nichts gefunden -> wir liefern den ersten Pfad als "Ziel",
    # aber melden, dass er nicht existiert.
    return None, "Keine learning_journal.json gefunden. Erwartet unter:\n - {}\n - {}".format(
        candidates[0],
        candidates[1],
    )


def _normalize_entries(data: Any) -> List[Dict[str, Any]]:
    """
    Versucht, beliebige JSON-Struktur in eine Liste von Dicts umzuwandeln.

    Regeln:
    - Liste[Dict] -> direkt zurueck
    - Dict mit "entries" -> entries
    - Dict -> Liste von {"key": k, "value": v} fuer Items
    - alles andere -> leere Liste
    """
    if isinstance(data, list):
        entries: List[Dict[str, Any]] = []
        for itm in data:
            if isinstance(itm, dict):
                entries.append(itm)
            else:
                entries.append({"value": itm})
        return entries

    if isinstance(data, dict):
        if "entries" in data and isinstance(data["entries"], list):
            return _normalize_entries(data["entries"])
        # generisches Dict -> in Liste von key/value-Dicts umwandeln
        entries: List[Dict[str, Any]] = []
        for k, v in data.items():
            if isinstance(v, dict):
                entry = {"key": k}
                entry.update(v)
                entries.append(entry)
            else:
                entries.append({"key": k, "value": v})
        return entries

    # alles andere
    return []


def _load_learning_journal() -> Tuple[List[Dict[str, Any]], str]:
    """
    Laedt das LearningJournal aus der JSON-Datei.

    Rueckgabe:
        (entries, info_text)

    info_text enthaelt Hinweistexte (z. B. Pfad, Fehlerhinweise).
    """
    path, info = _find_journal_file()
    if path is None:
        _log("learning_journal.json nicht gefunden.")
        return [], info

    try:
        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as exc:
        msg = "Fehler beim Lesen von {}: {}".format(path, exc)
        _log(msg)
        return [], msg

    entries = _normalize_entries(raw)
    _log("LearningJournal geladen: {} Eintraege aus {}".format(len(entries), path))
    return entries, info




def learning_log_event(event_type: str, message: str, data: Optional[Dict[str, Any]] = None) -> None:
    """Appendiert einen Eintrag in die learning_journal.json.

    - event_type: z.B. "runner", "error", "fix", "meta"
    - message:   kurze Beschreibung
    - data:      optionale strukturierte Zusatzdaten

    Die Funktion ist defensiv implementiert: Fehler werden geloggt,
    aber niemals nach aussen geworfen, damit sie die GUI nicht stoert.
    """
    try:
        import datetime as _dt  # lokaler Import, um Abhaengigkeiten minimal zu halten

        # Pfad bestimmen (bestehende Logik wiederverwenden)
        path, _info = _find_journal_file()
        if path is None:
            path = ROOT / "learning_journal.json"

        # Bestehende Daten laden (falls vorhanden)
        if path.exists():
            try:
                with path.open("r", encoding="utf-8") as f:
                    raw = json.load(f)
            except Exception as exc:
                _log(
                    f"learning_log_event: Fehler beim Lesen von {path}: {exc} - neues Journal wird angelegt."
                )
                raw = {"entries": []}
        else:
            raw = {"entries": []}

        # entries-Liste extrahieren
        if isinstance(raw, dict) and isinstance(raw.get("entries"), list):
            entries = list(raw["entries"])
        elif isinstance(raw, list):
            entries = list(raw)
        else:
            entries = []

        # naechste ID bestimmen
        next_id = 1
        for e in entries:
            v = e.get("id")
            try:
                n = int(str(v))
            except Exception:
                continue
            if n >= next_id:
                next_id = n + 1

        timestamp = _dt.datetime.now().isoformat(sep=" ", timespec="microseconds")

        entry: Dict[str, Any] = {
            "id": f"{next_id:03d}",
            "timestamp": timestamp,
            "type": event_type,
            "message": message,
            "event": {
                "name": event_type,
                "category": event_type,
            },
            "meta": {
                "source": "ShrimpDev",
                "created_by": "LearningEngine",
            },
        }

        if data is not None:
            if isinstance(data, dict):
                entry["data"] = data
            else:
                entry["data"] = {"value": data}

        entries.append(entry)

        # Journal sicher schreiben (.tmp + replace)
        new_raw = {"entries": entries}
        tmp = path.with_suffix(path.suffix + ".tmp")
        try:
            with tmp.open("w", encoding="utf-8") as f:
                json.dump(new_raw, f, indent=2, ensure_ascii=False)
            tmp.replace(path)
        except Exception as exc:
            _log(f"learning_log_event: Fehler beim Schreiben von {path}: {exc}")
            try:
                if tmp.exists():
                    tmp.unlink()
            except Exception:
                pass
            return

        _log(f"Learning-Eintrag geschrieben: type={event_type}, id={entry['id']}")
    except Exception as exc:
        _log(f"learning_log_event: unerwarteter Fehler: {exc}")
def _build_stats_text(entries: List[Dict[str, Any]]) -> str:
    'Kompakte Statistikzeile fuer das LearningJournal.'
    if not entries:
        return 'Keine Eintraege vorhanden.'

    events: List[str] = []
    error_count = 0
    for e in entries:
        level = str(e.get('level') or '').lower()
        if level in ('error', 'critical', 'warn', 'warning'):
            error_count += 1

        ev = e.get('event')
        if isinstance(ev, dict):
            name = ev.get('name') or ev.get('category') or ''
            ev_str = str(name or '').strip()
            if not ev_str:
                ev_str = str(e.get('type') or 'unknown')
        else:
            ev_str = str(ev or e.get('type') or 'unknown')
        events.append(ev_str or 'unknown')

    counts = Counter(events)
    total = len(entries)

    most_common = counts.most_common(3)
    parts = [f'{name}={cnt}' for name, cnt in most_common]

    base = f'Eintraege: {total}'
    if parts:
        base = base + ' | ' + ', '.join(parts)
    if error_count:
        base = base + f' | errors={error_count}'
    return base


def _summarize_entry(idx: int, entry: Dict[str, Any]) -> str:
    """
    Erzeugen eines kurzen Labels fuer die linke Liste.

    Bevorzugte Keys:
        "title", "name", "id", "timestamp", "date"
    """
    for key in ("title", "name", "id", "timestamp", "date"):
        if key in entry and entry[key]:
            return "{:03d} - {}".format(idx + 1, str(entry[key]))
    # Fallback: erste paar Keys anzeigen
    keys = list(entry.keys())
    if keys:
        return "{:03d} - {{...}} ({})".format(idx + 1, ", ".join(keys[:3]))
    return "{:03d} - <leer>".format(idx + 1)


def _format_entry_json(entry: Dict[str, Any]) -> str:
    """
    JSON-Pretty-Print fuer einen Eintrag. Nutzt ensure_ascii=False, damit Umlaute sichtbar bleiben.
    """
    try:
        return json.dumps(entry, indent=2, ensure_ascii=False)
    except Exception as exc:
        return "Fehler beim Formatieren des Eintrags:\n{}\n\nRohdaten:\n{}".format(
            exc,
            repr(entry),
        )


def build_learningjournal_tab(parent: tk.Frame, app: tk.Misc) -> None:
    root = parent.winfo_toplevel()

    parent.grid_rowconfigure(1, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    header = ttk.Frame(parent)
    header.grid(row=0, column=0, sticky='ew', padx=8, pady=(8, 4))
    header.columnconfigure(0, weight=0)
    header.columnconfigure(1, weight=0)
    header.columnconfigure(2, weight=1)
    header.columnconfigure(3, weight=0)
    header.columnconfigure(4, weight=0)

    lbl_title = ttk.Label(header, text='LearningJournal')
    lbl_title.grid(row=0, column=0, sticky='w')

    btn_reload = ttk.Button(header, text='Neu laden')
    btn_reload.grid(row=0, column=3, sticky='e', padx=(4, 0))

    btn_diag = ttk.Button(header, text='Diagnose (R1802)')
    btn_diag.grid(row=0, column=4, sticky='e', padx=(4, 0))

    info_var = tk.StringVar(value='')
    lbl_info = ttk.Label(header, textvariable=info_var, anchor='w')
    lbl_info.grid(row=1, column=0, columnspan=5, sticky='w', pady=(4, 0))

    stats_var = tk.StringVar(value='')
    lbl_stats = ttk.Label(header, textvariable=stats_var, anchor='w')
    lbl_stats.grid(row=2, column=0, columnspan=5, sticky='w', pady=(2, 0))

    filter_var = tk.StringVar(value='alle')
    search_var = tk.StringVar(value='')

    lbl_filter = ttk.Label(header, text='Filter:')
    lbl_filter.grid(row=3, column=0, sticky='w', pady=(4, 0))

    combo_filter = ttk.Combobox(
        header,
        textvariable=filter_var,
        state='readonly',
        values=['alle', 'error', 'runner', 'intake', 'meta'],
    )
    combo_filter.grid(row=3, column=1, sticky='w', pady=(4, 0))

    lbl_search = ttk.Label(header, text='Suche:')
    lbl_search.grid(row=3, column=2, sticky='e', pady=(4, 0))

    entry_search = ttk.Entry(header, textvariable=search_var)
    entry_search.grid(row=3, column=3, sticky='ew', pady=(4, 0))

    btn_reset = ttk.Button(header, text='Reset')
    btn_reset.grid(row=3, column=4, sticky='e', padx=(4, 0), pady=(4, 0))
    btn_scans = ttk.Button(header, text='Scans')
    btn_scans.grid(row=4, column=4, sticky='e', padx=(4, 0), pady=(4, 0))

    paned = ttk.Panedwindow(parent, orient='horizontal')
    paned.grid(row=1, column=0, sticky='nsew', padx=8, pady=(4, 8))

    frame_left = ttk.Frame(paned)
    paned.add(frame_left, weight=1)

    lbl_list = ttk.Label(frame_left, text='Eintraege')
    lbl_list.pack(anchor='w')

    listbox = tk.Listbox(frame_left, exportselection=False, height=20)
    listbox.pack(side='left', fill='both', expand=True, pady=(2, 0))

    scroll_list = ttk.Scrollbar(frame_left, orient='vertical', command=listbox.yview)
    scroll_list.pack(side='right', fill='y')
    listbox.configure(yscrollcommand=scroll_list.set)

    frame_right = ttk.Frame(paned)
    paned.add(frame_right, weight=3)

    lbl_detail = ttk.Label(frame_right, text='Details / JSON')
    lbl_detail.pack(anchor='w')

    text_detail = tk.Text(frame_right, wrap='word', height=20)
    text_detail.pack(side='left', fill='both', expand=True, pady=(2, 0))

    scroll_detail = ttk.Scrollbar(frame_right, orient='vertical', command=text_detail.yview)
    scroll_detail.pack(side='right', fill='y')
    text_detail.configure(yscrollcommand=scroll_detail.set)

    state = {
        'entries': [],
        'filtered': [],
    }

    def set_detail_text(text: str) -> None:
        text_detail.configure(state='normal')
        text_detail.delete('1.0', 'end')
        text_detail.insert('1.0', text)
        text_detail.configure(state='disabled')

    def _matches_filter(entry: dict, mode: str, search_text: str) -> bool:
        try:
            if not mode or mode == 'alle':
                mode_ok = True
            else:
                ev = str(entry.get('event') or entry.get('type') or '').lower()
                level = str(entry.get('level') or '').lower()
                if mode == 'error':
                    mode_ok = 'error' in ev or level == 'error'
                elif mode == 'runner':
                    mode_ok = 'runner' in ev
                elif mode == 'intake':
                    mode_ok = 'intake' in ev
                elif mode == 'meta':
                    mode_ok = 'meta' in ev
                else:
                    mode_ok = True
            search_text = (search_text or '').strip().lower()
            if not search_text:
                return mode_ok
            parts = []
            for k, v in entry.items():
                parts.append(str(k))
                parts.append(str(v))
            haystack = ' '.join(parts).lower()
            return mode_ok and (search_text in haystack)
        except Exception:
            return True

    def apply_filter() -> None:
        entries = state.get('entries') or []
        mode = filter_var.get()
        search_text = search_var.get()
        filtered = []
        for e in entries:
            if _matches_filter(e, mode, search_text):
                filtered.append(e)
        state['filtered'] = filtered
        listbox.delete(0, 'end')
        if not filtered:
            if entries:
                set_detail_text('Keine Eintraege zur aktuellen Filter-/Sucheinstellung.\n')
            else:
                set_detail_text('Keine Eintraege verfuegbar.\n')
            return
        for idx, entry in enumerate(filtered):
            try:
                label = _summarize_entry(idx, entry)
            except Exception:
                label = str(entry)
            listbox.insert('end', label)
        try:
            first = filtered[0]
            text = _format_entry_json(first)
            set_detail_text(text)
        except Exception:
            pass
        try:
            stats_var.set(_build_stats_text(entries))
        except Exception:
            pass

    def reload_entries() -> None:
        entries, info = _load_learning_journal()
        state['entries'] = entries
        info_var.set(info)
        apply_filter()

    def on_select(event: tk.Event) -> None:
        try:
            sel = listbox.curselection()
            if not sel:
                return
            idx = int(sel[0])
        except Exception:
            return
        entries = state.get('filtered') or []
        if idx < 0 or idx >= len(entries):
            return
        entry = entries[idx]
        try:
            text = _format_entry_json(entry)
        except Exception:
            text = str(entry)
        set_detail_text(text)

    def run_diagnose() -> None:
        try:
            from pathlib import Path as _P
            import subprocess as _sp
            root_dir = _P(__file__).resolve().parent.parent
            cmd_path = root_dir / 'tools' / 'R1802.cmd'
            if not cmd_path.exists():
                info_var.set('Diagnose nicht verfuegbar (R1802.cmd nicht gefunden).')
                _log('R1802.cmd nicht gefunden unter ' + str(cmd_path))
                return
            _sp.Popen(['cmd', '/c', str(cmd_path)], cwd=str(root_dir))
            info_var.set('Diagnose (R1802) gestartet - siehe Konsole/Reports.')
        except Exception as exc:
            info_var.set('Fehler beim Start von R1802: ' + repr(exc))
            _log('run_diagnose: Fehler: ' + repr(exc))

    def on_filter_change(event=None) -> None:
        apply_filter()

    def on_search_change(event=None) -> None:
        apply_filter()

    def reset_filter() -> None:
        filter_var.set('alle')
        search_var.set('')
        apply_filter()

    def show_scans() -> None:
        filter_var.set('alle')
        search_var.set('error_scan')
        apply_filter()


    combo_filter.bind('<<ComboboxSelected>>', on_filter_change)
    entry_search.bind('<KeyRelease>', on_search_change)
    btn_reset.configure(command=reset_filter)
    btn_scans.configure(command=show_scans)
    btn_reload.configure(command=reload_entries)
    btn_diag.configure(command=run_diagnose)
    listbox.bind('<<ListboxSelect>>', on_select)

    reload_entries()
    _log('LearningJournal-Tab (Filter/Suche) gebaut und initial geladen.')

