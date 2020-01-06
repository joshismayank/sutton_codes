import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#constants
RENTAL_EARNING = 10
MOVE_COST = 2
MAX_CARS = 20
MAX_MOVE = 5
DISCOUNT = 0.9
LAMBDA_1_RENT = 3
LAMBDA_2_RENT = 4
LAMBDA_1_RETURN = 3
LAMBDA_2_RETURN = 2
ACCEPTABLE_ERROR = 1e-2


#20X20 array for value function: gives value/earning for this state
values = np.random.random((MAX_CARS+1,MAX_CARS+1))
#20X20 aray for policy
policy = np.random.randint(11,size=(MAX_CARS+1,MAX_CARS+1))


def calc_poisson(lam,n):
    val = math.exp(lam*-1)
    val = val * (lam**n)
    val = val/(math.factorial(n))
    return val


def calc_reward(location,rented,returned,new_i,new_j):
    reward = rented * RENTAL_EARNING
    reward = reward + DISCOUNT*values[new_i,new_j]
    if location == 1:
        prob = calc_poisson(LAMBDA_1_RENT,rented) * calc_poisson(LAMBDA_1_RETURN,returned)
    else:
        prob = calc_poisson(LAMBDA_2_RENT,rented) * calc_poisson(LAMBDA_2_RETURN,returned)
    reward = reward * prob
    return reward


def policy_valuation():
    print("policy_valuation")
    delta = 0
    iteration = 0
    while True:
        iteration = iteration + 1
        print("value_iteration: {}".format(iteration))
        for i in range(0,MAX_CARS):
            for j in range(0,MAX_CARS):
                #state (i,j)
                curr_val = values[i,j]
                curr_action = policy[i,j]
                curr_cars_i = i + curr_action
                curr_cars_j = j - curr_action
                if curr_cars_i < 0 or curr_cars_i > MAX_CARS:
                    continue
                if curr_cars_j < 0 or curr_cars_j > MAX_CARS:
                    continue
                #print("i: {}, j: {}, curr_action: {}".format(i,j,curr_action))
                #print("curr_cars: i {}, j {}".format(curr_cars_i,curr_cars_j))
                curr_reward = abs(curr_action)*MOVE_COST*-1
                for x_return in range(curr_cars_i,MAX_CARS+1):
                    for y_return in range(curr_cars_j,MAX_CARS+1):
                        return_x = x_return - curr_cars_i
                        curr_cars_x = x_return
                        return_y = y_return - curr_cars_j
                        curr_cars_y = y_return
                        #print("cars returned: i {}, j {}".format(return_x,return_y))
                        for x_rented in range(0,curr_cars_x+1):
                            for y_rented in range(0,curr_cars_y+1):
                                new_i = curr_cars_i - x_rented
                                new_j = curr_cars_j - y_rented
                                #print("cars rented: i {}, j {}".format(x_rented,y_rented))
                                #print("new state: i {}, j {}".format(new_i,new_j))
                                reward_x = calc_reward(1,x_rented,return_x,new_i,new_j)
                                reward_y = calc_reward(2,y_rented,return_y,new_i,new_j)
                                curr_reward = curr_reward + reward_x + reward_y
                #print("total reward: {}".format(curr_reward))
                delta = max(delta,abs(curr_val-curr_reward))
        if delta < ACCEPTABLE_ERROR:
            break
        if iteration > 9:
            break


def policy_improvement():
    print("policy_improvement")
    stable = True
    for i in range(0, MAX_CARS):
        for j in range(0, MAX_CARS):
            curr_action = policy[i,j]
            curr_val = values[i,j]
            max_val = curr_val
            max_action = curr_action
            #print("state: i {}, j {}, action {}".format(i,j,curr_action))
            for action in range(MAX_MOVE*-1,MAX_MOVE+1):
                if action > 0 and action > j:
                    continue
                if action > 0 and (action+i) > 20:
                    continue
                if action < 0 and action*-1 > i:
                    continue
                if action < 0 and (action*-1 + j) > 20:
                    continue
                curr_cars_i = i + action #=1
                curr_cars_j = j - action #=0
                #action = 1
                #print("action: {}, curr_cars: i {}, j {}".format(action,curr_cars_i,curr_cars_j))
                curr_reward = abs(action*MOVE_COST)*-1
                for x_return in range(curr_cars_i,MAX_CARS+1):
                    for y_return in range(curr_cars_j,MAX_CARS+1):
                        return_x = x_return - curr_cars_i #=-1
                        return_y = y_return - curr_cars_j #=1
                        curr_cars_x = curr_cars_i + return_x #=0
                        curr_cars_y = curr_cars_j + return_y #=1
                        #print("returned: i {}, j {}, curr_cars: i {}, j {}".format(return_x,return_y,curr_cars_x,curr_cars_y))
                        for x_rent in range(0,curr_cars_x+1):
                            for y_rent in range(0,curr_cars_y+1):
                                new_i = curr_cars_x - x_rent
                                new_j = curr_cars_y - y_rent
                                #print("cars_rented: i {}, j {}".format(x_rent,y_rent))
                                #print("new_state: i {}, j {}".format(new_i,new_j))
                                reward_x = calc_reward(1,x_rent,return_x,new_i,new_j)
                                reward_y = calc_reward(2,y_rent,return_y,new_i,new_j)
                                curr_reward = curr_reward + reward_x + reward_y
                #print("curr_reward: {}".format(curr_reward))
                val = curr_reward
                if val > curr_val:
                    max_action = action
                    max_val = val
            if max_action != curr_action:
                policy[i,j] = max_action
                stable = False
                return stable
    return stable


def policy_iteration():
    stable = False
    policy_iteration_no = 1
    while stable is False and policy_iteration_no < 80:
        print("policy_iteration_no: {}".format(policy_iteration_no))
        policy_valuation()
        stable = policy_improvement()
        policy_iteration_no = policy_iteration_no + 1

 
def main():
    for i in range(0,20):
        for j in range(0,20):
            policy[i,j] = policy[i,j] - 5
    policy_iteration()
    print("policy_iteration complete")
    x = np.arange(0,MAX_CARS,1)
    xx = np.meshgrid(x,x)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(xx,xx,values)
    plt.savefig('values.png')
    ax.plot_surface(xx,xx,policy)
    plt.savefig('policy.png')


main()
