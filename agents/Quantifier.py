class Quantifier(object):
    def __init__(self):
        self.behaviour = {}

    def adjust_reward(self, found, knowledge):
        for observation in self.behaviour:
            behaviour = self.behaviour[observation]
            information = knowledge.get_information(observation)
            if found:
                information.adjust_behaviour(behaviour, 2)
            else:
                information.adjust_behaviour(behaviour, 0.9)
