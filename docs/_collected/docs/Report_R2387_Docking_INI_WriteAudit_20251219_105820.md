# Report R2387 – Docking INI Presence + Write-Audit (READ-ONLY)

- Timestamp: 2025-12-19 10:58:20
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`

## ShrimpDev.ini Status
- INI: `C:\Users\rasta\OneDrive\ShrimpDev\ShrimpDev.ini`
- Size: 993 bytes
- SHA256: `bcd40915b43673fa69df5b8b04fabd10dfc6992ece6247c6cbae889a639e2f85`

- Has [Docking]: **True**
- Docking keys count: 17

## Docking Keys (expected)
- `main`: open=`1` docked=`1` geo=`1216x703+104+104` ts=`2025-12-19 10:57:52`
- `pipeline`: open=`1` docked=`0` geo=`900x700+312+195` ts=`2025-12-19 10:57:45`
- `log`: open=`0` docked=`0` geo=`` ts=`2025-12-19 10:57:52`
- `runner_products`: open=`1` docked=`0` geo=`900x700+312+195` ts=`2025-12-19 10:57:52`

## Write-Audit (Code Grep)
### config_loader.save
- main_gui.py:396: `config_loader.save(cfg)`
- modules\config_loader.py:9: `- config_loader.save(cfg)`
- modules\config_mgr.py:9: `- config_loader.save(cfg)`
- modules\logic_actions.py:1127: `'''ShrimpDev.ini ueber modules.config_loader.save() speichern.'''`
- modules\logic_actions.py:1387: `"""ShrimpDev.ini ueber modules.config_loader.save() speichern."""`
- modules\ui_filters.py:43: `config_loader.save(cfg)`
- modules\ui_filters.py:57: `config_loader.save(cfg)`

### ini_writer.merge_write_ini
- modules\config_manager.py:100: `w.merge_write_ini(str(cfg_path), updates)`
- modules\config_manager.py:106: `merge_write_ini(str(cfg_path), updates)`
- modules\ini_writer.py:157: `def merge_write_ini(project_root: Path,`

### configparser.write
- main_gui.py:41: `f.write(line + "\n")`
- modules\config_loader.py:98: `existing.write(f)`
- modules\config_loader.py:102: `existing.write(f)`
- modules\config_mgr.py:98: `existing.write(f)`
- modules\config_mgr.py:102: `existing.write(f)`
- modules\exception_logger.py:23: `f.write(text)`
- modules\exception_logger.py:25: `f.write('\n')`
- modules\exception_logger.py:172: `f.write(line + '\n')`
- modules\ini_writer.py:116: `base.write(f)`
- modules\ini_writer.py:190: `base.write(f)`
- modules\learning_engine.py:97: `f.write(line + "\n")`
- modules\logic_actions.py:75: `f.write(msg + "\n")`
- modules\logic_actions.py:767: `f.write(content)`
- modules\logic_actions.py:1850: `#             f.write(line)`
- modules\logic_actions.py:2576: `#             f.write(text or "")`
- modules\module_agent.py:86: `f.write(f"[{_t.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")`
- modules\module_docking.py:86: `cfg.write(f)`
- modules\module_docking.py:91: `cfg.write(f)`
- modules\module_docking.py:701: `base.write(f)`
- modules\module_docking.py:942: `base.write(f)`
- modules\module_gate_smoke.py:14: `f.write(f"[GATE { _ts() }] {msg}\n")`
- modules\module_learningjournal.py:47: `f.write(line + "\n")`
- modules\module_patch_release.py:27: `z.write(p, p.relative_to(ROOT))`
- modules\module_runner_exec.py:32: `f.write(msg.rstrip() + "\n")`
- modules\module_runner_exec.py:79: `f.write(_bat_template(rel_py, title or f"ShrimpDev - {base}"))`
- modules\module_runner_exec.py:116: `f.write(res["output"])`
- modules\module_runner_exec.py:137: `f.write((msg or "").rstrip() + "\n")`
- modules\module_runner_exec.py:149: `f.write(line.rstrip('\n') + '\n')`
- modules\module_runnerbar.py:16: `f.write(f"[RunnerBar {ts}] {msg}\n")`
- modules\move_journal.py:49: `f.write(json.dumps(entry, ensure_ascii=False) + "\n")`
- modules\snippets\agent_client.py:18: `(INBOX / f"{int(time.time())}_{os.getpid()}.jsonl").open("a", encoding="utf-8").write(json.dumps(ev, ensure_ascii=False)+"\n")`
- modules\snippets\logger_snippet.py:35: `f.write(line)`
- modules\snippets\snippet_file_ops.py:19: `f.write(f"[{ts}] [FileOps] {msg}\n")`
- modules\snippets\snippet_file_ops.py:37: `with open(self.path, "w", encoding="utf-8") as f: f.write("[]")`
- modules\snippets\snippet_log_runner.py:56: `f.write(msg + "\n")`
- modules\tools\patchlib_guard.py:33: `f.write(ctx.original)`
- modules\tools\patchlib_guard.py:39: `f.write(ctx.modified)`
- modules\tools\shrimpdev_event.py:25: `).write(json.dumps(ev, ensure_ascii=False) + "\n")`
- modules\ui_toolbar.py:418: `cfg.write(f)`
- modules\ui_toolbar.py:483: `cfg.write(f)`

### open(..., 'w')
- modules\ini_writer.py:115: `with open(tmp, 'w', encoding='utf-8') as f:`
- modules\logic_actions.py:766: `with open(path, "w", encoding="utf-8") as f:`
- modules\logic_actions.py:2575: `#         with open(path, "w", encoding="utf-8") as f:`
- modules\module_docking.py:85: `with open(path, 'w', encoding='utf-8') as f:`
- modules\module_docking.py:90: `with open(path, 'w') as f:`
- modules\module_docking.py:700: `with open(path, "w", encoding="utf-8") as f:`
- modules\module_docking.py:941: `with open(path, "w", encoding="utf-8") as f:`
- modules\module_runner_exec.py:78: `with open(bat_abs, "w", encoding="utf-8", newline="") as f:`
- modules\module_runner_exec.py:115: `with open(report_path, "w", encoding="utf-8", newline="") as f:`
- modules\snippets\snippet_file_ops.py:37: `with open(self.path, "w", encoding="utf-8") as f: f.write("[]")`
- modules\snippets\snippet_file_ops.py:46: `with open(self.path, "w", encoding="utf-8") as f:`
- modules\tools\patchlib_guard.py:32: `with open(bak, "w", encoding="utf-8") as f:`
- modules\tools\patchlib_guard.py:38: `with open(ctx.path, "w", encoding="utf-8", newline="") as f:`
- modules\ui_toolbar.py:417: `with open(ini_path, "w", encoding="utf-8") as f:`
- modules\ui_toolbar.py:482: `with open(ini_path, "w", encoding="utf-8") as f:`

### Path.write_text
- modules\context_state.py:57: `p.write_text(json.dumps(_CONTEXT, indent=2, ensure_ascii=False), encoding="utf-8")`
- modules\learning_engine\persistence.py:22: `DB.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")`
- modules\module_agent.py:84: `p.write_text("", encoding="utf-8", errors="ignore") if not p.exists() else None`
- modules\module_agent.py:102: `p.write_text(`
- modules\module_agent.py:130: `p.write_text(`
- modules\module_agent.py:500: `_agent_last_action_path().write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')`
- modules\module_agent.py:597: `p.write_text("".join(lines), encoding="utf-8")`
- modules\module_preflight.py:35: `rep.write_text("\n".join([f"{a}\t{b}\t{c}" for a, b, c in rows]), encoding="utf-8")`
- modules\module_project_scan.py:81: `MAP_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")`
- modules\module_project_scan.py:88: `MAP_HTML.write_text(`
- modules\module_project_scan.py:104: `p.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")`
- modules\module_registry.py:28: `REG.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")`
- modules\module_settings_ui.py:16: `try: CFG.write_text(json.dumps(conf, ensure_ascii=False, indent=2), encoding="utf-8")`
- modules\snippets\safeio.py:8: `tmp.write_text(data, encoding="utf-8")`
- modules\ui_pipeline_tab.py:313: `p.write_text("".join(lines), encoding="utf-8")`
