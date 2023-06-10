python "%SUMO_HOME%\tools\randomTrips.py"  -n net.net.xml.gz --seed 42 --fringe-factor 10 -p 6  -r osm.passenger.rou.xml -b 50400 -e 54000 --vehicle-class passenger --vclass passenger --prefix veh --min-distance 300 --trip-attributes "departLane=\"best\"" --fringe-start-attributes "departSpeed=\"max\"" --allow-fringe.min-length 1000 --lanes  -L -l --validate
python "%SUMO_HOME%\tools\routeSampler.py" -r osm.passenger.rou.xml --edgedata-files edge_data_cars.xml -o samplertrips.rou.xml --optimize full