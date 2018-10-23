from datetime import datetime
import time
import os
from databasemanager import Database as Db
from collections import namedtuple
import urllib.request as url
import json
import math
from geopy.geocoders import Nominatim
# import aiohttp
import asyncio

INSTANCE = "01"


class Position:
    def __init__(self):
        self.location = "None (International waters)"
        self.hemisphere = "Unknown"
        self.latitude = 0
        self.longitude = 0
        self.api_return = None
        self.timestamp = None
        self.date = None
        self.coordinates = (self.latitude, self.longitude)
        self.request_failed = False

    def time_format(self, utc):
        if utc is False:
            self.date = datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.date = datetime.utcfromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')  # TODO: giving utc suffix regardless???
            self.date = self.date + " (UTC)"

    def get_pos(self, utc=bool):  # TODO: http error handling
        try:
            request = url.urlopen("http://api.open-notify.org/iss-now.json").read()
            loaded = json.loads(request)
            if loaded["message"] == "success":
                self.api_return = True
                self.latitude = float(loaded["iss_position"]["latitude"])
                self.longitude = float(loaded["iss_position"]["longitude"])
                self.timestamp = int(loaded["timestamp"])
                self.time_format(utc)
            else:
                self.api_return = False
        except url.URLError or url.HTTPError:
            self.request_failed = True

    # TODO: find correct way to parse json in aiohttp

    def api_check(self):
        if self.api_return is None:
            self.get_pos()  # TODO: correct use of await?

    def location_query(self):
        self.api_check()

        query = "%d,%d" % (self.latitude, self.longitude)
        address = Nominatim(user_agent=("iss_checker_unit_%s" % INSTANCE))  # https://bit.ly/2RLDLOA
        try:
            self.location = str(address.reverse(query))
        except TypeError:
            self.location = "None (International waters)"

    def get_hemisphere(self):
        self.api_check()
        lat = self.latitude
        lon = self.longitude
        if lat >= 0:
            lat = "NORTH"
        else:
            lat = "SOUTH"
        if lon >= 0:
            lon = "EAST"
        else:
            lon = "WEST"

        self.hemisphere = lat + " " + lon + " " + "HEMISPHERE"  # TODO: can attributes be declared outside __init__?

    def orbit_distance(self, pos1, pos2):
        self.api_check()
        return distance(pos1, pos2)

    @staticmethod
    def distance_legacy(pos1, pos2):
        lat1 = float(pos1[0])
        lon1 = float(pos1[1])
        lat2 = float(pos2[0])
        lon2 = float(pos2[1])
        # lat1, lon1 = int(origin)
        # lat2, lon2 = int(destination)
        radius = 6779  # radius of ISS orbit in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(
            dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return radius * c

# class Calculate(Position):
  #  def __init__(self):
   #     Position.__init__(self)




if __name__ == "__main__":
    position = Position()

    # TODO: need to create event loop to use methods
    # TODO: dont add asyncio until end of successful test build