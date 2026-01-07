<!-- LEGACY_NON_CANONICAL -->
**⚠️ Legacy / Nicht-kanonisch** (gesetzt: 2025-12-24 00:04:38)  
Kanonisch: `docs/PIPELINE.md`  
Bitte diese Datei nicht mehr als Quelle verwenden.

---

# Report R2405 – Pipeline Update (Auto)

- Timestamp: 2025-12-20 00:05:32
- Root: `C:\Users\rasta\OneDrive\ShrimpDev`
- Target: `C:\Users\rasta\OneDrive\ShrimpDev\docs\PIPELINE.md`

- backup: `C:\Users\rasta\OneDrive\ShrimpDev\_Archiv\PIPELINE.md.R2405_20251220_000532.bak`
- sha256 before: `235108498b1e3151384aecd376c598d2a4a57b52a3e82f3c1cfce9a4149f67d2`
- sha256 after: `3c7f2a4912e000be4822fd70dd57ebf6a55780c7ea5a7ed16b541e6954a87cc4`

## Added tasks
- Artefakte/Popup „intern anzeigen“: Button „Quelle kopieren“ (Datei-INHALT in Zwischenablage, nicht Pfad).
- SingleWriter: Finaler Audit – keine direkten ShrimpDev.ini Overwrites mehr (config_loader/config_mgr/ui_toolbar etc.).
- SingleWriter: optional Guard-Runner bauen, der direkte INI-Writes in Zukunft als Pipeline-Warnung meldet.
- Docking/Geometry: Drift & Centering final fix (R2404 auswerten, dann minimaler Patch nur am echten Post-Restore Setter).
- Docking/Geometry: kurzer Smoke-Test-Runner (Start/Restart, Fensterpositionen vergleichen, Report).
- Doku/Architektur: Docking-stabil + SingleWriter-Delegation (R2402/R2403) sauber dokumentieren (Architektur + Troubleshooting).
- Doku: Report-Index/Changelog-Eintrag für DockingStable Snapshot (R2398) + relevante Reports verlinken.
