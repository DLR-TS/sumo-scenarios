gunzip $SUMO_HOME/tools/contributed/saga/tests/wildau_osm.xml.gz -c > ../wildau_osm.xml
python $SUMO_HOME/tools/contributed/saga/scenarioFromOSM.py --osm ../wildau_osm.xml --out . --processes 4 --population 10000 --single-taz
