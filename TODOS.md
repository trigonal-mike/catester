## sandboxing:
- Wie kann das sinnvoll umgesetzt werden?
- Wie wird das in matlab gemacht?
- Wie kann/soll das in python gemacht werden?
- os.chroot würde sich anbieten, aber das geht nur mit root-Rechten, welche der test-worker (lt. Max) nicht haben darf!?
- jede einzelne Funktion "die raus kann" zu patchen, ist denke ich (viel) zu großer Aufwand

## Erweiterungen:
- Was soll geändert/hinzugefügt werden?

## readme.md:
- Klare Anleitung, was die test-engine kann, welche Einstellungen getroffen werden können,
Beispiele für unterschiedliche Test-Szenarien (=> "doc"-Folder)

## Einstellungen:
- verbosity ist zzt (noch) nicht ideal einstellbar

## Allowed/Disallowed Modules:
- moduleBlacklist ist umgesetzt
- eine whiteList ist nicht praktisch, weil zb. numpy insg. 176, und matplotlib insg. 338 weitere Module benötigt/importiert

## sonstiges folgt...