import googlemaps
from datetime import datetime
import numpy
from sklearn import cluster
import matplotlib.pyplot as plt
import tqdm
import random
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import GoogleV3

gmapsclient2 = GoogleV3(api_key='AIzaSyAjCIaky34JZGSKrAJ293MQ8e9NX6egqpg')
gmaps = googlemaps.Client(key='AIzaSyAjCIaky34JZGSKrAJ293MQ8e9NX6egqpg')

def get_coords_from_adress(adress: str):
    tempmeasure = gmaps.geocode(adress)[0]["geometry"]["location"]
    return (tempmeasure["lat"], tempmeasure["lng"])
class Adress_clusters():
    def __init__(self, address_array:list = []):
        self.latlong = []
        self.referbackdic = {}
        
        with open(r"./Addresses.txt", "r", encoding="UTF-8-sig") as file:
            self.latlong = []
            for line in file.readlines():
                tempmeasure = gmaps.geocode(line)[0]["geometry"]["location"]
                self.latlong.append([tempmeasure["lat"], tempmeasure["lng"]])


    def clustering(self):
        self.clustermodel = cluster.AffinityPropagation().fit(self.latlong)
        #plt.figure(figsize =(20, 20))
        self.clusters = self.clustermodel.fit_predict(self.latlong)
        #plt.scatter([x[0] for x in self.latlong], [x[0] for x in self.latlong],
                    #c = self.clustermodel.fit_predict(self.latlong), cmap = "turbo")
        #plt.show()
        
    def find_stop(self):
        coor_cluster = {}
        self.cluster_coor = {}
        for clusterY in set(self.clusters):
                self.cluster_coor[clusterY] = []
        for count, x in enumerate(self.clusters):
            coor_cluster.update({tuple(self.latlong[count]): x})
            self.cluster_coor[x].append(tuple(self.latlong[count]))
        self.stopcoords = []
        self.bustops = {}
        for clus in self.cluster_coor.values():
            templist = [clus[x][0] for x in range(len(clus))]
            templist2 = [clus[x][1] for x in range(len(clus))]
            try:
                road = gmaps.nearest_roads(str(numpy.average(templist))+","+str(numpy.average(templist2)))[0]["location"]
            except:
                rev = gmapsclient2.reverse(str(numpy.average(templist))+","+str(numpy.average(templist2)))[0]
                print(rev)
                road = gmaps.geocode(rev)[0]["geometry"]["location"]
                road = {"latitude": road["lat"], "longitude": road["lng"]}
            self.stopcoords.append(road)
            self.bustops[str(road["latitude"])+','+str(road["longitude"])] = len(clus)
    def get_stops(self):
        return self.bustops
def run():
    hi = Adress_clusters()
    hi.clustering()
    hi.find_stop()
    return hi
