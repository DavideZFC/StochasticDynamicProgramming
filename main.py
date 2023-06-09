import numpy as np
import yaml
from classes.MDP import MDP
from classes.Greedy_policy import Greedy_policy
from classes.My_policy import My_policy

env = MDP()
policy = My_policy()

for t in range(364):
    action = policy.act(env.s)
    env.step(action)

env.plot_energy_profiles()
env.plot_monthly_energy_profiles()