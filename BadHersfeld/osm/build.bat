"%SUMO_HOME%/bin/polyconvert" -c defaults/osm.polycfg -n osm_edited.net.xml.gz
python "%SUMO_HOME%/tools/randomTrips.py" -n osm_edited.net.xml.gz --fringe-factor 5 -p 0.685790 -o osm.passenger.trips.xml -e 3600 --vehicle-class passenger --vclass passenger --prefix veh --min-distance 300 --trip-attributes "departLane=\"best\"" --fringe-start-attributes "departSpeed=\"max\"" --allow-fringe.min-length 1000 --lanes --validate

