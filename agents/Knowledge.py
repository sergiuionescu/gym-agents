from collections import OrderedDict


class Knowledge(object):
    behaviour = {}
    cursor = 0

    def add_behaviour(self, behaviour, weight):
        if behaviour in self.behaviour:
            self.behaviour[behaviour] += weight
        else:
            self.behaviour[behaviour] = weight
        self.behaviour = OrderedDict(sorted(self.behaviour.items(), key=lambda x: x[1], reverse=True))

    def replace_behaviour(self, behaviour):
        """

        :type behaviour: OrderedDict
        """
        self.behaviour = self.behaviour = OrderedDict(sorted(behaviour.items(), key=lambda x: x[1], reverse=True))