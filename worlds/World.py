import os
import random
import _pickle as pickle

from agents.DiffAgentSpeculative import DiffAgentSpeculative
from agents.DiffAgent import DiffAgent
from agents.DiffAgentKnowledgeable import DiffAgentKnowledgeable
from agents.Experience import Experience
from agents.Knowledge import Knowledge


class World(object):
    def __init__(self, environment, agent_class):
        self.population = {}
        self.environment = environment
        self.agent_class = agent_class

        with open(os.path.join('data', 'worlds.txt'), 'r') as f:
            data = f.readline()
            names = data.split(',')
            self.name = random.choice(names)

        with open(os.path.join('data', 'people.txt')) as f:
            self.names = map(lambda s: s.strip(), f.readlines())

    def get_agent(self, action_space, observation):
        next_agent = self.birth(action_space, observation)

        return next_agent

    def birth(self, action_space, observation):
        knowledge = Knowledge()
        experience = Experience()

        class_map = {"DiffAgentSpeculative": DiffAgentSpeculative, "DiffAgent": DiffAgent,
                     "DiffAgentKnowledgeable": DiffAgentKnowledgeable}
        agent = class_map[self.agent_class](experience, knowledge, action_space, observation)
        agent.name = random.choice(list(self.names))
        self.population[self.population.__len__()] = agent

        return agent

    def wake(self, name, observation):
        if name:
            self.name = name
            path = self.get_path()
            if os.path.exists(path):
                agent_paths = os.listdir(path)
                agent_paths.sort(reverse=True)
                for agent_path in agent_paths:
                    agent = pickle.load(open(os.path.join(path, agent_path), 'rb'))
                    agent.reset_behaviour(observation)
                    self.population[self.population.__len__()] = agent

    def sleep(self):
        path = self.get_path()
        if not os.path.exists(path):
            os.makedirs(path)

        for key, agent in self.population.items():
            agent.sleep()
            pickle.dump(agent, open(os.path.join(path, agent.name + '.pcl'), 'wb'))

    def get_path(self):
        return os.path.join('rem', self.environment, self.name)
