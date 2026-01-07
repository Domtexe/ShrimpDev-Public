# Report R2407 – Docking Start State Audit (READ-ONLY)

- Timestamp: 2025-12-20 00:18:41
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- INI: `C:\Users\rasta\OneDrive\ShrimpDev\ShrimpDev.ini`

## INI [Docking]
- present: **True**

- main: open=`1` docked=`1` geo=`1216x695+3+4` ts=`2025-12-20 00:13:13`
- pipeline: open=`0` docked=`0` geo=`1608x451+77+792` ts=`2025-12-19 22:40:10`
- runner_products: open=`0` docked=`0` geo=`938x571+191+393` ts=`2025-12-19 22:39:49`
- log: open=`0` docked=`0` geo=`` ts=`2025-12-20 00:13:13`

## Runtime Audit Notes
- Dieser Runner ist READ-ONLY und liest nur die INI.
- Für den Runtime-Teil (existierende Fenster im _dock_manager) brauchen wir einen App-Hook beim Start.

## Next
- Wenn Fenster trotz korrekt gesetzter INI zentrieren: dann kommt ein Start-Hook in main_gui.py, der direkt nach DockManager.restore_from_ini() einen Log-Dump schreibt (R2408).

