import numpy as np

EPSILON = 0.1
DISCOUNT = 1
ALPHA_STEP_SIZE = 0.5
ACTION_UP = 0
ACTION_DOWN = 1
ACTION_RIGHT = 2
ACTION_LEFT = 3
WORLD_HEIGHT = 4
WORLD_WIDTH = 12
EPISODES = 100
TERMINAL_STATE = np.asarray([3,11])
START_STATE = np.asarray([3,0])
DEAD_STATES = [[3,1],[3,2],[3,3],[3,4],[3,5],[3,6],[3,7],[3,8],[3,9],[3,10]]
q_s_a = None


def initialize_values():
    global q_s_a
    q_s_a = np.random.random((WORLD_HEIGHT,WORLD_WIDTH,4))


def compute_next_state(curr_state,curr_action):
    #print("in compute next state")
    next_state = np.copy(curr_state)
    if curr_action == ACTION_UP:
        if next_state[0] > 0:
            next_state[0] = next_state[0] - 1
    elif curr_action == ACTION_LEFT:
        if next_state[1] > 0:
            next_state[1] = next_state[1] - 1
    elif curr_action == ACTION_DOWN:
        if next_state[0] < (WORLD_HEIGHT - 1):
            next_state[0] = next_state[0] + 1
    elif curr_action == ACTION_RIGHT:
        if next_state[1] < (WORLD_WIDTH - 1):
            next_state[1] = next_state[1] + 1
    return next_state


def infer_action(curr_action):
    if curr_action == ACTION_LEFT:
        return 'L'
    elif curr_action == ACTION_DOWN:
        return 'D'
    elif curr_action == ACTION_UP:
        return 'U'
    elif curr_action == ACTION_RIGHT:
        return 'R'


def print_path():
    global q_s_a
    i = 0
    curr_state = START_STATE
    while not np.array_equal(curr_state,TERMINAL_STATE) and i < 50:
        i = i + 1
        print("{}->".format(curr_state)),
        alpha = q_s_a[curr_state[0],curr_state[1],:]
        #print("alpha: {}".format(alpha))
        beta = np.argmax(alpha)
        #print("beta: {}".format(beta))
        curr_action = beta
        next_state = compute_next_state(curr_state,curr_action)
        #print("next_state: {}".format(next_state))
        curr_action = infer_action(curr_action)
        curr_state = next_state


def perform_action(curr_state,curr_action):
    next_state = np.copy(curr_state)
    if curr_action == ACTION_UP:
        if next_state[0] > 0:
            next_state[0] = next_state[0] - 1
        return -1, next_state
    elif curr_action == ACTION_DOWN:
        if next_state[0] < (WORLD_HEIGHT - 1):
            next_state[0] = next_state[0] + 1
        if np.array(next_state).tolist() in DEAD_STATES:
            return -100, next_state
        return -1, next_state
    elif curr_action == ACTION_LEFT:
        if next_state[1] > 0:
            next_state[1] = next_state[1] - 1
        return -1, next_state
    elif curr_action == ACTION_RIGHT:
        if next_state[1] < (WORLD_WIDTH - 1):
            next_state[1] = next_state[1] + 1
        #print("DEAD_STATES: {}, type - {}".format(DEAD_STATES,type(DEAD_STATES)))
        #print("next_state: {}, type - {}".format(next_state,type(next_state)))
        if np.array(next_state).tolist() in DEAD_STATES:
            return -100, next_state
        return -1, next_state


def get_action(curr_state):
    #print("in get_action")
    global q_s_a
    if np.random.binomial(1,EPSILON) == 1:
        #print("random action")
        return np.random.choice([ACTION_UP,ACTION_DOWN,ACTION_LEFT,ACTION_RIGHT])
    else:
        #print("action from q_s_a")
        max_value = np.max(q_s_a[curr_state[0],curr_state[1],:])
        #print("max_value from q_s_a: {}".format(max_value))
        possible_actions = []
        for action in [ACTION_UP,ACTION_DOWN,ACTION_LEFT,ACTION_RIGHT]:
            #print("iterating action: {}".format(action))
            if q_s_a[curr_state[0],curr_state[1],action] == max_value:
                possible_actions.append(action)
                #print("apended actions: {}".format(action))
            #else:
                #print("did not append action bcs value: {}".format(q_s_a[curr_state[0],curr_state[1],action]))
        return np.random.choice(possible_actions)


def main():
    global q_s_a
    initialize_values()
    for e in range(EPISODES):
        #print("episode: {}".format(e))
        curr_state = START_STATE
        while not np.array_equal(curr_state,TERMINAL_STATE):
            curr_action = get_action(curr_state)
            #print("curr_state: {}, curr_action: {}".format(curr_state,curr_action))
            reward, next_state = perform_action(curr_state,curr_action)
            #print("reward: {}, next_state: {}".format(reward,next_state))
            optimum_action = int(np.argmax(q_s_a[next_state[0],next_state[1],:]))
            #print("optimum_action: {}".format(optimum_action))
            #print("q_s_a old: {}".format(q_s_a))
            #print("next_state: {}, curr_state: {}, optimum_action: {}, curr_action: {}".format(next_state,curr_state,optimum_action,curr_action))
            temp = reward + DISCOUNT*q_s_a[next_state[0],next_state[1],optimum_action] - q_s_a[curr_state[0],curr_state[1],curr_action]
            q_s_a[curr_state[0],curr_state[1],curr_action] = q_s_a[curr_state[0],curr_state[1],curr_action] + ALPHA_STEP_SIZE*temp
            #print("q_s_a new: {}".format(q_s_a))
            curr_state = next_state
            if np.array(curr_state).tolist() in DEAD_STATES:
                #print("curr_state: {} in DEAD_STATES - breaking".format(curr_state))
                break
        if e%99 == 0:
            print("after episode: {}".format(e))
            print_path()


main()
