from datetime import datetime
import time
import os
from databasemanager import Database as Db
from collections import namedtuple
import urllib.request as url
import json
import math
from geopy.geocoders import Nominatim
import asyncio
from position import Position

VERSION = "1.0, REWRITE"


class Tracker:
    def __init__(self):
        self.version = VERSION
        self.data = namedtuple("data", "time velocity long lat identifier")
        self.database = Db("recorded positions")
        self.database_entry = None
        self.utc = False
        self.wait_time = 1
        self.velocity = 0

    def database(self, position):
        self.database_entry = self.data(position.timestamp, self.velocity, position.longitude, position.latitude, None)
        # TODO

    def run(self):
        print("ISS Tracker // Author: Henning S. & Birk N.")
        print("Version:", self.version)
        print("Starting up...")
        pos1 = Position()

        i = 0
        while True:
            if i == 0:
                self.wait_time = int(input("Seconds between position updates? (MUST BE MORE THAN 1): "))
                if self.wait_time < 1:
                    self.wait_time = 1
                utc_check = input("Do you want time displayed in UTC or local time? (Y/n): ")
                if utc_check == "y":
                    self.utc = True
                print("Tracking first position...")
                while True:
                    start_time = time.time().__float__()
                    pos1.get_pos(utc=self.utc)
                    if pos1.request_failed is True:
                        print("...HTTP request failed...")
                        break
                    pos1.get_hemisphere()
                    pos1.location_query()
                    os.system("cls")
                    print("The current position of the the ISS is Lat:", pos1.latitude, "and Lon:", pos1.longitude, "//", pos1.hemisphere)
                    print("Current address:", pos1.location)  # TODO TypeError: __str__ returned non-string (type NoneType) [search up object documentation]
                    print("Timestamp: ", pos1.date)
                    stop_time = time.time().__float__()
                    elapsed = stop_time - start_time
                    print("Completion time:", elapsed, "seconds")
                    time.sleep(self.wait_time)


if __name__ == "__main__":
    app = Tracker()
    app.run()
