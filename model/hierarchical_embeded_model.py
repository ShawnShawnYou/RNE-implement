import numpy as np
import math
from config.model_config import get_config
from util.train import normalization


class TreeNode(object):
    def __init__(self, parent=None, level=None, node_id=None):
        dimension = get_config("dimension")

        self.value = np.random.randn(dimension)
        self.value = normalization(self.value)
        self.node_id = node_id
        self.level = level
        
        self.parent = parent
        self.child_list = []

    def get_child_list(self):
        return self.child_list

    def insert_child(self, node_id=None):
        child = TreeNode(self, self.level + 1, node_id)
        self.child_list.append(child)
        return child




class Model(object):
    def __init__(self):
        fan_out = get_config("fan_out")
        k = get_config("k")
        # math.ceil(math.log(k, fan_out)) + 1层内部节点
        self.num_inside_layer = math.ceil(math.log(k, fan_out)) + 1
        self.data_size = 0
        # 多1层叶子节点
        self.M_local = [[] for i in range(self.num_inside_layer + 1)]
        # 根节点不考虑
        self.M_local[0].append(TreeNode(None, 0))
        for i in range(self.num_inside_layer - 1):
            for node in self.M_local[i]:
                for j in range(fan_out):
                    child = node.insert_child()
                    self.M_local[i + 1].append(child)
        self.gps_positions = []


    def set_leaf_node_space(self, num_node):
        self.data_size = num_node
        self.M_local[self.num_inside_layer] = [None for i in range(num_node)]
        self.gps_positions = [None for i in range(num_node)]


    def get_M_value_of_Leaf(self, index):
        now_node = self.get_leaf_node(index)
        value_m = now_node.value
        while True:
            now_node = now_node.parent
            if now_node is None:
                break
            value_m += now_node.value

        return value_m

    def get_leaf_node(self, index):
        leaf_layer = self.M_local[-1]
        assert 0 <= index < len(leaf_layer)
        now_node = leaf_layer[index]
        return now_node

