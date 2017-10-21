import argparse, sys, subprocess, re

parser = argparse.ArgumentParser(description="Launches worlds")
parser.add_argument('--env', nargs="?", default="RepeatCopy-v0")
parser.add_argument('--agent_class', nargs="?", default="DiffAgentKnowledgeable")
parser.add_argument('--world', nargs="?", default="")
parser.add_argument('--sleep', nargs="?", default=0, type=float)
parser.add_argument('--episodes', nargs="?", default=100, type=int)
parser.add_argument('--agents', nargs="?", default=1, type=int)
parser.add_argument('--attempts', nargs="?", default=100, type=int)


args = parser.parse_args()

agents = args.agents
command = "python ./run.py " + re.sub('--agents=\d+',"",' '.join(sys.argv[1:]))

for i in range(agents):
    subprocess.Popen(command, shell=True)
