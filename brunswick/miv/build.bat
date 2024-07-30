%SUMO_LIBRARIES%\utils\patch.exe -N ../osm/BS_detail.osm.xml ../osm/tram4.diff
%SUMO_HOME%\bin\netconvert.exe -c miv.netccfg
python %SUMO_HOME%\tools\tls\tls_csvSignalGroups.py -n netpatch/miv.net.xml -i netpatch/Rudolfplatz_SP33.csv -o netpatch/Rudolfplatz.tll.xml
%SUMO_HOME%\bin\netconvert.exe -c miv2.netccfg
python %SUMO_HOME%\tools\import\gtfs\gtfs2pt.py -n miv.net.xml.gz --gtfs ../gtfs/gtfs_connect-with_low_level_stops_20200514.zip --date 20200514 --begin 97200 --end 172800 --vtype-output "" --skip-access
%SUMO_HOME%\bin\duarouter.exe -c fromgeo.duarcfg
