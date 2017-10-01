import numpy as np


class DiffAgentSpeculative(object):
    diff = []
    prediction = []
    name = ''

    def __init__(self, agent_experience, space):

        self.space = space
        self.experience = agent_experience
        self.random_prediction()

    def random_prediction(self):
        self.diff = np.random.randint(0, self.space.spaces[2].n)

    def act(self, ob):
        self.prediction = (self.diff + ob) % self.space.spaces[2].n

        a = [1, 1, self.prediction]
        return a

    def add_reward(self, reward):
        self.experience.add_reward(reward)
        self.experience.success += reward > 0
        self.experience.total_success += reward > 0