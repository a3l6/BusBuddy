from graph2  import Digraph, Node, WeightedEdge
import copy
import numpy
from Create_Clusters import get_coords_from_adress
import Create_Clusters

def main():
    def coord_distance(one, two):
        one = one.split(",")
        two = two.split(",")
        return numpy.arccos(numpy.sin(float(one[0]))*numpy.sin(float(two[0]))+numpy.cos(float(one[0]))*numpy.cos(float(two[0]))*numpy.cos(float(two[1])-float(one[1])))*6371
    def get_others(stops, badstop):
        stops.pop(badstop)
        return stops


    def load_map(address_dictionary):
        Mit_Digraph = Digraph(get_coords_from_adress("899 Nebo Rd, Hannon, ON L0R 1P0"), get_coords_from_adress("700 Main St W, Hamilton, ON L8S 1A5"))

        keylist = address_dictionary.keys()
        for count, cluster in enumerate(address_dictionary.keys()):
            new_node_1 = Node(cluster)
            Mit_Digraph.add_node(new_node_1)
        for count, cluster in enumerate(address_dictionary.keys()):
            new_node_1 = Node(cluster)
            new_edges = [WeightedEdge(new_node_1, Node(x), int(address_dictionary[x]), float(coord_distance(cluster, x))/40) for x in get_others(list(keylist), count)]
            for new_edge in new_edges:
                Mit_Digraph.add_edge(new_edge)
        
        newnode2 = Mit_Digraph.get_start()
        newnode2 = Node(str(newnode2[0])+','+str(newnode2[1]))
        Mit_Digraph.add_node(newnode2)
        new_edges = [WeightedEdge(newnode2, Node(x), int(address_dictionary[x]), float(coord_distance(newnode2.get_name(), x))/40) for x in keylist]
        for new_edge in new_edges:
                Mit_Digraph.add_edge(new_edge)

        newnode3 = Mit_Digraph.get_end()
        Mit_Digraph.add_node(Node(str(newnode3[0])+','+str(newnode3[1])))
        newnode3 = Node(str(newnode3[0])+','+str(newnode3[1]))
        new_edges = [WeightedEdge(newnode3, Node(x), 3000, float(coord_distance(newnode3.get_name(), x))/40) for x in keylist]
        new_edges.extend([WeightedEdge(Node(x), newnode3, int(address_dictionary[x]), float(coord_distance(x, newnode3.get_name()))/40) for x in get_others(list(keylist), count)])
        
        for new_edge in new_edges:
                Mit_Digraph.add_edge(new_edge)
        return Mit_Digraph

    def get_best_path(digraph, start, end, max_time,number_of_stations, number_of_busses, path = [[]], best_HTN = None,
                    best_path = None):
        if path == [[]]:
            path.append(0) #HOUSES/TIME/NODES MAXIMIZE
            path.append(0) #NO LESS THAN NODES THAN NUMBEROFNODES/NUMBEROFBUSSES + 1
            path.append(0) #NO MORE TIME THAN 1 HOUR
        path[0].append(start)
        if start == end:
            return path
        for edges in digraph.get_edges_for_node(start):
            if edges.get_destination() not in path[0]:
                if path[3] + edges.get_total_time() <= max_time:
                    temp_path = copy.deepcopy(path)
                    try:
                        temp_path[1] += edges.get_houses()/edges.get_total_time()/len(path)
                    except:
                        temp_path[1] += edges.get_houses()/1/len(path)
                    temp_path[2] += 1
                    temp_path[3] += edges.get_total_time()
                    if best_HTN == None or temp_path[1]>best_HTN and temp_path[2] in (number_of_stations/number_of_busses-1,  number_of_stations/number_of_busses,  number_of_stations/number_of_busses+1):
                        new_path = get_best_path(digraph, edges.get_destination(), end, max_time, number_of_stations, number_of_busses, temp_path, best_HTN, best_path)
                        if new_path != None:
                            best_path = copy.deepcopy(new_path)
                            best_HTN = new_path[1]

        return best_path

    Clusters_object = Create_Clusters.run()
    busstopppps = Clusters_object.bustops
    lol = load_map(Clusters_object.bustops)
    newnode2 = lol.get_start()
    newmode3 = lol.get_end()
    busnum = 5
    THELAWRDLYROUTES = []
    for bus in range(busnum):
        hi = get_best_path(lol, Node(str(newnode2[0])+','+str(newnode2[1])), Node(str(newmode3[0])+','+str(newmode3[1])), 40, number_of_busses= busnum-bus, number_of_stations=len(busstopppps.keys())+2)
        THELAWRDLYROUTES.append([x.tupleit() for x in hi[0]])
        for thing in hi[0]:
            if thing.get_name() in busstopppps:
                busstopppps.pop(thing.get_name())


    return THELAWRDLYROUTES
        