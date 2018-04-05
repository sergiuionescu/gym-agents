import tensorflow as tf

from agents.Information import Information


class Knowledge(object):

    def __init__(self):
        self.knowledge = {}
        self.behaviour = {}

    def add_information(self, observation, information):
        self.knowledge[observation] = information

    def get_information(self, observation) -> Information:
        if observation not in self.knowledge.keys():
            self.knowledge[observation] = Information()
        return self.knowledge[observation]

    def show_summary(self):
        for key in self.knowledge:
            print('***' + str(key) + '***')
            self.knowledge[key].show_top_behaviour()

    def __add__(self, other):
        knowledge = Knowledge()

        for i in self.knowledge:
            knowledge.add_information(i, self.knowledge[i] + other.get_information(i))

        return knowledge

    def get_prediction(self, observation, sess):
        if observation not in self.behaviour:
            information = self.get_information(observation)
            if information.behaviour:
                elems = tf.convert_to_tensor(list(information.behaviour.keys()))
                samples = tf.multinomial(tf.log([list(information.behaviour.values())]), 1)

                self.behaviour[observation] = list(elems[tf.cast(samples[0][0], tf.int32)].eval(session=sess))
            else:
                return None

        return self.behaviour[observation]
