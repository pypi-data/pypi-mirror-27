from ..utils.math_utils import dot_product, magnitude


def cosine_distance(u, v):
    """
    returns the cosine distance between vectors u and v
    :param u:
    :param v:
    :return:
    """
    return dot_product(u, v) / (magnitude(u) * magnitude(v))


def cosine_similarity(u, v):
    return 1 - cosine_distance(u, v)
