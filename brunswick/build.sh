# Step 0: installing tools
#wget -O - http://m.m.i24.cc/osmfilter.c |cc -x c - -O3 -o osmfilter
#wget -O - http://m.m.i24.cc/osmconvert.c | cc -x c - -lz -O3 -o osmconvert

# Step 1: preparing OSM
$SUMO_HOME/tools/osmGet.py -b 9.60,51.69,11.07,52.77 -p TF_NDS
osmconvert TF_NDS_bbox.osm.xml -o=TF_NDS.o5m
osmfilter --verbose TF_NDS.o5m --keep-ways="highway=primary =primary_link =secondary =secondary_link =trunk =trunk_link =motorway =motorway_link" --keep-nodes= --keep-relations= --out-o5m > TF_NDS_main_roads.o5m
osmconvert TF_NDS_main_roads.o5m -o=TF_NDS_main_roads.osm.xml
rm TF_NDS_bbox.osm.xml TF_NDS_main_roads.o5m
gzip TF_NDS_main_roads.osm.xml

# Step 2: network preparation
$SUMO_HOME/tools/osmBuild.py -f TF_NDS_main_roads.osm.xml.gz

# Step 3: TAPAS
#tapas/bs_miv.netccfg 
#./t2s.py --tapas-trips tapas-trips-in/braunschweig_trips_2015y_10m_29d_11h_47m_07s_427ms.csv --net-file scenario_workdir/braunschweig_osm/net.net.xml --iteration-dir scenario_workdir/braunschweig_osm/iteration000/ --bidi-taz-file scenario_workdir/braunschweig_osm/bidi.taz.xml
#time ./t2s.py --tapas-trips tapas-trips-in/braunschweig_trips_2015y_10m_29d_11h_47m_07s_427ms.csv --net-file scenario_workdir/braunschweig_osm/net.net.xml --iteration-dir scenario_workdir/braunschweig_osm/iteration000/ --bidi-taz-file scenario_workdir/braunschweig_osm/bidi.taz.xml --no-rectify --default-vtype car --max-radius 5000

# Step 4: cutRoutes
#$SUMO_HOME/tools/route/cutRoutes.py --orig-net ../bs_miv.net.xml --speed-factor 0.7 --min-length 2 --trips-output bs_miv_detail3.trips.xml ../bs_miv_detail3.net.xml
#/scr2/sip-svn-trunk/projects/tapas/scenario_workdir/braunschweig_osm/iteration000/oneshot/saved_result/vehroutes_oneshot_meso.rou.xml

# Step 2a: convert to geo-trips:
#duarouter -c trips2geo.duacfg

# Step 3: prepare detail simulation
#netconvert -c bs_miv_detail.netccfg
#duarouter -c fromgeo.duacfg

# Step 4: run detail simulation

#sumo -c oneshot.sumocfg
