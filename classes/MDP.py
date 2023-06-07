from classes.state import state

class MDP:
    def __init__(self):
        self.s = state()
        self.s.make_initial()

    def step(self, action):
        An = action[0]
        Ab = action[1]

        self.s.step(An, Ab)
        self.s.print()