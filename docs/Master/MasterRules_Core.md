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
