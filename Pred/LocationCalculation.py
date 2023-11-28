import numpy as np
import pickle

# Search Radius (m)
SEARCH_RADIUS = 200
# Field of View (degrees)
FOV = 120

def haversine(lon1, lat1, lon2, lat2):
  """
  Calculate the great circle distance between two points
  on the earth (specified in decimal degrees)

  All args must be of equal length/precision.

  Args:
    long1 (double): longitude of first location
    lat1 (double): latitude of first location
    lon2 (double): longitude of second location
    lat2 (double): latitude of second location

  Returns
    distance (double): distance between two coordinates in (m)
  """

  earthr = 6378137
  lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

  dlon = lon2 - lon1
  dlat = lat2 - lat1

  a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
  c = 2 * np.arcsin(np.sqrt(a))
  m = earthr * c

  return m


def get_bearing(lon1, lat1, lon2, lat2):
  """
  Calculate bearing angle between two coordinates in degrees
  (from 1 to 2 where 1 is current location).

  Args:
    long1 (double): longitude of first location
    lat1 (double): latitude of first location
    lon2 (double): longitude of second location
    lat2 (double): latitude of second location

  Returns:
    bearing (double): bearing angle from coordinate 1 to coordinate 2
  """

  lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

  dLon = (lon2 - lon1)

  x = np.cos(lat2) * np.sin(dLon)
  y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dLon)
  brng = np.arctan2(x,y)
  brng = (np.degrees(brng) + 360) % 360

  return brng


def get_valid_buildings(my_long, my_lat, my_bearing):
  """
  Determine valid buildings from dataset within user's field of view
  
  Args:
    my_long (double): longitude of first location
    my_lat (double): latitude of first location
    my_bearing (double): bearing angle of user (in degrees)

  Returns:
    valid_buildings (list): list of valid building names

  Note: 
    - Bearing of 0 degrees = North, moving clockwise
    - Google Maps gives coordinates as (Lat, Long), this wants (Long, Lat)
  """

  data_file = 'Pred/building_info.pkl'

  with open(data_file, "rb") as handle:
    building_info = pickle.load(handle)

  valid_buildings = []

  for name, (id, latitude, longitude) in building_info.items():
    distance = haversine(my_long, my_lat, longitude, latitude)
    angle = get_bearing(my_long, my_lat, longitude, latitude)

    angle_diff = (angle - my_bearing) % 360
    abs_diff = np.minimum(angle_diff, 360 - angle_diff)

    if abs_diff < FOV / 2 and distance < SEARCH_RADIUS:
      valid_buildings.append(name)

  return valid_buildings
