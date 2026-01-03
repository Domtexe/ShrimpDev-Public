from __future__ import annotations


from __future__ import annotations
import sys
import os
import re
import subprocess
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox


MAX_COPY_BYTES = 10 * 1024 * 1024  # 10 MB safety limit for file copy previews


# --- R2497_HELPERS_START ---
def _r2497_set_clipboard_file_drop_windows(file_paths, hwnd=None):
    """
    Windows Explorer Paste-ready file copy:
    Put paths into clipboard as CF_HDROP + Preferred DropEffect=COPY.

    Returns: (ok: bool, diag: str)
    """
    try:
        import ctypes
        from ctypes import wintypes
        import time
    except Exception as e:
        return False, f"ctypes/time import fail: {e!r}"

    # Use last-error aware DLLs + proper typing to avoid 64-bit handle truncation.
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    user32 = ctypes.WinDLL("user32", use_last_error=True)

    CF_HDROP = 15
    GMEM_MOVEABLE = 0x0002
    CFSTR_PREFERREDDROPEFFECT = "Preferred DropEffect"
    DROPEFFECT_COPY = 1

    class DROPFILES(ctypes.Structure):
        _fields_ = [
            ("pFiles", wintypes.DWORD),
            ("pt_x", wintypes.LONG),
            ("pt_y", wintypes.LONG),
            ("fNC", wintypes.BOOL),
            ("fWide", wintypes.BOOL),
        ]

    # Typing (critical)
    kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
    kernel32.GlobalAlloc.restype = wintypes.HGLOBAL

    kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalLock.restype = wintypes.LPVOID

    kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalUnlock.restype = wintypes.BOOL

    kernel32.GlobalFree.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalFree.restype = wintypes.HGLOBAL

    user32.OpenClipboard.argtypes = [wintypes.HWND]
    user32.OpenClipboard.restype = wintypes.BOOL

    user32.EmptyClipboard.argtypes = []
    user32.EmptyClipboard.restype = wintypes.BOOL

    user32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
    user32.SetClipboardData.restype = wintypes.HANDLE

    user32.CloseClipboard.argtypes = []
    user32.CloseClipboard.restype = wintypes.BOOL

    user32.RegisterClipboardFormatW.argtypes = [wintypes.LPCWSTR]
    user32.RegisterClipboardFormatW.restype = wintypes.UINT

    kernel32.FormatMessageW.argtypes = [
        wintypes.DWORD,
        wintypes.LPCVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPWSTR,
        wintypes.DWORD,
        wintypes.LPVOID,
    ]
    kernel32.FormatMessageW.restype = wintypes.DWORD

    def _fmt_last_error(prefix):
        err = ctypes.get_last_error()
        buf = ctypes.create_unicode_buffer(2048)
        kernel32.FormatMessageW(0x00001000, None, err, 0, buf, len(buf), None)
        msg = buf.value.strip()
        return f"{prefix} | GetLastError={err} | {msg}"

    # Build payload
    flist = "".join([str(p) + "\x00" for p in file_paths]) + "\x00"
    data = flist.encode("utf-16le")

    df = DROPFILES()
    df.pFiles = ctypes.sizeof(DROPFILES)
    df.pt_x = 0
    df.pt_y = 0
    df.fNC = False
    df.fWide = True

    total_size = ctypes.sizeof(DROPFILES) + len(data)
    hglob = kernel32.GlobalAlloc(GMEM_MOVEABLE, total_size)
    if not hglob:
        return False, _fmt_last_error("GlobalAlloc failed")

    ptr = kernel32.GlobalLock(hglob)
    if not ptr:
        kernel32.GlobalFree(hglob)
        return False, _fmt_last_error("GlobalLock failed")

    try:
        ctypes.memmove(ptr, ctypes.addressof(df), ctypes.sizeof(DROPFILES))
        ctypes.memmove(ctypes.c_void_p(ptr + ctypes.sizeof(DROPFILES)), data, len(data))
    finally:
        kernel32.GlobalUnlock(hglob)

    # DropEffect = COPY
    fmt = user32.RegisterClipboardFormatW(CFSTR_PREFERREDDROPEFFECT)
    hfx = kernel32.GlobalAlloc(GMEM_MOVEABLE, 4)
    if not hfx:
        # not fatal; proceed without drop effect
        hfx = None
    else:
        pfx = kernel32.GlobalLock(hfx)
        if not pfx:
            kernel32.GlobalFree(hfx)
            hfx = None
        else:
            try:
                ctypes.memmove(pfx, ctypes.byref(ctypes.c_uint(DROPEFFECT_COPY)), 4)
            finally:
                kernel32.GlobalUnlock(hfx)

    # Open clipboard (retry)
    hwnd_val = wintypes.HWND(hwnd or 0)
    for attempt in range(1, 6):
        if user32.OpenClipboard(hwnd_val):
            break
        time.sleep(0.05 * attempt)
    else:
        kernel32.GlobalFree(hglob)
        if hfx:
            kernel32.GlobalFree(hfx)
        return False, _fmt_last_error("OpenClipboard failed (busy/owner)")

    try:
        user32.EmptyClipboard()

        res = user32.SetClipboardData(CF_HDROP, hglob)
        if not res:
            diag = _fmt_last_error("SetClipboardData(CF_HDROP) failed")
            kernel32.GlobalFree(hglob)
            if hfx:
                kernel32.GlobalFree(hfx)
            return False, diag

        # Ownership transfers to clipboard; do NOT free hglob after success

        # Also provide plaintext paths for apps that paste text (e.g. chat/editor).
        # Explorer will still prefer CF_HDROP for Ctrl+V file copy.
        CF_UNICODETEXT = 13
        try:
            text_payload = "\r\n".join([str(p) for p in file_paths]) + "\r\n"
            text_data = text_payload.encode("utf-16le") + b"\x00\x00"
            htxt = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(text_data))
            if htxt:
                ptxt = kernel32.GlobalLock(htxt)
                if ptxt:
                    try:
                        ctypes.memmove(ptxt, text_data, len(text_data))
                    finally:
                        kernel32.GlobalUnlock(htxt)
                    # transfer ownership to clipboard
                    user32.SetClipboardData(CF_UNICODETEXT, htxt)
                else:
                    kernel32.GlobalFree(htxt)
        except Exception:
            pass
            if hfx and fmt:
                user32.SetClipboardData(fmt, hfx)

        return True, "OK"
    finally:
        user32.CloseClipboard()


def _r2497_copy_file_for_paste(p, hwnd=None):
    """
    Copies a single file path 'p' into clipboard as file copy (Explorer paste).
    """
    try:
        if not p:
            return False, "Kein Pfad."
        ap = os.path.abspath(p)
        if not os.path.isfile(ap):
            return False, f"Keine Datei: {ap}"
        ok, diag = _r2497_set_clipboard_file_drop_windows([ap], hwnd=hwnd)
        if ok:
            return True, "OK"
        return False, diag
        return (ok, "OK" if ok else "Clipboard nicht verfügbar")
    except Exception as e:
        return False, repr(e)


# --- R2497_HELPERS_END ---

try:
    from modules import ui_theme_classic
except Exception:
    ui_theme_classic = None


def _root_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def _safe_open_file(path: str) -> None:
    try:
        if path and os.path.isfile(path):
            os.startfile(path)
    except Exception:
        pass


def _safe_open_folder(path: str) -> None:
    try:
        if not path:
            return
        p = path
        if os.path.isfile(p):
            p = os.path.dirname(p)
        if p and os.path.isdir(p):
            subprocess.Popen(["explorer", p])
    except Exception:
        pass


# --- R2304 INTERNAL VIEWER -----------------------------------------------------------
_R2304_MAX_VIEW_BYTES = 1024 * 1024  # 1 MB
_R2304_TEXT_EXT = {
    ".txt",
    ".md",
    ".py",
    ".json",
    ".log",
    ".ini",
    ".cfg",
    ".yaml",
    ".yml",
    ".csv",
    ".bat",
    ".cmd",
    ".ps1",
}


def _r2304_is_text_file(p: Path) -> bool:
    try:
        return p.suffix.lower() in _R2304_TEXT_EXT
    except Exception:
        return False


def _r2304_open_internal_viewer(app, title: str, path: Path) -> None:
    """Read-only Text-Viewer wie Runner-Popup, für Runner-Produkte."""
    try:
        import tkinter as tk
        from tkinter import messagebox
    except Exception:
        _safe_open_file(str(path))
        return

    try:
        if not path.exists() or not path.is_file():
            return
    except Exception:
        return

    try:
        if path.stat().st_size > _R2304_MAX_VIEW_BYTES:
            # zu groß -> extern
            _safe_open_file(str(path))
            return
    except Exception:
        pass

    # Fenster
    try:
        win = tk.Toplevel(app if app is not None else None)

        # --- R2306 CENTER_OVER_APP -------------------------------------------------
        try:
            # "über Shrimpi" (Hauptfenster) halten
            if app is not None:
                win.transient(app)
            win.lift()
        except Exception:
            pass
        # --- /R2306 CENTER_OVER_APP ------------------------------------------------
        win.title(title)
        win.geometry("980x650")

        # --- R2306 CENTER_OVER_APP (position) --------------------------------------
        try:
            win.update_idletasks()
            # Ziel: über app (Shrimpi) zentrieren, sonst Screen-Mitte
            if app is not None:
                ax = app.winfo_rootx()
                ay = app.winfo_rooty()
                aw = app.winfo_width()
                ah = app.winfo_height()
            else:
                ax = win.winfo_screenwidth() // 2
                ay = win.winfo_screenheight() // 2
                aw = 0
                ah = 0

            ww = win.winfo_width()
            wh = win.winfo_height()

            if app is not None and aw > 0 and ah > 0:
                x = ax + (aw - ww) // 2
                y = ay + (ah - wh) // 2
            else:
                x = (win.winfo_screenwidth() - ww) // 2
                y = (win.winfo_screenheight() - wh) // 2

            # nicht negativ
            x = max(0, x)
            y = max(0, y)
            win.geometry(f"{ww}x{wh}+{x}+{y}")
        except Exception:
            pass
        # --- /R2306 CENTER_OVER_APP (position) -------------------------------------
        win.minsize(720, 420)
    except Exception:
        _safe_open_file(str(path))
        return

    # Top: Info
    top = tk.Frame(win)
    top.pack(side="top", fill="x", padx=8, pady=6)

    lbl = tk.Label(top, text=str(path), anchor="w", justify="left")
    lbl.pack(side="left", fill="x", expand=True)

    # Center: Text + Scroll
    mid = tk.Frame(win)
    mid.pack(side="top", fill="both", expand=True, padx=8, pady=6)

    txt = tk.Text(mid, wrap="none")
    txt.pack(side="left", fill="both", expand=True)

    sb_y = tk.Scrollbar(mid, orient="vertical", command=txt.yview)
    sb_y.pack(side="right", fill="y")
    txt.configure(yscrollcommand=sb_y.set)

    sb_x = tk.Scrollbar(win, orient="horizontal", command=txt.xview)
    sb_x.pack(side="bottom", fill="x")
    txt.configure(xscrollcommand=sb_x.set)

    # Load content (best effort)
    try:
        data = path.read_text(encoding="utf-8", errors="replace")
        txt.insert("1.0", data)
        txt.see("1.0")
    except Exception as e:
        try:
            messagebox.showerror("Öffnen fehlgeschlagen", str(e))
        except Exception:
            pass

    txt.configure(state="disabled")

    # Bottom buttons (zentriert)
    bot = tk.Frame(win)
    bot.pack(side="bottom", fill="x", padx=8, pady=8)

    row = tk.Frame(bot)
    row.pack(side="top", expand=True)

    def _open_external():
        _safe_open_file(str(path))

    def _open_folder():
        _safe_open_folder(str(path))

    def _close():
        try:
            win.destroy()
        except Exception:
            pass

    btn_ext = tk.Button(row, text="Extern öffnen", command=_open_external)
    btn_folder = tk.Button(row, text="Ordner", command=_open_folder)
    btn_close = tk.Button(row, text="Schließen", command=_close)

    btn_ext.pack(side="left", padx=8)
    btn_folder.pack(side="left", padx=8)
    btn_close.pack(side="left", padx=8)


# --- /R2304 INTERNAL VIEWER ----------------------------------------------------------


def _parse_runner_id(name: str) -> str:
    try:
        m = re.search(r"\bR(\d{3,5}[a-zA-Z]?)\b", name)
        return ("R" + m.group(1)) if m else ""
    except Exception:
        return ""


def _format_dt(ts_val: float) -> str:
    try:
        return datetime.fromtimestamp(ts_val).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ""


def _classify_type(root: Path, p: Path) -> str:
    try:
        rel = str(p).replace(str(root), "")
        rel_low = rel.lower()
        if "\\_reports\\" in rel_low or "/_reports/" in rel_low:
            return "Report"
        if "\\_archiv\\" in rel_low or "/_archiv/" in rel_low:
            return "Backup"
        if "\\docs\\" in rel_low or "/docs/" in rel_low:
            return "Doc"
        return "File"
    except Exception:
        return "File"


def _scan_files(root: Path) -> list[dict]:
    items: list[dict] = []
    bases = [root / "_Reports", root / "docs", root / "_Archiv"]
    for b in bases:
        try:
            if not b.exists():
                continue
        except Exception:
            continue
        try:
            for p in b.rglob("*"):
                try:
                    if not p.is_file():
                        continue
                except Exception:
                    continue
                try:
                    st = p.stat()
                    mtime = st.st_mtime
                    size = st.st_size
                except Exception:
                    mtime = 0.0
                    size = 0
                name = p.name
                rid = _parse_runner_id(name)
                typ = _classify_type(root, p)
                items.append(
                    {
                        "name": name,
                        "path": str(p),
                        "type": typ,
                        "runner": rid,
                        "mtime": mtime,
                        "mtime_s": _format_dt(mtime),
                        "size": size,
                    }
                )
        except Exception:
            continue
    try:
        items.sort(key=lambda x: float(x.get("mtime", 0.0) or 0.0), reverse=True)
    except Exception:
        pass
    return items


def build_runner_products_tab(parent: tk.Widget, app) -> None:
    root = _root_dir()
    bg = None
    try:
        bg = ui_theme_classic.BG_MAIN if ui_theme_classic else None
    except Exception:
        bg = None

    container = tk.Frame(parent, bg=bg)
    container.pack(fill="both", expand=True)

    top = tk.Frame(container, bg=bg)
    top.pack(fill="x", padx=8, pady=6)

    tk.Label(top, text="Artefakte (Read-Only)", bg=bg).pack(side="left")

    btn_refresh = tk.Button(top, text="Refresh")
    btn_refresh.pack(side="right")

    mid = tk.Frame(container, bg=bg)
    mid.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    # Left: list, Right: preview
    left = tk.Frame(mid, bg=bg)
    left.pack(side="left", fill="both", expand=True)
    right = tk.Frame(mid, bg=bg)
    right.pack(side="right", fill="both", expand=True)

    # Filters
    f = tk.Frame(left, bg=bg)
    f.pack(fill="x", pady=(0, 6))

    tk.Label(f, text="Runner:", bg=bg).pack(side="left")
    var_runner = tk.StringVar(value="")
    ent_runner = tk.Entry(f, textvariable=var_runner, width=10)
    ent_runner.pack(side="left", padx=(4, 10))

    tk.Label(f, text="Typ:", bg=bg).pack(side="left")
    var_type = tk.StringVar(value="All")
    cmb_type = ttk.Combobox(
        f,
        textvariable=var_type,
        values=["All", "Report", "Doc", "Backup", "File"],
        width=10,
        state="readonly",
    )
    cmb_type.pack(side="left", padx=(4, 10))

    tk.Label(f, text="Suche:", bg=bg).pack(side="left")
    var_q = tk.StringVar(value="")
    ent_q = tk.Entry(f, textvariable=var_q)
    ent_q.pack(side="left", fill="x", expand=True, padx=(4, 0))

    # Tree
    cols = ("mtime", "type", "runner", "name", "size")
    tree = ttk.Treeview(left, columns=cols, show="headings", height=18)
    tree.heading("mtime", text="Zeit")
    tree.heading("type", text="Typ")
    tree.heading("runner", text="Runner")
    tree.heading("name", text="Datei")
    tree.heading("size", text="Bytes")
    tree.column("mtime", width=150, anchor="w")
    tree.column("type", width=70, anchor="w")
    tree.column("runner", width=70, anchor="w")
    tree.column("name", width=360, anchor="w")
    tree.column("size", width=80, anchor="e")
    tree.pack(side="left", fill="both", expand=True)

    sb = ttk.Scrollbar(left, orient="vertical", command=tree.yview)
    sb.pack(side="right", fill="y")
    tree.configure(yscrollcommand=sb.set)

    # Preview
    tk.Label(right, text="Preview", bg=bg).pack(anchor="w")
    txt = tk.Text(right, wrap="word")
    txt.pack(fill="both", expand=True)

    # Actions
    act = tk.Frame(container, bg=bg)
    act.pack(fill="x", padx=8, pady=(0, 8))
    btn_open = tk.Button(act, text="Öffnen")
    btn_open.pack(side="left")
    btn_view = tk.Button(act, text="Intern anzeigen")
    btn_view.pack(side="left", padx=6)
    btn_folder = tk.Button(act, text="Ordner")
    btn_folder.pack(side="left", padx=6)
    btn_copy = tk.Button(act, text="Pfad kopieren")
    btn_copy.pack(side="left")

    state = {"items": [], "id2path": {}}

    def _apply_filters(items: list[dict]) -> list[dict]:
        rid = (var_runner.get() or "").strip()
        typ = (var_type.get() or "All").strip()
        q = (var_q.get() or "").strip().lower()
        out: list[dict] = []
        for it in items:
            try:
                if rid:
                    r0 = (it.get("runner") or "").strip()
                    if r0 != rid:
                        continue
                if typ and typ != "All":
                    if (it.get("type") or "") != typ:
                        continue
                if q:
                    hay = ((it.get("name") or "") + " " + (it.get("path") or "")).lower()
                    if q not in hay:
                        continue
                out.append(it)
            except Exception:
                continue
        return out

    def _fill_tree(items: list[dict]) -> None:
        try:
            for iid in tree.get_children():
                tree.delete(iid)
        except Exception:
            pass
        state["id2path"] = {}
        for it in items:
            try:
                vals = (
                    it.get("mtime_s"),
                    it.get("type"),
                    it.get("runner"),
                    it.get("name"),
                    str(it.get("size")),
                )
                iid = tree.insert("", "end", values=vals)
                state["id2path"][iid] = it.get("path") or ""
            except Exception:
                continue

    def _refresh(*_a):
        items = _scan_files(root)
        state["items"] = items
        filtered = _apply_filters(items)
        _fill_tree(filtered)

    def _selected_path() -> str:
        try:
            sel = tree.selection()
            if not sel:
                return ""
            return state["id2path"].get(sel[0], "")
        except Exception:
            return ""

    def _load_preview(path: str) -> None:
        try:
            txt.configure(state="normal")
        except Exception:
            pass
        try:
            txt.delete("1.0", "end")
        except Exception:
            pass
        if not path:
            return
        try:
            if os.path.getsize(path) > 2 * 1024 * 1024:
                txt.insert("end", "(Datei zu groß für Preview > 2MB)\n" + path)
                return
        except Exception:
            pass
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception as exc:
            content = "Fehler beim Lesen: " + repr(exc)
        try:
            txt.insert("end", content)
        except Exception:
            pass

    def _on_select(_evt=None):
        _load_preview(_selected_path())

    def _on_viewer():
        p = _selected_path()
        if not p:
            return
        try:
            pp = Path(p)
            if _r2304_is_text_file(pp):
                _r2304_open_internal_viewer(app, f"Runner-Produkt: {pp.name}", pp)
            else:
                _safe_open_file(p)
        except Exception:
            _safe_open_file(p)

    def _on_open():
        p = _selected_path()
        if not p:
            return
        try:
            pp = Path(p)
            if _r2304_is_text_file(pp):
                _r2304_open_internal_viewer(app, f"Runner-Produkt: {pp.name}", pp)
            else:
                _safe_open_file(p)
        except Exception:
            _safe_open_file(p)

    def _on_folder():
        _safe_open_folder(_selected_path())

    def _on_copy():
        p = _selected_path()
        if not p:
            return
        try:
            app.clipboard_clear()
            app.clipboard_append(p)
        except Exception:
            try:
                parent.clipboard_clear()
                parent.clipboard_append(p)
            except Exception:
                pass

    btn_refresh.configure(command=_refresh)
    btn_open.configure(command=_on_open)
    try:
        btn_view.configure(command=_on_viewer)
    except Exception:
        pass
    btn_folder.configure(command=_on_folder)
    btn_copy.configure(command=_on_copy)

    try:
        tree.bind("<<TreeviewSelect>>", _on_select)
    except Exception:
        pass

    # --- R2303 TREE UX: Click / Context / Copy --------------------------------------
    _R2303_MAX_COPY_BYTES = 512 * 1024  # 512 KB

    def _on_copy_content():
        p = _selected_path()
        if not p:
            return

        pp = Path(p)
        if not pp.exists():
            return

        # Größencheck
        try:
            if pp.stat().st_size > _R2303_MAX_COPY_BYTES:
                try:
                    from tkinter import messagebox
                    messagebox.showwarning(
                        "Zu groß",
                        f"Datei > {_R2303_MAX_COPY_BYTES // 1024} KB – Inhalt wird nicht kopiert.",
                    )
                except Exception:
                    pass
                return
        except Exception:
            pass

        # Inhalt lesen
        try:
            data = pp.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return

        # Clipboard (App → Fallback Parent)
        try:
            app.clipboard_clear()
            app.clipboard_append(data)
        except Exception:
            try:
                parent.clipboard_clear()
                parent.clipboard_append(data)
            except Exception:
                pass

    def _tree_open_selected(_ev=None):
        _on_open()

    def _tree_copy_path(_ev=None):
        _on_copy()

    def _tree_copy_content(_ev=None):
        _on_copy_content()

    # R2497_ACTION_START
    def _on_copy_file_paste():
        try:
            p2 = _selected_path()
        except Exception:
            p2 = None
        try:
            _hwnd = tree.winfo_id()
        except Exception:
            _hwnd = None
        ok, msg = _r2497_copy_file_for_paste(p2, hwnd=_hwnd)
        try:
            from tkinter import messagebox

            if ok:
                messagebox.showinfo("Datei kopieren", "Datei im Clipboard. (Explorer: Strg+V)")
            else:
                messagebox.showwarning("Datei kopieren", f"Nicht möglich: {msg}")
        except Exception:
            pass

    # R2497_ACTION_END
    # --- R2511_START: Backup restore (SAFE) ----------------------------------------------
    def _is_backup_path(pth: str) -> bool:
        try:
            pnorm = os.path.normpath(pth or "")
            return (os.sep + "_Archiv" + os.sep) in (pnorm + os.sep) and pnorm.lower().endswith(
                ".bak"
            )
        except Exception:
            return False

    def _infer_restore_basename(backup_path: str) -> str:
        """
        Try to map: something.ext.R####_YYYYMMDD_HHMMSS.bak  -> something.ext
        Fallback: strip trailing '.bak'
        """
        bn = os.path.basename(backup_path or "")
        # common pattern: <base>.R1234_<stamp>.bak  (or longer runner id)
        m = re.match(r"^(?P<base>.+?)\.R\d{3,6}_.+?\.bak$", bn, flags=re.IGNORECASE)
        if m:
            return m.group("base")
        if bn.lower().endswith(".bak"):
            return bn[:-4]
        return bn

    def _find_restore_candidates(base_name: str):
        """
        Search project root for exact filename matches outside _Archiv/_Snapshots.
        Returns list of absolute paths.
        """
        hits = []
        try:
            for dirpath, dirnames, filenames in os.walk(_root_dir):
                # prune
                dn = [
                    d for d in dirnames if d not in ("_Archiv", "_Snapshots", ".git", "__pycache__")
                ]
                dirnames[:] = dn
                if base_name in filenames:
                    hits.append(os.path.join(dirpath, base_name))
        except Exception:
            pass
        return hits

    def _on_restore_backup():
        p = _selected_path()
        if not p:
            return
        if not _is_backup_path(p):
            try:
                from tkinter import messagebox

                messagebox.showwarning(
                    "Backup wiederherstellen", "Auswahl ist kein Backup aus _Archiv (*.bak)."
                )
            except Exception:
                pass
            return

        base = _infer_restore_basename(p)
        cands = _find_restore_candidates(base)

        if len(cands) != 1:
            # ambiguous or missing -> do not restore blindly
            msg = f"Restore nicht möglich (Treffer={len(cands)}).\nBackup:\n{p}\n\nZiel-Dateiname:\n{base}\n"
            if cands:
                msg += "\nKandidaten:\n- " + "\n- ".join(cands[:20])
                if len(cands) > 20:
                    msg += f"\n... (+{len(cands) - 20} weitere)"
            try:
                from tkinter import messagebox

                messagebox.showwarning("Backup wiederherstellen", msg)
            except Exception:
                pass
            try:
                app.clipboard_clear()
                app.clipboard_append("\n".join(cands) if cands else base)
            except Exception:
                pass
            return

        target_path = cands[0]

        # Safety: back up current target before overwrite
        try:
            arch = os.path.join(_root_dir, "_Archiv")
            os.makedirs(arch, exist_ok=True)
            stamp2 = datetime.now().strftime("%Y%m%d_%H%M%S")
            safety_bak = os.path.join(
                arch, f"{os.path.basename(target_path)}.RESTORE_BEFORE_{RID}_{stamp2}.bak"
            )
            shutil.copy2(target_path, safety_bak)
        except Exception:
            safety_bak = None

        try:
            shutil.copy2(p, target_path)
            ok = True
        except Exception as e:
            ok = False
            err = str(e)

        try:
            from tkinter import messagebox

            if ok:
                msg = f"OK: Wiederhergestellt.\n\nBackup:\n{p}\n\nZiel:\n{target_path}"
                if safety_bak:
                    msg += f"\n\nSicherungs-Backup vorher:\n{safety_bak}"
                messagebox.showinfo("Backup wiederherstellen", msg)
            else:
                messagebox.showerror(
                    "Backup wiederherstellen",
                    f"FEHLER:\n{err}\n\nBackup:\n{p}\n\nZiel:\n{target_path}",
                )
        except Exception:
            pass

    # --- R2511_END: Backup restore (SAFE) -----------------------------------------------

    def _tree_context_menu(ev):
        try:
            iid = tree.identify_row(ev.y)
            if iid:
                tree.selection_set(iid)
        except Exception:
            pass

        p = _selected_path()
        if not p:
            return

        try:
            m = tk.Menu(tree, tearoff=0)
            m.add_command(label="Intern anzeigen", command=_on_viewer)
            m.add_command(label="Öffnen", command=_on_open)
            m.add_command(label="Ordner öffnen", command=_on_folder)
            # R2515: gated restore only for _Archiv backups
            if _is_backup_path(p):
                m.add_command(label="Backup wiederherstellen", command=_on_restore_backup)
                m.add_separator()
            m.add_command(label="Pfad kopieren", command=_on_copy)

            m.add_command(label="Datei kopieren (Explorer-Paste)", command=_on_copy_file_paste)
            m.add_command(label="Inhalt kopieren (Text)", command=_on_copy_content)
            m.tk_popup(ev.x_root, ev.y_root)
        except Exception:
            pass

    try:
        tree.bind("<Double-Button-1>", _tree_open_selected)
        tree.bind("<Button-3>", _tree_context_menu)

    except Exception:
        pass

    # --- R2508_START: Preview right-click menu ------------------------------------------
    def _preview_copy_selection_or_all():
        # Copy selected text; if none selected, copy all preview text
        try:
            sel = txt.selection_get()
            data = sel if sel else ""
        except Exception:
            data = ""
        if not data:
            try:
                data = txt.get("1.0", "end-1c")
            except Exception:
                data = ""
        try:
            app.clipboard_clear()
            app.clipboard_append(data or "")
        except Exception:
            pass

    def _preview_copy_path():
        p = _selected_path()
        try:
            app.clipboard_clear()
            app.clipboard_append(p or "")
        except Exception:
            pass

    def _preview_copy_file_for_paste():
        p2 = _selected_path()
        if not p2:
            return
        try:
            _hwnd = txt.winfo_id()
        except Exception:
            _hwnd = None
        ok, msg = _r2497_copy_file_for_paste(p2, hwnd=_hwnd)
        try:
            from tkinter import messagebox

            if not ok:
                messagebox.showwarning("Datei kopieren", msg or "Nicht verfügbar.")
        except Exception:
            pass

    def _preview_context_menu(ev):
        # Ensure focus (some apps require focus for selection_get)
        try:
            txt.focus_set()
        except Exception:
            pass
        try:
            m = tk.Menu(txt, tearoff=0)
            m.add_command(label="Inhalt kopieren (Text)", command=_preview_copy_selection_or_all)
            m.add_separator()
            m.add_command(label="Pfad kopieren", command=_preview_copy_path)
            m.add_command(
                label="Datei kopieren (Explorer-Paste)", command=_preview_copy_file_for_paste
            )
            m.tk_popup(ev.x_root, ev.y_root)
        except Exception:
            pass

    try:
        txt.bind("<Button-3>", _preview_context_menu)
    except Exception:
        pass
        # --- R2508_END: Preview right-click menu --------------------------------------------
        tree.bind("<Control-c>", _tree_copy_path)
        tree.bind("<Control-Shift-C>", _tree_copy_content)
    except Exception:
        pass
    # --- /R2303 TREE UX --------------------------------------------------------------

    def _refilter(*_a):
        try:
            filtered = _apply_filters(state.get("items") or [])
            _fill_tree(filtered)
        except Exception:
            pass

    try:
        var_runner.trace_add("write", lambda *_x: _refilter())
        var_type.trace_add("write", lambda *_x: _refilter())
        var_q.trace_add("write", lambda *_x: _refilter())
    except Exception:
        pass

    _refresh()


# --- R2300 UX: Click / Copy / Context -------------------------------------------


def _rp_open(path: Path):
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)  # type: ignore
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except Exception as e:
        messagebox.showerror("Öffnen fehlgeschlagen", str(e))


def _rp_open_folder(path: Path):
    try:
        _rp_open(path.parent)
    except Exception as e:
        messagebox.showerror("Ordner öffnen fehlgeschlagen", str(e))


def _rp_copy_path(root, path: Path):
    root.clipboard_clear()
    root.clipboard_append(str(path))
    root.update_idletasks()


def _rp_copy_content(root, path: Path):
    try:
        if path.stat().st_size > MAX_COPY_BYTES:
            messagebox.showwarning(
                "Zu groß",
                f"Datei ist größer als {MAX_COPY_BYTES // 1024} KB – Kopieren abgebrochen.",
            )
            return
        text = path.read_text(encoding="utf-8", errors="replace")
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update_idletasks()
    except Exception as e:
        messagebox.showerror("Kopieren fehlgeschlagen", str(e))


def _rp_bind_listbox(root, listbox, get_path_callable):
    def on_dbl(_):
        p = get_path_callable()
        if p:
            _rp_open(p)

    def on_menu(ev):
        p = get_path_callable()
        if not p:
            return
        m = tk.Menu(listbox, tearoff=0)
        m.add_command(label="Öffnen", command=lambda: _rp_open(p))
        m.add_command(label="Ordner öffnen", command=lambda: _rp_open_folder(p))
        m.add_separator()
        m.add_command(label="Pfad kopieren", command=lambda: _rp_copy_path(root, p))
        m.add_command(label="Inhalt kopieren", command=lambda: _rp_copy_content(root, p))
        m.tk_popup(ev.x_root, ev.y_root)

    def on_copy(_):
        p = get_path_callable()
        if p:
            _rp_copy_path(root, p)

    def on_copy_content(_):
        p = get_path_callable()
        if p:
            _rp_copy_content(root, p)

    listbox.bind("<Double-Button-1>", on_dbl)
    listbox.bind("<Button-3>", on_menu)
    listbox.bind("<Control-c>", on_copy)
    listbox.bind("<Control-Shift-C>", on_copy_content)


# --- /R2300 UX -------------------------------------------------------------------
