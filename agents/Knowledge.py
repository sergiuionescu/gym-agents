from collections import OrderedDict


class Knowledge(object):
    behaviour = {}
    cursor = 0

    def add_behaviour(self, behaviour, reaward):
        if behaviour in self.behaviour:
            self.behaviour[behaviour] += reaward
        else:
            self.behaviour[behaviour] = reaward

    def show_top_behaviour(self):
        top_behaviour = OrderedDict(sorted(self.behaviour.items(), key=lambda x: x[1], reverse=True))
        max = 3
        for key, value in top_behaviour.items():
            print("Action:" + str(key) + " Score:" + str(value))
            max -= 1
            if (max == 0):
                break
