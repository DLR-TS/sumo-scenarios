cadyts 

Eine weitere Möglichkeit der Routenwahl anhand von Zähldaten und Routenalternativen bietet das Tool „cadyts“.
Cadyts führt 100 Iterationsschritte durch, bei denen die Wahrscheinlichkeiten der Routenwahl aus einer Routendatei versucht werden an die Zähldaten anzupassen.
Hierzu werden in jedem Iterationsschritt die Ergebnisse der vorherigen Iteration ausgewertet und die Wahrscheinlichkeiten werden ggf. angepasst um nahe an die Zähldaten zu gelangen.
Um cadyts ausführen zu können muss jedoch zunächst eine batch-Datei ("cadyts.bat") angelegt werden, wobei zuerst duaIterate ("duaIterate.bat") ausgeführt werden muss.
DuaIterate erstellt für jede Iteration (die Anzahl der Iterationen ist abhängig vom Zeitslot) eine alternative Routendatei, die dann cadyts übergeben wird. 

Hinweis: Der Pfadname in den cadyts.bat muss an den eigenen Pfad angepasst werden. 

Cadyts benötigt die Zähldaten im Format einer measurements-Datei ("measurements.xml").

Anschließend kann eine output-Datei erstellt werden. 
