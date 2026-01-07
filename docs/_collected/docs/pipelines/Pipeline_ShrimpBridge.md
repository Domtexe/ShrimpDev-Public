# Pipeline – ShrimpBridge

Status: **IDEA / PARKED**

## Vision
Ein Tool, das Playlists (und später ggf. weitere Library-Objekte) von **Spotify → Deezer** übertragen kann, mit hoher Trefferquote, sauberem Logging und Report-Ausgabe.

## MVP (Phase 1)
- Spotify OAuth Login
- Deezer OAuth Login
- Spotify Playlists listen + Auswahl
- Tracks aus gewählten Playlists auslesen
- Deezer Track-Suche (Artist/Title/Album) + best-effort Match
- Deezer Playlists anlegen/befüllen
- Report: gefunden / nicht gefunden / Mehrdeutig / Duplikate
- Robustheit: Rate-Limits, Retries, Abbruch-resume (einfach)

## Match-Strategie (Start)
1. Wenn verfügbar: **ISRC**
2. Sonst: Normalisierung (lowercase, feat.-Strip, Klammern/Remaster entfernen) + Fuzzy Match
3. Tie-breaker: Dauer (±2–3s), Album (optional)

## Risiken / offene Punkte
- API-Limits + Token-Lifetime (Spotify/Deezer)
- Trefferquote bei Remaster/Live/feat.-Schreibweisen
- Deezer API-Abdeckung je Objekt (Likes/Library evtl. eingeschränkt)

## Definition of Done (MVP)
- Eine beliebige Spotify-Playlist lässt sich reproduzierbar nach Deezer übertragen
- Report-Datei wird erzeugt und ist nachvollziehbar
- Fehlertoleranz: sinnvolle Retries/Backoff, keine Crash-Kaskaden

## Nächste Schritte (wenn aktiv)
- POC: 1 Playlist, 50 Tracks
- Reports: CSV + Markdown
- GUI/CLI Entscheidung (später: ShrimpHub-Integration möglich)
