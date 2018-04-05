import numpy as np

from . import DiffAgentBase


class DiffAgentSpeculative(DiffAgentBase.DiffAgentBase):

    def prediction(self, observation):
        self.diff = np.random.randint(0, self.space.spaces[2].n)

    def act(self, ob):
        self.current_prediction = (self.diff + ob) % self.space.spaces[2].n

        a = [1, 1, self.current_prediction]
        return a

    def add_reward(self, observation,  reward):
        if reward <= 0:
            self.prediction()

        self.experience.add_reward(observation, reward)
        self.experience.success += reward > 0
        self.experience.total_success += reward > 0
