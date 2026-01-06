# INI Single Writer – Architektur

## Zweck
- Verhindert konkurrierende Writes in `ShrimpDev.ini`
- Behebt Zustandsverluste (Docking, Fensterpositionen, Settings)
- Erzwingt klare Ownership

## Grundprinzip
- **Eine** autorisierte Instanz schreibt
- Alle anderen Module **delegieren**
- Merge-Write, kein Full-Overwrite
- Optional: atomic write (tmp + replace)

## Zuständigkeiten
| Bereich | Verantwortlich |
|-------|----------------|
| INI Lesen | Zentraler INI-Writer |
| INI Schreiben | Zentraler INI-Writer |
| Docking | Delegiert an INI-Writer |
| Settings/Filters | Delegiert |

## Verbote
- Kein Modul darf `configparser.write()` direkt auf `ShrimpDev.ini` anwenden
- Kein Full-Overwrite außerhalb des INI-Writers

## Diagnose-first
- Bei Fehlern zuerst Instrumentierung
- Fix erst nach messbarem IST/SOLL-Vergleich
