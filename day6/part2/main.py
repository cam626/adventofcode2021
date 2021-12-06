import argparse
import numpy as np
from tqdm import tqdm


def parse_file(filename):
    file = open(filename, "r")
    strTimers = file.read().strip("\n").split(",")
    return np.array([int(timer) for timer in strTimers])


def decreaseTimers(timers):
    timers -= 1


def spawnChildren(timers):
    numNewChildren = len(timers) - np.count_nonzero(timers)

    newChildren = np.ones(numNewChildren) * 9
    timers = np.append(timers, newChildren)
    
    return timers


def resetParents(timers):
    timers[np.where(timers == 0)] = 7


def simulate(timers, numDays):
    for day in tqdm(range(numDays)):
        timers = spawnChildren(timers)
        resetParents(timers)
        decreaseTimers(timers)
    return timers


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    timers = parse_file(args.filename)
    timers = simulate(timers, 256)
    print(len(timers))