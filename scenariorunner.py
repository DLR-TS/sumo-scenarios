#!/usr/bin/env python
# this script is meant be run from a test directory

import os,subprocess,sys,shutil,types,string
from glob import glob
from optparse import OptionParser
import shutil

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
else:   
    sys.exit("please declare environment variable 'SUMO_HOME'")

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

import extractTest

if "SUMO_BINDIR" not in os.environ:
    if "SUMO_HOME" in os.environ:
        os.environ["SUMO_BINDIR"] = os.path.join(os.environ["SUMO_HOME"], "bin")
    if "SUMO" in os.environ:
        os.environ["SUMO_BINDIR"] = os.path.join(os.environ["SUMO"], "bin")

DEPLOY_SANDBOX = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'DEPLOY_SANDBOX')

def run(process, verbose):
    for step in process:
        if isinstance(step, types.FunctionType):
            step()
        else:
            if step[0]=='<':
                os.chdir(step[1:-1])
                continue
            cmd = string.Template(step).safe_substitute(os.environ)
            if verbose:
                print('calling cmd "%s" in directory "%s"' % (cmd, os.getcwd()))
            subprocess.call(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr)

def deploy(path, verbose, toRemove, toDeploy):
    try: 
        os.makedirs(path)
    except: 
        pass
    for file in toDeploy:
        if verbose:
            print("copying '%s' to '%s'" % (file, path))
        if os.path.isdir(file):
            shutil.copytree(file, os.path.join(path, os.path.basename(file)))
        else:
            shutil.copy2(file, path)
        if file in toRemove:
            if verbose:
                print("removing '%s'" % (file))
            os.remove(file)


def get_options():
    optParser = OptionParser()
    optParser.add_option("-s", "--scenario", 
            help="path of the scenario to deploy (defaults to current directory)")
    optParser.add_option("-d", "--dest", 
            help="path in which to deploy the scenario (defaults to a subdirectory in the current directory with a generated name)")
    optParser.add_option("-v", "--verbose", action="store_true",
            default=False, help="tell me what you are doing")
    optParser.add_option("-a", "--additional", 
            help="additional argument to pass to the scenario")
    (options, args) = optParser.parse_args()
    if args:
        optParser.error("no arguments allowed. Use options")
    options.deploy = options.scenario is not None or options.dest is not None
    if options.deploy:
        if options.scenario is None:
            options.scenario = os.getcwd()
        if options.dest is None:
            options.dest = extractTest.generateTargetName(THIS_DIR, options.scenario)
        else:
            options.dest = os.path.abspath(options.dest)
    return options



# there are two ways in which this can be called:
# 1) without arguments. This assumes texttest has created the appropriate sandbox
# 2) with arguments for deployment. This means we have to create the sandbox manually and maybe clean up afterwards
import stddefs
stddefs.options = get_options();
if stddefs.options.deploy:
    # create the sandbox
    if os.path.isdir(DEPLOY_SANDBOX):
        shutil.rmtree(DEPLOY_SANDBOX)
    if stddefs.options.verbose:
        print("extracting text from '%s'" % stddefs.options.scenario)
    extractTest.main(extractTest.get_options(
            ['--skip-configuration',
                "%s;%s" % (stddefs.options.scenario, DEPLOY_SANDBOX)])) 
    os.chdir(DEPLOY_SANDBOX)
    # proceed from the sandbox
    sys.path.append(DEPLOY_SANDBOX)
    import scenariodefs
    run(scenariodefs.buildProcess, stddefs.options.verbose)
    deploy(stddefs.options.dest, stddefs.options.verbose, scenariodefs.toRemove, scenariodefs.toDeploy)
else:
    sys.path.append('.')
    import scenariodefs
    run(scenariodefs.buildProcess, stddefs.options.verbose)
    run(scenariodefs.runProcess, stddefs.options.verbose)
