# Step 0: installing tools
#wget -O - http://m.m.i24.cc/osmfilter.c |cc -x c - -O3 -o osmfilter
#wget -O - http://m.m.i24.cc/osmconvert.c | cc -x c - -lz -O3 -o osmconvert
TSC_HOME=$HOME/tsc
SCENARIO_HOME=$HOME/git/sumo-scenarios

# Step 1: preparing OSM Brunswick
cd $SCENARIO_HOME/brunswick
$SUMO_HOME/tools/osmGet.py -b 10.462365,52.193273,10.601086,52.332196 -p osm/BS_detail
netconvert -c miv/miv.netccfg

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
time $SUMO_HOME/tools/route/cutRoutes.py --orig-net $TSC_HOME/scenario_workdir/testfield/net.net.xml.gz --speed-factor 0.7 --min-length 2 --trips-output miv/bs_miv_cut.trips.xml.gz miv/miv.net.xml $TSC_HOME/scenario_workdir/testfield/iteration000/oneshot/vehroutes_oneshot_meso.rou.xml --min-air-dist 100

# Step 5: convert to geo-trips:
duarouter -c miv/trips2geo.duarcfg

# Step 6: run simulation
sumo -c miv/oneshot.sumocfg


#  now some optional points to go from here
# Step 7a: modify network / prepare custom simulation
#netconvert -c bs_miv_detail.netccfg
#duarouter -c fromgeo.duacfg

# or Step 6b: choose smaller subnetwork
cd $SCENARIO_HOME/brunswick
netconvert -s miv/miv.net.xml --keep-edges.in-geo-boundary 10.521967,52.249556,10.585906,52.319634 -o miv/detail.net.xml
time $SUMO_HOME/tools/route/cutRoutes.py --orig-net $TSC_HOME/scenario_workdir/testfield/net.net.xml.gz --speed-factor 0.7 --min-length 2 --trips-output miv/detail.rou.xml.gz miv/detail.net.xml $TSC_HOME/scenario_workdir/testfield/iteration000/oneshot/vehroutes_oneshot_meso.rou.xml --min-air-dist 100
