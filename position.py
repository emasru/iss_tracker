from datetime import datetime
import time
import os
from databasemanager import Database as Db
from collections import namedtuple
import urllib.request as url
import json
import math
from geopy.geocoders import Nominatim
import aiohttp
import asyncio

INSTANCE = "01"

class Position:
    def __init__(self):
        self.url_data = None
        self.location = "None (International waters)"
        self.hemisphere = "Unknown"

    async def get_status(self):
        async with aiohttp.ClientSession() as request:
            async with request.get("http://api.open-notify.org/iss-now.json") as data:
                self.url_data = json.load(data)  # TODO: find correct way to parse json in aiohttp

    async def data_check(self):
        if self.url_data is None:
            await self.get_status()  # TODO: correct use of await?

    async def location_query(self):
        self.data_check()
        latitude = self.url_data.get("latitude")
        longitude = self.url_data.get("longitude")

        query = latitude + "," + longitude
        address = Nominatim(user_agent=("iss_checker_unit_%s" % INSTANCE))  # https://bit.ly/2RLDLOA
        self.location = await address.reverse(query)

    def hemisphere(self):
        self.data_check()
        lat = float(self.url_data.get("latitude"))
        lon = float(self.url_data.get("longitude"))

        if lat >= 0:
            lat = "NORTH"
        else:
            lat = "SOUTH"
        if lon >= 0:
            lon = "EAST"
        else:
            lon = "WEST"

        self.hemisphere = lat + " " + lon + " " + "HEMISPHERE"  # TODO: can attributes be declared outside __init__?


if __name__ == "__main__":
    position = Position()
    position.location_query()
    print(position.location)

    # TODO: need to create event loop to use methods
