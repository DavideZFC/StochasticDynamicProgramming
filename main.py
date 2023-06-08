import numpy as np
import yaml
from classes.MDP import MDP

env = MDP()
for t in range(364):
    env.step([0,0])

env.plot_energy_profiles()