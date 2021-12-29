from config.model_config import get_config
import linecache


def manhattan_distance(s, t):
    node_s = linecache.getline(get_config("node_data_path"), s + 2)
    node_t = linecache.getline(get_config("node_data_path"), t + 2)

    s_x, s_y = float(node_s.split()[0]), float(node_s.split()[1])
    t_x, t_y = float(node_t.split()[0]), float(node_t.split()[1])

    return abs(s_x - t_x) + abs(s_y - t_y)


def a_star_algorithm(s, t):
    pass


def classic_shortest_path(s, t):
    return manhattan_distance(s, t)
