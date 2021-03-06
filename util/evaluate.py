import random
import linecache
import json
import csv
import numpy as np
from algorithm.classic_shortest_path_algorithm import classic_shortest_path
from config.model_config import get_config
from util.sample import get_road_graph
import networkx as nx


def get_file_of_line(path, index):
    # 问题在于一个数据不是一行
    with open(path) as f:
        reader = csv.reader(f)
        headers = next(reader)

        i = 0
        for row in reader:
            if len(row) == 0:
                continue
            if i == index:
                return row
            else:
                i += 1


def load_embedding(path):
    with open(path) as f:
        reader = csv.reader(f)

        i = 0
        row_list = []
        for row in reader:
            if len(row) == 0:
                continue
            row_list.append(row)
            i += 1

        return row_list


def MES(a, b):
    return (a - b) ** 2


def error_rate(approx_value, real_value):
    if real_value == 0:
        return 0
    error = abs(approx_value - real_value) / real_value
    return error


def simple_evaluate(print_flag, my_test_round, cache_dijkstra):
    with open(get_config("node_data_path"), 'rb') as f:
        num_node = int(f.readline())

    embedding = load_embedding(get_config("embedding_final_data_path"))
    road_graph = get_road_graph()
    draw_data = []

    sample_set = []

    total_error_rate = 0
    total_normal_error_rate = 0
    total_overflow_error_rate = 0

    test_round = 1
    normal_round = 1
    overflow_round = 1
    for i in range(my_test_round):
        s = random.randint(0, num_node - 1)
        # s = 1
        try:
            if s not in cache_dijkstra.keys():
                cache_dijkstra[s] = nx.single_source_dijkstra_path_length(road_graph, s)
            dijkstra_result_s = cache_dijkstra[s]
        except Exception as e:
            continue

        for j in range(100):
            try:
                t = random.randint(0, num_node - 1)
                # t = 200000
                real_value = dijkstra_result_s[t]
            except Exception as e:
                continue

            vector_s = np.array(embedding[s]).astype(np.float)
            vector_t = np.array(embedding[t]).astype(np.float)
            approx_value = np.linalg.norm(vector_s - vector_t, ord=1) * 10**get_config("norm_factor")
            # approx_value = np.sum(abs(vector_s - vector_t), keepdims=True)
            error_rate_value = error_rate(approx_value, real_value) * 100

            test_round += 1
            total_error_rate += error_rate_value
            if error_rate_value >= 10:
                sample = {
                    "s": s,
                    "t": t,
                    "value": real_value
                }
                sample_set.append(sample)
            if error_rate_value >= 100:
                total_overflow_error_rate += error_rate_value
                overflow_round += 1
            else:
                total_normal_error_rate += error_rate_value
                normal_round += 1

            draw_data.append(error_rate_value)

    avg_error_rate = total_error_rate / test_round
    avg_normal_rate = total_normal_error_rate / normal_round
    avg_overflow_rate = total_overflow_error_rate / overflow_round

    draw_data.sort()
    count = [0 for i in range(11)]

    for i in draw_data:
        if i < 100:
            count[int(i / 10)] += 1
        else:
            count[10] += 1

    count = [round(i * 100 / test_round, 4) for i in count]

    if print_flag:
        print(avg_error_rate)
        print(avg_normal_rate)
        print(avg_overflow_rate)
        print(count)
        print(draw_data[10000], draw_data[25000], draw_data[50000],
              draw_data[75000], draw_data[90000], draw_data[-1])

    return sample_set


if __name__ == "__main__":
    simple_evaluate(True, get_config("test_round"), {})





