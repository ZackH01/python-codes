"""
Graph data structure
"""

class Graph:
    def __init__(self):
        #Attributes
        self.nodes = []
        self.edges = []
        self.next_node_id = 0


    def add_node(self, node_id=None):
        #Adds a node with the given id, leave blank for auto generated ids
        if node_id == None:
            node_id = self.next_node_id

        if node_id not in self.nodes:
            self.nodes.append(node_id)

            while self.next_node_id in self.nodes:
                self.next_node_id += 1


    def add_edge(self, start_node, end_node, weight=0):
        #Adds an edge between two given nodes with a given weight
        if start_node in self.nodes and end_node in self.nodes:
            edge = [start_node, end_node, weight]

            if edge not in self.edges:
                self.edges.append(edge)
                self.edges.append([edge[1], edge[0], weight])


    def add_directed_edge(self, start_node, end_node, weight=0):
        #Adds a directed edge from one node to another with a given weight
        if start_node in self.nodes and end_node in self.nodes:
            edge = [start_node, end_node, weight]
            
            if edge not in self.edges:
                self.edges.append(edge)

