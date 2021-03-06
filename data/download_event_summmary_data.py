import datetime
import tables
from sapphire import esd
import pandas as pd

dir = 'event_summary_data\\'
DATAFILE = dir+'data.h5'
STATIONS = [501, 503, 506]
START = datetime.datetime(2016, 1, 1)
END = datetime.datetime(2016, 1, 2)


if __name__ == '__main__':
    if 'data' not in globals():
        data = tables.open_file(DATAFILE, 'a')

    for station in STATIONS:
        group = '/s%d' % station
        if group not in data:
            esd.download_data(data, group, station, START, END)

store = pd.HDFStore(DATAFILE)
print(store)
print('-----------')
#print(data)