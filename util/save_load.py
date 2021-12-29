import json
import numpy as np
from config.model_config import get_config
import csv


def text_model_save(model):
    # 注意底层节点是按id序的插入，所以不用记录id
    # TODO: 这里也要存树的embedding，单独存一个文件比较好，最终的embedding可以存一个文件，一共3个文件
    # TODO: 问题在于，存text的时候他没有按照一行一个数据来走的，他是多行一个数据，读取的时候还是动态的，太难读了
    # 存最终的好处：可以不用加载模型直接计算，计算时间快
    # 不去存的好处：节省保存模型时间，减少一半

    with open(get_config("embedding_leaf_data_path"), "w") as f:
        f.write(str(model.data_size) + "\n")
    with open(get_config("embedding_final_data_path"), "w") as f:
        f.write(str(model.data_size) + "\n")

    with open(get_config("embedding_leaf_data_path"), "a") as f:
        for i in range(model.data_size):
            now_node = model.get_leaf_node(i)
            f.write(str(now_node.value) + "\n")

    with open(get_config("embedding_tree_data_path"), "a") as f:
        for i in range(model.num_inside_layer):
            now_layer = model.M_local[i]
            for now_node in now_layer:
                f.write(str(now_node.value) + "\n")

    with open(get_config("embedding_final_data_path"), "a") as f:
        for i in range(model.data_size):
            now_m_value = model.get_M_value_of_Leaf(i)
            f.write(str(now_m_value) + "\n")


def text_model_load(model):

    with open(get_config("embedding_leaf_data_path"), "rb") as f:
        num_node = int(f.readline())
        for i in range(model.data_size):
            value = np.array(json.loads(f.readline()))
            now_node = model.get_leaf_node(i)
            now_node.value = value


    with open(get_config("embedding_tree_data_path"), "rb") as f:
        for i in range(model.num_inside_layer):
            now_layer = model.M_local[i]
            for now_node in now_layer:
                value = np.array(json.loads(f.readline()))
                now_node.value = value


def csv_model_save(model):
    with open(get_config("embedding_leaf_data_path"), "w") as f:
        writer = csv.writer(f)
        for i in range(model.data_size):
            now_node = model.get_leaf_node(i)
            writer.writerow(now_node.value)

    with open(get_config("embedding_tree_data_path"), "w") as f:
        writer = csv.writer(f)
        for i in range(model.num_inside_layer):
            now_layer = model.M_local[i]
            for now_node in now_layer:
                writer.writerow(now_node.value)

    with open(get_config("embedding_final_data_path"), "w") as f:
        writer = csv.writer(f)
        for i in range(model.data_size):
            now_m_value = model.get_M_value_of_Leaf(i)
            writer.writerow(now_m_value)
