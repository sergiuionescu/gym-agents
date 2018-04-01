import gym
from gym import wrappers
import numpy as np
import os
import logging
import statsd
import argparse
import time
import tensorflow as tf

import worlds.World

parser = argparse.ArgumentParser(description="Launches worlds")
parser.add_argument('--env', nargs="?", default="Copy-v0")
parser.add_argument('--agent_class', nargs="?", default="AgentKnowledgeable")
parser.add_argument('--world', nargs="?", default="")
parser.add_argument('--sleep', nargs="?", default=0, type=float)
parser.add_argument('--episodes', nargs="?", default=200, type=int)
parser.add_argument('--attempts', nargs="?", default=100, type=int)
parser.add_argument('--render', nargs="?", default=1, type=int)

args = parser.parse_args()

environment = args.env
world_name = args.world
sleep = args.sleep
agent_class = args.agent_class
max_episodes = args.episodes
max_attempts = args.attempts
render = args.render
env = gym.make(environment)

statsd = statsd.StatsClient('localhost', 8125, prefix='agents', maxudpsize=1024)

gym.scoreboard.api_key = "sk_MXIkB1v6Shebbl5pMWtTA"
outdir = '/tmp/cem-agent-results'

env = wrappers.Monitor(env, outdir, force=True)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

np.random.seed(0)

observation = env.reset()
with tf.Session(config=tf.ConfigProto(device_count={'GPU': 0})) as sess:
    world = worlds.World.World(environment, agent_class)
    world.wake(world_name, observation)

    found = False

    agent = world.get_agent(env.action_space, observation)
    agent.set_session(sess)
    for episodes in range(max_episodes):
        agent.experience.reset_attempts()
        agent.reset_behaviour(observation)
        for t in range(max_attempts):
            time.sleep(sleep)
            action = agent.act(observation)
            new_observation, reward, done, info = env.step(action)
            if render and episodes % 50 == 0:
                env.render()
                time.sleep(2)

            agent.add_reward(observation, reward)
            observation = new_observation

            statsd.set(world.name + '.' + agent.name, agent.experience.total_reward)
            statsd.gauge(world.name + '.' + agent.name + '.' + 'success_rate', agent.experience.get_success_rate())
            statsd.gauge(world.name + '.' + agent.name + '.' + 'avg_success_rate',
                         agent.experience.get_avg_success_rate())

            if done:
                found = True
                print("Episode finished after {} timesteps".format(t + 1))
                break
        information = agent.knowledge.get_information(observation)
        print(str(episodes) + "-" + str(agent.experience.get_avg_success_rate()) + "/" + str(
            len(information.behaviour)))
        information.show_top_behaviour()
        if not found:
            break
        observation = env.reset()

agent.knowledge.show_summary()


def writefile(fname, s):
    with open(os.path.join(outdir, fname), 'w') as fh: fh.write(s)


env.close()
sess.close()

world.sleep()
