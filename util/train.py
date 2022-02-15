from algorithm.classic_shortest_path_algorithm import classic_shortest_path
import numpy as np

from config.model_config import get_config
from util.evaluate import error_rate


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


def training_hier(model, alpha_list, sample_set):
    for sample in sample_set:
        s = sample['s']
        t = sample['t']
        shortest_path_value = sample['value'] / 10**get_config("norm_factor")

        vector_s = model.get_M_value_of_Leaf(s)
        vector_t = model.get_M_value_of_Leaf(t)

        # 下面这个算法没啥用，还是要单独计算导数的公式的
        approximate_shortest_path_value = np.linalg.norm(vector_s - vector_t, ord=1)
        # loss = (approximate_shortest_path_value - shortest_path_value) ** 2
        # error_rate_value = error_rate(approximate_shortest_path_value, shortest_path_value) * 100
        # TODO: 问题在于为什么一条边也收敛不了
        derivative_s = 2 * np.sign(vector_s - vector_t) * \
                       (approximate_shortest_path_value - shortest_path_value)


        derivative_t = -1 * derivative_s

        now_s_node = model.get_leaf_node(s)
        now_t_node = model.get_leaf_node(t)

        for i in range(model.num_inside_layer):
            now_level = model.num_inside_layer - i
            alpha = alpha_list[now_level]

            # now_s_node.value *= (1 - get_config("regular_factor"))
            # now_t_node.value *= (1 - get_config("regular_factor"))

            now_s_node.value -= alpha * derivative_s
            now_t_node.value -= alpha * derivative_t

            now_s_node = now_s_node.parent
            now_t_node = now_t_node.parent
            if now_s_node == now_t_node:
                break
