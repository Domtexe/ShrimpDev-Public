# MVP — Affiliate, Disclosure & Tracking (Comparison Site)

## Ziel
Monetarisierung so vorbereiten, dass die MVP-Seite sofort sauber live gehen kann:
- Affiliate-Links vorbereitet (Shortlist + Fallback)
- Disclosure-Text fertig
- Tracking-Minimum definiert (ohne Overengineering)

---

## 1) Affiliate-Programme — Shortlist

### A) Primär: Offizielle Programme (First Choice)
- **Notion**: Offizielles Partner-/Affiliate-Programm prüfen (falls verfügbar).
- **Obsidian**: Offizielles Partner-/Affiliate-Programm prüfen (falls verfügbar).

> Hinweis: Programme können sich ändern. Für den MVP reicht: „existiert / existiert nicht“ + Anmeldeschritt.

### B) Fallback: Partner-Netzwerke (Second Choice)
Wenn kein offizielles Programm verfügbar ist:
- **Impact**, **Partnerize**, **Awin**, **CJ** (je nach Verfügbarkeit/Region)
- Alternativ: Reseller/Marketplace-Angebote (nur seriöse Quellen)

### C) Worst-Case (MVP bleibt möglich)
Falls kein Affiliate möglich:
- CTA als „Testen/Download“ ohne Affiliate
- KPI bleibt Indexierung/Impressions, Monetarisierung folgt als Iteration

---

## 2) Disclosure (DE) — kurze, MVP-taugliche Variante

### Platzierung
- Direkt **oberhalb der ersten CTA-Buttons/Links** (nach TL;DR)
- Optional nochmal im Footer/FAQ kurz wiederholen

### Textvorschlag (kurz)
**Transparenz-Hinweis:** Einige Links auf dieser Seite sind Affiliate-Links. Wenn du darüber etwas kaufst oder abschließt, erhalte ich ggf. eine Provision. Für dich entstehen keine Mehrkosten.

### Textvorschlag (ultrakurz)
**Hinweis:** Affiliate-Links – ggf. erhalte ich eine Provision, ohne Mehrkosten für dich.

---

## 3) Tracking-Minimum (MVP)

### KPI (Monetization-MVP)
- **Primary KPI:** Erste Indexierung (GSC sichtbar)
- **Secondary (optional):** Erste Klicks auf CTA-Links (nicht zwingend vor Go-Live)

### UTM-Schema (einfach & konsistent)
Für jeden CTA-Link:
- `utm_source=site`
- `utm_medium=affiliate`
- `utm_campaign=notion-vs-obsidian`
- `utm_content=cta1_tldr` (oder cta2_notion_section, cta3_obsidian_section, cta4_fazit)

Beispiel:
- `...?utm_source=site&utm_medium=affiliate&utm_campaign=notion-vs-obsidian&utm_content=cta1_tldr`

### Klickmessung (MVP-Optionen)
**Option 1 (einfach, später):**
- nur UTM + Netzwerk-Reporting (falls Affiliate-Netzwerk Klicks zählt)

**Option 2 (robuster, aber noch ohne Overkill):**
- eigene Redirect-Links (z. B. `/go/notion`), die serverseitig zählen
- *Implementierung später*, aktuell nur als Konzept

---

## 4) Go-Live DoD (MVP)

### Pflicht
- [ ] Disclosure oberhalb der ersten CTA
- [ ] CTA-Links enthalten UTM-Schema
- [ ] Seite ist indexierbar (keine noindex)
- [ ] Title/Description gesetzt
- [ ] Sitemap/Robots (sofern vorhanden) blockieren nicht

### Optional (Iteration 1)
- [ ] Redirect-Links mit Klickzählung
- [ ] FAQ erweitern
- [ ] Vergleichstabelle verbessern

---

## 5) No-Gos (MVP Disziplin)
- Keine 10 Tools listen
- Kein Newsletter
- Kein Tracking-Stack (GA4 etc.) vor dem Proof
- Keine Skalierung auf weitere Seiten vor Indexierung
