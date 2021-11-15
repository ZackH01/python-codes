from tkinter import Tk, Canvas
from graph import Graph


def draw_nodes(graph):
    node_list = graph.nodes
    size = 50
    seperation = 200
    offset = 100
    
    #Create a circle to represent each node
    drawn_nodes = {}
    for i, node in enumerate(node_list):
        x = seperation*i +offset
        y = 100
        drawn_nodes[node] = canvas.create_oval(x, y, x+size, y+size, fill="blue")

    return drawn_nodes #Dictionary mapping node id's to canvas objects


def draw_edges(graph):
    edge_list = graph.edges

    #Draw a line from the centre of a node to another to represent and edge
    drawn_edges = []
    for i, edge in enumerate(edge_list):
        node_pos = canvas.coords(drawn_nodes.get(edge[0]))
        start_node_centre = [node_pos[0]+(node_pos[2]-node_pos[0])/2, node_pos[1]+(node_pos[3]-node_pos[1])/2]
        node_pos = canvas.coords(drawn_nodes.get(edge[1]))
        end_node_centre = [node_pos[0]+(node_pos[2]-node_pos[0])/2, node_pos[1]+(node_pos[3]-node_pos[1])/2]

        drawn_edges.append(canvas.create_line(start_node_centre[0], start_node_centre[1], end_node_centre[0], end_node_centre[1]))

    return draw_edges


if __name__ == "__main__":
    #Create window
    window = Tk()
    window.title("Graph")
    window.geometry("500x500")
    canvas = Canvas(window, height=500, width=500)
    canvas.pack()

    #Create test graph
    my_graph = Graph()
    my_graph.add_node()
    my_graph.add_node()
    my_graph.add_edge(0, 1)

    #Draw graph
    drawn_nodes = draw_nodes(my_graph)
    draw_edges(my_graph)
    
    window.mainloop()


