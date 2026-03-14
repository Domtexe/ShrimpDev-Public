# ShrimpDev Safe Patch Rules

Purpose:
Prevent destructive AI patches and architecture drift.

These rules apply to all agents modifying the repository.

## 1. Minimal Change Principle

Always make the smallest possible change that solves the problem.

Never:
- refactor unrelated code
- rewrite modules unnecessarily
- restructure directories
- change architecture casually

## 2. Diagnosis Before Patch

Never patch blindly.

Required workflow:

`DIAG -> FIX -> VERIFY -> REPORT`

Before modifying code the agent must identify:

- failing component
- caller functions
- callee functions
- architecture ownership

If ownership is unclear:

STOP and run DIAG.

## 3. Target File Discipline

Agents must modify only the file(s) directly related to the task.

Forbidden:

- cross-module edits without justification
- large search/replace operations
- speculative cleanups

## 4. Architecture Boundary Rule

Respect architecture layers:

- governance/docs
- GUI layer
- module layer
- runner layer
- Excel/VBA layer
- subprojects

Do not cross boundaries without explicit instruction.

## 5. UI Patch Safety

UI changes are high risk.

Before modifying UI code agents must verify:

- widget parent container
- layout method (`pack`/`grid`/`place`)
- handler binding
- module ownership

Never guess UI layout.

## 6. Runner Discipline

Operational tasks should use runners.

Runner structure:

`tools/Rxxxx.cmd`  
`tools/Rxxxx.py`

Runners must:

- log actions
- produce reports
- avoid destructive operations

## 7. Excel/VBA Isolation

Excel work must remain inside workbook scope.

Agents must NOT mix:

- Excel debugging
with
- Python repository diagnostics

## 8. Verification Required

After patching agents must verify:

Python:
`python -m py_compile <module>`

Excel:
`VBA compile`

## 9. Stop Condition

If verification fails:

STOP patching.

Return to DIAG phase.

Never stack speculative patches.

## 10. Final Principle

Small patches.
Verified fixes.
Architecture respected.

No blind changes.
