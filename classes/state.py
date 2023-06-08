import numpy as np
import yaml
from functions.generate_temperature_curve import generate_temperature_curve
from functions.generate_weather_curve import generate_weather_curve


class state:
    def __init__(self):
        # initialize to zero all variables

        self.t = 0
        self.T = 0
        self.C = 0
        self.R = 0

        with open('classes\config.yml', 'r') as file:
            self.config = yaml.safe_load(file)


    def make_initial(self, T0=45, C=1, R=0):
        # command to specify the initial state of the system.
        # default are standard values

        self.T = T0
        self.C = C
        self.R = R

        self.temperature_hot = generate_temperature_curve('hot')
        self.temperature_cold = generate_temperature_curve('cold')
        self.weather = generate_weather_curve()

        self.d = self.config['demand']['d']
        self.sigma = self.config['demand']['sigma'] 
        self.lam = self.config['solar']['lam']   
        self.gs = self.config['solar']['gs']
        self.gc = self.config['solar']['gc']
        self.w = self.config['wind']['w']
        self.ps = self.config['wind']['ps']
        self.pc = self.config['wind']['pc']
        self.cg = self.config['gas']['cg']
        self.sr = self.config['reserve']['sr']
        self.cr = self.config['reserve']['cr']
        self.ce = self.config['electric']['ce']
        self.pe = self.config['electric']['pe']

        
    def step(self, An, Ab):
        # make one transition in the system

        if (Ab > self.R):
            # this action is unfeasible, we have to clip it
            Ab = self.R

        # sample the demand for the current day
        D = np.random.normal(self.d,self.sigma)

        # compute solar energy
        S = self.gs*self.T if self.C == 0 else self.gc*self.T

        # compute wind energy
        p = self.ps if self.C == 0 else self.pc
        W = self.w*np.random.binomial(1,p)

        # compute the three components of the reward
        reward1 = -An*self.cg
        E = W + S + Ab

        reward2 = -self.sr*self.R

        if D > E:
            reward3 = -(D-E)*self.ce
        else:
            reward3 = (E-D)*self.pe
        
        reward = reward1 + reward2 + reward3


        # transition of time
        self.t += 1

        # transition of temperature
        Thot = self.temperature_hot[self.t]
        Tcold = self.temperature_cold[self.t]
        self.T = self.lam*self.T + (1-self.lam)*np.random.uniform(Tcold, Thot)

        # transition of weather
        p = self.lam*self.C + (1-self.lam)*(1-self.weather[self.t])
        self.C = np.random.binomial(n=1, p=p)

        # transition of reserve
        self.R = min(self.R - Ab, self.cr) + An

        return reward, S, W, Ab, D

    def print(self):
        # print all current values in the state
        print('day: {}, temperature: {}, clouds: {}, reserve: {}'.format(self.t, self.T, self.C, self.R))
        
