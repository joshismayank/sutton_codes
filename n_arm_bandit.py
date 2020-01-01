import numpy as np
import matplotlib.pyplot as plt

#datastructures - greedy_bandit_rewards[10]: avg total rewards received till now for each bandit
#                 greedy_bandit_counts[10]: counts of bandits used
#                 epsi_bandit_rewards[10]: --same--
#                 epsi_bandit_counts[10]: --same--
#                 actual_tot_reward[2000], greedy_tot_reward[2000], epsi_tot_reward[2000]

actual_total_reward = None
greedy_total_reward = None
epsi_greedy_total_reward = None
greedy_bandit_avg_rewards = np.zeros(10)
greedy_bandit_counts = np.zeros(10)
epsi_greedy_bandit_avg_rewards = np.zeros(10)
epsi_greedy_bandit_counts = np.zeros(10)
curr_actual_rewards = np.zeros(10)


def get_actual_reward(iteration):
    global actual_total_reward
    global curr_actual_rewards
    curr_actual_rewards = np.random.rand(10)
    reward = np.max(curr_actual_rewards)
    if iteration > 0:
        actual_total_reward[iteration] = reward + actual_total_reward[iteration-1]
    else:
        actual_total_reward[iteration] = reward


def get_greedy_reward(iteration):
    global greedy_bandit_avg_rewards
    global curr_actual_rewards
    global greedy_bandit_counts
    global greedy_total_reward
    bandit = np.argmax(greedy_bandit_avg_rewards)
    if greedy_bandit_avg_rewards[bandit] == 0:
        bandit = np.random.choice(10)
    reward = curr_actual_rewards[bandit]
    temp_reward = greedy_bandit_avg_rewards[bandit]
    temp_count = greedy_bandit_counts[bandit]
    greedy_bandit_avg_rewards[bandit] = ((temp_reward * temp_count) + reward)/(temp_count+1)
    greedy_bandit_counts[bandit] = temp_count+1
    if iteration > 0:
        greedy_total_reward[iteration] = reward + greedy_total_reward[iteration-1]
    else:
        greedy_total_reward[iteration] = reward


def get_epsi_greedy_reward(iteration,epsi):
    global epsi_greedy_bandit_avg_rewards
    global epsi_greedy_bandit_counts
    global curr_actual_rewards
    global epsi_greedy_total_reward
    if np.random.rand() < epsi:
        bandit = np.random.choice(10)
    else:
        bandit = np.argmax(epsi_greedy_bandit_avg_rewards)
    reward = curr_actual_rewards[bandit]
    temp_reward = epsi_greedy_bandit_avg_rewards[bandit]
    temp_count = epsi_greedy_bandit_counts[bandit]
    epsi_greedy_bandit_avg_rewards[bandit] = ((temp_reward * temp_count) + reward)/(temp_count+1)
    epsi_greedy_bandit_counts[bandit] = temp_count + 1
    if iteration > 0:
        epsi_greedy_total_reward[iteration] = reward + epsi_greedy_total_reward[iteration-1]
    else:
        epsi_greedy_total_reward[iteration] = reward


def plot_graphs():
    global actual_total_reward
    global greedy_total_reward
    global epsi_greedy_total_reward
    x = np.arange(1,2001)
    greedy_y = greedy_total_reward/actual_total_reward
    epsi_greedy_y = epsi_greedy_total_reward/actual_total_reward
    plt.plot(x, greedy_y, label="greedy")
    plt.plot(x, epsi_greedy_y, label="epsilon-greedy")
    plt.legend(loc="upper right")
    plt.show()


def main():
    iterations = 2000
    epsi = 0.1
    global actual_total_reward
    global greedy_total_reward
    global epsi_greedy_total_reward
    actual_total_reward = np.zeros(iterations)
    greedy_total_reward = np.zeros(iterations)
    epsi_greedy_total_reward = np.zeros(iterations)

    for i in range (iterations):
        get_actual_reward(i)
        get_greedy_reward(i)
        get_epsi_greedy_reward(i,epsi)

    plot_graphs()

if __name__ == "__main__":
    main()
