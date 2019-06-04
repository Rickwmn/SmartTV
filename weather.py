import requests
import json
import socket


def getHostname(): return socket.getfqdn()


def getLocalIP(): return socket.gethostbyname(socket.gethostname())


class Location:
    def __init__(self):
        self.location_info = json.loads(
            requests.get("http://ip-api.com/json/").text)

    @property
    def publicIP(self):
        return self.location_info["query"]

    @property
    def timeZone(self):
        return self.location_info["timezone"]

    @property
    def country(self):
        return self.location_info["country"]

    @property
    def countryCode(self):
        return self.location_info["CountryCode"]

    @property
    def region(self):
        return self.location_info["regionName"]


class Weather:
    def __init__(self):
        with open("keys.txt", "r") as f:
            self.apikey = f.read().split("\n")[0]

        # self.response = requests.get(
        #     "https://api.openweathermap.org/data/2.5/weather?q=Novi%20Sad&units=metric&appid="+apikey).text

        self.response = requests.get(
            "https://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=b6907d289e10d714a6e88b30761fae22").text

        self.response = json.loads(response)

    @property
    def temperature(self):
        return self.response["main"]["temp"]
