# MasterRules_GUI – GUI-Regeln

_Automatisch generiert oder aktualisiert durch R2037 am 2025-12-09 09:39:55_

## 1. Modularer Aufbau

- GUI-Elemente (Toolbar, Intake, TreeView, Tabs) werden in eigene Module
  ausgelagert.

## 2. UX-Grundsätze

- Klare Statusanzeige (Statusleiste, LEDs) ohne die Oberfläche zu blockieren.
- Längere Operationen blockieren nicht den UI-Thread, wo immer möglich.

## 3. Dark-Mode & Style

- Farben und Styles sind zentral definiert (z. B. ui_theme_* Module) und werden
  nicht hart im Code verstreut.

## Tools Purge
Tools-Purge: Purge ist ROOT-only (nur tools\*.*). Subfolder werden NICHT gescannt und NICHT bewegt.
