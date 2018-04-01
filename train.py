import sys, subprocess, re

command = "python ./run.py --config=.train"

for i in range(4):
    subprocess.Popen(command, shell=True)
