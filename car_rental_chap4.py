import numpy as np
import math

#20X20 array for value function: gives value/earning for this state
values = np.random.random((20,20))
#20X20 aray for policy
policy = np.random.randint(10,size=(20,20))

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


def calc_poisson(lam,n):
    val = math.exp(lam*-1)
    val = val * (lam**n)
    val = val/(math.factorial(n))
    return val


def calc_reward(location,rented,returned,new_i,new_j):
    reward = rented * RENTAL_EARNING
    reward = reward + DISCOUNT*values[new_i,new_j]
    if location == 1:
        prob = calc_poisson(LAMDA_1_RENT,rented) * calc_poisson(LAMDA_1_RETURN,returned)
    else:
        prob = calc_poisson(LAMDA_2_RENT,rented) * calc_poisson(LAMDA_2_RETURN,returned)
    reward = reward * prob
    return reward


def policy_iteration():
    #policy valuation
    delta = 0
    iteration = 0
    while True:
        iteration = iteration + 1
        for i in range(0,MAX_CARS):
            for j in range(0,MAX_CARS):
                #state (i,j)
                curr_val = values[i,j]
                curr_action = policy[i,j]
                curr_cars_i = i + curr_action
                curr_cars_j = j - curr_action
                curr_reward = abs(curr_action)*MOVE_COST*-1
                for x_return in range(curr_cars_i,MAX_CARS+1):
                    for y_return in range(curr_cars_j,MAX_CARS+1):
                        return_x = x_return - curr_cars_x
                        curr_cars_x = curr_cars_x + x_return
                        return_y = y_return - curr_cars_y
                        curr_cars_y = curr_cars_y + y_return
                        for x_rented in range(0,curr_cars_x+1):
                            for y_rented in range(0,curr_cars_y+1):
                                new_i = curr_cars_x - x_rented
                                new_j = curr_cars_y - y_rented
                                reward_x = calc_reward(1,x_rented,x_return,new_i,new_j)
                                reward_y = calc_reward(2,y_rented,y_return,new_i,new_j)
                                curr_reward = curr_reward + reward_x + reward_y
                delta = max(delta,abs(curr_val-curr_reward))
        if delta < ACCEPTABLE_ERROR:
            break
        if iteration > 9:
            break
    #do policy improvement

 
def main():
    for i in range(0,20):
        for j in range(0,20):
            policy[i,j] = policy[i,j] - 10
    policy_iteration()
