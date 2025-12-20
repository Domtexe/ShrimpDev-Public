@echo off
setlocal
set ROOT=D:\ShrimpDev
set MOD=%ROOT%\modules
set ARCH=%ROOT%\_Archiv
set SRC=%MOD%\module_code_intake.py
set SHIM=%MOD%\module_shim_intake.py
set ADD=%MOD%\module_intake_core_addons.py

echo [R1240] AllInOne starting...

:: 1) Backup (nur wenn vorhanden)
if exist "%SRC%" (
  copy /y "%SRC%" "%ARCH%\module_code_intake.py.%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%.bak" >nul
  echo [R1240] Backup created for module_code_intake.py
)

:: 2) (Re)write Addon mit LED/AutoDetect + SaveAs ins Menü, Button verstecken
py - <<'PY'
from pathlib import Path
mod_dir=Path(r"%MOD%")
add=mod_dir/"module_intake_core_addons.py"
code=r'''# -*- coding: utf-8 -*-
"""
Intake Core Add-ons (idempotent, nicht-invasiv):
- LED-Logik: ok_name, ok_ext, ok_syntax, ok_all (ok_all nur grün, wenn nicht dirty)
- Auto-Detect nach Insert/Änderung
- "Speichern unter" als Menüeintrag; Button "Speichern unter" wird versteckt.
- "Speichern" bleibt als Hauptbutton.
"""
from __future__ import annotations

def apply_intake_core_addons(mod):
    Dev=getattr(mod,"DevIntake",None)
    if Dev is None or getattr(Dev,"_addon_intake_core_applied_",False): 
        return

    def _led_eval(self):
        ok_name=bool(getattr(self,"var_name",None) and self.var_name.get().strip())
        ok_ext =bool(getattr(self,"var_ext",None)  and self.var_ext.get().strip())
        ok_syntax=True
        if hasattr(self,"_check_syntax"):
            try: ok_syntax=bool(self._check_syntax())
            except Exception: ok_syntax=False
        ok_all=(ok_name and ok_ext and ok_syntax and (not getattr(self,"_dirty",False)))
        return ok_name,ok_ext,ok_syntax,ok_all

    def _update_leds(self):
        try:
            ok_name,ok_ext,ok_syntax,ok_all=_led_eval(self)
            if hasattr(self,"led_name"):   self.led_name.config(foreground=("green" if ok_name else "red"))
            if hasattr(self,"led_ext"):    self.led_ext.config(foreground=("green" if ok_ext else "red"))
            if hasattr(self,"led_syntax"): self.led_syntax.config(foreground=("green" if ok_syntax else "red"))
            if hasattr(self,"led_all"):    self.led_all.config(foreground=("green" if ok_all else "red"))
        except Exception:
            pass

    old_on_mod=getattr(Dev,"_on_mod",None)
    def _on_mod(self,*a,**kw):
        if callable(old_on_mod):
            try: old_on_mod(self,*a,**kw)
            except Exception: pass
        try:
            self._dirty=True
            _update_leds(self)
        except Exception:
            pass

    old_insert=getattr(Dev,"_insert",None)
    def _insert(self):
        res=old_insert(self) if callable(old_insert) else None
        try:
            if hasattr(self,"_detect"): self._detect()
            _update_leds(self)
        except Exception:
            pass
        return res

    old_save_as=getattr(Dev,"_save_as",None)
    def _save_as(self):
        # Endung aus Combo übernehmen, wenn vorhanden
        try:
            if hasattr(self,"cmb_ext"):
                ext=self.cmb_ext.get().strip()
                if ext and hasattr(self,"var_ext"): self.var_ext.set(ext)
        except Exception:
            pass
        res=old_save_as(self) if callable(old_save_as) else getattr(self,"_save",lambda:None)()
        try:
            self._dirty=False
            _update_leds(self)
        except Exception:
            pass
        return res

    # Monkey-Patches setzen
    Dev._update_leds=_update_leds
    Dev._on_mod=_on_mod
    Dev._insert=_insert
    Dev._save_as=_save_as

    # UI-Nacharbeiten zur Laufzeit
    _old_build=getattr(Dev,"_build_ui",None)
    def _build_ui(self):
        r=_old_build(self) if callable(_old_build) else None
        # "Speichern unter" Button verstecken, falls vorhanden
        for attr in ("btn_save_as","button_save_as","btn_speichern_unter"):
            b=getattr(self,attr,None)
            try:
                if b: b.grid_forget() if hasattr(b,"grid_info") else b.pack_forget()
            except Exception: pass
        # Menüeintrag "Speichern unter..." in die Top-Menüleiste
        try:
            import tkinter as tk
            top=self.winfo_toplevel()
            if not hasattr(top,"_intake_menu_injected_"):
                mbar=getattr(top,"_menubar_",None)
                if mbar is None:
                    mbar=tk.Menu(top)
                    top.config(menu=mbar)
                    top._menubar_=mbar
                # Datei-Menü finden/erstellen
                file_menu=getattr(top,"_menu_file_",None)
                if file_menu is None:
                    file_menu=tk.Menu(mbar, tearoff=False)
                    mbar.add_cascade(label="Datei", menu=file_menu)
                    top._menu_file_=file_menu
                # Eintrag "Speichern unter..." idempotent hinzufügen
                labels=[file_menu.entrycget(i,"label") for i in range(file_menu.index("end")+1)] if file_menu.index("end") is not None else []
                if "Speichern unter..." not in labels:
                    file_menu.add_command(label="Speichern unter...", command=lambda:self._save_as())
                top._intake_menu_injected_=True
        except Exception:
            pass
        # LEDs initial zeichnen
        try: self._dirty=False; _update_leds(self)
        except Exception: pass
        return r
    Dev._build_ui=_build_ui

    Dev._addon_intake_core_applied_=True
'''
add.write_text(code,encoding="utf-8")
print("[R1240] Addon file written.")
PY
if errorlevel 1 goto :ERR

:: 3) Hook am Ende von module_code_intake.py (nur wenn noch nicht vorhanden)
py - <<'PY'
from pathlib import Path, py_compile
src=Path(r"%SRC%")
txt=src.read_text(encoding="utf-8")
hook = """
# --- Intake Core Addons Hook (idempotent) ---
try:
    from modules import module_intake_core_addons as _ia
    _ia.apply_intake_core_addons(__import__("modules.module_code_intake"))
except Exception:
    pass
"""
if "Intake Core Addons Hook" not in txt:
    src.write_text(txt.rstrip()+"\n"+hook,encoding="utf-8")
py_compile.compile(str(src), doraise=True)
print("[R1240] Hook ensured & syntax OK.")
PY
if errorlevel 1 goto :ERR

:: 4) Shim härten (robustes Mounting)
if exist "%SHIM%" copy /y "%SHIM%" "%ARCH%\module_shim_intake.py.%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%.bak" >nul
py - <<'PY'
from pathlib import Path, py_compile
p=Path(r"%SHIM%")
code=r'''# -*- coding: utf-8 -*-
from __future__ import annotations
def mount_intake_tab(nb):
    import importlib, tkinter.ttk as ttk, tkinter as tk
    mod = importlib.import_module("modules.module_code_intake")
    # Tab "Intake" schon vorhanden?
    try:
        for i in range(nb.index("end")):
            if nb.tab(i,"text")=="Intake": return
    except Exception:
        pass
    # 1) create_intake_tab verfügbar?
    if hasattr(mod,"create_intake_tab"):
        return mod.create_intake_tab(nb)
    # 2) DevIntake Klasse direkt montieren
    Dev=getattr(mod,"DevIntake",None)
    if Dev:
        f=ttk.Frame(nb)
        try: Dev(f)
        except TypeError: Dev()
        nb.add(f,text="Intake"); return
    # 3) Fallback
    f=tk.Frame(nb,bg="#ffeeee")
    tk.Label(f,text="Intake Shim – Fallback aktiv",fg="red",bg="#ffeeee").pack(padx=12,pady=12)
    nb.add(f,text="Intake")
'''
p.write_text(code,encoding="utf-8")
py_compile.compile(str(p), doraise=True)
print("[R1240] Shim hardened & syntax OK.")
PY
if errorlevel 1 goto :ERR

:: 5) SyntaxGate (alle Module)
py - <<'PY'
from pathlib import Path, py_compile, sys
root=Path(r"%MOD%"); bad=[]
for f in root.rglob("*.py"):
    try: py_compile.compile(str(f), doraise=True)
    except Exception as e: bad.append((str(f), e))
if bad:
    print("[R1240] Syntaxfehler:")
    for f,e in bad: print(" -",f,":",e)
    sys.exit(1)
print("[R1240] Syntax OK for all modules.")
PY
if errorlevel 1 goto :ERR

:: 6) Start GUI
echo [R1240] Launching GUI...
py -3 -u "%ROOT%\main_gui.py"
echo [R1240] Done.
exit /b 0

:ERR
echo [R1240] FAILED. See console above.
exit /b 1
