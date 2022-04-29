#!/bin/bash
netconvert -c miv.netccfg
netconvert -c miv2.netccfg
duarouter -c fromgeo.duarcfg
