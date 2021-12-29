import math
from config.model_config import get_config


def gauss_function(a, b, c, x):
    exp = -1 * (x - b)**2 / (2 * c**2)
    return a * math.pow(math.e, exp)


def fraction_rate_function(a, b, x):
    return a / (math.fabs(x - b) + 1)


def level_learning_rate(level, l):
    a = get_config("alpha")
    c = get_config("variance")
    return gauss_function(a, level, c, l)
