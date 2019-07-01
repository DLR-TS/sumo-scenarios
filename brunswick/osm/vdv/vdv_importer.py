#!/usr/bin/python

"""
@author  Daniel Wesemeyer
@date    2018-11-05
@version $Id: vdv_importer.py

Copyright (C) 2018 DLR/TS, Germany
All rights reserved
"""

import os, sys
import optparse

sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

from sumolib.net import Net, readNet
import subprocess
import operator
from collections import defaultdict
import math
from sets import Set

#if "SUMO_HOME" in os.environ:
#    sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools", "xml"))
#    sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools", "assign"))
#else:
#    exit("Please declare environment variable 'SUMO_HOME'")
#from dijkstra import priorityDictionary


BASE_DIR = ''
DELIMITER = ';'
OFFSET = 0

# functional place types
FILE_ONR_TYPE = 'menge_onr_typ.x10'
FILE_PLACES = 'rec_ort.x10'
FILE_STOPS = 'rec_hp.x10'
FILE_SECTIONS = 'rec_sel.x10'
FILE_VEHICLE_TYPES = 'menge_fzg_typ.x10'
FILE_VEHICLES = 'fahrzeug.x10'
FILE_ROUTES = 'lid_verlauf.x10'
FILE_DOMAINS = 'menge_bereich.x10'
FILE_UMLAUF = 'rec_umlauf.x10'
FILE_TRIPS = 'rec_frt.x10'
FILE_FGR = 'ort_hztf.x10'


DEFAULT_STOP_TIME = 10
STOP_LENGTH = 30.0


# mapping of possible VDV vehicle types to SUMO vClass / GUI shapes / emission class
VEHICLE_TYPES = {
        'Niederflur-Glz'                          : ('bus', 'bus/flexible', 'Bus'),
        'Niederflur-Solo - kein Ersatz durch Glz' : ('bus', 'bus', 'Bus'),
        'Solaris Urbino Glz Elektro'              : ('bus', 'bus', 'zero'),
        '81er Zug'                                : ('tram', 'rail/railcar', 'zero'),
        'GT6-NF'                                  : ('tram', 'rail/railcar', 'zero'),
        'NGT8D'                                   : ('tram', 'rail/railcar', 'zero'),
        'Tramino S110b'                           : ('tram', 'rail/railcar', 'zero'),
        'GT6-NF-Erweiterung'                      : ('tram', 'rail/railcar', 'zero'),
        'NGT8D Zug'                               : ('tram', 'rail/railcar', 'zero'),
        'Niederflur-Solo'                         : ('bus', 'bus', 'Bus'),
        'DLR-Testbus'                             : ('bus', 'bus', 'Bus'),
        'Kleinbus'                                : ('bus', 'bus', 'Bus')
        }

DOMAINS = {
        'Bus'  : 'bus',
        'Tram' : 'tram'
        }


def get_options(args = None):
    optParser = optparse.OptionParser()

    optParser.add_option('--netfile', '-n', default=None, 
            help='The underlying SUMO network for the public transport system. If no network is given, the importer creates a simplified network with stop-to-stop connections (not implemented yet).')
    optParser.add_option('--daytypes', '-T', default=1, type=int, help='The type of day you want to extract schedule info for.')
    optParser.add_option('--use-lines', dest='uselines', default='all', help='Apply a filter on which lines to convert from the VDV data (comma separated). Default is "all".')
    optParser.add_option('--ignore-lines', dest='ignorelines', default='', help='Apply a filter on which lines not to convert from the VDV data (comma separated). Default is "".')
    optParser.add_option('--departure-offset', dest='departureOffset', default=0, type=int, help='An offset (in seconds) to the departures read from the VDV data')
    optParser.add_option('--generate-umlauf', dest='generateUmlauf', action="store_true", help='If "true", no single vehicle trip for each VDV trip is generated, but a complete umlauf (succession of trips) over the whole day.')
    optParser.add_option('--stop-patch-file', dest='stopPatchFile', help='A file that contains patches for localization of stops on specific lanes.')

    (options, args) = optParser.parse_args(args = args)

    return options


"""
Parses an .x10 text file and returns the actual data (records).
Columns containing the row type and the version of the data are omitted.
"""
def get_content(filename):
    with open(BASE_DIR + '/' + filename) as f:
        content = f.readlines()
    # omit first two records because they only consist of the type (record) and the version nr
    return [c.split(DELIMITER)[2:] for c in content if c.split(DELIMITER)[0] == 'rec']


"""
Parses a dms (degree, minute, second) string and returns a decimal degree number.
The dms strings in VDV 4.5.2 are defined to be in the range of +/- 1800000000, so we have three digits for the degree, two for the minute, two for the seconds and three for decimal places.
"""
def dms2dd(string):
    degrees = ''
    minutes = ''
    seconds = ''
    if len(string) == 10:
        degrees = string[0:3]
        minutes = string[3:5]
        seconds = string[5:7] + '.' + string[7:]
    else:
        degrees = string[0:2]
        minutes = string[2:4]
        seconds = string[4:6] + '.' + string[6:]
#    print degrees,minutes,seconds
    result = float(degrees)
    if len(minutes) > 0:
        result += float(minutes)/60.
    if len(seconds) > 1:
        result += float(seconds)/3600.
    return result


"""
Reads the functional types of places in the public transport network.
Functional types can be stops, depots, way points, traffic lights or charging stations.
"""
def read_functional_place_types():
    content = get_content(FILE_ONR_TYPE)
    result = dict([(c[1], c[2]) for c in content])
    print(' INFO: Read %s functional place types from %s' % (len(result), FILE_ONR_TYPE))
    return result


"""
Reads the actual places existing in the public transport network.
Consists of all possible functional types.
"""
def read_places():
    content = get_content(FILE_PLACES)
    # id -> (type, name, lat, lon)
    places = {}
    for c in content:
        onr_typ_nr          = c[0].strip()
        ort_nr              = c[1].strip()
        ort_name            = c[2].strip().decode('latin1').encode('ascii', 'replace')
        ort_ref_ort         = c[3].strip()
        ort_ref_ort_typ     = c[4].strip()
        ort_ref_ort_langnr  = c[5].strip()
        ort_ref_ort_kuerzel = c[6].strip()
        ort_ref_ort_name    = c[7].strip().decode('latin1').encode('ascii', 'replace')
        zone_wabe_nr        = c[8].strip()
        ort_pos_laenge      = dms2dd(c[9].strip())
        ort_pos_breite      = dms2dd(c[10].strip())
        ort_pos_hoehe       = int(c[11].strip())
        code                = c[12].strip()
        #ladest_typ_nr       = c[12].strip()
        #netzanschl_nr       = c[13].strip()
        #max_leistung        = int(c[14].strip())
        if ort_pos_laenge > 0 and ort_pos_breite > 0:
            places[(ort_nr, onr_typ_nr)] = (ort_name, ort_pos_laenge, ort_pos_breite)
    print(' INFO: Read %s places from %s' % (len(places), FILE_PLACES))
    return places


def read_sections(places):
    content = get_content(FILE_SECTIONS)
    # (fromId, toId) -> length
    sections = {}
    for c in content:
        fromId = c[2].strip()
        toId = c[3].strip()
        length = int(c[5].strip())
        if fromId in [k[0] for k in places.keys()] and toId in [k[0] for k in places.keys()]:
            sections[(fromId, toId)] = length
    return sections


"""
Reads the existing public transport domains (e.g. bus, tram, light rail).
"""
def read_domains():
    content = get_content(FILE_DOMAINS)
    domains = {}
    # domain_id -> transport_mode
    for c in content:
        domain = c[0]
        mode = c[1]
        domains[domain] = mode
    return domains


"""
Reads the vehicle types existing in the public transport system.
"""
def read_vehicle_types():
    content = get_content(FILE_VEHICLE_TYPES)
    # type_id -> (sumo_class, length, width, capacity, guiShape)
    vTypes = {}
    for t in content:
        veh_type_nr = t[0].strip()
        vdv_type = t[4].strip().replace('"', '')
        vClass = VEHICLE_TYPES[vdv_type][0]
        length = t[1]
        width = float(t[10])/1000
        capacity = int(t[2]) + int(t[3])
        guiShape = VEHICLE_TYPES[vdv_type][1]
        vTypes[veh_type_nr] = (vClass, length, width, capacity, guiShape)
    print(' INFO: Read %s vehicle types from %s' % (len(vTypes), FILE_VEHICLE_TYPES))
    return vTypes


"""
Reads the vehicles existing in the public transport system.
"""
def read_vehicles():
    content = get_content(FILE_VEHICLES)
    vehicles = {}
    for v in content:
        veh_nr = int(v[0].strip())
        veh_type_nr = int(v[1].strip())
        vehicles[veh_nr] = (veh_type_nr)
    print(' INFO: Read %s vehicles from %s' % (len(vehicles), FILE_VEHICLES))
    return vehicles


"""
Reads all routes (lines) of the public transport system.
Using the filters 'use_lines' or 'ignore'lines', you can define which lines you want to have converted.
"""
def read_routes(use_lines, ignore_lines):
    content = get_content(FILE_ROUTES)
    # (line_id, line_var_id) -> [stop1, stop2, ...]
    routes = {}
    # stop_id -> [line_1, line_2, ...]
    stops2lines = {}
    for c in content:
        line_nr = c[1].strip()
        if (use_lines == 'all' or line_nr in use_lines.split(',')) and not line_nr in ignore_lines.split(','):
            line_var = c[2].strip().replace('"', '')
            stop = c[4].strip()
            if not (line_nr, line_var) in routes.keys():
                routes[(line_nr, line_var)] = []
            if not stop in stops2lines.keys():
                stops2lines[stop] = []
            stops2lines[stop].append(stop)
            routes[(line_nr, line_var)].append(stop)
    return routes, stops2lines


"""
Reads all trips of public transport vehicles.
"""
def read_trips(vtypes, daytype, use_lines, ignore_lines):
    content = get_content(FILE_TRIPS)
    trips = {}
#0        1          2      3            4         5            6       7           8       9              10             11
#FRT_FID; FRT_START; LI_NR; TAGESART_NR; LI_KU_NR; FAHRTART_NR; FGR_NR; STR_LI_VAR; UM_UID; MAX_VER_FRUEH; MAX_VER_SPAET; FZG_TYP_GRUPPE_NR
    # id -> (departure, line_id, line_var_id, veh_type)
    for c in content:
        if int(c[3]) == daytype:
            trip_id = c[0].strip()
            depart = int(c[1].strip())
            line_id = c[2].strip()
            if (use_lines == 'all' or line_id in use_lines.split(',')) and not line_id in ignore_lines.split(','):
                line_var_id = c[7].strip().replace('"', '')
                #veh_type = c[11].strip() if c[11].strip() in vtypes else '1'
                fgr_nr = c[6]
                mode = 'tram' if int(c[11]) == 4 else 'bus'
                umlauf_id = c[8]
                trips[trip_id] = (depart, line_id, line_var_id, fgr_nr, mode, umlauf_id)
    print(' INFO: Read %s trips from %s' % (len(trips), FILE_TRIPS))
    return trips


"""
Read the stop times for specific stops.
The stop times depend on the time of the day (i.e. HVZ, NVZ, ...) and overwrite the default of 20 seconds.
"""
def read_stop_times():
    content = get_content(FILE_FGR)
    stop_times = defaultdict(lambda : defaultdict(lambda : 20))
    for c in content:
        fgr_nr = c[0].strip()
        place_nr = c[2].strip()
        stop_time = int(c[3].strip())
        stop_times[(place_nr, fgr_nr)] = stop_time
    print(' INFO: Read %s stop times from %s' % (len(stop_times), FILE_FGR))
    return stop_times


def read_umlaeufe(daytype):
    content = get_content(FILE_UMLAUF)
    umlaeufe = {}
    uniqueIDs = Set()
    for c in content:
        if int(c[0]) == daytype:
#        0            1       2        3            4        5            6
#        TAGESART_NR; UM_UID; ANF_ORT; ANF_ONR_TYP; END_ORT; END_ONR_TYP; FZG_TYP_NR
            uid = c[1]
            veh_type = int(c[6])
            umlaeufe[uid] = veh_type
            uniqueIDs.add(uid)
    print(' INFO: Read %s umlaeufe from %s (%s unique items)' % (len(umlaeufe), FILE_UMLAUF, len(uniqueIDs)))
    return umlaeufe


def create_trips(routes, trips, umlaeufe, net, generateUmlauf):
    warnCounter = 0
    # trip_id -> (vehType, departure, [edge1, edge2, ...], [stop1, stop2, ...])
    veh_trips = {}
    stop2Modes = {}
    edges = []
    for trip_id, (depart, line_id, line_var_id, fgr_nr, mode, umlauf_id) in trips.items():
        identifier = line_id + '_' + line_var_id + '_' + trip_id
        # only consider stops that are placed on any lane and are actual stops (no way points, traffic lights etc.)
        stops = []
        for stop_id in routes[(line_id, line_var_id)]:
            #if stop_id in stop2lane and int(stop2lane[stop_id][1]) < 3:
            stops.append(stop_id)
            if not stop_id in stop2Modes:
                stop2Modes[stop_id] = []
            if not mode in stop2Modes[stop_id]:
                stop2Modes[stop_id].append(mode)
        #stops = [stop_id for stop_id in routes[(line_id, line_var_id)] if stop_id in stop2lane and int(stop2lane[stop_id][1]) < 3]
        #for i, edge in enumerate(stop2lane.values()[1:]):
        #    edges.append(net.getShortestPath(stop2lane[stop2lane.keys()[i]], edge))
        if len(stops) < 2:
            warnCounter += 1
            if warnCounter < 10:
                print("Too few stops for trip %s on line %s. Ignoring." % (trip_id, line_id))
            continue
        #edges = [stop2lane[stops[0]][2].getID(), stop2lane[stops[len(stops)-1]][2].getID()]
        veh_type = umlaeufe[umlauf_id]
        if generateUmlauf:
            if not umlauf_id in veh_trips:
                veh_trips[umlauf_id] = []
            veh_trips[umlauf_id].append((depart, veh_type, edges, routes[(line_id, line_var_id)], fgr_nr))
        else:
            veh_trips[identifier] = (depart, veh_type, edges, routes[(line_id, line_var_id)], fgr_nr)
    return veh_trips, stop2Modes


"""
Writes the route file for all transit vehicles' trips..
"""
def write_route_file(vTypes, vehicles, routes, trips, stop_times, stop2edge, generateUmlauf):
    with open('transitVTypes.add.xml', 'w') as f:
        f.write('<routes>\n')
        # vehicle types
        for vType, (vClass, l, w, cap, guiShape) in vTypes.items():
            veh_type_nr = 'id="%s" ' % vType
            vClass = 'vClass="%s" ' % vClass
            length = 'length="%s" ' % float(l) if float(l) > 0 else ''
            width = 'width="%s" ' % float(w) if w > 0 else ''
            capacity = 'personCapacity="%s" ' % cap
            guiShape = 'guiShape="%s" ' % guiShape
            color = 'color="204,255,204" ' if vType == '8' else 'color="255,204,153" '
            if vType == '8':
                f.write('    <vType %s%s%s%s%s%s%s>\n' % (veh_type_nr, vClass, length, width, capacity, guiShape, color))
                f.write('        <param key="maximumBatteryCapacity" value="2000"/>\n')
                f.write('        <param key="maximumPower" value="1000"/>\n')
                f.write('    </vType>\n')
            else:
                f.write('    <vType %s%s%s%s%s%s%s/>\n' % (veh_type_nr, vClass, length, width, capacity, guiShape, color))
        f.write('\n</routes>')

    with open('transit.rou.xml', 'w') as f:
        f.write('<routes>\n')
        # vehicles (actually create one vehicle per scheduled trip)
        if generateUmlauf:
            generateAndWriteUmlaeufe(f, vehicles, routes, trips, stop_times, stop2edge)
        else:
            sorted_trips = sorted(trips.items(), key=operator.itemgetter(1))
            for trip_id, (depart, veh_type, edges, stops, fgr_nr) in sorted_trips:
                stops = [stop_id for stop_id in stops if stop_id in stop2edge]
                if len(stops) < 2:
                    continue
                fromEdge = stop2edge[stops[0]][2].getID().split('_')[0]
                toEdge = stop2edge[stops[len(stops)-1]][2].getID().split('_')[0]
                f.write('    <trip id="%s" type="%s" depart="%s" from="%s" to="%s" >\n' % (trip_id, veh_type, depart + OFFSET, fromEdge, toEdge))
                for stop in stops:
                    stop_time = stop_times.get((stop,fgr_nr.strip()), DEFAULT_STOP_TIME)
                    f.write('        <stop busStop="%s" duration="%s" />\n' % (stop, stop_time))
                f.write('    </trip>\n')

        f.write('</routes>')


def generateAndWriteUmlaeufe(outf, vehicles, routes, trips, stop_times, stop2edge):
    umlauf2vehicle = {}
    virtualVehicleCounter = 0
    for umlauf_id in trips:
        umlauf = trips.get(umlauf_id)
        veh_type = umlauf[0][1]
        vehicle = None
        for vehicle_id, vType in vehicles.items():
            if vType == veh_type:
                vehicle = vehicle_id
                break
        if vehicle is not None:
            del vehicles[vehicle]
        else:
            # should actually not happen...
            # XXX the correct way to handle this: create a timeline of vehicle availabilities and assign an available vehicle to the umlauf
            # currently, a vehicle is unavailable as soon as it has one umlauf per day
            print(' Warning: Could not find a vehicle for umlauf %s (needed type: %s)! Creating virtual vehicle.') % (umlauf_id, veh_type)
            vehicle = 'virtual_' + str(virtualVehicleCounter)
            virtualVehicleCounter += 1
        umlauf2vehicle[umlauf_id] = vehicle
    umlaeufe = {}
    for umlauf_id, umlaufList in trips.items():
        vehicle = umlauf2vehicle.get(umlauf_id)
        #print umlaufList
        tripStart = False
        firstDep = 0
        for depart, veh_type, edges, stops, fgr_nr in sorted(umlaufList, key=operator.itemgetter(0)):
            stops = [stop_id for stop_id in stops if stop_id in stop2edge]
            if len(stops) < 2:
                continue
            fromEdge = stop2edge[stops[0]][2].getID().split('_')[0]
            toEdge = stop2edge[stops[len(stops)-1]][2].getID().split('_')[0]
            #umlaeufe[(depart, vehicle)] += '    <trip id="%s" type="%s" depart="%s" from="%s" to="%s">\n' % (vehicle, veh_type, depart + OFFSET, fromEdge, toEdge)
            if not tripStart:
                tripStart = True
                firstDep = depart
                umlaeufe[(firstDep,vehicle)] = ''
                umlaeufe[(firstDep,vehicle)] += '    <trip id="%s" type="%s" depart="%s">\n' % (vehicle, veh_type, depart + OFFSET)
            else:
                umlaeufe[(firstDep,vehicle)] += '        <stop lane="%s" endPos="0.2" until="%s" parking="true" />\n' % (fromEdge+'_0', depart + OFFSET)
            for i, stop in enumerate(stops):
                stop_time = stop_times.get((stop,fgr_nr.strip()), DEFAULT_STOP_TIME)
                umlaeufe[(firstDep,vehicle)] += '        <stop busStop="%s" duration="%s" />\n' % (stop, stop_time)
                #if i >= len(stops)-1:
                #    umlaeufe[(firstDep,vehicle)] += '        <stop lane="%s" until="%s" parking="true" />\n' % (toEdge+'_0', depart + OFFSET)
        umlaeufe[(firstDep,vehicle)] += '    </trip>\n'
    for (depart,vehicleId), string in sorted(umlaeufe.items(), key=operator.itemgetter(0)):
        outf.write(string)


def map_stops_to_lanes(places, net, stop2Modes):
    warnCounter = 0
    stop2lane = {}
    bbox = network.getBBoxXY() #[(bottom_left_X, bottom_left_Y), (top_right_X, top_right_Y)]
    for (pid, ptype), (name, lon, lat) in places.items():
        x, y = net.convertLonLat2XY(lon, lat)
        #print(ptype, x,y)
        #print(bbox)
        if ((int(ptype) < 3 and pid in stop2Modes) or int(ptype) > 6) and (x >= bbox[0][0] and x <= bbox[1][0] and y >= bbox[0][1] and y <= bbox[1][1]):
            #print('x=%s y=%s' % (x,y))
            lanes = net.getNeighboringLanes(x, y, r=10)
            if len(lanes) < 1:
                warnCounter += 1
                #if warnCounter < 10:
                print("Could not find a lane near stop %s (%s, type=%s)!" % (pid, name, ptype))
                continue
            lanes = sorted(lanes, key=lambda x : x[1])
            if int(ptype) < 3:
                for lane in lanes:
                    modes = stop2Modes[pid]
                    allowed = [lane[0].allows(mode) for mode in modes]
                    if sum(allowed) == len(modes):
                        l = lane[0]
                        # correction: if the stop is placed in the middle of the road, it might be more probable the stop lies at the side of the road
                        linkIndex = int(lane[0].getID().split('_')[1])
                        if linkIndex > 0:
                           testLane = net.getLane(lane[0].getID().split('_')[0]+'_0')
                           if sum([testLane.allows(mode) for mode in modes]) == len(modes):
                               l = testLane
                        stop2lane[pid] = [name, ptype, l, (x, y)]
                        break
            else:
                stop2lane[pid] = [name, ptype, lanes[0][0], (x, y)]
    return stop2lane


def correct_stop2lane(patchFile, stop2lane, net):
    with open(patchFile) as infile:
        for line in infile.readlines():
            parts = line.split(':')
            stop2lane[parts[0]][2] = net.getLane(parts[1])
    return stop2lane


def write_places(stop2lane):
    with open('stops.add.xml', 'w') as outf:
        outf.write('<additional>\n')
        for pid, (name, ptype, lane, (x, y)) in stop2lane.items():
            if int(ptype) < 3:
                outf.write(create_stop_string(pid, name, lane, (x, y)))
            elif int(ptype) == 7:
                outf.write(create_charging_station_string(pid, name, lane, (x, y)))
        outf.write('</additional>')


def create_stop_string(pid, name, lane, pos):
    minPos, dist = lane.getClosestLanePosAndDist(pos)
    if minPos < STOP_LENGTH:
        minPos = STOP_LENGTH
    return '    <busStop id="%s" lane="%s" startPos="%s" endPos="%s" name=%s friendlyPos="true" />\n' % (pid, lane.getID(), minPos - STOP_LENGTH, minPos, name)


def create_charging_station_string(pid, name, lane, pos, max_cap=200):
    minPos, minDist = lane.getClosestLanePosAndDist(pos)
    if minPos < STOP_LENGTH:
        minPos = STOP_LENGTH
    return '    <chargingStation id="%s" chargeDelay="2" chargeInTransit="1" power="%s" efficiency="0.95" endPos="%s" lane="%s" startPos="%s" friendlyPos="true" />\n' % (pid, max_cap * 1000, minPos, lane.getID(), minPos - STOP_LENGTH)


def create_route_fcd_file(places, routes):
    with open('bus_routes.xml', 'w') as outf:
        outf.write('<fcd-export>\n')
        outf.write('    <timestep time="%s"><vehicle id="%s_%s" x="%s" y="%s" until="%s" name="%s" fareZone="%s" fareToken="%s" startToken="%s" speed="20"/></timestep>\n')
        outf.write('</fcd-export>')


def create_route_gpx_file(places, routes):
    with open('bus_routes.gpx', 'w') as outf:
        outf.write('<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n')
        outf.write('<gpx version=\"1.0\"/>\n')
        #print stops
        for (line_nr, line_var), stops in routes.items():
            outf.write('    <trk><name>%s</name><trkseg>\n' % (line_nr + "_" + line_var))
            for stop in stops:
                id = stop
                if (id, type) in places.keys():
                    type_nr, name, lat, lon, cap = places[stop]
                    outf.write('        <trkpt lon=\"%s\" lat=\"%s\"><time>%s</time></trkpt>\n' % (lat, lon, 0))
            outf.write('    </trkseg></trk>\n')
        outf.write('</gpx>')

def write_places_csv(places):
    with open("places.csv", "w") as outf:
        outf.write("id;x;y;type\n")
        for (id, type), (name, lat, lon) in places.items():
            outf.write("%s;%s;%s;%s\n" % (id, lat, lon, type))


if __name__ == '__main__':
    options = get_options()
    if len(sys.argv) < 2:
        sys.stderr.write('  FATAL: No directory for VDV files given. Aborting...')
        sys.exit(1)
    BASE_DIR = sys.argv[1]
    OFFSET = options.departureOffset

    # read network
    network = readNet(options.netfile)

    # read functional place types
    func_places = read_functional_place_types()
    # read network points (stops, charging stations, depots)
    places = read_places()
    write_places_csv(places)
    stop_times = read_stop_times()
    sections = read_sections(places)
    domains = read_domains()
    # read vehicle types
    vTypes = read_vehicle_types()
    # read vehicles
    vehicles = read_vehicles()
    # read routes
    (routes, stops2lines) = read_routes(options.uselines, options.ignorelines)
    umlaeufe = read_umlaeufe(options.daytypes)
    trips = read_trips(vTypes, options.daytypes, options.uselines, options.ignorelines)

    #create_route_gpx_file(places, routes)
    
    #places = remove_disregarded_stops(places, stops2lines)
    veh_trips, stop2Modes = create_trips(routes, trips, umlaeufe, network, options.generateUmlauf)
    stop2lane = map_stops_to_lanes(places, network, stop2Modes)
    if options.stopPatchFile:
        stop2lane = correct_stop2lane(options.stopPatchFile, stop2lane, network)
    write_places(stop2lane)
    write_route_file(vTypes, vehicles, routes, veh_trips, stop_times, stop2lane, options.generateUmlauf)
