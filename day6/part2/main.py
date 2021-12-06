import argparse
import numpy as np
from tqdm import tqdm


class Timers():
    def __init__(self, timerList):
        self.timers = {}

        largestTimer = max(timerList)

        for element in range(10):
            self.timers[element] = 0

        for element in timerList:
            self.timers[element] += 1


    def simulate(self, numDays):
        for _ in tqdm(range(numDays)):
            # Spawn new children
            self.timers[9] = self.timers[0]

            # Move parents to new timer location
            self.timers[7] += self.timers[0]
            self.timers[0] = 0

            # Shift all timers down
            for i in range(0, 9):
                self.timers[i] = self.timers[i+1]

            self.timers[9] = 0

    
    def numTimers(self):
        s = 0
        for key in self.timers:
            s += self.timers[key]

        return s


def parse_file(filename):
    file = open(filename, "r")
    strTimers = file.read().strip("\n").split(",")
    return np.array([int(timer) for timer in strTimers])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    timers = parse_file(args.filename)
    t = Timers(timers)
    t.simulate(256)
    print(t.numTimers())