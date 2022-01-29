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


def load_embedding(path):
    with open(path) as f:
        reader = csv.reader(f)
        headers = next(reader)

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

    return abs(approx_value - real_value) / real_value


def draw(data):
    from matplotlib import pyplot as plt
    from matplotlib import font_manager


    a = data
    # 设置组距
    d = 3
    plt.figure(figsize=(20, 8), dpi=80)
    plt.hist(a, 50)
    plt.xlabel('error')
    plt.ylabel('num')
    plt.xlim(0, 10)


    plt.show()

def simple_evaluate():
    with open(get_config("node_data_path"), 'rb') as f:
        num_node = int(f.readline())

    embedding = load_embedding(get_config("embedding_final_data_path"))

    draw_data = []
    total_error_rate = 0
    for i in range(get_config("test_round")):
        s = random.randint(0, num_node - 2)
        t = random.randint(0, num_node - 2)

        real_value = classic_shortest_path(s, t) / 10**get_config("norm_factor")

        # TODO: 这里还是一次性全读进内存把，读csv太傻了
        vector_s = np.array(embedding[s]).astype(np.float)
        vector_t = np.array(embedding[t]).astype(np.float)
        approx_value = np.linalg.norm(vector_s - vector_t, ord=1) / get_config("dimension")
        # approx_value = np.sum(abs(vector_s - vector_t), keepdims=True)
        error_rate_value = error_rate(approx_value, real_value)
        total_error_rate += error_rate(approx_value, real_value)
        draw_data.append(error_rate_value)

    avg_error_rate = total_error_rate / get_config("test_round")

    return avg_error_rate, draw_data


if __name__ == "__main__":
    avg_error_rate, draw_data = simple_evaluate()
    draw(draw_data)
    print(avg_error_rate)




