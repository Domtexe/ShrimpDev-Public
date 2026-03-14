# ShrimpDev AI Patch Validator

## Purpose

Detect common AI patch mistakes before work continues.

## What the validator checks

- patch touched files outside task scope
- forbidden files were modified
- AGENTS.md duplication risk
- Excel task mixed with Python repo diagnostics
- suspicious multi-file expansion
- patch touched high-risk files
- documentation-only task changed code
- code task changed architecture/governance docs unexpectedly

## High-risk files

- `main_gui.py`
- runner execution modules
- governance docs
- Excel/VBA modules

## Validation outcomes

- `OK`
- `WARNING`
- `FAIL`

## Typical fail reasons

- wrong file patched
- unrelated files changed
- multiple architecture boundaries crossed
- docs-only task changed code
- Excel task leaked into Python scope
- duplicate `AGENTS.md` created

## Operational rule

If the validator returns `FAIL`:

STOP  
Return to DIAG  
Do not continue patching

## Runner form

The validator runner follows the normal numbered runner format:

- `tools/R9417.cmd`
- `tools/R9417.py`

## Protection status

`R9417` is a protected infrastructure runner.

It is used as the validator preflight and must not be purged, auto-pruned, or treated as disposable legacy runner noise.
