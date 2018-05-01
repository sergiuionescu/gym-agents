import tensorflow as tf

from agents.Agent import Agent
from agents.Experience import Experience
from agents.PositiveBoostPerception import PositiveBoostPerception
from agents.Quantifier import Quantifier


class AgentKnowledgeable(Agent):
    latest_observation = 0
    current_prediction = []
    name = ''
    session = None
    initial_learning_rate = 0.5
    behaviour = []

    def __init__(self, experience, knowledge, space, observation):
        self.space = space
        self.experience = experience
        self.knowledge = knowledge
        self.prediction(observation)
        self.quantifier = Quantifier()

    def reset(self, found):
        self.quantifier.adjust_reward(found, self.knowledge)
        self.quantifier = Quantifier()

    def sleep(self):
        self.experience = Experience()

    def set_session(self, session):
        pass

    def prediction(self, observation):
        self.behaviour = None
        if self.knowledge.get_information(observation):
            learning_rate = self.get_learning_rate()
            elems = tf.convert_to_tensor([0, 1])
            samples = tf.multinomial(tf.log([[learning_rate, 1 - learning_rate]]), 1)
            explore = elems[tf.cast(samples[0][0], tf.int32)].eval(session=self.session)

            if not explore:
                self.behaviour = self.knowledge.get_prediction(observation, self.session)

        if not self.behaviour:
            self.behaviour = self.random_prediction()

        return self.behaviour

    def random_prediction(self):
        return self.space.sample()

    def act(self, ob):
        return self.prediction(PositiveBoostPerception.get_perceived_observation(ob))

    def add_reward(self, observation, reward):
        observation, reward = PositiveBoostPerception.get_perceived_reward(observation, reward)
        information = self.knowledge.get_information(observation)
        information.add_behaviour(tuple(self.behaviour), reward)

        self.knowledge.add_information(observation, information)
        self.quantifier.add(observation, tuple(self.behaviour))
        if reward <= 0:
            self.knowledge.behaviour.pop(observation, None)

        self.experience.add_reward(reward)
        self.experience.success += reward > 0
        self.experience.total_success += reward > 0

    def get_learning_rate(self):
        success_rate = self.experience.get_avg_success_rate()
        return success_rate + self.initial_learning_rate
