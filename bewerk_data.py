from __future__ import division, print_function

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import tables
from sapphire import (download_coincidences, ReconstructESDCoincidences, HiSPARCStations)
from sapphire.utils import pbar
from sapphire.transformations.celestial import zenithazimuth_to_equatorial
import os
import time

DATAFILE = 'coinc.h5'
STATIONS = [2003, 2004, 2005, 2008, 2001, 2002, 2006]

show_events = False

t0 = time.time()

if __name__ == '__main__':
    if 'data' not in globals():
        # 'r+' an existing file is opened for reading and writing
        print('Opening data file')
        try:
            data = tables.open_file(DATAFILE, 'r+')
        except:
            print('Could not open data file, exit()')
            exit()
            pass

t1 = time.time()
print('Opening data took: %.5f' % (t1-t0))
print('Aantal coincidenties: %s' % len(data.root.coincidences.coincidences))

recs = data.root.coincidences.reconstructions.read()
theta = recs['zenith']
recs = recs.compress(~np.isnan(theta))

t2 = time.time()
print('Removing NaNs from recs[theta] took: %.5f' % (t2-t1))

print("Aantal reconstructions : %.2f " % (len(recs)))

lla = HiSPARCStations(STATIONS).get_lla_coordinates()
lat, lon, alt = lla

t3 = time.time()
print('get_lla_coordinates() took: %.5f' % (t3-t2))


events = []
for rec in pbar(recs):
    timestamp = rec['ext_timestamp'] / 1.e9
    theta = rec['zenith']
    phi = rec['azimuth']
    r, d = zenithazimuth_to_equatorial(lat, lon, timestamp, theta, phi)  # Zelf maken zodat het sneller gaat?
    events.append((r-np.pi, d))
events = np.array(events)

t4 = time.time()
print('Creating events = np.array(events) took: %.5f' % (t4 - t3))

ra = np.degrees(events[:, 0])

dec = np.degrees(events[:, 1])

t5 = time.time()
print('RA & DEC naar degrees omzetten took: %.5f' % (t5 - t4))


t6 = time.time()
print('Total runtime: %.2f' % (t6-t0))
