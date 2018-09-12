import urllib.request as url
import json
import math
try:
    from geopy.geocoders import Nominatim
except:
    pass


def location_query(position):
    location_query_latitude = str(position.get("latitude"))
    location_query_longitude = str(position.get("longitude"))
    try:
        constructed_query = location_query_latitude + "," + location_query_longitude
        address = Nominatim(user_agent="iss-checker1")
        location = address.reverse(constructed_query)
        return location.address
    except:
        pass


def distance(origin, destination):  # Measures distance between one global position and one variable second position
    lat1 = float(origin.get("latitude"))
    lon1 = float(origin.get("longitude"))
    lat2 = float(destination.get("latitude"))
    lon2 = float(destination.get("longitude"))
    # lat1, lon1 = int(origin)
    # lat2, lon2 = int(destination)
    radius = 6779  # radius of ISS orbit in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
                                                  * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(
        dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def hemisphere_check(position):  # Checks for current hemisphere
    lat = float(position.get("latitude"))
    lon = float(position.get("longitude"))

    if lat >= 0:
        lat = "NORTH"
    else:
        lat = "SOUTH"
    if lon >= 0:
        lon = "EAST"
    else:
        lon = "WEST"

    final = lat + " " + lon + " " + "HEMISPHERE"
    return final


def pos_update():  # Sends a GET request for information about the ISS (position w/ timestamp
    try:
        url_data = url.urlopen("http://api.open-notify.org/iss-now.json").read()
        loaded = json.loads(url_data)
        return loaded
    except Exception:
        print("Could not retrieve position")
        return 1

