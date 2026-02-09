# Nachsorge+ SOP v1 (ShrimpDev / ShrimpHub)

**Status:** kanonisch  
**Scope:** Governance / Hygiene / Konsistenz (kein Bugfix-Prozess)  
**Prinzip:** Read-only Diagnose zuerst, Apply nur kontrolliert.

---

## 1. Zweck

Nachsorge+ ist der standardisierte Prozess zur:

- Systemhygiene & Stabilität
- Governance-Sicherung (MR/DoD/Scope)
- Pipeline-Konsistenz (SSOT)
- Reduktion technischer Schulden
- Früherkennung wiederkehrender Fehler

**Wichtig:** Nachsorge+ ist *kein* Feature-Bau und *kein* Refactoring-Marathon.

---

## 2. Trigger (wann Nachsorge+ läuft)

Nachsorge+ wird durchgeführt bei mindestens einem der folgenden Trigger:

- ≥5–10 neue Runner seit letzter Nachsorge+
- Abschluss eines Feature-Blocks / Subsystems
- vor Releases/Version-Marken
- Häufung von FAIL/WARN in Reports
- subjektivem „Unordnungsgefühl“ / zunehmender Reibung
- längeren Entwicklungssessions (mehrere Stunden)
- Architektur- oder Governance-Änderungen

---

## 3. Grundprinzipien (MR-konform)

1. **Diagnose vor Aktion**
2. **Read-Only zuerst**
3. **Pipeline ist SSOT**
4. **Minimal-invasives Vorgehen**
5. **Alles erzeugt Reports**
6. **Keine stillen Änderungen**
7. **Apply nur mit Zustimmung / Token / Dedupe**

---

## 4. Ablauf (3 Phasen)

| Phase | Typ | Pflicht |
|------|-----|--------|
| Phase 1 – Diagnose | Read-Only | ✅ |
| Phase 2 – Bewertung | Analyse | ✅ |
| Phase 3 – Apply | Kontrolliert | Optional |

---

## 5. Phase 1 – Diagnose (Read-Only)

### 5.1 Report-Analyse

**Ziel:** Muster erkennen.

Prüfen:
- FAIL/WARN-Cluster
- wiederkehrende Fehler/Keywords
- ExitCode-Häufungen
- betroffene Module/Flows
- zeitliche Korrelationen

Output:
- Cluster-Summary
- Top-Hotspots (Top 3–10)
- Risikoindikatoren

---

### 5.2 Pipeline-Audit

Prüfen:
- Tasks ohne Owner/Status
- Phantom-Runner-IDs (referenziert, aber Artefakte fehlen)
- veraltete P0/P1 (nicht mehr P0-relevant)
- doppelte Tasks / Drift

Output:
- Pipeline-Audit-Report (mit Empfehlungen: P0/P1/P2/skip/archived)

---

### 5.3 MR-Compliance-Check

Prüfen:
- Fix ohne Diagnose?
- APPLY ohne Docs („Docs not needed“ fehlt)?
- Runner ohne Report/Verifikation?
- Scope-Leaks / unsichere Anchors?

Output:
- MR-Compliance-Summary (OK / Findings / Actions)

---

### 5.4 Changelog-Sync

Prüfen:
- Runner seit letztem Eintrag ohne Changelog
- größere Änderungen ohne Log-Eintrag
- veraltete Einträge / falsche Referenzen

Output:
- Changelog-Sync-Hinweise

---

### 5.5 Architektur-Drift

Prüfen:
- neue Module/Contracts undocumented
- veraltete Architektur-Aussagen
- inkonsistente Pfade / canonical path drift
- neue Governance-Prinzipien nicht verankert

Output:
- Architektur-Drift-Hinweise

---

## 6. Phase 2 – Bewertung (Auto-Priorisierung)

Alle Findings klassifizieren:

| Kategorie | Bedeutung |
|--------|-----------|
| Kritisch | Pipeline P0 |
| Relevant | Pipeline P1/P2 |
| Kosmetik | Sammelliste |
| Obsolet | skip/archived |

Ergebnis:
- Top-5 Maßnahmenliste
- Priorisierungsempfehlung
- Risiko-Score

---

## 7. Phase 3 – Apply (Optional, kontrolliert)

Nur mit expliziter Zustimmung.

Erlaubt:
- genau **ein** Pipeline-Eintrag (oder ein definierter kleiner Batch)
- dedupe-sicher
- Backup vor Änderung
- voller Report danach

Verboten:
- Massenänderungen
- Scope-fremde Fixes
- stille Korrekturen

---

## 8. Output-Pflicht

Jede Nachsorge+ erzeugt mindestens:
- Summary-Report (Timestamp, Runner-ID, Scope)
- Risiko-Score
- Top-5 Maßnahmen
- Next-Step-Empfehlung (DIAG/APPLY)

---

## 9. Frequenz (Empfehlung)

| Intensität | Rhythmus |
|--------|---------|
| Leicht | alle 5–10 Runner |
| Standard | wöchentlich |
| Intensiv | vor Releases |
| Voll | monatlich |

---

## 10. Erfolgsindikatoren

Nachsorge+ ist erfolgreich, wenn:
- weniger wiederkehrende Fehler
- stabilere Pipeline/Prioritäten
- weniger Chaos-Fixes
- höhere Planbarkeit
- konsistentere Docs/Governance

---

## 11. Abgrenzung

Nachsorge+ ist **nicht**:
- Bugfix-Runner
- Refactoring-Marathon
- Rewrite-Ausrede
- Feature-Entwicklung

---

## 12. Versionierung

- v1 = Grundstandard
- Änderungen sind dokumentationspflichtig (Changelog/MR, je nach Scope)
