import numpy as np
import tensorflow as tf

from agents import DiffAgentBase


class DiffAgentKnowledgeable(DiffAgentBase.DiffAgentBase):
    last_reward = 0
    previous_diff = []
    reward_streak = 0
    initial_learning_rate = 0.1

    def prediction(self, observation):
        if self.behaviour:
            learning_rate = self.get_learning_rate()
            elems = tf.convert_to_tensor([0, 1])
            samples = tf.multinomial(tf.log([[learning_rate, 1 - learning_rate]]), 1)
            explore = elems[tf.cast(samples[0][0], tf.int32)].eval(session=self.session)

            if explore:
                self.random_prediction()
                return

            self.random_distribution_behaviour(observation)
            return
        self.random_prediction()

    def random_distribution_behaviour(self, observation):
        information = self.knowledge.get_information(observation)
        elems = tf.convert_to_tensor(list(information.behaviour.keys()))
        samples = tf.multinomial(tf.log([list(information.behaviour.values())]), 1)

        behaviour = elems[tf.cast(samples[0][0], tf.int32)].eval(session=self.session)

        self.diff = list(behaviour[0])
        self.noise_reduction = list(behaviour[1])

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

    def add_reward(self, observation, reward):
        if self.diff == self.previous_diff and reward > 0:
            self.reward_streak += 1
            perceived_reward = 10 * reward
        else:
            self.reward_streak = 1
            perceived_reward = reward

        if reward == 0:
            perceived_reward = -1.0

        self.previous_diff = self.diff

        behaviour = tuple([tuple(self.diff), tuple(self.noise_reduction)])
        information = self.knowledge.get_information(observation)
        information.add_behaviour(behaviour, perceived_reward)

        self.knowledge.add_information(observation, information)
        if reward > 0:
            if reward > self.last_reward:
                if not self.behaviour:
                    self.reset(observation)
        else:
            self.prediction(observation)
        self.last_reward = reward

        self.experience.add_reward(reward)
        self.experience.success += reward > 0
        self.experience.total_success += reward > 0

    def get_learning_rate(self):
        success_rate = self.experience.get_avg_success_rate()
        return success_rate if success_rate > 0 else self.initial_learning_rate
