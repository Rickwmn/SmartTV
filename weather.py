import requests
import json
# import socket


# public_ip_address = json.loads(requests.get("http://jsonip.com").text)["ip"]
# local_ip_address = socket.gethostbyname(socket.gethostname())
# hostname = socket.getfqdn()

with open("keys.txt", "r") as f:
    apikey = f.read().split("\n")[0]
# response = requests.get(
#     "https://api.openweathermap.org/data/2.5/weather?q=Novi%20Sad&units=metric&appid="+apikey).text

response = requests.get(
    "https://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=b6907d289e10d714a6e88b30761fae22").text
jsonweather = json.loads(response)
temp = jsonweather["main"]["temp"]
print(temp)
# print(public_ip_address, local_ip_address, hostname)
