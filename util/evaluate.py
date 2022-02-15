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


def simple_evaluate():
    with open(get_config("node_data_path"), 'rb') as f:
        num_node = int(f.readline())

    embedding = load_embedding(get_config("embedding_final_data_path"))
    road_graph = get_road_graph()
    draw_data = []
    total_error_rate = 0
    test_round = 0
    for i in range(get_config("test_round")):
        s = random.randint(0, num_node - 1)
        # s = 1
        try:
            dijkstra_result_s = nx.single_source_dijkstra_path_length(road_graph, s)
        except Exception as e:
            continue

        for j in range(100):
            try:
                t = random.randint(0, num_node - 1)
                # t = 200000
                real_value = dijkstra_result_s[t] / 10**get_config("norm_factor")
            except Exception as e:
                continue
            test_round += 1
            vector_s = np.array(embedding[s]).astype(np.float)
            vector_t = np.array(embedding[t]).astype(np.float)
            approx_value = np.linalg.norm(vector_s - vector_t, ord=1)
            # approx_value = np.sum(abs(vector_s - vector_t), keepdims=True)
            error_rate_value = error_rate(approx_value, real_value) * 100

            total_error_rate += error_rate_value
            draw_data.append(error_rate_value)

    avg_error_rate = total_error_rate / test_round

    draw_data.sort()
    count = [0 for i in range(11)]

    for i in draw_data:
        if i < 100:
            count[int(i / 10)] += 1
        else:
            count[10] += 1

    count = [round(i * 100 / test_round, 4) for i in count]

    return avg_error_rate, count


if __name__ == "__main__":
    print(simple_evaluate())




