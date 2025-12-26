from __future__ import annotations
import re

from pathlib import Path
import tkinter as tk
import tkinter.ttk as ttk


def _project_root() -> Path:
    # modules/ui_pipeline_tab.py -> project root
    return Path(__file__).resolve().parent.parent


def _pipeline_path() -> Path:
    return _project_root() / "docs" / "PIPELINE.md"


def build_pipeline_tab(parent, app) -> None:
    # PIPELINE_TREEVIEW_R2156
    # UX+Debug: Task-Liste (Treeview) + Toggle + Filter + Summary + Auto-Reload + Diagnose

    header = ttk.Label(parent, text="Pipeline", anchor="w")
    # PIPELINE_UX_R2166

    header.pack(fill="x", padx=10, pady=(10, 4))

    diag = ttk.Label(parent, text="", anchor="w")
    diag.pack(fill="x", padx=10, pady=(0, 4))

    summary = ttk.Label(parent, text="", anchor="w")
    summary.pack(fill="x", padx=10, pady=(0, 6))

    bar = ttk.Frame(parent)
    bar.pack(fill="x", padx=10, pady=(0, 8))

    var_show_open = tk.BooleanVar(value=True)
    var_show_done = tk.BooleanVar(value=True)

    ttk.Checkbutton(bar, text="Offen", variable=var_show_open).pack(side="left")
    ttk.Checkbutton(bar, text="Erledigt", variable=var_show_done).pack(side="left", padx=(8, 0))

    ttk.Label(bar, text="|").pack(side="left", padx=8)

    var_query = tk.StringVar(value="")
    ttk.Label(bar, text="Suche:").pack(side="left", padx=(0, 6))
    ent_query = ttk.Entry(bar, textvariable=var_query, width=26)
    ent_query.pack(side="left")
    btn_clear = ttk.Button(bar, text="X", width=3, command=lambda: var_query.set(""))
    btn_clear.pack(side="left", padx=(6, 0))

    btn_reload = ttk.Button(bar, text="Neu laden")
    btn_reload.pack(side="left")

    btn_open = ttk.Button(bar, text="Im Explorer")
    btn_open.pack(side="left", padx=(8, 0))

    hint = ttk.Label(bar, text="Tipp: Doppelklick oder SPACE toggelt ☐/☑", anchor="w")
    hint.pack(side="right")

    content = ttk.Frame(parent)
    content.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    cols = ("status", "prio", "task", "section")

    style = ttk.Style()
    try:
        style.configure("Pipeline.Treeview", rowheight=22)
    except Exception:
        pass

    tree = ttk.Treeview(
        content, columns=cols, show="headings", selectmode="browse", style="Pipeline.Treeview"
    )
    tree.heading("status", text="Status")
    tree.heading("prio", text="Prio")
    tree.heading("task", text="Task")
    tree.heading("section", text="Section")
    tree.column("status", width=70, stretch=False, anchor="w")
    tree.column("prio", width=80, stretch=False, anchor="w")
    tree.column("task", width=700, stretch=True, anchor="w")
    tree.column("section", width=220, stretch=False, anchor="w")

    # UX tags (zebra + emphasis)
    try:
        tree.tag_configure("odd", background="#f7f7f7")
        tree.tag_configure("even", background="#ffffff")
        tree.tag_configure("done", foreground="#888888")
        tree.tag_configure("high", foreground="#b00020")
    except Exception:
        pass

    sort_state = {"col": "", "desc": False}

    def _set_sort(col: str) -> None:
        try:
            if sort_state.get("col") == col:
                sort_state["desc"] = not bool(sort_state.get("desc"))
            else:
                sort_state["col"] = col
                sort_state["desc"] = False
        except Exception:
            sort_state["col"] = col
            sort_state["desc"] = False
        _render()

    # headings clickable (sort)
    try:
        tree.heading("status", command=lambda: _set_sort("status"))
        tree.heading("prio", command=lambda: _set_sort("prio"))
        tree.heading("task", command=lambda: _set_sort("task"))
        tree.heading("section", command=lambda: _set_sort("section"))
    except Exception:
        pass

    scr = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scr.set)
    tree.pack(side="left", fill="both", expand=True)
    scr.pack(side="right", fill="y")

    empty = ttk.Label(parent, text="", anchor="w")
    empty.pack(fill="x", padx=10, pady=(0, 10))

    state = {
        "last_mtime": None,
        "items": [],
        "raw_lines": [],
        "visible": [],
        "path": None,
    }

    def _is_visible() -> bool:
        try:
            nb = getattr(app, "nb", None)
            if nb is None:
                return True
            return nb.select() == str(parent)
        except Exception:
            return True

    def _set_diag(p) -> None:
        try:
            exists = bool(p and p.exists())
            diag.config(text=f"Datei: {p}   |   exists={exists}")
        except Exception:
            pass

    def _parse_pipeline(raw: str) -> tuple[list[dict], list[str]]:
        # R2158: robust task parsing for PIPELINE.md
        # supports:
        #  - Markdown: - [ ] / - [x] (also * bullets)
        #  - Unicode:  ⬜ / ✔ (also * bullets)
        lines = raw.splitlines(True)
        items = []
        section = ""
        task_md = re.compile(r"^\s*[-*]\s*\[([ xX])\]\s+(.*)$")
        task_uni = re.compile(r"^\s*[-*]\s*([⬜✔])\s+(.*)$")
        for i, ln in enumerate(lines):
            s = ln.strip()
            if s.startswith("## "):
                section = s[3:].strip()
                continue
            done = None
            rest = None
            m1 = task_md.match(ln)
            if m1:
                done = m1.group(1).lower() == "x"
                rest = m1.group(2).strip()
            else:
                m2 = task_uni.match(ln)
                if m2:
                    done = m2.group(1) == "✔"
                    rest = m2.group(2).strip()
            if done is None:
                continue
            prio = ""
            mprio = re.search(r"\((HIGH|MEDIUM|LOW)\)", rest)
            if mprio:
                prio = mprio.group(1)
            items.append(
                {
                    "line_index": i,
                    "done": bool(done),
                    "prio": prio,
                    "task": rest,
                    "section": section,
                }
            )
        return items, lines

    def _rebuild_visible() -> None:
        show_open = bool(var_show_open.get())
        show_done = bool(var_show_done.get())
        q = ""
        try:
            q = (var_query.get() or "").strip().lower()
        except Exception:
            q = ""

        def _match(it: dict) -> bool:
            if not q:
                return True
            try:
                hay = (
                    str(it.get("task", ""))
                    + " "
                    + str(it.get("section", ""))
                    + " "
                    + str(it.get("prio", ""))
                ).lower()
                return q in hay
            except Exception:
                return True

        vis = []
        for it in state["items"]:
            if it.get("done") and not show_done:
                continue
            if (not it.get("done")) and not show_open:
                continue
            if not _match(it):
                continue
            vis.append(it)
        state["visible"] = vis

    def _render() -> None:
        for iid in tree.get_children(""):
            tree.delete(iid)

        done_n = sum(1 for it in state["items"] if it["done"])
        open_n = sum(1 for it in state["items"] if not it["done"])
        try:
            summary.config(text=f"Erledigt: {done_n}   Offen: {open_n}")
        except Exception:
            pass

        _rebuild_visible()

        # sort visible (if any)
        def _prio_rank(p: str) -> int:
            if p == "HIGH":
                return 0
            if p == "MEDIUM":
                return 1
            if p == "LOW":
                return 2
            return 9

        try:
            col = str(sort_state.get("col") or "").strip()
            desc = bool(sort_state.get("desc"))
        except Exception:
            col = ""
            desc = False

        items = list(state.get("visible") or [])
        if col == "status":
            items.sort(
                key=lambda it: (0 if it.get("done") else 1, str(it.get("task", ""))), reverse=desc
            )
        elif col == "prio":
            items.sort(
                key=lambda it: (_prio_rank(str(it.get("prio", ""))), str(it.get("task", ""))),
                reverse=desc,
            )
        elif col == "task":
            items.sort(key=lambda it: str(it.get("task", "")).lower(), reverse=desc)
        elif col == "section":
            items.sort(key=lambda it: str(it.get("section", "")).lower(), reverse=desc)

        for idx, it in enumerate(items):
            status_txt = "☑" if it.get("done") else "☐"
            tags = []
            tags.append("odd" if (idx % 2 == 1) else "even")
            if it.get("done"):
                tags.append("done")
            if str(it.get("prio", "")) == "HIGH":
                tags.append("high")
            tree.insert(
                "",
                "end",
                values=(status_txt, it.get("prio", ""), it.get("task", ""), it.get("section", "")),
                tags=tuple(tags),
            )

        if len(state["items"]) == 0:
            empty.config(
                text="Keine Tasks erkannt. Prüfe Checkbox-Format oder Datei-Pfad (siehe oben)."
            )
        else:
            empty.config(text="")

    def _load(force: bool = False) -> None:
        p = _pipeline_path()
        state["path"] = p
        _set_diag(p)
        if not p.exists():
            state["items"] = []
            state["raw_lines"] = []
            state["last_mtime"] = None
            _render()
            return
        try:
            mtime = p.stat().st_mtime
        except Exception:
            mtime = None
        if (not force) and (mtime is not None) and (state.get("last_mtime") == mtime):
            return
        try:
            raw = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return
        state["items"], state["raw_lines"] = _parse_pipeline(raw)
        if mtime is not None:
            state["last_mtime"] = mtime
        _render()

    def _toggle_line(line_index: int) -> None:
        p = state.get("path") or _pipeline_path()
        if not p.exists():
            return
        lines = list(state.get("raw_lines") or [])
        if not lines:
            try:
                lines = p.read_text(encoding="utf-8", errors="replace").splitlines(True)
            except Exception:
                return
        if line_index < 0 or line_index >= len(lines):
            return
        ln = lines[line_index]
        m = re.match(r"^(\s*[-*]\s*)\[([ xX])\](\s+.*)$", ln)
        if not m:
            return
        pre, mark, tail = m.group(1), m.group(2), m.group(3)
        new_mark = "x" if mark.strip() == "" else " "
        lines[line_index] = f"{pre}[{new_mark}]{tail}"
        try:
            p.write_text("".join(lines), encoding="utf-8")
        except Exception:
            return
        _load(force=True)

    def _selected_visible_index() -> int | None:
        sel = tree.selection()
        if not sel:
            return None
        iid = sel[0]
        vals = tree.item(iid, "values")
        if not vals or len(vals) < 3:
            return None
        status_txt, prio, task = vals[0], vals[1], vals[2]
        for it in state.get("visible") or []:
            if (
                ("☑" if it["done"] else "☐") == status_txt
                and it["prio"] == prio
                and it["task"] == task
            ):
                return it["line_index"]
        return None

    def _toggle_selected(_e=None) -> None:
        li = _selected_visible_index()
        if li is None:
            return
        _toggle_line(li)

    def _on_double_click(_e=None) -> None:
        _toggle_selected()

    def _open_in_explorer() -> None:
        p = state.get("path") or _pipeline_path()
        try:
            import os

            if p.exists():
                os.startfile(str(p))
            else:
                os.startfile(str(p.parent))
        except Exception:
            pass

    try:
        btn_reload.config(command=lambda: _load(force=True))
        btn_open.config(command=_open_in_explorer)
    except Exception:
        pass

    def _refilter(*_a) -> None:
        _render()

    try:
        var_show_open.trace_add("write", _refilter)
        var_show_done.trace_add("write", _refilter)
        var_query.trace_add("write", _refilter)
    except Exception:
        pass

    try:
        tree.bind("<Double-1>", _on_double_click, add=True)
        tree.bind("<space>", _toggle_selected, add=True)
    except Exception:
        pass

    def _tick() -> None:
        try:
            if _is_visible():
                _load(force=False)
        except Exception:
            pass
        try:
            parent.after(2000, _tick)
        except Exception:
            pass

    def _on_tab_changed(_e=None) -> None:
        try:
            if _is_visible():
                _load(force=True)
        except Exception:
            pass

    try:
        nb = getattr(app, "nb", None)
        if nb is not None:
            nb.bind("<<NotebookTabChanged>>", _on_tab_changed, add=True)
    except Exception:
        pass

    _load(force=True)
    _tick()
