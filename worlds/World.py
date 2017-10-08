import os
import random
import cPickle as pickle

from agents import DiffAgentSpeculative
from agents import DiffAgent
from agents import DiffAgentKnowledgeable
from agents import Experience
from agents import Knowledge


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

    def get_agent(self, agent_position, action_space):
        next_agent = self.population[agent_position] if agent_position in self.population else self.birth(action_space)

        return next_agent

    def birth(self, action_space):
        knowledge = Knowledge()
        experience = Experience()

        class_map = {"DiffAgentSpeculative": DiffAgentSpeculative, "DiffAgent": DiffAgent, "DiffAgentKnowledgeable": DiffAgentKnowledgeable}
        agent = class_map[self.agent_class](experience, knowledge, action_space)
        agent.name = random.choice(self.names)
        self.population[self.population.__len__()] = agent

        return agent

    def wake(self, name):
        if name:
            self.name = name
            path = self.get_path()
            if os.path.exists(path):
                agent_paths = os.listdir(path)
                agent_paths.sort(reverse=True)
                for agent_path in agent_paths:
                    agent = pickle.load(open(os.path.join(path, agent_path), 'r'))
                    agent.wake()
                    self.population[self.population.__len__()] = agent

    def sleep(self):
        path = self.get_path()
        if not os.path.exists(path):
            os.makedirs(path)

        for key, agent in self.population.items():
            agent.sleep()
            pickle.dump(agent,
                        open(os.path.join(path, str(agent.experience.total_reward) + '.' + agent.name + '.pcl'), 'w'))

    def get_path(self):
        return os.path.join('rem', self.environment, self.name)
