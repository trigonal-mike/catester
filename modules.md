Allowed/Disallowed Modules:
Ich hab mir angesehen wie ich alle importierten Module(-Names) bekomme,
das funktioniert gut, die Frage ist ob rekursiv im import tree gesucht werden soll, oder nicht.
Falls rekursiv, dann bekomme ich wirklich alle module:
zb: import json #importiert insg. 15 Module (json, json.decoder, json.encoder, json.scanner, re, enum, usw...)
oder numpy importiert insg. 176, und matplotlib importiert insg. 338 Module
In diesem Fall wäre eigentlich nur die disallowed-List hilfreich.

Nicht rekursiv bekomme ich "nur" die Module, die vom Entry-File importiert werden.
=================================
ex.py (abgabe file):
import add1

add1.py (additional file)
import disallowed_module
=================================
hier, wenn ich nicht-rekursiv suche bekomme ich nur ["add1"] als Module-Liste zurück

Zwei gute Möglichkeiten sehe ich für das test.yaml:
1.) nur "disallowedModules" und immer rekursiv suchen
2.) "allowedModules" und "disallowedModules" UND searchRecursive (bool)

Was sagt ihr? 1 oder 2?
Andere Vorschläge (auch bzgl. Naming) gerne willkommen.

