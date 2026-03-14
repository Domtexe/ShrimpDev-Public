# ShrimpDev – Agent Playbook

This document describes the **operational behavior** expected from agents working in this repository.

It complements:

AGENTS.md  
docs/MasterRules.md  
docs/FILE_MAP.md  

AGENTS.md defines rules.  
This playbook describes **how to work step-by-step**.

---

# 1. STANDARD WORKFLOW

Every task must follow the workflow:

DIAG → FIX → VERIFY → REPORT

Never skip DIAG.

---

# 2. TASK START PROCEDURE

Before doing anything:

1. Identify task scope
2. Identify target file(s)
3. Check AGENTS.md
4. Check FILE_MAP.md
5. Determine architecture context

Questions the agent must answer first:

- Which file is the primary target?
- Which module owns the behavior?
- Which functions call this code?
- Which functions are called by this code?

If this cannot be answered:

STOP.

Run DIAG first.

---

# 3. DIAG PLAYBOOK

DIAG must identify:

### For Python / UI tasks

- parent container
- layout method (pack/grid/place)
- widget hierarchy
- handler wiring
- module boundaries

Minimum DIAG checklist:

- target function start/end
- caller(s)
- callee(s)
- layout containers
- existing handlers

---

### For Runner tasks

Check:

tools/Rxxxx.cmd  
tools/Rxxxx.py  

Confirm:

- runner target
- execution environment
- expected report output
- side effects

---

### For Excel / VBA tasks

Inspect:

- target workbook
- VBA module
- affected procedures
- helper functions
- tables/columns referenced

Check specifically for:

forbidden names  
string continuation issues  
compile errors  

---

# 4. FIX PLAYBOOK

After DIAG, the patch must be:

Minimal  
Deterministic  
Scoped

Guidelines:

- change only requested behavior
- prefer existing architecture
- do not introduce new systems

Prefer:

- wiring existing handlers
- layout corrections
- syntax fixes
- variable renames

Avoid:

- architecture rewrites
- module restructuring
- speculative improvements

---

# 5. VERIFY PLAYBOOK

Verification must be performed immediately after a patch.

### Python tasks

Run:

python -m py_compile main_gui.py

and other modified modules.

### Excel tasks

Run:

VBA Compile

Confirm:

No syntax errors.

---

# 6. REPORT PLAYBOOK

Every task must generate a report.

Location:

Reports/Report_Rxxxx_<timestamp>.md

Report structure:

## Task

What was requested.

## Diagnosis

What was discovered.

## Patch

What changed.

## Verification

Compile or runtime verification.

## Result

Goal achieved or not.

Reports must stay inside the task scope.

---

# 7. PATCH SCOPE CONTROL

Agents must obey strict scope rules.

Allowed scope:

- files explicitly named in task
- direct helper functions
- minimal required context

Forbidden scope expansion:

- repository refactors
- module reorganizations
- UI redesign
- business logic changes

If additional files appear necessary:

STOP  
Report the issue  
Wait for instruction.

---

# 8. RUNNER WORKFLOW

Operational changes should use runners.

Structure:

tools/Rxxxx.cmd  
tools/Rxxxx.py  

Runner responsibilities:

- execute change
- log clearly
- produce report
- avoid destructive operations

---

# 9. ARCHITECTURE CHECK

Before modifying any code:

Check:

docs/FILE_MAP.md

Determine:

- module ownership
- architecture boundaries
- responsible component

Never guess architecture.

---

# 10. THREADCUT HANDOFF

When a thread ends and work continues elsewhere:

Old thread:

alt - <title>

New thread:

Aktiv - <title>

Remove existing `Aktiv -` prefix before applying `alt -`.

Multiple `Aktiv -` threads are allowed.

---

# 11. FAILURE MODE

If a patch fails verification:

1. Stop patching
2. Produce diagnostic report
3. Identify root cause
4. Propose minimal fix

Never stack patches blindly.

---

# 12. DIAG ESCALATION

If a problem persists after first fix:

Switch to diagnostic mode.

Actions:

- add instrumentation
- add logging
- isolate minimal reproduction

Then retry patch.

---

# 13. FILE MAP MAINTENANCE

If architecture changes:

Update:

docs/FILE_MAP.md  
docs/FILE_MAP_TECH.md

Maps must remain curated.

Never dump raw filesystem listings.

---

# 14. PRINCIPLE

Small patches.  
Verified changes.  
Architecture respected.

No guesswork.

This repository is **structure-driven**.