randomActivityGen 

Das Tool muss zunächst zusätzlich installiert werden. Hierzu müssen anschließend über den Aufruf "pip install -r testing/requirements.txt" und "pipwin install noise" installiert werden.

Mithilfe von randomActivityGen kann die Nachfrage bzw. die Routenwahl innerhalb eines Netzes anhand der Einwohnerzahl erzeugt werden.
Hierbei ist insbesondere der Netz-File ("Netzmodell2.net.xml") wichtig. Dieser wird dem Tool übergeben, wobei in einer separaten Datei die Einwohnerzahl der Stadt definiert werden ("stats.xml").

Nachdem die batch-Datei ("randombatch.bat") ausgeführt worden ist, wird eine output-Datei erstellt, welche im zweiten Schritt dem AcitivityGen ("activitygenbatch.bat").
Jetzt wird eine Routen-Datei erstellt, welche mit dem duaRouter ("duarouter.bat") weiterausgeführt werden kann.
Anschließend können die Ergebnisse vom duaRouter mithilfe einer output-Datei  ausgewertet werden. 
