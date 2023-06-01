import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

YEAR = 365



def generate_temperature_curve(tip):

    if tip == 'hot':
        xy = np.loadtxt('data/temp_hot.txt')
    else:
        xy = np.loadtxt('data/temp_cold.txt')

    x = xy[:,0]
    y = xy[:,1]

    f_cubic = interp1d(x, y, kind='cubic')

    xnew = np.linspace(0, YEAR, YEAR)
    return f_cubic(xnew)

