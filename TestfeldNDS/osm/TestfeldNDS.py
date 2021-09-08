#!/usr/bin/env python
import json
import subprocess

umap = json.load(open("TestfeldNDS.umap"))
coords = umap["layers"][0]["features"][0]["geometry"]["coordinates"]
with open("TestfeldNDS.poly", "w") as poly:
    print("polygon\n1", file=poly)
    for lon, lat in coords:
        print("\t%s\t%s" % (lon, lat), file=poly)
    print("END\nEND", file=poly)
subprocess.call("osmconvert nds.o5m -o=TestfeldNDS.o5m -B=TestfeldNDS.poly".split())
subprocess.call('osmfilter TestfeldNDS.o5m --keep-ways="highway=primary =primary_link =secondary =secondary_link =trunk =trunk_link =motorway =motorway_link" --keep-nodes= --keep-relations= --out-o5m | osmconvert - | gzip > TestfeldNDS_main_roads.osm.xml.gz', shell=True)
