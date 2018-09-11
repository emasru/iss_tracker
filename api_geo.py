from datetime import datetime
import time
import os
from databasemanager import Database as Db
from collections import namedtuple
import update as f



VERSION = 2.1
print("ISS Tracker // Author: Henning S. & Birk N.")
print("Version:", VERSION)
print("Starting up...")

global first_position_timestamp
data = namedtuple("data", "time velocity long lat identifier")
d = Db("recorded_positions")
id_to_use = d.largest_identifier() + 1
i = 0

while True:
    if i == 0:  # Init: Tracks the global first position and sets the wait_time
        wait_time = int(input("Seconds between position updates? (MUST BE MORE THAN 1): "))
        if wait_time < 1:
            wait_time = 1
        print("Tracking first position...")
        contents = f.pos_update()
        if contents == 1:
            break
        position1 = contents.get("iss_position")
        try:
            geo_name = f.location_query(position1)
        except:
            pass
        hemisphere = f.hemisphere_check(position1)
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
    if i > 0:  # Tracks the second position every wait_time seconds and calculates the average speed constanly based
        #        on the first position
        contents = f.pos_update()  # Updates position
        if contents == 1:  # If the function returns a 1 it means it has encountered an HTTP exception,
            break  # and kills the program
        timestamp = int(contents.get("timestamp"))
        position2 = contents.get("iss_position")
        try:
            geo_name = f.location_query(position2)  # Fetches the current address
        except:
            pass
        hemisphere = f.hemisphere_check(position2)
        distance_measure = f.distance(position1, position2)
        v = distance_measure / (wait_time * i)
        distance_measure = round(distance_measure, 2)
        v += 0.35
        v = round(v, 2)
        if wait_time < 10:
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
        print("Run ID: ", id_to_use)
        print(" ")
        out = data(timestamp, v, position2.get("latitude"), position2.get("longitude"), id_to_use)
        d.enter_data(out)
    i = i + 1
    countdown = wait_time
    if wait_time > 2:
        while countdown > 0:
            print("Next update:", countdown, " ", end="\r")
            time.sleep(1)  # TODO SOMEHOW MAKE THE FORMATTING SMOOTHER
            countdown = countdown - 1
print("Shutting down...")

