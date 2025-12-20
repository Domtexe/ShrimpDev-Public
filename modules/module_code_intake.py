"""
Legacy Intake Module (Deprecated)

Dieses Modul wird seit R1965 von ShrimpDev NICHT MEHR verwendet.
Es bleibt nur aus historischen Gründen bestehen.
Enthält keinen aktiven Code.
"""

# R2243: zentraler Runner-Start aus Intake
def _run_runner_from_intake(runner_id: str):
    from modules.module_runner_exec import run
    run(runner_id, source='intake')

def _run_cmd(path: str) -> None:
    # FINAL FIX: Intake-Run MUSS Runner-ID verwenden (Logging garantiert)
    import os
    import re
    base = os.path.basename(path)
    m = re.search(r"\bR(\d{3,5}[a-zA-Z]?)\b", base)
    if not m:
        return
    runner_id = m.group(1)
    _run_runner_from_intake(runner_id)

