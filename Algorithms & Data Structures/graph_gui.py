from tkinter import Tk, Canvas
from graph import Graph


class MainWindow:
    def __init__(self, width, height, title):
        self.window = Tk()
        self.window.geometry(str(width)+"x"+str(height))
        self.window.title(str(title))

    def display(self):
        self.window.mainloop()


class GraphCanvas:
    def __init__(self, window, graph):
        self.canvas = Canvas(window, width=500, height=500)
        self.graph = graph


    #Completely revamp drawing
    """
    @staticmethod
    def count_node_edges(graph):
        #Returns a list of the nodes with their corresponding edges
        edges = graph.edges
        edge_count = [] #List of pairs [node, edge count]

        for i, node in enumerate(graph.nodes):
            edge_count.append([node, 0]) #[node_id, edge_count]
            for edge in edges:
                if edge[0] == node:
                    edge_count[i][1] += 1
        
        return edge_count
    """
    
    @staticmethod
    def find_node_pos(graph):
        #Returns a list of relative positions of each node's centre
        nodes = graph.nodes
        #edges = graph.edges
        node_pos = [] #List of [node_id, x_pos, y_pos]

        #Put nodes in a list
        for i, node in enumerate(nodes):
            node_pos.append([node, i, 0])

        return node_pos


    def draw_graph(self):
        node_positions = self.find_node_pos(self.graph)
        edges = self.graph.edges

        #Variables that affect the appearence of the image
        size = 25 #Radius of each node
        x_offset = 100
        y_offset = 150
        spacing = 150
        colour = "blue"
        thickness = 5

        #Draw edges
        for edge in edges:
            #Find start and end points for the edge
            for node in node_positions:
                if edge[0] == node[0]:
                    start_node = node
                if edge[1] == node[0]:
                    end_node = node

            x1 = start_node[1]*spacing+x_offset
            y1 = start_node[2]*spacing+y_offset
            x2 = end_node[1]*spacing+x_offset
            y2 = end_node[2]*spacing+y_offset
            self.canvas.create_line(x1, y1, x2, y2, width=thickness)

        #Draw nodes
        for node in node_positions:
            x1 = node[1]*spacing-size+x_offset
            y1 = node[2]*spacing-size+y_offset
            x2 = node[1]*spacing+size+x_offset
            y2 = node[2]*spacing+size+y_offset
            self.canvas.create_oval(x1, y1, x2, y2, fill=colour)

        self.canvas.pack()


def main():
    #Create window
    main_window = MainWindow(500, 500, "Graph")

    #Create test graph
    my_graph = Graph()
    my_graph.add_node()
    my_graph.add_node()
    my_graph.add_node()
    my_graph.add_edge(1, 0)
    my_graph.add_edge(1, 2)

    #Draw graph
    graph_image = GraphCanvas(main_window.window, my_graph)
    graph_image.draw_graph()

    main_window.display()


if __name__ == "__main__": main()
