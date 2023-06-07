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

        
    def step(self, An, Ab):
        # make one transition in the system

        if (Ab > self.R):
            # this action is unfeasible, we have to clip it
            Ab = self.R

        # transition of time
        self.t += 1

        # transition of temperature
        lam = self.config['solar']['lam']
        Thot = self.temperature_hot[self.t]
        Tcold = self.temperature_cold[self.t]
        self.T = lam*self.T + (1-lam)*np.random.uniform(Tcold, Thot)

        # transition of weather
        p = lam*self.C + (1-lam)*(1-self.weather[self.t])
        self.C = np.random.binomial(n=1, p=p)

        # transition of reserve
        self.R = min(self.R - Ab, self.config['reserve']['sr']) + An

    def print(self):
        # print all current values in the state
        print('day: {}, temperature: {}, clouds: {}, reserve: {}'.format(self.t, self.T, self.C, self.R))
        
