#!/bin/bash
# we currently work with the manually edited net so no net building here
#$SUMO_HOME/bin/netconvert -c defaults/osm.netccfg
#$SUMO_HOME/bin/netconvert -c patched.netccfg
$SUMO_HOME/bin/polyconvert -c defaults/osm.polycfg -n osm_edited.net.xml.gz
#python "$SUMO_HOME/tools/ptlines2flows.py" -n osm.net.xml -e 3600 -p 600 --random-begin --seed 42 --ptstops osm_stops.add.xml --ptlines osm_ptlines.xml -o osm_pt.rou.xml --ignore-errors --vtype-prefix pt_ --stopinfos-file stopinfos.xml --routes-file vehroutes.xml --trips-file trips.trips.xml --min-stops 0 --extend-to-fringe --verbose
#python "$SUMO_HOME/tools/randomTrips.py" -n osm_edited.net.xml.gz --fringe-factor 5 -p 0.685790 -o osm.passenger.trips.xml -e 3600 --vehicle-class passenger --vclass passenger --prefix veh --min-distance 300 --trip-attributes "departLane=\"best\"" --fringe-start-attributes "departSpeed=\"max\"" --allow-fringe.min-length 1000 --lanes --validate
