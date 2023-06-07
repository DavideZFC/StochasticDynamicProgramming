import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

YEAR = 365

def generate_weather_curve():
    xy = np.loadtxt('data/weather.txt')

    x = xy[:,0]
    y = xy[:,1]

    f_cubic = interp1d(x, y, kind='cubic')

    xnew = np.linspace(0, YEAR, YEAR)
    return f_cubic(xnew)/100
