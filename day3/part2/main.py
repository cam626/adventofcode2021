import argparse
import numpy as np
from enum import Enum

class FilterCriteria(Enum):
    COMMON = 1
    UNCOMMON = 2


def parse_file(filename):
    file = open(filename, "r")
    lines = file.readlines()

    data = []
    for line in lines:
        numbers = list(line.strip("\n"))
        row = np.array(numbers, dtype=int)
        data.append(row)

    return np.array(data)


def binaryListToInt(arr):
    indices = np.flip(np.array(range(len(arr))))
    powers = 2**indices
    sumElements = np.where(arr == 1, powers, 0)

    return np.sum(sumElements)


def filter(data, columnIdx, criteria=FilterCriteria.COMMON):
    numOnes = np.count_nonzero(data[:, columnIdx])
    halfSize = np.size(data, 0) / 2
    
    if numOnes > halfSize:
        keepVal = (1 if criteria == FilterCriteria.COMMON else 0)
    elif numOnes < halfSize:
        keepVal = (0 if criteria == FilterCriteria.COMMON else 1)
    else:
        keepVal = 1 if criteria == FilterCriteria.COMMON else 0

    filteredData = data[np.where(data[:, columnIdx] == keepVal), :]
    return filteredData.squeeze(0)


def findRatingWithFilterType(data, filterType):
    filtered_data = data
    for columnIdx in range(np.size(data, 1)):
        if np.size(filtered_data, 0) == 1:
            return filtered_data
            
        filtered_data = filter(filtered_data, columnIdx, filterType)

    return filtered_data


def findOxygenGeneratorRating(data):
    return findRatingWithFilterType(data, FilterCriteria.COMMON)


def findCO2ScrubberRating(data):
    return findRatingWithFilterType(data, FilterCriteria.UNCOMMON)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    data = parse_file(args.filename)

    ogr = findOxygenGeneratorRating(data).squeeze()
    csr = findCO2ScrubberRating(data).squeeze()

    ogr_int = binaryListToInt(ogr)
    csr_int = binaryListToInt(csr)
    lifeSupportRating = ogr_int * csr_int
    print("The life support rating of the submarine is:", lifeSupportRating)