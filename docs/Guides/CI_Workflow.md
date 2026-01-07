# CI Workflow (ShrimpDev)

Stand: 2025-12-28 23:08:34

## Ziele
- Valides YAML
- Frühe Fehlererkennung (Syntax)
- Public-Mirror-kompatibel

## Richtiger Step-Aufbau
```yaml
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.11"
```

## Guards für Public-Repos
```bash
if [ -f main_gui.py ]; then python -m py_compile main_gui.py; fi
```

## Minimaler Syntax-Gate
```bash
python -m compileall -q modules
python -m compileall -q tools
```
