import json
import folium

from geopy import distance
from flask import Flask
from yandex_geocoder import Client

with open("data-2897-2019-01-22.json", "r", encoding="cp1251") as my_file:
  bars_data = json.load(my_file)

bars = []

coordinates = list(Client.coordinates(input("Где вы сейчас находитесь?: ")))
coordinates.reverse()
map_view = folium.Map(
  location=coordinates,
  zoom_start=13
)

for bar in bars_data:
  bar = {
    'Title': bar['Name'],
    'longtitude': bar['geoData']['coordinates'][0],
    'latitude': bar['geoData']['coordinates'][1]
  }
  bar['distance'] = distance.distance(coordinates, [
            bar['latitude'],
            bar['longtitude']]).km
  bars.append(bar)

def get_distance_to_bar(bar):
  return bar['distance']

bars = sorted(bars, key=get_distance_to_bar)

for bar in bars[:5]:
  folium.Marker([bar['latitude'], bar['longtitude']], popup=bar['Title'], tooltip="Кликай").add_to(map_view)

map_view.save('index.html')

def main():
  with open('index.html') as file:
    return file.read()

app = Flask(__name__)
app.add_url_rule('/', 'Ближайшие бары', main)
app.run('0.0.0.0')