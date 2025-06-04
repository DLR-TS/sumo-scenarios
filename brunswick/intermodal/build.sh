#!/bin/bash
netconvert -c intermodal_pre.netccfg
netconvert -c intermodal.netccfg
duarouter -c fromgeo.duarcfg
$PYTHON $SUMO_HOME/tools/import/gtfs/gtfs2pt.py -n intermodal.net.xml.gz --gtfs ../gtfs/gtfs_connect-with_low_level_stops_20200514.zip --date 20200514 --begin 97200 --end 172800 --vtype-output "" --skip-access --stops intermodal_stops.add.xml

