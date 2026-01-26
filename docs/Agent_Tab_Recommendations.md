# Agent-Tab — Empfehlungen (stabilisiert)

## Ziel
- Empfehlungen sollen **nicht spammen**, sondern nur dann erscheinen, wenn sie wirklich sinnvoll sind.

## Regeln (Source of Truth)
### Diagnose (R1802)
- **Primary**: `Reports/Agent_LastDiag.json` (parsebarer Timestamp)
- **Fallback**: `learning_journal.json` (heuristisch)
- Empfehlung nur wenn:
  - `errors(last5) > 0` **oder**
  - keine/alte Diagnose (stale)

### Error-Scan (R2086)
- Empfehlung **nur bei Baseline-Delta**:
  - Baseline fehlt → initialer Scan
  - Baseline existiert → still (bis Delta gemeldet wird)

## Relevante Runner
- R3837: Heuristik-2 robust (R2086 baseline/delta)
- R3840: Heuristik-1 stale/absent/err-based (R1802)
- R3842: Heuristik-1 nutzt Agent_LastDiag.json (primary)
- R3843: R1802 schreibt Agent_LastDiag.json (Producer)
- R3844: DIAG (Stamp + agent_recommendations)

## Status
- Stand: 2026-01-26
- Status: DONE / Closed
