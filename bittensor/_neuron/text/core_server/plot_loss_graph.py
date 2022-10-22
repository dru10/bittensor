import sys
import numpy as np
import matplotlib.pyplot as plt
import os

try:
    f = open(sys.argv[1], "r")
except IndexError:
    print("Usage: python make_graph.py {filename}")
    exit()
except FileNotFoundError:
    print("Argument is not a valid log file")
    exit()

losses = np.array(f.readline().split(), dtype=np.float32)
x = range(len(losses))

start = sys.argv[1].rfind('/')
end = sys.argv[1].rfind('.txt')
date = sys.argv[1][start+1:end] # Date at which model started, removed leading pathname and trailing '.txt'

plt.figure()
plt.plot(x, losses)
plt.title(f"Losses for model started at: {date}")
plt.ylabel("Loss")
plt.xlabel("Iteration")

try:
    plt.savefig(f"plots/{date}.jpg")
except FileNotFoundError:
    os.mkdir("plots")
    plt.savefig(f"plots/{date}.jpg")

print(f"Plot saved in plots/{date}.jpg")