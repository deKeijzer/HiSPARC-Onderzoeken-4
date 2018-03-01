import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data\\heatmap_data.csv'\
                 , sep='\t', header=1, names=['id', 'ext_timestamp', 'zenith', 'azimuth'], decimal=".")

plt.plot(df['azimuth'], df['zenith'], '.')
plt.show()