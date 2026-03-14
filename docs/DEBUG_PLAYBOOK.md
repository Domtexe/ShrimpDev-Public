# ShrimpDev – Debug Playbook

This document defines structured debugging procedures for agents working in this repository.

It complements:

AGENTS.md  
docs/AGENT_PLAYBOOK.md

The purpose is to prevent blind patching and enforce systematic diagnosis.

---

# 1. DEBUG PRINCIPLE

Never patch before understanding the failure.

Always determine:

- where the failure occurs
- why it occurs
- which component owns the behavior

---

# 2. DEBUG WORKFLOW

Standard debugging workflow:

1. Reproduce the issue
2. Identify failing component
3. Inspect code boundaries
4. Add diagnostics if necessary
5. Confirm root cause
6. Apply minimal fix
7. Verify fix

Never skip steps.

---

# 3. PYTHON DEBUG CHECKLIST

When debugging Python issues:

Inspect:

- target file
- caller functions
- callee functions
- module imports
- UI container hierarchy
- layout methods (pack/grid/place)

Verify:

- syntax
- handler wiring
- variable scope

Compile check:

python -m py_compile <module>

---

# 4. UI DEBUG CHECKLIST

For UI issues inspect:

- parent container
- layout method
- widget creation order
- handler binding

Typical problems:

- wrong parent container
- conflicting pack/grid usage
- duplicate widgets
- missing handler wiring

---

# 5. RUNNER DEBUG CHECKLIST

When debugging runners:

Inspect:

tools/Rxxxx.cmd  
tools/Rxxxx.py

Verify:

- working directory
- command execution
- expected outputs
- report generation

Ensure:

Reports/Report_Rxxxx_<timestamp>.md exists.

---

# 6. EXCEL / VBA DEBUG CHECKLIST

When debugging Excel/VBA:

Inspect:

- workbook structure
- affected VBA module
- related procedures
- table column references

Check specifically:

- compile errors
- forbidden variable names (e.g. cDate)
- string continuation
- missing functions

Run:

VBA compile.

---

# 7. ROOT CAUSE ANALYSIS

Before patching confirm:

Root cause belongs to:

- syntax error
- handler wiring
- layout logic
- variable naming conflict
- incorrect module reference

Never guess root cause.

---

# 8. PATCH VALIDATION

After applying fix verify:

- compile success
- no new warnings
- behavior matches task request

If verification fails:

STOP.

Return to DIAG phase.

---

# 9. ESCALATION MODE

If problem persists after first fix:

Switch to diagnostic mode.

Allowed actions:

- add temporary logging
- isolate minimal reproduction
- instrument specific functions

Then retry patch.

---

# 10. DEBUG PRINCIPLE

Always prefer:

Small verified fixes.

Never apply:

Large speculative patches.

---

# FINAL RULE

Debugging must be systematic.

No blind patches.  
No guessing behavior.