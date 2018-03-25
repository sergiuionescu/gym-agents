class DiffAgentBase(object):
    diff = []
    noise_reduction = []
    latest_observation = 0
    current_prediction = []
    name = ''
    behaviour = None
    working_behaviour_size = 2
    session = None

    def __init__(self, experience, knowledge, space):

        self.space = space
        self.experience = experience
        self.knowledge = knowledge
        self.prediction()

    def reset_behaviour(self):

        total_score = 0
        count = 0
        if len(self.knowledge.behaviour) > 0:
            for b, score in self.knowledge.behaviour.items():
                total_score += score
            average_score = total_score / len(self.knowledge.behaviour)
            new_behaviour = {}
            for b, score in self.knowledge.behaviour.items():
                count += 1;
                if score >= average_score or count <= self.working_behaviour_size:
                    new_behaviour[b] = score
                else:
                    break
            self.behaviour = new_behaviour.items()

        #    self.behaviour = self.knowledge.behaviour.iteritems()

    def sleep(self):
        self.behaviour = None
        self.session = None

    def set_session(self, session):
        self.session = session
