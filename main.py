import datetime
import tables
from sapphire import esd
from sapphire.analysis import reconstructions
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dir = 'data\directions_for_coincidences\\'
DATAFILE = dir+'data.h5'
STATIONS = [501, 503, 506]
START = datetime.datetime(2016, 1, 1)
END = datetime.datetime(2016, 1, 2)


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


def print_data():
    """
    Print de datafile om inzicht te krijgen in de inhoud ervan
    :return:
    """
    store = pd.HDFStore(DATAFILE)
    print(store)
    store.close()


print_data()

if __name__ == '__main__':
    if 'data' not in globals():
        # ‘a’: Append; an existing file is opened for reading and writing, and if the file does not exist it is created.
        data = tables.open_file(DATAFILE, 'a')

    if '/coincidences' not in data:
        esd.download_coincidences(data, stations=STATIONS, start=START, end=END)

    #if '/reconstructions' not in data:
    #    rec = reconstructions.ReconstructESDCoincidences(data)
    #    rec.reconstruct_and_store()

plot_zenith_distribution(data)