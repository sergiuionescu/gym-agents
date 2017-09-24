import gym
from gym import wrappers
import numpy as np
import json
import os
import logging
import random
import cPickle as pickle
from agents import SpeculativeDiffAgent as Agent

environment = 'Copy-v0'
env = gym.make(environment)

max_agents = 10
max_episodes = 100
max_attempts = 100

gym.scoreboard.api_key = "sk_MXIkB1v6Shebbl5pMWtTA"
outdir = '/tmp/cem-agent-results'
env = wrappers.Monitor(env, outdir, force=True)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

np.random.seed(0)


class World(object):
    def __init__(self, environment):
        self.population = {}
        self.environment = environment

        with open(os.path.join('data', 'worlds.txt'), 'r') as f:
            data = f.readline()
            names = data.split(',')
            self.name = random.choice(names)

        with open(os.path.join('data', 'people.txt')) as f:
            self.names = map(lambda s: s.strip(), f.readlines())

    def birth(self, agent):
        agent.name = random.choice(self.names)
        self.population[self.population.__len__()] = agent

    def sleep(self):
        path = os.path.join('rem', self.environment, self.name)
        if not os.path.exists(path):
            os.makedirs(path)

        for key, agent in self.population.items():
            pickle.dump(agent, open(os.path.join(path, str(agent.total_reward) + '.' + agent.name + '.pcl'), 'w'))


world = World(environment)

found = False
for max_agents in range(max_agents):
    observation = env.reset()
    agent = Agent(env.action_space)
    world.birth(agent)
    for episodes in range(max_episodes):
        for t in range(max_attempts):
            action = agent.act(observation)
            observation, reward, done, info = env.step(action)
            env.render()
            if reward < 1:
                print("Agent was not selected  after {} timesteps".format(t + 1))
                break
            else:
                agent.total_reward += 1
            if done:
                found = True
                print("Episode finished after {} timesteps".format(t + 1))
                break
        if not found:
            break
        observation = env.reset()


def writefile(fname, s):
    with open(os.path.join(outdir, fname), 'w') as fh: fh.write(s)


writefile('info.json', json.dumps(info))

env.close()

world.sleep()

logger.info(
    "Successfully ran cross-entropy method. Now trying to upload results to the scoreboard. If it breaks, you can always just try re-uploading the same results.")
gym.upload(outdir)
