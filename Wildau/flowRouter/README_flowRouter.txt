flowRouter
Ein weiteres Tool für die Routengenerierung bzw. die Generierung von Verkehrsflüssen ist der flowRouter. Dieser wird in einer batch-Datei aufgerufen ("flowRouter.bat"). 

Dem flowRouter wird die Netzdatei sowie eine Detektor-Datei übergeben. Die Detektor-Datei ("detectors.xml") beinhaltet definierte Schleifen, wobei die Anzahl an Fahrzeugen die diese Schleife passiert haben angegeben werden. 

Beim type wird angegeben, ob es sich um eine Kante innerhalb des Netzes oder um eine Kante, wo Verkehr zu- bzw. abfließt handelt.

Als output-Dateien werden die Routen und Flows generiert, nachdem die batch-Datei ausgeführt worden ist.
Anschließend kann wieder eine output-Datei erstellt werden (siehe oben), um input und ouput zu vergleichen (übertragen in Excel-Tabelle).
Wichtig bei der (output)batch-Datei ist, dass bei dem Routen-File auch der Flow-File mit „,“ dazwischen übergeben wird. 
