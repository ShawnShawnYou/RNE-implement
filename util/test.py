# -*- coding: utf-8 -*-

import networkx as nx
import pylab
import numpy as np

from config.model_config import get_config

def test():
    edge = [(0, 1, 2), (0, 2, 1), (0, 3, 8), (1, 4, 1),
            (2, 5, 3), (3, 6, 5), (3, 5, 2), (5, 6, 1), (6, 7, 1)]

    G = nx.Graph()
    G.add_weighted_edges_from(edge)

    pos = nx.shell_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='white', edge_color='red', node_size=400, alpha=0.5)
    pylab.show()

    result = nx.floyd_warshall(G)


def test1():
    road_graph = nx.Graph()

    edges = []
    with open(get_config("edge_data_path"), "rb") as f:
        num_node = int(f.readline())

        # while True:
        for i in range(10000):
            line = f.readline().split()
            if not line:
                break
            edges.append((int(line[0]), int(line[1]), float(line[2])))

    road_graph.add_weighted_edges_from(edges)
    result = nx.floyd_warshall(road_graph)
    print(result)


    dir_path = get_config("shortest_data_dir")
    for key in result.keys():
        shortest_path = dir_path + str(key) + ".txt"
        with open(shortest_path, 'w') as f:
            f.write(str(dict(result[key])))

test1()