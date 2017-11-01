class DiffAgentBase(object):
    diff = []
    noise_reduction = []
    latest_observation = 0
    current_prediction = []
    name = ''
    behaviour = None
    working_behaviour_size = 2

    def __init__(self, experience, knowledge, space):

        self.space = space
        self.experience = experience
        self.knowledge = knowledge
        self.prediction()

    def reset_behaviour(self):

        total_score = 0
        count = 0
        if len(self.knowledge.behaviour) > 0:
            for b, score in self.knowledge.behaviour.iteritems():
                total_score += score
            average_score = total_score / len(self.knowledge.behaviour)
            new_behaviour = {}
            for b, score in self.knowledge.behaviour.iteritems():
                count += 1;
                if score >= average_score or count <= self.working_behaviour_size:
                    new_behaviour[b] = score
            self.behaviour = new_behaviour.iteritems()

        #    self.behaviour = self.knowledge.behaviour.iteritems()

    def sleep(self):
        self.behaviour = None