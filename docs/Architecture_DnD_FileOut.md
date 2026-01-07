# Architecture: DnD File-out (Artefakte → Explorer)

## Scope
- Drag & Drop **aus ShrimpDev heraus** (Artefakt-Tree) **in Windows Explorer / Desktop / Zielordner**.
- Supported: **Files** (z. B. `.png`, `.mp4`, `.txt`, `.md`, `.zip`) aus Artefakt-Baum.
- Optional später: Ordner (nicht in PoC).

## Non-Goals
- Kein Drag **in andere Apps** (Photoshop, Browser Upload etc.) im PoC.
- Kein Drag **in ShrimpDev hinein** (anderes Kapitel).
- Kein „Move“ (nur Copy-Äquivalent).

## UX-Regeln
- Drag startet **nur** aus Artefakt-Tree (linke Seite).
- Cursor/Feedback: „Copy“ (Standard).
- Wenn Ziel nicht unterstützt → sauber abbrechen, kein Crash.

## Sicherheitsgates
- Drag ist **disabled**, wenn Quelle unter `_Archiv/` liegt (default: blocked).
- Keine Pfade außerhalb Repo/Arbeitsverzeichnis, wenn Resolver nicht eindeutig ist.
- Kein Drag von „intern/sensitiv“ (TODO: Flag/Policy).

## Technische Architektur (Windows/Tkinter)
- PoC bevorzugt `tkinterdnd2` (geringer Integrationsdruck).
- Dependency check + Fallback: Feature bleibt aus, Log-Hinweis.

## Integrationspunkte (später)
- Artefakt-Tree: Hook `on_drag_start`
- Resolver liefert absolute Dateipfade
- Logging über zentrale Log-Schiene

## Testkriterien (DoD)
- Drag einer Datei vom Tree auf Desktop: Copy/Drop ohne Crash.
- Unsupported target: refusal + log.
- `_Archiv/*.bak` bleibt blockiert.
