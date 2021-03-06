import gym
from gym import wrappers
import numpy as np
import os
import logging
import statsd
import argparse
import time
import tensorflow as tf
from dotenv import load_dotenv
from pathlib import Path

import worlds.World

parser = argparse.ArgumentParser(description="Launches worlds")
parser.add_argument('--config', nargs="?", default=".env")

args = parser.parse_args()
load_dotenv(str(Path('.') / args.config))

args = parser.parse_args()

environment = os.getenv("ENV")
agent_class = os.getenv("AGENT")
world_name = os.getenv("WORLD")
sleep = int(os.getenv("SLEEP"))
max_episodes = int(os.getenv("MAX_EPISODES"))
max_attempts = int(os.getenv("MAX_ATTEMPTS"))
render_each = int(os.getenv("RENDER_EACH"))
use_gpu = int(os.getenv("USE_GPU"))
save_agent = int(os.getenv("SAVE_AGENT"))
env = gym.make(environment)

statsd = statsd.StatsClient('graphite', 8125, prefix='agents', maxudpsize=1024)

gym.scoreboard.api_key = "sk_MXIkB1v6Shebbl5pMWtTA"
outdir = '/tmp/cem-agent-results'

env = wrappers.Monitor(env, outdir, force=True)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

np.random.seed(0)

observation = env.reset()
config = tf.ConfigProto() if use_gpu else tf.ConfigProto(device_count={'GPU': 0})
with tf.Session(config=config) as sess:
    world = worlds.World.World(environment, agent_class, world_name)

    found = False
    reward = 0

    agent = world.get_agent(env.action_space, observation)
    agent.set_session(sess)
    for episodes in range(max_episodes):
        agent.experience.reset_attempts()
        agent.reset(found and reward > 0)

        if found:
            statsd.set(environment + '.' + agent.name + '.' + 'success_rate', 1)
        else:
            statsd.set(environment + '.' + agent.name + '.' + 'episode', 1)
        found = False
        for t in range(max_attempts):
            action = agent.act(observation)
            new_observation, reward, done, info = env.step(action)
            if episodes % render_each == 0:
                env.render()
                time.sleep(sleep)

            agent.add_reward(observation, reward)
            observation = new_observation

            statsd.set(environment + '.' + agent.name, agent.experience.total_reward)
            statsd.gauge(environment + '.' + agent.name + '.' + 'avg_success_rate',
                         agent.experience.get_avg_success_rate())

            if done:
                found = True
                print("Episode finished after {} timesteps".format(t + 1))
                break
        if episodes % render_each == 0:
            information = agent.knowledge.get_information(observation)
            print(str(episodes) + "-" + str(agent.experience.get_avg_success_rate()) + "/" + str(
                len(information.behaviour)))
            information.show_top_behaviour()
        if not found:
            break
        observation = env.reset()

agent.knowledge.show_summary()


def writefile(fname, s):
    with open(os.path.join(outdir, fname), 'w') as fh:
        fh.write(s)


env.close()
sess.close()

if save_agent:
    world.sleep()
