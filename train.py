import subprocess
import os
from dotenv import load_dotenv
from pathlib import Path
import _pickle as pickle

load_dotenv(Path('.') / '.train')

environment = os.getenv("ENV")
world_name = os.getenv("WORLD")
lifetimes = int(os.getenv("LIFETIMES"))

command = "python ./run.py --config=.train"

population = 4
processes = {}

for lifetime in range(lifetimes):
    for i in range(population):
        processes[i] = subprocess.Popen(command, shell=True)

    done = False
    while not done:
        done = True
        for key in processes:
            done = done and processes[key].poll() is not None

    world_path = os.path.join('rem', environment, world_name)
    agent_paths = os.listdir(world_path)

    key = 0
    agents = {}
    min_rate = 1
    worst_agent = 0
    for path in agent_paths:
        dir_path = os.path.join(world_path, path)
        if not os.path.isfile(dir_path):
            children_paths = os.listdir(dir_path)
            for file_path in children_paths:
                file_path = os.path.join(dir_path, file_path)
                with open(file_path, 'rb') as f:
                    agent = pickle.load(f)
                agent_success = agent.experience.get_avg_success_rate()
                if agent_success < min_rate:
                    min_rate = agent_success
                    worst_agent = key
                agents[key] = agent
                key += 1
                os.remove(file_path)
    agents.pop(worst_agent, None)
    key, master_agent = agents.popitem()
    agents.pop(key, None)
    for key in agents:
        master_agent.knowledge = master_agent.knowledge + agent.knowledge
        master_agent.experience = master_agent.experience + agent.experience

    with open(os.path.join(world_path, master_agent.name + '.pcl'), 'wb') as f:
        pickle.dump(agent, f)

    print("Lifecycle done:" + str(lifetime))
