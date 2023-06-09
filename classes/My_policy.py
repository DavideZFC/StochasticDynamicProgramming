import numpy as np

class My_policy:
    def __init__(self):
        pass

    def act(self, state):
        d = state.d
        E = state.predict_next()

        return [d-E, d-E]