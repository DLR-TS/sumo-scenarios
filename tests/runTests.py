#!/usr/bin/env python
import os
import subprocess
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-s", "--suffix", default="", help="suffix to the binaries to start")
options, args = arg_parser.parse_known_args()
suffix = options.suffix if os.name == "posix" else options.suffix + ".exe"

BINARIES = ("activitygen", "emissionsDrivingCycle", "emissionsMap",
            "dfrouter", "duarouter", "jtrrouter", "marouter",
            "netconvert", "netedit", "netgenerate",
            "od2trips", "polyconvert", "sumo", "sumo-gui",
            "TraCITestClient")
if "SUMO_HOME" not in os.environ:
    os.environ["SUMO_HOME"] = os.path.join(os.environ["HOME"], "sumo")
os.environ["TEXTTEST_HOME"] = os.path.dirname(__file__)
for binary in BINARIES:
    if binary == "sumo-gui":
        os.environ["GUISIM_BINARY"] = os.path.join(os.environ["SUMO_HOME"], "bin", binary + suffix)
    else:
        os.environ[binary.upper() + "_BINARY"] = os.path.join(os.environ["SUMO_HOME"], "bin", binary + suffix)
subprocess.call(['texttest'] + args)
