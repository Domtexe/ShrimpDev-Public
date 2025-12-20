# INI Write Map – ShrimpDev
- Runner: R2371
- Zeit: 2025-12-18 19:55:08

## Ziel-INI
- Datei: `ShrimpDev.ini`
- Exists: True
- mtime: 2025-12-18 19:06:19
- size: 870 bytes

## Gefundene potenzielle Schreibstellen (READ-ONLY Scan)

### `D:\ShrimpDev\_Exports\LearningEngine_PhaseC_R1800_20251127_215504\modules\config_loader.py`
- Zeile 1: **uses configparser (inspect for write/save)**
  ```
  import configparser
  ```
- Zeile 7: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 14: **possible write() call**
  ```
  cfg.write(f)
  ```

### `D:\ShrimpDev\_Exports\LearningEngine_PhaseC_R1800_20251127_215504\modules\config_mgr.py`
- Zeile 3: **uses configparser (inspect for write/save)**
  ```
  import os, threading, configparser
  ```
- Zeile 35: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 39: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 46: **uses configparser (inspect for write/save)**
  ```
  self.cfg = configparser.ConfigParser()
  ```
- Zeile 57: **possible write() call**
  ```
  self.cfg.write(f)
  ```
- Zeile 78: **possible save() call**
  ```
  self.save()
  ```
- Zeile 101: **possible save() call**
  ```
  self.save()
  ```
- Zeile 111: **possible save() call**
  ```
  self.save()
  ```
- Zeile 118: **possible save() call**
  ```
  self.save()
  ```

### `D:\ShrimpDev\_Exports\LearningEngine_PhaseC_R1800_20251127_215504\modules\logic_actions.py`
- Zeile 29: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 342: **possible write() call**
  ```
  f.write(txt)
  ```
- Zeile 1905: **possible write() call**
  ```
  f.write(state.content)
  ```

### `D:\ShrimpDev\_OldStuff\Legacy_Runners\tools\R1626.py`
- Zeile 31: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 46: **possible write() call**
  ```
  dst.write(src.read())
  ```
- Zeile 56: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 65: **possible write() call**
  ```
  buf.write(f"Syntaxfehler in {path}: {exc}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Legacy_Runners\tools\R1630.py`
- Zeile 31: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 47: **possible write() call**
  ```
  dst.write(src.read())
  ```
- Zeile 58: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 67: **possible write() call**
  ```
  buf.write(f"Syntaxfehler in {path}: {exc}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Legacy_Runners\tools\R1632.py`
- Zeile 31: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 47: **possible write() call**
  ```
  dst.write(src.read())
  ```
- Zeile 58: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 67: **possible write() call**
  ```
  buf.write(f"Syntaxfehler in {path}: {exc}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Legacy_Runners\tools\R1670.py`
- Zeile 49: **possible write() call**
  ```
  f.write(line + os.linesep)
  ```

### `D:\ShrimpDev\_OldStuff\Legacy_Runners\tools\R1839.py`
- Zeile 38: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 112: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 463: **possible write() call**
  ```
  f.write("\n\n")
  ```
- Zeile 464: **possible write() call**
  ```
  f.write(patch)
  ```

### `D:\ShrimpDev\_OldStuff\Legacy_Runners\tools\Runner_1154e_IntakeSyntaxHeal.py`
- Zeile 49: **possible write() call**
  ```
  with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 186: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src1)
  ```
- Zeile 198: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src1)
  ```
- Zeile 202: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(patched2)
  ```

### `D:\ShrimpDev\_OldStuff\Legacy_Runners\tools\Runner_1171a_IntakeUXAndDetect.py`
- Zeile 280: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 289: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 332: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 338: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\_OldStuff\Legacy_Runners\tools\Runner_1182_DevIntakePro.py`
- Zeile 39: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{pfx}] {msg}\\n")
  ```
- Zeile 272: **possible write() call**
  ```
  z.write(p, p.relative_to(root))
  ```
- Zeile 310: **possible write() call**
  ```
  f.write(f"[R1182] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Legacy_Runners\tools\Runner_1211_FixIntakeCoreStable.py`
- Zeile 28: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\Runner_999_IntakeINI.py`
- Zeile 21: **possible write() call**
  ```
  f.write(f"[R999] {ts} {msg}\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 89: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {msg}\n")
  ```
- Zeile 131: **uses configparser (inspect for write/save)**
  ```
  import os, configparser, threading
  ```
- Zeile 154: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 158: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 164: **uses configparser (inspect for write/save)**
  ```
  self.cfg = configparser.ConfigParser()
  ```
- Zeile 174: **possible write() call**
  ```
  self.cfg.write(f)
  ```
- Zeile 195: **possible save() call**
  ```
  self.save()
  ```
- Zeile 215: **possible save() call**
  ```
  self.save()
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1000_IntakeActions.py`
- Zeile 18: **possible write() call**
  ```
  f.write(f"[R1000] {ts} {msg}\n")
  ```
- Zeile 29: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 63: **possible write() call**
  ```
  f.write(CHANGELOG_APPEND)
  ```
- Zeile 84: **possible save() call**
  ```
  self.save()
  ```
- Zeile 91: **possible save() call**
  ```
  self.save()
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1001_AlwaysOnTopFixImports.py`
- Zeile 134: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 143: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 216: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 222: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1002_SnippetsRestore.py`
- Zeile 17: **possible write() call**
  ```
  f.write(f"[R1002] {ts} {msg}\n")
  ```
- Zeile 28: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {msg}\n")
  ```
- Zeile 79: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {msg}\n")
  ```
- Zeile 107: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1003_FixIndentFallbackLogger.py`
- Zeile 18: **possible write() call**
  ```
  f.write(f"[R1003] {ts} {msg}\n")
  ```
- Zeile 29: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 49: **possible write() call**
  ```
  "                f.write(f'[{prefix}] {ts} {msg}\\n')\n"
  ```
- Zeile 85: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1004_ShrimpDev_PathFix.py`
- Zeile 20: **possible write() call**
  ```
  f.write(f"[R1004] {ts} {msg}\n")
  ```
- Zeile 31: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {msg}\n")
  ```
- Zeile 85: **possible write() call**
  ```
  "                f.write(f'[{prefix}] {ts} {msg}\\n')\n"
  ```
- Zeile 141: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1005_MainGUI_Rewrite.py`
- Zeile 17: **possible write() call**
  ```
  f.write(f"[R1005] {ts} {msg}\n")
  ```
- Zeile 28: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {msg}\n")
  ```
- Zeile 137: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1006_ConfigMgr_Restore.py`
- Zeile 21: **possible write() call**
  ```
  f.write(f"[R1006] {ts} {msg}\n")
  ```
- Zeile 32: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 36: **uses configparser (inspect for write/save)**
  ```
  import os, threading, configparser
  ```
- Zeile 66: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 70: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 77: **uses configparser (inspect for write/save)**
  ```
  self.cfg = configparser.ConfigParser()
  ```
- Zeile 88: **possible write() call**
  ```
  self.cfg.write(f)
  ```
- Zeile 109: **possible save() call**
  ```
  self.save()
  ```
- Zeile 132: **possible save() call**
  ```
  self.save()
  ```
- Zeile 142: **possible save() call**
  ```
  self.save()
  ```
- Zeile 149: **possible save() call**
  ```
  self.save()
  ```
- Zeile 161: **possible write() call**
  ```
  f.write("")
  ```
- Zeile 170: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1007_UIFrames_Restore.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[R1007] {ts} {msg}\n")
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 83: **possible write() call**
  ```
  f.write("")
  ```
- Zeile 157: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1008_IntakeUX_Revamp.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[R1008] {ts} {msg}\n")
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 73: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 277: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1010_IntakeUX_Refine.py`
- Zeile 18: **possible write() call**
  ```
  f.write(f"[R1010] {ts} {msg}\n")
  ```
- Zeile 29: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 46: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 259: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 351: **possible write() call**
  ```
  f.write(f"[{p}] {ts} {m}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1011_IntakeUX_ActionsBar.py`
- Zeile 26: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 151: **possible write() call**
  ```
  f.write(new)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1012_FixMenuIndent.py`
- Zeile 17: **possible write() call**
  ```
  f.write(f"[R1012] {ts} {msg}\n")
  ```
- Zeile 60: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 67: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.3\n")
  ```
- Zeile 69: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1013_SafeBoot_Debug.py`
- Zeile 20: **possible write() call**
  ```
  f.write(f"[R1013] {ts} {msg}\n")
  ```
- Zeile 201: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 205: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.4\n")
  ```
- Zeile 207: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1014_SafeBoot_StringFix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(f"[R1014] {ts} {msg}\n")
  ```
- Zeile 48: **possible write() call**
  ```
  f.write(src_fixed)
  ```
- Zeile 54: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.5\n")
  ```
- Zeile 56: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1015_SafeBoot_StringHardFix.py`
- Zeile 37: **possible write() call**
  ```
  f.write(f"[{p}] {ts} {m}\n")
  ```
- Zeile 183: **possible write() call**
  ```
  f.write(f"[R1015] {ts} {msg}\n")
  ```
- Zeile 194: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 201: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1016_IntakeFix_ContextActions.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[R1016] {ts} {msg}\n")
  ```
- Zeile 28: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 103: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.7\n")
  ```
- Zeile 105: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1017_IntakeUX_CopyPasteName.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[R1017] {ts} {msg}\n")
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 256: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 349: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 358: **possible write() call**
  ```
  f.write("[R1017] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1018_ExtOverride_AndQA.py`
- Zeile 21: **possible write() call**
  ```
  f.write(f"[R1018] {ts} {msg}\n")
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 172: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.9\n")
  ```
- Zeile 174: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1019_ExtOverride_DetectFix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(f"[R1019] {ts} {msg}\n")
  ```
- Zeile 27: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 111: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.10\n")
  ```
- Zeile 113: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1020_SafeBoot_Logfix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(f"[R1020] {ts} {msg}\n")
  ```
- Zeile 26: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 52: **possible write() call**
  ```
  "                f.write(msg)\n"
  ```
- Zeile 70: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.11\n")
  ```
- Zeile 72: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1021_SafeBoot_FinalFix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(f"[R1021] {ts} {msg}\n")
  ```
- Zeile 26: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 62: **possible write() call**
  ```
  "                f.write(msg)\n"
  ```
- Zeile 79: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.12\n")
  ```
- Zeile 81: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1022_MainGUI_SafeImportsRepair.py`
- Zeile 55: **possible write() call**
  ```
  f.write(f"[R1022] {ts} {msg}\n")
  ```
- Zeile 65: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 96: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.13\n")
  ```
- Zeile 98: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1023_SafeFallbackRepair.py`
- Zeile 52: **possible write() call**
  ```
  f.write(f"[R1023] {ts} {msg}\n")
  ```
- Zeile 60: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 74: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.14\n")
  ```
- Zeile 76: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1024_LoggerAtomicFix.py`
- Zeile 17: **possible write() call**
  ```
  f.write(f"[R1024] {ts} {msg}\n")
  ```
- Zeile 25: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 59: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 71: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.15\n")
  ```
- Zeile 73: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1025_SafeFallbackCapture.py`
- Zeile 58: **possible write() call**
  ```
  f.write(f"[R1025] {ts} {msg}\n")
  ```
- Zeile 68: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 87: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.16\n")
  ```
- Zeile 89: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1026_IntakeIndentFix.py`
- Zeile 16: **possible write() call**
  ```
  f.write(f"[R1026] {ts} {msg}\n")
  ```
- Zeile 24: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 56: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.17\n")
  ```
- Zeile 58: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1027_IntakeSaveRewrite.py`
- Zeile 21: **possible write() call**
  ```
  f.write(f"[R1027] {ts} {msg}\n")
  ```
- Zeile 31: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 47: **possible write() call**
  ```
  "                    f.write(data)\n"
  ```
- Zeile 145: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.18\n")
  ```
- Zeile 147: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1028_IntakeModule_Reset.py`
- Zeile 20: **possible write() call**
  ```
  f.write(f"[R1028] {ts} {msg}\n")
  ```
- Zeile 280: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 394: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 402: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1030_IntakeButtons_Fix.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[R1030] {ts} {msg}\n")
  ```
- Zeile 100: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 122: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.20\n")
  ```
- Zeile 124: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 136: **possible write() call**
  ```
  f.write("[R1030] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1031_ButtonsForceWire_Debug.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[R1031] {ts} {msg}\n")
  ```
- Zeile 172: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 182: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.21\n")
  ```
- Zeile 184: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1032_ButtonsHardBind_Ping.py`
- Zeile 20: **possible write() call**
  ```
  f.write(f"[R1032] {ts} {msg}\n")
  ```
- Zeile 178: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 184: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.22\n")
  ```
- Zeile 186: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 197: **possible write() call**
  ```
  f.write("[R1032] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1033_FixBrokenPanedwindow.py`
- Zeile 21: **possible write() call**
  ```
  f.write(f"[R1033] {ts} {msg}\n")
  ```
- Zeile 31: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 87: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.23\n")
  ```
- Zeile 89: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 101: **possible write() call**
  ```
  f.write("[R1033] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1034_IntakeDetect_SmartFix.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[R1034] {ts} {msg}\n")
  ```
- Zeile 32: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 139: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.24\n")
  ```
- Zeile 141: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 153: **possible write() call**
  ```
  f.write("[R1034] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1035_DetectWire_All.py`
- Zeile 20: **possible write() call**
  ```
  f.write(f"[R1035] {ts} {msg}\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 155: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.25\n")
  ```
- Zeile 157: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 165: **possible write() call**
  ```
  f.write("[R1035] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1036_NameDetect_FromCode.py`
- Zeile 20: **possible write() call**
  ```
  f.write(f"[R1036] {ts} {msg}\n")
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 136: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.26\n")
  ```
- Zeile 138: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 150: **possible write() call**
  ```
  f.write("[R1036] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1037_FixDetectSyntax.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[R1037] {ts} {msg}\n")
  ```
- Zeile 48: **possible write() call**
  ```
  f.write(fixed)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1038_DetectBlock_Rewrite.py`
- Zeile 21: **possible write() call**
  ```
  f.write(f"[R1038] {ts} {msg}\n")
  ```
- Zeile 177: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.27\n")
  ```
- Zeile 179: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 196: **possible write() call**
  ```
  f.write(src3)
  ```
- Zeile 206: **possible write() call**
  ```
  f.write("[R1038] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1039_IndentFix_TryExcept.py`
- Zeile 23: **possible write() call**
  ```
  f.write(f"[R1039] {ts} {msg}\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 93: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.28\n")
  ```
- Zeile 95: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1040_Intake_FullReset.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[R1040] {ts} {msg}\n")
  ```
- Zeile 363: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 481: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 487: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1041_AutoDetect_OnPaste.py`
- Zeile 23: **possible write() call**
  ```
  f.write(f"[R1041] {ts} {msg}\n")
  ```
- Zeile 32: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 118: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.31\n")
  ```
- Zeile 120: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 136: **possible write() call**
  ```
  f.write("[R1041] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1042_AutoDetect_Hardwire_Scan.py`
- Zeile 21: **possible write() call**
  ```
  f.write(f"[R1042] {ts} {msg}\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 164: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.32\n")
  ```
- Zeile 166: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 182: **possible write() call**
  ```
  f.write("[R1042] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1043_NoBell_StripTypeHints.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[R1043] {ts} {msg}\n")
  ```
- Zeile 31: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 66: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.33\n")
  ```
- Zeile 68: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1044_Intake_Reinstall_Clean.py`
- Zeile 23: **possible write() call**
  ```
  f.write(f"[R1044] {ts} {msg}\n")
  ```
- Zeile 402: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 531: **possible write() call**
  ```
  f.write(SRC)
  ```
- Zeile 534: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.34\n")
  ```
- Zeile 536: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1045_NameForceAndDateCols.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[R1045] {ts} {msg}\n")
  ```
- Zeile 31: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 124: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.35\n")
  ```
- Zeile 126: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1046_NameDocstring_Fallback_DateCols.py`
- Zeile 21: **possible write() call**
  ```
  f.write(f"[R1046] {ts} {msg}\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 106: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.36\n")
  ```
- Zeile 108: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1047_Intake_CleanHardReset.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[R1047] {ts} {msg}\n")
  ```
- Zeile 383: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 517: **possible write() call**
  ```
  f.write(SRC)
  ```
- Zeile 519: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.37\n")
  ```
- Zeile 521: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1048_Intake_DeleteAndRecent50.py`
- Zeile 25: **possible write() call**
  ```
  f.write(f"[R1048] {ts} {msg}\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 190: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.38\n")
  ```
- Zeile 192: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1049_Intake_ResizeNameExt.py`
- Zeile 28: **possible write() call**
  ```
  f.write(f"[R1049] {ts} {msg}\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 110: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.39\n")
  ```
- Zeile 112: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1050_ExtDetectStrong.py`
- Zeile 31: **possible write() call**
  ```
  f.write(f"[R1050] {ts} {msg}\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 152: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.40\n")
  ```
- Zeile 154: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1051_ExtDetectStrong_FixSub.py`
- Zeile 86: **possible write() call**
  ```
  f.write(f"[R1051] {ts} {msg}\n")
  ```
- Zeile 99: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 135: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.41\n")
  ```
- Zeile 137: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1052_FixEntExtGrid.py`
- Zeile 20: **possible write() call**
  ```
  f.write(f"[R1052] {ts} {msg}\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 61: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.42\n")
  ```
- Zeile 63: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1053_Intake_ClearOnDelete_RefreshOnPaste.py`
- Zeile 21: **possible write() call**
  ```
  f.write(f"[R1053] {ts} {msg}\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 106: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.43\n")
  ```
- Zeile 108: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1054_Intake_QuoteFix_ClearDelete_PasteReset.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[R1054] {ts} {msg}\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 122: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.44\n")
  ```
- Zeile 124: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1055_FixIndent_OnEditorModified.py`
- Zeile 24: **possible write() call**
  ```
  f.write(f"[R1055] {ts} {msg}\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 87: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.45\n")
  ```
- Zeile 89: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1056_FixIndent_OnEditorModified_Strict.py`
- Zeile 33: **possible write() call**
  ```
  f.write(f"[R1056] {ts} {msg}\n")
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 88: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.46\n")
  ```
- Zeile 90: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1057_IndentAudit_IntakeFrame.py`
- Zeile 36: **possible write() call**
  ```
  f.write(f"[R1057] {ts} {msg}\n")
  ```
- Zeile 59: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 103: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.47\n")
  ```
- Zeile 105: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1058_FixKeyAndModified_Block.py`
- Zeile 37: **possible write() call**
  ```
  f.write(f"[R1058] {ts} {msg}\n")
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 95: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.48\n")
  ```
- Zeile 97: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1059_FixDeleteIndent.py`
- Zeile 48: **possible write() call**
  ```
  f.write(f"[R1059] {ts} {msg}\n")
  ```
- Zeile 61: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 97: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.49\n")
  ```
- Zeile 99: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1060_FixAskYesNo_StringConcat.py`
- Zeile 53: **possible write() call**
  ```
  f.write(f"[R1060] {ts} {msg}\n")
  ```
- Zeile 66: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 103: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.50\n")
  ```
- Zeile 105: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1061_FixAskYesNo_StringEscape.py`
- Zeile 51: **possible write() call**
  ```
  f.write(f"[R1061] {ts} {msg}\n")
  ```
- Zeile 64: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1062_FutureAtTop.py`
- Zeile 23: **possible write() call**
  ```
  f.write(f"[R1062] {ts} {msg}\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 117: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.52\n")
  ```
- Zeile 119: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1064_IntegrateGuard_UI.py`
- Zeile 22: **possible write() call**
  ```
  with open(p, "w", encoding="utf-8", newline="\r\n") as f: f.write(data)
  ```
- Zeile 137: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.54\n")
  ```
- Zeile 139: **possible write() call**
  ```
  f.write("\n## v9.9.54\n- Intake: Guard-Button + Handler integriert (Prüfen & ✅-Markierung)\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1065_IntakeRescueAndRollback.py`
- Zeile 25: **possible write() call**
  ```
  f.write(f"[R1065] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1066_FixGuard_MissingHelpers.py`
- Zeile 40: **possible write() call**
  ```
  f.write(f"[R1063] {ts} {msg}\n")
  ```
- Zeile 173: **possible write() call**
  ```
  with open(p, "w", encoding="utf-8", newline="\r\n") as f: f.write(data)
  ```
- Zeile 191: **possible write() call**
  ```
  with open(fail, "w", encoding="utf-8", newline="\r\n") as f: f.write(src1)
  ```
- Zeile 212: **possible write() call**
  ```
  f.write(GUARD_SRC)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1067_WriteGuard_Safe.py`
- Zeile 39: **possible write() call**
  ```
  f.write(f'[R1063] {ts} {msg}\\n')
  ```
- Zeile 172: **possible write() call**
  ```
  with open(p, 'w', encoding='utf-8', newline='\\r\\n') as f: f.write(data)
  ```
- Zeile 190: **possible write() call**
  ```
  with open(fail, 'w', encoding='utf-8', newline='\\r\\n') as f: f.write(src1)
  ```
- Zeile 211: **possible write() call**
  ```
  f.write(GUARD_SRC)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1068_FixLonelyTry.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[R1068] {ts} {msg}\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1069_FixIntake_GuardToolbar.py`
- Zeile 26: **possible write() call**
  ```
  f.write(f"[R1069] {ts} {msg}\n")
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1070_FixSemicolonLines.py`
- Zeile 20: **possible write() call**
  ```
  f.write(f"[R1070] {ts} {msg}\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1071_AddRunButton_PyExec.py`
- Zeile 28: **possible write() call**
  ```
  f.write(f"[R1071] {ts} {msg}\n")
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1072_InsertRunButton_AnyAnchor.py`
- Zeile 23: **possible write() call**
  ```
  f.write(f"[R1072] {ts} {msg}\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1073_FixToolbarAndRunButton.py`
- Zeile 24: **possible write() call**
  ```
  f.write(f"[R1073] {ts} {msg}\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1074_DeleteButtons_WithRecycleBin.py`
- Zeile 25: **possible write() call**
  ```
  f.write(f"[R1074] {ts} {msg}\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1074b_DeleteButtons_WithRecycleBin_Fix.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[R1074b] {ts} {msg}\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1077_FixIndent_UIBlock.py`
- Zeile 45: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1078_WriteGuard_Clean.py`
- Zeile 84: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1082_Guard_VerboseOK.py`
- Zeile 81: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1084_FixGuard_ArgParse.py`
- Zeile 100: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1089_ApplyNameDetect_GuardRun_Delete.py`
- Zeile 36: **possible write() call**
  ```
  f.write(s.encode("utf-8"))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1095_ClassSafeguard_Intake.py`
- Zeile 15: **possible write() call**
  ```
  f_out.write(f_in.read())
  ```
- Zeile 40: **possible write() call**
  ```
  open(MOD, "w", encoding="utf-8").write(patch)
  ```
- Zeile 62: **possible write() call**
  ```
  open(MOD, "w", encoding="utf-8").write(patched)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1096_Reindent_IntakeMethods.py`
- Zeile 17: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 88: **possible write() call**
  ```
  f.write("".join(lines))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1097_FixIntake_Reindent.py`
- Zeile 25: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1097b_FixIntake_Reindent2.py`
- Zeile 13: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 25: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1097c_FixIntake_ReindentHard.py`
- Zeile 13: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 25: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1097d_Reindent_Intake_Strict.py`
- Zeile 13: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1098_FixIntake_ReindentClassBlocks.py`
- Zeile 22: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 133: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1099_FixIntake_RepairIndentPass2.py`
- Zeile 21: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(text.encode("utf-8"))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1100_Reindent_IntakeFrame_Harden.py`
- Zeile 22: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(text.encode("utf-8"))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1101_FixIntake_ReindentAll.py`
- Zeile 21: **possible write() call**
  ```
  with open(p, "wb") as f: f.write(s.encode("utf-8", "utf-8"))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1101a_FixReplace_RecycleBin.py`
- Zeile 21: **possible write() call**
  ```
  f.write(s.encode("utf-8"))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1103_FixIntake_ReindentAndScope.py`
- Zeile 28: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1104_ReplaceIntake_Clean.py`
- Zeile 372: **possible write() call**
  ```
  f.write(self.txt.get("1.0","end-1c"))
  ```
- Zeile 475: **possible write() call**
  ```
  f.write(NEW_SRC)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1105_FixDeleteSignature_Compile.py`
- Zeile 24: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1106_ShrimpGuard_Integriert.py`
- Zeile 33: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1106b_IntegrateGuard_UI.py`
- Zeile 22: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(txt)
  ```
- Zeile 116: **possible write() call**
  ```
  f"{indent}        tmp.write(self.txt.get('1.0', 'end-1c').encode('utf-8'))\n"
  ```
- Zeile 133: **possible write() call**
  ```
  f"{indent}            f.write(out)\n"
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1106c_IntegrateGuard_UI_FixedFuture.py`
- Zeile 20: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(txt)
  ```
- Zeile 66: **possible write() call**
  ```
  "            tmp.write(self.txt.get('1.0', 'end-1c').encode('utf-8'))\n"
  ```
- Zeile 72: **possible write() call**
  ```
  "                f.write(out)\n"
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1107_AutoRepair_IndentBlocks.py`
- Zeile 26: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 40: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1107b_AutoRepair_IndentBlocks_ReturnFix.py`
- Zeile 19: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 29: **possible write() call**
  ```
  f.write(t)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1108_DisableButtonReleaseBinds.py`
- Zeile 19: **possible write() call**
  ```
  g.write(f.read())
  ```
- Zeile 29: **possible write() call**
  ```
  f.write(t)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1109_EnableTkCallbackTrace.py`
- Zeile 19: **possible write() call**
  ```
  g.write(f.read())
  ```
- Zeile 29: **possible write() call**
  ```
  f.write(t)
  ```
- Zeile 38: **possible write() call**
  ```
  f.write("\n--- Tk-Callback-Exception ---\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1110_FixIntake_ToolbarTryAndHelpers.py`
- Zeile 22: **possible write() call**
  ```
  w.write(r.read())
  ```
- Zeile 32: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1112_DeepRepair_IntakeAndGUI.py`
- Zeile 54: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1113_DeepRepair_FixReturnScope.py`
- Zeile 33: **possible write() call**
  ```
  with open(path, "w", encoding="utf-8", newline="\n") as f: f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1114_DeepSanityAndRepair.py`
- Zeile 42: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1114b_FixUnexpectedIndent_MainGUI.py`
- Zeile 35: **possible write() call**
  ```
  with open(p,"w",encoding="utf-8",newline="\n") as f: f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1115_IntegrateRepairUI.py`
- Zeile 23: **possible write() call**
  ```
  with open(p,"w",encoding="utf-8",newline="\n") as f: f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1116_ReentrantBindGuard.py`
- Zeile 29: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1116a_FixMainGUITabs.py`
- Zeile 23: **possible write() call**
  ```
  with open(p,"w",encoding="utf-8",newline="\n") as f: f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1116b_ReentrantBindGuard_AST.py`
- Zeile 22: **possible write() call**
  ```
  with open(p,"w",encoding="utf-8",newline="\n") as f: f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1116c_DeepFix_IntakeUI.py`
- Zeile 20: **possible write() call**
  ```
  f.write(t)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1116d_FixRecycleBinHelper_Only.py`
- Zeile 15: **possible write() call**
  ```
  f.write(t)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1116e_DeepFix_IntakeUI_Safe.py`
- Zeile 24: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1116f_DumpSyntaxContext.py`
- Zeile 49: **possible write() call**
  ```
  f.write(ctx + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1116g_FixToolbarBlock.py`
- Zeile 22: **possible write() call**
  ```
  f.write(s.encode("utf-8"))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1117.py`
- Zeile 35: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 213: **possible write() call**
  ```
  report.write(f"Datei: {os.path.relpath(path, ROOT)}\nZeit : {datetime.now()}\n\n")
  ```
- Zeile 220: **possible write() call**
  ```
  report.write("[Bindings]\n")
  ```
- Zeile 222: **possible write() call**
  ```
  report.write(f"  Zeile {ln:>5}: bind({seq!r}, {cb})\n")
  ```
- Zeile 224: **possible write() call**
  ```
  report.write("  (keine gefunden)\n")
  ```
- Zeile 225: **possible write() call**
  ```
  report.write("\n[Button-Commands]\n")
  ```
- Zeile 227: **possible write() call**
  ```
  report.write(f"  Zeile {ln:>5}: command={cb}\n")
  ```
- Zeile 229: **possible write() call**
  ```
  report.write("  (keine gefunden)\n")
  ```
- Zeile 232: **possible write() call**
  ```
  report.write("\n[Verdacht: doppelte Callback-Verwendung]\n")
  ```
- Zeile 240: **possible write() call**
  ```
  report.write(f"  ⚠ Callback '{cb}' taucht in command und bind auf (z.B. Zeile {ln}).\n")
  ```
- Zeile 241: **possible write() call**
  ```
  report.write("  -> Empfehlung: bind-Handler auf Button mit lambda e: button.invoke(); return 'break'\n")
  ```
- Zeile 242: **possible write() call**
  ```
  report.write("    oder nur eine Quelle beibehalten (command ODER bind-basiert), um Doppeltrigger zu vermeiden.\n")
  ```
- Zeile 244: **possible write() call**
  ```
  report.write("  (kein offensichtlicher Doppeltrigger gefunden)\n")
  ```
- Zeile 248: **possible write() call**
  ```
  report.write("\n[Methoden & Aufrufe]\n")
  ```
- Zeile 251: **possible write() call**
  ```
  report.write(f"  def {name} (Z {info.lineno}) -> [{calls}]\n")
  ```
- Zeile 254: **possible write() call**
  ```
  report.write("\n[Direkte Rekursion]\n")
  ```
- Zeile 258: **possible write() call**
  ```
  report.write(f"  ⚠ {m.name} ruft sich selbst auf (Z {m.lineno}).\n")
  ```
- Zeile 260: **possible write() call**
  ```
  report.write("  (keine direkte Rekursion)\n")
  ```
- Zeile 263: **possible write() call**
  ```
  report.write("\n[Zirkuläre Verweise]\n")
  ```
- Zeile 282: **possible write() call**
  ```
  report.write("\n".join(sorted(set(cyc_lines))) + "\n")
  ```
- Zeile 284: **possible write() call**
  ```
  report.write("  (keine Zyklen 2/3 erkannt)\n")
  ```
- Zeile 287: **possible write() call**
  ```
  report.write("\n[Toolbar-Kontext ~Z120-180 ±40]\n")
  ```
- Zeile 288: **possible write() call**
  ```
  report.write(textwrap.indent(approx_slice if approx_slice.strip() else "(kein Auszug)", "  "))
  ```
- Zeile 297: **possible write() call**
  ```
  cg.write(f"{name} -> {callee}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1118_SafeTkHandler.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 54: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 72: **possible write() call**
  ```
  "                f.write(text)\n"
  ```
- Zeile 127: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 134: **possible write() call**
  ```
  f.write("Runner_1118_SafeTkHandler - Start\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1118b_GlobalTkPatch.py`
- Zeile 24: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 42: **possible write() call**
  ```
  open(p, "w", encoding="utf-8", newline="\n").write(new)
  ```
- Zeile 59: **possible write() call**
  ```
  "                f.write(txt)\n"
  ```
- Zeile 122: **possible write() call**
  ```
  open(p, "w", encoding="utf-8", newline="\n").write(src)
  ```
- Zeile 128: **possible write() call**
  ```
  open(REPORT, "w", encoding="utf-8", newline="\n").write("Runner_1118b_GlobalTkPatch - Start\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1119_TkGuardTopLevel.py`
- Zeile 26: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 46: **possible write() call**
  ```
  "                f.write(txt)\n"
  ```
- Zeile 110: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 115: **possible write() call**
  ```
  f.write("Runner_1119_TkGuardTopLevel - Start\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1120_FixFutureAndGuard.py`
- Zeile 26: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 49: **possible write() call**
  ```
  "                f.write(txt)\n"
  ```
- Zeile 178: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 183: **possible write() call**
  ```
  f.write("Runner_1120_FixFutureAndGuard - Start\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1121_CentralGuard.py`
- Zeile 30: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 73: **possible write() call**
  ```
  "                    f.write(f\"[{prefix}] {ts} {message}\\n\")\n"
  ```
- Zeile 121: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 127: **possible write() call**
  ```
  f.write("Runner_1121_CentralGuard - Start\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1122_RepairMainGUI_SafeLogging.py`
- Zeile 45: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 99: **possible write() call**
  ```
  "                    f.write(f\"[{prefix}] {ts} {message}\\n\")\n"
  ```
- Zeile 171: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 177: **possible write() call**
  ```
  f.write("Runner_1122_RepairMainGUI_SafeLogging - Start\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1123_EditorGuardPatch.py`
- Zeile 30: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {message}\n")
  ```
- Zeile 183: **possible write() call**
  ```
  f.write("Runner_1123_EditorGuardPatch - Start\n")
  ```
- Zeile 195: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 207: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1124_AllFixes_IntakeStable.py`
- Zeile 31: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 74: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {message}\n")
  ```
- Zeile 83: **possible write() call**
  ```
  f.write(LOGGER_SRC)
  ```
- Zeile 111: **possible write() call**
  ```
  "                    f.write(f\"[{prefix}] {ts} {message}\\n\")\n"
  ```
- Zeile 186: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 194: **possible write() call**
  ```
  f.write(orig)
  ```
- Zeile 211: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {message}\n")
  ```
- Zeile 324: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 332: **possible write() call**
  ```
  f.write(orig)
  ```
- Zeile 339: **possible write() call**
  ```
  f.write("Runner_1124_AllFixes_IntakeStable - Start\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1125_IntakeRescue.py`
- Zeile 70: **possible write() call**
  ```
  f.write(f"[{prefix}] {_ts} {message}\\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1126_IntakeRescue2.py`
- Zeile 27: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 86: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {message}\n")
  ```
- Zeile 192: **possible write() call**
  ```
  f.write("Runner_1126_IntakeRescue2 - Start\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1127_IntakeDetox.py`
- Zeile 33: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {msg}\n")
  ```
- Zeile 79: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {message}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1127_IntakeFix_All.py`
- Zeile 26: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1128_FixToolbarAndBindings.py`
- Zeile 24: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 90: **possible write() call**
  ```
  f.write("Runner_1128_FixToolbarAndBindings - Start\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1129_IntakeLoadGuard.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 42: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {message}\n")
  ```
- Zeile 98: **possible write() call**
  ```
  f.write("Runner_1129_IntakeLoadGuard - Start\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1130_IntakeDiagnose.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(f"IntakeDiagnose {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1131_FixIntakeToolbar.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg.rstrip()+"\n")
  ```
- Zeile 52: **possible write() call**
  ```
  f.write("Runner_1131_FixIntakeToolbar - Start\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1132_FixGuardParent.py`
- Zeile 36: **possible write() call**
  ```
  f.write(text.rstrip() + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1132_FixIntakeActions.py`
- Zeile 23: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 29: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 38: **possible write() call**
  ```
  f_out.write(f_in.read())
  ```
- Zeile 132: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1133_IntakeAutoHeal.py`
- Zeile 30: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 148: **possible write() call**
  ```
  f.write("Runner_1133_IntakeAutoHeal - Start\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1134_IntakePathFix.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1135_ModulesInitAndDiagnose.py`
- Zeile 32: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(f"Runner_1135_ModulesInitAndDiagnose {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1136_FixMissingRepairButton.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 80: **possible write() call**
  ```
  f.write("[CRASH]\n" + traceback.format_exc())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1137_IntakeLoadFix.py`
- Zeile 33: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 190: **possible write() call**
  ```
  def logrep(s: str): buf.write(s + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1137a_IntakeLoadFix.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg.rstrip()+"\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 142: **possible write() call**
  ```
  f.write("[CRASH]\n"+traceback.format_exc())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1138_IntakeLoadFix2.py`
- Zeile 27: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1139_IntakeFrameRepair.py`
- Zeile 54: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1140_IntakeFinalFix.py`
- Zeile 34: **possible write() call**
  ```
  sys.stdout.write(line)
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 46: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 227: **possible write() call**
  ```
  rep.write("OK: Patch angewendet.\n")
  ```
- Zeile 228: **possible write() call**
  ```
  rep.write(f"Backup: {backup}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1141_IntakeDefuse.py`
- Zeile 27: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {message}\\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1142_DefuseSafe.py`
- Zeile 31: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1143_IntakeToolbarGuardFix.py`
- Zeile 22: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 27: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1143b_IntakeToolbarGuardFix_Safe.py`
- Zeile 28: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1144_ReplaceIntakeSafe.py`
- Zeile 419: **possible write() call**
  ```
  f.write(self.txt.get("1.0","end-1c"))
  ```
- Zeile 534: **possible write() call**
  ```
  f.write(FIXED)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1145_IntakeAudit.py`
- Zeile 23: **possible write() call**
  ```
  f.write(line.rstrip() + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1146_FeatureGapAudit.py`
- Zeile 31: **possible write() call**
  ```
  f.write(line.rstrip() + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1148_ImproveDetection.py`
- Zeile 22: **possible write() call**
  ```
  f.write(line.rstrip() + "\n")
  ```
- Zeile 185: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1148b_ForceDetectionFix.py`
- Zeile 23: **possible write() call**
  ```
  with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 85: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(txt)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1149_TablePopulate.py`
- Zeile 24: **possible write() call**
  ```
  with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 193: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_txt)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1150_DetectionFinalFix.py`
- Zeile 24: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 82: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(txt)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1151_AddPackSaveButton.py`
- Zeile 28: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 79: **possible write() call**
  ```
  zf.write(sub, arcname=sub.relative_to(root))
  ```
- Zeile 84: **possible write() call**
  ```
  zf.write(item, arcname=item.relative_to(root))
  ```
- Zeile 99: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(txt)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1152_TableUX_Interactions.py`
- Zeile 29: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 267: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(src2)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1153_SmartDetect_AutoSave.py`
- Zeile 25: **possible write() call**
  ```
  with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 84: **possible write() call**
  ```
  f.write(self.txt.get("1.0","end-1c"))
  ```
- Zeile 268: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1153d_RegexHyphenFix.py`
- Zeile 28: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1153f_SafeDetectRegex.py`
- Zeile 23: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 52: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(txt)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1153g_SafeRegexAllIntake.py`
- Zeile 26: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 55: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(txt)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1153h_FixDetectAndRegex.py`
- Zeile 29: **possible write() call**
  ```
  w.write(r.read())
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 204: **possible write() call**
  ```
  sys.stderr.write(f"[Syntax] {e}\n")
  ```
- Zeile 255: **possible write() call**
  ```
  w.write(r.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1153k_DetectGuard.py`
- Zeile 24: **possible write() call**
  ```
  with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 140: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1154_AddDeleteButtons.py`
- Zeile 25: **possible write() call**
  ```
  with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 237: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1154b_AddDeleteButtons.py`
- Zeile 23: **possible write() call**
  ```
  with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 237: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1154c_AddDeleteButtons.py`
- Zeile 19: **possible write() call**
  ```
  with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 227: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1154d_FixIntakeToolbarAndGuard.py`
- Zeile 52: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 214: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(src3)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1154e_IntakeSyntaxHeal.py`
- Zeile 49: **possible write() call**
  ```
  with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 186: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src1)
  ```
- Zeile 198: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src1)
  ```
- Zeile 202: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(patched2)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1154g_FixIntakeButtonsAndGuard.py`
- Zeile 47: **possible write() call**
  ```
  f.write(line.rstrip()+"\n")
  ```
- Zeile 146: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(src3)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1154h_FixMissingBuildUiDef.py`
- Zeile 21: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 86: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(patched)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1155_IntakeBootDiag.py`
- Zeile 26: **possible write() call**
  ```
  f.write(f"[R1155] {ts} {msg}\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 40: **possible write() call**
  ```
  writeln = lambda s="": out.write(s + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1156_AddInitAndBuildUI.py`
- Zeile 23: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 176: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(src3)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1156c_FixTtkAndInitUI.py`
- Zeile 21: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 192: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(src4)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1156d_TtkGlobalizeLocals.py`
- Zeile 23: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 166: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(src2)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1156e_CombineInitAndTtk.py`
- Zeile 21: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 191: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(src3)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1157_FixDetectPatterns.py`
- Zeile 25: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 160: **possible write() call**
  ```
  f.write(new)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1158_UX_ToolbarLayout.py`
- Zeile 23: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 185: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1158c_UX_ToolbarLayoutFix.py`
- Zeile 22: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 128: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1161_DetectRegex_Hotfix.py`
- Zeile 27: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 102: **possible write() call**
  ```
  f.write(new)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1162_DetectRegexScanner.py`
- Zeile 27: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1163_DetectGuardFix.py`
- Zeile 27: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 89: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1163b_DetectGuardFixSafe.py`
- Zeile 25: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```
- Zeile 63: **possible write() call**
  ```
  with io.open(MOD, "w", encoding="utf-8", newline="\n") as f: f.write(new)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1163d_DetectGuardFixSafePlain.py`
- Zeile 25: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```
- Zeile 82: **possible write() call**
  ```
  with io.open(MOD, "w", encoding="utf-8", newline="\n") as f: f.write(new)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1163e_DetectGuardFix_AST.py`
- Zeile 23: **possible write() call**
  ```
  with io.open(LOGF,"a",encoding="utf-8") as f: f.write(line)
  ```
- Zeile 83: **possible write() call**
  ```
  io.open(MOD,"w",encoding="utf-8",newline="\n").write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1163f_FixPyHeadRegex.py`
- Zeile 40: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1163h2_FixPythonHeadRegex_SafePlain.py`
- Zeile 28: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1163h3_FixPythonHeadRegex_DirectReplace.py`
- Zeile 20: **possible write() call**
  ```
  with open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1163h4_FixPythonHeadRegex_LineSwap.py`
- Zeile 27: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1163h_FixPythonHeadRegex_Safe.py`
- Zeile 20: **possible write() call**
  ```
  f.write(f"[R1163h] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1164_ClearAlsoClearsExt.py`
- Zeile 18: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(f"[R1164] {ts} {msg}\n")
  ```
- Zeile 73: **possible write() call**
  ```
  with io.open(MOD, "w", encoding="utf-8", newline="\n") as f: f.write(new)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1164b_OptionalConfirmOnClear.py`
- Zeile 19: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(f"[R1164b] {ts} {msg}\n")
  ```
- Zeile 105: **possible write() call**
  ```
  with io.open(MOD, "w", encoding="utf-8", newline="\n") as f: f.write(new)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1164c_ClearExt_And_OptionalConfirm.py`
- Zeile 74: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(f"[R1164c] {ts} {msg}\n")
  ```
- Zeile 124: **possible write() call**
  ```
  with io.open(MOD, "w", encoding="utf-8", newline="\n") as f: f.write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1164d_ClearExt_OptionalConfirm_Traversal.py`
- Zeile 83: **possible write() call**
  ```
  with io.open(LOGF,"a",encoding="utf-8") as f: f.write(f"[R1164d] {ts} {msg}\n")
  ```
- Zeile 116: **possible write() call**
  ```
  io.open(MOD,"w",encoding="utf-8",newline="\n").write(new)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1165_IntakeInitFix.py`
- Zeile 27: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1166_IntakeTTK_ScopeFix_and_Rules.py`
- Zeile 73: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1166b_IntakeScopeFix_SafeIndent.py`
- Zeile 73: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1166c_Intake_MinimalScopeFix.py`
- Zeile 42: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1166d_Intake_IndentAndTTKFix.py`
- Zeile 74: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1166e_Intake_FinalFix.py`
- Zeile 77: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1166f_Intake_DeepRepair.py`
- Zeile 48: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1166g_Intake_SafeDedent.py`
- Zeile 42: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1166h_Intake_SafeDedent2.py`
- Zeile 40: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1167a_Intake_SanityCheck.py`
- Zeile 41: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1167b_GUIIntakePresenceCheck.py`
- Zeile 22: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1167c_GUIRenderTrace.py`
- Zeile 23: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1167d_GUIMountRefresher.py`
- Zeile 35: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 45: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 78: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 85: **possible write() call**
  ```
  fw.write(fb.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1167e_RunnerExecSafeImport.py`
- Zeile 32: **possible write() call**
  ```
  f.write((msg or "").rstrip() + "\\n")
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 55: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 86: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 94: **possible write() call**
  ```
  fw.write(fb.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1167f_RunnerExecSafeImport2.py`
- Zeile 27: **possible write() call**
  ```
  f.write((msg or "").rstrip() + "\\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(f"[1167f {ts}] {msg}\n")
  ```
- Zeile 45: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 69: **possible write() call**
  ```
  open(TARGET, "w", encoding="utf-8", newline="").write(new_src)
  ```
- Zeile 74: **possible write() call**
  ```
  open(TARGET, "w", encoding="utf-8").write(open(bak, "r", encoding="utf-8").read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1167g_RunnerExecLogAppendSafe.py`
- Zeile 33: **possible write() call**
  ```
  f.write((msg or "").rstrip() + "\\n")
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 55: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 75: **possible write() call**
  ```
  f.write(APPEND_BLOCK)
  ```
- Zeile 82: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1167h_IntakeErrDump.py`
- Zeile 20: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(err or "[leer]")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1167i_IntakeFix_CallModuleFunc.py`
- Zeile 11: **possible write() call**
  ```
  io.open(p, "w", encoding="utf-8", newline="\n").write(new)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1167j_IniDetectHelperPatch.py`
- Zeile 47: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 57: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 97: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 104: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1170a_IntakeRegression.py`
- Zeile 27: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1170b_IntakeBindRepair.py`
- Zeile 114: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 124: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 166: **possible write() call**
  ```
  open(TARGET, "w", encoding="utf-8", newline="\n").write(src)
  ```
- Zeile 170: **possible write() call**
  ```
  open(TARGET, "w", encoding="utf-8", newline="\n").write(open(bak, "r", encoding="utf-8").read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1170c_IntakeShortcutWire.py`
- Zeile 51: **possible write() call**
  ```
  f.write(f"[1170c {time.strftime('%Y-%m-%d %H:%M:%S')}] {m}\n")
  ```
- Zeile 57: **possible write() call**
  ```
  open(dst,"w",encoding="utf-8",newline="").write(open(path,"r",encoding="utf-8").read())
  ```
- Zeile 87: **possible write() call**
  ```
  open(TARGET,"w",encoding="utf-8",newline="\n").write(src)
  ```
- Zeile 91: **possible write() call**
  ```
  open(TARGET,"w",encoding="utf-8",newline="\n").write(open(bak,"r",encoding="utf-8").read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1170d_UXLayoutPolish.py`
- Zeile 87: **possible write() call**
  ```
  f.write(f"[1170d {time.strftime('%Y-%m-%d %H:%M:%S')}] {m}\n")
  ```
- Zeile 93: **possible write() call**
  ```
  open(dst,"w",encoding="utf-8",newline="").write(open(path,"r",encoding="utf-8").read())
  ```
- Zeile 120: **possible write() call**
  ```
  open(TARGET,"w",encoding="utf-8",newline="\n").write(src)
  ```
- Zeile 124: **possible write() call**
  ```
  open(TARGET,"w",encoding="utf-8",newline="\n").write(open(bak,"r",encoding="utf-8").read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1170e_IntakeLifecycleWire.py`
- Zeile 33: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 42: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 88: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 95: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1171a_IntakeUXAndDetect.py`
- Zeile 280: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 289: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 332: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 338: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1171b_IntakeUXAndDetect.py`
- Zeile 263: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 272: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 315: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 321: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1171c_IntakeDetectClean.py`
- Zeile 173: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 182: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 239: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 246: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1171d_IntakeHelperIndentFix.py`
- Zeile 28: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 37: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 110: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 116: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1171e_IntakeToolbarFix.py`
- Zeile 24: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 33: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 87: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 94: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1171f_IntakeToolbarFix2.py`
- Zeile 27: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 36: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 111: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 118: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1171g_IntakeToolbarReflow.py`
- Zeile 145: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 154: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 198: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 204: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1171h_IntakeHelperIndentSweep.py`
- Zeile 23: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 32: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 103: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 110: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1171j_IntakeToolbarReflowTopLevel.py`
- Zeile 132: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 141: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 252: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 256: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 263: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1171k_IntakeToolbarReflowExternalize.py`
- Zeile 122: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 131: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 156: **possible write() call**
  ```
  f.write("# package for external helpers\n")
  ```
- Zeile 158: **possible write() call**
  ```
  f.write(HELPER_CODE)
  ```
- Zeile 218: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 226: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1171n_IntakeSyntaxRebuilder.py`
- Zeile 19: **possible write() call**
  ```
  with open(LOG, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1171p_IntakeIndentHeal.py`
- Zeile 19: **possible write() call**
  ```
  with io.open(LOG, "a", encoding="utf-8") as f: f.write(line+"\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1171q_IntakeCleanAndExternalize.py`
- Zeile 50: **possible write() call**
  ```
  with LOG.open("a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1171q_IntakeToolbarReflowSafe.py`
- Zeile 19: **possible write() call**
  ```
  with io.open(LOG, "a", encoding="utf-8") as f: f.write(line+"\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(dedent(open(os.path.join(os.path.dirname(__file__), "..", "modules", "snippets", "intake_toolbar_reflow_helper.py"), "r", encoding="utf-8").read()
  ```
- Zeile 70: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1171r_IntakeUILayoutTidy.py`
- Zeile 63: **possible write() call**
  ```
  with io.open(LOG, "a", encoding="utf-8") as f: f.write(line+"\n")
  ```
- Zeile 80: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1172_IntakeTabGuard.py`
- Zeile 25: **possible write() call**
  ```
  with open(LOG, "a", encoding="utf-8") as f: f.write(line)
  ```
- Zeile 89: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1173_IntakeUILayoutFix.py`
- Zeile 29: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 194: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1173b_IntakeUILayoutFix.py`
- Zeile 22: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 160: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1173c_IntakeTTKImportFix.py`
- Zeile 24: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 115: **possible write() call**
  ```
  f.write(new)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1173d_IntakeFallbackReturnFix.py`
- Zeile 25: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 70: **possible write() call**
  ```
  f.write(orig)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1173e_MainGuiTabHelper.py`
- Zeile 17: **possible write() call**
  ```
  def write(p,s): io.open(p, "w", encoding="utf-8").write(s)
  ```
- Zeile 52: **possible write() call**
  ```
  _f.write("\n[IntakeTab] Fehler beim Erzeugen von IntakeFrame:\n")
  ```
- Zeile 53: **possible write() call**
  ```
  _f.write(traceback.format_exc())
  ```
- Zeile 75: **possible write() call**
  ```
  _f.write("\n[IntakeTab] Unbekannter Fehler beim Einhaengen des Tabs:\n")
  ```
- Zeile 76: **possible write() call**
  ```
  _f.write(traceback.format_exc())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1173f_IntakeTabSafeAdd.py`
- Zeile 17: **possible write() call**
  ```
  f.write(f"[1173f] {msg}\n")
  ```
- Zeile 27: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 61: **possible write() call**
  ```
  _f.write("[1173f] " + _msg + "\n")
  ```
- Zeile 70: **possible write() call**
  ```
  _f.write("[1173f] Intake-Load-ERR:\n" + "".join(traceback.format_exception(type(ex), ex, ex.__traceback__)) + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1173h_MainGuiHelpersOrderFix.py`
- Zeile 21: **possible write() call**
  ```
  io.open(path, "w", encoding="utf-8", newline="\n").write(txt)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1173i_MainGuiHeadDedent.py`
- Zeile 16: **possible write() call**
  ```
  def W(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1173k_MainGuiCallRelocate.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[1173k {ts}] {msg}\n")
  ```
- Zeile 29: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1173m_MainGuiIntakeWireFix.py`
- Zeile 36: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(f"[1173m {ts}] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1173p_MainGuiIntakeWireForce.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[1173p {ts}] {msg}\n")
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174a_MainGuiIntakeHelpersFix.py`
- Zeile 66: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 86: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174aa_IntakeTabCleanser.py`
- Zeile 50: **possible write() call**
  ```
  f.write("[1174aa] Intake mount failed: %r\n" % (e,))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174b_MainGuiIntakeHelpersFix.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[1174b {ts}] {msg}\n")
  ```
- Zeile 26: **possible write() call**
  ```
  def write(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)
  ```
- Zeile 58: **possible write() call**
  ```
  f.write("[1174b] IntakeFrame-Fehler:\\n" + "".join(traceback.format_exception(type(ex), ex, ex.__traceback__)) + "\\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174c_MainGuiIntakeHelpersFix.py`
- Zeile 19: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174d_MainGuiIntakeCleanup.py`
- Zeile 18: **possible write() call**
  ```
  f.write(f"[1174d {ts}] {msg}\n")
  ```
- Zeile 28: **possible write() call**
  ```
  def write(path, data): open(path, "w", encoding="utf-8", newline="\n").write(data)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174e_MainGuiIntakeCleanup.py`
- Zeile 20: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  with open(p, "w", encoding="utf-8", newline="\n") as f: f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174f_MainGuiIntakeCleanup.py`
- Zeile 20: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174g_IntakeClassRebind.py`
- Zeile 23: **possible write() call**
  ```
  f.write("[1174g] " + msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174g_IntakePostBuildFix.py`
- Zeile 83: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174g_MainGuiReorderFix.py`
- Zeile 20: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174h_IntakeHardReset.py`
- Zeile 118: **possible write() call**
  ```
  f.write(f"[1174h] {ts} {msg}\n")
  ```
- Zeile 142: **possible write() call**
  ```
  f.write(SAFE_SRC)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174i_IntakeRestoreSmart.py`
- Zeile 27: **possible write() call**
  ```
  f.write(f"[1174i] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174j_IntakeRestoreSmartFix.py`
- Zeile 21: **possible write() call**
  ```
  f.write(f"[1174j] {ts} {msg}\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174k_IntakeFeatureRestore.py`
- Zeile 21: **possible write() call**
  ```
  f.write(f"[1174k {time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174m_IntakeFrameRebuild.py`
- Zeile 21: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174n_IntakeHotFix_UIInit.py`
- Zeile 20: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174p_IntakeCtorFix.py`
- Zeile 16: **possible write() call**
  ```
  f.write(f"[1174p {ts}] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174r_IntakeTabRebind.py`
- Zeile 30: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174s_MainGuiSmoke.py`
- Zeile 11: **possible write() call**
  ```
  f.write(f"[1174s {ts}] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174t_IntakeTabRebindFix.py`
- Zeile 12: **possible write() call**
  ```
  with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174v_IntakeTabHarden.py`
- Zeile 12: **possible write() call**
  ```
  f.write(f"[1174v {ts}] {msg}\n")
  ```
- Zeile 15: **possible write() call**
  ```
  def wr(p,s): io.open(p, "w", encoding="utf-8", newline="").write(s)
  ```
- Zeile 48: **possible write() call**
  ```
  "                _f.write(f\"[1174v {time.strftime('%Y-%m-%d %H:%M:%S')}] Direct mount failed: {e!r}\\n\")\n"
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174w_MainSyntaxSmoke.py`
- Zeile 12: **possible write() call**
  ```
  f.write(f"[1174w {ts}] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174x_IntakeRevive.py`
- Zeile 23: **mentions atomic write**
  ```
  def atomic_write(dst: Path, content: str):
  ```
- Zeile 97: **possible write() call**
  ```
  tmp.write(fixed)
  ```
- Zeile 105: **mentions atomic write**
  ```
  atomic_write(target, fixed)
  ```
- Zeile 133: **possible write() call**
  ```
  f.write("\\n[1174x] Importfehler IntakeFrame: %r\\n" % (e,))
  ```
- Zeile 144: **possible write() call**
  ```
  f.write("\\n[1174x] Aufbaufehler IntakeFrame: %r\\n" % (e,))
  ```
- Zeile 166: **mentions atomic write**
  ```
  atomic_write(main_file, src)
  ```
- Zeile 185: **mentions atomic write**
  ```
  atomic_write(target, fixed)
  ```
- Zeile 204: **possible write() call**
  ```
  f.write("\n[1174x] Runner-Fehler: %r\n" % (e,))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1174z_IntakeTabRestoreSafe.py`
- Zeile 16: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 62: **possible write() call**
  ```
  f.write("[1174z] Intake direct mount failed: %r\n" % (e,))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1175a_MainGuiIntakeHelperFix.py`
- Zeile 62: **possible write() call**
  ```
  f.write("\\n[INTAKE_MOUNT_ERROR]\\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1175b_IntakeApiSoftGuard.py`
- Zeile 38: **possible write() call**
  ```
  f.write("\n[INTAKE_API_WRAPPER_ERROR]\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1175d_MainEntryGuard.py`
- Zeile 18: **possible write() call**
  ```
  f.write("\n[MAIN_START_ERROR]\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1175e_MainIntakeShim.py`
- Zeile 13: **possible write() call**
  ```
  f.write(f"\n[{tag}] {type(e).__name__}: {e}\n")
  ```
- Zeile 82: **possible write() call**
  ```
  b.write(read(MAIN))
  ```
- Zeile 84: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1175g_ModulesPackageFix.py`
- Zeile 13: **possible write() call**
  ```
  f.write("# modules package marker\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1175h_IntakeCleanRestore.py`
- Zeile 11: **mentions atomic write**
  ```
  def _write_atomic(path: Path, data: str) -> None:
  ```
- Zeile 14: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(f"[INTAKE] {msg}\n")
  ```
- Zeile 120: **possible write() call**
  ```
  f.write(self.txt.get("1.0","end-1c"))
  ```
- Zeile 169: **mentions atomic write**
  ```
  _write_atomic(MOD, NEW)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1175m_IntakeResurrect.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 57: **possible write() call**
  ```
  f.write(new)
  ```
- Zeile 92: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1175n_FixPyCallAndCleanMain.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(new)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1175q_IntakeHardRestore.py`
- Zeile 121: **possible write() call**
  ```
  f.write(BASIS_CODE)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1176a_IntakeShimUpgrade.py`
- Zeile 38: **possible write() call**
  ```
  f.write("[IntakeShim %s] Mount-Fehler: %r\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), _e))
  ```
- Zeile 51: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 129: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 140: **possible write() call**
  ```
  f.write(fb.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1176b_FixIntakeMount.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[1176b {time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
  ```
- Zeile 30: **possible write() call**
  ```
  w.write(r.read())
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 111: **possible write() call**
  ```
  w.write(r.read())
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1176c_GatePanelIntegration.py`
- Zeile 23: **possible write() call**
  ```
  f.write(f"[1176c {time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
  ```
- Zeile 31: **possible write() call**
  ```
  w.write(r.read())
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 176: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1176d_FixShimName.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[1176d {time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
  ```
- Zeile 25: **possible write() call**
  ```
  w.write(r.read())
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1176d_IntakeShimHotfix.py`
- Zeile 11: **possible write() call**
  ```
  f.write(f"[1176d {ts}] {msg}\n")
  ```
- Zeile 19: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(f"[GATE { _ts() }] {msg}\n")
  ```
- Zeile 127: **possible write() call**
  ```
  f.write("[INTAKE_SHIM] Import/Build-Fehler:\\n" + buf.getvalue() + "\\n")
  ```
- Zeile 159: **possible write() call**
  ```
  f.write("[MAIN] _safe_add_intake_tab Exception\\n"+buf.getvalue()+"\\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177a_IntakeMountAdapter.py`
- Zeile 53: **possible write() call**
  ```
  f.write(f"[{ts}] {msg}\n")
  ```
- Zeile 145: **possible write() call**
  ```
  f.write(f"[{now_ts()}] {msg}\n")
  ```
- Zeile 155: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 163: **possible write() call**
  ```
  out.write(src.read())
  ```
- Zeile 215: **possible write() call**
  ```
  src += "            f.write(f\"[{ts}] {msg}\\n\")\n"
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177a_IntakeMountAdapter_Hotfix.py`
- Zeile 16: **possible write() call**
  ```
  f.write(f"[{ts}] [1177a-Hotfix] {msg}\n")
  ```
- Zeile 23: **possible write() call**
  ```
  out.write(src.read())
  ```
- Zeile 36: **possible write() call**
  ```
  open(MAIN, "w", encoding="utf-8").write(fixed)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177b_DevIntakeRestore.py`
- Zeile 41: **possible write() call**
  ```
  f.write(f"[{ts}] [DevIntake] {msg}\\n")
  ```
- Zeile 262: **possible write() call**
  ```
  f.write(f"[{_ts()}] [R1177b_Dev] {msg}\n")
  ```
- Zeile 275: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177b_IntakeRestore.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177b] {msg}\n")
  ```
- Zeile 31: **possible write() call**
  ```
  with open(path, "rb") as s, open(bak, "wb") as d: d.write(s.read())
  ```
- Zeile 33: **possible write() call**
  ```
  with open(path, "w", encoding="utf-8") as f: f.write(content)
  ```
- Zeile 60: **possible write() call**
  ```
  f.write(f"[{ts}] [IntakeShim] {msg}\n")
  ```
- Zeile 155: **possible write() call**
  ```
  f.write(f"[{ts}] [Intake] {msg}\n")
  ```
- Zeile 399: **possible write() call**
  ```
  f.write(f"[{ts}] [FileOps] {msg}\n")
  ```
- Zeile 417: **possible write() call**
  ```
  with open(self.path, "w", encoding="utf-8") as f: f.write("[]")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177c_IntakeRecover.py`
- Zeile 35: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177c] {msg}\n")
  ```
- Zeile 103: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177d_DevIntakeButtons.py`
- Zeile 25: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177d] {msg}\n")
  ```
- Zeile 91: **possible write() call**
  ```
  f.write(f"[{ts}] [DevIntake] {_msg}\\n")
  ```
- Zeile 258: **possible write() call**
  ```
  with open(p, "w", encoding="utf-8") as f: f.write(s)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177e_DevToolbarFix.py`
- Zeile 24: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177e] {msg}\n")
  ```
- Zeile 145: **possible write() call**
  ```
  f.write(NEW_SNIPPET)
  ```
- Zeile 168: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177f_DevIntakeVisualFix.py`
- Zeile 24: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177f] {msg}\n")
  ```
- Zeile 127: **possible write() call**
  ```
  f.write(NEW_SNIPPET)
  ```
- Zeile 161: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177g_DevIntakeCoreRebuild.py`
- Zeile 20: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177g] {msg}\n")
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(f"[{ts}] [DevIntake] {msg}\\n")
  ```
- Zeile 287: **possible write() call**
  ```
  f.write(PAYLOAD)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177h_IntakeImportCheck.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177h] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177i_ImportPathFix.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177i] {msg}\n")
  ```
- Zeile 89: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177j_IntakeShimHardFix.py`
- Zeile 23: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177j] {msg}\n")
  ```
- Zeile 58: **possible write() call**
  ```
  f.write(f"[{ts}] {_TAG} {msg}\n")
  ```
- Zeile 140: **possible write() call**
  ```
  f.write(PAYLOAD)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177k_RuntimeImportBridge.py`
- Zeile 23: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177k] {msg}\n")
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(f"[{ts}] {_TAG} {msg}\n")
  ```
- Zeile 157: **possible write() call**
  ```
  f.write(PAYLOAD)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177l_CleanTabMount.py`
- Zeile 23: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177l] {msg}\n")
  ```
- Zeile 183: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177m_FixMainAndGate.py`
- Zeile 20: **possible write() call**
  ```
  f.write(f"[R1177m] {ts} {msg}\n")
  ```
- Zeile 31: **possible write() call**
  ```
  open(dst, "w", encoding="utf-8").write(data)
  ```
- Zeile 123: **possible write() call**
  ```
  open(MAIN, "w", encoding="utf-8").write(src)
  ```
- Zeile 166: **possible write() call**
  ```
  "                f.write('[R1177m] Gate safe mount error: %s\\n' % e)\n"
  ```
- Zeile 175: **possible write() call**
  ```
  open(GATE, "w", encoding="utf-8").write(src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177m_MainGuiFix.py`
- Zeile 24: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177m] {msg}\n")
  ```
- Zeile 126: **possible write() call**
  ```
  with open(TARGET, "w", encoding="utf-8") as f: f.write(src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1177n_GatePanelUpdate.py`
- Zeile 21: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177n] {msg}\n")
  ```
- Zeile 61: **possible write() call**
  ```
  with open(TARGET, "w", encoding="utf-8") as f: f.write(src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1178i_ImportPathFix.py`
- Zeile 9: **possible write() call**
  ```
  f.write("[R1178i] " + msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write("[R1178i] IntakeMountERR: %s\\n" % e)
  ```
- Zeile 56: **possible write() call**
  ```
  f.write(new)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1178j_FixDevIntake.py`
- Zeile 16: **possible write() call**
  ```
  f.write(f"[R1178j] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1178m_FixGatePanelAndLaunch.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[GATE] {strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```
- Zeile 75: **possible write() call**
  ```
  f.write("[R1178m] " + msg + "\n")
  ```
- Zeile 82: **possible write() call**
  ```
  f.write(NEW)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1178o_FixGatePanelAndLaunch.py`
- Zeile 13: **possible write() call**
  ```
  f.write(f"[R1178o] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1180_StartFix.py`
- Zeile 20: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 67: **possible write() call**
  ```
  f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [1180] Safe starters written.\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1181_IntakeDeDuplicate.py`
- Zeile 20: **possible write() call**
  ```
  f.write(f"[R1181] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 83: **possible write() call**
  ```
  f.write("[Shim] Intake mount failed:\\n")
  ```
- Zeile 106: **possible write() call**
  ```
  open(SHIM, "w", encoding="utf-8").write(src)
  ```
- Zeile 148: **possible write() call**
  ```
  open(MAIN, "w", encoding="utf-8").write(src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1181b_MainGuiIndentFix.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[R1181b] {ts} {msg}\n")
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 59: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1181c_MainGuiIndentFix2.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[R1181c] {ts} {msg}\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 105: **possible write() call**
  ```
  f.write(fixed)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1181d_MainGuiTryFix.py`
- Zeile 35: **possible write() call**
  ```
  f.write(f"[R1181d] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 71: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1182_DevIntakePro.py`
- Zeile 39: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{pfx}] {msg}\\n")
  ```
- Zeile 272: **possible write() call**
  ```
  z.write(p, p.relative_to(root))
  ```
- Zeile 310: **possible write() call**
  ```
  f.write(f"[R1182] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1182a_DevIntakePro_Clean.py`
- Zeile 35: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{pfx}] {msg}\n")
  ```
- Zeile 255: **possible write() call**
  ```
  z.write(p, p.relative_to(root))
  ```
- Zeile 289: **possible write() call**
  ```
  f.write(f"[R1182a] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1183_DevIntakeUX.py`
- Zeile 25: **uses configparser (inspect for write/save)**
  ```
  import os, sys, time, shutil, zipfile, traceback, subprocess, configparser
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{tag}] {msg}\n")
  ```
- Zeile 89: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 101: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 108: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 406: **possible write() call**
  ```
  z.write(p, p.relative_to(root))
  ```
- Zeile 443: **possible write() call**
  ```
  f.write(f"[R1183] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1183c_DevIntakeUX_DetectFix.py`
- Zeile 27: **uses configparser (inspect for write/save)**
  ```
  import os, sys, time, shutil, zipfile, traceback, subprocess, configparser, re
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{tag}] {msg}\n")
  ```
- Zeile 100: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 112: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 119: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 384: **possible write() call**
  ```
  if p.is_file(): z.write(p, p.relative_to(root))
  ```
- Zeile 418: **possible write() call**
  ```
  f.write(f"[R1183c] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1184_DevIntakeUX_Polish.py`
- Zeile 20: **possible write() call**
  ```
  f.write(f"[R1184] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```
- Zeile 24: **uses configparser (inspect for write/save)**
  ```
  import os, sys, time, shutil, zipfile, traceback, subprocess, configparser, re
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{tag}] {msg}\n")
  ```
- Zeile 101: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser(); p = Path(os.getcwd())/INI_FILE
  ```
- Zeile 108: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 116: **possible write() call**
  ```
  with open(Path(os.getcwd())/INI_FILE, "w", encoding="utf-8", newline="\n") as f: cfg.write(f)
  ```
- Zeile 386: **possible write() call**
  ```
  if p.is_file(): z.write(p, p.relative_to(root))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1185_DevIntakeLEDs_Detect2.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[R1185] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```
- Zeile 23: **uses configparser (inspect for write/save)**
  ```
  import os, sys, time, shutil, zipfile, traceback, subprocess, configparser, re
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{tag}] {msg}\n")
  ```
- Zeile 161: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser(); p = Path(os.getcwd())/INI_FILE
  ```
- Zeile 168: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 176: **possible write() call**
  ```
  with open(Path(os.getcwd())/INI_FILE, "w", encoding="utf-8", newline="\n") as f: cfg.write(f)
  ```
- Zeile 481: **possible write() call**
  ```
  if p.is_file(): z.write(p, p.relative_to(root))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1185b_DevIntakeLEDs_Detect2Fix.py`
- Zeile 16: **possible write() call**
  ```
  f.write(f"[R1185b] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1186_IntakeUX_FixDetectAndUX.py`
- Zeile 13: **possible write() call**
  ```
  f.write(f"[R1186] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1187_IntakeLEDs_Add.py`
- Zeile 14: **possible write() call**
  ```
  f.write(f"[R1187] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1188_IntakeLEDs_DetectHardening.py`
- Zeile 108: **possible write() call**
  ```
  f.write(out)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1189_IntakeRepairAndLEDsFix.py`
- Zeile 14: **possible write() call**
  ```
  f.write(f"[R1189] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1190_DevIntake_Install.py`
- Zeile 16: **possible write() call**
  ```
  f.write(f"[R1190] {time.strftime('%Y-%m-%d %H:%M:%S')} {tag} {msg}\n")
  ```
- Zeile 36: **uses configparser (inspect for write/save)**
  ```
  import os, sys, time, zipfile, traceback, configparser, subprocess, re
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{tag}] {msg}\n")
  ```
- Zeile 157: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser(); p = Path(os.getcwd())/INI_FILE
  ```
- Zeile 168: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 177: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 548: **possible write() call**
  ```
  z.write(p, p.relative_to(root))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1191_DevIntake_CleanInstall.py`
- Zeile 9: **uses configparser (inspect for write/save)**
  ```
  import os, sys, time, zipfile, traceback, configparser, subprocess, re
  ```
- Zeile 20: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{tag}] {msg}\n")
  ```
- Zeile 112: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser(); p = Path(os.getcwd())/INI_FILE
  ```
- Zeile 121: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 130: **possible write() call**
  ```
  cfg.write(f)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1192_DevIntake_UIRefine.py`
- Zeile 8: **uses configparser (inspect for write/save)**
  ```
  import sys, time, traceback, configparser, subprocess, re, zipfile
  ```
- Zeile 21: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{tag}] {msg}\n")
  ```
- Zeile 118: **uses configparser (inspect for write/save)**
  ```
  c=configparser.ConfigParser(); c.read(p, encoding="utf-8")
  ```
- Zeile 125: **uses configparser (inspect for write/save)**
  ```
  c=configparser.ConfigParser()
  ```
- Zeile 136: **possible write() call**
  ```
  with (Path.cwd()/INI).open("w",encoding="utf-8",newline="\n") as f: c.write(f)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1193_DevIntake_FixDetectAndInstall.py`
- Zeile 22: **uses configparser (inspect for write/save)**
  ```
  import time, re, configparser, traceback
  ```
- Zeile 31: **possible write() call**
  ```
  f.write(f"[DevIntake] {ts} [{tag}] {msg}\n")
  ```
- Zeile 102: **uses configparser (inspect for write/save)**
  ```
  c=configparser.ConfigParser(); c.read(p, encoding="utf-8")
  ```
- Zeile 108: **uses configparser (inspect for write/save)**
  ```
  c=configparser.ConfigParser()
  ```
- Zeile 118: **possible write() call**
  ```
  c.write(f)
  ```
- Zeile 369: **possible write() call**
  ```
  if p.is_file(): zp.write(p, p.relative_to(tgt))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1194_DevIntake_UIArrange.py`
- Zeile 29: **possible write() call**
  ```
  f.write(f"[DevIntake] {ts} [{tag}] {msg}\n")
  ```
- Zeile 308: **possible write() call**
  ```
  if p.is_file(): zp.write(p, p.relative_to(tgt))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1195_DevIntake_UISortPolish.py`
- Zeile 30: **possible write() call**
  ```
  f.write(f"[DevIntake] {ts} [{tag}] {msg}\n")
  ```
- Zeile 346: **possible write() call**
  ```
  if p.is_file(): zp.write(p, p.relative_to(tgt))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1196_DevIntake_Apply.py`
- Zeile 42: **possible write() call**
  ```
  f.write(f"[DevIntake] {ts} [{tag}] {msg}\n")
  ```
- Zeile 368: **possible write() call**
  ```
  if p.is_file(): zp.write(p, p.relative_to(tgt))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1198_IntakeLedFix.py`
- Zeile 21: **possible write() call**
  ```
  f.write(f"[R1198] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1199_FixSaveAndLEDs.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[R1199] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1199_IntakeHotfix.py`
- Zeile 23: **possible write() call**
  ```
  f.write(f"[R1199] {ts} {msg}\n")
  ```
- Zeile 198: **possible write() call**
  ```
  f.write(f"[R1199] {ts} ERROR {e}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1201_DevIntake_Stabilize.py`
- Zeile 27: **possible write() call**
  ```
  f.write(f"{TAG} {ts} {line}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1202_FixIndentationPath.py`
- Zeile 18: **possible write() call**
  ```
  f.write(f"[R1202] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1203_DevIntake_Recovery.py`
- Zeile 27: **possible write() call**
  ```
  f.write(s+"\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1205_FixIntakeIndentAndLEDs.py`
- Zeile 23: **possible write() call**
  ```
  fp.write(f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} {TAG} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1206_FixIntakeCore.py`
- Zeile 23: **possible write() call**
  ```
  f.write(f"[R1206] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1208_FixRegexEscape.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[R1208] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1209_IntakePathFinalFix.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[R1209] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1211_FixIntakeCoreStable.py`
- Zeile 28: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1215_FixIntakeCoreFinal.py`
- Zeile 24: **possible write() call**
  ```
  f.write(f"[R1215] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1216_FixIntakeCore_Final.py`
- Zeile 24: **possible write() call**
  ```
  f.write(f"[R1216] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1218_FixIntakeCoreSuperSafe.py`
- Zeile 22: **possible write() call**
  ```
  f.write(f"[R1218] {ts} {msg}\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(txt)
  ```
- Zeile 54: **possible write() call**
  ```
  f.write(f"[DevIntake] {ts} [{tag}] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1218_FixIntake_NewlineSafe.py`
- Zeile 14: **possible write() call**
  ```
  LOG.open("a", encoding="utf-8", newline="\n").write(f"[R1218] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1220_SyntaxGate_AllModules.py`
- Zeile 11: **possible write() call**
  ```
  LOG.open("a", encoding="utf-8", newline="\n").write(f"[R1220] {line}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1221_IntakeCore_Addons.py`
- Zeile 25: **possible write() call**
  ```
  f.write(f"[INTAKE] [{tag}] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```
- Zeile 142: **possible write() call**
  ```
  LOG.open("a", encoding="utf-8", newline="\n").write(f"[R1221] {msg}\n")
  ```
- Zeile 175: **possible write() call**
  ```
  from pathlib import Path; Path(__file__).resolve().parents[1].joinpath("debug_output.txt").open("a", encoding="utf-8", newline="\\n").write(f"[R1221] APPLY_ERROR: {_e!r}\\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1225_IntakeCore_RepairAndIntegrate.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[R1225] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1230_RestoreIntakeFromBackup.py`
- Zeile 13: **possible write() call**
  ```
  LOG.open("a", encoding="utf-8", newline="\n").write(f"[R1230] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1231_Intake_MinimalFixes.py`
- Zeile 13: **possible write() call**
  ```
  LOG.open("a", encoding="utf-8", newline="\n").write(f"[R1231] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1234_IntakeCore_RepairIntegrate.py`
- Zeile 24: **possible write() call**
  ```
  f.write(f"[R1234] {ts} {msg}\n")
  ```
- Zeile 172: **possible write() call**
  ```
  (Path(__file__).resolve().parents[1]/"debug_output.txt").open("a", encoding="utf-8").write(
  ```
- Zeile 199: **possible write() call**
  ```
  (Path(__file__).resolve().parents[1]/"debug_output.txt").open("a", encoding="utf-8").write(msg+"\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_1242_Intake_RepairAndIntegrate.py`
- Zeile 24: **possible write() call**
  ```
  f.write(f"[R1242] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_900_Setup.py`
- Zeile 50: **possible write() call**
  ```
  (ROOT/"debug_output.txt").open("a", encoding="utf-8", errors="ignore").write(f"[CONFIG] {msg}\n")
  ```
- Zeile 89: **possible write() call**
  ```
  try: (ROOT/"debug_output.txt").open("a", encoding="utf-8", errors="ignore").write(f"[AGENT] {s}\n")
  ```
- Zeile 107: **possible write() call**
  ```
  try: EVENTS.open("a", encoding="utf-8").write(json.dumps(ev, ensure_ascii=False) + "\n")
  ```
- Zeile 190: **possible write() call**
  ```
  try: (ROOT/"debug_output.txt").open("a", encoding="utf-8", errors="ignore").write(f"[AGENT_UI] {s}\n")
  ```
- Zeile 265: **possible write() call**
  ```
  (INBOX / f"{int(time.time())}_{os.getpid()}.jsonl").open("a", encoding="utf-8").write(json.dumps(ev, ensure_ascii=False)+"\n")
  ```
- Zeile 283: **possible write() call**
  ```
  try: (ROOT/"debug_output.txt").open("a", encoding="utf-8", errors="ignore").write(f"[INTAKE] {s}\n")
  ```
- Zeile 424: **possible write() call**
  ```
  try: (ROOT/"debug_output.txt").open("a", encoding="utf-8", errors="ignore").write(f"[MAIN] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_903_Fix.py`
- Zeile 54: **possible write() call**
  ```
  (ROOT/"debug_output.txt").open("a", encoding="utf-8", errors="ignore").write(f"[MAIN] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_910_Install.py`
- Zeile 28: **possible write() call**
  ```
  try: Path(r"D:\ShrimpDev\debug_output.txt").open("a", encoding="utf-8").write(f"[SCAN] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_913_Silence.py`
- Zeile 20: **possible write() call**
  ```
  (inbox/f"{int(time.time())}.jsonl").open("a", encoding="utf-8").write(
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_930_AllInOne.py`
- Zeile 234: **possible write() call**
  ```
  if p.exists(): zipf.write(p, arcname=arc)
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_935_FixMainGUI.py`
- Zeile 109: **possible write() call**
  ```
  (ROOT/"debug_output.txt").open("a", encoding="utf-8", errors="ignore").write(f"[MAIN] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_941_Preflight.py`
- Zeile 19: **possible write() call**
  ```
  (inbox/f"{int(time.time())}.jsonl").open("a", encoding="utf-8").write(json.dumps({"runner":"R941", **ev}, ensure_ascii=False)+"\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_943_NewRunner.py`
- Zeile 29: **possible write() call**
  ```
  (inbox/f"{{int(time.time())}}.jsonl").open("a", encoding="utf-8").write(json.dumps({{"runner":"R{RID}", **ev}}, ensure_ascii=False)+"\\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_960_BootFix.py`
- Zeile 26: **possible write() call**
  ```
  "            f.write(line)\n"
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_962_FixMainGUI.py`
- Zeile 87: **possible write() call**
  ```
  .write(f"[MAIN] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_970_AllInOneInstall.py`
- Zeile 13: **possible write() call**
  ```
  try: LOGF.open("a", encoding="utf-8", errors="ignore").write(f"[R970] {msg}\n")
  ```
- Zeile 435: **possible write() call**
  ```
  z.write(p, p.relative_to(ROOT))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_971_UnifyTabs.py`
- Zeile 11: **possible write() call**
  ```
  try: LOG.open("a", encoding="utf-8", errors="ignore").write(f"[R971] {msg}\n")
  ```
- Zeile 433: **possible write() call**
  ```
  z.write(p, p.relative_to(ROOT))
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_972_SafePatch.py`
- Zeile 11: **possible write() call**
  ```
  try: LOGF.open("a", encoding="utf-8", errors="ignore").write(f"[R972] {msg}\n")
  ```
- Zeile 15: **mentions atomic write**
  ```
  def write_text_atomic(target: Path, content: str) -> bool:
  ```
- Zeile 20: **mentions atomic write**
  ```
  os.replace(tmp, target)  # atomic if same volume
  ```
- Zeile 115: **mentions atomic write**
  ```
  # 2) Atomic append (read + write_atomic)
  ```
- Zeile 118: **mentions atomic write**
  ```
  if write_text_atomic(tgt, new):
  ```
- Zeile 121: **mentions atomic write**
  ```
  log(f"FAILED (atomic): {rel} - wird deferred")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_980_DevConsolidate.py`
- Zeile 12: **possible write() call**
  ```
  try: LOGF.open("a", encoding="utf-8", errors="ignore").write(f"[R980] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_981_IntakeUX.py`
- Zeile 10: **possible write() call**
  ```
  try: LOGF.open("a", encoding="utf-8", errors="ignore").write(f"[R981] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_982_IntakeUIEnhance.py`
- Zeile 12: **possible write() call**
  ```
  try: LOGF.open("a", encoding="utf-8", errors="ignore").write(f"[R982] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_983_IntakeFix.py`
- Zeile 10: **possible write() call**
  ```
  try: LOGF.open("a", encoding="utf-8", errors="ignore").write(f"[R983] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_984_IntakeGeometryFix.py`
- Zeile 11: **possible write() call**
  ```
  try: LOG.open("a", encoding="utf-8", errors="ignore").write(f"[R984] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_990_FixGUI.py`
- Zeile 19: **possible write() call**
  ```
  DEBUG.open("a", encoding="utf-8", errors="ignore").write(f"[MAIN] {msg}\n")
  ```

### `D:\ShrimpDev\_OldStuff\Runners_Friedhof\modules\tools\Runner_991_AllTabsIntegrate.py`
- Zeile 13: **possible write() call**
  ```
  try: LOGF.open("a", encoding="utf-8", errors="ignore").write(f"[R991] {msg}\n")
  ```
- Zeile 170: **possible write() call**
  ```
  HIST.open("a", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False)+"\n")
  ```
- Zeile 311: **possible write() call**
  ```
  HIST.open("a", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False)+"\n")
  ```

### `D:\ShrimpDev\_Trash\20251130_183623__R1837jjj.py`
- Zeile 264: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\_Trash\20251205_114531__R1969b.py`
- Zeile 290: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 346: **possible write() call**
  ```
  f.write(patched)
  ```

### `D:\ShrimpDev\_Trash\20251209_223022__Runner_900_Setup.py`
- Zeile 57: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 66: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 81: **possible write() call**
  ```
  (ROOT/"debug_output.txt").open("a", encoding="utf-8", errors="ignore").write(f"[CONFIG] {msg}\n")
  ```
- Zeile 120: **possible write() call**
  ```
  try: (ROOT/"debug_output.txt").open("a", encoding="utf-8", errors="ignore").write(f"[AGENT] {s}\n")
  ```
- Zeile 138: **possible write() call**
  ```
  try: EVENTS.open("a", encoding="utf-8").write(json.dumps(ev, ensure_ascii=False) + "\n")
  ```
- Zeile 221: **possible write() call**
  ```
  try: (ROOT/"debug_output.txt").open("a", encoding="utf-8", errors="ignore").write(f"[AGENT_UI] {s}\n")
  ```
- Zeile 296: **possible write() call**
  ```
  (INBOX / f"{int(time.time())}_{os.getpid()}.jsonl").open("a", encoding="utf-8").write(json.dumps(ev, ensure_ascii=False)+"\n")
  ```
- Zeile 314: **possible write() call**
  ```
  try: (ROOT/"debug_output.txt").open("a", encoding="utf-8", errors="ignore").write(f"[INTAKE] {s}\n")
  ```
- Zeile 455: **possible write() call**
  ```
  try: (ROOT/"debug_output.txt").open("a", encoding="utf-8", errors="ignore").write(f"[MAIN] {msg}\n")
  ```

### `D:\ShrimpDev\_Trash\20251215_160653__patchlib_guard.py`
- Zeile 33: **possible write() call**
  ```
  f.write(ctx.original)
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(ctx.modified)
  ```

### `D:\ShrimpDev\_Trash\20251215_160653__shrimpdev_event.py`
- Zeile 25: **possible write() call**
  ```
  ).write(json.dumps(ev, ensure_ascii=False) + "\n")
  ```

### `D:\ShrimpDev\main_gui.py`
- Zeile 41: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 128: **possible save() call**
  ```
  _cfg_top.save(cfg)
  ```
- Zeile 396: **possible save() call**
  ```
  config_loader.save(cfg)
  ```
- Zeile 682: **uses configparser (inspect for write/save)**
  ```
  import configparser, os
  ```
- Zeile 685: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```

### `D:\ShrimpDev\modules\config_loader.py`
- Zeile 9: **possible save() call**
  ```
  - config_loader.save(cfg)
  ```
- Zeile 19: **uses configparser (inspect for write/save)**
  ```
  import configparser
  ```
- Zeile 26: **uses configparser (inspect for write/save)**
  ```
  class ShrimpDevConfig(configparser.ConfigParser):
  ```
- Zeile 98: **possible write() call**
  ```
  existing.write(f)
  ```
- Zeile 102: **possible write() call**
  ```
  existing.write(f)
  ```

### `D:\ShrimpDev\modules\config_manager.py`
- Zeile 17: **uses configparser (inspect for write/save)**
  ```
  import configparser
  ```
- Zeile 32: **uses configparser (inspect for write/save)**
  ```
  self._config: Optional[configparser.ConfigParser] = None
  ```
- Zeile 53: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 83: **possible save() call**
  ```
  - Dadurch überschreibt config_manager.save() nicht mehr Docking-Persistenz.
  ```
- Zeile 88: **uses configparser (inspect for write/save)**
  ```
  import configparser
  ```
- Zeile 93: **uses configparser (inspect for write/save)**
  ```
  base = configparser.ConfigParser()
  ```
- Zeile 110: **possible write() call**
  ```
  self._config.write(f)
  ```
- Zeile 115: **possible write() call**
  ```
  base.write(f)
  ```
- Zeile 155: **possible save() call**
  ```
  self.save()
  ```

### `D:\ShrimpDev\modules\config_mgr.py`
- Zeile 9: **possible save() call**
  ```
  - config_loader.save(cfg)
  ```
- Zeile 19: **uses configparser (inspect for write/save)**
  ```
  import configparser
  ```
- Zeile 26: **uses configparser (inspect for write/save)**
  ```
  class ShrimpDevConfig(configparser.ConfigParser):
  ```
- Zeile 98: **possible write() call**
  ```
  existing.write(f)
  ```
- Zeile 102: **possible write() call**
  ```
  existing.write(f)
  ```

### `D:\ShrimpDev\modules\exception_logger.py`
- Zeile 23: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 25: **possible write() call**
  ```
  f.write('\n')
  ```
- Zeile 172: **possible write() call**
  ```
  f.write(line + '\n')
  ```

### `D:\ShrimpDev\modules\learning_engine.py`
- Zeile 97: **possible write() call**
  ```
  f.write(line + "\n")
  ```

### `D:\ShrimpDev\modules\learning_engine\persistence.py`
- Zeile 26: **possible save() call**
  ```
  self.save()
  ```

### `D:\ShrimpDev\modules\logic_actions.py`
- Zeile 75: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 767: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 1127: **possible save() call**
  ```
  '''ShrimpDev.ini ueber modules.config_loader.save() speichern.'''
  ```
- Zeile 1133: **possible save() call**
  ```
  _r1851_cfg.save(cfg)
  ```
- Zeile 1387: **possible save() call**
  ```
  """ShrimpDev.ini ueber modules.config_loader.save() speichern."""
  ```
- Zeile 1393: **possible save() call**
  ```
  _r1852_cfg.save(cfg)
  ```
- Zeile 1850: **possible write() call**
  ```
  #             f.write(line)
  ```
- Zeile 2576: **possible write() call**
  ```
  #             f.write(text or "")
  ```

### `D:\ShrimpDev\modules\module_agent.py`
- Zeile 86: **possible write() call**
  ```
  f.write(f"[{_t.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
  ```

### `D:\ShrimpDev\modules\module_docking.py`
- Zeile 7: **uses configparser (inspect for write/save)**
  ```
  import configparser
  ```
- Zeile 71: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 86: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 91: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 636: **uses configparser (inspect for write/save)**
  ```
  import configparser, os
  ```
- Zeile 637: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 650: **uses configparser (inspect for write/save)**
  ```
  import configparser, os
  ```
- Zeile 651: **uses configparser (inspect for write/save)**
  ```
  base = configparser.ConfigParser()
  ```
- Zeile 670: **possible write() call**
  ```
  base.write(f)
  ```
- Zeile 762: **uses configparser (inspect for write/save)**
  ```
  import configparser, os
  ```
- Zeile 763: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 878: **uses configparser (inspect for write/save)**
  ```
  import configparser, os
  ```
- Zeile 879: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 891: **uses configparser (inspect for write/save)**
  ```
  import configparser, os
  ```
- Zeile 892: **uses configparser (inspect for write/save)**
  ```
  base = configparser.ConfigParser()
  ```
- Zeile 911: **possible write() call**
  ```
  base.write(f)
  ```

### `D:\ShrimpDev\modules\module_gate_smoke.py`
- Zeile 14: **possible write() call**
  ```
  f.write(f"[GATE { _ts() }] {msg}\n")
  ```

### `D:\ShrimpDev\modules\module_learningjournal.py`
- Zeile 47: **possible write() call**
  ```
  f.write(line + "\n")
  ```

### `D:\ShrimpDev\modules\module_patch_release.py`
- Zeile 27: **possible write() call**
  ```
  z.write(p, p.relative_to(ROOT))
  ```

### `D:\ShrimpDev\modules\module_runner_exec.py`
- Zeile 32: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 79: **possible write() call**
  ```
  f.write(_bat_template(rel_py, title or f"ShrimpDev - {base}"))
  ```
- Zeile 116: **possible write() call**
  ```
  f.write(res["output"])
  ```
- Zeile 137: **possible write() call**
  ```
  f.write((msg or "").rstrip() + "\n")
  ```
- Zeile 149: **possible write() call**
  ```
  f.write(line.rstrip('\n') + '\n')
  ```

### `D:\ShrimpDev\modules\module_runnerbar.py`
- Zeile 16: **possible write() call**
  ```
  f.write(f"[RunnerBar {ts}] {msg}\n")
  ```

### `D:\ShrimpDev\modules\move_journal.py`
- Zeile 49: **possible write() call**
  ```
  f.write(json.dumps(entry, ensure_ascii=False) + "\n")
  ```

### `D:\ShrimpDev\modules\snippets\agent_client.py`
- Zeile 18: **possible write() call**
  ```
  (INBOX / f"{int(time.time())}_{os.getpid()}.jsonl").open("a", encoding="utf-8").write(json.dumps(ev, ensure_ascii=False)+"\n")
  ```

### `D:\ShrimpDev\modules\snippets\logger_snippet.py`
- Zeile 35: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\modules\snippets\safeio.py`
- Zeile 5: **mentions atomic write**
  ```
  def write_atomic(target: Path, data: str) -> bool:
  ```

### `D:\ShrimpDev\modules\snippets\snippet_file_ops.py`
- Zeile 19: **possible write() call**
  ```
  f.write(f"[{ts}] [FileOps] {msg}\n")
  ```
- Zeile 37: **possible write() call**
  ```
  with open(self.path, "w", encoding="utf-8") as f: f.write("[]")
  ```

### `D:\ShrimpDev\modules\snippets\snippet_log_runner.py`
- Zeile 56: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\modules\tools\patchlib_guard.py`
- Zeile 33: **possible write() call**
  ```
  f.write(ctx.original)
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(ctx.modified)
  ```

### `D:\ShrimpDev\modules\tools\shrimpdev_event.py`
- Zeile 25: **possible write() call**
  ```
  ).write(json.dumps(ev, ensure_ascii=False) + "\n")
  ```

### `D:\ShrimpDev\modules\ui_filters.py`
- Zeile 43: **possible save() call**
  ```
  config_loader.save(cfg)
  ```
- Zeile 57: **possible save() call**
  ```
  config_loader.save(cfg)
  ```

### `D:\ShrimpDev\modules\ui_left_panel.py`
- Zeile 122: **possible save() call**
  ```
  _cfg_r1647b.save(cfg)
  ```

### `D:\ShrimpDev\modules\ui_project_tree.py`
- Zeile 135: **possible save() call**
  ```
  _cfg_tree.save(cfg_ws)
  ```
- Zeile 373: **possible save() call**
  ```
  _cfg_tree.save(cfg)
  ```
- Zeile 568: **possible save() call**
  ```
  _cfg_tree_save2.save(cfg)
  ```

### `D:\ShrimpDev\modules\ui_settings_tab.py`
- Zeile 82: **possible save() call**
  ```
  mgr.save()
  ```

### `D:\ShrimpDev\modules\ui_toolbar.py`
- Zeile 243: **uses configparser (inspect for write/save)**
  ```
  import configparser
  ```
- Zeile 304: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 410: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 418: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 452: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 475: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 483: **possible write() call**
  ```
  cfg.write(f)
  ```

### `D:\ShrimpDev\tools\Archiv\R1252_LearningJournal.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1288_RestoreOriginalIntake.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(f"[R1288] {ts} {msg}\n")
  ```
- Zeile 96: **possible write() call**
  ```
  "            f.write(f\"[Intake] {ts} [{tag}] {msg}\\n\")\n"
  ```

### `D:\ShrimpDev\tools\Archiv\R1300_IntakeV1_Install.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1301_IntakeV1_Install.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1305_IntakeHardFix.py`
- Zeile 10: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  with open(p, "w", encoding="utf-8", newline="\n") as f: f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\R1306_FixIntakeV1.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 42: **possible write() call**
  ```
  w.write(r.read())
  ```
- Zeile 45: **mentions atomic write**
  ```
  def write_atomic(path: str, content: str) -> None:
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 150: **possible write() call**
  ```
  with open(os.path.join(d,name), "w", encoding="utf-8") as f: f.write(txt.get("1.0","end"))
  ```
- Zeile 269: **mentions atomic write**
  ```
  write_atomic(v1_path, INTAKE_V1)
  ```
- Zeile 275: **mentions atomic write**
  ```
  write_atomic(gui_path, patched)
  ```

### `D:\ShrimpDev\tools\Archiv\R1310_IntakeV1_Fix.py`
- Zeile 13: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 40: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 181: **possible write() call**
  ```
  f.write(editor.get("1.0","end"))
  ```

### `D:\ShrimpDev\tools\Archiv\R1311_RestoreTrueIntake.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\tools\Archiv\R1312_FixMainGUI_IntakeMount.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 44: **mentions atomic write**
  ```
  def write_atomic(p, content):
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 133: **mentions atomic write**
  ```
  write_atomic(GUI, src)
  ```

### `D:\ShrimpDev\tools\Archiv\R1313_MainGUI_TrueFix.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\tools\Archiv\R1350_LearningJournalTab.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 100: **uses configparser (inspect for write/save)**
  ```
  import os, subprocess, webbrowser, configparser
  ```
- Zeile 109: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 124: **uses configparser (inspect for write/save)**
  ```
  p = configparser.ConfigParser()
  ```
- Zeile 135: **possible write() call**
  ```
  p.write(f)
  ```

### `D:\ShrimpDev\tools\Archiv\R1351_MainGUI_FixFutureImport.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 119: **possible write() call**
  ```
  f.write(fixed)
  ```

### `D:\ShrimpDev\tools\Archiv\R1402_PatchTopmostAndLabels.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 42: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\tools\Archiv\R1404_RemoveRootMenuPatch.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1405_FixRootMenuBlock.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1405_PatchIntakeNaming.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1406_UI_NamesAndVersion.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1407_Fastfix.py`
- Zeile 10: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1413_FixIntakeIndent.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1418_FixMainGuiClass.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1421_UIThemeAndTabs.py`
- Zeile 10: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1422_DefaultPath.py`
- Zeile 1: **uses configparser (inspect for write/save)**
  ```
  import re, pathlib, configparser, os
  ```
- Zeile 10: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 21: **uses configparser (inspect for write/save)**
  ```
  cp = configparser.ConfigParser()
  ```
- Zeile 28: **possible write() call**
  ```
  cp.write(f)
  ```
- Zeile 42: **uses configparser (inspect for write/save)**
  ```
  r"        import configparser, os\n"
  ```
- Zeile 44: **uses configparser (inspect for write/save)**
  ```
  r"        cp = configparser.ConfigParser()\n"
  ```

### `D:\ShrimpDev\tools\Archiv\R1423_MenuAndPolish.py`
- Zeile 10: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1428_IntakeHeal.py`
- Zeile 24: **possible write() call**
  ```
  with open(logp, "a", encoding="utf-8") as f: f.write(msg + "\n")
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 177: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\tools\Archiv\R1429_SyntaxRepair.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1430_IntakeAndMenuGuards.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1432_AddIntakeHelpers.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1433_ShrimpAppRestore.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1434_FixTryBlocks.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1436_FutureOrderFix.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(f"[R1436] {ts} {msg}\n")
  ```
- Zeile 32: **possible write() call**
  ```
  sys.stderr.write(f"[R1436] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R1504b.py`
- Zeile 10: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 29: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\R1623b.py`
- Zeile 10: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\R1648b.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 32: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 47: **possible write() call**
  ```
  d.write(s.read())
  ```
- Zeile 82: **possible save() call**
  ```
  "                _cfg_r1648.save(cfg)\n"
  ```
- Zeile 96: **possible write() call**
  ```
  f.write(new_txt)
  ```

### `D:\ShrimpDev\tools\Archiv\R1670b.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 48: **possible write() call**
  ```
  f.write(line + os.linesep)
  ```

### `D:\ShrimpDev\tools\Archiv\R1690b.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(line + os.linesep)
  ```

### `D:\ShrimpDev\tools\Archiv\R1693b.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(line + os.linesep)
  ```

### `D:\ShrimpDev\tools\Archiv\R1694b.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(line + os.linesep)
  ```

### `D:\ShrimpDev\tools\Archiv\R1802.py`
- Zeile 26: **possible write() call**
  ```
  f.write(ts + ' ' + text + '\n')
  ```

### `D:\ShrimpDev\tools\Archiv\R1841b.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write("[R1841b] " + msg + "\n")
  ```
- Zeile 131: **possible write() call**
  ```
  f.write("\n\n" + patch)
  ```

### `D:\ShrimpDev\tools\Archiv\R1931b.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2020.py`
- Zeile 34: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2021.py`
- Zeile 32: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2022.py`
- Zeile 29: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2027.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(line + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2028.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2030.py`
- Zeile 25: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2032.py`
- Zeile 32: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2034.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2034a.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2034b.py`
- Zeile 28: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2037b.py`
- Zeile 29: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2044.py`
- Zeile 153: **possible write() call**
  ```
  f.write(msg + "\\n")
  ```
- Zeile 205: **possible write() call**
  ```
  f.write(msg + "\\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2045.py`
- Zeile 92: **possible write() call**
  ```
  f.write(msg + "\\n")
  ```
- Zeile 131: **possible write() call**
  ```
  f.write(msg + "\\n")
  ```
- Zeile 136: **possible write() call**
  ```
  f.write(msg + "\\n")
  ```
- Zeile 175: **possible write() call**
  ```
  f.write(msg + "\\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2052.py`
- Zeile 44: **possible write() call**
  ```
  f.write(f"{ts} [{RUNNER_ID}] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2053.py`
- Zeile 33: **possible write() call**
  ```
  f.write(f"{ts} [{RUNNER_ID}] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2064.py`
- Zeile 24: **possible write() call**
  ```
  f.write(ts + " [" + RUNNER_ID + "] " + msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2066.py`
- Zeile 104: **possible save() call**
  ```
  "                _cfg_mod.save(cfg)\n"
  ```

### `D:\ShrimpDev\tools\Archiv\R2070.py`
- Zeile 26: **possible write() call**
  ```
  f.write(ts + " [" + RUNNER_ID + "] " + msg + "\n")
  ```
- Zeile 89: **possible save() call**
  ```
  "                _cfg_top.save(cfg)\n"
  ```

### `D:\ShrimpDev\tools\Archiv\R2072.py`
- Zeile 31: **possible write() call**
  ```
  f.write(ts + " [" + RUNNER_ID + "] " + msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2077.py`
- Zeile 34: **possible write() call**
  ```
  f.write(ts + " " + text + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2078.py`
- Zeile 31: **possible write() call**
  ```
  f.write(ts + " " + text + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2079.py`
- Zeile 31: **possible write() call**
  ```
  f.write(ts + " " + text + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2080.py`
- Zeile 27: **possible write() call**
  ```
  f.write(f"{ts} {text}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2081.py`
- Zeile 31: **possible write() call**
  ```
  f.write(ts + " " + text + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2082.py`
- Zeile 31: **possible write() call**
  ```
  f.write(ts + " " + text + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2083.py`
- Zeile 24: **possible write() call**
  ```
  f.write(f"{ts} {line}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2084.py`
- Zeile 29: **possible write() call**
  ```
  f.write(ts + " " + text + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2085.py`
- Zeile 29: **possible write() call**
  ```
  f.write(ts + " " + text + "\n")
  ```
- Zeile 78: **possible write() call**
  ```
  lines.append("            f.write(ts + ' ' + text + '\\n')")
  ```

### `D:\ShrimpDev\tools\Archiv\R2086.py`
- Zeile 102: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 141: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\tools\Archiv\R2087.py`
- Zeile 29: **possible write() call**
  ```
  f.write(ts + " " + text + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2088.py`
- Zeile 21: **possible write() call**
  ```
  f.write(ts + " " + txt + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2089.py`
- Zeile 20: **possible write() call**
  ```
  f.write(ts + " " + txt + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2090.py`
- Zeile 22: **possible write() call**
  ```
  f.write(ts + " " + txt + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2091.py`
- Zeile 28: **possible write() call**
  ```
  f.write(ts + " " + text + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2092.py`
- Zeile 28: **possible write() call**
  ```
  f.write(ts + " " + text + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2093.py`
- Zeile 29: **possible write() call**
  ```
  f.write(ts + " " + text + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2094.py`
- Zeile 30: **possible write() call**
  ```
  f.write(ts + " " + txt + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2124.py`
- Zeile 53: **possible write() call**
  ```
  f.write(f"[{_t.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2138.py`
- Zeile 66: **possible write() call**
  ```
  f.write(f"\n- [{ts}] {msg}\n")
  ```
- Zeile 123: **possible write() call**
  ```
  zf.write(fpath, arcname=str(rel))
  ```

### `D:\ShrimpDev\tools\Archiv\R2139.py`
- Zeile 111: **possible write() call**
  ```
  zf.write(fp, arcname=str(rel))
  ```
- Zeile 152: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2140.py`
- Zeile 89: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2141.py`
- Zeile 171: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2142.py`
- Zeile 58: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\R2143.py`
- Zeile 44: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\R2144.py`
- Zeile 46: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 203: **possible write() call**
  ```
  f.write(
  ```
- Zeile 209: **possible write() call**
  ```
  f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " [R2144] Hotfix: ui_masterrules_tab.py SyntaxError beseitigt, ShrimpDev startet wieder.\n")
  ```
- Zeile 211: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – " + RUNNER_ID + "\n- Fixed: Crash beim Start (SyntaxError in modules/ui_masterrules_tab.py).\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2144a.py`
- Zeile 45: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 181: **possible write() call**
  ```
  f.write(arch_add)
  ```
- Zeile 183: **possible write() call**
  ```
  f.write(notes_add)
  ```
- Zeile 185: **possible write() call**
  ```
  f.write(ch_add)
  ```

### `D:\ShrimpDev\tools\Archiv\R2145.py`
- Zeile 34: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2146.py`
- Zeile 31: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2147.py`
- Zeile 32: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 199: **possible write() call**
  ```
  f.write("\n## R2147 – Pipeline Auto-Reload\n- Pipeline-Tab laedt docs/PIPELINE.md automatisch neu (mtime-Check, bei Tab-Fokus + Timer).\n")
  ```
- Zeile 202: **possible write() call**
  ```
  f.write(stamp + " [R2147] Pipeline-Tab Auto-Reload implementiert.\n")
  ```
- Zeile 204: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2147\n- Added: Pipeline-Tab Auto-Reload (aktueller Stand).\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2148.py`
- Zeile 32: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 167: **possible write() call**
  ```
  f.write("\n## R2148 – Log Auto-Tail\n- Log-Tab laedt neue debug_output.txt Eintraege automatisch nach (append only, sichtbarkeitsbasiert).\n")
  ```
- Zeile 170: **possible write() call**
  ```
  f.write(stamp + " [R2148] Log Auto-Tail implementiert (1s tick, nur wenn Tab sichtbar).\n")
  ```
- Zeile 172: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2148\n- Added: Log-Tab Auto-Refresh/Tail (neue Eintraege automatisch).\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2149.py`
- Zeile 37: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 242: **possible write() call**
  ```
  f.write(
  ```
- Zeile 247: **possible write() call**
  ```
  f.write(stamp + " [R2149] Pipeline-Tab Auto-Reload (robust) implementiert.\n")
  ```
- Zeile 249: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2149\n")
  ```
- Zeile 250: **possible write() call**
  ```
  f.write("- Fixed: Pipeline-Tab Patch robust (build_pipeline_tab Signatur/Annotation egal).\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2150.py`
- Zeile 46: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 256: **possible write() call**
  ```
  f.write(
  ```
- Zeile 261: **possible write() call**
  ```
  f.write(stamp + " [R2150] Pipeline Auto-Reload (MR-konform) umgesetzt.\n")
  ```
- Zeile 263: **possible write() call**
  ```
  f.write(
  ```

### `D:\ShrimpDev\tools\Archiv\R2151.py`
- Zeile 28: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2152.py`
- Zeile 38: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 170: **possible write() call**
  ```
  f.write("\n## R2152 – Pipeline Auto-Reload\n- ui_pipeline_tab.py: Auto-Reload (mtime-check, Tab-Fokus + Timer), Triple-Quotes entfernt.\n")
  ```
- Zeile 173: **possible write() call**
  ```
  f.write(stamp + " [R2152] Pipeline Auto-Reload implementiert.\n")
  ```
- Zeile 175: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2152\n")
  ```
- Zeile 176: **possible write() call**
  ```
  f.write("- Added: Pipeline-Tab Auto-Reload (aktueller Stand) + MR-konforme Docstring-Entfernung.\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2153.py`
- Zeile 43: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 232: **possible write() call**
  ```
  f.write(
  ```
- Zeile 238: **possible write() call**
  ```
  f.write(stamp + " [R2153] Pipeline: Done/Offen sichtbar + Auto-Reload stabilisiert.\n")
  ```
- Zeile 240: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2153\n")
  ```
- Zeile 241: **possible write() call**
  ```
  f.write("- Fixed: ui_pipeline_tab.py (Indentation/Syntax) + Added: Done/Offen Anzeige.\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2154.py`
- Zeile 43: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 138: **possible write() call**
  ```
  f.write(
  ```
- Zeile 143: **possible write() call**
  ```
  f.write(stamp + " [R2154] Pipeline: Checkboxen klickbar + Save.\n")
  ```
- Zeile 145: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2154\n")
  ```
- Zeile 146: **possible write() call**
  ```
  f.write("- Added: Pipeline-Tab Checkbox click-to-toggle + persist to PIPELINE.md.\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2155.py`
- Zeile 44: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 355: **possible write() call**
  ```
  f.write("\n## R2155 – Pipeline Tab UX (Treeview)\n- Pipeline-Tab nutzt Treeview: Status/Prio/Task/Section, Toggle, Filter, Summary, Auto-Reload.\n")
  ```
- Zeile 357: **possible write() call**
  ```
  f.write(stamp + " [R2155] Pipeline-Tab UX verbessert (Treeview + Toggle + Filter + Summary).\n")
  ```
- Zeile 359: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2155\n")
  ```
- Zeile 360: **possible write() call**
  ```
  f.write("- Improved: Pipeline-Tab Lesbarkeit/Bedienbarkeit (Task-Liste statt Text).\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2156.py`
- Zeile 44: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 361: **possible write() call**
  ```
  f.write("\n## R2156 – Pipeline Tab Debug+Parser\n- Diagnose (Pfad/exists) + robustes Task-Parsing (+ Explorer-Button).\n")
  ```
- Zeile 363: **possible write() call**
  ```
  f.write(stamp + " [R2156] Pipeline: Diagnose + robustes Parsing (*/- Checkboxen).\n")
  ```
- Zeile 365: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2156\n")
  ```
- Zeile 366: **possible write() call**
  ```
  f.write("- Fixed: Pipeline-Tab zeigt jetzt Datei-Pfad/Status und erkennt Tasks robuster.\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2157.py`
- Zeile 42: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 151: **possible write() call**
  ```
  f.write("\n## R2157 – Pipeline Parser Fix\n- Fix: import re + Parser erkennt ⬜/✔ und - [ ]/- [x].\n")
  ```
- Zeile 153: **possible write() call**
  ```
  f.write(stamp + " [R2157] Pipeline: NameError re + Task-Parsing fuer ⬜/✔ erweitert.\n")
  ```
- Zeile 155: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2157\n")
  ```
- Zeile 156: **possible write() call**
  ```
  f.write("- Fixed: Pipeline-Tab Crash (re missing) + Added: ⬜/✔ Task-Erkennung.\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2158.py`
- Zeile 33: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 169: **possible write() call**
  ```
  f.write("\n## R2158 – Pipeline Tab Recovery\n- Rollback auf R2157-Backup + sauberer Parser-Replace (Indent stabil) + import re.\n")
  ```
- Zeile 171: **possible write() call**
  ```
  f.write(stamp + " [R2158] Pipeline: Recovery nach R2157 (IndentationError) + robust parsing.\n")
  ```
- Zeile 173: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2158\n")
  ```
- Zeile 174: **possible write() call**
  ```
  f.write("- Fixed: R2157 IndentationError by rollback + safe patch.\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2159.py`
- Zeile 34: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 79: **possible write() call**
  ```
  "            f.write(text)",
  ```
- Zeile 81: **possible write() call**
  ```
  "                f.write('\\n')",
  ```
- Zeile 280: **possible write() call**
  ```
  f.write("\n## R2159 – Exception Logging Basis\n")
  ```
- Zeile 281: **possible write() call**
  ```
  f.write("- Added: modules/exception_logger.py (debug_output + sys.excepthook + Tk callback hook).\n")
  ```
- Zeile 282: **possible write() call**
  ```
  f.write("- Patched: main_gui.py installiert Logging beim Start.\n")
  ```
- Zeile 284: **possible write() call**
  ```
  f.write(stamp + " [R2159] HIGH: Exceptions/Tracebacks sichtbar machen (Basis installiert).\n")
  ```
- Zeile 286: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2159\n")
  ```
- Zeile 287: **possible write() call**
  ```
  f.write("- Added: Central exception logging (debug_output.txt, Tk callback, sys.excepthook).\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2162.py`
- Zeile 34: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 137: **possible write() call**
  ```
  f.write("\n## R2162 – Exception Logger Install Fix\n")
  ```
- Zeile 138: **possible write() call**
  ```
  f.write("- Patched: main_gui.py main() detection robust (supports -> None) + installs exception_logger.\n")
  ```
- Zeile 140: **possible write() call**
  ```
  f.write(stamp + " [R2162] HIGH: main_gui.py patched to install exception logging (R2159 fix).\n")
  ```
- Zeile 142: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2162\n")
  ```
- Zeile 143: **possible write() call**
  ```
  f.write("- Fixed: R2159 main() detection (main() -> None) + install exception_logger.install(ROOT).\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2164.py`
- Zeile 28: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 30: **possible write() call**
  ```
  f.write("\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2165.py`
- Zeile 60: **possible write() call**
  ```
  f.write(
  ```
- Zeile 67: **possible write() call**
  ```
  f.write(
  ```
- Zeile 75: **possible write() call**
  ```
  f.write(
  ```
- Zeile 81: **possible write() call**
  ```
  f.write(
  ```

### `D:\ShrimpDev\tools\Archiv\R2166.py`
- Zeile 37: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 271: **possible write() call**
  ```
  f.write("\n## R2166 – Pipeline Tab UX\n")
  ```
- Zeile 272: **possible write() call**
  ```
  f.write("- Added: Search field + zebra rows + done/high emphasis + column sorting.\n")
  ```
- Zeile 273: **possible write() call**
  ```
  f.write("- Scope: modules/ui_pipeline_tab.py only.\n")
  ```
- Zeile 275: **possible write() call**
  ```
  f.write(stamp + " [R2166] (A/MEDIUM) Pipeline-Tab besser lesbar/bedienbar (Search+Sort+Zebra).\n")
  ```
- Zeile 277: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2166\n")
  ```
- Zeile 278: **possible write() call**
  ```
  f.write("- Improved: Pipeline tab UX (Search, Sort, Zebra, emphasis for done/HIGH).\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2167.py`
- Zeile 136: **possible write() call**
  ```
  f.write("\n".join(arch_append))
  ```
- Zeile 142: **possible write() call**
  ```
  f.write(stamp + " [R2167] Doku: Tab-Verträge/TABS.md eingeführt/aktualisiert.\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2167a.py`
- Zeile 158: **possible write() call**
  ```
  f.write("\n## R2167a – Agent Vertrag & Legacy bereinigt\n")
  ```
- Zeile 159: **possible write() call**
  ```
  f.write("- Agent-Tab ist verbindlich: modules/module_agent.py -> build_agent_tab(parent, app)\n")
  ```
- Zeile 160: **possible write() call**
  ```
  f.write("- modules/module_agent_ui.py als LEGACY/UNUSED markiert (nicht löschen/umbenennen).\n")
  ```
- Zeile 161: **possible write() call**
  ```
  f.write("- docs/TABS.md als zentrale Tab-Vertragsdatei gepflegt.\n")
  ```
- Zeile 164: **possible write() call**
  ```
  f.write(stamp + " [R2167a] Doku: Agent-Vertrag fixiert + module_agent_ui.py als Legacy markiert.\n")
  ```
- Zeile 167: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2167a\n")
  ```
- Zeile 168: **possible write() call**
  ```
  f.write("- Docs: Agent contract clarified; legacy Agent UI module marked as unused.\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2170.py`
- Zeile 54: **possible write() call**
  ```
  f.write(stamp + " [R2170] Pipeline: HIGH Intake Autosave nach Paste (nur bei Syntax OK).\n")
  ```
- Zeile 56: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2170\n")
  ```
- Zeile 57: **possible write() call**
  ```
  f.write("- Pipeline: Added HIGH item for Intake autosave-on-paste (guarded by syntax check).\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2171.py`
- Zeile 112: **possible write() call**
  ```
  f.write(stamp + f" [R2171] Pipeline: HIGH Intake Autosave nach Paste (Pfad={pipeline_path}).\n")
  ```
- Zeile 114: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2171\n")
  ```
- Zeile 115: **possible write() call**
  ```
  f.write("- Pipeline: Added HIGH item for Intake autosave-on-paste (guarded by syntax check).\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2173.py`
- Zeile 291: **possible write() call**
  ```
  f.write("\n## R2173 – Agent UI klickbar\n")
  ```
- Zeile 292: **possible write() call**
  ```
  f.write("- Agent-Tab: Empfehlungen als Liste + Aktionen (Ausführen, Pfad kopieren, In Pipeline).\n")
  ```
- Zeile 293: **possible write() call**
  ```
  f.write("- Pipeline-Pfad fest: docs/PIPELINE.md (mit Nachfrage).\n")
  ```
- Zeile 295: **possible write() call**
  ```
  f.write(stamp + " [R2173] Agent: Empfehlungen klickbar (Run/Copy/Pipeline).\n")
  ```
- Zeile 297: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2173\n")
  ```
- Zeile 298: **possible write() call**
  ```
  f.write("- Added: Clickable recommendations in Agent tab (run/copy/pipeline).\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2174.py`
- Zeile 104: **possible write() call**
  ```
  f.write(
  ```
- Zeile 111: **possible write() call**
  ```
  f.write(
  ```

### `D:\ShrimpDev\tools\Archiv\R2180.py`
- Zeile 169: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2180\n")
  ```
- Zeile 170: **possible write() call**
  ```
  f.write("- Docs: Generated docs/Runner_Status.md (read-only runner status report).\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2181.py`
- Zeile 130: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2181\n")
  ```
- Zeile 131: **possible write() call**
  ```
  f.write("- Docs: Generated docs/Runner_Archive_Plan.md (archive proposal, no changes).\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2183.py`
- Zeile 275: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2183\n")
  ```
- Zeile 276: **possible write() call**
  ```
  f.write("- Pipeline: Added item to remove obsolete GUI buttons across all tabs.\n")
  ```
- Zeile 277: **possible write() call**
  ```
  f.write("- Docs: Generated docs/GUI_Obsolete_Buttons.md (read-only analysis report).\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2184.py`
- Zeile 195: **possible write() call**
  ```
  f.write("\n## " + datetime.now().strftime("%Y-%m-%d") + " – R2184\n")
  ```
- Zeile 196: **possible write() call**
  ```
  f.write("- Docs: Generated docs/GUI_Tab_Inventory.md (tabs/buttons inventory, read-only).\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2194.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2196.py`
- Zeile 26: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2197.py`
- Zeile 32: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2198.py`
- Zeile 30: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2199.py`
- Zeile 36: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2200.py`
- Zeile 32: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2201.py`
- Zeile 40: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2202.py`
- Zeile 44: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2204.py`
- Zeile 40: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2205.py`
- Zeile 31: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2206.py`
- Zeile 59: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2207.py`
- Zeile 32: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2208.py`
- Zeile 22: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 29: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2239.py`
- Zeile 66: **possible write() call**
  ```
  "        f.write(line + '\\n')\n"
  ```

### `D:\ShrimpDev\tools\Archiv\R2249.py`
- Zeile 99: **possible write() call**
  ```
  "            f.write(line.rstrip('\\n') + '\\n')\n"
  ```

### `D:\ShrimpDev\tools\Archiv\R2257.py`
- Zeile 65: **possible write() call**
  ```
  f.write(f"[{RUNNER_ID}] RUN-PFAD-ANALYSE (READ-ONLY)\n")
  ```
- Zeile 66: **possible write() call**
  ```
  f.write(f"Root: {ROOT}\n")
  ```
- Zeile 67: **possible write() call**
  ```
  f.write(f"Timestamp: {datetime.now()}\n\n")
  ```
- Zeile 70: **possible write() call**
  ```
  f.write("Keine Treffer gefunden.\n")
  ```
- Zeile 73: **possible write() call**
  ```
  f.write(f"{cls} {line}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2266.py`
- Zeile 19: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\tools\Archiv\R2271.py`
- Zeile 24: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 32: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```

### `D:\ShrimpDev\tools\Archiv\R2274.py`
- Zeile 22: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\tools\Archiv\R2277.py`
- Zeile 239: **possible write() call**
  ```
  f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] [RUNNER] {RID} applied\\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2280.py`
- Zeile 240: **possible write() call**
  ```
  f.write("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] [INFO] [RUNNER] R2280 applied\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2281.py`
- Zeile 184: **possible write() call**
  ```
  f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [RUNNER] {RID} applied\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2282.py`
- Zeile 204: **possible write() call**
  ```
  f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [RUNNER] {RID} applied\\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2284.py`
- Zeile 261: **possible write() call**
  ```
  f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [RUNNER] R2284 applied\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2285.py`
- Zeile 128: **possible write() call**
  ```
  f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [RUNNER] {RID} applied\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2286.py`
- Zeile 260: **possible write() call**
  ```
  f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [RUNNER] {RID} applied\\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2293.py`
- Zeile 101: **possible write() call**
  ```
  fp.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [RUNNER] {RID} report={out.name}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2295.py`
- Zeile 125: **possible write() call**
  ```
  f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [RUNNER] {RID} applied\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2296.py`
- Zeile 63: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 111: **possible write() call**
  ```
  f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [RUNNER] {RID} applied\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2297.py`
- Zeile 234: **possible write() call**
  ```
  f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [RUNNER] {RID} applied (purge hard protect)\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2298.py`
- Zeile 40: **possible write() call**
  ```
  f.write(line + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2299.py`
- Zeile 37: **possible write() call**
  ```
  f.write(line + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2303.py`
- Zeile 49: **possible write() call**
  ```
  f.write(line + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2304.py`
- Zeile 40: **possible write() call**
  ```
  f.write(line + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R2320.py`
- Zeile 32: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\tools\Archiv\R2321.py`
- Zeile 33: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 52: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\tools\Archiv\R2322.py`
- Zeile 34: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 54: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\tools\Archiv\R2323.py`
- Zeile 33: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\tools\Archiv\R2324.py`
- Zeile 33: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\tools\Archiv\R2325.py`
- Zeile 33: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\tools\Archiv\R2326.py`
- Zeile 33: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 52: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 81: **uses configparser (inspect for write/save)**
  ```
  # 1) Imports erweitern (configparser)
  ```
- Zeile 83: **uses configparser (inspect for write/save)**
  ```
  if imp_anchor in text and "import configparser" not in text:
  ```
- Zeile 84: **uses configparser (inspect for write/save)**
  ```
  text = text.replace(imp_anchor, imp_anchor + "import configparser\n")
  ```
- Zeile 85: **uses configparser (inspect for write/save)**
  ```
  log_line("OK: import configparser hinzugefügt", log_path)
  ```
- Zeile 112: **uses configparser (inspect for write/save)**
  ```
  "    cfg = configparser.ConfigParser()\n"
  ```
- Zeile 127: **possible write() call**
  ```
  "            cfg.write(f)\n"
  ```
- Zeile 132: **possible write() call**
  ```
  "                cfg.write(f)\n"
  ```

### `D:\ShrimpDev\tools\Archiv\R2328.py`
- Zeile 38: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 58: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 111: **uses configparser (inspect for write/save)**
  ```
  # wir wollen am Ende: import os, import configparser
  ```
- Zeile 122: **uses configparser (inspect for write/save)**
  ```
  if "import configparser\n" not in text:
  ```
- Zeile 125: **uses configparser (inspect for write/save)**
  ```
  text = text.replace(anchor, anchor + "import configparser\n")
  ```
- Zeile 128: **uses configparser (inspect for write/save)**
  ```
  text = "import configparser\n" + text
  ```
- Zeile 160: **uses configparser (inspect for write/save)**
  ```
  "    cfg = configparser.ConfigParser()\n"
  ```
- Zeile 175: **possible write() call**
  ```
  "            cfg.write(f)\n"
  ```
- Zeile 180: **possible write() call**
  ```
  "                cfg.write(f)\n"
  ```

### `D:\ShrimpDev\tools\Archiv\R2329.py`
- Zeile 33: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 103: **possible write() call**
  ```
  "            f.write(line + '\\n')\n"
  ```
- Zeile 151: **uses configparser (inspect for write/save)**
  ```
  "    import configparser\n"
  ```
- Zeile 152: **uses configparser (inspect for write/save)**
  ```
  "    cfg = configparser.ConfigParser()\n"
  ```
- Zeile 168: **possible write() call**
  ```
  "            cfg.write(f)\n"
  ```
- Zeile 173: **possible write() call**
  ```
  "                cfg.write(f)\n"
  ```
- Zeile 397: **uses configparser (inspect for write/save)**
  ```
  if "import configparser\n" not in text:
  ```
- Zeile 401: **uses configparser (inspect for write/save)**
  ```
  text = text.replace(anchor, anchor + "import configparser\n")
  ```
- Zeile 403: **uses configparser (inspect for write/save)**
  ```
  text = "import configparser\n" + text
  ```

### `D:\ShrimpDev\tools\Archiv\R2330.py`
- Zeile 33: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\tools\Archiv\R2331.py`
- Zeile 33: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\tools\Archiv\R2332.py`
- Zeile 33: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\tools\Archiv\R9997.py`
- Zeile 10: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 25: **possible write() call**
  ```
  f.write(f"[R9997 {ts}] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R9998.py`
- Zeile 10: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\R9999.py`
- Zeile 10: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1000_IntakeActions.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 32: **possible write() call**
  ```
  f.write(f"[R1000] {ts} {msg}\n")
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 77: **possible write() call**
  ```
  f.write(CHANGELOG_APPEND)
  ```
- Zeile 98: **possible save() call**
  ```
  self.save()
  ```
- Zeile 105: **possible save() call**
  ```
  self.save()
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1001_AlwaysOnTopFixImports.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 148: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 157: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 230: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 236: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1002_SnippetsRestore.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 31: **possible write() call**
  ```
  f.write(f"[R1002] {ts} {msg}\n")
  ```
- Zeile 42: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 55: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {msg}\n")
  ```
- Zeile 93: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {msg}\n")
  ```
- Zeile 121: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1003_FixIndentFallbackLogger.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 32: **possible write() call**
  ```
  f.write(f"[R1003] {ts} {msg}\n")
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 63: **possible write() call**
  ```
  "                f.write(f'[{prefix}] {ts} {msg}\\n')\n"
  ```
- Zeile 99: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1004_ShrimpDev_PathFix.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(f"[R1004] {ts} {msg}\n")
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 51: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 63: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {msg}\n")
  ```
- Zeile 99: **possible write() call**
  ```
  "                f.write(f'[{prefix}] {ts} {msg}\\n')\n"
  ```
- Zeile 155: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1005_MainGUI_Rewrite.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 31: **possible write() call**
  ```
  f.write(f"[R1005] {ts} {msg}\n")
  ```
- Zeile 42: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 67: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {msg}\n")
  ```
- Zeile 152: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1006_ConfigMgr_Restore.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(f"[R1006] {ts} {msg}\n")
  ```
- Zeile 46: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 50: **uses configparser (inspect for write/save)**
  ```
  import os, threading, configparser
  ```
- Zeile 80: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 84: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 91: **uses configparser (inspect for write/save)**
  ```
  self.cfg = configparser.ConfigParser()
  ```
- Zeile 102: **possible write() call**
  ```
  self.cfg.write(f)
  ```
- Zeile 123: **possible save() call**
  ```
  self.save()
  ```
- Zeile 146: **possible save() call**
  ```
  self.save()
  ```
- Zeile 156: **possible save() call**
  ```
  self.save()
  ```
- Zeile 163: **possible save() call**
  ```
  self.save()
  ```
- Zeile 175: **possible write() call**
  ```
  f.write("")
  ```
- Zeile 184: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1007_UIFrames_Restore.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(f"[R1007] {ts} {msg}\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 97: **possible write() call**
  ```
  f.write("")
  ```
- Zeile 171: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1008_IntakeUX_Revamp.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(f"[R1008] {ts} {msg}\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 87: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 291: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1010_IntakeUX_Refine.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 32: **possible write() call**
  ```
  f.write(f"[R1010] {ts} {msg}\n")
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 60: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 273: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 365: **possible write() call**
  ```
  f.write(f"[{p}] {ts} {m}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1011_IntakeUX_ActionsBar.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 40: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 165: **possible write() call**
  ```
  f.write(new)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1012_FixMenuIndent.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 31: **possible write() call**
  ```
  f.write(f"[R1012] {ts} {msg}\n")
  ```
- Zeile 74: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 81: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.3\n")
  ```
- Zeile 83: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1013_SafeBoot_Debug.py`
- Zeile 20: **possible write() call**
  ```
  f.write(f"[R1013] {ts} {msg}\n")
  ```
- Zeile 201: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 205: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.4\n")
  ```
- Zeile 207: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1014_SafeBoot_StringFix.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 32: **possible write() call**
  ```
  f.write(f"[R1014] {ts} {msg}\n")
  ```
- Zeile 62: **possible write() call**
  ```
  f.write(src_fixed)
  ```
- Zeile 68: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.5\n")
  ```
- Zeile 70: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1015_SafeBoot_StringHardFix.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 51: **possible write() call**
  ```
  f.write(f"[{p}] {ts} {m}\n")
  ```
- Zeile 198: **possible write() call**
  ```
  f.write(f"[R1015] {ts} {msg}\n")
  ```
- Zeile 209: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 216: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1016_IntakeFix_ContextActions.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(f"[R1016] {ts} {msg}\n")
  ```
- Zeile 42: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 117: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.7\n")
  ```
- Zeile 119: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1017_IntakeUX_CopyPasteName.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(f"[R1017] {ts} {msg}\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 270: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 363: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 372: **possible write() call**
  ```
  f.write("[R1017] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1018_ExtOverride_AndQA.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(f"[R1018] {ts} {msg}\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 186: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.9\n")
  ```
- Zeile 188: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1019_ExtOverride_DetectFix.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 32: **possible write() call**
  ```
  f.write(f"[R1019] {ts} {msg}\n")
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 125: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.10\n")
  ```
- Zeile 127: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1020_SafeBoot_Logfix.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 32: **possible write() call**
  ```
  f.write(f"[R1020] {ts} {msg}\n")
  ```
- Zeile 40: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 66: **possible write() call**
  ```
  "                f.write(msg)\n"
  ```
- Zeile 84: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.11\n")
  ```
- Zeile 86: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1021_SafeBoot_FinalFix.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 32: **possible write() call**
  ```
  f.write(f"[R1021] {ts} {msg}\n")
  ```
- Zeile 40: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 76: **possible write() call**
  ```
  "                f.write(msg)\n"
  ```
- Zeile 93: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.12\n")
  ```
- Zeile 95: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1022_MainGUI_SafeImportsRepair.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 69: **possible write() call**
  ```
  f.write(f"[R1022] {ts} {msg}\n")
  ```
- Zeile 79: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 110: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.13\n")
  ```
- Zeile 112: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1023_SafeFallbackRepair.py`
- Zeile 15: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 66: **possible write() call**
  ```
  f.write(f"[R1023] {ts} {msg}\n")
  ```
- Zeile 74: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 88: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.14\n")
  ```
- Zeile 90: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1024_LoggerAtomicFix.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 31: **possible write() call**
  ```
  f.write(f"[R1024] {ts} {msg}\n")
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 63: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 73: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 85: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.15\n")
  ```
- Zeile 87: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1025_SafeFallbackCapture.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 72: **possible write() call**
  ```
  f.write(f"[R1025] {ts} {msg}\n")
  ```
- Zeile 82: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 101: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.16\n")
  ```
- Zeile 103: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1026_IntakeIndentFix.py`
- Zeile 15: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(f"[R1026] {ts} {msg}\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 70: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.17\n")
  ```
- Zeile 72: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1027_IntakeSaveRewrite.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(f"[R1027] {ts} {msg}\n")
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 61: **possible write() call**
  ```
  "                    f.write(data)\n"
  ```
- Zeile 159: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.18\n")
  ```
- Zeile 161: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1028_IntakeModule_Reset.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(f"[R1028] {ts} {msg}\n")
  ```
- Zeile 294: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 408: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 416: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1030_IntakeButtons_Fix.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[R1030] {ts} {msg}\n")
  ```
- Zeile 114: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 136: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.20\n")
  ```
- Zeile 138: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 151: **possible write() call**
  ```
  f.write("[R1030] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1031_ButtonsForceWire_Debug.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[R1031] {ts} {msg}\n")
  ```
- Zeile 186: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 196: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.21\n")
  ```
- Zeile 198: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1032_ButtonsHardBind_Ping.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(f"[R1032] {ts} {msg}\n")
  ```
- Zeile 192: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 198: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.22\n")
  ```
- Zeile 200: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 212: **possible write() call**
  ```
  f.write("[R1032] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1033_FixBrokenPanedwindow.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(f"[R1033] {ts} {msg}\n")
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 101: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.23\n")
  ```
- Zeile 103: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 116: **possible write() call**
  ```
  f.write("[R1033] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1034_IntakeDetect_SmartFix.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[R1034] {ts} {msg}\n")
  ```
- Zeile 46: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 153: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.24\n")
  ```
- Zeile 155: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 168: **possible write() call**
  ```
  f.write("[R1034] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1035_DetectWire_All.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(f"[R1035] {ts} {msg}\n")
  ```
- Zeile 48: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 169: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.25\n")
  ```
- Zeile 171: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 179: **possible write() call**
  ```
  f.write("[R1035] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1036_NameDetect_FromCode.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(f"[R1036] {ts} {msg}\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 150: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.26\n")
  ```
- Zeile 152: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 165: **possible write() call**
  ```
  f.write("[R1036] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1037_FixDetectSyntax.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(f"[R1037] {ts} {msg}\n")
  ```
- Zeile 62: **possible write() call**
  ```
  f.write(fixed)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1038_DetectBlock_Rewrite.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(f"[R1038] {ts} {msg}\n")
  ```
- Zeile 191: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.27\n")
  ```
- Zeile 193: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 210: **possible write() call**
  ```
  f.write(src3)
  ```
- Zeile 220: **possible write() call**
  ```
  f.write("[R1038] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1039_IndentFix_TryExcept.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(f"[R1039] {ts} {msg}\n")
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 107: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.28\n")
  ```
- Zeile 109: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1040_Intake_FullReset.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(f"[R1040] {ts} {msg}\n")
  ```
- Zeile 377: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 495: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 501: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1041_AutoDetect_OnPaste.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(f"[R1041] {ts} {msg}\n")
  ```
- Zeile 46: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 132: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.31\n")
  ```
- Zeile 134: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 151: **possible write() call**
  ```
  f.write("[R1041] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1042_AutoDetect_Hardwire_Scan.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(f"[R1042] {ts} {msg}\n")
  ```
- Zeile 48: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 178: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.32\n")
  ```
- Zeile 180: **possible write() call**
  ```
  f.write("""
  ```
- Zeile 197: **possible write() call**
  ```
  f.write("[R1042] FEHLER:\n" + traceback.format_exc() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1043_NoBell_StripTypeHints.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[R1043] {ts} {msg}\n")
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 80: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.33\n")
  ```
- Zeile 82: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1044_Intake_Reinstall_Clean.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(f"[R1044] {ts} {msg}\n")
  ```
- Zeile 416: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 545: **possible write() call**
  ```
  f.write(SRC)
  ```
- Zeile 548: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.34\n")
  ```
- Zeile 550: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1045_NameForceAndDateCols.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[R1045] {ts} {msg}\n")
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 138: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.35\n")
  ```
- Zeile 140: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1046_NameDocstring_Fallback_DateCols.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(f"[R1046] {ts} {msg}\n")
  ```
- Zeile 48: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 120: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.36\n")
  ```
- Zeile 122: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1047_Intake_CleanHardReset.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[R1047] {ts} {msg}\n")
  ```
- Zeile 397: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 531: **possible write() call**
  ```
  f.write(SRC)
  ```
- Zeile 533: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.37\n")
  ```
- Zeile 535: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1048_Intake_DeleteAndRecent50.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(f"[R1048] {ts} {msg}\n")
  ```
- Zeile 52: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 204: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.38\n")
  ```
- Zeile 206: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1049_Intake_ResizeNameExt.py`
- Zeile 25: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 42: **possible write() call**
  ```
  f.write(f"[R1049] {ts} {msg}\n")
  ```
- Zeile 51: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 124: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.39\n")
  ```
- Zeile 126: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1050_ExtDetectStrong.py`
- Zeile 29: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 46: **possible write() call**
  ```
  f.write(f"[R1050] {ts} {msg}\n")
  ```
- Zeile 59: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 167: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.40\n")
  ```
- Zeile 169: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1051_ExtDetectStrong_FixSub.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 100: **possible write() call**
  ```
  f.write(f"[R1051] {ts} {msg}\n")
  ```
- Zeile 113: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 149: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.41\n")
  ```
- Zeile 151: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1052_FixEntExtGrid.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(f"[R1052] {ts} {msg}\n")
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 75: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.42\n")
  ```
- Zeile 77: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1053_Intake_ClearOnDelete_RefreshOnPaste.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(f"[R1053] {ts} {msg}\n")
  ```
- Zeile 48: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 120: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.43\n")
  ```
- Zeile 122: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1054_Intake_QuoteFix_ClearDelete_PasteReset.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[R1054] {ts} {msg}\n")
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 136: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.44\n")
  ```
- Zeile 138: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1055_FixIndent_OnEditorModified.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(f"[R1055] {ts} {msg}\n")
  ```
- Zeile 51: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 101: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.45\n")
  ```
- Zeile 103: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1056_FixIndent_OnEditorModified_Strict.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(f"[R1056] {ts} {msg}\n")
  ```
- Zeile 57: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 102: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.46\n")
  ```
- Zeile 104: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1057_IndentAudit_IntakeFrame.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(f"[R1057] {ts} {msg}\n")
  ```
- Zeile 73: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 117: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.47\n")
  ```
- Zeile 119: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1058_FixKeyAndModified_Block.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 51: **possible write() call**
  ```
  f.write(f"[R1058] {ts} {msg}\n")
  ```
- Zeile 64: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 109: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.48\n")
  ```
- Zeile 111: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1059_FixDeleteIndent.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 62: **possible write() call**
  ```
  f.write(f"[R1059] {ts} {msg}\n")
  ```
- Zeile 75: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 111: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.49\n")
  ```
- Zeile 113: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1060_FixAskYesNo_StringConcat.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 67: **possible write() call**
  ```
  f.write(f"[R1060] {ts} {msg}\n")
  ```
- Zeile 80: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 117: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.50\n")
  ```
- Zeile 119: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1061_FixAskYesNo_StringEscape.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 65: **possible write() call**
  ```
  f.write(f"[R1061] {ts} {msg}\n")
  ```
- Zeile 78: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1062_FutureAtTop.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(f"[R1062] {ts} {msg}\n")
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 131: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.52\n")
  ```
- Zeile 133: **possible write() call**
  ```
  f.write("""
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1063_Intake_SanityGuard.py`
- Zeile 14: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1064_IntegrateGuard_UI.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  with open(p, "w", encoding="utf-8", newline="\r\n") as f: f.write(data)
  ```
- Zeile 151: **possible write() call**
  ```
  f.write("ShrimpDev v9.9.54\n")
  ```
- Zeile 153: **possible write() call**
  ```
  f.write("\n## v9.9.54\n- Intake: Guard-Button + Handler integriert (Prüfen & ✅-Markierung)\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1065_IntakeRescueAndRollback.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(f"[R1065] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1066_FixGuard_MissingHelpers.py`
- Zeile 42: **possible write() call**
  ```
  #             f.write(f"[R1063] {ts} {msg}\n")
  ```
- Zeile 175: **possible write() call**
  ```
  #         with open(p, "w", encoding="utf-8", newline="\r\n") as f: f.write(data)
  ```
- Zeile 193: **possible write() call**
  ```
  #         with open(fail, "w", encoding="utf-8", newline="\r\n") as f: f.write(src1)
  ```
- Zeile 214: **possible write() call**
  ```
  #         f.write(GUARD_SRC)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1067_WriteGuard_Safe.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(f'[R1063] {ts} {msg}\\n')
  ```
- Zeile 186: **possible write() call**
  ```
  with open(p, 'w', encoding='utf-8', newline='\\r\\n') as f: f.write(data)
  ```
- Zeile 204: **possible write() call**
  ```
  with open(fail, 'w', encoding='utf-8', newline='\\r\\n') as f: f.write(src1)
  ```
- Zeile 226: **possible write() call**
  ```
  f.write(GUARD_SRC)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1068_FixLonelyTry.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[R1068] {ts} {msg}\n")
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1069_FixIntake_GuardToolbar.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 40: **possible write() call**
  ```
  f.write(f"[R1069] {ts} {msg}\n")
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1070_FixSemicolonLines.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(f"[R1070] {ts} {msg}\n")
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1071_AddRunButton_PyExec.py`
- Zeile 25: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 42: **possible write() call**
  ```
  f.write(f"[R1071] {ts} {msg}\n")
  ```
- Zeile 55: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1072_InsertRunButton_AnyAnchor.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(f"[R1072] {ts} {msg}\n")
  ```
- Zeile 51: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1073_FixToolbarAndRunButton.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(f"[R1073] {ts} {msg}\n")
  ```
- Zeile 51: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1074_DeleteButtons_WithRecycleBin.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(f"[R1074] {ts} {msg}\n")
  ```
- Zeile 52: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1074b_DeleteButtons_WithRecycleBin_Fix.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[R1074b] {ts} {msg}\n")
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1077_FixIndent_UIBlock.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 59: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1078_WriteGuard_Clean.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 99: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1082_Guard_VerboseOK.py`
- Zeile 83: **possible write() call**
  ```
  #         f.write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1084_FixGuard_ArgParse.py`
- Zeile 102: **possible write() call**
  ```
  #         f.write(text)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1089_ApplyNameDetect_GuardRun_Delete.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(s.encode("utf-8"))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1090_FixIntake_Indent.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1092_FixRecycleBinIndent.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1093_FixIntake_IndentGlobal.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1094_FixRecycleBinIndentFinal.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1095_ClassSafeguard_Intake.py`
- Zeile 14: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 29: **possible write() call**
  ```
  f_out.write(f_in.read())
  ```
- Zeile 54: **possible write() call**
  ```
  open(MOD, "w", encoding="utf-8").write(patch)
  ```
- Zeile 76: **possible write() call**
  ```
  open(MOD, "w", encoding="utf-8").write(patched)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1096_Reindent_IntakeMethods.py`
- Zeile 13: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 31: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 102: **possible write() call**
  ```
  f.write("".join(lines))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1097_FixIntake_Reindent.py`
- Zeile 13: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 39: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 52: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1097b_FixIntake_Reindent2.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 27: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1097c_FixIntake_ReindentHard.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 27: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1097d_Reindent_Intake_Strict.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 27: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1098_FixIntake_ReindentClassBlocks.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 147: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1099_FixIntake_RepairIndentPass2.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 51: **possible write() call**
  ```
  f.write(text.encode("utf-8"))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1100_FixIntake_ReindentAll.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1100_Reindent_IntakeFrame_Harden.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(text.encode("utf-8"))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1101_FixIntake_ReindentAll.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  with open(p, "wb") as f: f.write(s.encode("utf-8", "utf-8"))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1101a_FixReplace_RecycleBin.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(s.encode("utf-8"))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1102_FixIntake_ReindentAndScope.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1103_FixIntake_ReindentAndScope.py`
- Zeile 14: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 42: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1104_ReplaceIntake_Clean.py`
- Zeile 14: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 386: **possible write() call**
  ```
  f.write(self.txt.get("1.0","end-1c"))
  ```
- Zeile 489: **possible write() call**
  ```
  f.write(NEW_SRC)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1105_FixDeleteSignature_Compile.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1106_ShrimpGuard_Integriert.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1106b_IntegrateGuard_UI.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(txt)
  ```
- Zeile 130: **possible write() call**
  ```
  f"{indent}        tmp.write(self.txt.get('1.0', 'end-1c').encode('utf-8'))\n"
  ```
- Zeile 147: **possible write() call**
  ```
  f"{indent}            f.write(out)\n"
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1106c_IntegrateGuard_UI_FixedFuture.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(txt)
  ```
- Zeile 80: **possible write() call**
  ```
  "            tmp.write(self.txt.get('1.0', 'end-1c').encode('utf-8'))\n"
  ```
- Zeile 86: **possible write() call**
  ```
  "                f.write(out)\n"
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1107_AutoRepair_IndentBlocks.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 40: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 54: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1107_AutoRepair_Intake_BindsAndTry.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1107b_AutoRepair_IndentBlocks_ReturnFix.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(t)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1108_DisableButtonReleaseBinds.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  g.write(f.read())
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(t)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1109_EnableTkCallbackTrace.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  g.write(f.read())
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(t)
  ```
- Zeile 52: **possible write() call**
  ```
  f.write("\n--- Tk-Callback-Exception ---\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1110_FixIntake_ToolbarTryAndHelpers.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  w.write(r.read())
  ```
- Zeile 46: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1112_DeepRepair_IntakeAndGUI.py`
- Zeile 29: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 68: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1113_DeepRepair_FixReturnScope.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 47: **possible write() call**
  ```
  with open(path, "w", encoding="utf-8", newline="\n") as f: f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1114_DeepSanityAndRepair.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 56: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1114b_FixUnexpectedIndent_MainGUI.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 49: **possible write() call**
  ```
  with open(p,"w",encoding="utf-8",newline="\n") as f: f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1115_IntegrateRepairUI.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  with open(p,"w",encoding="utf-8",newline="\n") as f: f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1116_ReentrantBindGuard.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1116a_FixMainGUITabs.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  with open(p,"w",encoding="utf-8",newline="\n") as f: f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1116b_ReentrantBindGuard_AST.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  with open(p,"w",encoding="utf-8",newline="\n") as f: f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1116c_DeepFix_IntakeUI.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(t)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1116d_FixRecycleBinHelper_Only.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 29: **possible write() call**
  ```
  f.write(t)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1116e_DeepFix_IntakeUI_Safe.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1116f_DumpSyntaxContext.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 63: **possible write() call**
  ```
  f.write(ctx + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1116g_FixToolbarBlock.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(s.encode("utf-8"))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1117.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 59: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 227: **possible write() call**
  ```
  report.write(f"Datei: {os.path.relpath(path, ROOT)}\nZeit : {datetime.now()}\n\n")
  ```
- Zeile 234: **possible write() call**
  ```
  report.write("[Bindings]\n")
  ```
- Zeile 236: **possible write() call**
  ```
  report.write(f"  Zeile {ln:>5}: bind({seq!r}, {cb})\n")
  ```
- Zeile 238: **possible write() call**
  ```
  report.write("  (keine gefunden)\n")
  ```
- Zeile 239: **possible write() call**
  ```
  report.write("\n[Button-Commands]\n")
  ```
- Zeile 241: **possible write() call**
  ```
  report.write(f"  Zeile {ln:>5}: command={cb}\n")
  ```
- Zeile 243: **possible write() call**
  ```
  report.write("  (keine gefunden)\n")
  ```
- Zeile 246: **possible write() call**
  ```
  report.write("\n[Verdacht: doppelte Callback-Verwendung]\n")
  ```
- Zeile 254: **possible write() call**
  ```
  report.write(f"  ⚠ Callback '{cb}' taucht in command und bind auf (z.B. Zeile {ln}).\n")
  ```
- Zeile 255: **possible write() call**
  ```
  report.write("  -> Empfehlung: bind-Handler auf Button mit lambda e: button.invoke(); return 'break'\n")
  ```
- Zeile 256: **possible write() call**
  ```
  report.write("    oder nur eine Quelle beibehalten (command ODER bind-basiert), um Doppeltrigger zu vermeiden.\n")
  ```
- Zeile 258: **possible write() call**
  ```
  report.write("  (kein offensichtlicher Doppeltrigger gefunden)\n")
  ```
- Zeile 262: **possible write() call**
  ```
  report.write("\n[Methoden & Aufrufe]\n")
  ```
- Zeile 265: **possible write() call**
  ```
  report.write(f"  def {name} (Z {info.lineno}) -> [{calls}]\n")
  ```
- Zeile 268: **possible write() call**
  ```
  report.write("\n[Direkte Rekursion]\n")
  ```
- Zeile 272: **possible write() call**
  ```
  report.write(f"  ⚠ {m.name} ruft sich selbst auf (Z {m.lineno}).\n")
  ```
- Zeile 274: **possible write() call**
  ```
  report.write("  (keine direkte Rekursion)\n")
  ```
- Zeile 277: **possible write() call**
  ```
  report.write("\n[Zirkuläre Verweise]\n")
  ```
- Zeile 296: **possible write() call**
  ```
  report.write("\n".join(sorted(set(cyc_lines))) + "\n")
  ```
- Zeile 298: **possible write() call**
  ```
  report.write("  (keine Zyklen 2/3 erkannt)\n")
  ```
- Zeile 301: **possible write() call**
  ```
  report.write("\n[Toolbar-Kontext ~Z120-180 ±40]\n")
  ```
- Zeile 302: **possible write() call**
  ```
  report.write(textwrap.indent(approx_slice if approx_slice.strip() else "(kein Auszug)", "  "))
  ```
- Zeile 311: **possible write() call**
  ```
  cg.write(f"{name} -> {callee}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1118_SafeTkHandler.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 68: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 86: **possible write() call**
  ```
  "                f.write(text)\n"
  ```
- Zeile 141: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 148: **possible write() call**
  ```
  f.write("Runner_1118_SafeTkHandler - Start\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1118b_GlobalTkPatch.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 56: **possible write() call**
  ```
  open(p, "w", encoding="utf-8", newline="\n").write(new)
  ```
- Zeile 73: **possible write() call**
  ```
  "                f.write(txt)\n"
  ```
- Zeile 136: **possible write() call**
  ```
  open(p, "w", encoding="utf-8", newline="\n").write(src)
  ```
- Zeile 142: **possible write() call**
  ```
  open(REPORT, "w", encoding="utf-8", newline="\n").write("Runner_1118b_GlobalTkPatch - Start\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1119_TkGuardTopLevel.py`
- Zeile 24: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 40: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 60: **possible write() call**
  ```
  "                f.write(txt)\n"
  ```
- Zeile 124: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 129: **possible write() call**
  ```
  f.write("Runner_1119_TkGuardTopLevel - Start\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1120_FixFutureAndGuard.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 40: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 63: **possible write() call**
  ```
  "                f.write(txt)\n"
  ```
- Zeile 192: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 197: **possible write() call**
  ```
  f.write("Runner_1120_FixFutureAndGuard - Start\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1121_CentralGuard.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 87: **possible write() call**
  ```
  "                    f.write(f\"[{prefix}] {ts} {message}\\n\")\n"
  ```
- Zeile 135: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 142: **possible write() call**
  ```
  f.write("Runner_1121_CentralGuard - Start\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1122_RepairMainGUI_SafeLogging.py`
- Zeile 30: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 59: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 113: **possible write() call**
  ```
  "                    f.write(f\"[{prefix}] {ts} {message}\\n\")\n"
  ```
- Zeile 185: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 191: **possible write() call**
  ```
  f.write("Runner_1122_RepairMainGUI_SafeLogging - Start\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1123_EditorGuardPatch.py`
- Zeile 27: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 64: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {message}\n")
  ```
- Zeile 197: **possible write() call**
  ```
  f.write("Runner_1123_EditorGuardPatch - Start\n")
  ```
- Zeile 209: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 221: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1124_AllFixes_IntakeStable.py`
- Zeile 26: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 88: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {message}\n")
  ```
- Zeile 97: **possible write() call**
  ```
  f.write(LOGGER_SRC)
  ```
- Zeile 125: **possible write() call**
  ```
  "                    f.write(f\"[{prefix}] {ts} {message}\\n\")\n"
  ```
- Zeile 200: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 208: **possible write() call**
  ```
  f.write(orig)
  ```
- Zeile 225: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {message}\n")
  ```
- Zeile 338: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 346: **possible write() call**
  ```
  f.write(orig)
  ```
- Zeile 353: **possible write() call**
  ```
  f.write("Runner_1124_AllFixes_IntakeStable - Start\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1125_IntakeRescue.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 84: **possible write() call**
  ```
  f.write(f"[{prefix}] {_ts} {message}\\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1126_IntakeRescue2.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 100: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {message}\n")
  ```
- Zeile 206: **possible write() call**
  ```
  f.write("Runner_1126_IntakeRescue2 - Start\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1127_IntakeDetox.py`
- Zeile 26: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {msg}\n")
  ```
- Zeile 93: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {message}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1127_IntakeFix_All.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 40: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 52: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1128_FixToolbarAndBindings.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 104: **possible write() call**
  ```
  f.write("Runner_1128_FixToolbarAndBindings - Start\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1129_IntakeLoadGuard.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 56: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {message}\n")
  ```
- Zeile 112: **possible write() call**
  ```
  f.write("Runner_1129_IntakeLoadGuard - Start\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1130_IntakeDiagnose.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 48: **possible write() call**
  ```
  f.write(f"IntakeDiagnose {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1131_FixIntakeToolbar.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(msg.rstrip()+"\n")
  ```
- Zeile 66: **possible write() call**
  ```
  f.write("Runner_1131_FixIntakeToolbar - Start\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1132_FixGuardParent.py`
- Zeile 25: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(text.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1132_FixIntakeActions.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 52: **possible write() call**
  ```
  f_out.write(f_in.read())
  ```
- Zeile 146: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1133_IntakeAutoHeal.py`
- Zeile 28: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 162: **possible write() call**
  ```
  f.write("Runner_1133_IntakeAutoHeal - Start\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1134_IntakePathFix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1135_ModulesInitAndDiagnose.py`
- Zeile 26: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 46: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 67: **possible write() call**
  ```
  f.write(f"Runner_1135_ModulesInitAndDiagnose {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1136_FixMissingRepairButton.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(msg.rstrip() + "\n")
  ```
- Zeile 95: **possible write() call**
  ```
  f.write("[CRASH]\n" + traceback.format_exc())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1137_IntakeLoadFix.py`
- Zeile 28: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 58: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 204: **possible write() call**
  ```
  def logrep(s: str): buf.write(s + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1137a_IntakeLoadFix.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(msg.rstrip()+"\n")
  ```
- Zeile 52: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 157: **possible write() call**
  ```
  f.write("[CRASH]\n"+traceback.format_exc())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1138_IntakeLoadFix2.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1139_IntakeFrameRepair.py`
- Zeile 15: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 68: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1140_IntakeFinalFix.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 48: **possible write() call**
  ```
  sys.stdout.write(line)
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 60: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 241: **possible write() call**
  ```
  rep.write("OK: Patch angewendet.\n")
  ```
- Zeile 242: **possible write() call**
  ```
  rep.write(f"Backup: {backup}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1141_IntakeDefuse.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 64: **possible write() call**
  ```
  f.write(f"[{prefix}] {ts} {message}\\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1142_DefuseSafe.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1143_IntakeToolbarGuardFix.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1143b_IntakeToolbarGuardFix_Safe.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 42: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1144_ReplaceIntakeSafe.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 433: **possible write() call**
  ```
  f.write(self.txt.get("1.0","end-1c"))
  ```
- Zeile 548: **possible write() call**
  ```
  f.write(FIXED)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1145_IntakeAudit.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(line.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1146_FeatureGapAudit.py`
- Zeile 29: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(line.rstrip() + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1148_ImproveDetection.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(line.rstrip() + "\n")
  ```
- Zeile 199: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1148b_ForceDetectionFix.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 99: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1149_TablePopulate.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 207: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1150_DetectionFinalFix.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 96: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1151_AddPackSaveButton.py`
- Zeile 24: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 42: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 93: **possible write() call**
  ```
  zf.write(sub, arcname=sub.relative_to(root))
  ```
- Zeile 98: **possible write() call**
  ```
  zf.write(item, arcname=item.relative_to(root))
  ```
- Zeile 113: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1152_TableUX_Interactions.py`
- Zeile 26: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 281: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(src2)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1153_SmartDetect_AutoSave.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 39: **possible write() call**
  ```
  with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 98: **possible write() call**
  ```
  f.write(self.txt.get("1.0","end-1c"))
  ```
- Zeile 282: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1153d_RegexHyphenFix.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 42: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1153e_PathInitFix.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1153f_SafeDetectRegex.py`
- Zeile 23: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 52: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1153g_SafeRegexAllIntake.py`
- Zeile 26: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 55: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1153h_FixDetectAndRegex.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 43: **possible write() call**
  ```
  w.write(r.read())
  ```
- Zeile 52: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 218: **possible write() call**
  ```
  sys.stderr.write(f"[Syntax] {e}\n")
  ```
- Zeile 269: **possible write() call**
  ```
  w.write(r.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1153k_DetectGuard.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 154: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1154_AddDeleteButtons.py`
- Zeile 27: **possible write() call**
  ```
  #     with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 239: **possible write() call**
  ```
  #     io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1154b_AddDeleteButtons.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 251: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1154c_AddDeleteButtons.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  with io.open(REPORT, "a", encoding="utf-8", newline="\n") as f: f.write(s.rstrip()+"\n")
  ```
- Zeile 241: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1154d_FixIntakeToolbarAndGuard.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 66: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 228: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(src3)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1154g_FixIntakeButtonsAndGuard.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 61: **possible write() call**
  ```
  f.write(line.rstrip()+"\n")
  ```
- Zeile 160: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(src3)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1154h_FixMissingBuildUiDef.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 100: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(patched)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1155_IntakeBootDiag.py`
- Zeile 24: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 40: **possible write() call**
  ```
  f.write(f"[R1155] {ts} {msg}\n")
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 54: **possible write() call**
  ```
  writeln = lambda s="": out.write(s + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1156_AddInitAndBuildUI.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 190: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(src3)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1156c_FixTtkAndInitUI.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 206: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(src4)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1156d_TtkGlobalizeLocals.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 180: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(src2)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1156e_CombineInitAndTtk.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(s.rstrip()+"\n")
  ```
- Zeile 205: **possible write() call**
  ```
  io.open(MODFILE, "w", encoding="utf-8", newline="\n").write(src3)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1157_FixDetectPatterns.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 174: **possible write() call**
  ```
  f.write(new)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1158_UX_ToolbarLayout.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 199: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1158c_UX_ToolbarLayoutFix.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 142: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1161_DetectRegex_Hotfix.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 116: **possible write() call**
  ```
  f.write(new)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1162_DetectRegexScanner.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1163_DetectGuardFix.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 103: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1163b_DetectGuardFixSafe.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 39: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```
- Zeile 77: **possible write() call**
  ```
  with io.open(MOD, "w", encoding="utf-8", newline="\n") as f: f.write(new)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1163d_DetectGuardFixSafePlain.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 39: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```
- Zeile 96: **possible write() call**
  ```
  with io.open(MOD, "w", encoding="utf-8", newline="\n") as f: f.write(new)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1163e_DetectGuardFix_AST.py`
- Zeile 23: **possible write() call**
  ```
  with io.open(LOGF,"a",encoding="utf-8") as f: f.write(line)
  ```
- Zeile 83: **possible write() call**
  ```
  io.open(MOD,"w",encoding="utf-8",newline="\n").write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1163f_FixPyHeadRegex.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 54: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1163h2_FixPythonHeadRegex_SafePlain.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 42: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1163h3_FixPythonHeadRegex_DirectReplace.py`
- Zeile 15: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  with open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1163h4_FixPythonHeadRegex_LineSwap.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 41: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1163h_FixPythonHeadRegex_Safe.py`
- Zeile 15: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(f"[R1163h] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1164_ClearAlsoClearsExt.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 32: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(f"[R1164] {ts} {msg}\n")
  ```
- Zeile 87: **possible write() call**
  ```
  with io.open(MOD, "w", encoding="utf-8", newline="\n") as f: f.write(new)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1164b_OptionalConfirmOnClear.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(f"[R1164b] {ts} {msg}\n")
  ```
- Zeile 119: **possible write() call**
  ```
  with io.open(MOD, "w", encoding="utf-8", newline="\n") as f: f.write(new)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1164c_ClearExt_And_OptionalConfirm.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 88: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(f"[R1164c] {ts} {msg}\n")
  ```
- Zeile 138: **possible write() call**
  ```
  with io.open(MOD, "w", encoding="utf-8", newline="\n") as f: f.write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1164d_ClearExt_OptionalConfirm_Traversal.py`
- Zeile 83: **possible write() call**
  ```
  with io.open(LOGF,"a",encoding="utf-8") as f: f.write(f"[R1164d] {ts} {msg}\n")
  ```
- Zeile 116: **possible write() call**
  ```
  io.open(MOD,"w",encoding="utf-8",newline="\n").write(new)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1165_IntakeInitFix.py`
- Zeile 24: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 41: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1166_IntakeTTK_ScopeFix_and_Rules.py`
- Zeile 29: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 87: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1166b_IntakeScopeFix_SafeIndent.py`
- Zeile 29: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 87: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1166c_Intake_MinimalScopeFix.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 56: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1166d_Intake_IndentAndTTKFix.py`
- Zeile 32: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 88: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1166e_Intake_FinalFix.py`
- Zeile 33: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 91: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1166f_Intake_DeepRepair.py`
- Zeile 27: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 62: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1166g_Intake_SafeDedent.py`
- Zeile 28: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 56: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1166h_Intake_SafeDedent2.py`
- Zeile 26: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 54: **possible write() call**
  ```
  with io.open(LOGF, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1167a_Intake_SanityCheck.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 55: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1167b_GUIIntakePresenceCheck.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1167c_GUIRenderTrace.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1167d_GUIMountRefresher.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 59: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 92: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 99: **possible write() call**
  ```
  fw.write(fb.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1167e_RunnerExecSafeImport.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 46: **possible write() call**
  ```
  f.write((msg or "").rstrip() + "\\n")
  ```
- Zeile 59: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 69: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 100: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 108: **possible write() call**
  ```
  fw.write(fb.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1167f_RunnerExecSafeImport2.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 41: **possible write() call**
  ```
  f.write((msg or "").rstrip() + "\\n")
  ```
- Zeile 51: **possible write() call**
  ```
  f.write(f"[1167f {ts}] {msg}\n")
  ```
- Zeile 59: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 83: **possible write() call**
  ```
  open(TARGET, "w", encoding="utf-8", newline="").write(new_src)
  ```
- Zeile 88: **possible write() call**
  ```
  open(TARGET, "w", encoding="utf-8").write(open(bak, "r", encoding="utf-8").read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1167g_RunnerExecLogAppendSafe.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 47: **possible write() call**
  ```
  f.write((msg or "").rstrip() + "\\n")
  ```
- Zeile 59: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 69: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 89: **possible write() call**
  ```
  f.write(APPEND_BLOCK)
  ```
- Zeile 96: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1167h_IntakeErrDump.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 52: **possible write() call**
  ```
  f.write(err or "[leer]")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1167i_IntakeFix_CallModuleFunc.py`
- Zeile 10: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 25: **possible write() call**
  ```
  io.open(p, "w", encoding="utf-8", newline="\n").write(new)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1167j_IniDetectHelperPatch.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 61: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 71: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 111: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 118: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1170a_IntakeRegression.py`
- Zeile 25: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1170b_IntakeBindRepair.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 128: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 138: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 180: **possible write() call**
  ```
  open(TARGET, "w", encoding="utf-8", newline="\n").write(src)
  ```
- Zeile 184: **possible write() call**
  ```
  open(TARGET, "w", encoding="utf-8", newline="\n").write(open(bak, "r", encoding="utf-8").read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1170c_IntakeShortcutWire.py`
- Zeile 51: **possible write() call**
  ```
  f.write(f"[1170c {time.strftime('%Y-%m-%d %H:%M:%S')}] {m}\n")
  ```
- Zeile 57: **possible write() call**
  ```
  open(dst,"w",encoding="utf-8",newline="").write(open(path,"r",encoding="utf-8").read())
  ```
- Zeile 87: **possible write() call**
  ```
  open(TARGET,"w",encoding="utf-8",newline="\n").write(src)
  ```
- Zeile 91: **possible write() call**
  ```
  open(TARGET,"w",encoding="utf-8",newline="\n").write(open(bak,"r",encoding="utf-8").read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1170d_UXLayoutPolish.py`
- Zeile 87: **possible write() call**
  ```
  f.write(f"[1170d {time.strftime('%Y-%m-%d %H:%M:%S')}] {m}\n")
  ```
- Zeile 93: **possible write() call**
  ```
  open(dst,"w",encoding="utf-8",newline="").write(open(path,"r",encoding="utf-8").read())
  ```
- Zeile 120: **possible write() call**
  ```
  open(TARGET,"w",encoding="utf-8",newline="\n").write(src)
  ```
- Zeile 124: **possible write() call**
  ```
  open(TARGET,"w",encoding="utf-8",newline="\n").write(open(bak,"r",encoding="utf-8").read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1170e_IntakeLifecycleWire.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 56: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 102: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 109: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1171b_IntakeUXAndDetect.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 277: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 286: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 329: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 335: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1171c_IntakeDetectClean.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 187: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 196: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 253: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 260: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1171d_IntakeHelperIndentFix.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 42: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 51: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 124: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 130: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1171e_IntakeToolbarFix.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 47: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 101: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 108: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1171f_IntakeToolbarFix2.py`
- Zeile 24: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 50: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 125: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 132: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1171g_IntakeToolbarReflow.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 159: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 168: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 212: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 218: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1171h_IntakeHelperIndentSweep.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 46: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 117: **possible write() call**
  ```
  f.write(new_src)
  ```
- Zeile 124: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1171j_IntakeToolbarReflowTopLevel.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 146: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 155: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 266: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 270: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 277: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1171k_IntakeToolbarReflowExternalize.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 136: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 145: **possible write() call**
  ```
  fo.write(fi.read())
  ```
- Zeile 170: **possible write() call**
  ```
  f.write("# package for external helpers\n")
  ```
- Zeile 172: **possible write() call**
  ```
  f.write(HELPER_CODE)
  ```
- Zeile 232: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 240: **possible write() call**
  ```
  fo.write(fi.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1171m_IntakeToolbarReflowFix.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1171n_IntakeSyntaxRebuilder.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  with open(LOG, "a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1171p_IntakeIndentHeal.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  with io.open(LOG, "a", encoding="utf-8") as f: f.write(line+"\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1171q_IntakeCleanAndExternalize.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 64: **possible write() call**
  ```
  with LOG.open("a", encoding="utf-8") as f: f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1171q_IntakeToolbarReflowSafe.py`
- Zeile 15: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  with io.open(LOG, "a", encoding="utf-8") as f: f.write(line+"\n")
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(dedent(open(os.path.join(os.path.dirname(__file__), "..", "modules", "snippets", "intake_toolbar_reflow_helper.py"), "r", encoding="utf-8").read()
  ```
- Zeile 84: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1171r_IntakeUILayoutTidy.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 77: **possible write() call**
  ```
  with io.open(LOG, "a", encoding="utf-8") as f: f.write(line+"\n")
  ```
- Zeile 94: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1172_IntakeTabGuard.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 39: **possible write() call**
  ```
  with open(LOG, "a", encoding="utf-8") as f: f.write(line)
  ```
- Zeile 103: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1173_IntakeUILayoutFix.py`
- Zeile 25: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 208: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1173b_IntakeUILayoutFix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 174: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1173c_IntakeTTKImportFix.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 129: **possible write() call**
  ```
  f.write(new)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1173d_IntakeFallbackReturnFix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 84: **possible write() call**
  ```
  f.write(orig)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1173e_MainGuiTabHelper.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 31: **possible write() call**
  ```
  def write(p,s): io.open(p, "w", encoding="utf-8").write(s)
  ```
- Zeile 66: **possible write() call**
  ```
  _f.write("\n[IntakeTab] Fehler beim Erzeugen von IntakeFrame:\n")
  ```
- Zeile 67: **possible write() call**
  ```
  _f.write(traceback.format_exc())
  ```
- Zeile 89: **possible write() call**
  ```
  _f.write("\n[IntakeTab] Unbekannter Fehler beim Einhaengen des Tabs:\n")
  ```
- Zeile 90: **possible write() call**
  ```
  _f.write(traceback.format_exc())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1173f_IntakeTabSafeAdd.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 31: **possible write() call**
  ```
  f.write(f"[1173f] {msg}\n")
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 75: **possible write() call**
  ```
  _f.write("[1173f] " + _msg + "\n")
  ```
- Zeile 84: **possible write() call**
  ```
  _f.write("[1173f] Intake-Load-ERR:\n" + "".join(traceback.format_exception(type(ex), ex, ex.__traceback__)) + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1173g_IntakeTabSmoke.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1173h_MainGuiHelpersOrderFix.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  io.open(path, "w", encoding="utf-8", newline="\n").write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1173i_MainGuiHeadDedent.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 30: **possible write() call**
  ```
  def W(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1173k_MainGuiCallRelocate.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(f"[1173k {ts}] {msg}\n")
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1173m_MainGuiIntakeWireFix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 57: **possible write() call**
  ```
  f.write(f"[1173m {ts}] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1173p_MainGuiIntakeWireForce.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(f"[1173p {ts}] {msg}\n")
  ```
- Zeile 57: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1173z_IntakeSmoke.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174a_MainGuiIntakeHelpersFix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 80: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 100: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174aa_IntakeTabCleanser.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 64: **possible write() call**
  ```
  f.write("[1174aa] Intake mount failed: %r\n" % (e,))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174b_MainGuiIntakeHelpersFix.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[1174b {ts}] {msg}\n")
  ```
- Zeile 40: **possible write() call**
  ```
  def write(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)
  ```
- Zeile 72: **possible write() call**
  ```
  f.write("[1174b] IntakeFrame-Fehler:\\n" + "".join(traceback.format_exception(type(ex), ex, ex.__traceback__)) + "\\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174c_MainGuiIntakeHelpersFix.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174d_MainGuiIntakeCleanup.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 32: **possible write() call**
  ```
  f.write(f"[1174d {ts}] {msg}\n")
  ```
- Zeile 42: **possible write() call**
  ```
  def write(path, data): open(path, "w", encoding="utf-8", newline="\n").write(data)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174e_MainGuiIntakeCleanup.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 47: **possible write() call**
  ```
  with open(p, "w", encoding="utf-8", newline="\n") as f: f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174f_MainGuiIntakeCleanup.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174g_IntakeClassRebind.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write("[1174g] " + msg + "\n")
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174g_IntakePostBuildFix.py`
- Zeile 10: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 97: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174g_MainGuiReorderFix.py`
- Zeile 20: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174h_IntakeHardReset.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 132: **possible write() call**
  ```
  f.write(f"[1174h] {ts} {msg}\n")
  ```
- Zeile 156: **possible write() call**
  ```
  f.write(SAFE_SRC)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174i_IntakeRestoreSmart.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(f"[1174i] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174j_IntakeRestoreSmartFix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(f"[1174j] {ts} {msg}\n")
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(data)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174k_IntakeFeatureRestore.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(f"[1174k {time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174m_IntakeFrameRebuild.py`
- Zeile 13: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174n_IntakeHotFix_UIInit.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174p_IntakeCtorFix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(f"[1174p {ts}] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174r_IntakeTabRebind.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174s_MainGuiSmoke.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 25: **possible write() call**
  ```
  f.write(f"[1174s {ts}] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174t_IntakeTabRebindFix.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 26: **possible write() call**
  ```
  with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174u_MainGuiRestoreLast.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174v_IntakeTabHarden.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 26: **possible write() call**
  ```
  f.write(f"[1174v {ts}] {msg}\n")
  ```
- Zeile 29: **possible write() call**
  ```
  def wr(p,s): io.open(p, "w", encoding="utf-8", newline="").write(s)
  ```
- Zeile 62: **possible write() call**
  ```
  "                _f.write(f\"[1174v {time.strftime('%Y-%m-%d %H:%M:%S')}] Direct mount failed: {e!r}\\n\")\n"
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174w_MainSyntaxSmoke.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 26: **possible write() call**
  ```
  f.write(f"[1174w {ts}] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174x_IntakeRevive.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **mentions atomic write**
  ```
  def atomic_write(dst: Path, content: str):
  ```
- Zeile 111: **possible write() call**
  ```
  tmp.write(fixed)
  ```
- Zeile 119: **mentions atomic write**
  ```
  atomic_write(target, fixed)
  ```
- Zeile 147: **possible write() call**
  ```
  f.write("\\n[1174x] Importfehler IntakeFrame: %r\\n" % (e,))
  ```
- Zeile 158: **possible write() call**
  ```
  f.write("\\n[1174x] Aufbaufehler IntakeFrame: %r\\n" % (e,))
  ```
- Zeile 180: **mentions atomic write**
  ```
  atomic_write(main_file, src)
  ```
- Zeile 199: **mentions atomic write**
  ```
  atomic_write(target, fixed)
  ```
- Zeile 219: **possible write() call**
  ```
  f.write("\n[1174x] Runner-Fehler: %r\n" % (e,))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174y_DebugPathFix.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174z_DebugPathFix.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1174z_IntakeTabRestoreSafe.py`
- Zeile 13: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 76: **possible write() call**
  ```
  f.write("[1174z] Intake direct mount failed: %r\n" % (e,))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1175a_MainGuiIntakeHelperFix.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 76: **possible write() call**
  ```
  f.write("\\n[INTAKE_MOUNT_ERROR]\\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1175b_IntakeApiSoftGuard.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 52: **possible write() call**
  ```
  f.write("\n[INTAKE_API_WRAPPER_ERROR]\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1175d_MainEntryGuard.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 32: **possible write() call**
  ```
  f.write("\n[MAIN_START_ERROR]\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1175e_MainIntakeShim.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 27: **possible write() call**
  ```
  f.write(f"\n[{tag}] {type(e).__name__}: {e}\n")
  ```
- Zeile 96: **possible write() call**
  ```
  b.write(read(MAIN))
  ```
- Zeile 98: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1175f_IntakeShimFix.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1175g_ModulesPackageFix.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 27: **possible write() call**
  ```
  f.write("# modules package marker\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1175h_IntakeCleanRestore.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 25: **mentions atomic write**
  ```
  def _write_atomic(path: Path, data: str) -> None:
  ```
- Zeile 28: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 55: **possible write() call**
  ```
  f.write(f"[INTAKE] {msg}\n")
  ```
- Zeile 134: **possible write() call**
  ```
  f.write(self.txt.get("1.0","end-1c"))
  ```
- Zeile 183: **mentions atomic write**
  ```
  _write_atomic(MOD, NEW)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1175i_RemoveFakeNbAdd.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1175m_IntakeResurrect.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 71: **possible write() call**
  ```
  f.write(new)
  ```
- Zeile 106: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1175n_FixPyCallAndCleanMain.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 32: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 63: **possible write() call**
  ```
  f.write(new)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1175q_IntakeHardRestore.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 135: **possible write() call**
  ```
  f.write(BASIS_CODE)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1176a_IntakeShimUpgrade.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 52: **possible write() call**
  ```
  f.write("[IntakeShim %s] Mount-Fehler: %r\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), _e))
  ```
- Zeile 65: **possible write() call**
  ```
  fdst.write(fsrc.read())
  ```
- Zeile 144: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 155: **possible write() call**
  ```
  f.write(fb.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1176b_FixIntakeMount.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[1176b {time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
  ```
- Zeile 44: **possible write() call**
  ```
  w.write(r.read())
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 125: **possible write() call**
  ```
  w.write(r.read())
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1176c_GatePanelIntegration.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(f"[1176c {time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
  ```
- Zeile 45: **possible write() call**
  ```
  w.write(r.read())
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 190: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1176d_FixShimName.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(f"[1176d {time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
  ```
- Zeile 39: **possible write() call**
  ```
  w.write(r.read())
  ```
- Zeile 59: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1176d_IntakeShimHotfix.py`
- Zeile 11: **possible write() call**
  ```
  f.write(f"[1176d {ts}] {msg}\n")
  ```
- Zeile 19: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(f"[GATE { _ts() }] {msg}\n")
  ```
- Zeile 127: **possible write() call**
  ```
  f.write("[INTAKE_SHIM] Import/Build-Fehler:\\n" + buf.getvalue() + "\\n")
  ```
- Zeile 159: **possible write() call**
  ```
  f.write("[MAIN] _safe_add_intake_tab Exception\\n"+buf.getvalue()+"\\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177a_IntakeMountAdapter.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 67: **possible write() call**
  ```
  f.write(f"[{ts}] {msg}\n")
  ```
- Zeile 159: **possible write() call**
  ```
  f.write(f"[{now_ts()}] {msg}\n")
  ```
- Zeile 169: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 177: **possible write() call**
  ```
  out.write(src.read())
  ```
- Zeile 229: **possible write() call**
  ```
  src += "            f.write(f\"[{ts}] {msg}\\n\")\n"
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177a_IntakeMountAdapter_Hotfix.py`
- Zeile 15: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(f"[{ts}] [1177a-Hotfix] {msg}\n")
  ```
- Zeile 37: **possible write() call**
  ```
  out.write(src.read())
  ```
- Zeile 50: **possible write() call**
  ```
  open(MAIN, "w", encoding="utf-8").write(fixed)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177b_DevIntakeRestore.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 55: **possible write() call**
  ```
  f.write(f"[{ts}] [DevIntake] {msg}\\n")
  ```
- Zeile 276: **possible write() call**
  ```
  f.write(f"[{_ts()}] [R1177b_Dev] {msg}\n")
  ```
- Zeile 289: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177b_IntakeRestore.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177b] {msg}\n")
  ```
- Zeile 45: **possible write() call**
  ```
  with open(path, "rb") as s, open(bak, "wb") as d: d.write(s.read())
  ```
- Zeile 47: **possible write() call**
  ```
  with open(path, "w", encoding="utf-8") as f: f.write(content)
  ```
- Zeile 74: **possible write() call**
  ```
  f.write(f"[{ts}] [IntakeShim] {msg}\n")
  ```
- Zeile 169: **possible write() call**
  ```
  f.write(f"[{ts}] [Intake] {msg}\n")
  ```
- Zeile 413: **possible write() call**
  ```
  f.write(f"[{ts}] [FileOps] {msg}\n")
  ```
- Zeile 431: **possible write() call**
  ```
  with open(self.path, "w", encoding="utf-8") as f: f.write("[]")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177c_IntakeRecover.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177c] {msg}\n")
  ```
- Zeile 117: **possible write() call**
  ```
  f.write(text)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177d_DevIntakeButtons.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177d] {msg}\n")
  ```
- Zeile 105: **possible write() call**
  ```
  f.write(f"[{ts}] [DevIntake] {_msg}\\n")
  ```
- Zeile 272: **possible write() call**
  ```
  with open(p, "w", encoding="utf-8") as f: f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177e_DevToolbarFix.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177e] {msg}\n")
  ```
- Zeile 159: **possible write() call**
  ```
  f.write(NEW_SNIPPET)
  ```
- Zeile 182: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177f_DevIntakeVisualFix.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177f] {msg}\n")
  ```
- Zeile 141: **possible write() call**
  ```
  f.write(NEW_SNIPPET)
  ```
- Zeile 175: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177g_DevIntakeCoreRebuild.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177g] {msg}\n")
  ```
- Zeile 67: **possible write() call**
  ```
  f.write(f"[{ts}] [DevIntake] {msg}\\n")
  ```
- Zeile 301: **possible write() call**
  ```
  f.write(PAYLOAD)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177h_IntakeImportCheck.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177h] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177i_ImportPathFix.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177i] {msg}\n")
  ```
- Zeile 103: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177j_IntakeShimHardFix.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177j] {msg}\n")
  ```
- Zeile 72: **possible write() call**
  ```
  f.write(f"[{ts}] {_TAG} {msg}\n")
  ```
- Zeile 154: **possible write() call**
  ```
  f.write(PAYLOAD)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177k_RuntimeImportBridge.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177k] {msg}\n")
  ```
- Zeile 67: **possible write() call**
  ```
  f.write(f"[{ts}] {_TAG} {msg}\n")
  ```
- Zeile 171: **possible write() call**
  ```
  f.write(PAYLOAD)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177l_CleanTabMount.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177l] {msg}\n")
  ```
- Zeile 197: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177m_FixMainAndGate.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(f"[R1177m] {ts} {msg}\n")
  ```
- Zeile 45: **possible write() call**
  ```
  open(dst, "w", encoding="utf-8").write(data)
  ```
- Zeile 137: **possible write() call**
  ```
  open(MAIN, "w", encoding="utf-8").write(src)
  ```
- Zeile 180: **possible write() call**
  ```
  "                f.write('[R1177m] Gate safe mount error: %s\\n' % e)\n"
  ```
- Zeile 189: **possible write() call**
  ```
  open(GATE, "w", encoding="utf-8").write(src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177m_MainGuiFix.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177m] {msg}\n")
  ```
- Zeile 140: **possible write() call**
  ```
  with open(TARGET, "w", encoding="utf-8") as f: f.write(src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1177n_GatePanelUpdate.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(f"[{ts()}] [R1177n] {msg}\n")
  ```
- Zeile 75: **possible write() call**
  ```
  with open(TARGET, "w", encoding="utf-8") as f: f.write(src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1178i_ImportPathFix.py`
- Zeile 10: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 23: **possible write() call**
  ```
  f.write("[R1178i] " + msg + "\n")
  ```
- Zeile 49: **possible write() call**
  ```
  f.write("[R1178i] IntakeMountERR: %s\\n" % e)
  ```
- Zeile 70: **possible write() call**
  ```
  f.write(new)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1178j_FixDevIntake.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(f"[R1178j] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1178m_FixGatePanelAndLaunch.py`
- Zeile 10: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(f"[GATE] {strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```
- Zeile 89: **possible write() call**
  ```
  f.write("[R1178m] " + msg + "\n")
  ```
- Zeile 96: **possible write() call**
  ```
  f.write(NEW)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1178o_FixGatePanelAndLaunch.py`
- Zeile 10: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 27: **possible write() call**
  ```
  f.write(f"[R1178o] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1180_StartFix.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 81: **possible write() call**
  ```
  f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [1180] Safe starters written.\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1181_IntakeDeDuplicate.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(f"[R1181] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 97: **possible write() call**
  ```
  f.write("[Shim] Intake mount failed:\\n")
  ```
- Zeile 120: **possible write() call**
  ```
  open(SHIM, "w", encoding="utf-8").write(src)
  ```
- Zeile 162: **possible write() call**
  ```
  open(MAIN, "w", encoding="utf-8").write(src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1181b_MainGuiIndentFix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(f"[R1181b] {ts} {msg}\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 73: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1181c_MainGuiIndentFix2.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[R1181c] {ts} {msg}\n")
  ```
- Zeile 48: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 119: **possible write() call**
  ```
  f.write(fixed)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1181d_MainGuiTryFix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(f"[R1181d] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```
- Zeile 61: **possible write() call**
  ```
  f.write(src)
  ```
- Zeile 85: **possible write() call**
  ```
  f.write(new_src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1182a_DevIntakePro_Clean.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{pfx}] {msg}\n")
  ```
- Zeile 269: **possible write() call**
  ```
  z.write(p, p.relative_to(root))
  ```
- Zeile 303: **possible write() call**
  ```
  f.write(f"[R1182a] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1183_DevIntakeUX.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 39: **uses configparser (inspect for write/save)**
  ```
  import os, sys, time, shutil, zipfile, traceback, subprocess, configparser
  ```
- Zeile 51: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{tag}] {msg}\n")
  ```
- Zeile 103: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 115: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 122: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 420: **possible write() call**
  ```
  z.write(p, p.relative_to(root))
  ```
- Zeile 457: **possible write() call**
  ```
  f.write(f"[R1183] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1183c_DevIntakeUX_DetectFix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 41: **uses configparser (inspect for write/save)**
  ```
  import os, sys, time, shutil, zipfile, traceback, subprocess, configparser, re
  ```
- Zeile 53: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{tag}] {msg}\n")
  ```
- Zeile 114: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 126: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 133: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 398: **possible write() call**
  ```
  if p.is_file(): z.write(p, p.relative_to(root))
  ```
- Zeile 432: **possible write() call**
  ```
  f.write(f"[R1183c] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1184_DevIntakeUX_Polish.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(f"[R1184] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```
- Zeile 38: **uses configparser (inspect for write/save)**
  ```
  import os, sys, time, shutil, zipfile, traceback, subprocess, configparser, re
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{tag}] {msg}\n")
  ```
- Zeile 115: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser(); p = Path(os.getcwd())/INI_FILE
  ```
- Zeile 122: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 130: **possible write() call**
  ```
  with open(Path(os.getcwd())/INI_FILE, "w", encoding="utf-8", newline="\n") as f: cfg.write(f)
  ```
- Zeile 400: **possible write() call**
  ```
  if p.is_file(): z.write(p, p.relative_to(root))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1185_DevIntakeLEDs_Detect2.py`
- Zeile 21: **possible write() call**
  ```
  #         f.write(f"[R1185] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```
- Zeile 25: **uses configparser (inspect for write/save)**
  ```
  # import os, sys, time, shutil, zipfile, traceback, subprocess, configparser, re
  ```
- Zeile 37: **possible write() call**
  ```
  #             f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{tag}] {msg}\n")
  ```
- Zeile 163: **uses configparser (inspect for write/save)**
  ```
  #         cfg = configparser.ConfigParser(); p = Path(os.getcwd())/INI_FILE
  ```
- Zeile 170: **uses configparser (inspect for write/save)**
  ```
  #             cfg = configparser.ConfigParser()
  ```
- Zeile 178: **possible write() call**
  ```
  #             with open(Path(os.getcwd())/INI_FILE, "w", encoding="utf-8", newline="\n") as f: cfg.write(f)
  ```
- Zeile 483: **possible write() call**
  ```
  #                     if p.is_file(): z.write(p, p.relative_to(root))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1185b_DevIntakeLEDs_Detect2Fix.py`
- Zeile 15: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(f"[R1185b] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1186_IntakeUX_FixDetectAndUX.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 27: **possible write() call**
  ```
  f.write(f"[R1186] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1187_IntakeLEDs_Add.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 28: **possible write() call**
  ```
  f.write(f"[R1187] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1188_IntakeLEDs_DetectHardening.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 122: **possible write() call**
  ```
  f.write(out)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1189_IntakeRepairAndLEDsFix.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 28: **possible write() call**
  ```
  f.write(f"[R1189] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1190_DevIntake_Install.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 30: **possible write() call**
  ```
  f.write(f"[R1190] {time.strftime('%Y-%m-%d %H:%M:%S')} {tag} {msg}\n")
  ```
- Zeile 50: **uses configparser (inspect for write/save)**
  ```
  import os, sys, time, zipfile, traceback, configparser, subprocess, re
  ```
- Zeile 61: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{tag}] {msg}\n")
  ```
- Zeile 171: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser(); p = Path(os.getcwd())/INI_FILE
  ```
- Zeile 182: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 191: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 562: **possible write() call**
  ```
  z.write(p, p.relative_to(root))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1191_DevIntake_CleanInstall.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 23: **uses configparser (inspect for write/save)**
  ```
  import os, sys, time, zipfile, traceback, configparser, subprocess, re
  ```
- Zeile 34: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{tag}] {msg}\n")
  ```
- Zeile 126: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser(); p = Path(os.getcwd())/INI_FILE
  ```
- Zeile 135: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 144: **possible write() call**
  ```
  cfg.write(f)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1192_DevIntake_UIRefine.py`
- Zeile 8: **uses configparser (inspect for write/save)**
  ```
  import sys, time, traceback, configparser, subprocess, re, zipfile
  ```
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(f"[DevIntake] {time.strftime('%Y-%m-%d %H:%M:%S')} [{tag}] {msg}\n")
  ```
- Zeile 132: **uses configparser (inspect for write/save)**
  ```
  c=configparser.ConfigParser(); c.read(p, encoding="utf-8")
  ```
- Zeile 139: **uses configparser (inspect for write/save)**
  ```
  c=configparser.ConfigParser()
  ```
- Zeile 150: **possible write() call**
  ```
  with (Path.cwd()/INI).open("w",encoding="utf-8",newline="\n") as f: c.write(f)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1193_DevIntake_FixDetectAndInstall.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **uses configparser (inspect for write/save)**
  ```
  import time, re, configparser, traceback
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(f"[DevIntake] {ts} [{tag}] {msg}\n")
  ```
- Zeile 116: **uses configparser (inspect for write/save)**
  ```
  c=configparser.ConfigParser(); c.read(p, encoding="utf-8")
  ```
- Zeile 122: **uses configparser (inspect for write/save)**
  ```
  c=configparser.ConfigParser()
  ```
- Zeile 132: **possible write() call**
  ```
  c.write(f)
  ```
- Zeile 383: **possible write() call**
  ```
  if p.is_file(): zp.write(p, p.relative_to(tgt))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1193_IntakeDetectUpgrade.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1194_DevIntake_UIArrange.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(f"[DevIntake] {ts} [{tag}] {msg}\n")
  ```
- Zeile 322: **possible write() call**
  ```
  if p.is_file(): zp.write(p, p.relative_to(tgt))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1194_LEDBackgroundFix.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1195_DevIntake_UISortPolish.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(f"[DevIntake] {ts} [{tag}] {msg}\n")
  ```
- Zeile 360: **possible write() call**
  ```
  if p.is_file(): zp.write(p, p.relative_to(tgt))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1196_DevIntake_Apply.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 56: **possible write() call**
  ```
  f.write(f"[DevIntake] {ts} [{tag}] {msg}\n")
  ```
- Zeile 382: **possible write() call**
  ```
  if p.is_file(): zp.write(p, p.relative_to(tgt))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1198_IntakeLedFix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 35: **possible write() call**
  ```
  f.write(f"[R1198] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1199_FixSaveAndLEDs.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[R1199] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1199_IntakeHotfix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(f"[R1199] {ts} {msg}\n")
  ```
- Zeile 213: **possible write() call**
  ```
  f.write(f"[R1199] {ts} ERROR {e}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1200_DevIntake_AutoDetectAndPolish.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1201_DevIntake_Stabilize.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(f"{TAG} {ts} {line}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1202_FixIndentationPath.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 32: **possible write() call**
  ```
  f.write(f"[R1202] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1203_DevIntake_Recovery.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 41: **possible write() call**
  ```
  f.write(s+"\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1204_FixIndent_AutoDetect_SaveAs.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1205_FixIntakeIndentAndLEDs.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  fp.write(f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} {TAG} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1206_FixIntakeCore.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 37: **possible write() call**
  ```
  f.write(f"[R1206] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1207_FixIntakeCoreSafe.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1208_FixRegexEscape.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(f"[R1208] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1209_IntakePathFinalFix.py`
- Zeile 17: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(f"[R1209] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1210_DevIntake_FixCoreAndUX.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1212_FixIntakeCoreStable.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1213_FixIntakeCoreStable.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1214_FixIntake_Final.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1215_FixIntakeCoreFinal.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(f"[R1215] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1216_FixIntakeCore_Final.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(f"[R1216] {ts} {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1218_FixIntakeCoreSuperSafe.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[R1218] {ts} {msg}\n")
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(txt)
  ```
- Zeile 68: **possible write() call**
  ```
  f.write(f"[DevIntake] {ts} [{tag}] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1218_FixIntake_NewlineSafe.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 28: **possible write() call**
  ```
  LOG.open("a", encoding="utf-8", newline="\n").write(f"[R1218] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1220_SyntaxGate_AllModules.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 25: **possible write() call**
  ```
  LOG.open("a", encoding="utf-8", newline="\n").write(f"[R1220] {line}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1221_IntakeCore_Addons.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(f"[INTAKE] [{tag}] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
  ```
- Zeile 156: **possible write() call**
  ```
  LOG.open("a", encoding="utf-8", newline="\n").write(f"[R1221] {msg}\n")
  ```
- Zeile 189: **possible write() call**
  ```
  from pathlib import Path; Path(__file__).resolve().parents[1].joinpath("debug_output.txt").open("a", encoding="utf-8", newline="\\n").write(f"[R1221] APPLY_ERROR: {_e!r}\\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1225_IntakeCore_RepairAndIntegrate.py`
- Zeile 13: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  f.write(f"[R1225] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1230_RestoreIntakeFromBackup.py`
- Zeile 13: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 27: **possible write() call**
  ```
  LOG.open("a", encoding="utf-8", newline="\n").write(f"[R1230] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1231_Intake_MinimalFixes.py`
- Zeile 13: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 27: **possible write() call**
  ```
  LOG.open("a", encoding="utf-8", newline="\n").write(f"[R1231] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1234_IntakeCore_RepairIntegrate.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(f"[R1234] {ts} {msg}\n")
  ```
- Zeile 186: **possible write() call**
  ```
  (Path(__file__).resolve().parents[1]/"debug_output.txt").open("a", encoding="utf-8").write(
  ```
- Zeile 213: **possible write() call**
  ```
  (Path(__file__).resolve().parents[1]/"debug_output.txt").open("a", encoding="utf-8").write(msg+"\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1241_Intake_AllInOne.py`
- Zeile 25: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1242_Intake_RepairAndIntegrate.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(f"[R1242] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1244_SyntaxRecovery_Final.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 52: **possible write() call**
  ```
  sys.stderr.write(f"[LOG-FAIL] {tag}: {msg}\n")
  ```
- Zeile 99: **possible write() call**
  ```
  f.write(line)
  ```
- Zeile 101: **possible write() call**
  ```
  sys.stderr.write(f"[INTAKE-LOG-FAIL] {tag}: {msg} ({ex})\\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1244b_SyntaxRecovery_Final.py`
- Zeile 24: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 40: **possible write() call**
  ```
  f.write(f"[{ts}] [R1244b:{tag}] {msg}\n")
  ```
- Zeile 80: **possible write() call**
  ```
  f.write(line)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1245_IntakeSyntaxResurrection.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(f"[{ts}] [R1245:{tag}] {msg}\n")
  ```
- Zeile 85: **possible write() call**
  ```
  '            f.write(line)\n'
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1246_IntakeCodePurge.py`
- Zeile 34: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(f"[{ts}] [R1246:{tag}] {msg}\n")
  ```
- Zeile 91: **possible write() call**
  ```
  '            f.write(line)\n'
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1247_WriteTextFixer.py`
- Zeile 29: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(f"[{ts}] [R1247:{tag}] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1248_IntakeSyntaxRescue.py`
- Zeile 22: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 38: **possible write() call**
  ```
  f.write(f"[{ts}] [R1248:{tag}] {msg}\n")
  ```
- Zeile 74: **possible write() call**
  ```
  f.write(f"[DevIntake] {ts} [{tag}] {msg}\\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1249_IntakeHardRestore.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[R1249] {ts} {msg}\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 75: **possible write() call**
  ```
  f.write(f"[DevIntake] {ts} [{tag}] {msg}\\n")
  ```
- Zeile 130: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1250_MasterRulesPersist.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(f"[{ts}] [R1250:{tag}] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1251_SanityGateDaemon.py`
- Zeile 28: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(f"[{ts}] [R1251:{tag}] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1257_AddCmdSupport.py`
- Zeile 27: **possible write() call**
  ```
  f.write(f"[{ts}] [R1257:{tag}] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1258_IntakeRebuildFinal.py`
- Zeile 23: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 39: **possible write() call**
  ```
  f.write(f"[R1258] {ts} {msg}\n")
  ```
- Zeile 55: **possible write() call**
  ```
  f.write(data)
  ```
- Zeile 80: **possible write() call**
  ```
  f.write(f"[DevIntake] {ts} [{tag}] {msg}\\n")
  ```
- Zeile 146: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1259_IntakeRegexRebuild.py`
- Zeile 21: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(f"[R1259:{tag}] {ts} {msg}\n")
  ```
- Zeile 61: **possible write() call**
  ```
  f.write(s)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1260_IntakeRegexFinalFix.py`
- Zeile 18: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 40: **possible write() call**
  ```
  f.write(f"[R1260:{tag}] {ts} {msg}\n")
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1262_IntakeRestoreFromBackups.py`
- Zeile 20: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 49: **possible write() call**
  ```
  f.write(f"[R1262:{tag}] {ts} {msg}\n")
  ```
- Zeile 93: **possible write() call**
  ```
  '            f.write(f"[DevIntake] {ts} [{tag}] {msg}\\n")\n'
  ```
- Zeile 106: **possible write() call**
  ```
  # p.write_text(..., newline="\n") -> open(..., newline="\n").write(...)
  ```
- Zeile 113: **possible write() call**
  ```
  return f'with {obj}.open("w", encoding="utf-8", newline="\\n") as __f: __f.write({content})'
  ```
- Zeile 220: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1263_IntakeBackupDeepScan.py`
- Zeile 27: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 45: **possible write() call**
  ```
  f.write(f"[R1263:{tag}] {ts} {msg}\n")
  ```
- Zeile 128: **possible write() call**
  ```
  '            f.write(f"[DevIntake] {ts} [{tag}] {msg}\\n")\n'
  ```
- Zeile 141: **possible write() call**
  ```
  p.write_text(..., newline="\\n") -> with p.open("w", newline="\\n") as f: f.write(...)
  ```
- Zeile 151: **possible write() call**
  ```
  return f'with {obj}.open("w", encoding={enc}, newline="\\n") as __f: __f.write({content})'
  ```
- Zeile 252: **possible write() call**
  ```
  f.write(src)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1264.py`
- Zeile 24: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 42: **possible write() call**
  ```
  f.write(f"[R1264:{tag}] {ts} {msg}\n")
  ```
- Zeile 79: **possible write() call**
  ```
  '            f.write(f"[DevIntake] {ts} [{tag}] {msg}\\n")\n'
  ```
- Zeile 95: **possible write() call**
  ```
  return f'with {obj}.open("w", encoding={enc}, newline="\\n") as __f: __f.write({content})'
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1265.py`
- Zeile 5: **uses configparser (inspect for write/save)**
  ```
  import sys, time, shutil, ast, configparser
  ```
- Zeile 14: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 31: **possible write() call**
  ```
  f.write(f"[R1265] {ts} {msg}\n")
  ```
- Zeile 43: **uses configparser (inspect for write/save)**
  ```
  import configparser, json, os, time, re, traceback
  ```
- Zeile 54: **possible write() call**
  ```
  f.write(f"[DevIntake] {ts} [{tag}] {msg}\\n")
  ```
- Zeile 78: **uses configparser (inspect for write/save)**
  ```
  def _load_ini() -> configparser.ConfigParser:
  ```
- Zeile 79: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 91: **uses configparser (inspect for write/save)**
  ```
  def _save_ini(cfg: configparser.ConfigParser) -> None:
  ```
- Zeile 93: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 158: **possible write() call**
  ```
  f.write(txt)
  ```
- Zeile 422: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 432: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 439: **possible write() call**
  ```
  with INI.open("w", encoding="utf-8", newline="\n") as f: cfg.write(f)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_1293_UpdateIntakeMount.py`
- Zeile 19: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_901_Verify.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_902_LogTail.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_904_WarnSilence.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_905_FixToggle.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_913_Silence.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 34: **possible write() call**
  ```
  (inbox/f"{int(time.time())}.jsonl").open("a", encoding="utf-8").write(
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_914_NoPopup.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_915_QuietToggle.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_916_ScanUX.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_917_FixIndent.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_918_FixIndentMain.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_930_AllInOne.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 248: **possible write() call**
  ```
  if p.exists(): zipf.write(p, arcname=arc)
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_935_FixMainGUI.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 123: **possible write() call**
  ```
  (ROOT/"debug_output.txt").open("a", encoding="utf-8", errors="ignore").write(f"[MAIN] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_940_CoreKit.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_941_Preflight.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  (inbox/f"{int(time.time())}.jsonl").open("a", encoding="utf-8").write(json.dumps({"runner":"R941", **ev}, ensure_ascii=False)+"\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_942_NewModule.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_943_NewRunner.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 43: **possible write() call**
  ```
  (inbox/f"{{int(time.time())}}.jsonl").open("a", encoding="utf-8").write(json.dumps({{"runner":"R{RID}", **ev}}, ensure_ascii=False)+"\\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_944_AllGUIIntegrate.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_946_IntakeSmart.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_947_IntakeSelfTest.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_948_IntakeUX.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_949_TryFix.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_950.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_951_FixAgentStart.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_952_FixTryEverywhere.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_953_FixLoneTry.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_954_MainCleanup.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_960_BootFix.py`
- Zeile 26: **possible write() call**
  ```
  "            f.write(line)\n"
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_960_Menus.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_961_MenuFix.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_962_FixMainGUI.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 101: **possible write() call**
  ```
  .write(f"[MAIN] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_970_AllInOneInstall.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 27: **possible write() call**
  ```
  try: LOGF.open("a", encoding="utf-8", errors="ignore").write(f"[R970] {msg}\n")
  ```
- Zeile 449: **possible write() call**
  ```
  z.write(p, p.relative_to(ROOT))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_971_UnifyTabs.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 25: **possible write() call**
  ```
  try: LOG.open("a", encoding="utf-8", errors="ignore").write(f"[R971] {msg}\n")
  ```
- Zeile 447: **possible write() call**
  ```
  z.write(p, p.relative_to(ROOT))
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_972_SafePatch.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 25: **possible write() call**
  ```
  try: LOGF.open("a", encoding="utf-8", errors="ignore").write(f"[R972] {msg}\n")
  ```
- Zeile 29: **mentions atomic write**
  ```
  def write_text_atomic(target: Path, content: str) -> bool:
  ```
- Zeile 34: **mentions atomic write**
  ```
  os.replace(tmp, target)  # atomic if same volume
  ```
- Zeile 129: **mentions atomic write**
  ```
  # 2) Atomic append (read + write_atomic)
  ```
- Zeile 132: **mentions atomic write**
  ```
  if write_text_atomic(tgt, new):
  ```
- Zeile 135: **mentions atomic write**
  ```
  log(f"FAILED (atomic): {rel} - wird deferred")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_980_DevConsolidate.py`
- Zeile 11: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 26: **possible write() call**
  ```
  try: LOGF.open("a", encoding="utf-8", errors="ignore").write(f"[R980] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_981_IntakeUX.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 24: **possible write() call**
  ```
  try: LOGF.open("a", encoding="utf-8", errors="ignore").write(f"[R981] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_982_IntakeUIEnhance.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 26: **possible write() call**
  ```
  try: LOGF.open("a", encoding="utf-8", errors="ignore").write(f"[R982] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_983_IntakeFix.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 24: **possible write() call**
  ```
  try: LOGF.open("a", encoding="utf-8", errors="ignore").write(f"[R983] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_984_IntakeGeometryFix.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 25: **possible write() call**
  ```
  try: LOG.open("a", encoding="utf-8", errors="ignore").write(f"[R984] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_990_FixGUI.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 33: **possible write() call**
  ```
  DEBUG.open("a", encoding="utf-8", errors="ignore").write(f"[MAIN] {msg}\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_991_AllTabsIntegrate.py`
- Zeile 12: **possible write() call**
  ```
  f.write(msg + "\n")
  ```
- Zeile 27: **possible write() call**
  ```
  try: LOGF.open("a", encoding="utf-8", errors="ignore").write(f"[R991] {msg}\n")
  ```
- Zeile 184: **possible write() call**
  ```
  HIST.open("a", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False)+"\n")
  ```
- Zeile 325: **possible write() call**
  ```
  HIST.open("a", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False)+"\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_995_IntakeDetectorFix.py`
- Zeile 13: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_996_IntakeFix_And_Default.py`
- Zeile 16: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_997_Intake_BatAndDefault.py`
- Zeile 15: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_998_DefaultIntake.py`
- Zeile 13: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\Runner_998_IntakeBatDetector.py`
- Zeile 13: **possible write() call**
  ```
  f.write(msg + "\n")
  ```

### `D:\ShrimpDev\tools\Archiv\runner_guard.py`
- Zeile 31: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 33: **possible write() call**
  ```
  f.write("\n")
  ```

### `D:\ShrimpDev\tools\R2334.py`
- Zeile 19: **possible write() call**
  ```
  f.write(line + "\n")
  ```

### `D:\ShrimpDev\tools\R2335.py`
- Zeile 37: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 56: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 86: **uses configparser (inspect for write/save)**
  ```
  # 1) Imports: os + configparser
  ```
- Zeile 94: **uses configparser (inspect for write/save)**
  ```
  if "import configparser\n" not in text:
  ```
- Zeile 97: **uses configparser (inspect for write/save)**
  ```
  text = text.replace(anchor, anchor + "import configparser\n")
  ```
- Zeile 100: **uses configparser (inspect for write/save)**
  ```
  text = text.replace("import os\n", "import os\nimport configparser\n")
  ```
- Zeile 166: **uses configparser (inspect for write/save)**
  ```
  "    cfg = configparser.ConfigParser()\n"
  ```
- Zeile 181: **possible write() call**
  ```
  "            cfg.write(f)\n"
  ```
- Zeile 186: **possible write() call**
  ```
  "                cfg.write(f)\n"
  ```

### `D:\ShrimpDev\tools\R2336.py`
- Zeile 38: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 57: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 87: **uses configparser (inspect for write/save)**
  ```
  if "import configparser" not in text:
  ```
- Zeile 91: **uses configparser (inspect for write/save)**
  ```
  text = text.replace(anchor, anchor + "import configparser\n")
  ```
- Zeile 97: **uses configparser (inspect for write/save)**
  ```
  text = text.replace(anchor2, anchor2 + "import configparser\n")
  ```
- Zeile 148: **uses configparser (inspect for write/save)**
  ```
  "    cfg = configparser.ConfigParser()\n"
  ```
- Zeile 163: **possible write() call**
  ```
  "            cfg.write(f)\n"
  ```
- Zeile 168: **possible write() call**
  ```
  "                cfg.write(f)\n"
  ```

### `D:\ShrimpDev\tools\R2337.py`
- Zeile 28: **possible write() call**
  ```
  f.write(line + "\n")
  ```

### `D:\ShrimpDev\tools\R2338.py`
- Zeile 31: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 65: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 68: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 97: **uses configparser (inspect for write/save)**
  ```
  # Ensure imports: os + configparser
  ```
- Zeile 103: **uses configparser (inspect for write/save)**
  ```
  if "import configparser" not in text:
  ```
- Zeile 106: **uses configparser (inspect for write/save)**
  ```
  text = text.replace("import os\n", "import os\nimport configparser\n")
  ```
- Zeile 108: **uses configparser (inspect for write/save)**
  ```
  text = text.replace("import tkinter as tk\n", "import tkinter as tk\nimport configparser\n")
  ```
- Zeile 154: **uses configparser (inspect for write/save)**
  ```
  "    cfg = configparser.ConfigParser()\n"
  ```
- Zeile 169: **possible write() call**
  ```
  "            cfg.write(f)\n"
  ```
- Zeile 174: **possible write() call**
  ```
  "                cfg.write(f)\n"
  ```

### `D:\ShrimpDev\tools\R2339.py`
- Zeile 31: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 65: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 68: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 108: **uses configparser (inspect for write/save)**
  ```
  # Ensure imports: os + configparser
  ```
- Zeile 114: **uses configparser (inspect for write/save)**
  ```
  if "import configparser\n" not in text:
  ```
- Zeile 116: **uses configparser (inspect for write/save)**
  ```
  text = text.replace("import os\n", "import os\nimport configparser\n")
  ```
- Zeile 119: **uses configparser (inspect for write/save)**
  ```
  text = text.replace("import tkinter as tk\n", "import tkinter as tk\nimport configparser\n")
  ```
- Zeile 163: **uses configparser (inspect for write/save)**
  ```
  "    cfg = configparser.ConfigParser()\n"
  ```
- Zeile 178: **possible write() call**
  ```
  "            cfg.write(f)\n"
  ```
- Zeile 183: **possible write() call**
  ```
  "                cfg.write(f)\n"
  ```

### `D:\ShrimpDev\tools\R2340.py`
- Zeile 26: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 55: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 58: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\tools\R2341.py`
- Zeile 14: **possible write() call**
  ```
  with open(log_path,"a",encoding="utf-8") as f: f.write(line+"\n")
  ```
- Zeile 97: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\R2342.py`
- Zeile 13: **possible write() call**
  ```
  with open(log_path,"a",encoding="utf-8") as f: f.write(line+"\n")
  ```
- Zeile 86: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\R2343.py`
- Zeile 31: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 43: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 65: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 68: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 92: **uses configparser (inspect for write/save)**
  ```
  # Ensure configparser import exists
  ```
- Zeile 93: **uses configparser (inspect for write/save)**
  ```
  if "import configparser" not in txt:
  ```
- Zeile 95: **uses configparser (inspect for write/save)**
  ```
  txt = txt.replace("import os\n", "import os\nimport configparser\n")
  ```
- Zeile 98: **uses configparser (inspect for write/save)**
  ```
  txt = "import configparser\n" + txt
  ```

### `D:\ShrimpDev\tools\R2344.py`
- Zeile 41: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 44: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\tools\R2345.py`
- Zeile 26: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 48: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 51: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 67: **possible write() call**
  ```
  f.write(SHIM)
  ```

### `D:\ShrimpDev\tools\R2346.py`
- Zeile 26: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 48: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 51: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 62: **possible save() call**
  ```
  - config_loader.save(cfg)
  ```
- Zeile 72: **uses configparser (inspect for write/save)**
  ```
  import configparser
  ```
- Zeile 79: **uses configparser (inspect for write/save)**
  ```
  class ShrimpDevConfig(configparser.ConfigParser):
  ```
- Zeile 129: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 133: **possible write() call**
  ```
  cfg.write(f)
  ```
- Zeile 140: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\tools\R2347.py`
- Zeile 15: **possible write() call**
  ```
  with open(log_path,"a",encoding="utf-8") as f: f.write(line+"\n")
  ```
- Zeile 32: **possible write() call**
  ```
  with open(path,"a",encoding="utf-8") as f: f.write(content)
  ```
- Zeile 34: **possible write() call**
  ```
  with open(path,"w",encoding="utf-8") as f: f.write(content)
  ```
- Zeile 77: **possible write() call**
  ```
  "            existing.write(f)\n"
  ```
- Zeile 81: **possible write() call**
  ```
  "                existing.write(f)\n"
  ```
- Zeile 89: **possible write() call**
  ```
  f.write(txt2)
  ```
- Zeile 123: **possible save() call**
  ```
  "- config_loader.save()/config_mgr.save() machen Merge-Save: bestehende INI wird gelesen und nur übergebenen Keys überschrieben.\n"
  ```

### `D:\ShrimpDev\tools\R2348.py`
- Zeile 15: **possible write() call**
  ```
  with open(log_path,"a",encoding="utf-8") as f: f.write(line+"\n")
  ```
- Zeile 32: **possible write() call**
  ```
  with open(path,"a",encoding="utf-8") as f: f.write(content)
  ```
- Zeile 34: **possible write() call**
  ```
  with open(path,"w",encoding="utf-8") as f: f.write(content)
  ```
- Zeile 59: **possible write() call**
  ```
  "            existing.write(f)\n"
  ```
- Zeile 63: **possible write() call**
  ```
  "                existing.write(f)\n"
  ```
- Zeile 117: **possible write() call**
  ```
  f.write(patched)
  ```
- Zeile 131: **possible save() call**
  ```
  "- config_loader.save()/config_mgr.save() ersetzen jetzt robust die save()-Funktion (Type-Hints egal).\n"
  ```

### `D:\ShrimpDev\tools\R2349.py`
- Zeile 15: **possible write() call**
  ```
  with open(log_path,"a",encoding="utf-8") as f: f.write(line+"\n")
  ```
- Zeile 118: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\R2350.py`
- Zeile 15: **possible write() call**
  ```
  with open(log_path,"a",encoding="utf-8") as f: f.write(line+"\n")
  ```
- Zeile 34: **possible write() call**
  ```
  with open(path,"a",encoding="utf-8") as f: f.write(content)
  ```
- Zeile 36: **possible write() call**
  ```
  with open(path,"w",encoding="utf-8") as f: f.write(content)
  ```
- Zeile 67: **possible write() call**
  ```
  "            existing.write(f)\n"
  ```
- Zeile 71: **possible write() call**
  ```
  "                existing.write(f)\n"
  ```
- Zeile 124: **possible write() call**
  ```
  f.write(patched)
  ```
- Zeile 138: **possible save() call**
  ```
  "- config_loader.save()/config_mgr.save() schreiben INI jetzt als Merge (bestehende Sections bleiben erhalten, z.B. [Docking]).\n"
  ```

### `D:\ShrimpDev\tools\R2351.py`
- Zeile 14: **possible write() call**
  ```
  with open(log_path,"a",encoding="utf-8") as f: f.write(line+"\n")
  ```
- Zeile 123: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\R2352.py`
- Zeile 15: **possible write() call**
  ```
  with open(log_path,"a",encoding="utf-8") as f: f.write(line+"\n")
  ```
- Zeile 34: **possible write() call**
  ```
  with open(path,"a",encoding="utf-8") as f: f.write(content)
  ```
- Zeile 36: **possible write() call**
  ```
  with open(path,"w",encoding="utf-8") as f: f.write(content)
  ```
- Zeile 112: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\R2353.py`
- Zeile 26: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 36: **possible write() call**
  ```
  f.write(s)
  ```
- Zeile 47: **possible write() call**
  ```
  f.write(content)
  ```
- Zeile 50: **possible write() call**
  ```
  f.write(content)
  ```

### `D:\ShrimpDev\tools\R2354.py`
- Zeile 113: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\R2355.py`
- Zeile 100: **possible write() call**
  ```
  f.write(txt)
  ```

### `D:\ShrimpDev\tools\R2357.py`
- Zeile 18: **possible write() call**
  ```
  with open(log_path,"a",encoding="utf-8") as f: f.write(line+"\n")
  ```
- Zeile 39: **possible write() call**
  ```
  with open(p,"w",encoding="utf-8") as f: f.write(s)
  ```
- Zeile 43: **possible write() call**
  ```
  with open(p,"a",encoding="utf-8") as f: f.write(s)
  ```

### `D:\ShrimpDev\tools\R2358.py`
- Zeile 71: **possible write() call**
  ```
  f.write(item)
  ```

### `D:\ShrimpDev\tools\R2360.py`
- Zeile 1: **uses configparser (inspect for write/save)**
  ```
  import os, sys, datetime, configparser
  ```
- Zeile 13: **possible write() call**
  ```
  f.write(line + "\n")
  ```
- Zeile 25: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 35: **possible write() call**
  ```
  f.write("\n".join(lines))
  ```
- Zeile 87: **possible write() call**
  ```
  f.write("\n".join(lines))
  ```

### `D:\ShrimpDev\tools\R2361.py`
- Zeile 73: **possible write() call**
  ```
  open(path,"w",encoding="utf-8").write(txt)
  ```
- Zeile 82: **possible write() call**
  ```
  f.write(
  ```
- Zeile 89: **possible write() call**
  ```
  f.write(
  ```

### `D:\ShrimpDev\tools\R2363.py`
- Zeile 66: **possible write() call**
  ```
  open(md,"w",encoding="utf-8").write(txt)
  ```
- Zeile 72: **possible write() call**
  ```
  f.write("\n## R2363\n- Docking Refactor: Geometry exklusiv im DockManager\n")
  ```
- Zeile 74: **possible write() call**
  ```
  f.write("\n### Docking (R2363)\n- Geometry wird ausschließlich über wm_geometry() persistiert/restored.\n")
  ```

### `D:\ShrimpDev\tools\R2364.py`
- Zeile 45: **possible save() call**
  ```
  - Dadurch überschreibt config_manager.save() nicht mehr Docking-Persistenz.
  ```
- Zeile 50: **uses configparser (inspect for write/save)**
  ```
  import configparser
  ```
- Zeile 55: **uses configparser (inspect for write/save)**
  ```
  base = configparser.ConfigParser()
  ```
- Zeile 72: **possible write() call**
  ```
  self._config.write(f)
  ```
- Zeile 77: **possible write() call**
  ```
  base.write(f)
  ```
- Zeile 81: **possible write() call**
  ```
  open(cm_path, "w", encoding="utf-8").write(txt2)
  ```
- Zeile 100: **possible write() call**
  ```
  open(ut_path, "w", encoding="utf-8").write(txt)
  ```
- Zeile 135: **possible write() call**
  ```
  open(ut_path, "w", encoding="utf-8").write(txt2)
  ```
- Zeile 143: **possible write() call**
  ```
  f.write("\n## R2364\n- INI: config_manager.save() schreibt jetzt MERGE (bewahrt [Docking])\n- Restart: persist_all() vor quit()\n")
  ```
- Zeile 143: **possible save() call**
  ```
  f.write("\n## R2364\n- INI: config_manager.save() schreibt jetzt MERGE (bewahrt [Docking])\n- Restart: persist_all() vor quit()\n")
  ```
- Zeile 149: **possible write() call**
  ```
  f.write("\n### R2364 – INI Merge-Save\n- Niemals komplette INI überschreiben, wenn andere Module Sektionen (z.B. [Docking]) schreiben.\n- save() muss MERGE-Write verwenden.\n")
  ```

### `D:\ShrimpDev\tools\R2366.py`
- Zeile 70: **uses configparser (inspect for write/save)**
  ```
  import configparser, os
  ```
- Zeile 71: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 84: **uses configparser (inspect for write/save)**
  ```
  import configparser, os
  ```
- Zeile 85: **uses configparser (inspect for write/save)**
  ```
  base = configparser.ConfigParser()
  ```
- Zeile 104: **possible write() call**
  ```
  base.write(f)
  ```
- Zeile 181: **possible write() call**
  ```
  open(md, "w", encoding="utf-8").write(txt + patch)
  ```
- Zeile 190: **possible write() call**
  ```
  f.write("\n## R2366\n- Docking: Hard-Fix persist_one/persist_all (MERGE-write, geometry Pflicht)\n")
  ```

### `D:\ShrimpDev\tools\R2367.py`
- Zeile 66: **uses configparser (inspect for write/save)**
  ```
  import configparser, os
  ```
- Zeile 67: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 80: **uses configparser (inspect for write/save)**
  ```
  import configparser, os
  ```
- Zeile 81: **uses configparser (inspect for write/save)**
  ```
  base = configparser.ConfigParser()
  ```
- Zeile 100: **possible write() call**
  ```
  base.write(f)
  ```
- Zeile 176: **possible write() call**
  ```
  open(md, "w", encoding="utf-8").write(txt + patch)
  ```
- Zeile 184: **possible write() call**
  ```
  f.write("\n## R2367\n- Docking: Hard-Fix persist_one/persist_all (MERGE-write, geometry Pflicht)\n")
  ```

### `D:\ShrimpDev\tools\R2368.py`
- Zeile 71: **uses configparser (inspect for write/save)**
  ```
  import configparser, os
  ```
- Zeile 72: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 166: **possible write() call**
  ```
  open(md, "w", encoding="utf-8").write(txt + patch)
  ```
- Zeile 185: **uses configparser (inspect for write/save)**
  ```
  import configparser, os
  ```
- Zeile 188: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 215: **possible write() call**
  ```
  open(mg, "w", encoding="utf-8").write(mg_txt2)
  ```
- Zeile 223: **possible write() call**
  ```
  f.write("\n## R2368\n- Docking: Restore-Hardfix nutzt <key>.geometry + Offscreen-Fallback\n- Main: late-apply UI.geometry nach update_idletasks\n")
  ```

### `D:\ShrimpDev\tools\R2369.py`
- Zeile 74: **uses configparser (inspect for write/save)**
  ```
  import configparser, os
  ```
- Zeile 75: **uses configparser (inspect for write/save)**
  ```
  cfg = configparser.ConfigParser()
  ```
- Zeile 87: **uses configparser (inspect for write/save)**
  ```
  import configparser, os
  ```
- Zeile 88: **uses configparser (inspect for write/save)**
  ```
  base = configparser.ConfigParser()
  ```
- Zeile 107: **possible write() call**
  ```
  base.write(f)
  ```
- Zeile 252: **possible write() call**
  ```
  open(md, "w", encoding="utf-8").write(txt + patch)
  ```
- Zeile 288: **possible write() call**
  ```
  open(mg, "w", encoding="utf-8").write(mg_txt2)
  ```
- Zeile 297: **possible write() call**
  ```
  f.write("\n## R2369\n- Docking: pro Fenster Datensatz (open/docked/geometry/ts)\n- Docking: Diagnose-Logs persist/restore\n")
  ```

### `D:\ShrimpDev\tools\R2370.py`
- Zeile 29: **possible write() call**
  ```
  f.write(text)
  ```
- Zeile 124: **mentions atomic write**
  ```
  - API: `get() / set() / update_many() / save_merge_atomic()`
  ```
- Zeile 127: **mentions atomic write**
  ```
  - [ ] (HIGHEST / BLOCKER) **R2373 – Implementierung: zentraler INI-Writer (Merge + atomic)**
  ```
- Zeile 134: **possible save() call**
  ```
  - `config_manager.save()` darf niemals full-overwrite machen
  ```
- Zeile 164: **uses configparser (inspect for write/save)**
  ```
  - **Verbot:** Kein Modul darf `ShrimpDev.ini` direkt per `configparser.write()`/Full-Overwrite speichern.
  ```
- Zeile 164: **possible write() call**
  ```
  - **Verbot:** Kein Modul darf `ShrimpDev.ini` direkt per `configparser.write()`/Full-Overwrite speichern.
  ```
- Zeile 165: **mentions atomic write**
  ```
  - **Erlaubt:** Module melden Änderungen an den zentralen INI-Writer (Merge + atomic).
  ```

### `D:\ShrimpDev\tools\R2371.py`
- Zeile 11: **uses configparser (inspect for write/save)**
  ```
  # configparser writes / raw file writes
  ```
- Zeile 12: **uses configparser (inspect for write/save)**
  ```
  (r"\bconfigparser\b", "uses configparser (inspect for write/save)"),
  ```
- Zeile 17: **mentions atomic write**
  ```
  (r"atomic", "mentions atomic write"),
  ```

