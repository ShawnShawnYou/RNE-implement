import math
import random

import networkx as nx

from config.model_config import get_config


def test():
    road_graph = nx.Graph()

    edges = []
    with open("./dataset/chengdu/chengdu.edge", "rb") as f:
        f.readline()
        num_node = 214440

        while True:
            line = f.readline().split()
            if not line:
                break
            edges.append((int(line[0]), int(line[1]), float(line[2])))

    road_graph.add_weighted_edges_from(edges)

    for i in range(1):
        s = random.randint(0, num_node - 1)
        t = random.randint(0, num_node - 1)
        shortest_path_value = nx.dijkstra_path_length(road_graph, s, t)
        path = nx.dijkstra_path(road_graph, s, t)
        length, path1 = nx.single_source_dijkstra(road_graph, 0)
        print(path, shortest_path_value)

test()
