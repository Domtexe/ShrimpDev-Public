# R2373 – zentraler INI-Writer

- Zeit: 2025-12-18 21:01:30
- Scope: Neues Modul `modules/ini_writer.py` + Pipeline-Einsortierung
- Keine Migration bestehender Writer (kommt in R2374/R2375)

## Akzeptanzkriterien
- Merge-only (fremde Sections bleiben)
- Atomic write (tmp + replace)
- Logging mit source
- snapshot() vorhanden
