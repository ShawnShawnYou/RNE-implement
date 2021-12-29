
import random

from algorithm.classic_shortest_path_algorithm import classic_shortest_path
from config.model_config import get_config

"""
    return:
        sample_set = List<sample>
        sample["s"] = id of s
        sample["t"] = id of t
        sample["value"] = shortest path value from s to t
"""


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


def subgraph_level_samples(model, level):

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

        value = classic_shortest_path(s, t)
        sample = {
            "s": s,
            "t": t,
            "value": value
        }
        sample_set.append(sample)

    return sample_set


def landmark_based_samples(model):

    landmark_index_set = get_landmark_set(model)

    sample_set = []
    for i in range(get_config("sample_N")):
        landmark_index_chosen = random.choice(landmark_index_set)
        s = random.randint(0, model.data_size - 1)
        value = classic_shortest_path(s, landmark_index_chosen)
        sample = {
            "s": s,
            "t": landmark_index_chosen,
            "value": value
        }
        sample_set.append(sample)

    return sample_set



def error_based_samples(model):
    pass