from math import sqrt
from random import shuffle, seed

def simulate_and_count_adjacent(i):
    # set seed for reproducibility
    seed(i)
    # create a random advent calendar layout
    layout = [divmod(i, 6) for i in range(24)]
    shuffle(layout)
    # count number of adjacent consecutive
    cnt = 0
    for p1, p2 in zip(layout[:-1], layout[1:]):
        l1_dist = abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
        cnt += l1_dist == 1
    return cnt

def simulate_and_measure(i):
    # set seed for reproducibility
    seed(i)
    # create a random advent calendar layout
    layout = [divmod(i, 6) for i in range(24)]
    shuffle(layout)
    # calculate total distance between consecutive doors
    tot = 0
    for p1, p2 in zip(layout[:-1], layout[1:]):
        tot += sqrt((p1[0]-p2[0]) ** 2 + (p1[1]-p2[1]) ** 2)
    return tot
