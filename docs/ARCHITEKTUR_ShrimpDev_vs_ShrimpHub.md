# Architektur: ShrimpDev vs. ShrimpHub

## Zweck
Diese Architektur trennt **Denken** von **Produktion**, um langfristige Stabilität,
Disziplin und Skalierbarkeit sicherzustellen.

## Rollenmodell
### ShrimpDev
- Entscheidungsinstanz
- Pipeline & Priorisierung
- MasterRules & Governance
- Diagnose-first
- Dokumentation & Lernen

### ShrimpHub
- Produktionsoberfläche
- GUI & Workflows
- Medien-, Content- und Exportprozesse
- Keine Entscheidungslogik

## Warum die Trennung absichtlich ist
- Verhindert Regelumgehung aus Bequemlichkeit
- Schützt Systemdisziplin vor UI-Druck
- Ermöglicht stabile, wiederholbare Produktion

## Evolutionspfad
1. Strikte Trennung (heute)
2. Ein System mit zwei Modi (Dev / Hub)
3. ShrimpDev läuft unsichtbar im Hintergrund

## No-Gos
- Logik oder Regeln in ShrimpHub
- Ad-hoc-Ausnahmen ohne Pipeline-Entscheidung
- UI-Features ohne Dokumentation
- Architektur-Vermischung ohne explizite Freigabe

## Gültigkeit
Diese Architektur ist verbindlich, bis sie explizit per Pipeline-Entscheidung geändert wird.
