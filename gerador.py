from random import randrange
from math import sqrt, ceil

nnodes = int(input())
MAX_X = 1000
MAX_Y = 1000
INSTANCES_DIR = "instances/"

AIRPORT_COST = sqrt(MAX_X**2 + MAX_Y**2)

nodes = [
    (
        randrange(0, MAX_X),
        randrange(0, MAX_Y),
        randrange(int(AIRPORT_COST // 2), int(AIRPORT_COST * 1.5)),
    )
    for _ in range(nnodes)
]


def dist(x, y):
    delta_x = nodes[x][0] - nodes[y][0]
    delta_y = nodes[x][1] - nodes[y][1]
    return sqrt(delta_x**2 + delta_y**2)


distances = [(x, y, dist(x, y)) for x in range(nnodes) for y in range(nnodes)]

with open(INSTANCES_DIR + "planar_" + str(nnodes), "w") as fd:
    print(randrange(int(nnodes * 0.1), int(nnodes * 0.4)), file=fd)
    for n in range(nnodes):
        print(n, nodes[n][2], file=fd)
    for d in distances:
        print(*d, sep="\t", file=fd)
