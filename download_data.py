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

# 2017 1 1 naar 2017 1 2 met N=9 geeft mooie resultaten met stations 501 502 503 505

START = datetime(2016, 1, 1)
END = datetime(2017, 1, 1)
N = 9

file_name = 'coinc'
dir = 'data\\coincidences\\'
DATAFILE = dir+file_name+'.h5'
STATIONS = [501, 502, 503, 505, 506, 508, 509, 510, 511]
#STATIONS = [505, 509]

overwrite = True
reconstruct = False

if __name__ == '__main__':
    if overwrite:
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
    if ('/coincidences/reconstructions' not in data) & reconstruct:
        print('Creating reconstructions')
        rec = ReconstructESDCoincidences(data, overwrite=True)
        rec.reconstruct_and_store()
    if len(data.root.coincidences.coincidences) == 0:
        print('Aantel showers == 0')
        exit()

print("Aantal showers (coincidenties n=%d stations): %d " % (N, len(data.root.coincidences.coincidences)))