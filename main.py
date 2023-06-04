import numpy as np
import yaml


with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

exp_values = config['exp_values']
print(exp_values)