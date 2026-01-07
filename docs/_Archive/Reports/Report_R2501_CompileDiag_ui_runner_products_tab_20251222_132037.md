# R2501 – Compile Diag ui_runner_products_tab.py (READ-ONLY)

- Time: 20251222_132037
- Target: `C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py`

## Compile
- py_compile: FAIL
- Error: `  File "C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_runner_products_tab.py", line 167
    pass        if hfx and fmt:
                ^^
SyntaxError: invalid syntax
`

## CF_UNICODETEXT block hits
```text
L00150:         CF_UNICODETEXT = 13
L00163:                     user32.SetClipboardData(CF_UNICODETEXT, htxt)
```

## Context around line 167
```text
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
>> L00167:             pass        if hfx and fmt:
   L00168:             user32.SetClipboardData(fmt, hfx)
   L00169: 
   L00170:         return True, "OK"
   L00171:     finally:
   L00172:         user32.CloseClipboard()
   L00173: 
   L00174: def _r2497_copy_file_for_paste(p, hwnd=None):
   L00175:     """
   L00176:     Copies a single file path 'p' into clipboard as file copy (Explorer paste).
   L00177:     """
   L00178:     try:
   L00179:         if not p:
   L00180:             return False, "Kein Pfad."
   L00181:         ap = os.path.abspath(p)
   L00182:         if not os.path.isfile(ap):
   L00183:             return False, f"Keine Datei: {ap}"
   L00184:         ok, diag = _r2497_set_clipboard_file_drop_windows([ap], hwnd=hwnd)
   L00185:         if ok:
   L00186:             return True, "OK"
   L00187:         return False, diag
   L00188:         return (ok, "OK" if ok else "Clipboard nicht verfügbar")
   L00189:     except Exception as e:
   L00190:         return False, repr(e)
   L00191: # --- R2497_HELPERS_END ---
   L00192: 
   L00193: try:
   L00194:     from modules import ui_theme_classic
   L00195: except Exception:
   L00196:     ui_theme_classic = None
   L00197: 
   L00198: 
   L00199: def _root_dir() -> Path:
   L00200:     return Path(__file__).resolve().parent.parent
   L00201: 
   L00202: 
   L00203: def _safe_open_file(path: str) -> None:
   L00204:     try:
   L00205:         if path and os.path.isfile(path):
   L00206:             os.startfile(path)
   L00207:     except Exception:
```
