#!/bin/sh
python vdv_importer.py 20190206_vdv -n ../detail/bs_miv_detail.net.xml -T 1 --departure-offset 86400 --generate-umlauf --stop-patch-file patch.stop.txt
#sumo -c debug_vdv.sumocfg
