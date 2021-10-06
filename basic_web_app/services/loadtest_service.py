from math import sqrt
from random import randrange
from datetime import datetime


def simulate_load():

    load_cycles = 10000
    start_time = datetime.now()
    number = 0

    for i in range(0, load_cycles):
        load = sqrt(randrange(1, 1000))
        number += load

    return number


def get_load_test():

    load_test_results = simulate_load()

    return str(load_test_results)
