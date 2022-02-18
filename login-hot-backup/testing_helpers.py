from random import random, choice


def random_string_from(other_string, num_chars=10):
    return "".join([choice(other_string) for _ in range(num_chars)])