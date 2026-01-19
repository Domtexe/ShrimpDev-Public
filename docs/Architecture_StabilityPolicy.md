# Repository Stability Policy

## Zweck
Diese Policy beschreibt, wie Stabilitäts-Analysen (HOT/WARM/COLD) in ShrimpDev
zu interpretieren sind und **welche Konsequenzen sie haben – und welche nicht**.

---

## Begriffe

### HOT
Dateien/Module mit:
- hoher Import-Dichte
- Start- oder Runner-Relevanz
- Registry-/Systemzugriffen

**HOT bedeutet: kritisch im Betrieb, nicht kaputt.**

### WARM
- regelmäßig genutzt
- mittlere Abhängigkeiten
- geeignet für **kleine, gezielte Fixes**

### COLD
- selten genutzt
- isoliert
- **bewusst nicht anfassen**, solange kein Bug vorliegt

---

## Zentrale Regeln

### HOT ≠ Refactor-Pflicht
- HOT-Dateien sind oft stabil **wegen** ihrer Defensive.
- Präventives „Aufräumen“ ist verboten.
- Änderungen **nur bei konkretem Bug**.

### Archiv-Code ist inert
- Inhalte unter `tools/Archiv/` sind **nicht produktiv**.
- Sie beeinflussen keine Laufzeitpfade.
- Sie sind **keine** Kandidaten für Stabilitäts- oder Qualitätsmaßnahmen.

### Pflichtkette bei Änderungen an HOT/WARM
1. **DIAG** (IST messbar machen)
2. **Mini-APPLY** (kleinstmöglicher Scope)
3. **Report** (Bezug, Risiko, Verifikation)

Ohne diese Kette gilt eine Änderung als Regelverstoß.

---

## Zielzustand
- Stabilität durch **Governance**, nicht durch Dauer-Refactoring
- Wissen bleibt explizit, Entscheidungen nachvollziehbar
