from agents.Information import Information


class Knowledge(object):
    knowledge = {}

    def add_information(self, observation, information):
        self.knowledge[observation] = information

    def get_information(self, observation) -> Information:
        return self.knowledge[observation] if observation in self.knowledge else Information()

    def show_summary(self):
        for key in self.knowledge:
            print('***' + str(key) + '***')
            self.knowledge[key].show_top_behaviour()
