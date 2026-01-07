# R2377A – Restore-Code Diagnose

- Zeit: 2025-12-18 23:02:11
- Datei: modules/module_docking.py

## restore_from_ini – Struktur

- Startzeile: 420
- Basis-Indent: 4

```text
 420 |         def restore_from_ini(self):
 421 |                 ini = _r2339_ini_path(self.app)
 422 |                 try:
 423 |                         print('[Docking] INI path:', ini)
 424 |                 except Exception:
 425 |                         pass
 426 |                 cfg = _r2339_cfg_read(ini)
 427 |                 sec = 'Docking'
 428 |                 keys_raw = _r2339_cfg_get(cfg, sec, 'keys', '')
 429 |                 keys = [k.strip() for k in str(keys_raw).split(',') if k.strip()]
 430 |                 if not keys:
 431 |                         return False
 432 | 
 433 |                 mapping = {}
 434 |                 try:
 435 |                         from modules import ui_pipeline_tab
 436 |                         mapping['pipeline'] = ('Pipeline', ui_pipeline_tab.build_pipeline_tab)
 437 |                 except Exception:
 438 |                         pass
 439 |                 try:
 440 |                         from modules import ui_runner_products_tab
 441 |                         mapping['runner_products'] = ('Artefakte', ui_runner_products_tab.build_runner_products_tab)
 442 |                 except Exception:
 443 |                         pass
 444 |                 try:
 445 |                         from modules import ui_log_tab
 446 |                         mapping['log'] = ('Log', ui_log_tab.build_log_tab)
 447 |                 except Exception:
 448 |                         pass
 449 | 
 450 |                 sw = 0
 451 |                 sh = 0
 452 |                 try:
 453 |                         sw = _r2339_safe_int(self.app.winfo_screenwidth(), 0)
 454 |                         sh = _r2339_safe_int(self.app.winfo_screenheight(), 0)
 455 |                 except Exception:
 456 |                         pass
 457 | 
 458 |                 any_open = False
 459 |                 for key in keys:
 460 |                         if key not in mapping:
 461 |                                 continue
 462 |                         if self.is_open(key):
 463 |                                 continue
 464 |                         lab, builder = mapping[key]
 465 |                         ww = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.w', '0'), 0)
 466 |                         hh = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.h', '0'), 0)
 467 |                         xx = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.x', '0'), 0)
 468 |                         yy = _r2339_safe_int(_r2339_cfg_get(cfg, sec, key + '.y', '0'), 0)
 469 |                         restore_geo = None
 470 |                         if ww > 1 and hh > 1 and sw > 0 and sh > 0:
 471 |                                 if not _r2340_is_offscreen(xx, yy, ww, hh, sw, sh):
 472 |                                         restore_geo = str(ww) + 'x' + str(hh) + '+' + str(xx) + '+' + str(yy)
 473 |                         self.undock_readonly(key, lab, builder, restore_geometry=restore_geo)
 474 |                         any_open = True
 475 |                 return any_open
 476 | 
 477 | 
```

## Hinweise
- READ-ONLY Diagnose
- Dient als Grundlage für **exakt platzierte** Fixes (R2377B)
- Keine Aussagen über Verhalten, nur Struktur
