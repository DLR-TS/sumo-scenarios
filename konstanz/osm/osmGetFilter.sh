#!/bin/bash
# Download from OpenStreetMap
$SUMO_HOME/tools/osmGet.py -b 8.5504,47.1291,9.8724,48.1113
# Filter main roads for the whole network
osmfilter osm_bbox.osm.xml --keep-ways="highway=primary =primary_link =secondary =secondary_link =trunk =trunk_link =motorway =motorway_link" --keep-nodes= --keep-relations= | gzip > main_roads.osm.xml.gz
# Reduce to Konstanz "City"
osmconvert -b=9.104,47.629,9.216,47.701 osm_bbox.osm.xml | gzip > detail.osm.xml.gz
