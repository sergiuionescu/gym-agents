import numpy as np

from agents import DiffAgentBase


class DiffAgent(DiffAgentBase.DiffAgentBase):

    def prediction(self):
        self.diff = []
        self.noise_reduction = []
        for dimension in self.space.spaces:
            self.diff.append(np.random.randint(0, dimension.n))
            self.noise_reduction.append(np.random.randint(2))

    def act(self, ob):
        self.current_prediction = []
        key = 0
        for dimension in self.space.spaces:
            self.current_prediction.append((self.diff[key] + ob * self.noise_reduction[key]) % dimension.n)
            key += 1

        return self.current_prediction

    def add_reward(self, observation, reward):
        if reward <= 0:
            self.prediction()

        self.experience.add_reward(observation, reward)
        self.experience.success += reward > 0
        self.experience.total_success += reward > 0