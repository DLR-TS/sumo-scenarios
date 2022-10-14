#!/usr/bin/env python
import os
import sys
import subprocess
sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import sumolib

arg_parser = sumolib.options.ArgumentParser()
arg_parser.add_argument("sumocfg")
arg_parser.add_argument("-e", "--end", default="1000")
options = arg_parser.parse_args()

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
curdir = os.path.abspath(os.curdir) + "/"
dir, file = os.path.split(options.sumocfg)
os.chdir(os.path.join(root, dir))
subprocess.call([sumolib.checkBinary("sumo"), "-c", file, "--no-step-log",
                 "--output-prefix", curdir, "--end", options.end, "--aggregate-warnings", "0"])
os.chdir(curdir)
