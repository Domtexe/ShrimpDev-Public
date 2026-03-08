# IDEA_INBOX Spec

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

## Statuswerte

- NEW
- IMPORTED
- PARKED

## Regeln

- `Title` ist Pflicht
- `Status` ist Pflicht
- `Description` darf mehrzeilig sein
- `Tags` sind optional, aber sinnvoll
- Neue Ideen starten mit `Status: NEW`
