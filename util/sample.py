
import random
import networkx as nx

from config.model_config import get_config

"""
    return:
        sample_set = List<sample>
        sample["s"] = id of s
        sample["t"] = id of t
        sample["value"] = shortest path value from s to t
"""


def get_road_graph():
    road_graph = nx.Graph()

    edges = []
    with open(get_config("edge_data_path"), "rb") as f:
        f.readline()

        while True:
            line = f.readline().split()
            if not line:
                break
            edges.append((int(line[0]), int(line[1]), float(line[2])))

    road_graph.add_weighted_edges_from(edges)

    return road_graph


def get_landmark_set(model):
    data_size = model.data_size

    landmark_index_list = []
    for i in range(get_config("landmark_rate") * data_size):
        landmark_index = random.randint(0, data_size - 1)
        landmark_index_list.append(landmark_index)

    landmark_index_set = list(set(landmark_index_list))

    return landmark_index_set


def get_all_child_list(model, level, g_index):
    all_child_list = []
    now_node = model.M_local[level][g_index]
    to_be_visit = [now_node]
    while len(to_be_visit) != 0:
        now_node = to_be_visit.pop()
        if now_node.level <= model.num_inside_layer - 1:
            to_be_visit.extend(now_node.child_list)
        else:
            all_child_list.append(now_node.node_id)

    return all_child_list


def simple_subgraph_level_samples(model, level, road_graph):
    sample_set = []

    for i in range(get_config("sample_N")):
        s = random.randint(0, model.data_size - 1)

        try:
            dijkstra_result_s = nx.single_source_dijkstra_path_length(road_graph, s)
        except Exception as e:
            continue
        candidate_t = list(dijkstra_result_s.keys())

        # Batch for nearest
        list_t = candidate_t[:get_config("sample_N_t")]

        # Batch for random
        for j in range(get_config("sample_N_t")):
            t = random.choice(candidate_t)
            list_t.append(t)

        for t in list_t:
            value = dijkstra_result_s[t]
            sample = {
                "s": s,
                "t": t,
                "value": value
            }
            sample_set.append(sample)

    return sample_set

def subgraph_level_samples(model, level, road_graph):

    subgraph_node_list = model.M_local[level]

    sample_set = []
    # TODO: 这里暴力可以处理成batch优化一下
    for k in range(get_config("sample_N")):
        g1_index = random.randint(0, len(subgraph_node_list) - 1)
        g2_index = random.randint(0, len(subgraph_node_list) - 1)

        if level != model.num_inside_layer:
            all_child_list_s = get_all_child_list(model, level, g1_index)
            all_child_list_t = get_all_child_list(model, level, g2_index)

            # TODO: 这里主要是因为出现了一些区域为空。。。至于为什么会这样，可能是因为划分区域太暴力了
            if len(all_child_list_s) == 0 and len(all_child_list_t) == 0:
                continue
            elif len(all_child_list_s) == 0:
                all_child_list_s = all_child_list_t
            else:
                all_child_list_t = all_child_list_s

            s = random.choice(all_child_list_s)
            t = random.choice(all_child_list_t)
        else:
            s = g1_index
            t = g2_index

        try:
            value = nx.dijkstra_path_length(road_graph, s, t)
        except Exception as e:
            continue
        sample = {
            "s": s,
            "t": t,
            "value": value
        }
        sample_set.append(sample)

    return sample_set


def landmark_based_samples(model, road_graph):

    landmark_index_set = get_landmark_set(model)

    sample_set = []
    for i in range(get_config("sample_N")):
        landmark_index_chosen = random.choice(landmark_index_set)
        s = random.randint(0, model.data_size - 1)
        try:
            value = nx.dijkstra_path_length(road_graph, s, landmark_index_chosen)
        except Exception as e:
            continue
        sample = {
            "s": s,
            "t": landmark_index_chosen,
            "value": value
        }
        sample_set.append(sample)

    return sample_set



def error_based_samples(model, road_graph):
    pass