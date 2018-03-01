import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data\\heatmap_data.csv'\
                 , sep='\t', header=1, names=['id', 'ext_timestamp', 'zenith', 'azimuth'], decimal=".")


x = df['zenith']
y = df['azimuth']

plt.figure()
plt.subplot(111, projection="mollweide")
plt.scatter(x, y, s=1)
plt.grid()

plt.show()

print(x)