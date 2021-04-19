Busstops 

In Wildau ist der ÖPNV insbesondere durch den Busverkehr geprägt. Die Bushaltestellen und Buslinien können mithilfe eines additional-files ("osm_stops.add.xml", "busrouten.xml").
Mithilfe von NetEdit können die Bushaltestellen bearbeitet werden, wobei die additional-Datei mit den Stops zusätzlich in NetEdit geladen werden muss. 

Um die Busrouten zu erhalten mussten zunächst die Buslinien mit jedem einzelnen Stop definiert werden ("bustrips.xml").
Hierbei werden die Linien mit den Haltestellen (ID´s der Busstops), der duration (wie lange ein Fahrzeug an der Haltestelle wartet) und der Abfahrtszeit (until). 
Anschließend wurden die Busrouten mithilfe des duaRouter ("duarouter_bus.bat") erzeugt.
Als output-Datei werden die Busrouten erzeugt ("busrouten.xml").  

Um das ganze in SUMO-GUI ausführen zu können müssen die zum einen die Busstops als additional-file und die Busrouten hinter die Fahrzeugrouten-Datei in der Konfigurationsdatei gespeichert werden. 
Beispiel: 

<configuration>
	<input>
		<net-file value="Netzmodell2.net.xml"/>
		<route-files value="flows_SUMOV2.2.rou.xml,busrouten.xml"/>
		<gui-settings-file value="settings.xml"/>
		<additional-file value="osm_stops.add.xml"/>
		
	</input>
	<time>
		<begin value="53990"/>
		<end value="61000"/>
	</time>
</configuration>