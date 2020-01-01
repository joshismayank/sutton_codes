import numpy

GRIDWORLD_SIZE = 5
ACCEPTABLE_ERROR = 1e-4
ACTIONS = [numpy.array([0,-1]),numpy.array([-1,0]),numpy.array([0,1]),numpy.array([1,0])]
DISCOUNT = 0.9
ACTION_PROB = 0.25

def print_values(values):
    for i in range(GRIDWORLD_SIZE):
        for j in range(GRIDWORLD_SIZE):
            print("{}  ".format(values[i,j])),
        print(" ")


def perform_action(curr_i,curr_j,action):
    if curr_i == 0 and curr_j == 1:
        reward = 10
        curr_i = 4
        curr_j = 1
    elif curr_i == 0 and curr_j == 3:
        reward = 5
        curr_i = 2
        curr_j = 3
    else:
        i = curr_i+action[0]
        j = curr_j+action[1]
        if i >= GRIDWORLD_SIZE or i < 0:
            reward = -1
        elif j>= GRIDWORLD_SIZE or j< 0:
            reward = -1
        else:
            reward = 0
            curr_i = i
            curr_j = j
    return curr_i, curr_j, reward


def value_iteration():
    for n in range(0,12,5):
        iteration = 1
        curr_values = numpy.full((GRIDWORLD_SIZE,GRIDWORLD_SIZE),n)
        while True:
            new_values = numpy.zeros_like(curr_values)
            for i in range(0,GRIDWORLD_SIZE):
                for j in range(0,GRIDWORLD_SIZE):
                    temp_rewards = []
                    for action in ACTIONS:
                        next_i, next_j, reward = perform_action(i,j,action)
                        temp_rewards.append(reward + DISCOUNT*curr_values[next_i,next_j])
                    new_values[i,j] = numpy.max(temp_rewards)
            if numpy.sum(numpy.abs(curr_values-new_values)) < ACCEPTABLE_ERROR:
                print_values(curr_values)
                print("for n {}: iterations required - {}".format(n,iteration))
                break
            else:
                iteration = iteration+1
                curr_values = new_values


def bellman_iteration():
    for n in range(0,12,5):
        iteration = 1
        curr_values = numpy.full((GRIDWORLD_SIZE,GRIDWORLD_SIZE),n)
        while True:
            new_values = numpy.zeros_like(curr_values)
            for i in range(0,GRIDWORLD_SIZE):
                for j in range(0,GRIDWORLD_SIZE):
                    temp_rewards = []
                    for action in ACTIONS:
                        next_i, next_j, reward = perform_action(i,j,action)
                        new_values[i,j] += ACTION_PROB*(reward+DISCOUNT*curr_values[next_i,next_j])
            if numpy.sum(numpy.abs(curr_values-new_values)) < ACCEPTABLE_ERROR:
                print_values(curr_values)
                print("for n {}: iterations required - {}".format(n,iteration))
                break
            else:
                iteration = iteration+1
                curr_values = new_values


value_iteration()
bellman_iteration()
