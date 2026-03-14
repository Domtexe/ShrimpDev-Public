# ShrimpDev AI Failsafe Rules

Purpose:
Prevent catastrophic AI mistakes such as:
- patching wrong files
- breaking UI layout
- modifying architecture blindly
- corrupting runner logic
- mixing Excel and Python scopes

## 1. File Ownership Check

Before modifying any file agents must verify:

- which component owns the behavior
- which module defines the functionality
- whether the change belongs to this repository layer

If ownership is unclear:

STOP and run DIAG.

## 2. Wrong File Protection

Never patch the nearest file just because it contains similar code.

Always confirm:

- module ownership
- architecture layer
- calling context

## 3. UI Safety Lock

UI patches are high risk.

Before editing UI code verify:

- widget parent container
- layout manager (`pack`/`grid`/`place`)
- handler wiring
- module boundaries

Never guess UI structure.

## 4. Runner Protection

Do not modify runner behavior unless explicitly instructed.

Protected areas include:

`tools/Rxxxx.cmd`  
`tools/Rxxxx.py`

Runner workflow must remain:

`DIAG -> FIX -> VERIFY -> REPORT`

## 5. Architecture Protection

Never restructure repository architecture.

Forbidden actions:

- moving folders
- renaming core modules
- reorganizing subsystem docs
- deleting architecture files

## 6. Excel Scope Protection

Excel/VBA debugging must remain inside workbook scope.

Never combine:

Excel debugging
with
Python repository diagnostics.

## 7. Multi-File Patch Lock

If a change appears to require edits in multiple unrelated files:

STOP.

Return to DIAG.

Confirm architecture ownership first.

## 8. High-Risk Files

Extra caution required for:

`main_gui.py`  
core UI modules  
runner execution logic  
governance documentation  
Excel VBA modules

Patches must remain minimal.

## 9. Fail-Safe Abort Rule

If a patch introduces new errors:

STOP immediately.

Do not continue patching.

Return to DIAG phase.

## 10. Final Failsafe Principle

Never guess.

Always diagnose.

Always patch minimally.

Architecture integrity is more important than speed.
