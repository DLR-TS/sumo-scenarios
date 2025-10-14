# About 

Simulating traffic on all German motorways (Quick and Dirty edition)

# Inputs

https://download.geofabrik.de/europe/germany-latest.osm.pbf

# Tools

https://sumo.dlr.de/ (v1_24_0+1413  / v1_25_0)
https://wiki.openstreetmap.org/wiki/Osmconvert
https://wiki.openstreetmap.org/wiki/Osmfilter

# Preparation

## Network

osmconvert germany-latest.osm.pbf -o=germany.o5m
osmfilter germany.o5m --keep="highway=motorway =motorway_link" -o=germany-motorways.o5m
osmconvert germany-motorways.o5m -o=germany-motorways.osm.xml
netconvert --osm-files germany-motorways.osm.xml -o gmw.net.xml.gz --ramps.guess --no-internal-links --keep-edges.components 1 --no-turnarounds

## Traffic

sumo/tools/randomTrips.py -n gmw.net.xml.gz --insertion-rate 500000 --min-distance 50000 --max-distance 150000 --poisson --flows 10000 -v -r gmw.rou.xml

## Simulation

sumo gmw.net.xml.gz -r gmw.rou.xml --mesosim


