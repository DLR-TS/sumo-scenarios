#!/bin/bash
netconvert -c miv.netccfg
netconvert -c miv2.netccfg
if which python3; then
    PYTHON=python3
else
    PYTHON=python
fi
$PYTHON $SUMO_HOME/tools/import/gtfs/gtfs2pt.py -n miv.net.xml.gz --gtfs ../gtfs/gtfs_connect-with_low_level_stops_20200514.zip --date 20200514 --begin 97200 --end 172800
duarouter -c fromgeo.duarcfg
