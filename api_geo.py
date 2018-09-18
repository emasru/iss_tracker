from datetime import datetime
import time
import os
from databaseManager import Database as Db
from collections import namedtuple
import urllib.request as url
import json
import math
try:
    from geopy.geocoders import Nominatim
except:
    pass


class Tracker:
    def __init__(self, version):

        print("ISS Tracker // Author: Henning S. & Birk N.")
        print("Version:", version)
        print("Starting up...")

        global first_position_timestamp
        self.data = namedtuple("data", "time velocity long lat identifier")
        self.d = Db("recorded_positions")
        self.id_to_use = self.d.largest_identifier() + 1
        self.i = 0

    def location_query(self, position):
        location_query_latitude = str(position.get("latitude"))
        location_query_longitude = str(position.get("longitude"))
        try:
            constructed_query = location_query_latitude + "," + location_query_longitude
            address = Nominatim(user_agent="iss-checker1")
            location = address.reverse(constructed_query)
            return location.address
        except:
            pass

    def distance(self, origin, destination):  # Measures distance between one global position and one variable second position
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

    def hemisphere_check(self, position):  # Checks for current hemisphere
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

    def pos_update(self):  # Sends a GET request for information about the ISS (position w/ timestamp
        try:
            url_data = url.urlopen("http://api.open-notify.org/iss-now.json").read()
            loaded = json.loads(url_data)
            return loaded
        except Exception:
            print("Could not retrieve position")
            return 1

    def run(self):
        while True:
            if self.i == 0:  # Init: Tracks the global first position and sets the wait_time
                wait_time = int(input("Seconds between position updates? (MUST BE MORE THAN 1): "))
                if wait_time < 1:
                    wait_time = 1
                print("Tracking first position...")
                contents = self.pos_update()
                if contents == 1:
                    break
                position1 = contents.get("iss_position")
                try:
                    geo_name = self.location_query(position1)
                except:
                    pass
                hemisphere = self.hemisphere_check(position1)
                os.system("cls")
                print("The current position of the ISS is Lat:", position1.get("latitude"), " and Lon:",
                      position1.get("longitude"), "//", hemisphere)
                try:
                    print("Current address: ", geo_name)
                except:
                    pass
                timestamp = int(contents.get("timestamp"))
                first_position_timestamp = timestamp
                print("Timestamp (UTC): ", datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
                print(" ")
            if self.i > 0:  # Tracks the second position every wait_time seconds and calculates the average speed constanly based
                #        on the first position
                contents = self.pos_update()  # Updates position
                if contents == 1:  # If the function returns a 1 it means it has encountered an HTTP exception,
                    break  # and kills the program
                timestamp = int(contents.get("timestamp"))
                position2 = contents.get("iss_position")
                try:
                    geo_name = self.location_query(position2)  # Fetches the current address
                except:
                    pass
                hemisphere = self.hemisphere_check(position2)
                distance_measure = self.distance(position1, position2)
                v = distance_measure / (wait_time * self.i)
                distance_measure = round(distance_measure, 2)
                v = round(v, 2)
                if wait_time < 5:
                    v = None
                os.system("cls")

                print("The current position of the ISS is Lat:", position2.get("latitude"), " and Lon:",
                      position2.get("longitude"), "//", hemisphere)
                print("Distance traveled from first position: ", distance_measure, "km", "(",
                      datetime.utcfromtimestamp(first_position_timestamp).strftime('%Y-%m-%d %H:%M:%S'), ")")
                if wait_time < 10:
                    print("Average speed: [DISABLED WHEN UPDATES ARE UNDER 10s]")
                else:
                    print("Average speed: ", v,
                          "km/s")  # TODO COMPENSATION FOR HTTP REQUEST FOR THE AVERAGE SPEED IS REQUIRED
                try:
                    print("Current address: ", geo_name)
                except:
                    pass
                print("Timestamp (UTC): ", datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
                print("Run ID: ", self.id_to_use)
                print(" ")
                out = self.data(timestamp, v, position2.get("latitude"), position2.get("longitude"), self.id_to_use)
                self.d.enter_data(out)
            self.i = self.i + 1
            countdown = wait_time
            if wait_time > 2:
                while countdown > 0:
                    print("Next update:", countdown, " ", end="\r")
                    time.sleep(1)  # TODO SOMEHOW MAKE THE FORMATTING SMOOTHER
                    countdown = countdown - 1
        print("Shutting down...")

if __name__ == "__main__":
    VERSION = 2.3
    tracker = Tracker(VERSION)
    tracker.run()
