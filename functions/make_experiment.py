import numpy as np
from functions.confidence_bounds import bootstrap_ci
from functions.evaluate_policy import evaluate_policy
from functions.plot_from_dataset import plot_data
from classes.MDP import MDP
from classes.Greedy_policy import Greedy_policy
from classes.My_policy import My_policy
import matplotlib.pyplot as plt

def make_experiment(seeds=1):

    print('###################################')
    print('Performing the experiment with {} random seeds'.format(seeds))
    print('###################################')


    env = MDP()
    my_policy = My_policy()
    greedy_policy = Greedy_policy()

    my_results = evaluate_policy(my_policy, env, seeds=seeds)
    env.plot_monthly_energy_profiles('my')
    greedy_results = evaluate_policy(greedy_policy, env, seeds=seeds)
    env.plot_monthly_energy_profiles('greedy')
    my_low, my_high = bootstrap_ci(my_results)
    greedy_low, greedy_high = bootstrap_ci(greedy_results)


    # make plot
    plot_data(np.arange(0,len(greedy_low)), greedy_low, greedy_high, col='C1', label='My policy')
    plot_data(np.arange(0,len(my_low)), my_low, my_high, col='C0', label='Greedy policy')

    plt.legend()
    plt.savefig('figures/policy_performance.pdf')

