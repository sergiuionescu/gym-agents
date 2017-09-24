import numpy as np


class SpeculativeDiffAgent(object):
    def __init__(self, space):
        self.space = space
        self.diff = 0
        self.prediction = 0
        self.total_reward = 0
        self.random_prediction()
        self.name = ''

    def random_prediction(self):
        self.diff = np.random.randint(0, self.space.spaces[2].n)

    def act(self, ob):
        self.prediction = (self.diff + ob) % self.space.spaces[2].n

        a = [1, 1, self.prediction]
        return a
