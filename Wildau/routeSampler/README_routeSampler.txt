routeSampler

Ist das Erscheinungsbild von dem Ergebnis von randomTrips, insbesondere die Fahrzeugverteilung in Haupt- und Nebennetz, plausibel kann der routeSampler angewendet werden.
Hierbei können die Zähldaten mit den erzeugten Routen gekoppelt werden.
Zunächst muss hierfür jedoch erneut eine output-Datei (in diesen Beispiel schon vorhanden "edgedata-file_Wildau") erzeugt werden.
Dieser File enthält die Zähldaten, welche erreicht werden sollen. Hierzu wurden die Kanten, die keine Zähldaten hatten, gelöscht.
Der Sampler versucht mithilfe der Routen die Zähldaten der einzelnen Kanten zu erreichen.
Der routeSampler kann in der gleichen batch-Datei aufgerufen werden ("routeSampler.bat").

Gleichzeitigt wird eine separate output-Datei vom Sampler erzeugt und mithilfe des Aufrufes optimize, wird die Generierung optimiert. 
Die Ergebnisse des Samplers können nun über eine neue output-Datei, wobei die Routen die in dem <Output_File> des Sampler stehen, erzeugt und abgeglichen werden.
Ratsam ist es die gesammelten Ergebnisse der output-Daten in einer Excel-Tabelle zu notieren. 

Hinweis: Sollten die gewünschten Zähldaten vom routeSampler nicht erreicht werden bzw. kommt es zu großen Abweichungen, so ist es ratsam mithilfe von randomTrips mehr Routenalternativen zu erzeugen.
Annahme ist, dass der routeSampler eine gewisse Menge an Nachfrage/Routen benötigt, um die gewünschten Zählwerte zu erreichen.
