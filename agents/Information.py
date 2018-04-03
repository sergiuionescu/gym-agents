from collections import OrderedDict


class Information(object):
    def __init__(self):
        self.behaviour = {}

    def add_behaviour(self, behaviour, reward):
        if behaviour in self.behaviour:
            self.behaviour[behaviour] += reward
        else:
            self.behaviour[behaviour] = reward + 100

    def show_top_behaviour(self):
        top_behaviour = OrderedDict(sorted(self.behaviour.items(), key=lambda x: x[1], reverse=True))
        limit = 2
        for key, value in top_behaviour.items():
            print("Action:" + str(key) + " Score:" + str(value))
            limit -= 1
            if limit == 0:
                break

    def __add__(self, other):
        information = Information()

        for i in self.behaviour:
            information.add_behaviour(i, self.behaviour[i])

        for i in other.behaviour:
            information.add_behaviour(i, other.behaviour[i])

        return information