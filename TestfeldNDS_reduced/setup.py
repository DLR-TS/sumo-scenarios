#!/usr/bin/env python
from __future__ import print_function
import os, sys, shutil, subprocess, glob
sys.path += [os.path.join(os.environ["SUMO_HOME"], 'tools')]
import sumolib

here = sys.argv[2]
orig = os.path.join(os.path.dirname(here), "TestfeldNDS")
for f in ("__init__.py", "vtypes.xml"):
    shutil.copyfile(os.path.join(orig, f), os.path.join(here, f))
# generate the new net based on the boundaries
subprocess.check_call([sumolib.checkBinary("netconvert"), "-s", os.path.join(orig, "net.net.xml.gz"),
                       "-e", os.path.join(sys.argv[1], "reduced.edg.xml.gz"),
                       "-o", os.path.join(here, "net.net.xml.gz")])
