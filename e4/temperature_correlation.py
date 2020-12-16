import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

file1 = sys.argv[1]
file2 = sys.argv[2]
file3 = sys.argv[3]

stations = pd.read_json(file1, lines=True)
city = pd.read_csv(file2)

stations['avg_tmax'] = stations['avg_tmax']/10
city = city.dropna()

city['area'] = city['area']/1000000
city.drop(city[city.area > 10000].index, inplace=True)
city['density'] = city['population']/city['area']

# https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dLat = deg2rad(lat2-lat1)  
    dLon = deg2rad(lon2-lon1) 
    a = np.sin(dLat/2) * np.sin(dLat/2) + np.cos(deg2rad(lat1)) * np.cos(deg2rad(lat2)) * np.sin(dLon/2) * np.sin(dLon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a)) 
    d = R * c
    return d * 1000

def deg2rad(deg):
  return deg * (np.pi/180)

def distance(city2, stations):
    lat1 = city2['latitude']
    lon1 = city2['longitude']
    lat2 = stations['latitude']
    lon2 = stations['longitude']
    return haversine(lat1, lon1, lat2, lon2)

def best_tmax(city2, stations2):
	stations2['distance'] = distance(city2, stations2)
	min_ind = stations2.distance.idxmin
	return stations2.loc[min_ind]['avg_tmax']

city['avg_tmax'] = city.apply(best_tmax, axis=1, stations2=stations)
plt.scatter(city.avg_tmax, city.density)
plt.title('Temperature vs Population Density')
plt.xlabel('Avg Max Temperature (\u00b0C)')
plt.ylabel('Population Density (people/km\u00b2)')
plt.savefig(file3)
