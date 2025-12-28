# MasterRules_Core – Grundprinzipien

_Automatisch generiert oder aktualisiert durch R2037 am 2025-12-09 09:39:55_

## 1. Nicht-destruktive Änderungen

- Es werden keine produktiven Dateien ohne Backup geändert.
- Runner legen vor strukturellen Änderungen Backups an (z. B. unter `_Archiv`).
- Alte Versionen bleiben rekonstruierbar; neue Versionen sind minimal invasiv.

## 2. Modulprinzip

- Funktionen werden in klar getrennten Modulen implementiert.
- ShrimpDev und ShrimpHub arbeiten mit expliziten Imports, ohne versteckte
  exec/Reflection-Tricks.

## 3. Pfade & Umgebung

- Standardpfad ist immer der Projekt-Root, in dem das Skript ausgeführt wird.
- Keine harten Laufwerks-Pfade im Code; Runner arbeiten relativ zum Projekt.

## 4. Logging & Reports

- Wichtige Operationen erzeugen Reports unter `_Reports/`.
- Fehler werden nicht verschwiegen, sondern nachvollziehbar protokolliert.

## Patch-Rollback-Pflicht

- **Ziel:** Kein fehlerhafter Patch bleibt im Arbeitsstand liegen.
- **Trigger:** Wenn ein Runner-Patch
  - mit Exit-Code != 0 endet, oder
  - einen Syntax- oder Compile-Check nicht besteht, oder
  - einen definierten Smoke-Test nicht besteht,
  muss ein **Rollback** auf den letzten sicheren Stand erfolgen.
- **Pflichtablauf (Runner):**
  - Vor Patch: Backup der betroffenen Dateien nach `_Archiv/`.
  - Patch anwenden.
  - Validierung (mindestens Syntax/Compile, optional Smoke-Test).
  - Bei Fehler: automatisch Dateien aus Backup wiederherstellen.
  - Report in `Reports/` muss enthalten:
    - Grund des Rollbacks (SOLL/IST),
    - betroffene Dateien,
    - verwendete Backup-Dateien,
    - naechster Schritt (Diagnose-first, falls wiederholt).
- **No-Go:** Manuelles Liegenlassen eines kaputten Zustands oder Folge-Patches ohne Diagnose.
