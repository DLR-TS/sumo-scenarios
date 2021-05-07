Busstops

In Wildau the local public transport is particularly characterized by bus traffic. The bus stops and bus routes can be accessed using an additional file ("osm_stops.add.xml", "busrouten.xml").
The bus stops can be edited using NetEdit, where by the additional file with the stops must also be loaded into NetEdit.

In order to get the bus routes, the bus routes had to be defined first with each individual stop ("bustrips.xml").
The lines are shown with the stops (IDs of the bus stops), the duration (how long a vehicle waits at the stop) and the departure time (until).
The bus routes were then generated using the duaRouter ("duarouter_bus.bat").
The final bus routes are generated as an output file ("busrouten.xml").

In order to be able to do the whole thing in SUMO-GUI, on the one hand the bus stops must be saved as an additional file and the final bus routes should be written behind the vehicle route file in the configuration file.
Example:
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