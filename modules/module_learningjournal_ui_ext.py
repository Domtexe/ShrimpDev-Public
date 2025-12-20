
"""
LearningJournal UI Modul - korrigierte Version (R1670b)
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import tkinter as tk
from tkinter import ttk, messagebox

PROJECT_NAME = "ShrimpDev"
LEARNING_JOURNAL_FILENAME = "learning_journal.json"


def get_project_root_from_any(path: Optional[Path] = None) -> Path:
    if path is None:
        path = Path(__file__).resolve()
    cur = path
    for _ in range(5):
        if (cur / "tools").is_dir() and (cur / "modules").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return Path(__file__).resolve().parent.parent


def get_learning_journal_path(root: Optional[Path] = None) -> Path:
    if root is None:
        root = get_project_root_from_any()
    return root / LEARNING_JOURNAL_FILENAME


def load_learning_journal(root: Optional[Path] = None) -> Dict[str, Any]:
    path = get_learning_journal_path(root)
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except:
        return {}


def extract_phase_b_entries(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    lst = data.get("phaseB_analysis")
    if isinstance(lst, list):
        return [x for x in lst if isinstance(x, dict)]
    return []


def summarize_phase_b(entries: List[Dict[str, Any]]) -> Tuple[int, float]:
    if not entries:
        return 0, 0.0
    scores = []
    for e in entries:
        try:
            if "score" in e:
                scores.append(float(e["score"]))
        except:
            pass
    avg = sum(scores) / len(scores) if scores else 0.0
    return len(entries), avg


def build_learningjournal_panel(parent: tk.Widget, root_dir: Optional[Path] = None) -> tk.Frame:
    if root_dir is None:
        root_dir = get_project_root_from_any()

    frame = ttk.Frame(parent)

    # Header
    header = ttk.Frame(frame)
    header.pack(side="top", fill="x", padx=8, pady=6)

    ttk.Label(header, text="LearningJournal - Phase B Analyse", font=("", 11, "bold")).pack(side="left")

    btn_reload = ttk.Button(header, text="Neu laden")
    btn_reload.pack(side="right", padx=4)

    btn_open = ttk.Button(header, text="JSON öffnen")
    btn_open.pack(side="right", padx=4)

    lbl_path = ttk.Label(frame, text="Datei: {}".format(get_learning_journal_path(root_dir)))
    lbl_path.pack(side="top", anchor="w", padx=8)

    # Tree
    columns = ("id", "timestamp", "category", "score", "summary")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
    tree.pack(side="top", fill="both", expand=True, padx=8, pady=4)

    headers = {
        "id": "ID",
        "timestamp": "Zeitstempel",
        "category": "Kategorie",
        "score": "Score",
        "summary": "Zusammenfassung"
    }

    widths = {
        "id": 80,
        "timestamp": 150,
        "category": 120,
        "score": 80,
        "summary": 400
    }

    for col in columns:
        tree.heading(col, text=headers[col])
        tree.column(col, width=widths[col], anchor="w")

    footer = ttk.Frame(frame)
    footer.pack(side="bottom", fill="x", padx=8, pady=6)

    lbl_summary = ttk.Label(footer, text="Keine Phase-B-Daten geladen.")
    lbl_summary.pack(side="left")

    def refresh():
        data = load_learning_journal(root_dir)
        entries = extract_phase_b_entries(data)
        count, avg = summarize_phase_b(entries)

        for i in tree.get_children():
            tree.delete(i)

        for e in entries:
            tree.insert("", "end", values=(
                e.get("id", ""),
                e.get("timestamp", ""),
                e.get("category", ""),
                e.get("score", ""),
                e.get("summary", "")
            ))

        if entries:
            lbl_summary.config(text="Phase-B-Einträge: {} | Ø Score: {:.3f}".format(count, avg))
        else:
            lbl_summary.config(text="Keine Phase-B-Einträge gefunden.")

    def open_json():
        path = get_learning_journal_path(root_dir)
        if path.exists():
            try:
                import os
                os.startfile(str(path))
            except:
                pass

    btn_reload.configure(command=refresh)
    btn_open.configure(command=open_json)

    refresh()
    return frame
