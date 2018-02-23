import tables
from pylab import *


dir = 'directions_for_coincidences\\'


def plot_zenith_distribution(data):
    events = data.root.coincidences.reconstructions

    # get all zenith values
    zenith = events.col('zenith')

    # remove all NaNs.
    zenith = zenith.compress(~isnan(zenith))

    plt.hist(degrees(zenith), bins=linspace(0, 90, 51), histtype='step')
    plt.xlabel("zenith [deg]")
    plt.ylabel("count")
    plt.show()


if __name__ == '__main__':
    if 'data' not in globals():
        data = tables.open_file(dir+'data.h5')

    plot_zenith_distribution(data)