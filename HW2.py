import random
import math

import numpy


LENGTH = 3
WIDTH = 3
DEPTH = 3
MINE = None
GOLD_SET = None

GOLD_CHANCE = 0.05
MAX_COST = 50


def generate_mine():
    global MINE, GOLD_SET


GOLD_SET = []
while len(GOLD_SET) < 1:  # just in case we didn’t generate ANY gold
    MINE = numpy.zeros((LENGTH, WIDTH, DEPTH))
for l in range(LENGTH):
    for w in range(WIDTH):
        for d in range(DEPTH):
        index = (l, w, d)
MINE[index] = random.randint(1, 50)
if random.uniform(0, 1) <= GOLD_CHANCE:
    GOLD_SET.append(index)
print("### Mining volume generated ###")
print("Gold set ({0} cell(s)):\n{1}\n\n".format(len(GOLD_SET), GOLD_SET))


def push_probe():


    # for simplicity, we assume WLOG that:
    # - push costs are equivalent to excavation costs
    # - entering a cell is the same cost regardless of the start direction
    print("\nProblem 4: Probe Push")
    push_costs = numpy.zeros((LENGTH, WIDTH, DEPTH))  # initialize the matrix
    for d in range(DEPTH):
        for l in range(LENGTH):
        for w in range(WIDTH):

        curr = (l, w, d)
    push_costs[curr] = MINE[curr]
47
if curr == (0, 0, 0):
    48
continue
49
north, west, top = math.inf, math.inf, math.inf
50
if l > 0:
    51
north = push_costs[(l - 1, w, d)]  # probe can move south
52
if w > 0:
    53
west = push_costs[(l, w - 1, d)]  # probe can move east
54
if d > 0:
    55
top = push_costs[(l, w, d - 1)]  # probe can move down
56
push_costs[curr] += min(north, west, top)
Hans
Behrens(  # 1211230537) CSE 551 Spring 2018: Homework 2
          57
58  # extract the traversal path
59
curr = (LENGTH - 1, WIDTH - 1, DEPTH - 1)
60
print("Probe traversal complete! Lowest possible cost: {0}".format(push_costs[curr]))
61
opt_path = []
62
while curr != (0, 0, 0):
    63
opt_path.append(curr)
64
target_weight = push_costs[curr] - MINE[curr]
65
if curr[0] >= 1 and push_costs[(curr[0] - 1, curr[1], curr[2])] == target_weight:
    66
curr = (curr[0] - 1, curr[1], curr[2])
67 elif curr[1] >= 1 and push_costs[(curr[0], curr[1] - 1, curr[2])] == target_weight:
68
curr = (curr[0], curr[1] - 1, curr[2])
69 elif curr[2] >= 1 and push_costs[(curr[0], curr[1], curr[2] - 1)] == target_weight:
70
curr = (curr[0], curr[1], curr[2] - 1)
71 else:
72
print("ERROR FINDING PATH")
73
opt_path.append((0, 0, 0))
74
print("Optimal path:")
75
for tup in reversed(opt_path):
    76
print(tup)
77
78
79


def vertical_dig():


80
this_mine = numpy.copy(MINE)
81
82
print("\nProblem 3: Vertical Shafts")
83
84
dig_set = []
85
total_cost = 0
86
for gold in GOLD_SET:
    87
curr = list(gold)
88
curr[2] = 0  # must excavate from surface first
89
while curr[2] <= gold[2]:
    90
cost = this_mine[tuple(curr)]  # we can’t excavate a cell twice
91
if cost > 0:
    92
entry = curr.copy()  # remember cell location
93
entry.append(cost)  # remember cell cost
94
entry.append(curr[2] == gold[2])  # remember if cell had gold or not
95
dig_set.append(entry)
96
total_cost += cost
97
curr[2] += 1
98
print("We may excavate all gold by excavating {2} cells (at a cost of {0}) in this order:\n
{1}
".format(
99
total_cost, dig_set, len(dig_set)))
100
101
102


def main():


103
generate_mine()  # generate our cost cube
104
vertical_dig()  # problem 3
105
push_probe()  # problem 4
106
107
108
if __name__ == "__main__":
    109
try:
    110
main()
111 except Exception as e:
112
print(e)