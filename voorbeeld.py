"""
Bron van de code welke gebruikt is als basis:
https://github.com/HiSPARC/infopakket/blob/master/notebooks/10_sterrenkaart.md

Merk op dat hier en daar iets is aangepast
"""

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

t0 = time.time()

DATAFILE = 'coinc.h5'
#STATIONS = [501, 502, 503, 505, 506, 508, 509, 510, 511]
#STATIONS = [305, 304, 301]  # 1,75 km uit elkaar

"""
Waarschijnlijk moeten stations uit nijmegen gebruikt worden, deze zijn het oudst
"""

STATIONS = [8001, 8004, 8009, 8008]

START = datetime(2014, 3, 1)
END = datetime(2017, 6, 2)
N = 4  # Voor reconstructions minimum N=3

force_datafile_overwrite = True
show_events = True

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

recs = data.root.coincidences.reconstructions.read()
theta = recs['zenith']
recs = recs.compress(~np.isnan(theta))

print("Aantal reconstructions : %d " % (len(recs)))

lla = HiSPARCStations(STATIONS).get_lla_coordinates()
lat, lon, alt = lla
print(lat, lon)

events = []
for rec in pbar(recs):
    timestamp = rec['ext_timestamp'] / 1.e9
    theta = rec['zenith']
    phi = rec['azimuth']
    r, d = zenithazimuth_to_equatorial(lat, lon, timestamp, theta, phi)
    events.append((r-np.pi, d))
events = np.array(events)

ra = np.degrees(events[:, 0])

dec = np.degrees(events[:, 1])

# RA, DEC tuples van het steelpan asterisme in het sterrenbeeld Grote Beer
steelpan = np.array([[13.792222, 49.3167], [13.398889, 54.9333], [12.900556, 55.95],
                     [12.257222, 57.0333], [11.896944, 53.7000], [11.030833, 56.3833],
                     [11.062222, 61.7500], [12.257222, 57.0333]])

mw_contour = mw_contour_polar = []

t2 = time.time()
print('Getting to the plots took: %.2f' % (t2-t1))


def plot_events_on_mollweide(events, filename=None):
    """Plot events (een lijst van RA, DEC tuples) op een kaart in Mollweide projectie"""

    # Let op: De RA-as is gespiegeld. Alle RA coordinates worden gespiegeld (negatief)
    # geplot.

    events = np.array(events)
    print(events)

    fig = plt.figure(figsize=(15, 15))
    #fig = plt.figure()
    ax = fig.add_subplot(111, projection="mollweide")
    # let op: De RA as is gespiegeld:
    ax.set_xticklabels(['22', '20', '18', '16', '14', '12', '10', '8', '6', '4', '2'], fontsize='large')
    ax.set_yticklabels(['-75', '-60', '-45', '-30', '-15', '0', '15', '30', '45', '60', '75'], fontsize='large')
    ax.grid(True)
    ax.tick_params(axis='x', colors='white')
    ax.xaxis.label.set_color('white')
    ax.xaxis.set_label_coords(.5, .49)

    """
    Plot bron:
    https://python-graph-gallery.com/85-density-plot-with-matplotlib/
    """
    from scipy.stats import kde
    x = -events[:, 0]
    y = events[:, 1]

    # Evaluate a gaussian kde on a regular grid of nbins x nbins over data extents
    nbins = 100
    k = kde.gaussian_kde([x, y])
    xi, yi = np.mgrid[x.min():x.max():nbins * 1j, y.min():y.max():nbins * 1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))
    """ 
    Colormaps: https://matplotlib.org/examples/color/colormaps_reference.html
    jet

    """
    plt.pcolormesh(xi, yi, zi.reshape(xi.shape), cmap=plt.cm.jet, alpha=1)
    plt.colorbar(shrink=0.5, pad=0.01)
    if show_events:
        ax.scatter(-events[:, 0], events[:, 1], marker='x', alpha=.5, color='grey', label='events')

    # plot milky way contours
    for ra_mw, dec_mw in mw_contour:
        ax.plot(-ra_mw, dec_mw, color='grey')

    # plot steelpan in UMa
    ra_uma = np.radians(steelpan[:, 0] / 24 * 360 - 180.)
    dec_uma = np.radians(steelpan[:, 1])
    ax.plot(-ra_uma, dec_uma, color='white')
    ax.scatter(-ra_uma, dec_uma, color='white', s=10)

    # plot Polaris
    #ax.scatter(0., np.radians(90.), color='white', marker='*')
    #ax.text(np.radians(2.), np.radians(78.), 'Polaris', color='white', fontsize='10')

    # plot Galactic Center (RA 17h45, DEC -29)
    #ax.scatter(-np.radians(17.75 / 24 * 360 - 180.), np.radians(-29), color='white', marker='*')
    #ax.text(-np.radians(17.75 / 24 * 360 - 180. +2.), np.radians(-29 - 6.), 'Galactic Center', color='white', fontsize='10')

    t3 = time.time()
    print('Plotting took: %.2f' % (t3-t2))
    print('Total run time: %.2f' % (t3 - t0))
    plt.grid(alpha=.2)
    plt.xlabel('Rechte klimming [h]', fontsize='large')
    plt.ylabel('Declinatie [°]', fontsize='large')
    plt.tight_layout()
    #plt.legend()
    plt.show()

    if filename:
        plt.savefig(filename, dpi=200)


plot_events_on_mollweide(events, filename='figuren\\noordelijke hemel mollweide.png')

#plot_events_polar(events, filename='figuren\\noordelijke hemel polar.png')

data.close()