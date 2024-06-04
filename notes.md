- sandboxing:
Wie kann das sinnvoll umgesetzt werden?
Wie wird das in matlab gemacht?
Wie kann/soll das in python gemacht werden?
os.chroot würde sich anbieten, aber das geht nur mit root-Rechten, welche der test-worker (lt. Max) nicht haben darf!?
jede einzelne Funktion "die raus kann" zu patchen, ist denke ich (viel) zu großer Aufwand

- localTests:
Hier habe ich schon ein paar Erfahrungen/Wünsche der Tutoren gesammelt.
zzt. ist das (in python) nicht ganz ideal, vor allem bei zusätzlich (zu correct und empty) definierten Lösungen muss immer gut aufgepasst werden,
dass erzeugte/geänderte Files (zb test.yaml, additional-files, ...) rüberkopiert werden. Da könnte sicher einiges besser automatisiert/strukturiert werden.

- localTests - Struktur:
Die Ordner Struktur wäre (jedenfalls für python) zu überdenken,
vor allem bei Assignments, die Scripte vorangegangener Wochen verwenden sollen, ist das zzt. recht tricky.

- Erweiterungen:
Was soll geändert/hinzugefügt werden?
zb. Variable-Test nur auf Value und nicht auf type und shape zu testen (natürlich optional, für solche Fälle wo Lösungen zb mittels numpy einen anderen type ergeben, aber auch korrekte Ergebnisse sind, das geht zzt. nur mit dem setupcode, welcher eine Lösungsvariable umwandelt und dann diese vergleicht)

- readme.md:
Klare Anleitung, was die test-engine kann, welche Einstellungen getroffen werden können,
Beispiele für unterschiedliche Test-Szenarien (=> "doc"-Folder)

- Einstellungen:
verbosity ist zzt (noch) nicht ideal einstellbar
