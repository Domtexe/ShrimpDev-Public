Dim sh, cmd
Set sh = CreateObject("WScript.Shell")
sh.CurrentDirectory = "D:\ShrimpDev"
' Erst py -3 versuchen, sonst python
cmd = "cmd /c (where py >nul 2>nul && py -3 -W ignore::SyntaxWarning -u main_gui.py >> debug_output.txt 2>&1) || python -u main_gui.py >> debug_output.txt 2>&1"
sh.Run cmd, 0, False
