# IDEA_INBOX Spec

## Canonical Store

- Kanonische Quelle ist `docs/IDEA_INBOX.md`.
- `docs/ideas/ideas_inbox_*.md` ist kein Importpfad; falls vorhanden, dann nur Archiv/Beleg.
- Der bestehende Importweg arbeitet auf `NEW`-Eintraegen in `docs/IDEA_INBOX.md`.

## Format

Jeder Eintrag ist ein Block:

## ENTRY

Title: <Kurzname>

Description:
<Mehrzeilige Beschreibung>

Tags:
<TAG1, TAG2, TAG3>

Source:
<Quelle>

Status:
NEW

## Feldregeln

- `Title` ist Pflicht.
- `Status` ist Pflicht.
- `Description` darf mehrzeilig sein.
- `Tags` sind optional, aber sinnvoll.
- `Source` soll den echten Feeder nennen, z. B. `ShrimpDev GUI` oder `R9418 THREAD_BATCH <timestamp>`.
- Neue Ideen starten mit `Status: NEW`.

## Statuswerte

- NEW
- IMPORTED
- PARKED

## Batch-Vorbereitung

- Batch-Runner wie `R9418` muessen einzelne Ideen in einzelne `## ENTRY`-Bloecke aufloesen.
- Batch-Runner duerfen keinen zweiten Importpfad einfuehren.
- Archivdateien unter `docs/ideas/` sind nur Nebenablage und muessen als nicht-kanonisch behandelt werden.
- Der reguläre Import-Run bleibt `GUI -> R9341 -> bestehende Kette`.
