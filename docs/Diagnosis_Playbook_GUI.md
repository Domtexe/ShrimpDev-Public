# Diagnosis Playbook – GUI/State (ShrimpDev)

> Ziel: Kein Try&Error bei GUI-/State-Themen. Ab dem 2. Versuch immer Diagnose zuerst.
> Marker: R2353_DIAGNOSE_FIRST

## Wann Diagnose Pflicht ist (ab 2. Versuch)
Diagnose-Modus ist verpflichtend, wenn ein Fix **nicht beim 1. Versuch verifiziert** greift, z.B.:
- Fensterposition/Größe wird nicht korrekt restored
- after_idle / WM überschreibt geometry()
- INI wird geschrieben, aber Restore greift nicht
- “kommt immer zentriert” / “random position” / “nur 1x”

## SOLL/IST – Checkliste
**SOLL** (konkret):
- Was genau soll passieren? (z.B. “Artefakte kommt nach Neustart exakt wieder auf X/Y”)

**IST** (messbar):
- Welche Werte stehen in der INI?
- Welche Werte werden beim Start gelesen?
- Welche geometry() wird tatsächlich aufgerufen?
- Welche Position hat das Fenster effektiv *nach* WM/after_idle?

## Minimaler Diagnose-Runner (Template)
Ein Diagnose-Runner ist **read-only** oder minimal-invasiv:
- keine Refactors
- keine UI-Experimente
- nur Logging + klare Ausgabe

### Standard-Logpunkte (empfohlen)
Logge jeweils mit eindeutiger Prefix-Struktur:
- `[DIAG] ini_path=...`
- `[DIAG] ini_read key=... x=... y=... w=... h=... geo=...`
- `[DIAG] apply geometry=... (when)`
- `[DIAG] effective wm_geometry=... winfo_x=... winfo_y=...`

### Timing-Slots
- vor `after_idle`
- innerhalb `after_idle` / `after(0)`
- nach `update_idletasks()`

## Diagnose → Fix (Regel)
1) Diagnose: Hypothese beweisen (Messwert verändert sich erwartbar)
2) Fix: genau 1 minimaler Fix
3) Verify: Messwerte zeigen SOLL erreicht
4) Doku: kurze Notiz in Architecture + Changelog

## Offscreen-Fallback Standard
Wenn Restore außerhalb des sichtbaren Bereichs landen würde:
- clamp/center auf Default
- protokollieren: `[DIAG] offscreen detected -> default`

