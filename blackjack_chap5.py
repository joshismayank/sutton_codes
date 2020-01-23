from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
import numpy as np
from random import randrange
import random

HIT = 1
STAY = 0
MC_ES_ITERATIONS = 50000
MC_OP_ITERATIONS = 50000
EPSILON = 0.2
policy_es = None
policy_op = None
q_value = None
value = None
s_a_encounters = None
s_encounters = None
s_a_episode = None
s_episode = None


def initialize_values():
    global policy_es
    policy_es = np.full((200,1),HIT,dtype=int)
    for i in range(10):
        for j in range(2):
            temp = j*100 + i
            policy_es[temp+10*8] = STAY
            policy_es[temp+10*9] = STAY
    global policy_op
    policy_op = np.zeros((200,2))
    global q_value
    q_value = np.zeros((200,2))
    global value
    value = np.zeros((200,1))
    global s_a_encounters
    s_a_encounters = np.zeros((200,2))
    global s_encounters
    s_encounters = np.zeros((200,1))


def initialize_episode():
    global s_a_episode
    s_a_episode = np.zeros((200,2))
    global s_episode
    s_episode = np.zeros((200,1))


def player_play_es(player_sum,player_action,dealer_card,usable_ace):
    global policy_es
    global s_episode
    global s_a_episode
    if player_sum > 21:
        return player_sum
    if player_action == STAY:
        return player_sum
    else:
        next_sum = randrange(10) + 1
        next_state = usable_ace*100 + (next_sum-1)*10 + dealer_card - 1
        next_action = policy_es[next_state]
        s_episode[next_state] = s_episode[next_state] + 1
        s_a_episode[next_state,next_action] = s_a_episode[next_state,next_action] + 1
        player_play_es(next_sum,next_action,dealer_card,usable_ace)


def player_play_op(player_sum,player_action,dealer_card,usable_ace):
    global policy_op
    global s_episode
    global s_a_episode
    if player_sum > 21:
        return player_sum
    if player_action == STAY:
        return player_sum
    else:
        next_sum = randrange(10) + 1
        next_state = usable_ace*100 + (next_sum-1)*10 + dealer_card - 1
        if policy_op[next_state,0] > policy_op[next_state,1]:
            max_action = 0
        else:
            max_action = 1
        if random.uniform(0,1) > EPSILON:
            next_action = max_action
        else:
            next_action = 1 - max_action
        s_episode[next_state] = s_episode[next_state] + 1
        s_a_episode[next_state,next_action] = s_a_episode[next_state,next_action] + 1
        player_play_op(next_sum,next_action,dealer_card,usable_ace)


def dealer_play(dealer_card):
    curr_sum = dealer_card + randrange(11) + 1
    while curr_sum < 14:
        curr_sum = curr_sum + randrange(10) + 1
    return curr_sum


def update_q_value_es(return_episode):
    global s_a_episode
    global value
    global q_value
    global s_a_encounters
    global s_encounters
    for i in range(200):
        for j in range(2):
            if s_a_episode[i,j] != 0:
                q_value[i,j] = (q_value[i,j]*s_a_encounters[i,j] + return_episode)/(s_a_encounters[i,j]+1)
                s_a_encounters[i,j] = s_a_encounters[i,j] + 1
                value[i] = (value[i]*s_encounters[i]+return_episode)/(s_encounters[i]+1)
                s_encounters[i] = s_encounters[i] + 1
 

def update_policy_es():
    global q_value
    global policy_es
    for i in range(200):
        if s_episode[i] != 0:
            if q_value[i,0] > q_value[i,1]:
                action = 0
            else:
                action = 1
            policy_es[i] = action


def update_q_value_op(return_episode):
    global q_value
    global s_a_encounters
    global s_encounters
    for i in range(200):
        for j in range(2):
            if s_a_episode[i,j] != 0:
                q_value[i,j] = (q_value[i,j]*s_a_encounters[i,j] + return_episode)/(s_a_encounters[i,j]+1)
                s_a_encounters[i,j] = s_a_encounters[i,j] + 1
                value[i] = (value[i]*s_encounters[i]+return_episode)/(s_encounters[i]+1)
                s_encounters[i] = s_encounters[i] + 1
 

def update_policy_op():
    global s_episode
    global q_value
    global policy_op
    for i in range(200):
        if s_episode[i] != 0:
            if q_value[i,0] > q_value[i,1]:
                action = 0
            else:
                action = 1
            policy_op[i,action] = 1-EPSILON+(EPSILON/2)
            opposite_action = 1-action
            policy_op[i,opposite_action] = EPSILON/2


def monte_carlo_es(iterations):
    global s_episode
    global s_a_episode
    initialize_values()
    i = 0
    while i < iterations:
        i = i + 1
        return_episode = None
        curr_state = randrange(200)
        curr_action = randrange(2)
        temp1 = curr_state%10
        temp2 = temp1+1
        temp3 = curr_state/10
        temp4 = temp3%10
        temp5 = temp4+12
        temp6 = temp3/10
        initialize_episode()
        s_episode[curr_state] = 1
        s_a_episode[curr_state,curr_action] = 1
        player_sum = temp5
        player_action = curr_action
        dealer_card = temp2
        dealer_sum = dealer_card + randrange(10) + 1
        usable_ace = temp6
        player_sum = player_play_es(player_sum,player_action,dealer_card,usable_ace)
        if player_sum > 21:
            return_episode = -1
            update_q_value_es(return_episode)
            update_policy_es()
            continue
        dealer_sum = dealer_play(dealer_card)
        if dealer_sum == 21 and player_sum == 21:
            return_episode = 0
        elif player_sum == 21:
            return_episode = 1
        elif dealer_sum == 21:
            return_episode = -1
        elif dealer_sum > 21:
            return_episode = 1
        elif dealer_sum == player_sum:
            return_episode = 0
        elif dealer_sum > player_sum:
            return_episode = -1
        else:
            return_episode = 1
        update_q_value_es(return_episode)
        update_policy_es()


def monte_carlo_op(iterations):
    global policy_op
    global s_episode
    global s_a_episode
    initialize_values()
    i = 0
    while i < iterations:
        i = i + 1
        return_episode = None
        curr_state = randrange(200)
        if policy_op[curr_state,0] > policy_op[curr_state,1]:
            max_action = 0
        else:
            max_action = 1
        if random.uniform(0,1) > EPSILON:
            curr_action = max_action
        else:
            curr_action = 1 - max_action
        temp1 = curr_state%10
        temp2 = temp1+1
        temp3 = curr_state/10
        temp4 = temp3%10
        temp5 = temp4+12
        temp6 = temp3/10
        initialize_episode()
        s_episode[curr_state] = 1
        s_a_episode[curr_state,curr_action] = 1
        player_sum = temp5
        player_action = curr_action
        dealer_card = temp2
        dealer_sum = dealer_card + randrange(10) + 1
        usable_ace = temp6
        player_sum = player_play_op(player_sum,player_action,dealer_card,usable_ace)
        if player_sum > 21:
            return_episode = -1
            update_q_value_op(return_episode)
            update_policy_op()
            continue
        dealer_sum = dealer_play(dealer_card)
        if dealer_sum == 21 and player_sum == 21:
            return_episode = 0
        elif player_sum == 21:
            return_episode = 1
        elif dealer_sum == 21:
            return_episode = -1
        elif dealer_sum > 21:
            return_episode = 1
        elif dealer_sum == player_sum:
            return_episode = 0
        elif dealer_sum > player_sum:
            return_episode = -1
        else:
            return_episode = 1
        update_q_value_op(return_episode)
        update_policy_op()


def print_result_es():
    global policy_es
    global value
    #policy: player sum vs dealer card vs policy for usable ace
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(100,200):
        x = (i/10)%10 + 12 #player_sum
        y = i%10 + 1 #dealer_card
        z = policy_es[i]
        if z == 0:
            m = 'o'
            color = 'red'
        else:
            m = '^'
            color = 'blue'
        ax.scatter(x,y,z,marker=m,color=color)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.savefig('policy_usable_ace_es.png')
    #policy: player sum vs dealer card vs policy for non usable ace
    ax = fig.add_subplot(111, projection='3d')
    for i in range(100):
        x = (i/10)%10 + 12 #player_sum
        y = i%10 + 1 #dealer_card
        z = policy_es[i]
        if z == 0:
            m = 'o'
            color = 'red'
        else:
            m = '^'
            color = 'blue'
        ax.scatter(x,y,z,marker=m,color=color)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.savefig('policy_non_usable_ace_es.png')
    #value: player sum vs dealer card vs value for usable ace
    ax = fig.add_subplot(111, projection='3d')
    x = np.arange(12,22,1)
    y = np.arange(1,11,1)
    xx,yy = np.meshgrid(x,y)
    zz = np.zeros((10,10))
    for i in range(10):
        for j in range(10):
            zz[i,j] = value[100+i*10+j]
    ax.plot_wireframe(xx, yy, zz, rstride=1, cstride=1)
    plt.savefig('value_usable_ace_es.png')
    #value: player sum vs dealer card vs value for non usable ace
    ax = fig.add_subplot(111, projection='3d')
    x = np.arange(12,22,1)
    y = np.arange(1,11,1)
    xx,yy = np.meshgrid(x,y)
    zz = np.zeros((10,10))
    for i in range(10):
        for j in range(10):
            zz[i,j] = value[i*10+j]
    ax.plot_wireframe(xx, yy, zz, rstride=1, cstride=1)
    plt.savefig('value_non_usable_ace_es.png')


def print_result_op():
    global policy_op
    global value
    #policy: player sum vs dealer card vs policy for usable ace
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(100,200):
        x = (i/10)%10 + 12 #player_sum
        y = i%10 + 1 #dealer_card
        if policy_op[i,0] > policy_op[i,1]:
            z = policy_op[i,0]
        else:
            z = policy_op[i,1]
        if z == 0:
            m = 'o'
            color = 'red'
        else:
            m = '^'
            color = 'blue'
        ax.scatter(x,y,z,marker=m,color=color)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.savefig('policy_usable_ace_op.png')
    #policy: player sum vs dealer card vs policy for non usable ace
    ax = fig.add_subplot(111, projection='3d')
    for i in range(100):
        x = (i/10)%10 + 12 #player_sum
        y = i%10 + 1 #dealer_card
        if policy_op[i,0] > policy_op[i,1]:
            z = policy_op[i,0]
        else:
            z = policy_op[i,1]
        if z == 0:
            m = 'o'
            color = 'red'
        else:
            m = '^'
            color = 'blue'
        ax.scatter(x,y,z,marker=m,color=color)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.savefig('policy_non_usable_ace_op.png')
    #value: player sum vs dealer card vs value for usable ace
    ax = fig.add_subplot(111, projection='3d')
    x = np.arange(12,22,1)
    y = np.arange(1,11,1)
    xx,yy = np.meshgrid(x,y)
    zz = np.zeros((10,10))
    for i in range(10):
        for j in range(10):
            zz[i,j] = value[100+i*10+j]
    ax.plot_wireframe(xx, yy, zz, rstride=1, cstride=1)
    plt.savefig('value_usable_ace_op.png')
    #value: player sum vs dealer card vs value for non usable ace
    ax = fig.add_subplot(111, projection='3d')
    x = np.arange(12,22,1)
    y = np.arange(1,11,1)
    xx,yy = np.meshgrid(x,y)
    zz = np.zeros((10,10))
    for i in range(10):
        for j in range(10):
            zz[i,j] = value[i*10+j]
    ax.plot_wireframe(xx, yy, zz, rstride=1, cstride=1)
    plt.savefig('value_non_usable_ace_op.png')


def main():
    monte_carlo_es(MC_ES_ITERATIONS)
    print_result_es()
    monte_carlo_op(MC_OP_ITERATIONS)
    print_result_op()


main()
