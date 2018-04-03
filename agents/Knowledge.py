from agents.Information import Information


class Knowledge(object):

    def __init__(self):
        self.knowledge = {}

    def add_information(self, observation, information):
        self.knowledge[observation] = information

    def get_information(self, observation) -> Information:
        if observation in self.knowledge.keys():
            return self.knowledge[observation]
        else:
            return Information()

    def show_summary(self):
        for key in self.knowledge:
            print('***' + str(key) + '***')
            self.knowledge[key].show_top_behaviour()

    def __add__(self, other):
        knowledge = Knowledge()

        for i in self.knowledge:
            knowledge.add_information(i, self.knowledge[i] + other.get_information(i))

        return knowledge
