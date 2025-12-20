# INI Single Writer – Migration

## Ziel
- Schrittweise Abschaltung aller Neben-Writer

## Reihenfolge (verbindlich)
1. config_manager → delegiert
2. config_loader / config_mgr → read-only
3. module_docking → delegiert
4. UI-Module → delegiert

## Erfolgskriterium
- Jede Änderung an `ShrimpDev.ini` geht über genau eine Code-Stelle
