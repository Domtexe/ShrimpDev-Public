# Clarivoo — Deploy-Plan (Static Site) mit Hugo + netcup

## Warum überhaupt HTML?
- Webhosting liefert **HTML/CSS/JS** aus.
- Markdown (**.md**) ist **Quelle**, nicht Auslieferungsformat.
- Lösung: **Markdown → Generator → HTML → Upload**.

---

## Entscheidung: Generator
### Empfehlung: **Hugo**
Warum Hugo (für euch):
- Single-Binary (kein Node-Ökosystem nötig)
- Sehr schnell, stabil, gut für „wenig Wartung“
- Markdown-first, ideal als „Source of Truth“

Alternativen (nur der Vollständigkeit halber):
- 11ty (Node) – gut, aber Toolchain schwerer
- Astro – overkill fürs MVP
- WordPress – bewusst **nicht** (Wartung/Security/Scope)

---

## Zielzustand (Soll)
- Eure Inhalte bleiben in Markdown (Source of Truth)
- Build erzeugt:
  - `index.html`
  - `orientierung/index.html`
  - `vergleiche/notion-vs-obsidian/index.html`
  - `wissen/grundlagen/index.html`
  - `ueber/index.html`
- Upload zu netcup in den Webroot (meist `htdocs/`)

---

## Ordner- & URL-Design (empfohlen)
**Aktuell (Quelle):**
`docs/websites/clarivoo/`
- index.md
- orientierung.md
- vergleiche_pilot.md
- wissen_guide.md
- ueber.md
- SITE_MAP.md

**Ziel (Website URLs):**
- `/` (Start)
- `/orientierung/`
- `/vergleiche/notion-vs-obsidian/`
- `/wissen/grundlagen/`
- `/ueber/`

---

## Minimaler Hugo-Setup-Plan (ohne Theme-Abhängigkeit)

### 1) Hugo-Projekt anlegen (lokal)
- Ordner z. B.: `clarivoo_site/`
- Struktur:
  - `content/`
  - `layouts/`
  - `static/`
  - `hugo.toml`
  - `public/` (Build Output)

### 2) Inhalte aus euren Markdown-Dateien übernehmen
Mapping:
- `docs/websites/clarivoo/index.md` → `content/_index.md`
- `orientierung.md` → `content/orientierung/_index.md`
- `vergleiche_pilot.md` → `content/vergleiche/notion-vs-obsidian/_index.md`
- `wissen_guide.md` → `content/wissen/grundlagen/_index.md`
- `ueber.md` → `content/ueber/_index.md`

Hinweis:
- In Hugo ist `_index.md` für „Section/Folder Pages“ ideal.

### 3) Minimal-Layouts bauen (2 Dateien reichen)
- `layouts/_default/baseof.html`
- `layouts/_default/single.html` (oder `list.html` wenn gebraucht)

Ziel:
- saubere HTML-Struktur, Navigation, Footer
- später leicht erweiterbar

### 4) Build
- `hugo` (oder `hugo -D` für Drafts)
- Output landet in `public/`

---

## netcup Upload (Webhosting)
### Webroot
Bei netcup Webhosting typischerweise:
- `htdocs/` ist Webroot
(Details hängen vom Paket ab – im CCP/FTP sieht man den Zielordner)

### Upload-Methoden
- FTP (einfach)
- SFTP/SSH (wenn verfügbar, besser)
- File Manager im CCP (notfalls)

**Upload-Ziel:**
- Inhalt von `public/` nach `htdocs/` (oder entsprechende Domain-Docroot)

---

## Go-Live Checkliste (kurz & hart)
1. Domain zeigt aufs Hosting (DNS ok)
2. SSL aktiv (Let’s Encrypt im netcup Panel)
3. `index.html` erreichbar
4. Unterseiten:
   - `/orientierung/`
   - `/vergleiche/notion-vs-obsidian/`
   - `/wissen/grundlagen/`
   - `/ueber/`
5. 404 getestet (nicht kritisch, aber gut)
6. Optional:
   - `robots.txt` minimal
   - `sitemap.xml` (Hugo kann das automatisch)

---

## Monitoring / Messbarkeit (ohne Overkill)
- Google Search Console einrichten (Domain Property)
- Abdeckung/Indexierung beobachten
- Keine Tracker/Ads in dieser Phase

---

## Nächster Runner (wenn du willst)
APPLY:
- Hugo-Projektstruktur erstellen (separater Ordner, nicht in ShrimpDev-Core)
- Inhalte automatisch mappen/kopieren
- Minimal-Layouts + Build-Script
- Optional: Upload-Script (SFTP) – nur wenn SSH verfügbar

Wichtig:
- Keine Public-Repos nötig
- Alles bleibt lokal + Hosting in DE
