import numpy as np


class DiffAgent(object):
    diff = []
    prediction = []
    name = ''

    def __init__(self, agent_experience, space):

        self.space = space
        self.experience = agent_experience
        self.random_prediction()

    def random_prediction(self):
        self.diff = []
        for dimension in self.space.spaces:
            self.diff.append(np.random.randint(0, dimension.n))

    def act(self, ob):
        self.prediction = []
        key = 0
        for dimension in self.space.spaces:
            self.prediction.append((self.diff[key] + ob) % dimension.n)
            key += 1

        return self.prediction

    def add_reward(self, reward):
        self.experience.add_reward(reward)
        self.experience.success += reward > 0
        self.experience.total_success += reward > 0