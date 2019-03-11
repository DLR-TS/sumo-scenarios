#!/bin/bash

export TEXTTEST_HOME="`dirname $0`"
if test x"$SUMO_HOME" = x; then
  export SUMO_HOME="$HOME/sumo"
fi
export ACTIVITYGEN_BINARY="$SUMO_HOME/bin/activitygen$SUFFIX"
export DFROUTER_BINARY="$SUMO_HOME/bin/dfrouter$SUFFIX"
export DUAROUTER_BINARY="$SUMO_HOME/bin/duarouter$SUFFIX"
export JTRROUTER_BINARY="$SUMO_HOME/bin/jtrrouter$SUFFIX"
export MAROUTER_BINARY="$SUMO_HOME/bin/marouter$SUFFIX"
export NETCONVERT_BINARY="$SUMO_HOME/bin/netconvert$SUFFIX"
export NETEDIT_BINARY="$SUMO_HOME/bin/netedit$SUFFIX"
export NETGENERATE_BINARY="$SUMO_HOME/bin/netgenerate$SUFFIX"
export OD2TRIPS_BINARY="$SUMO_HOME/bin/od2trips$SUFFIX"
export POLYCONVERT_BINARY="$SUMO_HOME/bin/polyconvert$SUFFIX"
export SUMO_BINARY="$SUMO_HOME/bin/sumo$SUFFIX"
export GUISIM_BINARY="$SUMO_HOME/bin/sumo-gui$SUFFIX"
export PYTHON="python"

if which texttest &> /dev/null; then
  texttest "$@"
else
  texttest.py "$@"
fi
