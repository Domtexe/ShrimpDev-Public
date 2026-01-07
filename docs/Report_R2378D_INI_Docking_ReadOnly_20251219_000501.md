# R2378D – READ-ONLY Docking/INI Diagnose

- Zeit: 2025-12-19 00:04:57
- Projekt-Root: C:\Users\rasta\OneDrive\ShrimpDev
- INI: C:\Users\rasta\OneDrive\ShrimpDev\ShrimpDev.ini

## [Docking] – Keys
- keys (raw): `runner_products,main,log`
- keys (list): `runner_products, main, log`

## Screen-Check (Single-Monitor Risikoabschätzung)
- angenommene Screen-Size: 1920x1080 (nur für Offscreen-Risiko)

## Fenster-Datensätze (pro Key)
### `main`
- open: `1` | docked: `1` | ts: `2025-12-18 23:19:49`
- geometry: `1216x703+52+52`
- w/h/x/y: `///`
- parsed: w=1216, h=703, x=52, y=52
- offscreen-risk: `NO`

### `runner_products`
- open: `1` | docked: `0` | ts: `2025-12-18 23:19:49`
- geometry: `900x700+260+143`
- w/h/x/y: `///`
- parsed: w=900, h=700, x=260, y=143
- offscreen-risk: `NO`

### `log`
- open: `0` | docked: `0` | ts: `2025-12-18 23:19:49`
- geometry: ``
- w/h/x/y: `///`
- parsed: `n/a`

### `pipeline`
- open: `` | docked: `` | ts: ``
- geometry: ``
- w/h/x/y: `///`
- parsed: `n/a`

## INI/Config Write-Entry-Points (Code Scan – Shortlist)
- Treffer: 1001

1. `Path_open_write` – C:\Users\rasta\OneDrive\ShrimpDev\learning_engine.py:72 – `with tmp.open("w", encoding="utf-8") as f:`
2. `Path_open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\config_loader.py:97 – `with path.open('w', encoding='utf-8') as f:`
3. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\config_loader.py:98 – `existing.write(f)`
4. `Path_open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\config_loader.py:101 – `with path.open('w') as f:`
5. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\config_loader.py:102 – `existing.write(f)`
6. `Path_open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\config_mgr.py:97 – `with path.open('w', encoding='utf-8') as f:`
7. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\config_mgr.py:98 – `existing.write(f)`
8. `Path_open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\config_mgr.py:101 – `with path.open('w') as f:`
9. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\config_mgr.py:102 – `existing.write(f)`
10. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\ini_writer.py:115 – `with open(tmp, 'w', encoding='utf-8') as f:`
11. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\ini_writer.py:116 – `base.write(f)`
12. `Path_open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\learning_engine.py:163 – `with path.open("w", encoding="utf-8") as f:`
13. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\logic_actions.py:766 – `with open(path, "w", encoding="utf-8") as f:`
14. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\logic_actions.py:2575 – `#         with open(path, "w", encoding="utf-8") as f:`
15. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\module_docking.py:85 – `with open(path, 'w', encoding='utf-8') as f:`
16. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\module_docking.py:86 – `cfg.write(f)`
17. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\module_docking.py:90 – `with open(path, 'w') as f:`
18. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\module_docking.py:91 – `cfg.write(f)`
19. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\module_docking.py:700 – `with open(path, "w", encoding="utf-8") as f:`
20. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\module_docking.py:701 – `base.write(f)`
21. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\module_docking.py:941 – `with open(path, "w", encoding="utf-8") as f:`
22. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\module_docking.py:942 – `base.write(f)`
23. `Path_open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\module_learningjournal.py:220 – `with tmp.open("w", encoding="utf-8") as f:`
24. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\module_runner_exec.py:78 – `with open(bat_abs, "w", encoding="utf-8", newline="") as f:`
25. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\module_runner_exec.py:115 – `with open(report_path, "w", encoding="utf-8", newline="") as f:`
26. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:417 – `with open(ini_path, "w", encoding="utf-8") as f:`
27. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:418 – `cfg.write(f)`
28. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:482 – `with open(ini_path, "w", encoding="utf-8") as f:`
29. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\modules\ui_toolbar.py:483 – `cfg.write(f)`
30. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2335.py:55 – `with open(path, "w", encoding="utf-8") as f:`
31. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2335.py:180 – `"        with open(path, 'w', encoding='utf-8') as f:\n"`
32. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2335.py:181 – `"            cfg.write(f)\n"`
33. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2335.py:185 – `"            with open(path, 'w') as f:\n"`
34. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2335.py:186 – `"                cfg.write(f)\n"`
35. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2336.py:56 – `with open(path, "w", encoding="utf-8") as f:`
36. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2336.py:162 – `"        with open(path, 'w', encoding='utf-8') as f:\n"`
37. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2336.py:163 – `"            cfg.write(f)\n"`
38. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2336.py:167 – `"            with open(path, 'w') as f:\n"`
39. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2336.py:168 – `"                cfg.write(f)\n"`
40. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2338.py:42 – `with open(path, "w", encoding="utf-8") as f:`
41. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2338.py:67 – `with open(path, "w", encoding="utf-8") as f:`
42. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2338.py:168 – `"        with open(path, 'w', encoding='utf-8') as f:\n"`
43. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2338.py:169 – `"            cfg.write(f)\n"`
44. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2338.py:173 – `"            with open(path, 'w') as f:\n"`
45. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2338.py:174 – `"                cfg.write(f)\n"`
46. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2339.py:42 – `with open(path, "w", encoding="utf-8") as f:`
47. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2339.py:67 – `with open(path, "w", encoding="utf-8") as f:`
48. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2339.py:177 – `"        with open(path, 'w', encoding='utf-8') as f:\n"`
49. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2339.py:178 – `"            cfg.write(f)\n"`
50. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2339.py:182 – `"            with open(path, 'w') as f:\n"`
51. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2339.py:183 – `"                cfg.write(f)\n"`
52. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2340.py:35 – `with open(path, "w", encoding="utf-8") as f:`
53. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2340.py:57 – `with open(path, "w", encoding="utf-8") as f:`
54. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2341.py:96 – `with open(target,"w",encoding="utf-8") as f:`
55. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2342.py:85 – `with open(target,"w",encoding="utf-8") as f:`
56. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2343.py:42 – `with open(path, "w", encoding="utf-8") as f:`
57. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2343.py:67 – `with open(path, "w", encoding="utf-8") as f:`
58. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2344.py:43 – `with open(path, "w", encoding="utf-8") as f:`
59. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2344.py:123 – `with open(report_path, "w", encoding="utf-8") as f:`
60. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2345.py:50 – `with open(path, "w", encoding="utf-8") as f:`
61. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2345.py:66 – `with open(path, "w", encoding="utf-8") as f:`
62. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2346.py:50 – `with open(path, "w", encoding="utf-8") as f:`
63. `Path_open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2346.py:128 – `with path.open("w", encoding="utf-8") as f:`
64. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2346.py:129 – `cfg.write(f)`
65. `Path_open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2346.py:132 – `with path.open("w") as f:`
66. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2346.py:133 – `cfg.write(f)`
67. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2346.py:139 – `with open(path, "w", encoding="utf-8") as f:`
68. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2347.py:34 – `with open(path,"w",encoding="utf-8") as f: f.write(content)`
69. `Path_open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2347.py:76 – `"        with path.open('w', encoding='utf-8') as f:\n"`
70. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2347.py:77 – `"            existing.write(f)\n"`
71. `Path_open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2347.py:80 – `"            with path.open('w') as f:\n"`
72. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2347.py:81 – `"                existing.write(f)\n"`
73. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2347.py:88 – `with open(path,"w",encoding="utf-8") as f:`
74. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2348.py:34 – `with open(path,"w",encoding="utf-8") as f: f.write(content)`
75. `Path_open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2348.py:58 – `"        with path.open('w', encoding='utf-8') as f:\n"`
76. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2348.py:59 – `"            existing.write(f)\n"`
77. `Path_open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2348.py:62 – `"            with path.open('w') as f:\n"`
78. `config_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2348.py:63 – `"                existing.write(f)\n"`
79. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2348.py:116 – `with open(p,"w",encoding="utf-8") as f:`
80. `open_write` – C:\Users\rasta\OneDrive\ShrimpDev\tools\R2349.py:117 – `with open(target,"w",encoding="utf-8") as f:`

... (921 weitere Treffer im Projekt)

## Fazit (was dieses Report objektiv zeigt)
- Ob [Docking] überhaupt vollständig ist (pro Fenster 1 Datensatz).
- Ob Dual-Sources aktiv sind (geometry UND w/h/x/y).
- Ob open=1 ohne keys-Eintrag vorkommt.
- Welche Dateien potentiell INI/Config schreiben (Shortlist).