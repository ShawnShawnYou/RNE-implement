from model.hierarchical_embeded_model import Model
from config.model_config import get_config
import math

from util.save_load import *


def in_which_grid(x, y,
                  max_x, min_x, max_y, min_y):
    """
    grid:
            ----x-----
        |   0  1  2  3
        y   4  5  6  7
        |   8  9  10 11
        |   12 13 14 15
    """
    k = get_config("k")
    size = int(math.sqrt(k))

    x_grid_size = (max_x - min_x) / size
    y_grid_size = (max_y - min_y) / size

    x_index = int((x - min_x) / x_grid_size)
    y_index = int((y - min_y) / y_grid_size)

    if x_index == size:
        x_index -= 1
    if y_index == size:
        y_index -= 1

    return size * y_index + x_index


def get_range_of_data():
    max_x, min_x, max_y, min_y = 0, 0, 0, 0
    with open(get_config("node_data_path"), 'rb') as node_f:
        num_node = int(node_f.readline())

        node = node_f.readline().split()
        x, y = float(node[0]), float(node[1])
        max_x, min_x, max_y, min_y = x, x, y, y

        while True:
            node = node_f.readline().split()
            if not node:
                break
            x, y = float(node[0]), float(node[1])
            max_x = x if max_x < x else max_x
            max_y = y if max_y < y else max_y

            min_x = x if x < min_x else min_x
            min_y = y if y < min_y else min_y

    return max_x, min_x, max_y, min_y


def read_cluster(model):
    all_cluster = []
    cluster_16 = []
    with open(get_config("cluster_all_path"), "rb") as f:
        for i in range(model.data_size):
            value = int(f.readline())
            all_cluster.append(value)

    with open(get_config("cluster_16_path"), "rb") as f:
        for i in range(16):
            value = int(f.readline())
            cluster_16.append(value)

    index_cluster = [0 for i in range(16)]
    for i in range(16):
        index_cluster[cluster_16[i]] = i

    return all_cluster, index_cluster


def model_build():
    model = Model()

    # pseudo_k_way_partition
    # max_x, min_x, max_y, min_y = get_range_of_data()

    with open(get_config("node_data_path"), 'rb') as node_f:
        num_node = int(node_f.readline())
        model.set_leaf_node_space(num_node)
        all_cluster, index_cluster = read_cluster(model)

        i = 0
        while True:
            node = node_f.readline().split()

            if not node:
                break
            # x, y = float(node[0]), float(node[1])
            # model.gps_positions[i] = (x, y)
            # index_node = in_which_grid(x, y, max_x, min_x, max_y, min_y)

            cluster = all_cluster[i]
            index_node = index_cluster[cluster]

            child = model.M_local[model.num_inside_layer - 1][index_node].insert_child(i)
            model.M_local[model.num_inside_layer][i] = child
            i += 1

    # csv_model_load(model)

    return model


if __name__ == "__main__":
    model = model_build()
