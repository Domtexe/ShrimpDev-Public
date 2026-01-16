<!-- R3511_POLICY_BLOCK -->
# Runner-Referenz-Policy (aktiv vs. historisch)

## Problem, das wir ab jetzt verhindern
Runner-IDs tauchen in Pipeline/Docs/Reports auf, obwohl die zugehörigen Runner-Dateien (cmd/py) ggf. nicht mehr existieren.
Das erzeugt Phantom-Blocker und Reparatur-Kaskaden.

## Kanonische Regeln
1. **Aktiv** = Runner-Dateien existieren im Repo (typisch `tools/R####.cmd` + `tools/R####.py`) *und* sind bewusst in Nutzung.
2. **Historisch/Archiv** = Referenz existiert nur in Docs/Reports/Backups/Archiv, aber nicht als aktiver Runner.
3. **Phantom** = Pipeline/Docs referenzieren Runner-IDs, aber es gibt keine Runner-Artefakte → darf nicht als “P0 Blocker” behandelt werden, bis materialisiert.

## Diagnose-Standard (MR-konform)
- Vor jedem Fix: **rekursiver Scan** (z. B. R3510) → Dateien + Content-Referenzen.
- Erst danach: Entscheidung **(A)** materialisieren **oder** **(B)** Pipeline-Eintrag archivieren/downgraden.

## Aktueller Stand (aus Scan)
- Betroffene IDs: R2370, R2374, R2375, R2377, R2378, R2379
- Referenz: R3510 report/json in Reports (recursive reference scan).

<!-- R3511_POLICY_BLOCK -->

