"""
Bron van de code: https://github.com/HiSPARC/infopakket/blob/master/notebooks/10_sterrenkaart.md
Merk op dat hier en daar iets is aangepast
"""

# dit notebook werkt onder Python 2 en 3
from __future__ import division, print_function

# importeer modules en functies
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import tables
from sapphire import (download_coincidences, ReconstructESDCoincidences, HiSPARCStations)
from sapphire.utils import pbar
from sapphire.transformations.celestial import zenithazimuth_to_equatorial
import os
import time

t0 = time.time()

DATAFILE = 'coinc.h5'
#STATIONS = [501, 502, 503, 505, 506, 508, 509, 510, 511] # science park
STATIONS = [501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511]  # science park cluster

#STATIONS = [305, 304, 301]  # 1,75 km uit elkaar

"""
Waarschijnlijk moeten stations uit nijmegen gebruikt worden, deze zijn het oudst (data vanaf 2014).
"""

#STATIONS = [2003, 2004, 2005, 2008, 2001, 2002, 2006]

START = datetime(2016, 3, 1)
END = datetime(2018, 1, 2)
N = 11  # Voor reconstructions minimum N=3

force_datafile_overwrite = True
show_events = False

if __name__ == '__main__':
    if force_datafile_overwrite:
        try:
            print('Deleting data file')
            os.remove(DATAFILE)
        except:
            print('Could not delete file')
            pass
    if 'data' not in globals():
        # ‘a’: Append; an existing file is opened for reading and writing, and if the file does not exist it is created.
        print('Opening data file')
        data = tables.open_file(DATAFILE, 'a')
    if '/coincidences' not in data:
        print('Downloading coincidences')
        download_coincidences(data, stations=STATIONS, start=START, end=END, n=N)
    if len(data.root.coincidences.coincidences) == 0:
        print('Aantel showers == 0, exit()')
        exit()
    if '/coincidences/reconstructions' not in data:
        print('Creating reconstructions')
        rec = ReconstructESDCoincidences(data, overwrite=True)
        rec.reconstruct_and_store()
    if len(data.root.coincidences.reconstructions.read()) == 0:
        print('Aantel recs == 0, exit()')
        exit()

t1 = time.time()
print('Datafile preperation took: %.2f' % (t1-t0))

print("Aantal showers (coincidenties n=%d stations): %d " % (N, len(data.root.coincidences.coincidences)))