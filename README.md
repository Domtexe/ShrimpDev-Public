# ShrimpDev

ShrimpDev ist ein modulares Python/Tkinter-System zur Entwicklung, Diagnose und Reparatur – umgesetzt über strikt nummerierte Runner (R####).

## Kernprinzipien
- **Runner-first**: Änderungen erfolgen über `tools\R####.cmd` + `tools\R####.py`.
- **Rückbaubar**: Vor jeder Änderung Backups, klare Logs, keine “stillen” Rewrites.
- **Stabilität vor Tempo**: Erst Absicherung, dann Features.
- **Dokumentation ist Pflicht**: Architektur/Regeln werden mit jeder Änderung gepflegt.

## Quickstart
```bat
cd /d C:\Users\rasta\OneDrive\ShrimpDev
python main_gui.py
```

## Runner-Standard
- Starter: `tools\R####.cmd`
- Logik:   `tools\R####.py`

## Selbstlernen & KI-Features (high level)
ShrimpDev nutzt Selbstlern- und KI-gestützte Analysefunktionen, um Code/Strukturen nachvollziehbar zu prüfen, Verbesserungen zu planen und Reparaturen kontrolliert auszuführen.
Wichtig: **keine Magie, keine autonomen Rewrites** – immer regelgetrieben und reviewbar.

## Doku
- `docs/ARCHITECTURE.md` – Struktur & Zuständigkeiten
- `docs/DEVELOPMENT_RULES.md` – harte Regeln (Mastermodus)
- `docs/ASSISTANT_BRIEFING.md` – Briefing für neue Chat-Instanzen
- `docs/BOOTSTRAP_PROMPT.txt` – Copy/Paste Prompt für neue Chats
