"""
@file    __init__.py
@author  Michael.Behrisch@dlr.de
@date    2015-06-10
@version $Id: analysis.py 2493 2013-04-02 10:32:37Z behr_mi $

custom script collection for KoFIF

Copyright (C) 2015-2017 DLR/TS, Germany
All rights reserved
"""
import math

import assign
from constants import TH


def trip_filter(options, row, source, dest):
    dist = math.hypot(source[0] - dest[0], source[1] - dest[1])
    return dist >= 30000 or int(row[TH.taz_id_start]) <= 289 or int(row[TH.taz_id_end]) <= 289

assign_trips = assign.run_default
