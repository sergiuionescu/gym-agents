import gym
from gym import wrappers
import numpy as np
import json
import os
import logging
import statsd
import argparse
import time

from worlds import World


parser = argparse.ArgumentParser(description="Launches worlds")
parser.add_argument('--env', nargs="?", default="Copy-v0")
parser.add_argument('--world', nargs="?", default="")
parser.add_argument('--sleep', nargs="?", default=0, type=float)
args = parser.parse_args()

statsd = statsd.StatsClient('localhost', 8125, prefix='agents')

environment = args.env
world_name = args.world
sleep = args.sleep
env = gym.make(environment)

max_agents = 1
max_episodes = 100
max_attempts = 100

gym.scoreboard.api_key = "sk_MXIkB1v6Shebbl5pMWtTA"
outdir = '/tmp/cem-agent-results'

env = wrappers.Monitor(env, outdir, force=True)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

np.random.seed(0)

world = World(environment)
world.wake(world_name)

found = False
for agent_position in range(max_agents):
    observation = env.reset()
    agent = world.get_agent(agent_position, env.action_space)
    for episodes in range(max_episodes):
        agent.experience.reset_attempts()
        for t in range(max_attempts):
            time.sleep(sleep)
            action = agent.act(observation)
            observation, reward, done, info = env.step(action)
            env.render()

            if reward < 1:
                agent.random_prediction()

            agent.add_reward(reward)

            statsd.set(world.name + '.' + agent.name, agent.experience.total_reward)
            statsd.gauge(world.name + '.' + agent.name + '.' + 'success_rate', agent.experience.get_success_rate())
            statsd.gauge(world.name + '.' + agent.name + '.' + 'avg_success_rate', agent.experience.get_avg_success_rate())

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
#gym.upload(outdir)
