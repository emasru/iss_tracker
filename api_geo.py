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


class Position:
    def __init__(self):
        self.url_data = None

    async def get(self):
        async with aiohttp.ClientSession() as request:
            async with request.get("http://api.open-notify.org/iss-now.json") as data:
                self.url_data = json.load(data)


if __name__ == "__main__":
    position = Position()
    position.get()
