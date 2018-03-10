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

DATAFILE = 'coinc.h5'
# STATIONS = [501, 502, 503, 505, 506, 508, 509, 510, 511]
STATIONS = [505, 509, 504]

# 2017 1 1 naar 2017 1 2 met N=9 geeft mooie resultaten met stations 501 502 503 505
START = datetime(2016, 10, 1)
END = datetime(2017, 1, 1)
N = 3 # Voor reconstructions minimum N=3

force_datafile_overwrite = False

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
# Melkweg contouren als lijst van RA, DEC paren.
# `milky_way.npy` heeft *geen* verbinding tussen RA 23h59 en 0h00 en `milky_way_polar.npy` wel.
try:
    mw_contour = np.load('milky_way.npy')
    mw_contour_polar = np.load('milky_way_polar.npy')
except:
    mw_contour = mw_contour_polar = []


def plot_events_on_mollweide(events, filename=None):
    """Plot events (een lijst van RA, DEC tuples) op een kaart in Mollweide projectie"""

    # Let op: De RA-as is gespiegeld. Alle RA coordinates worden gespiegeld (negatief)
    # geplot.

    events = np.array(events)

    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection="mollweide")
    # let op: De RA as is gespiegeld:
    ax.set_xticklabels(['22h', '20h', '18h', '16h', '14h', '12h', '10h', '8h', '6h', '4h', '2h'], fontsize='large')
    ax.grid(True)

    # plot milky way contours
    for ra_mw, dec_mw in mw_contour:
        ax.plot(-ra_mw, dec_mw, color='grey')

    # plot steelpan in UMa
    ra_uma = np.radians(steelpan[:, 0] / 24 * 360 - 180.)
    dec_uma = np.radians(steelpan[:, 1])
    ax.plot(-ra_uma, dec_uma, color='red')
    ax.scatter(-ra_uma, dec_uma, color='red')

    # plot Polaris
    ax.scatter(0., np.radians(90.), color='red')

    # plot Galactic Center (RA 17h45, DEC -29)
    ax.scatter(-np.radians(17.75 / 24 * 360 - 180.), np.radians(-29), color='red', marker='*')

    """
    Plot bron:
    https://python-graph-gallery.com/85-density-plot-with-matplotlib/
    """
    from scipy.stats import kde
    x = -events[:,0]
    y = events[:,1]

    # Evaluate a gaussian kde on a regular grid of nbins x nbins over data extents
    nbins = 300
    k = kde.gaussian_kde([x, y])
    xi, yi = np.mgrid[x.min():x.max():nbins * 1j, y.min():y.max():nbins * 1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))

    # Make the plot
    plt.pcolormesh(xi, yi, zi.reshape(xi.shape))
    #plt.pcolormesh(xi, yi, zi.reshape(xi.shape), cmap=plt.cm.Greens_r)
    plt.colorbar()
    plt.show()

    if filename:
        plt.savefig(filename, dpi=200)

def plot_events_polar(events, filename=None):
    """Plot events (een lijst van RA, DEC paren) op een hemelkaart van de noordelijke hemel"""

    # Let op: De RA-as is gespiegeld. Alle RA coordinates worden gespiegeld (negatief)
    # geplot.

    events = np.array(events)

    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111, projection="polar")

    # let op: De RA as is gespiegeld:
    ax.set_xticklabels(['12h', '9h', '6h', '3h', '0h', '21h', '18h', '15h'], fontsize='large')
    ax.set_yticklabels(['80', '70', '60', '50', '40', '30', '20', '10', '0'])

    ax.grid(True)
    ax.set_theta_zero_location("W")


    # plot milky way contours
    for ra_mw, dec_mw in mw_contour_polar:
        ax.plot(-ra_mw, 90. - np.degrees(dec_mw), color='grey')

    # plot UMa
    ra_uma = np.radians(steelpan[:, 0] / 24 * 360 - 180)
    dec_uma = np.radians(steelpan[:, 1])
    ax.plot(-ra_uma, 90. - np.degrees(dec_uma), color='red')
    ax.scatter(-ra_uma, 90. - np.degrees(dec_uma), color='red')
    # plot Polaris
    ax.scatter(0., 0., color='red')

    # plot reconstructions
    ax.scatter(-events[:,0], 90. - np.degrees(events[:,1]), marker='x')
    ax.set_rmax(90.0)
    if filename:
        plt.savefig(filename, dpi=200)
    plt.show()


plot_events_on_mollweide(events, filename='figuren\\noordelijke hemel mollweide.png')

#plot_events_polar(events, filename='figuren\\noordelijke hemel polar.png')

data.close()