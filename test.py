"""list1 = [
    "119 Osler Dr, Dundas, ON L9H 6X4",
    "101 Osler Drive 108 A, ON L9H 4H4",
    "7 Don St, Dundas, ON L9H 4N8",
    "23 Dunning Ct, Dundas, ON L9H 4K8",
    "5 South Street E, Dundas, ON L9H 4K5",
    "41 South St W, Dundas, ON L9H 4C4",
    "94 Main St Unit 86, Dundas, ON L9H 2H1",
    "86 Main St, Dundas, ON L9H 2P9",
    "50 Hatt St, Dundas, ON L9H 0A1",
    "77 Governors Rd, Dundas, ON L9H 7N8"
]"""


list1 = [(43.2571822, -79.9411556), (43.2589868, -79.9433597), (43.2598176, -79.9409117), (43.2618995, -79.9409773), (43.2608843, -79.9442996), (43.2598637, -79.9490423), (43.262663, -79.95209729999999), (43.262674, -79.95266819999999), (43.2644808, -79.9550336), (43.2630413, -79.95621059999999)]

"""list2 = [
    "50 Governors Road, Dundas, ON L9H 5M3",
    "56 Governors Rd, Dundas, ON L9H 5G7",
    "205B Governors Rd, Dundas, ON L9H 3J7",
    "14 Kemp Dr, Dundas, ON L9H 2M9",
    "14 Central Park Ave, Dundas, ON L9H 2M6",
    "297 Mill St, Dundas, ON L9H 2L8",
    "366 Mill St, Dundas, ON L9H 2M1",
    "424 MacNab St, Dundas, ON L9H 2L3",
    "1 Head St unit 5E, Dundas, ON L9H 3H5",
    "343 King St W, Dundas, ON L9H 1W8"
]"""

list2 = [(43.2620507, -79.9564292), (43.2617504, -79.9576976), (43.26186, -79.96374999999999), (43.262559, -79.9652071), (43.2635961, -79.96270090000002), (43.2669998, -79.9694748), (43.267094, -79.97187129999999), (43.26900089999999, -79.975833), (43.2710415, -79.97354539999999), (43.2712603, -79.9698353)]
"""list3 = [
    "11 Woodlawn Ct, Hamilton, ON L9H 7S2",
    "15 Romar Dr, Dundas, ON L9H 5E2",
    "7 Westoby Ct, Dundas, ON L9H 7P9",
    "15 Parkway Pl, Dundas, ON L9H 6K3",
    "548 Old Dundas Rd, Ancaster, ON L9G 3J4"
]"""

list3 = [(43.2719998, -79.9583304), (43.2795749, -79.9466317), (43.2804636, -79.9369117), (43.27974649999999, -79.93472589999999), (43.2339176, -79.9738666)]

# importing geopy library and Nominatim class
from geopy.geocoders import Nominatim, GoogleV3
import time
from dotenv import load_dotenv
import os

load_dotenv()

# calling the Nominatim tool and create Nominatim class
loc = GoogleV3(api_key=os.getenv("GOOGLE_MAPS_KEY"))


def get_geocode_obj(addr):
    try:
        time.sleep(1)
        geocode = loc.geocode(addr)
        return geocode.latitude, geocode.longitude
    except AttributeError:
        return
"""# entering the location name
getLoc = loc.geocode("50 Governors Road, Dundas, ON L9H 5M3")

# printing address
print(getLoc.address)

# printing latitude and longitude
print("Latitude = ", getLoc.latitude, "\n")
print("Longitude = ", getLoc.longitude)"""

"""list4 = list(map(get_geocode_obj, list1))
print(list4)"""




list4 = list(map(lambda y: y.address.replace(" ", "+"),list(map(lambda x: loc.reverse(f"{x[0]}, {x[1]}"), list1))))
list5 = list(map(lambda y: y.address.replace(" ", "+"),list(map(lambda x: loc.reverse(f"{x[0]}, {x[1]}"), list2))))
list6 = list(map(lambda y: y.address.replace(" ", "+"),list(map(lambda x: loc.reverse(f"{x[0]}, {x[1]}"), list3))))


x = list4, list5, list6

urls = []
for l in x:
    url = "https://www.google.com/maps/dir/"
    for addr in l:
        url += addr + "/"
    urls.append(url)
    

print(urls)

"""print(list4)
for addr in list1:
    long = addr[0]
    lat = addr[1]
    print(loc.reverse(f"{long}, {lat}"))"""

"""print(f"{list1=}")
print(list4)"""

"""urls = []

for l in x:
    url = "https://www.google.com/maps/dir/"
    for address in l:
        temp = address.replace(" ", "+") + "/"
        url += temp
    urls.append(url)

print(urls)"""