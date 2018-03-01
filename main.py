import datetime
import tables
from sapphire import esd
from sapphire.analysis import reconstructions
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dir = 'data\directions_for_coincidences\\'
DATAFILE = dir+'data.h5'
#STATIONS = [501, 503, 506]
STATIONS = [501]
START = datetime.datetime(2016, 1, 1)
END = datetime.datetime(2016, 1, 2)

df = pd.DataFrame()


def create_df(data):
    global df
    events = data.root.coincidences.reconstructions

    zenith = events.col('zenith')
    azimuth = events.col('azimuth')
    ext_timestamp = events.col('ext_timestamp')
    id = events.col('id')

    df = pd.DataFrame()
    df['id'] = id
    df['ext_timestamp'] = ext_timestamp
    df['zenith'] = zenith
    df['azimuth'] = azimuth

    df = df.dropna()

    print(df)


def save_df():
    df.to_csv('data\\heatmap_data.csv', sep='\t')


def plot_hoeken():
    plt.figure(1)
    plt.subplot(211)
    plt.hist(df['zenith'])
    plt.xlabel("zenith [deg]")
    plt.ylabel("count")

    plt.subplot(212)
    plt.hist(df['azimuth'])
    plt.xlabel("azimuth [deg]")
    plt.ylabel("count")

    plt.tight_layout()
    plt.show()

def heatmap():
    plt.plot(df['zenith'], df['azimuth'], '.')
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


create_df(data)
save_df()