#!/usr/bin/env python
from __future__ import print_function
import os, sys, shutil, subprocess, glob
TOOLS = os.path.join(os.environ["SUMO_HOME"], 'tools')
sys.path += [TOOLS]
import sumolib

bs = os.path.join(os.path.dirname(sys.argv[1]), "brunswick", "miv")
orig = sys.argv[2]
reduced = orig + "_reduced"
os.makedirs(reduced, exist_ok=True)
for f in ("__init__.py", "vtypes.xml"):
    shutil.copyfile(os.path.join(orig, f), os.path.join(reduced, f))
# generate the new net based on the reduced edge list
subprocess.check_call([sumolib.checkBinary("netconvert"), "-c", os.path.join(bs, "miv.netccfg")])
subprocess.check_call([sys.executable, os.path.join(TOOLS, "net", "reduceLanes.py"),
                       "-n", os.path.join(bs, "netpatch", "miv.net.xml"),
                       "-o", os.path.join(reduced, "reduced.edg.xml")])
net = sumolib.net.readNet(os.path.join(orig, "net.net.xml.gz"))
edge_lengths = dict([(e.getID(), float(e.getLength())) for e in net.getEdges()])
with open(os.path.join(reduced, "reduce_fixed.edg.xml"), "w") as fixed:
    fixed.write("<edges>\n")
    for edge in sumolib.xml.parse(os.path.join(reduced, "reduced.edg.xml"), "edge"):
       if edge_lengths.get(edge.id, 0.) > 20.:
           print(edge.toXML("    "), file=fixed)
    fixed.write("</edges>\n")

subprocess.check_call([sumolib.checkBinary("netconvert"), "-s", os.path.join(orig, "net.net.xml.gz"),
                       "-e", os.path.join(reduced, "reduce_fixed.edg.xml"),
                       "-o", os.path.join(reduced, "net.net.xml.gz")])

with open(os.path.join(orig, "generated_nets.txt"), "w") as generated:
    print(os.path.abspath(os.path.join(orig, "net.net.xml.gz")), file=generated)
    print(os.path.abspath(os.path.join(reduced, "net.net.xml.gz")), file=generated)
