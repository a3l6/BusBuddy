import googlemaps
from datetime import datetime
import numpy
gmaps = googlemaps.Client(key='AIzaSyAjCIaky34JZGSKrAJ293MQ8e9NX6egqpg')

# Geocoding an address
latlong = []
with open(r"C:\Users\dolev\Desktop\Programs\School_Bus_Route_Optimization\Addresses.txt", "r", encoding="UTF-8") as file:
    for line in file.readlines():
        tempmeasure = gmaps.geocode(line)[0]["geometry"]["location"]
        latlong.append([tempmeasure["lat"], tempmeasure["lng"]])

averagedlll = [numpy.average([x[0] for x in latlong]), numpy.average([x[1] for x in latlong])]
nearestroadis = gmaps.nearest_roads(str(averagedlll[0])+","+str(averagedlll[1]))
print(nearestroadis)