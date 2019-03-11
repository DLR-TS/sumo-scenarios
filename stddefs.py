from __future__ import print_function
import sys
import os, glob, zipfile, subprocess
import re
from datetime import datetime
sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), 'tools'))
from sumolib.miscutils import Statistics
from sumolib.output import parse_fast

def getDefaults(netfile, tlsfile):
    if tlsfile!="":
        build = buildProcess + [get_python_tool("tls/tls_csv2SUMO.py") + ' %s %s > %s' % (",".join(sorted(glob.glob("data/*.csv"))), netfile, tlsfile)]
        toRemove = [netfile, tlsfile]
    else:
        build = buildProcess
        toRemove = [netfile]
    return build, runProcess, toRemove

def unzip(fname):
    zip = zipfile.ZipFile(fname)
    for each in zip.namelist():
        if not each.endswith('/'):
            dest = os.path.basename(each)
            file(dest, 'wb').write(zip.read(each))
    filelist = zip.namelist()
    zip.close()

def get_python_tool(rel_path):
    return '"' + os.environ.get("PYTHON", "python") + '" "' + os.path.join(os.environ["SUMO_HOME"], "tools", rel_path) + '"'

def get_app(name, name_variable):
    direct = os.environ.get(name_variable)
    homedir = os.environ.get("SUMO_HOME")
    if direct:
        return '"%s"' % direct
    if homedir:
        return '"%s"' % os.path.join(homedir, 'bin', name)
    return name


def filterLog(log="data/sumo_log.txt", statsOut="data/stats.txt", statsIn="stats.scenario", tripinfos="data/tripinfos.xml"):
    collisions = 0
    timeout = 0
    simEnd = -1
    for line in open(log):
        if "collision" in line:
            collisions += 1
        if "waited too long" in line:
            timeout += 1
        if line.startswith("Simulation ended at time: "):
            simEnd = line.split()[-1]
    if os.path.exists(tripinfos):
        durationStats = Statistics(' Traveltimes')
        for trip in parse_fast(tripinfos, 'tripinfo', ['id', 'duration']):
            durationStats.add(float(trip.duration), trip.id)
        durationStats = str(durationStats).replace('"','')
    else:
        durationStats = ''
    statLine = "Collisions: %s Timeouts: %s End: %s%s" % (collisions, timeout, simEnd, durationStats)
    with open(statsOut, 'w') as o:
        rootLength = len(os.environ["TEXTTEST_SANDBOX_ROOT"]) + 1
        testNameStart = os.environ["TEXTTEST_SANDBOX"].find("/", rootLength) + 1
        oldStats = os.path.join(os.environ["TEXTTEST_ROOT"], os.environ["TEXTTEST_SANDBOX"][testNameStart:], statsIn)
        if os.path.exists(oldStats):
            for line in open(oldStats):
                o.write(line)
            if line.strip() == statLine.strip():
                o.close()
                return
        sumoVersion = subprocess.check_output(get_app('sumo', 'SUMO_BINARY') + " -V", shell=True).splitlines()[0]
        print("%s %s\n%s" % (datetime.now(), sumoVersion, statLine), file=o)


buildProcess = ["%s -c data/build.netc.cfg" % get_app('netconvert', 'NETCONVERT_BINARY')]
runProcess = ["%s -c data/run.sumo.cfg --no-step-log --no-duration-log" % get_app('sumo', 'SUMO_BINARY'), filterLog]
