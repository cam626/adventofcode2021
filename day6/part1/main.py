import argparse


def parse_file(filename):
    file = open(filename, "r")
    strTimers = file.read().strip("\n").split(",")
    return [int(timer) for timer in strTimers]


def decreaseTimers(timers):
    for idx in range(len(timers)):
        timers[idx] -= 1


def spawnChildren(timers):
    for idx in range(len(timers)):
        if timers[idx] == 0:
            timers.append(9)


def resetParents(timers):
    for idx in range(len(timers)):
        if timers[idx] == 0:
            timers[idx] = 7


def simulate(timers, numDays):
    for day in range(numDays):
        spawnChildren(timers)
        resetParents(timers)
        decreaseTimers(timers)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    timers = parse_file(args.filename)
    simulate(timers, 80)
    print(len(timers))