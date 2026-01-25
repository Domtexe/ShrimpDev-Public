# Agent & Guard – Mini-Architektur

## Rollen (Trennung ist verbindlich)
- **Agent**: liest Reports, clustert, priorisiert, erzeugt Vorschläge (**read-only**).
- **UI**: zeigt Status/Cluster/Vorschläge an (**keine stillen Writes**).
- **Runner**: führt Änderungen aus (Docs-only oder Apply), erzeugt Reports (**Single Path to Change**).

Merksatz: **Agent denkt – UI zeigt – Runner führt aus.**

## Datenfluss (kanonisch)
1. **Reports entstehen** durch Runner-Ausführung (`Reports/Report_R####_*.md`).
2. **Agent liest** Reports (und ggf. zusammengefasste Indizes), erstellt Cluster & Prioritäten.
3. **UI zeigt** die Cluster/Empfehlungen an (Status: grün/gelb/rot; P0/P1/P2).
4. **Entscheidung** trifft der Nutzer bzw. Governance-Regeln.
5. **Runner führt aus** (Apply oder Docs-only) und schreibt neuen Report.

## Governance-Regeln
- **DIAG-first**: Erst Diagnose/Belege, dann Aktionen.
- **Leere P0/P1-Cluster** sind **OK** (Stabilität), kein Aktionismus.
- Große P2-Cluster sind oft Altbestand → **opportunistisch** anfassen, nicht als Pflicht.

## Pipeline als SSOT
- `docs/PIPELINE.md` ist die **Single Source of Truth**.
- Writes in Pipeline erfolgen **marker-basiert** (kein freies Patchen außerhalb von Markern).

## No-Gos
- Kein Auto-APPLY durch Agent oder UI.
- Keine stillen Änderungen ohne Runner/Report.
- Keine „freien“ Pipeline-Edits ohne Marker-Zielblock.
