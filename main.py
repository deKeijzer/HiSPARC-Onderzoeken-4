import tables
import datetime
from sapphire import esd
import matplotlib.pyplot as plt
import sapphire.time_util


#Directory, naam en file format van het data bestand
dir = 'data\\'
data_file = 'data'
file_extension = '.h5'

def download_data():
    """
    Download de data van station_number van start tot end tijden.
    Slaat de data op in data_file
    :return:
    """
    station_number = 501
    start = datetime.datetime(2016, 1, 1)
    end = datetime.datetime(2016, 1, 2)

    # Kijkt of het bestand al open is
    if 'data' not in globals():
        data = tables.open_file(dir+data_file+file_extension, 'w')
    # Kijkt of de data van station_number al bestaat
    if '/s'+str(station_number) not in data:
        esd.download_data(data, '/s'+str(station_number), station_number, start, end)

download_data()





#data = esd.quick_download(102)
#data = tables.open_file('mydata.h5', 'w')

#start = sapphire.time_util.GPSTime(2012, 12, 2, 12).gpstimestamp()
#end = sapphire.time_util.GPSTime(2012, 12, 2, 13).gpstimestamp()


#events = data.root.s501.events

#sel_events = events.read_where('(t0 <= timestamp) & (timestamp < t1)')

#esd.download_data(data, '/s501', 501, start, end)


#print(events[0]['pulseheights'])

#ph = events.col('pulseheights')

#plt.hist(ph)
#plt.show()