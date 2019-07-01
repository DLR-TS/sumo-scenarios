#!/bin/bash
time /scr1/sumo/tools/route/cutRoutes.py --orig-net ../tapas/bs_miv.net.xml --speed-factor 0.7 --min-length 2 --trips-output bs_miv_cut.trips.xml bs_miv_cut.net.xml /scr2/sip-svn-trunk/projects/tapas/scenario_workdir/braunschweig_osm/iteration000/oneshot/saved_result/vehroutes_oneshot_meso.rou.xml --min-air-dist 100
 
# convert to geo-trips:
duarouter -c trips2geo.duacfg
