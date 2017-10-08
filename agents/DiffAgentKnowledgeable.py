import numpy as np

from agents import DiffAgentBase


class DiffAgentKnowledgeable(DiffAgentBase):
    last_reward = 0

    def prediction(self):
        try:
            if self.behaviour:
                behaviour = list(self.behaviour.next()[0])
                self.diff = list(behaviour[0])
                self.noise_reduction = list(behaviour[1])
                return
        except StopIteration:
            self.behaviour = self.knowledge.behaviour.iteritems()
        self.random_prediction()

    def random_prediction(self):
        self.diff = []
        self.noise_reduction = []
        for dimension in self.space.spaces:
            self.diff.append(np.random.randint(0, dimension.n))
            self.noise_reduction.append(np.random.randint(2))

    def act(self, ob):
        self.latest_observation = ob
        self.current_prediction = []
        key = 0
        for dimension in self.space.spaces:
            self.current_prediction.append((self.diff[key] + ob * self.noise_reduction[key]) % dimension.n)
            key += 1

        return self.current_prediction

    def add_reward(self, reward):
        if reward > self.last_reward and reward > 0:
            self.knowledge.add_behaviour(tuple([tuple(self.diff), tuple(self.noise_reduction)]), 1)
            if not self.behaviour:
                self.behaviour = self.knowledge.behaviour.iteritems()
            self.last_reward = reward

        self.last_reward = reward
        if reward < 0:
            self.prediction()

        self.experience.add_reward(reward)
        self.experience.success += reward > 0
        self.experience.total_success += reward > 0


