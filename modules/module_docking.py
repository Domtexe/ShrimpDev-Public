# module_docking.py
# Dock/Undock Manager (Phase-1): Read-Only Tabs als Extra-Viewer
# Wichtig: Kein Reparenting von Widgets. Extra-Fenster wird neu aufgebaut.

import tkinter as tk
import os
import configparser


def _center_window(win, width, height, parent=None):
    try:
        win.update_idletasks()
    except Exception:
        pass

    x = 100
    y = 100
    try:
        if parent is not None:
            parent.update_idletasks()
            px = int(parent.winfo_rootx())
            py = int(parent.winfo_rooty())
            pw = int(parent.winfo_width())
            ph = int(parent.winfo_height())
            if pw > 50 and ph > 50:
                x = px + int((pw - width) / 2)
                y = py + int((ph - height) / 2)
            else:
                sw = int(win.winfo_screenwidth())
                sh = int(win.winfo_screenheight())
                x = int((sw - width) / 2)
                y = int((sh - height) / 2)
        else:
            sw = int(win.winfo_screenwidth())
            sh = int(win.winfo_screenheight())
            x = int((sw - width) / 2)
            y = int((sh - height) / 2)
    except Exception:
        pass

    if x < 0:
        x = 0
    if y < 0:
        y = 0
    try:
        w.geometry(str(width) + "x" + str(height) + "+" + str(x) + "+" + str(y))
    except Exception:
        pass


# R2339_DOCKING_PERSIST_V1
# Persist/Restore undocked windows in INI (w/h/x/y). Center only on first open.


def _r2339_safe_int(v, default=0):
    try:
        return int(v)
    except Exception:
        return int(default)


def _r2339_ini_path(app=None):
    # R2343_HARD_INI_GEOMETRY: always write to project-root ShrimpDev.ini
    pr = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    return os.path.join(pr, "ShrimpDev.ini")


def _r2339_cfg_read(path):
    cfg = configparser.ConfigParser()
    try:
        if os.path.isfile(path):
            cfg.read(path, encoding="utf-8")
    except Exception:
        try:
            cfg.read(path)
        except Exception:
            pass
    return cfg


def _r2339_cfg_write(cfg, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            cfg.write(f)
        return True
    except Exception:
        try:
            with open(path, "w") as f:
                cfg.write(f)
            return True
        except Exception:
            return False


def _r2339_cfg_set(cfg, sec, key, val):
    try:
        if not cfg.has_section(sec):
            cfg.add_section(sec)
        cfg.set(sec, key, str(val))
    except Exception:
        pass


def _r2339_cfg_get(cfg, sec, key, default=""):
    try:
        return cfg.get(sec, key, fallback=default)
    except Exception:
        try:
            return cfg.get(sec, key)
        except Exception:
            return default


def _r2340_is_offscreen(x, y, w, h, sw, sh, margin=20):
    try:
        if w <= 0 or h <= 0 or sw <= 0 or sh <= 0:
            return True
        if (x + w) < margin or (y + h) < margin:
            return True
        if x > (sw - margin) or y > (sh - margin):
            return True
        if x < -margin or y < -margin:
            return True
        if (x + w) > (sw + margin) or (y + h) > (sh + margin):
            return True
        return False
    except Exception:
        return True


# R2340_WM_GEOMETRY_FIX
def _r2340_parse_geo(geo_str):
    # returns (w,h,x,y) from 'WxH+X+Y' ; supports negative X/Y
    try:
        s = str(geo_str).strip()
        if "x" not in s:
            return (0, 0, 0, 0)
        wh, rest = s.split("+", 1) if "+" in s else (s, "")
        w_s, h_s = wh.split("x", 1)
        w = _r2339_safe_int(w_s, 0)
        # rest may contain +X+Y or -X+Y etc; easiest: find last '+' or '-' for Y
        if "+" in s[s.find("x") :] or "-" in s[s.find("x") :]:
            # normalize by replacing first 'WxH' part
            tail = s[len(wh) :]
            # tail starts with + or -
            # split into x and y by last sign occurrence
            # find second sign (for y)
            if len(tail) < 2:
                return (w, _r2339_safe_int(h_s, 0), 0, 0)
            # tail like '+10+20' or '-10+20' or '+10-20'
            # find separator between x and y (the second sign)
            idx = 2
            while idx < len(tail) and tail[idx] not in ["+", "-"]:
                idx += 1
            x_s = tail[0:idx]
            y_s = tail[idx:]
            x = _r2339_safe_int(x_s, 0)
            y = _r2339_safe_int(y_s, 0)
            h = _r2339_safe_int(h_s, 0)
            return (w, h, x, y)
        return (w, _r2339_safe_int(h_s, 0), 0, 0)
    except Exception:
        return (0, 0, 0, 0)


def _r2340_is_offscreen(x, y, w, h, sw, sh, margin=30):
    # Accept if at least a reasonable part is visible
    try:
        if w <= 0 or h <= 0 or sw <= 0 or sh <= 0:
            return True
        vis_left = max(0, x)
        vis_top = max(0, y)
        vis_right = min(sw, x + w)
        vis_bottom = min(sh, y + h)
        vis_w = max(0, vis_right - vis_left)
        vis_h = max(0, vis_bottom - vis_top)
        # require at least margin x margin visible area
        if vis_w < margin or vis_h < margin:
            return True
        return False
    except Exception:
        return True


class DockManager:
    def __init__(self, app):
        self.app = app
        self._wins = {}  # key -> Toplevel

    def _safe_title(self, title):
        try:
            return str(title)
        except Exception:
            return "Undocked"

    def is_open(self, key):
        w = self._wins.get(key)
        if w is None:
            return False
        try:
            return bool(w.winfo_exists())
        except Exception:
            return False

    def close(self, key):
        # R2389_CLOSE_OPEN0: close => open=0 + remove from _wins (best-effort)

        w = None

        try:
            w = self._wins.get(key)

        except Exception:
            w = None

        geo = ""

        try:
            if w is not None:
                geo = str(w.wm_geometry())

        except Exception:
            geo = ""

        try:
            if w is not None:
                try:
                    w.destroy()

                except Exception:
                    try:
                        w.withdraw()

                    except Exception:
                        pass

        except Exception:
            pass

        try:
            if hasattr(self, "_wins") and isinstance(self._wins, dict):
                self._wins.pop(key, None)

        except Exception:
            pass

        try:
            from modules import config_loader

            cfg = config_loader.load()

            sec = "Docking"

            if not cfg.has_section(sec):
                cfg.add_section(sec)

            cfg.set(sec, key + ".open", "0")

            cfg.set(sec, key + ".docked", "0")

            if geo:
                cfg.set(sec, key + ".geometry", geo)

            config_loader.save(cfg)

        except Exception:
            pass

    def undock_readonly(self, key, title, builder_func, restore_geometry=None):
        # key: 'pipeline' | 'runner_products' | 'log'
        # builder_func(frame, app)
        if self.is_open(key):
            try:
                w = self._wins.get(key)
                if w is not None:
                    w.deiconify()
                    w.lift()
                    w.focus_force()
            except Exception:
                pass
            return

        w = tk.Toplevel(self.app)
        # R2355_DOCK_DIAG: log INI + restore decision (no behavior change)
        try:
            ini = _r2339_ini_path(self.app)
            cfg = _r2339_cfg_read(ini)
            sec = "Docking"
            geo = _r2339_cfg_get(cfg, sec, str(key) + ".geometry", "")
            ww = _r2339_cfg_get(cfg, sec, str(key) + ".w", "")
            hh = _r2339_cfg_get(cfg, sec, str(key) + ".h", "")
            xx = _r2339_cfg_get(cfg, sec, str(key) + ".x", "")
            yy = _r2339_cfg_get(cfg, sec, str(key) + ".y", "")
            op = _r2339_cfg_get(cfg, sec, str(key) + ".open", "")
            keys = _r2339_cfg_get(cfg, sec, "keys", "")
            _r2355_diag(
                self.app,
                f"undock key={key} ini={ini} keys={keys} open={op} geo={geo} w={ww} h={hh} x={xx} y={yy} restore_in={restore_geometry}",
            )
        except Exception as e:
            _r2355_diag(self.app, f"ini_read_failed key={key} err={e!r}")
        # R2352_RESTORE_FIX: ensure restore_geometry from INI x/y/w/h when caller passes None
        try:
            if not restore_geometry:
                ini = _r2339_ini_path(self.app)
                cfg2 = _r2339_cfg_read(ini)
                sec2 = "Docking"
                ww = _r2339_safe_int(_r2339_cfg_get(cfg2, sec2, str(key) + ".w", "0"), 0)
                hh = _r2339_safe_int(_r2339_cfg_get(cfg2, sec2, str(key) + ".h", "0"), 0)
                xx = _r2339_safe_int(_r2339_cfg_get(cfg2, sec2, str(key) + ".x", "0"), 0)
                yy = _r2339_safe_int(_r2339_cfg_get(cfg2, sec2, str(key) + ".y", "0"), 0)
                if ww > 1 and hh > 1:
                    # offscreen guard; if screen size not ready yet, skip guard and apply anyway
                    try:
                        sw = _r2339_safe_int(self.app.winfo_screenwidth(), 0)
                        sh = _r2339_safe_int(self.app.winfo_screenheight(), 0)
                    except Exception:
                        sw = 0
                        sh = 0
                    if sw > 0 and sh > 0:
                        if not _r2340_is_offscreen(xx, yy, ww, hh, sw, sh):
                            restore_geometry = (
                                str(ww) + "x" + str(hh) + "+" + str(xx) + "+" + str(yy)
                            )
                    else:
                        restore_geometry = str(ww) + "x" + str(hh) + "+" + str(xx) + "+" + str(yy)
        except Exception:
            pass
        # R2352_RESTORE_FIX: removed buggy call (cfg/sec undefined)
        try:
            w.attributes("-topmost", True)
        except Exception:
            pass
        w.title(self._safe_title(title) + " (Undocked)")
        # R2339: center only on first open; restore geometry if provided
        _r2355_diag(self.app, f"restore_branch key={key} restore_geometry={restore_geometry!r}")
        if restore_geometry:
            # R2361_GEOMETRY_PERSIST
            geo = cfg.get("Docking", f"{key}.geometry", fallback="").strip()
            if geo:
                # Wichtig: restore_geometry muss STRING bleiben, sonst fällt Restore auf Center/WM-Default zurück
                restore_geometry = geo
            try:
                w.withdraw()
            except Exception:
                pass
            try:
                # apply after idle to avoid window-manager overriding geometry
                try:
                    w.after_idle(lambda g=str(restore_geometry): w.geometry(g))
                except Exception:
                    w.geometry(str(restore_geometry))
            except Exception:
                pass
            try:
                w.deiconify()
            except Exception:
                pass
        else:
            try:
                _center_window(w, 900, 700, parent=self.app)
            except Exception:
                pass

        outer = tk.Frame(w)
        outer.pack(fill="both", expand=True)

        # Mini-Header
        hdr = tk.Frame(outer)
        hdr.pack(fill="x", padx=6, pady=6)
        tk.Label(hdr, text=self._safe_title(title), anchor="w").pack(side="left")

        # R2342_FORCE_PERSIST_ON_CLOSE
        def _request_close():
            try:
                # persist THIS window right now (geometry + keys)
                if hasattr(self, "_persist_one"):
                    self._persist_one(key, w)
            except Exception:
                pass
            try:
                self.close(key)
            except Exception:
                pass

        btn = tk.Button(hdr, text="Schliessen", command=_request_close)
        btn.pack(side="right")

        body = tk.Frame(outer)
        body.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        # Build content fresh (read-only viewers)
        try:
            builder_func(body, self.app)
        except Exception as exc:
            try:
                tk.Label(body, text="Undock-Fehler: " + repr(exc), anchor="w").pack(
                    anchor="w", padx=8, pady=8
                )
            except Exception:
                pass

        def _on_close():
            _request_close()

        try:
            w.protocol("WM_DELETE_WINDOW", lambda: self.close(key))
        except Exception:
            pass

        self._wins[key] = w

    def _persist_one(self, key, w):
        ini = _r2339_ini_path(self.app)
        try:
            print("[Docking] INI path:", ini)
        except Exception:
            pass
        cfg = _r2339_cfg_read(ini)
        sec = "Docking"
        if not cfg.has_section(sec):
            cfg.add_section(sec)
        try:
            w.update_idletasks()
        except Exception:
            pass
        ww = 0
        hh = 0
        xx = 0
        yy = 0
        try:
            g = w.wm_geometry()
            ww, hh, xx, yy = _r2340_parse_geo(g)
        except Exception:
            pass
        _r2339_cfg_set(cfg, sec, str(key) + ".w", ww)
        _r2339_cfg_set(cfg, sec, str(key) + ".h", hh)
        _r2339_cfg_set(cfg, sec, str(key) + ".x", xx)
        _r2339_cfg_set(cfg, sec, str(key) + ".y", yy)
        _r2339_cfg_set(cfg, sec, str(key) + ".open", "1")
        keys_raw = _r2339_cfg_get(cfg, sec, "keys", "")
        keys = [k.strip() for k in str(keys_raw).split(",") if k.strip()]
        if str(key) not in keys:
            keys.append(str(key))
        _r2339_cfg_set(cfg, sec, "keys", ",".join(keys))
        _r2339_cfg_write(cfg, ini)

    def persist_all(self):
        ini = _r2339_ini_path(self.app)
        try:
            print("[Docking] INI path:", ini)
        except Exception:
            pass
        cfg = _r2339_cfg_read(ini)
        sec = "Docking"
        keys = []
        for key, w in list(self._wins.items()):
            try:
                if w is None or (hasattr(w, "winfo_exists") and not w.winfo_exists()):
                    continue
                self._persist_one(key, w)
                keys.append(str(key))
            except Exception:
                pass
        if not cfg.has_section(sec):
            cfg.add_section(sec)
        _r2339_cfg_set(cfg, sec, "keys", ",".join(keys))
        _r2339_cfg_write(cfg, ini)
        return True

    def _restore_window_from_ini(self, cfg, sec, key, lab, builder, sw, sh):
        try:
            open_v = str(_r2339_cfg_get(cfg, sec, key + ".open", "1")).strip()
            docked_v = str(_r2339_cfg_get(cfg, sec, key + ".docked", "0")).strip()
        except Exception:
            open_v, docked_v = "1", "0"
        if open_v != "1" or docked_v == "1":
            return False

        geo = str(_r2339_cfg_get(cfg, sec, key + ".geometry", "")).strip()
        ww = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + ".w", "0"), 0)
        hh = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + ".h", "0"), 0)
        xx = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + ".x", "0"), 0)
        yy = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + ".y", "0"), 0)

        restore_geo = None
        if geo:
            try:
                w2, h2, x2, y2 = _r2340_parse_geo(geo)
                if (
                    w2 > 1
                    and h2 > 1
                    and sw > 0
                    and sh > 0
                    and not _r2340_is_offscreen(x2, y2, w2, h2, sw, sh)
                ):
                    restore_geo = geo
            except Exception:
                restore_geo = None

        if restore_geo is None and ww > 1 and hh > 1 and sw > 0 and sh > 0:
            if not _r2340_is_offscreen(xx, yy, ww, hh, sw, sh):
                restore_geo = str(ww) + "x" + str(hh) + "+" + str(xx) + "+" + str(yy)

        self._restore_window_from_ini(cfg, sec, key, lab, builder, sw, sh)
        return True

    def restore_from_ini(self):
        ini = _r2339_ini_path(self.app)
        try:
            print("[Docking] INI path:", ini)
        except Exception:
            pass
        cfg = _r2339_cfg_read(ini)
        sec = "Docking"
        keys_raw = _r2339_cfg_get(cfg, sec, "keys", "")
        keys = [k.strip() for k in str(keys_raw).split(",") if k.strip()]
        if not keys:
            return False

        mapping = {}
        try:
            from modules import ui_pipeline_tab

            mapping["pipeline"] = ("Pipeline", ui_pipeline_tab.build_pipeline_tab)
        except Exception:
            pass
        try:
            from modules import ui_runner_products_tab

            mapping["runner_products"] = (
                "Artefakte",
                ui_runner_products_tab.build_runner_products_tab,
            )
        except Exception:
            pass
        try:
            from modules import ui_log_tab

            mapping["log"] = ("Log", ui_log_tab.build_log_tab)
        except Exception:
            pass

        sw = 0
        sh = 0
        try:
            sw = _r2339_safe_int(self.app.winfo_screenwidth(), 0)
            sh = _r2339_safe_int(self.app.winfo_screenheight(), 0)
        except Exception:
            pass

        any_open = False
        for key in keys:
            if key not in mapping:
                continue
            if self.is_open(key):
                continue
            lab, builder = mapping[key]
            # Respect persisted open/docked flags
            try:
                open_v = str(_r2339_cfg_get(cfg, sec, key + ".open", "0")).strip()
                docked_v = str(_r2339_cfg_get(cfg, sec, key + ".docked", "0")).strip()
            except Exception:
                open_v, docked_v = "0", "0"
            if open_v != "1" or docked_v == "1":
                continue
            # Prefer geometry string (WxH+X+Y)
            restore_geo = ""
            try:
                restore_geo = str(_r2339_cfg_get(cfg, sec, key + ".geometry", "")).strip()
            except Exception:
                restore_geo = ""
            if restore_geo:
                try:
                    ww, hh, xx, yy = _r2340_parse_geo(restore_geo)
                    if ww > 1 and hh > 1 and sw > 0 and sh > 0:
                        if _r2340_is_offscreen(xx, yy, ww, hh, sw, sh):
                            restore_geo = ""
                except Exception:
                    restore_geo = ""
            # Fallback: legacy w/h/x/y if geometry missing
            if not restore_geo:
                ww = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + ".w", "0"), 0)
                hh = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + ".h", "0"), 0)
                xx = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + ".x", "0"), 0)
                yy = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + ".y", "0"), 0)
                if ww > 1 and hh > 1 and sw > 0 and sh > 0:
                    if not _r2340_is_offscreen(xx, yy, ww, hh, sw, sh):
                        restore_geo = str(ww) + "x" + str(hh) + "+" + str(xx) + "+" + str(yy)
            self.undock_readonly(key, lab, builder, restore_geometry=(restore_geo or None))
            any_open = True
        return any_open


def install_notebook_context_menu(app, notebook):
    # Right-click context menu on tabs for undock (Phase-1: read-only tabs only)
    dm = getattr(app, "_dock_manager", None)
    if dm is None:
        dm = DockManager(app)
        app._dock_manager = dm
        try:
            dm.restore_from_ini()
        except Exception:
            pass

    # resolve builders lazily to avoid import cycles
    def _get_targets():
        targets = []
        try:
            from modules import ui_pipeline_tab

            targets.append(("Pipeline", "pipeline", ui_pipeline_tab.build_pipeline_tab))
        except Exception:
            pass
        try:
            from modules import ui_runner_products_tab

            targets.append(
                ("Artefakte", "runner_products", ui_runner_products_tab.build_runner_products_tab)
            )
        except Exception:
            pass
        try:
            from modules import ui_log_tab

            targets.append(("Log", "log", ui_log_tab.build_log_tab))
        except Exception:
            pass
        return targets

    def _tab_text_at(idx):
        try:
            return notebook.tab(idx, "text")
        except Exception:
            return ""

    def _on_right_click(ev):
        try:
            idx = notebook.index(f"@{ev.x},{ev.y}")
        except Exception:
            return
        tab_text = _tab_text_at(idx)
        targets = _get_targets()
        chosen = None
        for label, key, builder in targets:
            if label == tab_text:
                chosen = (label, key, builder)
                break
        if chosen is None:
            return

        label, key, builder = chosen
        menu = tk.Menu(app, tearoff=0)
        menu.add_command(label="Undock", command=lambda: dm.undock_readonly(key, label, builder))
        if dm.is_open(key):
            menu.add_command(label="Dock (Fenster schließen)", command=lambda: dm.close(key))
        try:
            menu.tk_popup(ev.x_root, ev.y_root)
        finally:
            try:
                menu.grab_release()
            except Exception:
                pass

    try:
        notebook.bind("<Button-3>", _on_right_click)
    except Exception:
        pass
    return dm


# R2342_FORCE_PERSIST_ON_CLOSE

# R2343_HARD_INI_GEOMETRY


def _r2351_apply_ini_geometry(w, cfg, sec, key, center_fn=None):
    """Apply geometry from INI.
    Priority: <key>.geometry, else build from w/h/x/y. Center only if nothing usable or offscreen.
    """
    try:
        # read geometry if present
        geo = None
        try:
            geo = _r2339_cfg_get(cfg, sec, str(key) + ".geometry", "")
        except Exception:
            geo = ""
        if not geo:
            try:
                ww = _r2339_safe_int(_r2339_cfg_get(cfg, sec, str(key) + ".w", 0), 0)
                hh = _r2339_safe_int(_r2339_cfg_get(cfg, sec, str(key) + ".h", 0), 0)
                xx = _r2339_safe_int(_r2339_cfg_get(cfg, sec, str(key) + ".x", 0), 0)
                yy = _r2339_safe_int(_r2339_cfg_get(cfg, sec, str(key) + ".y", 0), 0)
                if ww > 0 and hh > 0:
                    geo = str(ww) + "x" + str(hh) + "+" + str(xx) + "+" + str(yy)
            except Exception:
                pass
        if geo:
            try:
                w.geometry(geo)
            except Exception:
                pass
            # offscreen guard (single monitor): clamp to visible area, else center
            try:
                w.update_idletasks()
                sx = w.winfo_screenwidth()
                sy = w.winfo_screenheight()
                x = w.winfo_x()
                y = w.winfo_y()
                ww2 = w.winfo_width()
                hh2 = w.winfo_height()
                if (x + ww2) < 10 or (y + hh2) < 10 or x > (sx - 10) or y > (sy - 10):
                    if center_fn:
                        center_fn(w)
            except Exception:
                pass
        else:
            if center_fn:
                center_fn(w)
    except Exception:
        if center_fn:
            try:
                center_fn(w)
            except Exception:
                pass


# R2351_APPLY_INI_GEOMETRY

# R2352_RESTORE_FIX


# R2355_DOCK_DIAG
def _r2355_diag(app, msg):
    try:
        try:
            from . import exception_logger

            exception_logger.log(f"[DOCK_DIAG] {msg}")
            return
        except Exception:
            pass
        print(f"[DOCK_DIAG] {msg}")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# R2367_DOCKING_PERSIST_HARDFIX
# Zweck:
# - garantiertes Schreiben von [Docking] nach ShrimpDev.ini (MERGE-write)
# - Persist aus wm_geometry() (WxH+X+Y)
# - umgeht kaputte/inkonsistente Alt-Helper
# ---------------------------------------------------------------------------
def _r2367_ini_path():
    import os

    try:
        _root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    except Exception:
        _root = os.getcwd()
    return os.path.join(_root, "ShrimpDev.ini")


def _r2367_read_cfg(path):
    import configparser, os

    cfg = configparser.ConfigParser()
    try:
        if path and os.path.isfile(path):
            cfg.read(path, encoding="utf-8")
    except Exception:
        try:
            cfg.read(path)
        except Exception:
            pass
    return cfg


def _r2367_merge_write(cfg, path):
    import configparser, os

    base = configparser.ConfigParser()
    try:
        if path and os.path.isfile(path):
            base.read(path, encoding="utf-8")
    except Exception:
        pass

    for sec in cfg.sections():
        if not base.has_section(sec):
            base.add_section(sec)
        for k, v in cfg.items(sec):
            base.set(sec, k, str(v))

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except Exception:
        pass

    with open(path, "w", encoding="utf-8") as f:
        base.write(f)


def _r2367_persist_one(self, key, win):
    ini = _r2367_ini_path()
    try:
        print("[Docking][R2367] persist_one key=", key, "ini=", ini)
    except Exception:
        pass

    cfg = _r2367_read_cfg(ini)
    sec = "Docking"
    if not cfg.has_section(sec):
        cfg.add_section(sec)

    geo = ""
    try:
        win.update_idletasks()
    except Exception:
        pass
    try:
        geo = str(win.wm_geometry())
    except Exception:
        geo = ""

    if geo:
        cfg.set(sec, key + ".geometry", geo)

    cfg.set(sec, key + ".open", "1")
    cfg.set(sec, key + ".docked", "0")

    keys = []
    try:
        raw = cfg.get(sec, "keys", fallback="").strip()
        if raw:
            keys = [k.strip() for k in raw.split(",") if k.strip()]
    except Exception:
        keys = []
    if key not in keys:
        keys.append(key)
    cfg.set(sec, "keys", ",".join(keys))

    _r2367_merge_write(cfg, ini)
    return True


def _r2367_persist_all(self):
    ini = _r2367_ini_path()
    try:
        print("[Docking][R2367] persist_all ini=", ini)
    except Exception:
        pass

    wins = {}
    try:
        wins = getattr(self, "_wins", None) or {}
    except Exception:
        wins = {}

    for key, win in list(wins.items()):
        try:
            self._persist_one(key, win)
        except Exception:
            pass
    return True


# Monkeypatch in DockManager
try:
    DockManager._persist_one = _r2367_persist_one
    DockManager.persist_all = _r2367_persist_all
except Exception:
    pass


# ---------------------------------------------------------------------------
# R2368_DOCKING_RESTORE_HARDFIX
# Zweck:
# - Restore aus ShrimpDev.ini [Docking] <key>.geometry (WxH+X+Y)
# - Offscreen-Schutz -> fallback center
# - Monkeypatch: keine riskanten Umbauten
# ---------------------------------------------------------------------------
def _r2368_ini_path():
    import os

    try:
        _root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    except Exception:
        _root = os.getcwd()
    return os.path.join(_root, "ShrimpDev.ini")


def _r2368_read_cfg(path):
    import configparser, os

    cfg = configparser.ConfigParser()
    try:
        if path and os.path.isfile(path):
            cfg.read(path, encoding="utf-8")
    except Exception:
        try:
            cfg.read(path)
        except Exception:
            pass
    return cfg


def _r2368_parse_geo(geo):
    # "WxH+X+Y"
    import re

    m = re.match(r"^\s*(\d+)x(\d+)\+(-?\d+)\+(-?\d+)\s*$", str(geo))
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))


def _r2368_offscreen(win, w, h, x, y):
    try:
        sw = int(win.winfo_screenwidth())
        sh = int(win.winfo_screenheight())
    except Exception:
        return False
    # simple bounds (1 monitor assumption)
    if x < 0 or y < 0:
        return True
    if x + w > sw or y + h > sh:
        return True
    return False


def _r2368_restore_one(self, key, win):
    ini = _r2368_ini_path()
    cfg = _r2368_read_cfg(ini)
    if not cfg.has_section("Docking"):
        return False

    geo = cfg.get("Docking", key + ".geometry", fallback="").strip()
    if not geo:
        return False

    parsed = _r2368_parse_geo(geo)
    if not parsed:
        return False

    w, h, x, y = parsed

    try:
        win.update_idletasks()
    except Exception:
        pass

    if _r2368_offscreen(win, w, h, x, y):
        # fallback center (nur dann!)
        try:
            if hasattr(self, "_center_window"):
                self._center_window(win)
            else:
                # fallback center minimal
                sw = int(win.winfo_screenwidth())
                sh = int(win.winfo_screenheight())
                nx = int((sw - w) / 2)
                ny = int((sh - h) / 2)
                w.geometry(str(w) + "x" + str(h) + "+" + str(nx) + "+" + str(ny))
        except Exception:
            pass
        try:
            print("[Docking][R2368] offscreen -> center key=", key, "geo=", geo)
        except Exception:
            pass
        return True

    try:
        w.geometry(geo)
        try:
            print("[Docking][R2368] restore key=", key, "geo=", geo)
        except Exception:
            pass
        return True
    except Exception:
        return False


# Monkeypatch: restore hook verfügbar machen
try:
    DockManager._restore_one = _r2368_restore_one
except Exception:
    pass


# ---------------------------------------------------------------------------
# R2369_DOCKING_STATE_V2
# Docking State v2:
# - pro Fenster 1 Datensatz: open/docked/geometry/ts
# - keys: main, log, pipeline, runner_products (Artefakte)
# - MERGE-write, Projektroot/ShrimpDev.ini
# - Diagnose-Prints (werden im Log-Tab sichtbar)
# ---------------------------------------------------------------------------
def _r2369_now_iso():
    import datetime

    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _r2369_ini_path():
    import os

    try:
        _root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    except Exception:
        _root = os.getcwd()
    return os.path.join(_root, "ShrimpDev.ini")


def _r2369_read_cfg(path):
    import configparser, os

    cfg = configparser.ConfigParser()
    try:
        if path and os.path.isfile(path):
            cfg.read(path, encoding="utf-8")
    except Exception:
        try:
            cfg.read(path)
        except Exception:
            pass
    return cfg


def _r2369_merge_write(cfg, path):
    import configparser, os

    base = configparser.ConfigParser()
    try:
        if path and os.path.isfile(path):
            base.read(path, encoding="utf-8")
    except Exception:
        pass

    for sec in cfg.sections():
        if not base.has_section(sec):
            base.add_section(sec)
        for k, v in cfg.items(sec):
            base.set(sec, k, str(v))

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except Exception:
        pass

    with open(path, "w", encoding="utf-8") as f:
        base.write(f)


def _r2369_set_record(cfg, key, open_flag, docked_flag, geo):
    sec = "Docking"
    if not cfg.has_section(sec):
        cfg.add_section(sec)
    cfg.set(sec, key + ".open", "1" if open_flag else "0")
    cfg.set(sec, key + ".docked", "1" if docked_flag else "0")
    cfg.set(sec, key + ".geometry", str(geo or "").strip())
    cfg.set(sec, key + ".ts", _r2369_now_iso())

    # keys-liste pflegen
    keys = []
    try:
        raw = cfg.get(sec, "keys", fallback="").strip()
        if raw:
            keys = [k.strip() for k in raw.split(",") if k.strip()]
    except Exception:
        keys = []
    if key not in keys:
        keys.append(key)
    cfg.set(sec, "keys", ",".join(keys))


def _r2369_safe_geo(win):
    try:
        win.update_idletasks()
    except Exception:
        pass
    try:
        return str(win.wm_geometry())
    except Exception:
        return ""


def _r2369_persist_one(self, key, win, docked_flag=False):
    ini = _r2369_ini_path()
    cfg = _r2369_read_cfg(ini)
    geo = _r2369_safe_geo(win)
    _r2369_set_record(cfg, key, True, bool(docked_flag), geo)
    _r2369_merge_write(cfg, ini)
    try:
        print(
            "[Docking][R2369] persist key=",
            key,
            "geo=",
            geo,
            "ts=",
            cfg.get("Docking", key + ".ts", fallback=""),
        )
    except Exception:
        pass
    return True


def _r2369_persist_all(self):
    ini = _r2369_ini_path()
    cfg = _r2369_read_cfg(ini)

    # 1) Main window (Shrimpi) – falls DockManager app kennt
    app = getattr(self, "app", None)
    if app is not None:
        try:
            geo_main = _r2369_safe_geo(app)
            # R2388_UI_GEOMETRY_MIRROR: main_gui uses [UI].geometry
            try:
                if geo_main:
                    if not cfg.has_section("UI"):
                        cfg.add_section("UI")
                    cfg.set("UI", "geometry", str(geo_main))
            except Exception:
                pass

            _r2369_set_record(cfg, "main", True, True, geo_main)
            try:
                print("[Docking][R2369] persist main geo=", geo_main)
            except Exception:
                pass
        except Exception:
            pass

        # 2) Log-Window (best-effort: häufige Attribute)
        log_win = None
        for name in (
            "log_window",
            "_log_window",
            "log_toplevel",
            "_log_toplevel",
            "win_log",
            "_win_log",
        ):
            try:
                cand = getattr(app, name, None)
                if cand is not None:
                    log_win = cand
                    break
            except Exception:
                pass
        if log_win is not None:
            try:
                geo_log = _r2369_safe_geo(log_win)
                _r2369_set_record(cfg, "log", True, False, geo_log)
                try:
                    print("[Docking][R2369] persist log geo=", geo_log)
                except Exception:
                    pass
            except Exception:
                pass
        else:
            # record exists but closed/unknown
            _r2369_set_record(cfg, "log", False, False, "")

    # 3) Undocked windows aus _wins
    wins = {}
    try:
        wins = getattr(self, "_wins", None) or {}
    except Exception:
        wins = {}
    for key, win in list(wins.items()):
        try:
            geo = _r2369_safe_geo(win)
            _r2369_set_record(cfg, key, True, False, geo)
            try:
                print("[Docking][R2369] persist undocked key=", key, "geo=", geo)
            except Exception:
                pass
        except Exception:
            pass

    _r2369_merge_write(cfg, ini)
    return True


def _r2369_restore_one(self, key, win):
    ini = _r2369_ini_path()
    cfg = _r2369_read_cfg(ini)
    if not cfg.has_section("Docking"):
        try:
            print("[Docking][R2369] restore key=", key, "no [Docking]")
        except Exception:
            pass
        return False

    geo = ""
    try:
        geo = cfg.get("Docking", key + ".geometry", fallback="").strip()
    except Exception:
        geo = ""

    applied = 0
    if geo:
        try:
            w.geometry(geo)
            applied = 1
        except Exception:
            applied = 0

    try:
        print(
            "[Docking][R2369] restore key=",
            key,
            "geo=",
            geo,
            "applied=",
            applied,
            "ts=",
            cfg.get("Docking", key + ".ts", fallback=""),
        )
    except Exception:
        pass
    return bool(applied)


# Monkeypatch
try:
    DockManager.persist_all = _r2369_persist_all
    DockManager._persist_one = _r2369_persist_one
    DockManager._restore_one = _r2369_restore_one
except Exception:
    pass
