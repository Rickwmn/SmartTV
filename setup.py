import sqlite3
import weather

conn = sqlite3.connect("./data.db")
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS Data (id INTEGER PRIMARY KEY AUTOINCREMENT,username char(64),email char(256),age INTEGER, measure char(8),country char(64),region char(64),timezone char(32), icon char(512));")

measure = input("Mectric or Imperial?[m/i]:")
if measure == "m":
    measure = "metric"
elif measure == "i":
    measure = "imperial"
else:
    print("Wrong Input!")


username = input("Username:")
email = input("E-Mail:")
age = int(input("Age:"))
icon = input("Username icon (Paste URL):")
location = weather.Location()

timezone = location.timeZone
country = location.country
region = location.region


cursor.execute(
    "INSERT INTO DATA (username,email,age,measure,country,region,timezone,icon) VALUES (?,?,?,?,?,?,?,?);", (username, email, age, measure, country, region, timezone, icon))


conn.commit()
conn.close()
