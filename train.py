import subprocess
import os
from dotenv import load_dotenv
from pathlib import Path
import time

load_dotenv(str(Path('.') / '.train'))

environment = os.getenv("ENV")
world_name = os.getenv("WORLD")
lifetimes = int(os.getenv("LIFETIMES"))

command = "python ./run.py --config=.train"

population = 1
processes = {}

for lifetime in range(lifetimes):
    for i in range(population):
        processes[i] = subprocess.Popen(command, shell=True)

    done = False
    while not done:
        time.sleep(1)
        done = True
        for key in processes:
            done = done and processes[key].poll() is not None

    print("Lifecycle done:" + str(lifetime))
