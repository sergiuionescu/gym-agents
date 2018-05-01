from agents.Agent import Agent


class DiffAgentBase(Agent):
    diff = []
    noise_reduction = []
    latest_observation = 0
    current_prediction = []
    name = ''
    behaviour = None
    working_behaviour_size = 2
    session = None

    def __init__(self, experience, knowledge, space, observation):

        self.space = space
        self.experience = experience
        self.knowledge = knowledge
        self.prediction(observation)

    def reset(self, found):

        total_score = 0
        count = 0
        information = self.knowledge.get_information(found)
        if len(information.behaviour) > 0:
            for b, score in information.behaviour.items():
                total_score += score
            average_score = total_score / len(information.behaviour)
            new_behaviour = {}
            for b, score in information.behaviour.items():
                count += 1
                if score >= average_score or count <= self.working_behaviour_size:
                    new_behaviour[b] = score
                else:
                    break
            self.behaviour = new_behaviour.items()

    def sleep(self):
        self.behaviour = None
        self.session = None

    def set_session(self, session):
        self.session = session
