# Templates (Single Source of Truth)

Diese Templates sind verbindlich für neue Runner.

## Pflicht-Output (CMD)
- START-Block mit Trennern
- Root-Ausgabe
- ExitCode-Block
- Report-Hinweis

## Pflicht-Output (PY)
- schreibt Report in Reports/
- gibt Report-Pfad per print() aus

## Anti-Regression
- Neue Runner sollen aus diesen Templates erstellt werden.
- Wenn Output wieder 'hohl' wird: Output-Guard laufen lassen.

## Batch-Sonderzeichen (wichtig)
In .cmd-Dateien müssen Sonderzeichen in `echo` escaped werden:
- `&` als `^&`
- `|` als `^|`
- `>` als `^>` und `<` als `^<`
Sonst interpretiert CMD das als Befehlsverkettung/Redirect.
