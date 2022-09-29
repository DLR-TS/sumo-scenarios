#!/usr/bin/env python
import os
import sys
import subprocess
sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import sumolib

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
curdir = os.path.abspath(os.curdir) + "/"
for arg in sys.argv[1:]:
    if arg.endswith(".sumocfg"):
        dir, file = os.path.split(arg)
        os.chdir(os.path.join(root, dir))
        subprocess.call([sumolib.checkBinary("sumo"), "-c", file,
                         "--output-prefix", curdir, "--end", "1000"])
        os.chdir(curdir)
