# Page-Metadata-Standard v1 (Frontmatter)

**Runner:** R3552  
**Lane:** E (Website / SEO-Netzwerk)  
**Prio:** P2  
**Typ:** DOC  
**Basis:** R3542–R3551  
**Status:** Verbindlich (v1)  
**Stand:** 2026-01-17

---

## Zweck
Dieses Dokument definiert ein einheitliches **Frontmatter/Metadata-Schema** für alle Seiten.
Damit können später:
- Generatoren (Skeleton/Export)
- Sitemaps
- Index-Checks
- Release-Workflows
einfach automatisiert werden.

---

## Format
- YAML Frontmatter am Anfang der Markdown-Datei
- Keine verschachtelten Strukturen (MVP), nur flache Keys + simple Listen

---

## Pflichtfelder (MVP)

| Feld | Typ | Beispiel | Zweck |
|---|---|---|---|
| title | string | "Notion vs Obsidian: Welche Wahl passt zu dir?" | Seitentitel |
| slug | string | "notion-vs-obsidian" | URL/Path |
| category | string | "Notizen & Wissen" | Hub/Cluster |
| type | enum | comparison / alternatives / buy_or_skip | Seitenart |
| status | enum | draft / review / published | Workflow |
| last_updated | date | "2026-01-17" | Aktualität |
| intent | enum | decision / switch / doubt | Suchintention |
| monetization | enum | none / affiliate / own_product / mixed | Regel-Check (R3543) |

---

## Optionale Felder (MVP+)

| Feld | Typ | Beispiel | Zweck |
|---|---|---|---|
| description | string | "Ehrlicher Vergleich..." | Meta description |
| tags | list[str] | ["notizen","wissen"] | interne Filter |
| related | list[str] | ["alternativen-zu-notion"] | interne Links (optional) |
| canonical | string | "" | falls nötig |
| created | date | "2026-01-17" | Audit/History |

---

## Beispiel: comparison
```yaml
---
title: "Notion vs Obsidian: Welche Wahl passt zu dir?"
slug: "notion-vs-obsidian"
category: "Notizen & Wissen"
type: "comparison"
status: "draft"
intent: "decision"
monetization: "mixed"
description: "Vergleich mit klarer Entscheidungsmatrix: Für wen Notion passt, für wen Obsidian passt – und wann keines sinnvoll ist."
created: "2026-01-17"
last_updated: "2026-01-17"
tags: ["notizen","wissen","produktivität"]
related: ["alternativen-zu-notion"]
---
```

## Beispiel: alternatives
```yaml
---
title: "Alternativen zu Notion: Was passt besser zu deinem Setup?"
slug: "alternativen-zu-notion"
category: "Notizen & Wissen"
type: "alternatives"
status: "draft"
intent: "switch"
monetization: "mixed"
created: "2026-01-17"
last_updated: "2026-01-17"
tags: ["notizen","wissen"]
related: ["notion-vs-obsidian"]
---
```

## Beispiel: buy_or_skip
```yaml
---
title: "Lohnt sich Zapier? Kaufen oder lassen?"
slug: "zapier-kaufen-oder-lassen"
category: "Automatisierung"
type: "buy_or_skip"
status: "draft"
intent: "doubt"
monetization: "affiliate"
created: "2026-01-17"
last_updated: "2026-01-17"
tags: ["automatisierung"]
---
```

---

## Validierungsregeln (MVP)
- `slug` muss eindeutig sein
- `type` muss zu Template passen (R3544/R3545)
- `status` ist workflow-relevant
- `last_updated` muss gesetzt sein
- `monetization` muss R3543-konform geprüft werden (später automatisierbar)

---

## Versionierung
- v1.0 — Initial durch R3552
