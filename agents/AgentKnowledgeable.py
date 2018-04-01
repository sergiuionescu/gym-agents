import numpy as np
import tensorflow as tf

from agents.Agent import Agent


class AgentKnowledgeable(Agent):
    latest_observation = 0
    current_prediction = []
    name = ''
    session = None
    last_reward = 0
    initial_learning_rate = 0.1
    behaviour = []

    def __init__(self, experience, knowledge, space, observation):
        self.space = space
        self.experience = experience
        self.knowledge = knowledge
        self.prediction(observation)

    def reset_behaviour(self, observation):
        pass

    def sleep(self):
        pass

    def set_session(self, session):
        pass

    def prediction(self, observation):
        if self.knowledge.get_information(observation):
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

        self.behaviour = list(behaviour)

    def random_prediction(self):
        self.behaviour = []
        for dimension in self.space.spaces:
            self.behaviour.append(np.random.randint(0, dimension.n))

    def act(self, ob):
        return self.behaviour

    def add_reward(self, observation, reward):
        information = self.knowledge.get_information(observation)
        information.add_behaviour(tuple(self.behaviour), reward)

        self.knowledge.add_information(observation, information)
        if reward <= 0:
            self.prediction(observation)
        self.last_reward = reward

        self.experience.add_reward(reward)
        self.experience.success += reward > 0
        self.experience.total_success += reward > 0

    def get_learning_rate(self):
        success_rate = self.experience.get_avg_success_rate()
        return success_rate if success_rate > 0 else self.initial_learning_rate
