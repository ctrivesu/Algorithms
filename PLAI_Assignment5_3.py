__author__ = 'Sushant'
import random

import numpy as np


# Create a grid world
grid_size = 16
grid = np.zeros((grid_size, grid_size))
print(grid)

limit = (grid_size*grid_size/2)

# Fill with random k obstacles or wall
k = 0
while k < limit:
    i = np.random.choice(grid_size, 1)[0]
    j = np.random.choice(grid_size, 1)[0]
    if grid[i][j] == -1 or (i == 1 and j == 0):
        continue
    else:
        grid[i][j] = -1  # Obstacles
        k += 1
    print(grid)


# Randomly select an action. Do this for 15 timesteps
i, j = 1, 0       # our starting point of true path
step = 0
true_path = [[i, j]]
true_obs = []

# Take observation
obs = ""
if j == grid_size - 1 or grid[i][j + 1] == -1:
    obs += "E"
if j == 0 or grid[i][j - 1] == -1:
    obs += "W"
if i == 0 or grid[i - 1][j] == -1:
    obs += "N"
if i == grid_size - 1 or grid[i + 1][j] == -1:
    obs += "S"

true_obs.append(obs)
no_action = 0

# Move along a random path
while step < limit:
    all_actions = [0, 1, 2, 3]
    done = False

    # Try all possible choices by choosing an action randomly
    while len(all_actions) > 0 and not done:
        action = random.choice(all_actions)
        # print(action)
        if action == 0 and j < grid_size - 1 and grid[i][j+1] != -1: #Move East
                # print("moving east")
            j += 1
            done = True

        elif action == 1 and j > 1 and grid[i][j-1] != -1: #Move West
            # print("moving west")
            j -= 1
            done = True

        elif action == 2 and i > 1 and grid[i - 1][j] != -1: #Move North
            # print("moving north")
            i -= 1
            done = True

        elif action == 3 and i < grid_size - 1 and grid[i + 1][j] != -1: #Move South
            # print("moving south")
            i += 1
            done = True

        if not done:
            all_actions.remove(action)

    if not done:
        print("No action possible exiting")
        exit()

    # print("Move : ", step)

    # Take observation
    obs = ""
    if j == grid_size - 1 or grid[i][j + 1] == -1:
        obs += "E"
    if j == 0 or grid[i][j - 1] == -1:
        obs += "W"
    if i == 0 or grid[i - 1][j] == -1:
        obs += "N"
    if i == grid_size - 1 or grid[i + 1][j] == -1:
        obs += "S"

    true_obs.append(obs)

    # Increase step only when valid action is taken
    step += 1
    true_path.append([i, j])


print(true_path)
print(true_obs)

# Creating noisy observations:
# Add noise to about 75% observations
# for epsilon = 0 , discrepancy = 0. For all other values, discrepancy = 1

epsilon = [0, 0.05, 0.1, 0.2]
noisy_obs = [true_obs]

for i in range(1,len(epsilon)):
    noise = np.copy(true_obs)
    for j in range(len(true_obs)):
        """
        #Skip 25% of observations
        make_noisy = np.random.choice(4,1)
        if make_noisy == 0:
          continue
        """

        # Add noise to 75% observations with discrepancy 1
        all_obs = [0, 1, 2, 3]
        done = False

        while len(all_obs) > 0 and not done:
            val = random.choice(all_obs)
            if val == 0 and noise[j].find("E") < 0:
                noise[j] += "E"
                done = True
            # ''.join(sorted(a)) for sorting)
            elif val == 1 and noise[j].find("W") < 0:
                noise[j] += "W"
                done = True

            elif val == 2 and noise[j].find("N") < 0:
                noise[j] += "N"
                done = True

            elif val == 3 and noise[j].find("S") < 0:
                noise[j] += "E"
                done = True

            if not done:
                all_obs.remove(val)

    noisy_obs.append(noise.values)   # changes?-Sushant

for i in range(len(epsilon)):
    print(epsilon[i], noisy_obs[i])

# =========================
# Creating HMM MODEL
# =========================

total_states = grid_size * grid_size
scale = [10]
move_prob = np.full((1, 4), 0.25)
# move_prob = [E, W, N, S]

for k in scale:
    print("------------ k = ", k)
    print("1. Generating transition model")
    # Since south-west direction are more favoured, we multiple the prob for them by k and re normalize
    move_prob[0][0] *= k
    move_prob[0][3] *= k
    print("After scaling", move_prob)

    # Renormalize
    norm_factor = np.sum(move_prob)
    move_prob = move_prob / norm_factor
    print("After normalizing", move_prob)

    # 1. transition model - 3dimensional array
    T = np.zeros((total_states, total_states))
    print(T.shape)

    for z in range(T.shape[0]):
        curr_i = int(z / grid_size)
        curr_j = z % grid_size

        # Update transition probabilites of its neighbours in all directions
        # East
        if curr_j < grid_size - 1:
            T[z][(curr_i * grid_size) + (curr_j + 1)] = move_prob[0][0]

        # West
        if curr_j > 0:
            T[z][(curr_i * grid_size) + (curr_j - 1)] = move_prob[0][1]

        # North
        if curr_i > 0:
            T[z][((curr_i - 1) * grid_size) + curr_j] = move_prob[0][2]

        # South
        if curr_i < grid_size - 1:
            T[z][((curr_i + 1) * grid_size) + curr_j] = move_prob[0][3]

    # print(T)
    # Setting up prior distribution
    print("2. Prior distribution")

    # Initial location in northwest quadrant
    N = total_states / 4

    # initial_state:, a column vector
    state_prob = np.zeros((total_states, 1))

    for s in range(len(state_prob)):
        curr_i = int(s / grid_size)
        curr_j = s % grid_size
        if curr_i < grid_size / 2 and curr_j < grid_size / 2:
            state_prob[s][0] = 1 / N

    # print(state_prob)

    # Now start localization for each value of epsilon-error and correspoding observation
    for err in range(len(epsilon)):
        loc_error = []

        # Initializing the sensor_model
        print("3.Generating sensor model")
        O = np.zeros((total_states, total_states ))

        # Update the sensor model per observation
        for val in range(len(true_obs)):
            discrepancy = len(noisy_obs[err][val]) - len(true_obs[val])

        # Update the sensor_model for a state given the observation
        for o in range(total_states):
          O[o][o] = pow((1 - epsilon[err]), (4 - discrepancy)) * pow(epsilon[err], discrepancy)

        # Get new posterior probabilities
        # Renormalize the state prob distribution
        alpha = np.sum(state_prob)
        state_prob = state_prob / alpha
        # print(state_prob)

        new_state_prob = np.matmul(O, np.matmul(np.transpose(T), state_prob))
        del state_prob
        state_prob = np.copy(new_state_prob)
        del new_state_prob
        # print(state_prob)

        # Calculate the localization error
        most_likely_loc = np.argwhere(state_prob == np.amax(state_prob))
        error = 0
        for loc in most_likely_loc[0]:
            curr_i = int(loc / grid_size)
            curr_j = loc % grid_size

            # get manhattan distance and update error
            error = error + abs(true_path[val][0] - curr_i) + abs(true_path[val][0] - curr_i)
            # print("intermediate error = ", error)

        error /= len(most_likely_loc[0])
        print("Epsilon = ", epsilon[err], " : Error = ", error)
        loc_error.append(error)