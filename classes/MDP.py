from classes.state import state
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve1d

YEAR = 365

class MDP:
    def __init__(self):
        self.s = state()
        self.s.make_initial()

        self.S_history = np.zeros(YEAR)
        self.W_history = np.zeros(YEAR)
        self.GAS_history = np.zeros(YEAR)
        self.D_history = np.zeros(YEAR)

    def reset(self):
        self.s.make_initial()

        self.S_history = np.zeros(YEAR)
        self.W_history = np.zeros(YEAR)
        self.GAS_history = np.zeros(YEAR)
        self.D_history = np.zeros(YEAR)
        

    def step(self, action):
        An = action[0]
        Ab = action[1]

        reward, S, W, Ab, D = self.s.step(An, Ab)

        t = self.s.t
        self.S_history[t] = S
        self.W_history[t] = W
        self.GAS_history[t] = Ab
        self.D_history[t] = D

        return reward

    def plot_energy_profiles(self,name):
        x = np.linspace(0,YEAR, YEAR)

        alpha = 0.5
        plt.fill_between(x, 0*self.GAS_history, self.GAS_history, color='blue', alpha=alpha, label='gas')
        plt.fill_between(x, self.GAS_history, self.S_history+self.GAS_history, color='yellow',  alpha=alpha, label='solar')
        plt.fill_between(x, self.S_history+self.GAS_history, self.S_history+self.GAS_history+self.W_history,  alpha=alpha, color='green', label='wind')
        plt.plot(x,self.D_history, color='red',  label='demand')

        plt.legend()
        plt.savefig('figures/{}profile.pdf'.format(name))
        plt.show()

    
    
    def plot_monthly_energy_profiles(self, name):
        x = np.linspace(0,YEAR, YEAR)

        v = np.ones(30)/30

        GAS_smooth = convolve1d(self.GAS_history, v, mode='wrap')
        S_smooth = convolve1d(self.S_history, v, mode='wrap')
        W_smooth = convolve1d(self.W_history, v, mode='wrap')
        D_smooth = convolve1d(self.D_history, v, mode='wrap')

        alpha = 0.5
        plt.fill_between(x, 0*GAS_smooth, GAS_smooth, color='blue', alpha=alpha, label='gas')
        plt.fill_between(x, GAS_smooth, S_smooth+GAS_smooth, color='yellow',  alpha=alpha, label='solar')
        plt.fill_between(x, S_smooth+GAS_smooth, S_smooth+GAS_smooth+W_smooth,  alpha=alpha, color='green', label='wind')
        plt.plot(x,D_smooth, color='red',  label='demand')

        plt.legend()
        plt.savefig('figures/{}profile.pdf'.format(name))
        plt.show()
        