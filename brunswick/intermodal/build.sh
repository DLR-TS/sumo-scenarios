#!/bin/bash
netconvert -c intermodal_pre.netccfg
netconvert -c intermodal.netccfg
duarouter -c fromgeo.duacfg
