import unittest
class Node(object):
    """Represents a node in the graph"""
    def __init__(self, name):
        self.name = str(name)
    def get_name(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        # This function is necessary so that Nodes can be used as
        # keys in a dictionary, even though Nodes are mutable
        return self.name.__hash__()
    def tupleit(self):
        return (self.name.split(',')[0], self.name.split(',')[1])

class Edge(object):
    """Represents an edge in the dictionary. Includes a source and
    a destination."""
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def get_source(self):
        return self.src

    def get_destination(self):
        return self.dest

    def __str__(self):
        return '{}->{}'.format(self.src, self.dest)


class WeightedEdge(Edge):
    def __init__(self, src, dest, houses, total_time):
        self.src, self.dest = src, dest
        self.houses, self.total_time = houses, total_time
    def get_houses(self):
        return self.houses

    def get_total_time(self):
        return self.total_time

    def __str__(self):
        return '{}->{} ({}, {})'.format(self.src, self.dest, self.houses, self.total_time)
        

class Digraph(object):
    """Represents a directed graph of Node and Edge objects"""
    def __init__(self, start, end):
        self.nodes = set([])
        self.edges = {}  # must be a dict of Node -> list of edges
        self.start= start
        self.end = end
    def __str__(self):
        edge_strs = []
        for edges in self.edges.values():
            for edge in edges:
                edge_strs.append(str(edge))
        edge_strs = sorted(edge_strs)  # sort alphabetically
        return '\n'.join(edge_strs)  # concat edge_strs with "\n"s between them
    def get_edges_for_node(self, node):
        return self.edges[node]

    def has_node(self, node):
        return node in self.nodes

    def add_node(self, node):
        """Adds a Node object to the Digraph. Raises a ValueError if it is
        already in the graph."""
        if node not in self.nodes:
            self.nodes.add(node)
            self.edges[node] = []
        else:
            raise ValueError
    def get_end(self):
        return self.end

    def add_edge(self, edge):
        """Adds an Edge or WeightedEdge instance to the Digraph. Raises a
        ValueError if either of the nodes associated with the edge is not
        in the  graph."""
        if edge.get_source() not in self.nodes or edge.get_destination() not in self.nodes:
            raise ValueError
        else:
            self.edges[edge.get_source()].append(edge)

    def get_start(self):
        return self.start
