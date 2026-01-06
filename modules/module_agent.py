from __future__ import annotations
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

# R2130: Priorisierung-Helper


# UI_POPUP_CENTER_R2174
def _ui_msg(app, kind, title, text):
    root = getattr(app, "root", None)
    kwargs = {"parent": root} if root is not None else {}
    if kind == "info":
        return _ui_msg(app, "info", title, text, **kwargs)
    if kind == "warn":
        return _ui_msg(app, "warn", title, text, **kwargs)
    if kind == "error":
        return _ui_msg(app, "error", title, text, **kwargs)
    if kind == "ask":
        return _ui_msg(app, "ask", title, text, **kwargs)
    return None


def _agent_build_priority_block(agent_errors_last5, ctx) -> list[str]:
    # Anzeige-only: erzeugt JETZT / DANACH / OPTIONAL
    try:
        ctx = ctx or {}
        last_action = ctx.get("last_action")
        last_runner = ctx.get("last_runner")

        recs = []  # list of tuples (rid, title, why)

        # Fehler-Heuristik (konservativ)
        try:
            errs = int(agent_errors_last5) if agent_errors_last5 is not None else 0
        except Exception:
            errs = 0

        if errs > 0:
            recs.append(
                (
                    "R1802",
                    "Diagnose ausführen",
                    "Agent sieht fehlerhafte Einträge (letzte max. 5 > 0).",
                )
            )

        # Save-Heuristik
        if last_action == "intake_save":
            recs.insert(
                0,
                (
                    "R2086",
                    "Error-Scan ausführen",
                    "Code wurde gerade gespeichert – Status-Scan empfohlen.",
                ),
            )
        elif last_runner:
            recs.append(
                (
                    "R2086",
                    "Error-Scan ausführen",
                    f"Letzter Runner war {last_runner} – kurzer Status-Scan empfohlen.",
                )
            )

        # dedupe, Reihenfolge behalten
        seen = set()
        out = []
        for rid, title, why in recs:
            if rid in seen:
                continue
            seen.add(rid)
            out.append((rid, title, why))

        if not out:
            return []

        block = []
        block.append("")
        block.append("Empfohlene Reihenfolge:")
        for i, (rid, title, why) in enumerate(out, start=1):
            tag = "JETZT" if i == 1 else ("DANACH" if i == 2 else "OPTIONAL")
            block.append(f"{i}) {tag}: {title} ({rid})")
            block.append(f"   Grund: {why}")
        block.append("Hinweis: Empfehlung – keine Automatik, du startest selbst.")
        block.append("")
        return block
    except Exception:
        return []


def _debug_log(msg: str) -> None:
    """Zentraler Debug-Log: schreibt nach debug_output.txt im Projekt-Root."""
    try:
        from pathlib import Path
        import time as _t

        proj = Path(__file__).resolve().parent.parent
        p = proj / "debug_output.txt"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("", encoding="utf-8", errors="ignore") if not p.exists() else None
        with p.open("a", encoding="utf-8", errors="ignore") as f:
            f.write(f"[{_t.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except Exception:
        pass


def _agent_last_error(where: str, exc: Exception) -> None:
    """Schreibt die letzte Exception inkl. Traceback nach _Reports/Agent_LastError.txt."""
    try:
        import traceback
        from pathlib import Path
        import time as _t

        proj = Path(__file__).resolve().parent.parent
        rep = proj / "Reports"
        rep.mkdir(parents=True, exist_ok=True)
        p = rep / "Agent_LastError.txt"
        tb = traceback.format_exc()
        p.write_text(
            f"[{_t.strftime('%Y-%m-%d %H:%M:%S')}] Agent-Fehler in: {where}\n"
            f"Exception: {repr(exc)}\n\n"
            f"Traceback:\n{tb}\n",
            encoding="utf-8",
        )
    except Exception:
        pass


try:
    from modules import context_state
except Exception:
    context_state = None


def _agent_diag_write(where: str, exc: Exception) -> None:
    """Schreibt eine Agent-Diagnose inkl. Traceback nach _Reports."""
    try:
        import traceback
        from pathlib import Path
        import time as _t

        root = Path(__file__).resolve().parent.parent
        rep = root / "Reports"
        rep.mkdir(parents=True, exist_ok=True)
        p = rep / "Agent_LastError.txt"
        tb = traceback.format_exc()

        p.write_text(
            f"[{_t.strftime('%Y-%m-%d %H:%M:%S')}] Agent-Fehler in: {where}\n"
            f"Exception: {repr(exc)}\n\n"
            f"Traceback:\n{tb}\n",
            encoding="utf-8",
        )
    except Exception:
        pass


def _load_journal() -> list[dict[str, Any]]:
    path = Path("learning_journal.json")
    if not path.exists():
        return []
    try:
        txt = path.read_text(encoding="utf-8")
        data = json.loads(txt)
        return data.get("entries", [])
    except Exception:
        return []


def load_agent_data() -> dict[str, Any]:
    entries = _load_journal()
    out: dict[str, Any] = {}
    out["total"] = len(entries)
    # Häufigkeiten
    freq: dict[str, int] = {}
    for e in entries:
        t = e.get("type", "unknown")
        freq[t] = freq.get(t, 0) + 1
    out["freq"] = freq

    # letztes event
    out["last_event"] = entries[-1] if entries else None

    # Fehleranalyse
    errors = []
    for e in entries:
        try:
            ok = _is_errorish(e)
        except Exception:
            ok = False
        if ok:
            errors.append(e)
    out["errors"] = errors[-5:]  # nur letzte 5

    return out

    # R2119: Context aktualisieren (Tab = agent)
    if context_state is not None:
        try:
            context_state.update_context(active_tab="agent")
        except Exception:
            pass


def agent_summary() -> str:
    d = load_agent_data()
    lines = []
    # R2120: Context-Hinweise (read-only)
    if context_state is not None:
        try:
            ctx = context_state.get_context()
            if ctx.get("last_action") == "intake_save":
                lines.append("Hinweis: Code wurde gerade gespeichert – Prüfung empfohlen.")
            if ctx.get("last_runner"):
                lines.append(f"Hinweis: Letzter Runner: {ctx.get('last_runner')}")
            if ctx.get("active_tab") == "intake":
                lines.append("Hinweis: Du befindest dich im Intake-Tab.")
            lines.append("")
        except Exception:
            pass

    lines.append("Systemstatus des Agenten")
    lines.append("Gesamt-Einträge: " + str(d.get("total", 0)))

    freq = d.get("freq", {})
    lines.append("Häufigkeiten:")
    for k, v in freq.items():
        lines.append("  " + k + ": " + str(v))

    le = d.get("last_event")
    if le:
        lines.append("Letztes Event: " + str(le.get("type", "")))

    errs = d.get("errors", [])
    lines.append("Fehler (letzte max. 5): " + str(len(errs)))
    for e in errs:
        lines.append("  ID " + str(e.get("id", "?")) + " – " + e.get("type", ""))

    try:
        warnings = agent_warnings()
    except Exception:
        warnings = []
    lines.append("")

    try:
        recs = agent_recommendations()
    except Exception:
        recs = []
    lines.append("")
    lines.append("Empfohlene Reihenfolge:")
    try:
        chain = agent_action_chain()
    except Exception:
        chain = []
    if chain:
        i = 1
        for r in chain:
            title = str(r.get("title"))
            reason = r.get("reason") or ""
            lines.append(f"  {i}) " + title)
            if reason:
                lines.append("     Grund: " + str(reason))
            i += 1
    else:
        lines.append("  keine")

    lines.append(
        "  Hinweis: Das ist eine Empfehlung – du kannst jeden Schritt auch einzeln starten."
    )
    lines.append("")
    lines.append("Empfehlungen:")
    if recs:
        for r in recs:
            ex = "OK" if r.get("exists") else "FEHLT"
            title = str(r.get("title"))
            lines.append("  " + ex + " | " + title)
            reason = r.get("reason") or ""
            if reason:
                lines.append("      Grund: " + str(reason))
    else:
        lines.append("  keine")
    lines.append("Agent-Warnungen:")
    if warnings:
        for w in warnings:
            lines.append("  " + str(w))
    else:
        lines.append("  keine")

    try:
        la = get_last_agent_action()
    except Exception:
        la = None
    lines.append("")
    lines.append("Letzte Agent-Aktion:")
    if la:
        lines.append("  " + str(la.get("timestamp", "")) + " | " + str(la.get("action", "")))
        if la.get("detail"):
            lines.append("  " + str(la.get("detail")))
    else:
        lines.append("  keine")
    return "\n".join(lines)


def _parse_ts(value: Any) -> Any:
    if not value:
        return None
    s = str(value)
    try:
        return datetime.fromisoformat(s)
    except Exception:
        pass
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    return None


def _load_journal_any() -> list[dict[str, Any]]:
    path = Path("learning_journal.json")
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict) and isinstance(raw.get("entries"), list):
        return raw.get("entries") or []
    return []


def _entry_type(e: dict[str, Any]) -> str:
    t = e.get("type")
    if isinstance(t, str) and t:
        return t
    ev = e.get("event")
    if isinstance(ev, str) and ev:
        return ev
    if isinstance(ev, dict):
        n = ev.get("name") or ev.get("type") or ev.get("category")
        if n:
            return str(n)
    return "unknown"


def _is_errorish(e: dict[str, Any]) -> bool:
    lvl = str(e.get("level") or "").lower()
    if lvl in ("error", "critical", "warn", "warning"):
        return True
    try:
        dump = json.dumps(e, ensure_ascii=False).lower()
        if "traceback" in dump or "exception" in dump:
            return True
        if " error" in dump or "fehler" in dump:
            return True
    except Exception:
        pass
    return False


def agent_warnings(now: Any = None) -> list[str]:
    if now is None:
        now = datetime.now()
    try:
        entries = _load_journal_any()
    except Exception:
        entries = []

    warnings: list[str] = []

    # Zeitfenster
    win_5m = now.timestamp() - 5 * 60
    win_15m = now.timestamp() - 15 * 60
    win_60m = now.timestamp() - 60 * 60

    def in_win(e: dict[str, Any], cutoff: float) -> bool:
        ts = _parse_ts(e.get("timestamp"))
        if ts is None:
            return False
        try:
            return ts.timestamp() >= cutoff
        except Exception:
            return False

    # Restart-Loop Verdacht
    app_starts_5m = 0
    for e in entries:
        if _entry_type(e) == "app_start" and in_win(e, win_5m):
            app_starts_5m += 1
    if app_starts_5m >= 5:
        warnings.append(
            f"WARN: Viele app_start in 5 Min ({app_starts_5m}). Verdacht: Restart-Loop."
        )

    # Fehlertrend
    err_15m = 0
    err_60m = 0
    for e in entries:
        if _is_errorish(e):
            if in_win(e, win_15m):
                err_15m += 1
            if in_win(e, win_60m):
                err_60m += 1
    if err_15m >= 1:
        warnings.append(f"WARN: Fehlerereignisse in 15 Min: {err_15m} (letzte Stunde: {err_60m}).")

    # Error-Scan Ergebnisse (falls R2086 data/error_lines liefert)
    scan_bad_60m = 0
    for e in entries:
        if _entry_type(e) == "error_scan" and in_win(e, win_60m):
            data = e.get("data") if isinstance(e.get("data"), dict) else {}
            try:
                el = int(data.get("error_lines") or 0)
            except Exception:
                el = 0
            if el > 0:
                scan_bad_60m += 1
    if scan_bad_60m >= 1:
        warnings.append(f"WARN: Error-Scans mit Fehlern in 60 Min: {scan_bad_60m}.")

    # Ungewöhnliche Häufigkeiten (sehr simple Heuristik)
    saves_15m = 0
    for e in entries:
        if _entry_type(e) == "intake_save" and in_win(e, win_15m):
            saves_15m += 1
    if saves_15m >= 20:
        warnings.append(f"HINWEIS: Sehr viele intake_save in 15 Min ({saves_15m}).")

    return warnings


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _tool_cmd(runner_id: str) -> Path:
    rid = str(runner_id)
    if not rid.lower().endswith(".cmd"):
        rid = rid + ".cmd"
    return _project_root() / "tools" / rid


def agent_action_chain() -> list[dict]:
    """Leitet aus Empfehlungen eine sinnvolle Reihenfolge ab (read-only)."""
    recs = agent_recommendations()
    chain = []

    # Priorität: Error-Scan zuerst, dann Diagnose
    scan = [r for r in recs if "R2086" in str(r.get("title"))]
    diag = [r for r in recs if "R1802" in str(r.get("title"))]

    if scan:
        chain.extend(scan)
    if diag:
        chain.extend(diag)

    # Rest (falls später erweitert)
    for r in recs:
        if r not in chain:
            chain.append(r)

    return chain


def agent_recommendations() -> list[dict[str, Any]]:
    d = load_agent_data()
    recs: list[dict[str, Any]] = []

    # Heuristik 1: Wenn errors (letzte 5) vorhanden -> Diagnose empfehlen
    errs = d.get("errors") or []
    if isinstance(errs, list) and len(errs) > 0:
        p = _tool_cmd("R1802")
        recs.append(
            {
                "id": "diag",
                "title": "Diagnose ausfuehren (R1802)",
                "reason": "Agent sieht errorish Eintraege (letzte max. 5 > 0).",
                "path": str(p),
                "exists": p.exists(),
            }
        )

    # Heuristik 2: Error-Scan empfehlen, wenn debug_output.txt existiert
    # (nutzt R2086, falls vorhanden)
    pscan = _tool_cmd("R2086")
    if pscan.exists():
        recs.append(
            {
                "id": "scan",
                "title": "Error-Scan ausfuehren (R2086)",
                "reason": "Aktuellen Status aus debug_output.txt ins LearningJournal schreiben.",
                "path": str(pscan),
                "exists": True,
            }
        )

    return recs


def run_first_recommendation() -> dict[str, Any]:
    recs = agent_recommendations()
    if not recs:
        return {"ok": False, "msg": "Keine Empfehlungen vorhanden."}
    # erste existierende Empfehlung nehmen
    for r in recs:
        try:
            if r.get("exists") and r.get("path"):
                os.startfile(str(r.get("path")))
                return {"ok": True, "msg": "Gestartet: " + str(r.get("title"))}
        except Exception as exc:
            return {"ok": False, "msg": "Start fehlgeschlagen: " + repr(exc)}
    return {"ok": False, "msg": "Empfehlungen vorhanden, aber keine .cmd gefunden."}


def _agent_last_action_path() -> Path:
    p = _project_root() / "Reports"
    try:
        p.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return p / "Agent_LastAction.json"


def set_last_agent_action(action: str, detail: str = "") -> None:
    try:
        payload = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "action": str(action),
            "detail": str(detail),
        }
        _agent_last_action_path().write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception:
        pass


def get_last_agent_action() -> dict[str, Any] | None:
    try:
        p = _agent_last_action_path()
        if not p.exists():
            return None
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def build_agent_tab(parent, app):
    # AGENT_UI_CLICKABLE_R2173
    import tkinter as tk
    import tkinter.ttk as ttk

    header = ttk.Label(parent, text="Agent", anchor="w")
    header.pack(fill="x", padx=10, pady=(10, 6))

    outer = ttk.Frame(parent)
    outer.pack(fill="both", expand=True, padx=10, pady=(0, 8))

    left = ttk.Frame(outer)
    left.pack(side="left", fill="y")

    right = ttk.Frame(outer)
    right.pack(side="left", fill="both", expand=True, padx=(10, 0))

    cols = ("exists", "title")
    tree = ttk.Treeview(left, columns=cols, show="headings", height=14, selectmode="browse")
    tree.heading("exists", text="OK")
    tree.heading("title", text="Empfehlung")
    tree.column("exists", width=45, stretch=False, anchor="center")
    tree.column("title", width=360, stretch=True, anchor="w")
    vs = ttk.Scrollbar(left, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vs.set)
    tree.pack(side="left", fill="y")
    vs.pack(side="left", fill="y")

    scr = ttk.Scrollbar(right, orient="vertical")
    scr.pack(side="right", fill="y")
    txtw = tk.Text(right, wrap="word", yscrollcommand=scr.set)
    txtw.pack(side="left", fill="both", expand=True)
    scr.config(command=txtw.yview)
    try:
        txtw.config(state="disabled")
    except Exception:
        pass

    recs = []

    def _set_text(value: str) -> None:
        try:
            txtw.config(state="normal")
            txtw.delete("1.0", "end")
            txtw.insert("end", value or "")
            txtw.config(state="disabled")
        except Exception:
            pass

    def _pipeline_path() -> Path:
        return _project_root() / "docs" / "PIPELINE.md"

    def _insert_pipeline_item(line: str) -> bool:
        p = _pipeline_path()
        if not p.exists():
            return False
        try:
            content = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return False
        if line.strip() in content:
            return True
        lines = content.splitlines(True)
        insert_at = None
        for i, ln in enumerate(lines):
            s = ln.strip().lower()
            if s.startswith("## ") and "agent" in s:
                insert_at = i + 1
                while insert_at < len(lines) and lines[insert_at].strip() == "":
                    insert_at += 1
                break
        if insert_at is None:
            insert_at = 0
            for i, ln in enumerate(lines):
                if ln.strip().startswith("# "):
                    insert_at = i + 1
                    while insert_at < len(lines) and lines[insert_at].strip() == "":
                        insert_at += 1
                    break
            lines.insert(insert_at, "\n## Agent\n\n")
            insert_at += 2
        lines.insert(insert_at, line.rstrip() + "\n")
        try:
            p.write_text("".join(lines), encoding="utf-8")
            return True
        except Exception:
            return False

    def _selected():
        sel = tree.selection()
        if not sel:
            return None
        iid = sel[0]
        try:
            idx = int(tree.set(iid, "_idx"))
        except Exception:
            return None
        if 0 <= idx < len(recs):
            return recs[idx]
        return None

    if "_idx" not in tree["columns"]:
        tree["columns"] = ("_idx",) + tree["columns"]
        tree.column("_idx", width=0, stretch=False)
        tree.heading("_idx", text="")
        tree["displaycolumns"] = cols

    def _render() -> None:
        tree.delete(*tree.get_children())
        for i, r in enumerate(recs):
            ex = "OK" if r.get("exists") else "FEHLT"
            title = str(r.get("title") or "")
            iid = tree.insert("", "end", values=(ex, title))
            tree.set(iid, "_idx", str(i))

    def _show_selected(_evt=None) -> None:
        r = _selected()
        if not r:
            _set_text(agent_summary())
            return
        parts = []
        parts.append("Empfehlung:")
        parts.append("  " + str(r.get("title") or ""))
        parts.append("  OK: " + ("ja" if r.get("exists") else "nein"))
        if r.get("path"):
            parts.append("  Pfad: " + str(r.get("path")))
        if r.get("reason"):
            parts.append("")
            parts.append("Grund:")
            parts.append("  " + str(r.get("reason")))
        parts.append("")
        parts.append("-----")
        parts.append("")
        parts.append(agent_summary())
        _set_text("\n".join(parts))

    def _refresh() -> None:
        nonlocal recs
        try:
            recs = agent_recommendations() or []
        except Exception as e:
            _debug_log("Agent-Update Exception: " + repr(e))
            _agent_last_error("agent_update", e)
            recs = []
        _render()
        _show_selected()

    def _run_selected() -> None:
        r = _selected()
        if not r:
            _ui_msg(app, "info", "Agent", "Keine Empfehlung ausgewählt.")
            return
        if not r.get("exists") or not r.get("path"):
            _ui_msg(app, "info", "Agent", "Diese Empfehlung ist nicht startbar (FEHLT).")
            return
        try:
            os.startfile(str(r.get("path")))
            _ui_msg(app, "info", "Agent", "Gestartet: " + str(r.get("title") or ""))
        except Exception as exc:
            _debug_log("Agent run_selected failed: " + repr(exc))
            _agent_last_error("agent_run_selected", exc)
            _ui_msg(app, "info", "Agent", "Start fehlgeschlagen: " + repr(exc))
        _refresh()

    def _copy_selected_path() -> None:
        r = _selected()
        if not r:
            _ui_msg(app, "info", "Agent", "Keine Empfehlung ausgewählt.")
            return
        s = str(r.get("path") or "")
        if not s:
            _ui_msg(app, "info", "Agent", "Keine Pfad-Info vorhanden.")
            return
        try:
            parent.clipboard_clear()
            parent.clipboard_append(s)
            _ui_msg(app, "info", "Agent", "Pfad kopiert.")
        except Exception:
            _ui_msg(app, "info", "Agent", "Kopieren nicht möglich.")

    def _add_to_pipeline() -> None:
        r = _selected()
        if not r:
            _ui_msg(app, "info", "Agent", "Keine Empfehlung ausgewählt.")
            return
        title = str(r.get("title") or "").strip()
        reason = str(r.get("reason") or "").strip()
        line = "- [ ] (MEDIUM) Agent: " + title
        if reason:
            line += " — " + reason
        try:
            ok = _ui_msg(app, "ask", "Pipeline", "In docs/PIPELINE.md eintragen?\n\n" + line)
        except Exception:
            ok = False
        if not ok:
            return
        if _insert_pipeline_item(line):
            _ui_msg(app, "info", "Pipeline", "Eingetragen.")
        else:
            _ui_msg(app, "info", "Pipeline", "Konnte nicht eintragen (PIPELINE.md fehlt/gesperrt).")

    btnrow = ttk.Frame(parent)
    btnrow.pack(fill="x", padx=10, pady=(0, 10))
    ttk.Button(btnrow, text="Aktualisieren", command=_refresh).pack(side="left")
    ttk.Button(btnrow, text="Ausfuehren", command=_run_selected).pack(side="left", padx=(8, 0))
    ttk.Button(btnrow, text="Pfad kopieren", command=_copy_selected_path).pack(
        side="left", padx=(8, 0)
    )
    ttk.Button(btnrow, text="In Pipeline", command=_add_to_pipeline).pack(side="left", padx=(8, 0))

    tree.bind("<<TreeviewSelect>>", _show_selected)
    _refresh()
