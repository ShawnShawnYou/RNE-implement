from config.model_config import get_config
from util.level_learning_rate import level_learning_rate
from util.model_build import model_build
from util.sample import *
from util.save_load import *
from util.train import training_hier
from util.evaluate import simple_evaluate


def hierarchical_road_network_embedding():
    model = model_build()

    # road network graph
    road_graph = get_road_graph()

    # hierarchy embedding
    for level in range(1, model.num_inside_layer + 1):
        sample_set = simple_subgraph_level_samples(model, level, road_graph)
        alpha_list = [0 for i in range(model.num_inside_layer + 1)]
        for i in range(1, model.num_inside_layer + 1):
            alpha_list[i] = level_learning_rate(level, i)
        training_hier(model, alpha_list, sample_set)

    csv_model_save(model)
    return

    alpha_list = [0 for i in range(model.num_inside_layer + 1)]
    alpha_list[-1] = get_config("alpha_L")

    # vertices embedding
    sample_set = landmark_based_samples(model, road_graph)
    training_hier(model, alpha_list, sample_set)

    # fine tuning
    for k in range(get_config("error_based_epoch")):
        sample_set = error_based_samples(model, road_graph)
        training_hier(model, alpha_list, sample_set)


if __name__ == "__main__":
    print("origin")
    print(simple_evaluate())
    print()
    for i in range(40):
        hierarchical_road_network_embedding()
        print(i)
        print(simple_evaluate())
        print()
