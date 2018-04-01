import os
import random
import _pickle as pickle

from agents.DiffAgentSpeculative import DiffAgentSpeculative
from agents.DiffAgent import DiffAgent
from agents.DiffAgentKnowledgeable import DiffAgentKnowledgeable
from agents.AgentKnowledgeable import AgentKnowledgeable
from agents.Experience import Experience
from agents.Knowledge import Knowledge


class World(object):
    def __init__(self, environment, agent_class, name):
        self.population = {}
        self.environment = environment
        self.agent_class = agent_class
        self.name = name

        if not name:
            with open(os.path.join('data', 'worlds.txt'), 'r') as f:
                data = f.readline()
                names = data.split(',')
                self.name = random.choice(names)

        with open(os.path.join('data', 'people.txt')) as f:
            self.names = map(lambda s: s.strip(), f.readlines())

    def get_agent(self, action_space, observation):
        sleeper_agent = self.wake(observation)
        next_agent = sleeper_agent if sleeper_agent else self.birth(action_space, observation)

        return next_agent

    def birth(self, action_space, observation):
        knowledge = Knowledge()
        experience = Experience()

        class_map = {"DiffAgentSpeculative": DiffAgentSpeculative, "DiffAgent": DiffAgent,
                     "DiffAgentKnowledgeable": DiffAgentKnowledgeable, "AgentKnowledgeable": AgentKnowledgeable}
        agent = class_map[self.agent_class](experience, knowledge, action_space, observation)
        agent.name = random.choice(list(self.names))
        self.population[self.population.__len__()] = agent

        return agent

    def wake(self, observation):
        path = self.get_path()
        if os.path.exists(path):
            agent_paths = os.listdir(path)
            agent_paths.sort(reverse=True)
            for agent_path in agent_paths:
                with open(os.path.join(path, agent_path), 'rb') as f:
                    agent = pickle.load(f)
                agent.reset_behaviour(observation)
                self.population[self.population.__len__()] = agent
                return agent

    def sleep(self):
        path = self.get_path()
        if not os.path.exists(path):
            os.makedirs(path)

        for key, agent in self.population.items():
            agent.sleep()
            with open(os.path.join(path, agent.name + '.pcl'), 'wb') as f:
                pickle.dump(agent, f)

    def get_path(self):
        return os.path.join('rem', self.environment, self.name)
