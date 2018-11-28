__author__ = 'Sushant'
import random
import time

import numpy as np


# SET DIRECTION
def set_direction(r_dire=None):
    # NORTH, EAST, SOUTH, WEST
    dire = [0, 1, 2, 3]
    if r_dire:
        dire.remove(r_dire)
        return dire[random.randint(0, 2)]
    else:
        return dire[random.randint(0, 3)]


# ROBOT WORLD
g_width = int(input("Enter the Width: "))
g_length = int(input("Enter the Length: "))
r_location = random.randint(0, g_width - 1), random.randint(0, g_length - 1)
# r_location = 0,0
NORTH, EAST, SOUTH, WEST = range(4)
r_dir = set_direction()

# AT WALL CHECK
def at_wall():
    global r_location
    global r_dir
    global g_width
    global g_length
    x, y = r_location
    next_pos = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
    next_coord = next_pos[r_dir]
    if next_coord[0] >= g_width or next_coord[1] >= g_length or next_coord[0] < 0 or next_coord[1] < 0:
        return True
    else:
        return False

# MOVE ROBOTS
def robot_step():
    global r_dir
    global r_location
    global g_width
    global g_length

    rand = random.random()
    if rand <= 0.2:
        r_dir = set_direction(r_dir)

    while at_wall():
        print("WALL")
        r_dir = set_direction(r_dir)

    x, y = r_location
    next_locations = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
    r_location = next_locations[r_dir]


# ADJACENT LOCATION
def adj_location(mode):
    global r_location
    global g_width
    global g_length
    x, y = r_location
    l_s = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
    ls_2 = [(x - 2, y - 2), (x - 2, y - 1), (x - 2, y), (x - 2, y + 1), (x - 2, y + 2), (x - 1, y - 2),
            (x - 1, y + 2), (x, y - 2), (x, y + 2), (x + 1, y - 2), (x + 1, y + 2), (x + 2, y - 2), (x + 2, y - 1),
            (x + 2, y), (x + 2, y + 1), (x + 2, y + 2)]

    if mode == 1:
        adj = l_s[random.randint(0, 7)]
        if adj[0] >= g_width or adj[1] >= g_length or adj[0] < 0 or adj[1] < 0:
            return None
        else:
            return adj

    if mode == 2:
        adj = ls_2[random.randint(0, 15)]
        if adj[0] >= g_width or adj[1] >= g_length or adj[0] < 0 or adj[1] < 0:
            return None
        else:
            return adj

# SENSE LOCATION
def sensor_location():
    global r_location
    L = 0.1
    L_s = 0.05
    L_s2 = 0.025
    rand = random.random()
    if rand <= L:
        return r_location
    elif rand <= L + L_s * 8:
        return adj_location(1)
    elif rand <= L + L_s * 8 + L_s2 * 16:
        return adj_location(2)
    else:
        return None

# /////////////// HMM MODEL //////////////


# PROBABLE TRANSITIONS
def probable_transitions(state):
    global g_length
    global g_width
    x, y, direction = state

    # came from: NORTH, EAST, SOUTH, WEST
    neighbors = [(x, y - 1), (x - 1, y), (x, y + 1), (x + 1, y)]
    prev_pos = neighbors[direction]
    prev_x, prev_y = prev_pos

    # Check bounds
    if prev_x < 0 or prev_x >= g_width or prev_y < 0 or prev_y >= g_length:
        return []

    # 0.8 -> Same Direction, 0.2 -> Different Direction
    square_dir = [((prev_x, prev_y, direction), 0.8)]
    dirs_left = list([0, 1, 2, 3])
    dirs_left.remove(direction)
    # Check if any directions point to walls.
    faces_wall = []

    # NORTH, EAST, SOUTH, WEST
    if 3 in dirs_left:
        if prev_x == 0:
            faces_wall.append((prev_x, prev_y, 3))
        else:
            square_dir.append(((prev_x, prev_y, 3), 0.1))
    if 1 in dirs_left:
        if prev_x == g_width - 1:
            faces_wall.append((prev_x, prev_y, 1))
        else:
            square_dir.append(((prev_x, prev_y, 1), 0.1))
    if 2 in dirs_left:
        if prev_y == 0:
            faces_wall.append((prev_x, prev_y, 2))
        else:
            square_dir.append(((prev_x, prev_y, 2), 0.1))
    if 0 in dirs_left:
        if prev_y == g_length - 1:
            faces_wall.append((prev_x, prev_y, 0))
        else:
            square_dir.append(((prev_x, prev_y, 0), 0.1))

    for state in faces_wall:
        square_dir.append((state, float(1) / (4 - len(faces_wall))))
    return square_dir

# T-MATRIX
t_matrix = np.array(np.zeros(shape=(g_width * g_length * 4, g_width * g_length * 4)))
for i in range(g_width * g_length * 4):
    x = int(i / (g_length * 4))
    y = int((i / 4) % g_length)
    heading = i % 4

    prev_states = probable_transitions((x, y, heading))
    for (x_cp, y_cp, direction), probability in prev_states:
        t_matrix[i, x_cp * g_length * 4 + y_cp * 4 + direction] = probability
print("TMATRIX: ", t_matrix.shape)

# PRIOR MATRIX
pmsize = g_width * g_length * 4
priors = [float(1) / pmsize] * pmsize
p_matrix = np.array([priors])
print("PMATRIX: ", p_matrix.shape, pmsize)
p_matrix = p_matrix[0]

# ADJACENT POSSIBLE CHECK
def poss_adj(mode, x, y):
    possible_adj = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y),
                    (x + 1, y + 1)]

    possible_adj2 = [(x - 2, y - 2), (x - 2, y - 1), (x - 2, y), (x - 2, y + 1), (x - 2, y + 2), (x - 1, y - 2),
                     (x - 1, y + 2), (x, y - 2), (x, y + 2), (x + 1, y - 2), (x + 1, y + 2), (x + 2, y - 2),
                     (x + 2, y - 1),
                     (x + 2, y), (x + 2, y + 1), (x + 2, y + 2)]

    if mode == 1:
        # Bound check
        for poss_x, poss_y in list(possible_adj):
            if poss_x >= g_width or poss_x < 0 or poss_y >= g_length or poss_y < 0:
                possible_adj.remove((poss_x, poss_y))

        return possible_adj

    if mode == 2:
        # Bound check
        for poss_x, poss_y in list(possible_adj2):
            if poss_x >= g_width or poss_x < 0 or poss_y >= g_length or poss_y < 0:
                possible_adj2.remove((poss_x, poss_y))

        return possible_adj2


# N MATRIX
o_matrix = np.array(np.zeros(shape=(pmsize, pmsize)))

for i in range(pmsize):
    x = int(i / (g_length * 4))
    y = int((i / 4) % g_length)

    num_adj = 8 - len(poss_adj(1, x, y))
    num_adj2 = 16 - len(poss_adj(2, x, y))

    o_matrix[i, i] = 0.1 + 0.05 * num_adj + 0.025 * num_adj2

print("OMATRIX: ", o_matrix.shape)

# ADJACENT ASSIGNEMENT
def adjacent_list(fo_matrix, list_adj, prob):
    for poss_x, poss_y in list_adj:
        index = poss_x * g_length * 4 + poss_y * 4
        for k in range(4):
            fo_matrix[index + k, index + k] = prob
    return fo_matrix

# SENSOR MATRIX
def create_sensor_matrix(sensed_coord):
    if sensed_coord is None:
        return o_matrix
    global g_width
    global g_length
    o = np.array(np.zeros(shape=(g_width * g_length * 4, g_width * g_length * 4)))
    x, y = sensed_coord

    index = x * g_length * 4 + y * 4
    for i in range(4):
        o[index + i, index + i] = 0.1

    o = adjacent_list(o, poss_adj(1, x, y), 0.05)
    o = adjacent_list(o, poss_adj(2, x, y), 0.025)

    return o



def most_probable():
    global p_matrix
    max_prob_idx = np.argmax(p_matrix)
    x = int(max_prob_idx / (g_length * 4))
    y = int((max_prob_idx / 4) % g_length)
    return (x, y), p_matrix[max_prob_idx]

def forward_step(coord):
    global p_matrix
    o = create_sensor_matrix(coord)
    global t_matrix
    p_matrix = t_matrix.dot(p_matrix).dot(o)
    p_matrix /= np.sum(p_matrix)


def guess_move():
    sensed_location = sensor_location()
    print("Sensor senses: ", sensed_location)
    forward_step(sensed_location)
    move_estimate, prob = most_probable()
    print("Robot thinks it's in: ", move_estimate, " with probability: ", prob)
    return move_estimate, prob

# DECISION MAKING

moves = 0
correct_guess = 0
for i in range(100):
    robot_step()
    moves += 1
    print("\nRobot is in: ", r_location)
    guessed_move, probability = guess_move()
    if guessed_move == r_location:
        correct_guess += 1
    man_distance = abs(guessed_move[0] - r_location[0]) + abs(guessed_move[1] - r_location[1])
    print("Manhattan distance: ", man_distance)
    print("Robot has been correct:", float(correct_guess) / moves, "of the time.")
    time.sleep(1)

