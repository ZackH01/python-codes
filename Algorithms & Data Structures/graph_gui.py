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

    
    @staticmethod
    def find_node_pos(graph):
        #Returns a list of relative positions of each node's centre
        nodes = graph.nodes
        edges = graph.edges
        node_pos = [] #List of [node_id, x_pos, y_pos]

        #Find node with most edges
        node_edge_count = GraphCanvas.count_node_edges(graph)
        node_edge_count = sorted(node_edge_count, key=lambda l: l[1], reverse=True)
        node_order = [node_edge_count[0][0]] #Start at the node with the most edges
        next_pointer = 0

        placed_nodes = []
        while next_pointer < len(node_order):
            #Move to start/next node
            for pair in node_edge_count:
                if pair[0] == node_order[next_pointer]:
                    curr_node = pair
                    break
            dist_from_curr = -int(curr_node[1] / 4) - 1

            #Initialise start position
            if next_pointer == 0:
                curr_node_pos = (0, 0) #Starting position
                x = 0
                y = dist_from_curr
                prev_node = None
                #Place starting node
                node_pos.append([curr_node[0], 0, 0])
                placed_nodes.append(curr_node[0])

            #Find position of last node
            else:
                for node in node_pos:
                    if node[0] == prev_node:
                        x = node[1]
                        y = node[1] + dist_from_curr
                        break

            #Find nodes that connect to current node
            connected_nodes = []
            for edge in edges:
                if edge[0] == curr_node[0] and edge[1] not in connected_nodes:
                    connected_nodes.append(edge[1])

            #Place each node connected to current node in a clockwise pattern
            for i, node in enumerate(connected_nodes):
                if node not in placed_nodes:
                    #//////////////////////////////
                    #
                    #Validate placement here
                    #
                    #//////////////////////////////

                    node_pos.append([node, x, y])
                    node_order.append(node)
                    placed_nodes.append(node)

                    #Find next x and y
                    if i <= dist_from_curr or i > dist_from_curr*3:
                        x += 1
                    else:
                        x -= 1
                    x += curr_node_pos[0]

                    if i > 2 * dist_from_curr:
                        y += 1
                    else:
                        y -= 1
                    y += curr_node_pos[1]

            next_pointer += 1
            prev_node = curr_node[0]

        print(node_pos)
        return node_pos


    def draw_graph(self):
        node_positions = GraphCanvas.find_node_pos(self.graph)
        edges = self.graph.edges

        #Variables that affect the appearence of the image
        size = 25 #Radius of each node
        x_offset = 100
        y_offset = 150
        spacing = 100
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


if __name__ == "__main__":
    main()
