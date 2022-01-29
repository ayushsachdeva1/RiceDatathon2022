import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='cass', resolution='l',
            width=3E6, height=3E6, 
            lat_0=28.5, lon_0=-91)
m.bluemarble()

# Map (long, lat) to (x, y) for plotting
x, y = m(-88.289, 28.521)
plt.plot(x, y, 'ok', markersize=5, color='white')
plt.text(x, y, '  KIKT', fontsize=12, color='white')
x, y = m(-95.620, 28.314)
plt.plot(x, y, 'ok', markersize=5, color='white')
plt.text(x, y, '  KBQX', fontsize=12, color='white')
x, y = m(-88.842, 29.296)
plt.plot(x, y, 'ok', markersize=5, color='white')
plt.text(x, y, '  KMIS', fontsize=12, color='white')

x, y = m(-88.289, 28.521)
origin = np.array([[x],[y]])
vector = np.array([[1, 1]])
plt.quiver(*origin, vector[:,0], vector[:,1], color = ['r'], scale=14)
plt.show()

# origin = np.array([[0],[0]])
# vector = np.array([[1, 1]])
# plt.quiver(*origin, vector[:0], vector[:,1], color = ['r'], scale=14)
# plt.show()

#location['KIKT'] = (28.521, -88.289)
#location['KBQX'] = (28.314, -95.620)
#location['KMIS'] = (29.296, -88.842)