import tables
#from pylab import *
import matplotlib.pyplot as plt
import numpy as np

dir = 'directions_for_coincidences\\'


def plot_zenith_distribution(data):
    events = data.root.coincidences.reconstructions

    # get all zenith values
    zenith = events.col('zenith')

    # remove all NaNs.
    zenith = zenith.compress(~np.isnan(zenith))

    plt.hist(zenith)
    plt.xlabel("zenith [deg]")
    plt.ylabel("count")
    plt.show()


if __name__ == '__main__':
    if 'data' not in globals():
        data = tables.open_file(dir+'data.h5')

    plot_zenith_distribution(data)