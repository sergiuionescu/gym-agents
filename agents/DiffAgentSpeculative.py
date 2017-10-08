import numpy as np

from agents import DiffAgentBase


class DiffAgentSpeculative(DiffAgentBase):

    def prediction(self):
        self.diff = np.random.randint(0, self.space.spaces[2].n)

    def act(self, ob):
        self.current_prediction = (self.diff + ob) % self.space.spaces[2].n

        a = [1, 1, self.current_prediction]
        return a

    def add_reward(self, reward):
        if reward <= 0:
            self.prediction()

        self.experience.add_reward(reward)
        self.experience.success += reward > 0
        self.experience.total_success += reward > 0