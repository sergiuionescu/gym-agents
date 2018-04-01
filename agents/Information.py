from collections import OrderedDict


class Information(object):
    behaviour = {}
    cursor = 0

    def add_behaviour(self, behaviour, reward):
        if behaviour in self.behaviour:
            self.behaviour[behaviour] += reward
        else:
            self.behaviour[behaviour] = reward + 100

    def show_top_behaviour(self):
        top_behaviour = OrderedDict(sorted(self.behaviour.items(), key=lambda x: x[1], reverse=True))
        limit = 3
        for key, value in top_behaviour.items():
            print("Action:" + str(key) + " Score:" + str(value))
            limit -= 1
            if limit == 0:
                break
