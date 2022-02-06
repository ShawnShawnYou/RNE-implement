from algorithm.classic_shortest_path_algorithm import classic_shortest_path
import numpy as np

from config.model_config import get_config


def training_hier(model, alpha_list, sample_set):
    for sample in sample_set:
        s = sample['s']
        t = sample['t']
        shortest_path_value = sample['value']

        vector_s = model.get_M_value_of_Leaf(s)
        vector_t = model.get_M_value_of_Leaf(t)

        # 下面这个算法没啥用，还是要单独计算导数的公式的
        approximate_shortest_path_value = np.linalg.norm(vector_s - vector_t, ord=1) / get_config("dimension")
        # loss = (approximate_shortest_path_value - shortest_path_value) ** 2
        # TODO: 这个导数可能出问题了，导致会一直下降，应该是value要降范围到-1到1把
        derivative_s = 2 * np.sign(vector_s - vector_t) * \
                       (approximate_shortest_path_value - shortest_path_value) / 10**get_config("norm_factor")


        derivative_t = -1 * derivative_s

        now_s_node = model.get_leaf_node(s)
        now_t_node = model.get_leaf_node(t)

        for i in range(model.num_inside_layer):
            now_level = model.num_inside_layer - i
            alpha = alpha_list[now_level]

            now_s_node.value -= alpha * derivative_s
            now_t_node.value -= alpha * derivative_t

            now_s_node = now_s_node.parent
            now_t_node = now_t_node.parent
            if now_s_node == now_t_node:
                break
