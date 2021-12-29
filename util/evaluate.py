import random
import linecache
import json
import csv
import numpy as np
from algorithm.classic_shortest_path_algorithm import classic_shortest_path
from config.model_config import get_config


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



def MES(a, b):
    return (a - b) ** 2


def error_rate(approx_value, real_value):

    return abs(approx_value - real_value) / real_value


def simple_evaluate():
    with open(get_config("node_data_path"), 'rb') as f:
        num_node = int(f.readline())

    total_error_rate = 0
    for i in range(get_config("test_round")):
        s = random.randint(0, num_node - 1)
        t = random.randint(0, num_node - 1)

        real_value = classic_shortest_path(s, t) / 10**get_config("norm_factor")

        vector_s = np.array(get_file_of_line(get_config("embedding_final_data_path"), s)).astype(np.float)
        vector_t = np.array(get_file_of_line(get_config("embedding_final_data_path"), t)).astype(np.float)
        approx_value = np.linalg.norm(vector_s - vector_t, ord=1)
        # approx_value = np.sum(abs(vector_s - vector_t), keepdims=True)

        total_error_rate += error_rate(approx_value, real_value)

    avg_error_rate = total_error_rate / get_config("test_round")

    return avg_error_rate


if __name__ == "__main__":
    print(simple_evaluate())




