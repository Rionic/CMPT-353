import pandas as pd 
import numpy as np 
import xml.etree.ElementTree as et 
import sys
from xml.dom.minidom import parse
from math import radians, cos, sin, asin, sqrt
from pykalman import KalmanFilter


def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')


# references:
# https://www.guru99.com/manipulating-xml-with-python.html
# https://medium.com/@robertopreste/from-xml-to-pandas-dataframes-9292980b1c1c
def get_data(file):	
	data = parse(file)
	res = data.getElementsByTagName("trkpt")
	df = pd.DataFrame(columns=['lat', 'lon'])

	for item in res:
	    lat = float(item.getAttribute('lat'))
	    lon = float(item.getAttribute('lon'))
	    df = df.append(pd.DataFrame({"lat": [lat], "lon": [lon]}),
	     ignore_index = True)

	return df


def distance(points):
	lat1 = points['lat'].shift(1)
	lon1 = points['lon'].shift(1)
	lat2 = points['lat']
	lon2 = points['lon']

	dist = haversine(lat1, lon1, lat2, lon2)
	print(dist)
	return dist.sum()


# reference
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


def smooth(df):
	initial_state = df.iloc[0]
	observation_covariance = np.diag([20, 20]) ** 2 
	transition_covariance = np.diag([10, 10]) ** 2
	transition = [[1, 0], [0, 1]]

	kf = KalmanFilter(initial_state_mean=initial_state,
	                 initial_state_covariance=observation_covariance,
	                 observation_covariance=observation_covariance,
	                 transition_covariance=transition_covariance,
	                 transition_matrices=transition)
	kalman_smoothed, _ = kf.smooth(df)
	kalman_smoothed = pd.DataFrame(kalman_smoothed)
	kalman_smoothed = kalman_smoothed.rename(columns={0: 'lat', 1: 'lon'})
	return kalman_smoothed


def main():
	points = get_data(sys.argv[1])
	print('Unfiltered distance: %0.2f' % (distance(points)))
	smoothed_points = smooth(points)
	print('Filtered distance: %0.2f' % (distance(smoothed_points)))
	output_gpx(smoothed_points, 'out.gpx')

if __name__ == '__main__':
	main()
