# Sumo Scenarios
This repository contains publicly available traffic networks and corresponding demands for usage with [Eclipse SUMO](https://sumo.dlr.de).

Every directory corresponds to a region and might contain subdirectories with different scenarios. Some of them are also included as submodules.
Since the scenarios and their changesets are quite big it is recommended to do a shallow clone:
```
git clone --recursive --depth 1 https://github.com/DLR-TS/sumo-scenarios
```

Some of the scenarios are also (or only) usable with the [TAPAS-SUMO-Coupling](https://github.com/DLR-TS/tsc).
Currently this is the case for
- TestfeldNDS
- TestfeldNDS_reduced
