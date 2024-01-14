import googlemaps
from datetime import datetime
import numpy
from sklearn import cluster
import matplotlib.pyplot as plt
import tqdm
import random



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
        cluster_coor = {}
        for clusterY in set(self.clusters):
                cluster_coor[clusterY] = []
        for count, x in enumerate(self.clusters):
            coor_cluster.update({tuple(self.latlong[count]): x})
            cluster_coor[x].append(tuple(self.latlong[count]))
        self.stopcoords = []
        self.bustops = {}
        for clus in cluster_coor.values():
            templist = [clus[x][0] for x in range(len(clus))]
            templist2 = [clus[x][1] for x in range(len(clus))]
            try:
                road = gmaps.nearest_roads(str(numpy.average(templist))+","+str(numpy.average(templist2)))[0]["location"]
            except:
                road = gmaps.nearest_roads(str(numpy.average(templist)+1)+","+str(numpy.average(templist2)+1))[0]["location"]
            self.stopcoords.append(road)
            self.bustops[str(road["latitude"])+','+str(road["longitude"])] = len(clus)
    def get_stops(self):
        return self.bustops
def run():
    hi = Adress_clusters()
    hi.clustering()
    hi.find_stop()
    return hi
