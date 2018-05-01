class Quantifier(object):
    def __init__(self):
        self.behaviour = {}
        self.latest_observation = None
        self.latest_behaviour = None

    def add(self, observation, behaviour):
        self.behaviour[observation] = behaviour
        self.latest_observation = observation
        self.latest_behaviour = behaviour

    def adjust_reward(self, found, knowledge):
        for observation in self.behaviour:
            behaviour = self.behaviour[observation]
            information = knowledge.get_information(observation)
            if found:
                information.adjust_behaviour(behaviour, 2)
            else:
                information.adjust_behaviour(behaviour, 0.9)
            return

        self.adjust_latest_behaviour(found, knowledge)

    def adjust_latest_behaviour(self, found, knowledge):
        if not found and self.latest_behaviour:
            behaviour = self.behaviour[self.latest_observation]
            information = knowledge.get_information(self.latest_behaviour)
            information.adjust_behaviour(behaviour, 0.5)

