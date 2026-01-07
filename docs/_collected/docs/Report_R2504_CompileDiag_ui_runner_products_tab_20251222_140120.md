# R2504 – Compile Diag ui_runner_products_tab.py (READ-ONLY)

- Time: 20251222_140120
- Target: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py`

## Compile
- py_compile: FAIL
- Error: `Sorry: IndentationError: expected an indented block after 'if' statement on line 168 (ui_runner_products_tab.py, line 169)`

## Context around line 168
```text
   L00108:     # DropEffect = COPY
   L00109:     fmt = user32.RegisterClipboardFormatW(CFSTR_PREFERREDDROPEFFECT)
   L00110:     hfx = kernel32.GlobalAlloc(GMEM_MOVEABLE, 4)
   L00111:     if not hfx:
   L00112:         # not fatal; proceed without drop effect
   L00113:         hfx = None
   L00114:     else:
   L00115:         pfx = kernel32.GlobalLock(hfx)
   L00116:         if not pfx:
   L00117:             kernel32.GlobalFree(hfx)
   L00118:             hfx = None
   L00119:         else:
   L00120:             try:
   L00121:                 ctypes.memmove(pfx, ctypes.byref(ctypes.c_uint(DROPEFFECT_COPY)), 4)
   L00122:             finally:
   L00123:                 kernel32.GlobalUnlock(hfx)
   L00124: 
   L00125:     # Open clipboard (retry)
   L00126:     hwnd_val = wintypes.HWND(hwnd or 0)
   L00127:     for attempt in range(1, 6):
   L00128:         if user32.OpenClipboard(hwnd_val):
   L00129:             break
   L00130:         time.sleep(0.05 * attempt)
   L00131:     else:
   L00132:         kernel32.GlobalFree(hglob)
   L00133:         if hfx: kernel32.GlobalFree(hfx)
   L00134:         return False, _fmt_last_error("OpenClipboard failed (busy/owner)")
   L00135: 
   L00136:     try:
   L00137:         user32.EmptyClipboard()
   L00138: 
   L00139:         res = user32.SetClipboardData(CF_HDROP, hglob)
   L00140:         if not res:
   L00141:             diag = _fmt_last_error("SetClipboardData(CF_HDROP) failed")
   L00142:             kernel32.GlobalFree(hglob)
   L00143:             if hfx: kernel32.GlobalFree(hfx)
   L00144:             return False, diag
   L00145: 
   L00146:         # Ownership transfers to clipboard; do NOT free hglob after success
   L00147: 
   L00148:         # Also provide plaintext paths for apps that paste text (e.g. chat/editor).
   L00149:         # Explorer will still prefer CF_HDROP for Ctrl+V file copy.
   L00150:         CF_UNICODETEXT = 13
   L00151:         try:
   L00152:             text_payload = "\r\n".join([str(p) for p in file_paths]) + "\r\n"
   L00153:             text_data = text_payload.encode("utf-16le") + b"\x00\x00"
   L00154:             htxt = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(text_data))
   L00155:             if htxt:
   L00156:                 ptxt = kernel32.GlobalLock(htxt)
   L00157:                 if ptxt:
   L00158:                     try:
   L00159:                         ctypes.memmove(ptxt, text_data, len(text_data))
   L00160:                     finally:
   L00161:                         kernel32.GlobalUnlock(htxt)
   L00162:                     # transfer ownership to clipboard
   L00163:                     user32.SetClipboardData(CF_UNICODETEXT, htxt)
   L00164:                 else:
   L00165:                     kernel32.GlobalFree(htxt)
   L00166:         except Exception:
   L00167:             pass
>> L00168:             if hfx and fmt:
   L00169:             user32.SetClipboardData(fmt, hfx)
   L00170: 
   L00171:         return True, "OK"
   L00172:     finally:
   L00173:         user32.CloseClipboard()
   L00174: 
   L00175: def _r2497_copy_file_for_paste(p, hwnd=None):
   L00176:     """
   L00177:     Copies a single file path 'p' into clipboard as file copy (Explorer paste).
   L00178:     """
   L00179:     try:
   L00180:         if not p:
   L00181:             return False, "Kein Pfad."
   L00182:         ap = os.path.abspath(p)
   L00183:         if not os.path.isfile(ap):
   L00184:             return False, f"Keine Datei: {ap}"
   L00185:         ok, diag = _r2497_set_clipboard_file_drop_windows([ap], hwnd=hwnd)
   L00186:         if ok:
   L00187:             return True, "OK"
   L00188:         return False, diag
   L00189:         return (ok, "OK" if ok else "Clipboard nicht verfügbar")
   L00190:     except Exception as e:
   L00191:         return False, repr(e)
   L00192: # --- R2497_HELPERS_END ---
   L00193: 
   L00194: try:
   L00195:     from modules import ui_theme_classic
   L00196: except Exception:
   L00197:     ui_theme_classic = None
   L00198: 
   L00199: 
   L00200: def _root_dir() -> Path:
   L00201:     return Path(__file__).resolve().parent.parent
   L00202: 
   L00203: 
   L00204: def _safe_open_file(path: str) -> None:
   L00205:     try:
   L00206:         if path and os.path.isfile(path):
   L00207:             os.startfile(path)
   L00208:     except Exception:
   L00209:         pass
   L00210: 
   L00211: 
   L00212: def _safe_open_folder(path: str) -> None:
   L00213:     try:
   L00214:         if not path:
   L00215:             return
   L00216:         p = path
   L00217:         if os.path.isfile(p):
   L00218:             p = os.path.dirname(p)
   L00219:         if p and os.path.isdir(p):
   L00220:             subprocess.Popen(["explorer", p])
   L00221:     except Exception:
   L00222:         pass
   L00223: 
   L00224: 
   L00225: # --- R2304 INTERNAL VIEWER -----------------------------------------------------------
   L00226: _R2304_MAX_VIEW_BYTES = 1024 * 1024  # 1 MB
   L00227: _R2304_TEXT_EXT = {".txt", ".md", ".py", ".json", ".log", ".ini", ".cfg", ".yaml", ".yml", ".csv", ".bat", ".cmd", ".ps1"}
   L00228: 
```

## Suspicious lines (pass + if on same line)
- none found
