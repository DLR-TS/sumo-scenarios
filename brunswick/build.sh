# Step 0: installing tools
#wget -O - http://m.m.i24.cc/osmfilter.c |cc -x c - -O3 -o osmfilter
#wget -O - http://m.m.i24.cc/osmconvert.c | cc -x c - -lz -O3 -o osmconvert
TSC_HOME=$HOME/tsc
SCENARIO_HOME=$HOME/git/sumo-scenarios

# Step 1: preparing OSM Brunswick
pushd $SCENARIO_HOME/brunswick/miv
$SUMO_HOME/tools/osmGet.py -b 10.462365,52.193273,10.601086,52.332196 -p ../osm/BS_detail
./build.sh
popd

# Step 2: preparing OSM Test Field Lower Saxony
# first you may want to check the boundary available as GeoJSON at ../TestfeldNDS/osm/TestfeldNDS.umap
$SCENARIO_HOME/TestfeldNDS/osm/TestfeldNDS.py

# Step 3: TAPAS preparation
cd $TSC_HOME
./install_scenario_templates.py -c athene.tsccfg -p ~/git/sumo-scenarios

# Step 3: TAPAS (this is the current simkey for KoFiF 2030 reference scenario)
./tsc_main.py --sim-key 2022y_01m_26d_14h_31m_26s_378ms -c athene.tsccfg --sim-param SUMO_DESTINATION_FOLDER:testfield

# Step 4: cutRoutes
cd $SCENARIO_HOME/brunswick
time $SUMO_HOME/tools/route/cutRoutes.py --orig-net $TSC_HOME/scenario_workdir/testfield/net.net.xml.gz --speed-factor 0.7 --min-length 2 --trips-output miv/bs_miv_cut.trips.xml miv/miv.net.xml.gz $TSC_HOME/scenario_workdir/testfield/iteration000/oneshot/vehroutes_oneshot_meso.rou.xml --min-air-dist 100 -d keep

# Step 5: convert to geo-trips:
duarouter -c miv/trips2geo.duarcfg

# the geo trips in miv/bs_miv_cut.geotrips.xml.gz are the final result of the process
# because they can be mapped "universally" to a new network
# -----------------------------------------------------------------------------------------------------

#  now some optional points to go from here
# Step 6a: modify network / prepare custom simulation then recreate the net and mapped trips by running
cd $SCENARIO_HOME/brunswick/miv
./build.sh

# or Step 6b: choose smaller subnetwork
cd $SCENARIO_HOME/brunswick
netconvert -s miv/miv.net.xml.gz --keep-edges.in-geo-boundary 10.521967,52.249556,10.585906,52.319634 -o miv/detail.net.xml.gz
time $SUMO_HOME/tools/route/cutRoutes.py --orig-net $TSC_HOME/scenario_workdir/testfield/net.net.xml.gz --speed-factor 0.7 --min-length 2 --trips-output miv/detail.rou.xml \
 --min-air-dist 100 -a miv/gtfs_publictransport.add.xml --stops-output miv/pt_stops_detail.add.xml --pt-input miv/gtfs_publictransport.rou.xml --pt-output miv/pt_detail.rou.xml \
 miv/detail.net.xml.gz $TSC_HOME/scenario_workdir/testfield/iteration000/oneshot/vehroutes_oneshot_meso.rou.xml
sumo -n miv/detail.net.xml.gz -r miv/detail.rou.xml -a miv/vtypes.xml,miv/pt_stops_detail.add.xml,miv/pt_detail.rou.xml -C detail.sumocfg
