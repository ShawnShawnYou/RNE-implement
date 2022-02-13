model_config = {
    "dimension": 64,
    "L_num": 1,
    "fan_out": 2,
    "k": 16,        # 这里k应该是16 25 36这种可以开方的数字



    "node_data_path": "../dataset/chengdu/chengdu.node",
    "edge_data_path": "../dataset/chengdu/chengdu.edge",
    "shortest_data_dir": "../dataset/chengdu/shortest_path/",

    "embedding_leaf_data_path": "../dataset/chengdu/chengdu_leaf_embedding.csv",
    "embedding_tree_data_path": "../dataset/chengdu/chengdu_tree_embedding.csv",
    "embedding_final_data_path": "../dataset/chengdu/chengdu_final_embedding.csv",

    "alpha": 0.05,
    "alpha_L": 0.05,
    "regular_factor": 0.8,
    "variance": 20,  # 为1是标准高斯分布,
    "norm_factor": 3,

    "error_based_epoch": 10000,
    "sample_N": 1000,
    "sample_N_t": 500,
    "landmark_rate": 0.0001,
    # TODO:做下坐标和哪个啥的映射关系；;
    "test_round": 100

}


def validate_key(key):
    assert isinstance(key, str)
    assert key in model_config.keys()


def get_config(key):
    validate_key(key)
    return model_config[key]


def set_config(key, value):
    validate_key(key)
    model_config[key] = value

