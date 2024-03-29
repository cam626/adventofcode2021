import argparse
import numpy as np

def fuelCost(crabPositions, position):
    d = np.abs(crabPositions - position)
    return np.sum(d * (d+1) / 2)


def findBestPosition(crabPositions):
    start = np.min(crabPositions)
    end = np.max(crabPositions)

    bestCost = float("inf")
    bestPosition = -1
    for i in range(start, end+1):
        c = fuelCost(crabPositions, i)
        
        if c < bestCost:
            bestCost = c
            bestPosition = i

    return bestPosition, bestCost


def parse_file(filename):
    file = open(filename, "r")
    strTimers = file.read().strip("\n").split(",")
    return np.array([int(timer) for timer in strTimers])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    crabPositions = parse_file(args.filename)
    bestPos, bestCost = findBestPosition(crabPositions)
    print("Best cost:", bestCost)