import tables
import datetime
from sapphire import esd
import matplotlib.pyplot as plt

data = tables.open_file('mydata.h5', 'w')

start = datetime.datetime(2012, 10, 15, 19)
end = datetime.datetime(2012, 10, 20, 21)

esd.download_data(data, '/s501', 501, start, end)

events = data.root.s501.events

print(events[0]['pulseheights'])

ph = events.col('pulseheights')

plt.hist(ph)
plt.show()