import Digraphs
import time
from geopy.geocoders import GoogleV3
import os

def get_routes() -> list[str]: 

    # calling the Nominatim tool and create Nominatim class
    loc = GoogleV3(api_key=os.getenv("GOOGLE_MAPS_KEY"))


    def get_geocode_obj(addr):
        try:
            time.sleep(1)
            geocode = loc.geocode(addr)
            return geocode.latitude, geocode.longitude
        except AttributeError:
            return
    x = Digraphs.main()

    lists = []

    for i in x:
        print(i)
        lists.append(list(map(lambda y: y.address.replace(" ", "+"),list(map(lambda x: loc.reverse(f"{x[0]}, {x[1]}"), i)))))


    urls = []
    for l in lists:
        url = "https://www.google.com/maps/dir/"
        for addr in l:
            url += addr + "/"
        urls.append(url)

    return urls
    