# Bad Hersfeld
This repository contains data for Bad Hersfeld. The initial OpenStreetMap extraction is in the osm directory.

To get the initial simulation scenario on Windows just run build.bat (or build.sh on Linux). This needs a SUMO installation with
a correct SUMO_HOME environment variable being set (the installer usually does this).

Start `sumo-gui -c osm.sumocfg` to run the scenario (on Windows double click on the sumocfg works as well).

To run the small PRT test you need to run build.sh in the prt_infra dir and then the prt_runner.py in src.
To get all in one, run `prt_runner.py joined.sumocfg`

To run the whole simulation with demand and PRT:
- Create the `joined.net.xml` using the build script in `prt/prt_infra`
- Adapt route file in `joined.sumocfg` to select demand file (default `osm_activitygen_present_with_prt.rou.xml.gz`)
- Run simulation `sumo-gui -c joined.sumocfg` (with GUI) or `sumo -c joined.sumocfg` (without GUI)

## Demand

The `demand` directory contains SUMO route / trip files for different use cases.

- `osm_activitygen_present_no_prt.rou.xml.gz`: Demand representing current situation in Bad Hersfeld (hospitals not combined)
- `osm_activitygen_present_with_prt.rou.xml.gz`: Demand representing current situation in Bad Hersfeld (hospitals not combined)
where 30% of hospital traffic uses PRT.
- `osm_activitygen_present_only_prt.rou.xml.gz`: Demand representing only the 30% of PRT hospital traffic.

- `osm_activitygen_future_no_prt.rou.xml.gz`: Demand representing future situation in Bad Hersfeld (combined hospitals)
- `osm_activitygen_future_with_prt.rou.xml.gz`: Demand representing future situation in Bad Hersfeld (combined hospitals)
where 30% of hospital traffic uses PRT.
- `osm_activitygen_future_only_prt.rou.xml.gz`: Demand representing only the 30% of PRT hospital traffic.
