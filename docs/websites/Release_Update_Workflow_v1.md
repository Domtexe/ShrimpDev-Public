# Release- & Update-Workflow v1 (Lane E)

**Runner:** R3553  
**Lane:** E (Website / SEO-Netzwerk)  
**Prio:** P2  
**Typ:** DOC  
**Basis:** R3542–R3552  
**Status:** Verbindlich (v1)  
**Stand:** 2026-01-17

---

## Zweck
Dieser Workflow legt fest, wie Seiten von **Draft** zu **Published** werden,
wie Updates dokumentiert werden und wann Reviews stattfinden.
Ziel: Qualität + Vertrauen + Evergreen.

---

## Statusmodell (verbindlich)
- `draft` → wird geschrieben, darf unvollständig sein
- `review` → DoD erfüllt, wartet auf finalen Check
- `published` → live/ready, Update-Notiz gepflegt

Status steht im Frontmatter (`status`) gemäß R3552.

---

## Release-Gates (DoD = Gate 1)
Eine Seite darf nur auf `review`, wenn:
- Template vollständig erfüllt (R3544/R3545)
- TL;DR enthält Entscheidung
- (Vergleich) „Wann keines sinnvoll ist“ vorhanden
- Entscheidungsmatrix vorhanden (Vergleich)
- Alternativen vorhanden
- Monetarisierung (falls vorhanden) R3543-konform platziert
- Update-Notiz-Block vorhanden (R3550)

Eine Seite darf nur auf `published`, wenn zusätzlich:
- Titel + Description sind sinnvoll (R3551)
- Slug stabil und eindeutig (R3551/R3552)
- Interne Links gemäß Link-Plan (R3549) gesetzt (min. 1 sinnvoller Link)
- Kein offensichtlicher Spam/Floskeltext

---

## Update-Regeln (verbindlich)
Wenn sich etwas Relevantes ändert (Preis/Pläne/Features/Empfehlung):
- `last_updated` im Frontmatter aktualisieren
- Update-Notiz ergänzen (Datum + was + warum)
- Wenn Empfehlung kippt: TL;DR & Entscheidungsmatrix anpassen

Wenn nur Rechtschreibung/Format:
- `last_updated` optional (MVP: nicht nötig)
- Update-Notiz optional

---

## Review-Zyklus (MVP)
- Neue Seite nach Veröffentlichung: Review nach 14 Tagen (kurz)
- Danach: alle 90 Tage prüfen (nur wenn nötig updaten)

Trigger für außerplanmäßiges Update:
- Preissprung / Planänderung
- Feature-Änderung, die die Empfehlung beeinflusst
- Häufige Nutzerfrage (FAQ-Abschnitt nötig)

---

## Minimaler Release-Ablauf (praktisch)
1) Draft schreiben (Template folgen)
2) Gate 1: DoD check → Status `review`
3) Finalcheck (Titel/Slug/Links/Monetarisierung) → Status `published`
4) Nach 14 Tagen Kurzreview

---

## Rollen (MVP)
- Autor: schreibt + erfüllt Template
- Reviewer (kann identisch sein): prüft Gates mit Checkliste

---

## Checkliste: Published
- [ ] Template erfüllt
- [ ] TL;DR Entscheidung klar
- [ ] (Vergleich) Kein-sinnvoll-Abschnitt drin
- [ ] Entscheidungsmatrix drin
- [ ] 1–3 Alternativen drin
- [ ] Monetarisierung nach Entscheidung (oder none)
- [ ] Titel/Description/Slug sauber
- [ ] Mind. 1 sinnvoller interner Link
- [ ] Update-Notiz vorhanden

---

## Versionierung
- v1.0 — Initial durch R3553
