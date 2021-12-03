import argparse
import numpy as np

def parse_file(filename):
    file = open(filename, "r")
    lines = file.readlines()

    data = []
    for line in lines:
        numbers = list(line.strip("\n"))
        row = np.array(numbers, dtype=int)
        data.append(row)

    return np.array(data)


def getGammaRate(data):
    columnTotals = np.sum(data, axis=0)
    numRows = np.size(data, 0)
    return np.where(columnTotals > (numRows // 2), 1, 0)


def getEpsilonRate(data):
    columnTotals = np.sum(data, axis=0)
    numRows = np.size(data, 0)
    return np.where(columnTotals > (numRows // 2), 0, 1)


def binaryListToInt(arr):
    indices = np.flip(np.array(range(len(arr))))
    powers = 2**indices
    sumElements = np.where(arr == 1, powers, 0)

    return np.sum(sumElements)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    data = parse_file(args.filename)

    gammaRate = getGammaRate(data)
    epsilonRate = getEpsilonRate(data)

    powerConsumption = binaryListToInt(gammaRate) * binaryListToInt(epsilonRate)
    print("The submarine's power consumption is:", powerConsumption)