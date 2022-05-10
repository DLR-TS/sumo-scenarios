#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2012-2022 German Aerospace Center (DLR) and others.
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# https://www.eclipse.org/legal/epl-2.0/
# This Source Code may also be made available under the following Secondary
# Licenses when the conditions for such availability set forth in the Eclipse
# Public License 2.0 are satisfied: GNU General Public License, version 2
# or later which is available at
# https://www.gnu.org/licenses/old-licenses/gpl-2.0-standalone.html
# SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later

# @file    tripinfoPersons.py
# @author  Michael Behrisch
# @date    2022-03-16


from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.append(os.path.join(os.environ["SUMO_HOME"], 'tools'))
import sumolib
from sumolib.xml import parse_fast, parse_fast_structured
from sumolib.miscutils import Statistics, parseTime  # noqa


def get_options(args=None):
    argParser = sumolib.options.ArgumentParser()
    argParser.add_argument("--demand", help="the demand file(s)", default="../demand/osm_activitygen_present_no_prt.rou.xml.gz,../demand/osm_activitygen_future_no_prt.rou.xml.gz,../demand/osm_activitygen_future_with_prt.rou.xml.gz")
    argParser.add_argument("--tripinfo", help="the tripinfo file(s)", default="../osm/outputs/present_tripinfo.out.xml,../osm/outputs/future_tripinfo.out.xml,../osm/outputs/prt_tripinfo.out.xml")
    argParser.add_argument("--net", help="the net file", default="../prt_infra/joined.net.xml")
    argParser.add_argument("--roi", help="the region of interest label:lon,lat:radius", default="Klinikum:9.71452481,50.87592257:300")
    options = argParser.parse_args(args=args)
    return options


def find_roi_persons(region, demand):
    people_of_interest = set()
    vehicles_of_interest = set()
    for person in parse_fast_structured(demand, "person", ["id"], {"ride": ["lines"], "stop": ["lane"]}):
        # exclude people who walk only
        if person.ride is not None and len(person.ride) > 0:
            in_region = False
            for stop in person.stop:
                if stop.lane in region:
                    in_region = True
                    break
            if in_region:
                people_of_interest.add(person.id)
                for ride in person.ride:
                    vehicles_of_interest.add(ride.lines)
    return people_of_interest, vehicles_of_interest


def parse_persons(tripinfo, pids):
    travelSpeed = Statistics('travel speeds', histogram=True, scale=5.)
    invalid = 0
    attrs = {"ride": ["duration", "routeLength"], "walk": ["duration", "routeLength"], "stop": ["duration"]}
    for person in parse_fast_structured(tripinfo, "personinfo", ["id", "depart"], attrs):
        if pids is not None and person.id not in pids:
            continue
        length = 0
        duration = 0
        # exclude people who walk only
        usable = person.ride is not None and len(person.ride) > 0
        if usable:
            for stage in (person.ride or []) + (person.walk or []):
                if stage.duration == "-1":
                    usable = False
                    break
                length += float(stage.routeLength)
                duration += parseTime(stage.duration)
        if usable:
            travelSpeed.add(3.6 * length / duration, person.id)
        else:
            invalid += 1
    print(tripinfo, travelSpeed, invalid)
    return travelSpeed.meanAndStdDev()


def parse_vehicles(tripinfo, vids):
    travelDist = collections.defaultdict(float)
    sumCO2 = 0
    for v in parse_fast_structured(tripinfo, "tripinfo", ["id", "routeLength"], {"emissions": "CO2_abs"}):
        if vids is not None and v.id not in vids and "prt." not in v.id:
            continue
        if "prt." in v.id:
            travelDist["prt"] += float(v.routeLength) / 1000.
        elif "." in v.id:
            travelDist["bus"] += float(v.routeLength) / 1000.
        else:
            travelDist["car"] += float(v.routeLength) / 1000.
        if v.emissions:
            sumCO2 += float(v.emissions[0].CO2_abs)
    sumCO2 /= 1e6
    print(tripinfo, travelDist, sumCO2)
    return travelDist, sumCO2


if __name__ == "__main__":
    options = get_options()
    if options.roi:
        net = sumolib.net.readNet(options.net)
        regionLabel, lonLat, radius = options.roi.split(":")
        x, y = net.convertLonLat2XY(*map(float, lonLat.split(",")))
        region = set([lane.getID() for lane, dist in net.getNeighboringLanes(x, y, float(radius))])
        poi = []
        voi = []
        for demand in options.demand.split(","):
            pids, vids = find_roi_persons(region, demand)
            poi.append(pids)
            voi.append(vids)
    else:
        regionLabel = ""
        poi = voi = [None for _ in options.tripinfo.split(",")]

    labels = []
    speedMean = []
    speedDev = []
    vData = collections.defaultdict(list)
    eData = []
    for trips, pids, vids in zip(options.tripinfo.split(","), poi, voi):
        labels.append(os.path.basename(trips)[:3])
        mean, dev = parse_persons(trips, pids)
        speedMean.append(mean)
        speedDev.append(dev)
        travelDist, sumCO2 = parse_vehicles(trips, vids)
        for k, v in travelDist.items():
            vData[k].append(v)
        eData.append(sumCO2)

    fig, ax = plt.subplots()
    ax.bar(labels, speedMean, yerr=speedDev)
    ax.set_ylabel('km/h')
    ax.set_title('Reisegeschwindigkeit ' + regionLabel)
    plt.savefig(regionLabel + 'speed.png')
    plt.clf()

    fig, ax = plt.subplots()
    bottom = None
    for k, v in vData.items():
        if bottom is None:
            ax.bar(labels, v, label=k)
            bottom = v
        else:
            ax.bar(labels, v, bottom=bottom, label=k)
            bottom = [b + x for b, x in zip(bottom, v)]
    ax.set_ylabel('km')
    ax.set_title('Fahrleistung ' + regionLabel)
    ax.legend()
    plt.savefig(regionLabel + 'dist.png')
    plt.clf()

    fig, ax = plt.subplots()
    ax.bar(labels, eData)
    ax.set_ylabel('kg')
    ax.set_title('$CO_2$-Emissionen ' + regionLabel)
    plt.savefig(regionLabel + 'CO2.png')
    plt.clf()
