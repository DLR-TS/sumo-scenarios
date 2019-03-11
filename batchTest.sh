#!/bin/bash
cd `dirname $0`
export FILEPREFIX=$1
export SMTP_SERVER=localhost
STATUSLOG=${FILEPREFIX}status.log
TESTLOG=${FILEPREFIX}test.log
export SCENARIO_BATCH_RESULT=${FILEPREFIX}batch_result
export SCENARIO_REPORT=${FILEPREFIX}report
export TEXTTEST_TMP=$PWD/texttesttmp

export ACTIVITYGEN_BINARY="$SUMO_HOME/bin/activitygen"
export DFROUTER_BINARY="$SUMO_HOME/bin/dfrouter"
export DUAROUTER_BINARY="$SUMO_HOME/bin/duarouter"
export JTRROUTER_BINARY="$SUMO_HOME/bin/jtrrouter"
export MAROUTER_BINARY="$SUMO_HOME/bin/marouter"
export NETCONVERT_BINARY="$SUMO_HOME/bin/netconvert"
export NETEDIT_BINARY="$SUMO_HOME/bin/netedit"
export NETGENERATE_BINARY="$SUMO_HOME/bin/netgenerate"
export OD2TRIPS_BINARY="$SUMO_HOME/bin/od2trips"
export POLYCONVERT_BINARY="$SUMO_HOME/bin/polyconvert"
export SUMO_BINARY="$SUMO_HOME/bin/sumo"
export GUISIM_BINARY="$SUMO_HOME/bin/sumo-gui"
export PYTHON="python"

if test -e $SUMO_HOME/bin/sumo; then
    git pull > $TESTLOG
    REVISION=`git describe --always`
    SUMOVER=`$SUMO_BINARY -V 2>/dev/null | grep Version | head -1 | cut -d " " -f 3`
    TESTOPTS="-b ${FILEPREFIX} -name `LANG=C date +%d%b%y`r$REVISION$SUMOVER"
    texttest -a scenario,scenario.daily $TESTOPTS >> $TESTLOG
    if test `date +'%w'` == '6'; then
        texttest -a scenario.weekly $TESTOPTS >> $TESTLOG
    fi
    texttest -coll $TESTOPTS >> $TESTLOG
    $SUMO_HOME/tools/build/status.py $TESTLOG $TESTLOG $TEXTTEST_TMP $SMTP_SERVER > $STATUSLOG
fi
