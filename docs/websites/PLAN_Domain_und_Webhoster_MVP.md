# Plan — Domain & Webhoster (MVP, DE/EU)

## Leitplanken (fix)
- ShrimpDev-Repo bleibt **privat**
- Öffentlich ist **nur eine einzelne Seite**
- Kein automatisches Deploy aus ShrimpDev
- Jeder Schritt ist reversibel

---

## 1) Domain-Strategie (MVP-tauglich)

### Ziel
- Brand-neutral
- austauschbar
- kein langfristiges Commitment

### Empfohlene Muster
- `<thema>-vergleich.de`
- `<thema>-check.de`
- `<thema>-guide.de`

**Beispiele (nur Muster):**
- `notizen-vergleich.de`
- `tools-vergleich.de`
- `produktivitats-tools.de`

### TLD-Empfehlung
- **.de** (Vertrauen, Fokus)
- **.com** nur, wenn .de belegt ist

### No-Gos
- Fantasienamen
- Marken im Domainnamen
- Shrimp/ShirmDev/Brand-Namen

---

## 2) Webhoster — Shortlist (DE/EU)

### A) Sehr konservativ (Shared Hosting)
**Geeignet für:** statische Seite oder 1 WP-Seite
- all-inkl.com
- netcup
- IONOS (nur kleine Pakete)

**Warum:**
- günstig
- DSGVO-freundlich
- klassische Webspace-Modelle
- kein Zwang zu Baukästen

### B) Etwas technischer (aber sauber)
- Uberspace (DE)
- Hetzner Webhosting

**Warum:**
- mehr Kontrolle
- kein Vendor-Lock-in
- trotzdem MVP-tauglich

### Nicht empfohlen (für MVP)
- Baukästen (Wix, Jimdo)
- Server/VPS
- Cloud-Overkill

---

## 3) Technische Minimal-Architektur

### Variante 1 — Statisch (empfohlen)
- 1× `index.html` oder `index.php`
- optional 1× CSS-Datei
- Inhalte aus MVP-Dokumenten kopiert

**Vorteile:**
- keine Updates
- kein Angriffspunkt
- extrem stabil

### Variante 2 — Minimal-WordPress
- 1 Seite
- kein Blog
- max. 1–2 Plugins

**Nur wenn:** du Inhalte öfter ändern willst.

---

## 4) Trennung ShrimpDev ↔ Website (wichtig)

### Empfohlen
- **separater Ordner / separates Mini-Repo**
- manuelles Kopieren/Deploy
- keine Verbindung zu ShrimpDev-Tools

### Explizit verboten
- CI/CD aus ShrimpDev
- Public Mirrors
- automatische Syncs

---

## 5) MVP-Go-Live Checkliste

- [ ] Domain registriert
- [ ] Webspace aktiv
- [ ] SSL aktiv
- [ ] Seite erreichbar
- [ ] robots.txt erlaubt Indexierung
- [ ] Impressum/Datenschutz vorhanden
- [ ] eine Seite, nicht mehr

---

## 6) Entscheidungsregel
Erst wenn:
- Seite indexiert ist
- erste Impressionen sichtbar sind

… wird über:
- zweite Seite
- Branding
- Automatisierung
nachgedacht.

Bis dahin: **eine Seite, Ruhe bewahren**.
