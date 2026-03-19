# Public Architecture

## Overview

ShrimpDev is a desktop-oriented application with a documentation-heavy engineering workflow.

At a high level, the system is organized around:
- a main application entrypoint
- modular application logic
- a runner/tooling layer for controlled project operations
- documentation that explains public-facing structure and intent

## Public Architecture Surface

The public export keeps only a high-level architectural view:
- main application layer
- supporting modules
- curated tooling concept
- public documentation boundaries

## Deliberately Excluded

This public architecture view does not include:
- internal governance mechanics
- internal pipeline orchestration
- internal audit and report machinery
- internal runtime state or journal details
- local environment specifics

## Reader Guidance

Use this public architecture summary together with:
- `README.md`
- `docs/Public_Contract.md`
- `docs/Public_Roadmap.md`

If deeper internal process documentation exists in the private repository, it is intentionally not mirrored here.
