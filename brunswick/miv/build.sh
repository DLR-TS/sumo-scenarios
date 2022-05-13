#!/bin/bash
if which python3 &> /dev/null; then
    PYTHON=python3
else
    PYTHON=python
fi
netconvert -c miv.netccfg
#$PYTHON $SUMO_HOME/tools/tls/tls_csvSignalGroups.py -n netpatch/miv.net.xml -i netpatch/Rudolfplatz.csv -o netpatch/Rudolfplatz.tll.xml
$PYTHON $SUMO_HOME/tools/tls/tls_csvSignalGroups.py -n netpatch/miv.net.xml -i netpatch/Rudolfplatz_SP33.csv -o netpatch/Rudolfplatz.tll.xml
netconvert -c miv2.netccfg
$PYTHON $SUMO_HOME/tools/import/gtfs/gtfs2pt.py -n miv.net.xml.gz --gtfs ../gtfs/gtfs_connect-with_low_level_stops_20200514.zip --date 20200514 --begin 97200 --end 172800
duarouter -c fromgeo.duarcfg
